import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "experiments" / "WP-PWD01" / "p7b-qualification-contract.json"
PLAN_PATH = ROOT / "experiments" / "WP-PWD01" / "P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md"


class WP2P7BContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.plan = PLAN_PATH.read_text(encoding="utf-8")

    def test_contract_is_non_scored_single_reservation_three_cell_s3(self):
        c = self.contract
        self.assertEqual(c["schema_version"], "wp2-p7b-contract-v1")
        self.assertEqual(c["evidence_class"], "NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION")
        self.assertFalse(c["scored"])
        self.assertFalse(c["scored_runs_authorized"])
        self.assertEqual(c["reservation_limit"], 1)
        self.assertFalse(c["replacement_reservation_automatic"])
        self.assertEqual(
            [(x["order"], x["architecture"], x["scenario"]) for x in c["cells"]],
            [
                (1, "B1_MQTT_QOS1", "S3_OUTAGE_RESTART"),
                (2, "W1_OFFLINE_FIRST", "S3_OUTAGE_RESTART"),
                (3, "B2_MQTT_DURABLE_CLIENT", "S3_OUTAGE_RESTART"),
            ],
        )

    def test_frozen_science_and_restart_domain_are_preserved(self):
        c = self.contract
        self.assertEqual(c["profile"]["attenuator_ids"], [1, 33, 2, 34])
        self.assertEqual((c["profile"]["q0_db"], c["profile"]["q3_db"]), (0, 55))
        self.assertEqual(c["schedule"]["restart_offset_into_q3_s"], 60)
        self.assertEqual(c["schedule"]["h_app_s"], 300)
        self.assertEqual(c["schedule"]["h_app_anchor"], "t_service_ready")
        self.assertEqual(c["schedule"]["cohort_cutoff"], "t_rf_restore")
        r = c["restart_domain"]
        for key in (
            "telemetry_generator_outside_restart_domain",
            "gateway_client_process_only",
            "node_reboot_prohibited",
            "generator_pid_unchanged_required",
            "gateway_pid_change_required",
            "same_intra_run_client_identity_required",
            "source_sequence_continuity_required",
        ):
            self.assertTrue(r[key], key)

    def test_runtime_locks_and_washout_are_complete(self):
        c = self.contract
        matched = c["b1_w1_matched_transport"]
        self.assertEqual(matched["package"], "paho-mqtt==2.1.0")
        self.assertEqual(matched["protocol"], "MQTTv311")
        self.assertEqual(matched["qos"], 1)
        self.assertFalse(matched["clean_session"])
        self.assertEqual(matched["max_queued_messages"], 4096)
        self.assertEqual(matched["max_inflight_messages"], 20)
        b2 = c["b2_runtime"]
        self.assertEqual(b2["implementation"], "Eclipse Paho Java 1.2.5")
        self.assertEqual(
            b2["jar_sha256"],
            "59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185",
        )
        self.assertTrue(b2["disconnected_buffer"]["persist"])
        self.assertFalse(b2["disconnected_buffer"]["delete_oldest"])
        required = set(c["readiness_required"])
        self.assertTrue(
            {
                "four_attenuators_q0_readback",
                "tun_srsue_route",
                "initial_session_present_false",
                "fresh_architecture_state",
                "no_prior_process_or_session_residue",
                "healthy_utc_monotonic_clocks",
                "evidence_path_armed",
            }.issubset(required)
        )

    def test_acceptance_and_evidence_fail_closed(self):
        c = self.contract
        self.assertIn("accepted_unacknowledged_nonempty_before_restart", c["acceptance"]["b1"])
        self.assertIn("exact_low_level_match_to_b1", c["acceptance"]["w1"])
        self.assertIn("same_persistence_and_client_identity_reopened", c["acceptance"]["b2"])
        self.assertEqual(
            c["evidence_chain"],
            [
                "node_raw",
                "proj_persistent_escrow",
                "controller_pull",
                "github_actions_artifact",
                "independent_controller_readback",
                "outer_and_internal_sha256",
            ],
        )
        self.assertEqual(c["teardown_authority"], "EVIDENCE_ESCROW_GATE=PASS")
        self.assertTrue(c["fail_policy"]["stop_later_cells"])
        self.assertFalse(c["fail_policy"]["automatic_retry"])
        self.assertFalse(c["fail_policy"]["automatic_new_reservation"])

    def test_p7b_a_does_not_grant_live_authority(self):
        authority = self.contract["patch_authority"]
        self.assertEqual(authority["p7b_a"], "OFFLINE_CONTRACT_ONLY")
        self.assertIn("EXPLICIT", authority["p7b_b"])
        self.assertIn("SEPARATE_EXPLICIT_LIVE_AUTHORIZATION", authority["p7b_c"])
        for term in (
            "Live authority created by this document: NONE",
            "P7B-A contacts no POWDER system",
            "P7B-C authorization",
            "scored_runs_authorized=true",
        ):
            self.assertIn(term, self.plan)


if __name__ == "__main__":
    unittest.main()
