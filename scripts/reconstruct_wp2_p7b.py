#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from wellpulse.p7b import (
    compare_b1_w1_manifests,
    evaluate_b1_pre_restart,
    evaluate_readiness,
    evaluate_restart_proof,
    load_contract,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def proof_flags(proof: dict[str, Any], required: tuple[str, ...]) -> list[str]:
    return [field for field in required if proof.get(field) is not True]


def reconstruct(root: Path, contract: dict[str, Any]) -> dict[str, Any]:
    cells_root = root / "cells"
    result: dict[str, Any] = {
        "schema_version": "wp2-p7b-reconstruction-v1",
        "evidence_class": "NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION",
        "scored": False,
        "scored_runs_authorized": False,
        "cells": {},
        "failures": [],
    }

    manifests = {}
    for cell in contract["cells"]:
        cell_id = cell["id"]
        architecture = cell["architecture"]
        cell_root = cells_root / cell_id
        failures: list[str] = []

        readiness = load_json(cell_root / "readiness_observation.json")
        readiness_gate = evaluate_readiness(readiness, contract)
        failures.extend(f"READINESS:{x}" for x in readiness_gate.failures)

        restart = load_json(cell_root / "restart_proof.json")
        restart_gate = evaluate_restart_proof(restart)
        failures.extend(f"RESTART:{x}" for x in restart_gate.failures)

        manifest = load_json(cell_root / "runtime_manifest.json")
        manifests[architecture] = manifest

        if architecture == "B1_MQTT_QOS1":
            events = load_jsonl(cell_root / "mqtt_events.jsonl")
            snapshot = load_json(cell_root / "pre_restart_transport_snapshot.json")
            b1_gate = evaluate_b1_pre_restart(events, snapshot)
            failures.extend(f"B1:{x}" for x in b1_gate.failures)
        elif architecture == "W1_OFFLINE_FIRST":
            proof = load_json(cell_root / "w1_durability_proof.json")
            missing = proof_flags(
                proof,
                (
                    "generator_alive_during_restart",
                    "source_sequence_continuity",
                    "sqlite_wal",
                    "sqlite_synchronous_full",
                    "queue_path_survived_restart",
                    "pending_pre_restart_record_reconstructible_after_restart",
                    "same_queue_reopened",
                ),
            )
            failures.extend(f"W1:{x}" for x in missing)
        elif architecture == "B2_MQTT_DURABLE_CLIENT":
            proof = load_json(cell_root / "b2_durability_proof.json")
            required_sha = contract["b2_runtime"]["jar_sha256"]
            if proof.get("jar_sha256") != required_sha:
                failures.append("B2:JAR_SHA256")
            missing = proof_flags(
                proof,
                (
                    "exact_java_config",
                    "tun_srsue_tls_path",
                    "same_payload_and_evidence_schema",
                    "persisted_record_before_process_destruction",
                    "same_persistence_directory_reopened",
                    "same_intra_run_client_identity",
                    "pre_restart_record_set_present_after_restart",
                    "buffer_drained_by_fixed_horizon",
                ),
            )
            failures.extend(f"B2:{x}" for x in missing)

        result["cells"][cell_id] = {
            "architecture": architecture,
            "gate": "PASS" if not failures else "FAIL",
            "failures": failures,
        }
        result["failures"].extend(f"{cell_id}:{x}" for x in failures)

    match = compare_b1_w1_manifests(
        manifests["B1_MQTT_QOS1"], manifests["W1_OFFLINE_FIRST"]
    )
    result["b1_w1_match"] = match.public_dict()
    result["failures"].extend(f"B1_W1_MATCH:{x}" for x in match.failures)
    result["gate"] = "PASS" if not result["failures"] else "FAIL"
    result["claim_boundary"] = (
        "qualification mechanics only; no cross-cell scientific comparison"
    )
    return result


def write_report(result: dict[str, Any], output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# WP2-P7B qualification reconstruction",
        "",
        f"- Gate: **{result['gate']}**",
        "- Evidence class: **NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION**",
        "- Scored authorization: **UNCHANGED / BLOCKED**",
        "",
        "## Cells",
        "",
        "| Cell | Architecture | Gate |",
        "|---|---|---|",
    ]
    for cell_id, cell in result["cells"].items():
        lines.append(f"| {cell_id} | {cell['architecture']} | {cell['gate']} |")
    lines.extend(["", "## Failures", ""])
    if result["failures"]:
        lines.extend(f"- {failure}" for failure in result["failures"])
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "This report qualifies mechanics only and may not be used as scored evidence.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Reconstruct WP2-P7B non-scored qualification")
    ap.add_argument("--root", required=True)
    ap.add_argument(
        "--contract",
        default="experiments/WP-PWD01/p7b-qualification-contract.json",
    )
    args = ap.parse_args()
    root = Path(args.root)
    contract = load_contract(args.contract)
    result = reconstruct(root, contract)
    write_report(
        result,
        root / "analysis" / "p7b_reconstruction.json",
        root / "analysis" / "p7b_reconstruction.md",
    )
    print(f"WP2_P7B_RECONSTRUCTION={result['gate']}")
    print("SCORED_AUTHORIZATION=BLOCKED")
    return 0 if result["gate"] == "PASS" else 20


if __name__ == "__main__":
    raise SystemExit(main())
