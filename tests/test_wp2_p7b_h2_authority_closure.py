from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "experiments/WP-PWD01/p7b-h2-requalification-authority-v1.json"
BASE = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
RUNTIME = ROOT / "experiments/WP-PWD01/p7b-target-runtime-contract-v2.json"
MODULAR = ROOT / "experiments/WP-PWD01/p7b-modular-pipeline-contract-v1.json"
H24 = ROOT / "evidence/powder/wp2-p7b-h2-4-adversarial-qa.json"
H25 = ROOT / "evidence/powder/wp2-p7b-h2-5-regression.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


class P7BH2AuthorityClosureTests(unittest.TestCase):
    def setUp(self):
        self.auth = load(AUTH)
        self.base = load(BASE)
        self.runtime = load(RUNTIME)
        self.modular = load(MODULAR)

    def test_h2_terminal_decision_is_eligibility_not_live_authority(self):
        self.assertEqual(self.auth["terminal_h2_verdict"], "WP2_P7B_H2=PASS_REQUALIFICATION_REPAIR_CLOSED")
        self.assertTrue(self.auth["decision"]["h2_repair_sufficient_for_future_non_scored_requalification_request"])
        self.assertTrue(self.auth["future_live_eligibility"]["separate_explicit_user_live_authorization_required"])
        self.assertTrue(self.auth["future_live_eligibility"]["then_current_reservation_and_access_validation_required"])
        for value in self.auth["current_authority"].values():
            self.assertFalse(value)
        self.assertFalse(self.auth["decision"]["scored_execution_eligible"])
        self.assertFalse(self.auth["decision"]["wp3_execution_eligible"])

    def test_historical_abort_remains_null_consumed_and_new_session_is_bounded(self):
        d = self.auth["decision"]
        f = self.auth["future_live_eligibility"]
        self.assertTrue(d["historical_aborted_b1_remains_null_and_consumed"])
        self.assertEqual(d["historical_b1_scientific_verdict"], "NULL_ABORTED_AFTER_Q3")
        self.assertTrue(d["future_requalification_is_new_bounded_session_not_continuation_of_aborted_run"])
        self.assertEqual(f["maximum_new_reservations_if_later_authorized"], 1)
        self.assertEqual(f["maximum_live_session_attempts_if_later_authorized"], 1)
        self.assertFalse(f["automatic_retry_after_any_live_failure"])
        self.assertFalse(f["automatic_second_reservation"])
        self.assertTrue(f["user_creates_or_selects_reservation_in_powder_portal"])
        self.assertTrue(f["github_may_not_create_reservation"])

    def test_prospective_entrypoint_is_h2_overlay_with_exact_source_locks(self):
        p = self.auth["prospective_execution"]
        expected = {
            "scripts/wp2_p7b_c_node_h2.py": p["node_entrypoint_git_blob_sha"],
            "scripts/wp2_p7b_c_node_r2.py": p["inherited_frozen_r2_git_blob_sha"],
            "src/wellpulse/p7b_session_ownership.py": p["controller_ownership_library_git_blob_sha"],
            "scripts/wp2_p7b_service_restore_h2.sh": p["safe_restore_git_blob_sha"],
            "scripts/wp2_p7b_target_node_preflight.sh": p["target_preflight_git_blob_sha"],
        }
        self.assertEqual(p["node_entrypoint"], "scripts/wp2_p7b_c_node_h2.py")
        self.assertEqual(p["inherited_frozen_r2_entrypoint"], "scripts/wp2_p7b_c_node_r2.py")
        for rel, sha in expected.items():
            self.assertEqual(git_blob(ROOT / rel), sha, rel)

    def test_frozen_contract_and_h2_evidence_locks_are_exact(self):
        for item in self.auth["frozen_contract_locks"].values():
            self.assertEqual(git_blob(ROOT / item["path"]), item["git_blob_sha"], item["path"])
        for item in self.auth["h2_evidence_locks"].values():
            self.assertEqual(git_blob(ROOT / item["path"]), item["git_blob_sha"], item["path"])
        self.assertEqual(load(H24)["terminal_verdict"], "H2_4_ADVERSARIAL_QA=PASS")
        self.assertEqual(load(H25)["terminal_verdict"], "H2_5_REGRESSION=PASS")

    def test_scientific_controls_remain_equivalent_and_retry_false(self):
        frozen = self.auth["frozen_scientific_controls"]
        profile = self.base["profile"]
        schedule = self.base["schedule"]
        self.assertEqual(frozen["q_db"], [profile["q0_db"], profile["q1_db"], profile["q2_db"], profile["q3_db"]])
        self.assertEqual(frozen["attenuator_ids"], profile["attenuator_ids"])
        self.assertEqual(frozen["pre_q0_s"], schedule["pre_impairment_q0_s"])
        self.assertEqual(frozen["q3_s"], schedule["q3_s"])
        self.assertEqual(frozen["restart_offset_into_q3_s"], schedule["restart_offset_into_q3_s"])
        self.assertEqual(frozen["cell_order"], schedule["cell_sequence"])
        self.assertEqual(frozen["h_app_s"], schedule["h_app_s"])
        self.assertEqual(frozen["h_app_anchor"], schedule["h_app_anchor"])
        self.assertEqual(frozen["cohort_cutoff"], schedule["cohort_cutoff"])
        self.assertFalse(frozen["automatic_scientific_retry"])
        self.assertFalse(self.base["authority"]["automatic_retry"])
        self.assertFalse(self.modular["architecture"]["automatic_retry"])

    def test_no_live_workflow_exists_and_modular_manual_boundary_is_preserved(self):
        p = self.auth["prospective_execution"]
        self.assertTrue(p["future_live_workflow_must_not_exist_until_separate_user_live_authorization"])
        self.assertFalse((ROOT / p["future_live_workflow"]).exists())
        self.assertEqual(self.modular["architecture"]["future_trigger"], "workflow_dispatch_only")
        self.assertEqual(
            self.modular["architecture"]["workflow_creation_policy"],
            "CREATE_ONLY_AFTER_H2_PASS_AND_SEPARATE_EXPLICIT_USER_LIVE_AUTHORIZATION",
        )
        self.assertFalse(self.modular["architecture"]["automatic_reservation_create"])
        self.assertFalse(self.modular["architecture"]["automatic_teardown"])
        self.assertFalse(self.runtime["live_authorized"])
        self.assertTrue(self.runtime["future_execution"]["fresh_explicit_live_authorization_still_required"])


if __name__ == "__main__":
    unittest.main()
