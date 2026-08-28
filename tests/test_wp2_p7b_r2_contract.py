from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "experiments" / "WP-PWD01" / "p7b-requalification-r2-contract.json"
ORIGINAL = ROOT / "experiments" / "WP-PWD01" / "p7b-qualification-contract.json"
RQ2_ACTIVATION = ROOT / "experiments" / "WP-PWD01" / "p7b-rq2-live-authorization-2026-08-28.json"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("r2_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class P7BR2ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(R2.read_text(encoding="utf-8"))
        cls.original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
        cls.validator = load_module(ROOT / "scripts" / "wp2_p7b_r2_validate_controller.py")

    def test_r2_is_offline_non_scored_and_one_replacement_only(self):
        c = self.contract
        self.assertEqual(c["schema_version"], "wp2-p7b-r2-requalification-contract-v1")
        self.assertEqual(c["decision"], "GO_ONE_REPLACEMENT_NON_SCORED_QUALIFICATION")
        self.assertFalse(c["scored"])
        self.assertFalse(c["scored_runs_authorized"])
        self.assertFalse(c["live_authorized"])
        self.assertFalse(c["powder_contact_authorized"])
        r = c["replacement_reservation"]
        self.assertEqual(r["authority_id"], "P7B-RQ1")
        self.assertEqual(r["maximum_new_reservations"], 1)
        self.assertFalse(r["second_replacement_authorized"])
        self.assertFalse(r["automatic_retry"])
        self.assertFalse(r["automatic_new_reservation"])
        self.assertTrue(r["requires_separate_explicit_live_authorization"])
        self.assertFalse(r["current_live_authorized"])

    def test_original_attempt_is_preserved_and_original_limit_remains_consumed(self):
        c = self.contract
        self.assertEqual(self.original["reservation_limit"], 1)
        self.assertFalse(self.original["replacement_reservation_automatic"])
        self.assertEqual(c["original_contract"]["reservation_limit"], 1)
        self.assertTrue(c["original_contract"]["reservation_consumed"])
        a = c["original_attempt"]
        self.assertEqual(a["verdict"], "BLOCKED:RECEIVER_CONNECT_TIMEOUT")
        self.assertEqual(a["completed_cells"], [])
        self.assertFalse(a["scientific_measurement_started"])
        self.assertTrue(a["retained_evidence_must_remain_unchanged"])

    def test_scientific_schedule_and_profile_are_unchanged(self):
        c = self.contract["scientific_controls"]
        self.assertEqual(c["profile"], self.original["profile"]["name"])
        self.assertEqual(c["profile_revision"], self.original["profile"]["revision"])
        self.assertEqual(c["attenuator_ids"], self.original["profile"]["attenuator_ids"])
        self.assertEqual(c["q0_db"], self.original["profile"]["q0_db"])
        self.assertEqual(c["q3_db"], self.original["profile"]["q3_db"])
        self.assertEqual(c["pre_impairment_q0_s"], self.original["schedule"]["pre_impairment_q0_s"])
        self.assertEqual(c["q3_s"], self.original["schedule"]["q3_s"])
        self.assertEqual(c["restart_offset_into_q3_s"], self.original["schedule"]["restart_offset_into_q3_s"])
        self.assertEqual(c["h_app_s"], self.original["schedule"]["h_app_s"])
        self.assertEqual(c["h_app_anchor"], self.original["schedule"]["h_app_anchor"])
        self.assertEqual(c["primary_cohort_cutoff"], self.original["schedule"]["cohort_cutoff"])
        self.assertEqual(c["cell_sequence"], [x["id"] for x in self.original["cells"]])
        self.assertFalse(c["scientific_change_from_original_p7b"])

    def test_repaired_entrypoint_and_path_contract_are_frozen(self):
        e = self.contract["execution_lock"]
        for key in ("node_entrypoint", "path_contract", "preservation_helper", "controller_static_validator"):
            self.assertTrue((ROOT / e[key]).exists(), e[key])
        self.assertEqual(e["node_entrypoint"], "scripts/wp2_p7b_c_node_r1.py")
        node = (ROOT / e["node_entrypoint"]).read_text(encoding="utf-8")
        self.assertIn("RECEIVER_EXITED_BEFORE_CONNECT", node)
        self.assertIn("P7B_R1_DIAGNOSTICS_BEGIN", node)
        self.assertIn("receiver_path_contract.json", node)
        self.assertNotIn("portal-cli experiment create", node)
        self.assertNotIn("scored_runs_authorized=true", node)

    def test_future_live_patch_must_preserve_evidence_before_teardown(self):
        e = self.contract["evidence_survival"]
        self.assertTrue(e["required"])
        self.assertTrue(e["resolved_absolute_paths_only"])
        self.assertTrue(e["literal_home_or_tilde_tokens_prohibited"])
        self.assertEqual(
            e["teardown_authority"],
            "EVIDENCE_ESCROW_GATE=PASS_AND_CONTROLLER_OFFPOWDER_GATE=PASS",
        )
        self.assertEqual(e["on_evidence_gate_failure"], "LEAVE_EXPERIMENT_LIVE_AND_STOP")
        self.assertTrue(e["complete_raw_evidence_required"])

    def test_retired_old_controller_fails_r2_static_gate(self):
        old = (ROOT / "powder" / "wp2_p7b_c_execute.sh").read_text(encoding="utf-8")
        failures = self.validator.validate_controller_text(old, self.contract)
        self.assertIn("REPAIRED_NODE_ENTRYPOINT_MISSING", failures)
        self.assertIn("REPLACEMENT_AUTHORITY_MARKER_MISSING", failures)

    def test_synthetic_compliant_future_controller_passes_static_gate(self):
        text = """#!/usr/bin/env bash
set -euo pipefail
AUTHORITY_ID=P7B-RQ1
AUTOMATIC_RETRY=NO
SECOND_REPLACEMENT=NO
# exactly one create in the future live controller
portal-cli experiment create --name wp7brq1demo
python scripts/wp2_p7b_c_node_r1.py
source scripts/wp2_p7b_preservation_helpers.sh
# bounded failure diagnostics are emitted by wp2_p7b_c_node_r1.py
P7B_R1_DIAGNOSTICS_BEGIN=delegated
EVIDENCE_ESCROW_GATE=PASS
CONTROLLER_OFFPOWDER_GATE=PASS
TEARDOWN_AUTHORIZED=YES
portal-cli experiment terminate --experiment-id "$EXPID"
"""
        self.assertEqual(self.validator.validate_controller_text(text, self.contract), [])

    def test_r2_itself_grants_no_live_authority_and_later_surface_is_phase_bounded(self):
        # Historical R2 remains offline forever. Later live surfaces are legal only
        # when a newer explicit authority artifact exists; this does not mutate R2.
        self.assertFalse(self.contract["live_authorized"])
        self.assertFalse(self.contract["powder_contact_authorized"])
        self.assertFalse(self.contract["scored_runs_authorized"])

        workflows = {
            p.name
            for p in (ROOT / ".github" / "workflows").glob("*.yml")
            if "p7b" in p.name.lower() and "b2-semantics" not in p.name.lower()
        }
        allowed = {"wp2-p7b-r3-live.yml"}
        if RQ2_ACTIVATION.exists():
            activation = json.loads(RQ2_ACTIVATION.read_text(encoding="utf-8"))
            self.assertTrue(activation["user_live_authorization_received"])
            self.assertEqual(activation["authority_id"], "P7B-RQ2")
            allowed.add("wp2-p7b-rq2-session.yml")
        self.assertTrue(workflows.issubset(allowed), workflows)

        if "wp2-p7b-r3-live.yml" in workflows:
            text = (ROOT / ".github" / "workflows" / "wp2-p7b-r3-live.yml").read_text(encoding="utf-8")
            self.assertIn("authority_id=P7B-RQ1", text)
            self.assertIn("reservation_limit=1", text)
            self.assertIn("automatic_retry=NO", text)
            self.assertIn("second_replacement=NO", text)
            self.assertNotIn("workflow_dispatch", text)

        if "wp2-p7b-rq2-session.yml" in workflows:
            text = (ROOT / ".github" / "workflows" / "wp2-p7b-rq2-session.yml").read_text(encoding="utf-8")
            self.assertIn("workflow_dispatch:", text)
            self.assertNotIn("push:", text)
            self.assertNotIn("schedule:", text)
            self.assertIn("SCORED_AUTHORIZATION=BLOCKED", text)
            self.assertIn("TEARDOWN_AUTHORIZED=NO_MANUAL_T0_REQUIRED", text)


if __name__ == "__main__":
    unittest.main()
