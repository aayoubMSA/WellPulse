#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path

from wellpulse.horizon import compute_recovery_horizon


def parse_utc(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError(f"timestamp lacks timezone: {value}")
    return dt.astimezone(timezone.utc)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def reconstruct_trial(root: Path) -> dict:
    summary = json.loads((root / "sender_summary.json").read_text(encoding="utf-8"))
    generated = read_csv(root / "telemetry_generated.csv")
    received = read_csv(root / "telemetry_received.csv")

    cutoff_text = str(summary.get("cohort_cutoff_utc") or "")
    queue_zero_text = str(summary.get("queue_pending_zero_utc") or "")
    if not cutoff_text or not queue_zero_text:
        return {"run_id": summary.get("run_id", root.name), "valid": False, "reason": "missing cutoff or queue-zero timestamp"}

    cutoff = parse_utc(cutoff_text)
    queue_zero = parse_utc(queue_zero_text)
    cohort: dict[str, str] = {}
    for row in generated:
        if parse_utc(row["generated_ts_utc"]) <= cutoff:
            rid = row["record_id"]
            if rid in cohort:
                return {"run_id": summary.get("run_id", root.name), "valid": False, "reason": f"duplicate generated record_id: {rid}"}
            cohort[rid] = row["payload_sha256"]

    if not cohort:
        return {"run_id": summary.get("run_id", root.name), "valid": False, "reason": "empty calibration cohort"}

    first_valid_receipt: dict[str, datetime] = {}
    duplicate_valid_attempts = 0
    checksum_mismatch_attempts = 0
    unexpected_attempts = 0
    for row in received:
        rid = row["record_id"]
        expected = cohort.get(rid)
        if expected is None:
            unexpected_attempts += 1
            continue
        if row["payload_sha256"] != expected:
            checksum_mismatch_attempts += 1
            continue
        ts = parse_utc(row["received_ts_utc"])
        if rid in first_valid_receipt:
            duplicate_valid_attempts += 1
            if ts < first_valid_receipt[rid]:
                first_valid_receipt[rid] = ts
        else:
            first_valid_receipt[rid] = ts

    missing = sorted(set(cohort) - set(first_valid_receipt))
    sender_status = str(summary.get("status", ""))
    valid_sender = sender_status == "QUEUE_DRAIN_OBSERVED_PENDING_SINK_RECONSTRUCTION"

    if missing:
        return {
            "run_id": summary.get("run_id", root.name),
            "valid": False,
            "reason": "pre-restoration cohort incomplete at sink",
            "missing_count": len(missing),
            "cohort_count": len(cohort),
            "sender_status": sender_status,
            "checksum_mismatch_attempts": checksum_mismatch_attempts,
            "unexpected_attempts": unexpected_attempts,
            "duplicate_valid_attempts": duplicate_valid_attempts,
        }
    if not valid_sender:
        return {
            "run_id": summary.get("run_id", root.name),
            "valid": False,
            "reason": "sender trial did not pass technical queue/Q0 gate",
            "sender_status": sender_status,
            "cohort_count": len(cohort),
        }

    sink_complete = max(first_valid_receipt.values())
    drain_complete = max(sink_complete, queue_zero)
    drain_s = (drain_complete - cutoff).total_seconds()
    if drain_s < 0:
        return {"run_id": summary.get("run_id", root.name), "valid": False, "reason": "negative drain time"}

    return {
        "run_id": summary.get("run_id", root.name),
        "valid": True,
        "cohort_count": len(cohort),
        "cohort_cutoff_utc": cutoff_text,
        "sink_cohort_complete_utc": sink_complete.isoformat(),
        "queue_pending_zero_utc": queue_zero_text,
        "backlog_drain_complete_utc": drain_complete.isoformat(),
        "backlog_drain_time_s": drain_s,
        "duplicate_valid_attempts": duplicate_valid_attempts,
        "checksum_mismatch_attempts": checksum_mismatch_attempts,
        "unexpected_attempts": unexpected_attempts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize WP-PWD01 non-scored H calibration")
    parser.add_argument("--trial-dir", action="append", required=True, help="Repeat exactly three times")
    parser.add_argument("--output-json", default="h_calibration_result.json")
    parser.add_argument("--output-md", default="h_calibration_result.md")
    args = parser.parse_args()

    trials = [reconstruct_trial(Path(p)) for p in args.trial_dir]
    valid = [t for t in trials if t.get("valid")]
    result = {
        "evidence_class": "NON_SCORED_WP2_H_CALIBRATION",
        "required_valid_trials": 3,
        "trials": trials,
        "scored_runs_authorized": False,
    }

    exit_code = 20
    if len(args.trial_dir) != 3:
        result["gate"] = "BLOCKED"
        result["reason"] = "exactly three calibration trial directories are required"
    elif len(valid) != 3:
        result["gate"] = "BLOCKED"
        result["reason"] = f"only {len(valid)}/3 valid calibration trials"
    else:
        horizon = compute_recovery_horizon(t["backlog_drain_time_s"] for t in valid)
        result["p95_estimator"] = "empirical_nearest_rank"
        result["p95_backlog_drain_s"] = horizon.p95_drain_s
        result["recovery_horizon_s"] = horizon.recovery_horizon_s
        result["stop_and_investigate"] = horizon.stop_and_investigate
        if horizon.stop_and_investigate:
            result["gate"] = "BLOCKED_H_GT_300"
            result["reason"] = "frozen H rule produced a value above 300 s; do not cap"
        else:
            result["gate"] = "PASS"
            result["reason"] = "three valid W1 trials reconstructed and H frozen deterministically"
            exit_code = 0

    Path(args.output_json).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md = [
        "# WP-PWD01 H Calibration Result",
        "",
        f"- Gate: **{result.get('gate', 'BLOCKED')}**",
        "- Evidence class: **NON-SCORED WP2 CALIBRATION**",
        "- Scored runs authorized: **NO**",
        f"- Valid trials: **{len(valid)}/3**",
    ]
    for trial in trials:
        if trial.get("valid"):
            md.append(f"- `{trial['run_id']}`: valid, backlog drain = **{trial['backlog_drain_time_s']:.3f} s**")
        else:
            md.append(f"- `{trial.get('run_id', 'unknown')}`: INVALID — {trial.get('reason', 'unknown reason')}")
    if "recovery_horizon_s" in result:
        md.extend([
            f"- p95 backlog drain: **{result['p95_backlog_drain_s']:.3f} s**",
            f"- Frozen H: **{result['recovery_horizon_s']} s**",
            f"- Stop/investigate: **{'YES' if result['stop_and_investigate'] else 'NO'}**",
        ])
    md.extend(["", f"Reason: {result.get('reason', '')}", ""])
    Path(args.output_md).write_text("\n".join(md), encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
