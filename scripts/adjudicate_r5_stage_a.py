#!/usr/bin/env python3
"""Aggregate exactly three WellPulse R5 Stage-A T1 run verdicts.

This script never executes experiments and never discards a valid outcome.
Invalid attempts make Stage A incomplete rather than triggering automatic
replacement or favorable-run selection.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def adjudicate(runs: list[dict[str, Any]]) -> dict[str, Any]:
    if len(runs) != 3:
        raise ValueError("Stage A requires exactly three planned run verdicts")

    run_ids = [str(r.get("run_id")) for r in runs]
    if len(set(run_ids)) != 3:
        raise ValueError("Stage A run_id values must be unique")

    invalid = [r for r in runs if not bool(r.get("valid"))]
    positive = [r for r in runs if bool(r.get("positive_for_stage_rule"))]

    classes: dict[str, int] = {}
    for r in runs:
        cls = str(r.get("primary_class"))
        classes[cls] = classes.get(cls, 0) + 1

    if invalid:
        decision = "STAGE_A_INCOMPLETE_INVALID_RUN"
        stage_complete = False
        next_action = (
            "Do not adjudicate C6. Preserve all three attempts. Any replacement "
            "for an objectively INVALID attempt requires a separately authorized "
            "replacement run; no automatic retry is permitted."
        )
    else:
        stage_complete = True
        npos = len(positive)
        if npos >= 2:
            decision = "CONFIRM_REPEAT_OCCURRENCE_STOP"
            next_action = (
                "Stop Stage A. C6 may be elevated only to repeated experimental "
                "occurrence under the tested W1 conditions; no prevalence or "
                "population-frequency claim is permitted."
            )
        elif npos == 0:
            decision = "NOT_CONFIRMED_STOP"
            next_action = (
                "Stop. The central repeated-occurrence claim is not confirmed "
                "under Stage A. Retain individual bounded phenomena without "
                "upgrading C6."
            )
        else:
            decision = "STAGE_B_REQUIRED_TWO_ADDITIONAL_VALID_RUNS"
            next_action = (
                "Execute exactly two additional independently executed VALID T1 "
                "runs under the identical frozen protocol; total valid-run cap=5."
            )

    return {
        "stage": "R5_STAGE_A",
        "planned_valid_runs": 3,
        "observed_verdict_files": 3,
        "run_ids": run_ids,
        "all_runs_valid": not invalid,
        "invalid_run_ids": [str(r.get("run_id")) for r in invalid],
        "positive_run_count": len(positive),
        "positive_run_ids": [str(r.get("run_id")) for r in positive],
        "primary_class_counts": classes,
        "decision": decision,
        "stage_complete": stage_complete,
        "next_action": next_action,
        "claim_ceiling": (
            "No prevalence, probability, reliability-rate, or population "
            "frequency inference. Exact run outcomes must be reported."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-analysis", action="append", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    if len(args.run_analysis) != 3:
        raise SystemExit("--run-analysis must be supplied exactly three times")

    runs = [load(Path(p)) for p in args.run_analysis]
    result = adjudicate(runs)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["stage_complete"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
