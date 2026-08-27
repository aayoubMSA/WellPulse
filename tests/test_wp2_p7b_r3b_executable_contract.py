from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

from wellpulse.p7b_contract_v2 import EXPECTED_CELL_SEQUENCE, load_contract

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
V1 = ROOT / "experiments/WP-PWD01/p7b-qualification-contract.json"


def load_script(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class P7BR3BExecutableContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = load_contract(V2)
        cls.v1 = json.loads(V1.read_text(encoding="utf-8"))
        cls.evidence = load_script(ROOT / "scripts/wp2_p7b_evidence_gate_v2.py", "p7b_evidence_gate_v2_test")

    def test_contract_is_offline_non_scored_and_requires_fresh_live_authorization(self):
        raw = self.c.raw
        self.assertFalse(raw["scored"])
        self.assertFalse(raw["scored_runs_authorized"])
        self.assertFalse(raw["live_authorized"])
        self.assertTrue(raw["authority"]["requires_fresh_explicit_live_authorization_after_r3b"])
        self.assertEqual(raw["authority"]["maximum_new_reservations"], 1)
        self.assertFalse(raw["authority"]["automatic_retry"])
        self.assertFalse(raw["authority"]["second_replacement_authorized"])

    def test_v2_preserves_all_frozen_v1_scientific_controls(self):
        p2, s2 = self.c.profile, self.c.schedule
        p1, s1 = self.v1["profile"], self.v1["schedule"]
        self.assertEqual(p2["name"], p1["name"])
        self.assertEqual(p2["revision"], p1["revision"])
        self.assertEqual(p2["attenuator_ids"], p1["attenuator_ids"])
        self.assertEqual(p2["q0_db"], p1["q0_db"])
        self.assertEqual(p2["q3_db"], p1["q3_db"])
        self.assertEqual(s2["pre_impairment_q0_s"], s1["pre_impairment_q0_s"])
        self.assertEqual(s2["q3_s"], s1["q3_s"])
        self.assertEqual(s2["restart_offset_into_q3_s"], s1["restart_offset_into_q3_s"])
        self.assertEqual(s2["h_app_s"], s1["h_app_s"])
        self.assertEqual(s2["h_app_anchor"], s1["h_app_anchor"])
        self.assertEqual(s2["cohort_cutoff"], s1["cohort_cutoff"])
        self.assertEqual(tuple(s2["cell_sequence"]), EXPECTED_CELL_SEQUENCE)
        self.assertEqual(tuple(x["id"] for x in self.v1["cells"]), EXPECTED_CELL_SEQUENCE)
        self.assertEqual(self.c.b2_runtime["jar_sha256"], self.v1["b2_runtime"]["jar_sha256"])

    def test_v2_roots_are_resolved_runtime_templates_not_shell_tokens(self):
        ue = self.c.render_root("ue", ue_home="/users/aayoub", run_id="r1", core_home="/users/aayoub", experiment_id="e1")
        core = self.c.render_root("core", ue_home="/users/aayoub", run_id="r1", core_home="/users/aayoub", experiment_id="e1")
        escrow = self.c.render_root("escrow", ue_home="/users/aayoub", run_id="r1", core_home="/users/aayoub", experiment_id="e1")
        self.assertTrue(ue.startswith("/")); self.assertTrue(core.startswith("/")); self.assertTrue(escrow.startswith("/proj/WellPulse/"))
        self.assertNotIn("$HOME", ue + core + escrow)

    def test_only_r2_node_entrypoint_is_future_authoritative(self):
        e = self.c.raw["execution"]
        self.assertEqual(e["only_authoritative_node_entrypoint"], "scripts/wp2_p7b_c_node_r2.py")
        self.assertIn("scripts/wp2_p7b_c_node.py", e["legacy_entrypoints_prohibited"])
        self.assertIn("scripts/wp2_p7b_c_node_r1.py", e["legacy_entrypoints_prohibited"])
        text = (ROOT / e["only_authoritative_node_entrypoint"]).read_text(encoding="utf-8")
        for token in ("base.Q0_DB", "base.Q3_DB", "base.PRE_Q0_S", "base.Q3_S", "base.RESTART_OFFSET_S", "base.H_APP_S", "base.B2_JAR_SHA"):
            self.assertIn(token, text)
        self.assertNotIn("portal-cli experiment create", text)
        self.assertNotIn("portal-cli experiment terminate", text)
        self.assertNotIn("scored_runs_authorized=true", text)

    def _materialize_complete_tree(self, root: Path) -> tuple[Path, Path]:
        ue, core = root / "ue", root / "core"
        ue.mkdir(); core.mkdir()
        layout = self.c.raw["evidence_layout"]
        roots = {"ue": ue, "core": core}

        def make(spec: str, cell: str | None = None, empty: bool = False):
            owner, rel = spec.split(":", 1)
            if cell:
                rel = rel.format(cell=cell)
            p = roots[owner] / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("" if empty else "x\n", encoding="utf-8")
            return p

        for spec in layout["reservation_required_nonempty"]:
            make(spec)
        for cell in self.c.cell_sequence:
            for spec in layout["per_cell_required_nonempty"]:
                p = make(spec, cell)
                if p.name == "receiver_path_contract.json":
                    receiver = (core / "cells" / cell / "receiver").resolve()
                    p.write_text(json.dumps({
                        "writer_watcher_path_equal": True,
                        "receiver_output_dir": str(receiver),
                        "receiver_event_writer_path": str(receiver / "receiver_events.jsonl"),
                        "receiver_event_watcher_path": str(receiver / "receiver_events.jsonl"),
                        "receiver_console_path": str(receiver / "console.txt")
                    }), encoding="utf-8")
            for spec in layout["per_cell_required_exists"]:
                make(spec, cell, empty=True)
            for spec in layout["architecture_required_nonempty"].get(cell, []):
                make(spec)

        status = {
            "gate": "PASS_PHYSICAL_CELLS",
            "completed_cells": list(self.c.cell_sequence),
            "core_evidence_root": str(core.resolve()),
            "ue_evidence_root": str(ue.resolve()),
            "scored": False,
            "scored_runs_authorized": False,
        }
        (ue / "p7b_c_status.json").write_text(json.dumps(status), encoding="utf-8")
        reconstruction = {"gate": "PASS", "failures": [], "scored": False, "scored_runs_authorized": False}
        (ue / "analysis/p7b_reconstruction.json").write_text(json.dumps(reconstruction), encoding="utf-8")
        return ue, core

    def test_synthetic_complete_evidence_passes_and_single_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as td:
            ue, core = self._materialize_complete_tree(Path(td))
            result = self.evidence.evaluate(V2, ue, core)
            self.assertEqual(result["gate"], "PASS", result["failures"])
            victim = ue / "cells/P7B-W1-S3/w1_durability_proof.json"
            victim.unlink()
            result2 = self.evidence.evaluate(V2, ue, core)
            self.assertEqual(result2["gate"], "FAIL")
            self.assertTrue(any("w1_durability_proof.json" in x for x in result2["failures"]))

    def test_unresolved_status_core_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            ue, core = self._materialize_complete_tree(Path(td))
            status = json.loads((ue / "p7b_c_status.json").read_text())
            status["core_evidence_root"] = "$HOME/wellpulse-powder-evidence/p7b/demo-core"
            (ue / "p7b_c_status.json").write_text(json.dumps(status), encoding="utf-8")
            result = self.evidence.evaluate(V2, ue, core)
            self.assertEqual(result["gate"], "FAIL")
            self.assertIn("STATUS_CORE_ROOT_UNRESOLVED_TOKEN", result["failures"])

    def test_no_live_p7b_workflow_or_trigger_remains_on_main(self):
        workflows = {p.name for p in (ROOT / ".github/workflows").glob("*.yml")}
        self.assertFalse(any("p7b-r3" in x.lower() or "p7b-c-live" in x.lower() or "p7b-d" in x.lower() for x in workflows))
        self.assertFalse((ROOT / ".wp2-p7b-r3-live-trigger").exists())

    def test_teardown_requires_contract_escrow_and_offpowder_gates(self):
        required = set(self.c.raw["evidence_survival"]["teardown_requires"])
        self.assertEqual(required, {"EVIDENCE_CONTRACT_GATE=PASS", "EVIDENCE_ESCROW_GATE=PASS", "CONTROLLER_OFFPOWDER_GATE=PASS"})
        self.assertEqual(self.c.raw["evidence_survival"]["on_failure"], "LEAVE_EXPERIMENT_LIVE_AND_STOP")


if __name__ == "__main__":
    unittest.main()
