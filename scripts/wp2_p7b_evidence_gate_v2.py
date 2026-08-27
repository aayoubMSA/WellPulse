#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.p7b_contract_v2 import load_contract


def _split(spec: str) -> tuple[str, str]:
    owner, rel = spec.split(":", 1)
    if owner not in {"ue", "core"}:
        raise ValueError(f"unknown evidence owner: {owner}")
    return owner, rel


def _path(spec: str, roots: dict[str, Path], cell: str | None = None) -> Path:
    owner, rel = _split(spec)
    if cell is not None:
        rel = rel.format(cell=cell)
    return roots[owner] / rel


def evaluate(contract_path: Path, ue_root: Path, core_root: Path) -> dict:
    contract = load_contract(contract_path)
    roots = {"ue": ue_root.resolve(), "core": core_root.resolve()}
    failures: list[str] = []
    checked: list[str] = []

    for owner, root in roots.items():
        if not root.is_absolute():
            failures.append(f"ROOT_NOT_ABSOLUTE:{owner}:{root}")
        if "$HOME" in str(root) or "~" in str(root):
            failures.append(f"ROOT_UNRESOLVED_TOKEN:{owner}:{root}")

    layout = contract.raw["evidence_layout"]

    def require_nonempty(spec: str, *, cell: str | None = None) -> None:
        p = _path(spec, roots, cell)
        checked.append(str(p))
        if not p.is_file() or p.stat().st_size <= 0:
            failures.append(f"REQUIRED_NONEMPTY_MISSING:{p}")

    def require_exists(spec: str, *, cell: str | None = None) -> None:
        p = _path(spec, roots, cell)
        checked.append(str(p))
        if not p.exists():
            failures.append(f"REQUIRED_EXISTS_MISSING:{p}")

    for spec in layout["reservation_required_nonempty"]:
        require_nonempty(spec)
    for cell in contract.cell_sequence:
        for spec in layout["per_cell_required_nonempty"]:
            require_nonempty(spec, cell=cell)
        for spec in layout["per_cell_required_exists"]:
            require_exists(spec, cell=cell)
        for spec in layout["architecture_required_nonempty"].get(cell, []):
            require_nonempty(spec)

    status_path = ue_root / "p7b_c_status.json"
    if status_path.is_file():
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
            if status.get("gate") != "PASS_PHYSICAL_CELLS":
                failures.append("STATUS_GATE_NOT_PASS_PHYSICAL_CELLS")
            if tuple(status.get("completed_cells", [])) != contract.cell_sequence:
                failures.append("STATUS_COMPLETED_CELLS_MISMATCH")
            core_declared = str(status.get("core_evidence_root", ""))
            if "$HOME" in core_declared or core_declared.startswith("~"):
                failures.append("STATUS_CORE_ROOT_UNRESOLVED_TOKEN")
            if core_declared and Path(core_declared) != core_root.resolve():
                failures.append("STATUS_CORE_ROOT_MISMATCH")
        except Exception as exc:
            failures.append(f"STATUS_UNREADABLE:{type(exc).__name__}")

    for cell in contract.cell_sequence:
        p = ue_root / "cells" / cell / "receiver_path_contract.json"
        if p.is_file() and p.stat().st_size > 0:
            try:
                obj = json.loads(p.read_text(encoding="utf-8"))
                if obj.get("writer_watcher_path_equal") is not True:
                    failures.append(f"RECEIVER_WRITER_WATCHER_MISMATCH:{cell}")
                for key in ("receiver_output_dir", "receiver_event_writer_path", "receiver_event_watcher_path", "receiver_console_path"):
                    value = str(obj.get(key, ""))
                    if not value.startswith("/") or "$HOME" in value or value.startswith("~"):
                        failures.append(f"RECEIVER_PATH_NOT_RESOLVED:{cell}:{key}")
            except Exception as exc:
                failures.append(f"RECEIVER_PATH_CONTRACT_UNREADABLE:{cell}:{type(exc).__name__}")

    reconstruction = ue_root / "analysis" / "p7b_reconstruction.json"
    if reconstruction.is_file():
        try:
            obj = json.loads(reconstruction.read_text(encoding="utf-8"))
            if obj.get("gate") != "PASS":
                failures.append("RECONSTRUCTION_GATE_NOT_PASS")
        except Exception as exc:
            failures.append(f"RECONSTRUCTION_UNREADABLE:{type(exc).__name__}")

    return {
        "schema_version": "wp2-p7b-evidence-contract-gate-v2",
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "checked_paths": checked,
        "ue_root": str(ue_root.resolve()),
        "core_root": str(core_root.resolve()),
        "scored": False,
        "scored_runs_authorized": False,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Contract-driven evidence completeness gate for P7B executable contract v2")
    ap.add_argument("--contract", default="experiments/WP-PWD01/p7b-executable-contract-v2.json")
    ap.add_argument("--ue-root", required=True)
    ap.add_argument("--core-root", required=True)
    ap.add_argument("--output")
    args = ap.parse_args()
    result = evaluate(Path(args.contract), Path(args.ue_root), Path(args.core_root))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print("EVIDENCE_CONTRACT_GATE=" + result["gate"])
    for failure in result["failures"]:
        print("FAILURE=" + failure)
    print("SCORED_AUTHORIZATION=BLOCKED")
    return 0 if result["gate"] == "PASS" else 20


if __name__ == "__main__":
    raise SystemExit(main())
