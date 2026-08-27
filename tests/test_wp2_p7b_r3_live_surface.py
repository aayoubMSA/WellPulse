from pathlib import Path
import json
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class P7BR3LiveSurfaceTests(unittest.TestCase):
    def test_controller_is_shell_valid_and_r2_static_gate_passes(self):
        controller = ROOT / "powder" / "wp2_p7b_r3_execute.sh"
        p = subprocess.run(["bash", "-n", str(controller)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.returncode, 0, p.stdout)
        q = subprocess.run([
            "python3", str(ROOT / "scripts" / "wp2_p7b_r2_validate_controller.py"),
            "--controller", str(controller),
            "--contract", str(ROOT / "experiments" / "WP-PWD01" / "p7b-requalification-r2-contract.json"),
        ], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=ROOT)
        self.assertEqual(q.returncode, 0, q.stdout)
        self.assertIn("P7B_R2_CONTROLLER_STATIC_GATE=PASS", q.stdout)

    def test_progress_helper_is_runtime_safe_under_nounset(self):
        text = (ROOT / "powder" / "wp2_p7b_r3_execute.sh").read_text(encoding="utf-8")
        line = next(x for x in text.splitlines() if x.startswith("bar(){"))
        p = subprocess.run(
            ["bash", "-lc", f"set -u; {line}; bar 5 test"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("5%", p.stdout)

    def test_controller_has_exact_one_replacement_and_one_teardown(self):
        text = (ROOT / "powder" / "wp2_p7b_r3_execute.sh").read_text(encoding="utf-8")
        self.assertEqual(text.count("portal-cli experiment create"), 1)
        self.assertEqual(text.count("portal-cli experiment terminate"), 1)
        self.assertIn("P7B-RQ1", text)
        self.assertIn("AUTOMATIC_RETRY=NO", text)
        self.assertIn("SECOND_REPLACEMENT=NO", text)
        self.assertNotIn("scored_runs_authorized=true", text)

    def test_r1_entrypoint_and_absolute_path_preservation_are_mandatory(self):
        text = (ROOT / "powder" / "wp2_p7b_r3_execute.sh").read_text(encoding="utf-8")
        self.assertIn("scripts/wp2_p7b_c_node_r1.py", text)
        self.assertNotIn("scripts/wp2_p7b_c_node.py\"", text)
        self.assertIn("scripts/wp2_p7b_preservation_helpers.sh", text)
        self.assertIn("wp2_p7b_path_contract.py validate", text)
        self.assertIn("p7b_copy_tree_with_hash_manifest", text)

    def test_r2_blob_locks_are_checked_before_powder_api_list(self):
        text = (ROOT / "powder" / "wp2_p7b_r3_execute.sh").read_text(encoding="utf-8")
        for marker in (
            "6d28468c93742046d952668b9df1cad8e6ea78c0",
            "2e77e7e355e25c6e3f747956e2f2b0ac5ad46161",
            "9063ec2e97e9cbf7a9f76d6ea10920236d8370ef",
            "git hash-object",
        ):
            self.assertIn(marker, text)
        self.assertLess(text.index("git hash-object"), text.index("portal-cli experiment list"))
        self.assertLess(text.index("P7B_R2_CONTROLLER_STATIC_GATE=PASS"), text.index("portal-cli experiment list"))

    def test_strict_bundle_requires_all_three_receiver_ledgers(self):
        text = (ROOT / "powder" / "wp2_p7b_r3_execute.sh").read_text(encoding="utf-8")
        self.assertIn("for c in P7B-B1-S3 P7B-W1-S3 P7B-B2-S3", text)
        self.assertIn("receiver/receiver_events.jsonl", text)
        self.assertIn("receiver/telemetry_received.csv", text)
        self.assertIn("analysis/p7b_reconstruction.json", text)
        self.assertIn("BLOCKED_STRICT_COMPLETENESS", text)

    def test_receiver_console_is_provenance_not_nonempty_scientific_evidence(self):
        text = (ROOT / "powder" / "wp2_p7b_r3_execute.sh").read_text(encoding="utf-8")
        self.assertIn('test -e "$core/cells/$c/receiver/console.txt"', text)
        self.assertNotIn('test -s "$core/cells/$c/receiver/console.txt"', text)

    def test_teardown_markers_precede_terminate(self):
        text = (ROOT / "powder" / "wp2_p7b_r3_execute.sh").read_text(encoding="utf-8")
        term = text.index("portal-cli experiment terminate")
        for marker in ("EVIDENCE_ESCROW_GATE=PASS", "CONTROLLER_OFFPOWDER_GATE=PASS", "TEARDOWN_AUTHORIZED=YES"):
            self.assertLess(text.index(marker), term)

    def test_workflow_is_one_shot_trigger_and_surfaces_progress(self):
        path = ROOT / ".github" / "workflows" / "wp2-p7b-r3-live.yml"
        text = path.read_text(encoding="utf-8")
        self.assertIn(".wp2-p7b-r3-live-trigger", text)
        self.assertIn("execute=WP2_P7B_R3_LIVE_ONCE", text)
        self.assertIn("authority_id=P7B-RQ1", text)
        self.assertIn("reservation_limit=1", text)
        self.assertIn("automatic_retry=NO", text)
        self.assertIn("second_replacement=NO", text)
        self.assertIn("actions/upload-artifact", text)
        self.assertIn("actions/download-artifact", text)
        self.assertIn("Publish colorful progress and first-cause status", text)
        self.assertIn("FIRST-CAUSE CONTROLLER TAIL", text)
        self.assertNotIn("workflow_dispatch", text)

    def test_contract_remains_non_scored_and_replacement_only(self):
        c = json.loads((ROOT / "experiments" / "WP-PWD01" / "p7b-requalification-r2-contract.json").read_text())
        self.assertFalse(c["scored_runs_authorized"])
        self.assertEqual(c["replacement_reservation"]["maximum_new_reservations"], 1)
        self.assertFalse(c["replacement_reservation"]["automatic_retry"])
        self.assertFalse(c["replacement_reservation"]["second_replacement_authorized"])
        self.assertEqual(c["scientific_controls"]["cell_sequence"], ["P7B-B1-S3", "P7B-W1-S3", "P7B-B2-S3"])


if __name__ == "__main__":
    unittest.main()
