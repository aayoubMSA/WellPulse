#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from wellpulse.p7b import load_contract
from wellpulse.p7b_runtime_compat import evaluate_readiness_v2


def main() -> int:
    ap = argparse.ArgumentParser(description="Fail-closed WP2-P7B readiness evaluator for target-runtime contract")
    ap.add_argument("--contract", required=True)
    ap.add_argument("--observation", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    contract = load_contract(args.contract)
    observation = json.loads(Path(args.observation).read_text(encoding="utf-8"))
    verdict = evaluate_readiness_v2(observation, contract).public_dict()
    verdict.update({
        "status": "CELL_READY_TO_START_NON_SCORED_QUALIFICATION" if verdict["gate"] == "PASS" else "CELL_NOT_STARTED_READINESS_FAIL",
        "scored": False,
        "powder_mutation_authorized_by_verdict": False,
        "attenuation_readback_claim": False,
    })
    Path(args.output).write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"P7B_CELL_READINESS_V2={verdict['gate']}")
    return 0 if verdict["gate"] == "PASS" else 20


if __name__ == "__main__":
    raise SystemExit(main())
