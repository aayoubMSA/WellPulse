#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


def validate_controller_text(text: str, contract: dict) -> list[str]:
    failures: list[str] = []
    accepted = contract["future_controller_acceptance"]
    execution = contract["execution_lock"]

    create_token = "portal-cli experiment create"
    terminate_token = "portal-cli experiment terminate"
    required_entrypoint = accepted["required_node_entrypoint"]
    legacy_entrypoint = execution["legacy_node_entrypoint_prohibited"]
    authority_marker = accepted["required_authority_marker"]
    preservation_helper = accepted["required_preservation_helper"]

    if text.count(create_token) != int(accepted["exact_reservation_create_count"]):
        failures.append("RESERVATION_CREATE_COUNT")
    if required_entrypoint not in text:
        failures.append("REPAIRED_NODE_ENTRYPOINT_MISSING")
    legacy_pattern = re.compile(r"scripts/wp2_p7b_c_node\.py(?:\s|['\";]|$)")
    if legacy_pattern.search(text):
        failures.append("LEGACY_NODE_ENTRYPOINT_PRESENT")
    if authority_marker not in text:
        failures.append("REPLACEMENT_AUTHORITY_MARKER_MISSING")
    if preservation_helper not in text:
        failures.append("PRESERVATION_HELPER_MISSING")

    forbidden_scored = (
        "scored_runs_authorized=true",
        '"scored_runs_authorized": true',
        "SCORED_AUTHORIZATION=PASS",
    )
    if any(token in text for token in forbidden_scored):
        failures.append("SCORED_AUTHORITY_PRESENT")

    for marker, code in (
        ("AUTOMATIC_RETRY=NO", "AUTOMATIC_RETRY_GUARD_MISSING"),
        ("SECOND_REPLACEMENT=NO", "SECOND_REPLACEMENT_GUARD_MISSING"),
        ("EVIDENCE_ESCROW_GATE=PASS", "EVIDENCE_ESCROW_GATE_MISSING"),
        ("CONTROLLER_OFFPOWDER_GATE=PASS", "OFFPOWDER_GATE_MISSING"),
        ("TEARDOWN_AUTHORIZED=YES", "TEARDOWN_AUTHORITY_MARKER_MISSING"),
    ):
        if marker not in text:
            failures.append(code)

    if text.count(terminate_token) != 1:
        failures.append("TERMINATE_COUNT")
    else:
        terminate_at = text.index(terminate_token)
        for marker, code in (
            ("EVIDENCE_ESCROW_GATE=PASS", "EVIDENCE_GATE_NOT_BEFORE_TERMINATE"),
            ("CONTROLLER_OFFPOWDER_GATE=PASS", "OFFPOWDER_GATE_NOT_BEFORE_TERMINATE"),
            ("TEARDOWN_AUTHORIZED=YES", "TEARDOWN_AUTHORITY_NOT_BEFORE_TERMINATE"),
        ):
            if marker in text and text.index(marker) > terminate_at:
                failures.append(code)

    if "P7B_R1_DIAGNOSTICS_BEGIN" not in text and "wp2_p7b_c_node_r1.py" not in text:
        failures.append("BOUNDED_DIAGNOSTICS_CONTRACT_MISSING")

    return failures


def main() -> int:
    ap = argparse.ArgumentParser(description="Static acceptance gate for a future P7B-RQ1 authority-bearing controller")
    ap.add_argument("--controller", required=True)
    ap.add_argument(
        "--contract",
        default="experiments/WP-PWD01/p7b-requalification-r2-contract.json",
    )
    args = ap.parse_args()
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    if contract.get("schema_version") != "wp2-p7b-r2-requalification-contract-v1":
        raise ValueError("unsupported R2 contract schema")
    if contract.get("live_authorized") is not False or contract.get("scored_runs_authorized") is not False:
        raise ValueError("R2 contract must remain offline and non-scored")
    text = Path(args.controller).read_text(encoding="utf-8")
    failures = validate_controller_text(text, contract)
    print("P7B_R2_CONTROLLER_STATIC_GATE=" + ("PASS" if not failures else "FAIL"))
    for failure in failures:
        print("FAILURE=" + failure)
    print("LIVE_AUTHORIZATION=BLOCKED")
    print("SCORED_AUTHORIZATION=BLOCKED")
    return 0 if not failures else 20


if __name__ == "__main__":
    raise SystemExit(main())
