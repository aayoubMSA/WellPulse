#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from wellpulse.p7b_contract_v2 import load_contract


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_LOAD_FAIL:{path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser(description="P7B v2 contract-driven reconstruction + evidence completeness")
    ap.add_argument("--root", required=True, help="UE evidence root")
    ap.add_argument("--core-root", required=True)
    ap.add_argument("--contract", default="experiments/WP-PWD01/p7b-executable-contract-v2.json")
    args = ap.parse_args()

    ue_root = Path(args.root)
    core_root = Path(args.core_root)
    contract = load_contract(args.contract)
    legacy = contract.legacy_qualification_view()
    old = _load(ROOT / "scripts" / "reconstruct_wp2_p7b.py", "p7b_reconstruct_legacy")
    evidence = _load(ROOT / "scripts" / "wp2_p7b_evidence_gate_v2.py", "p7b_evidence_gate_v2")

    result = old.reconstruct(ue_root, legacy)
    old.write_report(result, ue_root / "analysis" / "p7b_reconstruction.json", ue_root / "analysis" / "p7b_reconstruction.md")
    evidence_result = evidence.evaluate(Path(args.contract), ue_root, core_root)
    result["evidence_contract_gate"] = evidence_result["gate"]
    result["evidence_contract_failures"] = evidence_result["failures"]
    result["executable_contract_schema"] = contract.raw["schema_version"]
    result["gate"] = "PASS" if not result["failures"] and evidence_result["gate"] == "PASS" else "FAIL"
    result["scored"] = False
    result["scored_runs_authorized"] = False
    old.write_report(result, ue_root / "analysis" / "p7b_reconstruction.json", ue_root / "analysis" / "p7b_reconstruction.md")
    (ue_root / "analysis" / "evidence_contract_gate.json").write_text(json.dumps(evidence_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("WP2_P7B_RECONSTRUCTION_V2=" + result["gate"])
    print("EVIDENCE_CONTRACT_GATE=" + evidence_result["gate"])
    print("SCORED_AUTHORIZATION=BLOCKED")
    return 0 if result["gate"] == "PASS" else 20


if __name__ == "__main__":
    raise SystemExit(main())
