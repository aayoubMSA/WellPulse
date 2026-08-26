#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path

from wellpulse.horizon import compute_recovery_horizon


TECHNICALLY_INVALID = "TECHNICALLY_INVALID"
VALID_W1_RECOVERY_FAILURE = "VALID_W1_RECOVERY_FAILURE"
VALID_W1_RECOVERY_SUCCESS = "VALID_W1_RECOVERY_SUCCESS"


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


def technical_invalid(run_id: str, reason: str, **fields) -> dict:
    return {
        "run_id": run_id,
        "valid": False,
        "technical_validity": TECHNICALLY_INVALID,
        "calibration_outcome": TECHNICALLY_INVALID,
        "replacement_allowed": True,
        "reason": reason,
        **fields,
    }


def recovery_failure(run_id: str, reason: str, **fields) -> dict:
    return {
        "run_id": run_id,
        "valid": False,
        "technical_validity": "PASS",
        "calibration_outcome": VALID_W1_RECOVERY_FAILURE,
        "replacement_allowed": False,
        "reason": reason,
        **fields,
    }


def reconstruct_trial(root: Path) -> dict:
    summary = json.loads((root / "sender_summary.json").read_text(encoding="utf-8"))
    run_id = str(summary.get("run_id", root.name))
    generated = read_csv(root / "telemetry_generated.csv")
    received = read_csv(root / "telemetry_received.csv")

    sender_status = str(summary.get("status", ""))
    cutoff_text = str(summary.get("cohort_cutoff_utc") or "")
    queue_zero_text = str(summary.get("queue_pending_zero_utc") or "")

    if not cutoff_text:
        return technical_invalid(run_id, "missing cohort cutoff timestamp", sender_status=sender_status)

    if sender_status.startswith("INVALID_"):
        return technical_invalid(
            run_id,
            "sender reported a predefined technical failure",
            sender_status=sender_status,
        )

    cutoff = parse_utc(cutoff_text)
    cohort: dict[str, str] = {}
    for row in generated:
        if parse_utc(row["generated_ts_utc"]) <= cutoff:
            rid = row["record_id"]
            if rid in cohort:
                return technical_invalid(run_id, f"duplicate generated record_id: {rid}")
            cohort[rid] = row["payload_sha256"]

    if not cohort:
        return technical_invalid(run_id, "empty calibration cohort")

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

    # A correctly applied trial in which W1 does not recover is adverse scientific
    # evidence, not technical invalidity. Never replace it as an "invalid" run.
    if sender_status == "STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S":
        return recovery_failure(
            run_id,
            "technically valid W1 recovery exceeded the frozen H calibration bound",
            sender_status=sender_status,
            cohort_count=len(cohort),
            missing_count=len(missing),
            checksum_mismatch_attempts=checksum_mismatch_attempts,
            unexpected_attempts=unexpected_attempts,
            duplicate_valid_attempts=duplicate_valid_attempts,
        )

    if missing:
        return recovery_failure(
            run_id,
            "pre-restoration cohort remained incomplete at sink after a technically valid trial",
            sender_status=sender_status,
            missing_count=len(missing),
            cohort_count=len(cohort),
            checksum_mismatch_attempts=checksum_mismatch_attempts,
            unexpected_attempts=unexpected_attempts,
            duplicate_valid_attempts=duplicate_valid_attempts,
        )

    if not queue_zero_text:
        return recovery_failure(
            run_id,
            "W1 durable pending cohort did not reach zero after a technically valid trial",
            sender_status=sender_status,
            cohort_count=len(cohort),
            checksum_mismatch_attempts=checksum_mismatch_attempts,
            unexpected_attempts=unexpected_attempts,
            duplicate_valid_attempts=duplicate_valid_attempts,
        )

    if sender_status != "QUEUE_DRAIN_OBSERVED_PENDING_SINK_RECONSTRUCTION":
        return technical_invalid(
            run_id,
            "sender trial did not reach the expected technically valid completion state",
            sender_status=sender_status,
            cohort_count=len(cohort),
        )

    queue_zero = parse_utc(queue_zero_text)
    sink_complete = max(first_valid_receipt.values())
    drain_complete = max(sink_complete, queue_zero)
    drain_s = (drain_complete - cutoff).total_seconds()
    if drain_s < 0:
        return technical_invalid(run_id, "negative drain time")

    return {
        "run_id": run_id,
        "valid": True,
        "technical_validity": "PASS",
        "calibration_outcome": VALID_W1_RECOVERY_SUCCESS,
        "replacement_allowed": False,
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
    parser.add_argument(
        "--trial-dir",
        action="append",
        required=True,
        help="Provide every attempted calibration trial. Technical-invalid replacements may make this more than three directories.",
    )
    parser.add_argument("--output-json", default="h_calibration_result.json")
    parser.add_argument("--output-md", default="h_calibration_result.md")
    args = parser.parse_args()

    trials = [reconstruct_trial(Path(p)) for p in args.trial_dir]
    successful = [t for t in trials if t.get("calibration_outcome") == VALID_W1_RECOVERY_SUCCESS]
    technical_invalids = [t for t in trials if t.get("calibration_outcome") == TECHNICALLY_INVALID]
    recovery_failures = [t for t in trials if t.get("calibration_outcome") == VALID_W1_RECOVERY_FAILURE]

    result = {
        "evidence_class": "NON_SCORED_WP2_H_CALIBRATION",
        "required_successful_trials": 3,
        "trials": trials,
        "successful_trial_count": len(successful),
        "technical_invalid_count": len(technical_invalids),
        "valid_w1_recovery_failure_count": len(recovery_failures),
        "scored_runs_authorized": False,
    }

    exit_code = 20
    if recovery_failures:
        result["gate"] = "BLOCKED_VALID_W1_RECOVERY_FAILURE"
        result["reason"] = (
            "at least one technically valid calibration produced adverse W1 recovery evidence; "
            "do not replace it as invalid and do not freeze H"
        )
    elif len(successful) < 3:
        result["gate"] = "BLOCKED_NEED_TECHNICAL_REPLACEMENT"
        result["reason"] = (
            f"only {len(successful)}/3 successful calibration trials; predefined technical invalidity may be replaced"
        )
    elif len(successful) > 3:
        result["gate"] = "BLOCKED_PROTOCOL_DEVIATION"
        result["reason"] = "more than three successful calibration trials were supplied; H must use exactly three"
    else:
        horizon = compute_recovery_horizon(t["backlog_drain_time_s"] for t in successful)
        result["p95_estimator"] = "empirical_nearest_rank_n3_equals_maximum_observed"
        result["p95_backlog_drain_s"] = horizon.p95_drain_s
        result["recovery_horizon_s"] = horizon.recovery_horizon_s
        result["stop_and_investigate"] = horizon.stop_and_investigate
        if horizon.stop_and_investigate:
            result["gate"] = "BLOCKED_H_GT_300"
            result["reason"] = "frozen H rule produced a value above 300 s; do not cap"
        else:
            result["gate"] = "PASS"
            result["reason"] = "three technically valid W1 recovery-success trials reconstructed and H frozen deterministically"
            exit_code = 0

    Path(args.output_json).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md = [
        "# WP-PWD01 H Calibration Result",
        "",
        f"- Gate: **{result.get('gate', 'BLOCKED')}**",
        "- Evidence class: **NON-SCORED WP2 CALIBRATION**",
        "- Scored runs authorized: **NO**",
        f"- Successful recovery trials: **{len(successful)}/3**",
        f"- Technical-invalid attempts: **{len(technical_invalids)}**",
        f"- Valid adverse W1 recovery outcomes: **{len(recovery_failures)}**",
    ]
    for trial in trials:
        outcome = trial.get("calibration_outcome", "UNKNOWN")
        if outcome == VALID_W1_RECOVERY_SUCCESS:
            md.append(
                f"- `{trial['run_id']}`: {outcome}, backlog drain = **{trial['backlog_drain_time_s']:.3f} s**"
            )
        else:
            md.append(
                f"- `{trial.get('run_id', 'unknown')}`: {outcome} — {trial.get('reason', 'unknown reason')}"
            )
    if "recovery_horizon_s" in result:
        md.extend([
            f"- n=3 nearest-rank value (maximum observed drain): **{result['p95_backlog_drain_s']:.3f} s**",
            f"- Frozen H: **{result['recovery_horizon_s']} s**",
            f"- Stop/investigate: **{'YES' if result['stop_and_investigate'] else 'NO'}**",
        ])
    md.extend(["", f"Reason: {result.get('reason', '')}", ""])
    Path(args.output_md).write_text("\n".join(md), encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
