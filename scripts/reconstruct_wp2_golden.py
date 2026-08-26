#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import sys


def dt(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    out = datetime.fromisoformat(text)
    if out.tzinfo is None:
        raise ValueError(f"timestamp lacks timezone: {value}")
    return out.astimezone(timezone.utc)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def find_service_ready(path: Path) -> datetime:
    pat = re.compile(r"^T_SERVICE_READY=(.+)$")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = pat.match(line.strip())
        if m:
            return dt(m.group(1))
    raise ValueError("T_SERVICE_READY missing from service_ready_probe.txt")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Reconstruct WP2 Golden E2E endpoint from escrowed raw evidence")
    ap.add_argument("--root", required=True, help="Escrow root containing sender/, receiver/, substrate/")
    ap.add_argument("--output-json", default=None)
    ap.add_argument("--output-md", default=None)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    gen_path = root / "sender" / "telemetry_generated.csv"
    rx_path = root / "receiver" / "telemetry_received.csv"
    att_path = root / "sender" / "attenuation_timeline.csv"
    service_path = root / "substrate" / "service_ready_probe.txt"

    for p in (gen_path, rx_path, att_path, service_path):
        if not p.is_file() or p.stat().st_size == 0:
            raise SystemExit(f"GOLDEN_RECONSTRUCTION=FAIL_MISSING {p}")

    att = rows(att_path)
    q0_restores = [r for r in att if str(r.get("programmed_attenuation_db", "")).strip() == "0"]
    if not q0_restores:
        raise SystemExit("GOLDEN_RECONSTRUCTION=FAIL_NO_Q0_RESTORE")
    # Golden schedule may contain an initial Q0 command; the final Q0 transition is the treatment endpoint.
    final_q0 = q0_restores[-1]
    t_rf_restore = dt(final_q0["command_end_utc"])
    t_service_ready = find_service_ready(service_path)
    if t_service_ready < t_rf_restore:
        raise SystemExit("GOLDEN_RECONSTRUCTION=FAIL_SERVICE_BEFORE_RF_RESTORE")
    horizon_end = t_service_ready + timedelta(seconds=300)

    generated = rows(gen_path)
    received = rows(rx_path)

    cohort: dict[str, str] = {}
    duplicate_generated: list[str] = []
    for r in generated:
        if dt(r["generated_ts_utc"]) <= t_rf_restore:
            rid = r["record_id"]
            if rid in cohort:
                duplicate_generated.append(rid)
            cohort[rid] = r["payload_sha256"]
    if not cohort or duplicate_generated:
        raise SystemExit("GOLDEN_RECONSTRUCTION=FAIL_GENERATED_COHORT")

    first_valid: dict[str, datetime] = {}
    duplicate_valid = 0
    checksum_mismatch = 0
    unexpected = 0
    late_valid = 0
    for r in received:
        rid = r["record_id"]
        expected = cohort.get(rid)
        if expected is None:
            unexpected += 1
            continue
        if r["payload_sha256"] != expected:
            checksum_mismatch += 1
            continue
        rx_time = dt(r["received_ts_utc"])
        if rid in first_valid:
            duplicate_valid += 1
            if rx_time < first_valid[rid]:
                first_valid[rid] = rx_time
        else:
            first_valid[rid] = rx_time
        if rx_time > horizon_end:
            late_valid += 1

    received_by_h = {rid: when for rid, when in first_valid.items() if when <= horizon_end}
    missing_by_h = sorted(set(cohort) - set(received_by_h))
    completeness = len(received_by_h) / len(cohort)

    t_app_complete = None
    if set(first_valid) >= set(cohort):
        candidate = max(first_valid[rid] for rid in cohort)
        if candidate <= horizon_end:
            t_app_complete = candidate

    t_service = (t_service_ready - t_rf_restore).total_seconds()
    t_app = (t_app_complete - t_service_ready).total_seconds() if t_app_complete else None
    t_total = (t_app_complete - t_rf_restore).total_seconds() if t_app_complete else None

    result = {
        "evidence_class": "NON_SCORED_WP2_GOLDEN_REHEARSAL",
        "root": str(root),
        "t_rf_restore": t_rf_restore.isoformat(),
        "t_service_ready": t_service_ready.isoformat(),
        "h_app_s": 300,
        "horizon_end_utc": horizon_end.isoformat(),
        "primary_cohort_count": len(cohort),
        "received_valid_by_horizon": len(received_by_h),
        "completeness_300": completeness,
        "missing_by_horizon_count": len(missing_by_h),
        "missing_record_ids": missing_by_h,
        "duplicate_valid_attempts": duplicate_valid,
        "checksum_mismatch_attempts": checksum_mismatch,
        "unexpected_attempts": unexpected,
        "late_valid_attempts": late_valid,
        "t_app_complete": t_app_complete.isoformat() if t_app_complete else None,
        "T_service_s": t_service,
        "T_app_s": t_app,
        "T_total_s": t_total,
        "input_sha256": {
            "telemetry_generated.csv": sha256(gen_path),
            "telemetry_received.csv": sha256(rx_path),
            "attenuation_timeline.csv": sha256(att_path),
            "service_ready_probe.txt": sha256(service_path),
        },
        "golden_scientific_outcome_is_scored": False,
        "reconstruction_gate": "PASS",
    }

    out_json = Path(args.output_json) if args.output_json else root / "analysis" / "golden_reconstruction.json"
    out_md = Path(args.output_md) if args.output_md else root / "analysis" / "golden_reconstruction.md"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    out_md.write_text(
        "# WP2 Golden Reconstruction\n\n"
        f"- Gate: **PASS**\n"
        f"- t_rf_restore: `{result['t_rf_restore']}`\n"
        f"- t_service_ready: `{result['t_service_ready']}`\n"
        f"- T_service: **{t_service:.3f} s**\n"
        f"- Primary cohort: **{len(cohort)}**\n"
        f"- Valid by 300 s horizon: **{len(received_by_h)}/{len(cohort)}**\n"
        f"- completeness_300: **{100*completeness:.3f}%**\n"
        f"- Missing by horizon: **{len(missing_by_h)}**\n"
        f"- Checksum mismatches: **{checksum_mismatch}**\n"
        f"- Duplicate valid attempts: **{duplicate_valid}**\n"
        f"- t_app_complete: `{result['t_app_complete']}`\n"
        f"- T_app: `{t_app}` s\n"
        f"- T_total: `{t_total}` s\n\n"
        "This is a non-scored Golden rehearsal reconstruction; application outcome direction does not determine Golden readiness.\n",
        encoding="utf-8",
    )
    print(f"GOLDEN_RECONSTRUCTION_JSON={out_json}")
    print(f"GOLDEN_RECONSTRUCTION_MD={out_md}")
    print("WP2_GOLDEN_RECONSTRUCTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
