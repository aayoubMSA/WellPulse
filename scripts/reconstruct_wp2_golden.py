#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re


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


def find_rf_restore(root: Path, att: list[dict[str, str]]) -> datetime:
    """Return the prospectively emitted physical Q3->Q0 restoration clock.

    The sender writes ``sender/rf_restore.ready`` immediately after the actual
    treatment-ending Q3->Q0 command. A later fail-safe cleanup also commands Q0,
    so selecting the *last* Q0 row from attenuation_timeline.csv is invalid.
    The marker is therefore authoritative and is cross-checked against an exact
    Q0 command-end timestamp in the immutable attenuation timeline.
    """
    marker = root / "sender" / "rf_restore.ready"
    if not marker.is_file() or marker.stat().st_size == 0:
        raise SystemExit(f"GOLDEN_RECONSTRUCTION=FAIL_MISSING {marker}")
    marker_text = marker.read_text(encoding="utf-8").strip()
    t_rf_restore = dt(marker_text)

    matching_q0 = []
    for row in att:
        if str(row.get("programmed_attenuation_db", "")).strip() != "0":
            continue
        end_text = str(row.get("command_end_utc", "")).strip()
        if not end_text:
            continue
        if dt(end_text) == t_rf_restore:
            matching_q0.append(row)
    if len(matching_q0) != 1:
        raise SystemExit(
            f"GOLDEN_RECONSTRUCTION=FAIL_RF_RESTORE_TIMELINE_MATCH count={len(matching_q0)}"
        )
    return t_rf_restore


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
    rf_restore_path = root / "sender" / "rf_restore.ready"
    service_path = root / "substrate" / "service_ready_probe.txt"

    for p in (gen_path, rx_path, att_path, rf_restore_path, service_path):
        if not p.is_file() or p.stat().st_size == 0:
            raise SystemExit(f"GOLDEN_RECONSTRUCTION=FAIL_MISSING {p}")

    att = rows(att_path)
    if not att:
        raise SystemExit("GOLDEN_RECONSTRUCTION=FAIL_EMPTY_ATTENUATION_TIMELINE")
    t_rf_restore = find_rf_restore(root, att)
    t_service_ready = find_service_ready(service_path)
    if t_service_ready < t_rf_restore:
        raise SystemExit("GOLDEN_RECONSTRUCTION=FAIL_SERVICE_BEFORE_RF_RESTORE")
    horizon_end = t_service_ready + timedelta(seconds=300)

    generated = rows(gen_path)
    received = rows(rx_path)

    generated_all: dict[str, tuple[datetime, str]] = {}
    duplicate_generated: list[str] = []
    for r in generated:
        rid = r["record_id"]
        if rid in generated_all:
            duplicate_generated.append(rid)
            continue
        generated_all[rid] = (dt(r["generated_ts_utc"]), r["payload_sha256"])
    if not generated_all or duplicate_generated:
        raise SystemExit("GOLDEN_RECONSTRUCTION=FAIL_GENERATED_RECORD_IDENTITY")

    cohort = {
        rid: digest
        for rid, (generated_at, digest) in generated_all.items()
        if generated_at <= t_rf_restore
    }
    post_cohort = {
        rid: digest
        for rid, (generated_at, digest) in generated_all.items()
        if generated_at > t_rf_restore
    }
    if not cohort:
        raise SystemExit("GOLDEN_RECONSTRUCTION=FAIL_GENERATED_COHORT")

    first_valid: dict[str, datetime] = {}
    duplicate_valid = 0
    checksum_mismatch = 0
    unexpected = 0
    unexpected_record_ids: set[str] = set()
    post_cohort_valid = 0
    post_cohort_checksum_mismatch = 0
    late_valid = 0

    for r in received:
        rid = r["record_id"]
        expected = cohort.get(rid)
        if expected is None:
            post_expected = post_cohort.get(rid)
            if post_expected is None:
                unexpected += 1
                unexpected_record_ids.add(rid)
            elif r["payload_sha256"] == post_expected:
                post_cohort_valid += 1
            else:
                post_cohort_checksum_mismatch += 1
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
        "t_rf_restore_authority": "sender/rf_restore.ready_crosschecked_to_attenuation_timeline",
        "t_service_ready": t_service_ready.isoformat(),
        "h_app_s": 300,
        "horizon_end_utc": horizon_end.isoformat(),
        "primary_cohort_count": len(cohort),
        "post_cohort_generated_count": len(post_cohort),
        "received_valid_by_horizon": len(received_by_h),
        "completeness_300": completeness,
        "missing_by_horizon_count": len(missing_by_h),
        "missing_record_ids": missing_by_h,
        "duplicate_valid_attempts": duplicate_valid,
        "checksum_mismatch_attempts": checksum_mismatch,
        "post_cohort_valid_attempts": post_cohort_valid,
        "post_cohort_checksum_mismatch_attempts": post_cohort_checksum_mismatch,
        "unexpected_attempts": unexpected,
        "unexpected_record_ids": sorted(unexpected_record_ids),
        "late_valid_attempts": late_valid,
        "t_app_complete": t_app_complete.isoformat() if t_app_complete else None,
        "T_service_s": t_service,
        "T_app_s": t_app,
        "T_total_s": t_total,
        "input_sha256": {
            "telemetry_generated.csv": sha256(gen_path),
            "telemetry_received.csv": sha256(rx_path),
            "attenuation_timeline.csv": sha256(att_path),
            "rf_restore.ready": sha256(rf_restore_path),
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
        "- t_rf_restore authority: `sender/rf_restore.ready` cross-checked to attenuation timeline\n"
        f"- t_service_ready: `{result['t_service_ready']}`\n"
        f"- T_service: **{t_service:.3f} s**\n"
        f"- Primary cohort: **{len(cohort)}**\n"
        f"- Post-cohort generated records: **{len(post_cohort)}**\n"
        f"- Valid by 300 s horizon: **{len(received_by_h)}/{len(cohort)}**\n"
        f"- completeness_300: **{100*completeness:.3f}%**\n"
        f"- Missing by horizon: **{len(missing_by_h)}**\n"
        f"- Checksum mismatches (primary cohort): **{checksum_mismatch}**\n"
        f"- Duplicate valid attempts (primary cohort): **{duplicate_valid}**\n"
        f"- Planned post-cohort valid attempts: **{post_cohort_valid}**\n"
        f"- Planned post-cohort checksum mismatches: **{post_cohort_checksum_mismatch}**\n"
        f"- Truly unexpected attempts: **{unexpected}**\n"
        f"- t_app_complete: `{result['t_app_complete']}`\n"
        f"- T_app: `{t_app}` s\n"
        f"- T_total: `{t_total}` s\n\n"
        "Post-cohort traffic is generated intentionally after t_rf_restore and is excluded from the primary denominator; it is not classified as unexpected merely because it is outside the primary cohort.\n\n"
        "This is a non-scored Golden rehearsal reconstruction; application outcome direction does not determine Golden readiness.\n",
        encoding="utf-8",
    )
    print(f"GOLDEN_RECONSTRUCTION_JSON={out_json}")
    print(f"GOLDEN_RECONSTRUCTION_MD={out_md}")
    print("WP2_GOLDEN_RECONSTRUCTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
