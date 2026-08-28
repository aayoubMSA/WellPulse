from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
DELTA = ROOT / "experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


class P7BH2ContractDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(BASE.read_text(encoding="utf-8"))
        cls.delta = json.loads(DELTA.read_text(encoding="utf-8"))

    def test_delta_remains_prospective_offline_and_base_is_exactly_pinned(self):
        d = self.delta
        self.assertTrue(d["status"].startswith("OFFLINE_H2_"), d["status"])
        self.assertTrue(d["status"].endswith("NOT_LIVE_AUTHORITY"), d["status"])
        self.assertEqual(d["delta_class"], "OPERATIONAL_SAFETY_AND_OBSERVABILITY_ONLY")
        self.assertFalse(d["scientific_change"])
        self.assertEqual(d["base_contract"]["path"], "experiments/WP-PWD01/p7b-executable-contract-v2.json")
        self.assertEqual(d["base_contract"]["schema_version"], self.base["schema_version"])
        self.assertEqual(d["base_contract"]["git_blob_sha"], git_blob_sha(BASE))
        self.assertIn(d["base_contract"]["mutation_policy"], {"DO_NOT_EDIT_BASE_AS_PART_OF_H2_1", "DO_NOT_EDIT_BASE_DURING_H2"})

    def test_all_authority_remains_false_and_fresh_user_authority_is_mandatory(self):
        a = self.delta["authority"]
        false_keys = {
            "live_authorized",
            "reservation_creation_authorized",
            "rf_authorized",
            "retry_authorized",
            "w1_b2_authorized",
            "teardown_authorized",
            "scored_authorized",
            "wp3_authorized",
            "automatic_retry",
            "automatic_new_reservation",
        }
        for key in false_keys:
            self.assertIn(key, a)
            self.assertIs(a[key], False, key)
        self.assertTrue(a["future_live_action_requires_separate_explicit_user_authorization"])
        self.assertEqual(
            a["promotion_requires"],
            [
                "H2_2_SESSION_OWNERSHIP=PASS",
                "H2_3_FRONTIER_EVIDENCE=PASS",
                "H2_4_ADVERSARIAL_QA=PASS",
                "H2_5_REGRESSION=PASS",
                "WP2_P7B_H2=PASS",
            ],
        )

    def test_exact_a1_to_a7_controls_are_machine_readable(self):
        self.assertEqual(set(self.delta["controls"]), {f"A{i}" for i in range(1, 8)})
        self.assertEqual(self.delta["h2_1_acceptance"]["exact_controls_required"], [f"A{i}" for i in range(1, 8)])
        self.assertEqual(self.delta["h2_1_acceptance"]["terminal_gate"], "H2_1_CONTRACT_DELTA=PASS")

    def test_frozen_scientific_controls_are_identical_to_base_contract(self):
        b = self.base
        d = self.delta["frozen_scientific_controls"]
        expected = {
            "q0_db": b["profile"]["q0_db"],
            "q1_db": b["profile"]["q1_db"],
            "q2_db": b["profile"]["q2_db"],
            "q3_db": b["profile"]["q3_db"],
            "attenuator_ids": b["profile"]["attenuator_ids"],
            "pre_impairment_q0_s": b["schedule"]["pre_impairment_q0_s"],
            "q3_s": b["schedule"]["q3_s"],
            "restart_offset_into_q3_s": b["schedule"]["restart_offset_into_q3_s"],
            "h_app_s": b["schedule"]["h_app_s"],
            "h_app_anchor": b["schedule"]["h_app_anchor"],
            "cohort_cutoff": b["schedule"]["cohort_cutoff"],
            "cell_sequence": b["schedule"]["cell_sequence"],
            "generator_outside_restart_domain": b["restart_domain"]["telemetry_generator_outside_restart_domain"],
            "automatic_scientific_retry": b["authority"]["automatic_retry"],
        }
        for key, value in expected.items():
            self.assertEqual(d[key], value, key)
        self.assertEqual(d["clocks_distinct"], ["t_rf_restore", "t_service_ready", "t_app_complete"])
        self.assertTrue(d["negative_null_unfavourable_evidence_retained"])

    def test_a1_disjointness_fails_closed_before_rf(self):
        a1 = self.delta["controls"]["A1"]
        self.assertEqual(a1["phase"], "PRE_RF")
        self.assertEqual(set(a1["forbidden_service_cleanup_namespaces"]), {"ue", "srs-ue", "enb", "srs-enb", "srs-epc"})
        self.assertTrue(a1["fail_closed_if_controller_in_cleanup_namespace"])
        self.assertEqual(a1["required_marker"], "CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS")
        self.assertEqual(a1["failure_effect"], "STOP_BEFORE_RF_MUTATION")

    def test_a2_ownership_blocks_unsafe_generic_tmux_kill(self):
        a2 = self.delta["controls"]["A2"]
        self.assertTrue(a2["generic_tmux_kill_session_without_ownership_proof_prohibited"])
        self.assertTrue(a2["ownership_proof_must_exclude_controller_pid"])
        self.assertTrue(a2["ownership_proof_must_exclude_controller_session"])
        self.assertEqual(a2["preferred_termination"], "PID_SCOPED_SERVICE_PROCESS_TERMINATION")
        self.assertEqual(set(a2["session_kill_allowed_only_if"]), {"SERVICE_OWNERSHIP_EXCLUSIVE=PASS", "CONTROLLER_NOT_PRESENT=PASS"})

    def test_a3_controller_is_outside_restore_failure_domain(self):
        a3 = self.delta["controls"]["A3"]
        self.assertIn("GITHUB_ACTIONS_CONTROLLER_HOST", a3["preferred_controller_domains"])
        self.assertTrue(a3["self_ssh_allowed_only_if_cleanup_cannot_destroy_caller_or_supervisor"])
        self.assertTrue(a3["cross_module_hidden_process_state_prohibited"])
        self.assertEqual(a3["required_marker"], "CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION=PASS")

    def test_a4_restart_transition_is_incremental_and_does_not_replace_final_proof(self):
        a4 = self.delta["controls"]["A4"]
        self.assertEqual(a4["path_template"], "ue:cells/{cell}/restart_transition.json")
        required = set(a4["required_fields"])
        for field in (
            "generator_pid_before",
            "generator_pid_after",
            "old_gateway_pid",
            "new_gateway_pid",
            "restart_request_utc",
            "restart_request_monotonic",
            "new_ready_utc",
            "new_ready_monotonic",
            "source_generation_continuity_status",
        ):
            self.assertIn(field, required)
        self.assertTrue(a4["final_restart_proof_remains_required"])
        self.assertTrue(a4["restart_transition_does_not_replace_final_restart_proof"])

    def test_a5_restoration_frontier_has_exact_order_and_no_added_delay(self):
        a5 = self.delta["controls"]["A5"]
        self.assertTrue(a5["observability_only_no_artificial_scientific_delay"])
        self.assertEqual(
            a5["ordered_markers"],
            [
                "RESTORE_REQUESTED",
                "UE_CLEANUP_BEGIN",
                "UE_CLEANUP_END",
                "CORE_CLEANUP_BEGIN",
                "CORE_CLEANUP_END",
                "CORE_START_BEGIN",
                "CORE_START_END",
                "CORE_STABLE_READY",
                "UE_START_BEGIN",
                "UE_START_END",
                "UE_PROCESS_READY",
                "SERVICE_READY_PROBE_BEGIN",
                "SERVICE_READY_PROBE_END",
            ],
        )
        self.assertEqual(a5["failure_requirement"], "LAST_DURABLY_WRITTEN_FRONTIER_MUST_SURVIVE")

    def test_a6_traps_are_supplementary_not_correctness_dependency(self):
        a6 = self.delta["controls"]["A6"]
        self.assertTrue(a6["required_as_supplementary_evidence"])
        self.assertEqual(set(a6["trap_candidates"]), {"EXIT", "TERM", "HUP"})
        self.assertTrue(a6["correctness_must_not_depend_on_trap_execution"])
        self.assertTrue(a6["abrupt_loss_must_remain_diagnosable_from_incremental_evidence"])

    def test_a7_has_all_required_adversarial_cases_and_no_live_powder_qa(self):
        a7 = self.delta["controls"]["A7"]
        self.assertEqual(
            set(a7["required_cases"]),
            {
                "CONTROLLER_IN_TMUX_UE_REJECTED_BEFORE_RF",
                "ALLOWED_CONTROLLER_SURVIVES_SERVICE_CLEANUP",
                "SERVICE_OWNERSHIP_SELECTION_CANNOT_MATCH_CONTROLLER_PID_OR_SESSION",
                "RESTART_TRANSITION_SURVIVES_SYNTHETIC_FAILURE_AFTER_GATEWAY_RESTART",
                "EACH_RESTORE_PHASE_FAILURE_PRESERVES_LAST_FRONTIER",
                "FROZEN_SCIENTIFIC_CONTROLS_UNCHANGED",
                "AUTOMATIC_RETRY_NOT_INTRODUCED",
            },
        )
        self.assertTrue(a7["live_powder_contact_for_qa_prohibited"])
        self.assertEqual(a7["required_gate"], "H2_4_ADVERSARIAL_QA=PASS")

    def test_prohibited_deltas_protect_science_and_authority(self):
        prohibited = set(self.delta["prohibited_deltas"])
        for token in (
            "RF_LEVEL_CHANGE",
            "ATTENUATOR_ID_CHANGE",
            "TIMING_CHANGE",
            "CELL_ORDER_CHANGE",
            "H_APP_REESTIMATION",
            "PRIMARY_COHORT_CUTOFF_CHANGE",
            "SCIENTIFIC_ENDPOINT_CHANGE",
            "AUTOMATIC_RETRY_ENABLEMENT",
            "SCORED_AUTHORIZATION",
            "LIVE_AUTHORIZATION",
        ):
            self.assertIn(token, prohibited)

    def test_next_patch_progression_is_h2_or_explicit_stop_not_live_execution(self):
        next_patch = self.delta["next_patch_on_pass"]
        self.assertTrue(next_patch.startswith("WP2-P7B-H2.") or next_patch.startswith("STOP"), next_patch)
        self.assertNotIn("workflow", next_patch.lower())
        self.assertNotIn("reservation", next_patch.lower())


if __name__ == "__main__":
    unittest.main()
