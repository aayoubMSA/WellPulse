from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/wp2-p7b-rq2-session.yml"
ACTIVATION = ROOT / "experiments/WP-PWD01/p7b-rq2-live-authorization-2026-08-28.json"
CONTROLLER = ROOT / "scripts/wp2_p7b_rq2_controller.sh"
ADAPTER = ROOT / "scripts/wp2_p7b_rq2_module_adapter.py"


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


class P7BRQ2LiveSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w = WORKFLOW.read_text(encoding="utf-8")
        cls.c = CONTROLLER.read_text(encoding="utf-8")
        cls.a = json.loads(ACTIVATION.read_text(encoding="utf-8"))

    def test_activation_is_explicit_but_r0_is_still_blocked_without_identity(self):
        self.assertTrue(self.a["user_live_authorization_received"])
        self.assertEqual(self.a["authority_id"], "P7B-RQ2")
        self.assertEqual(self.a["current_stage"], "AUTHORIZED_AWAITING_MANUAL_R0_RESERVATION_IDENTITY")
        self.assertIsNone(self.a["experiment_id"])
        self.assertIsNone(self.a["experiment_name"])
        self.assertFalse(self.a["workflow_dispatch_ready"])
        self.assertEqual(self.a["workflow_dispatch_blocker"], "MISSING_EXPERIMENT_ID_AND_EXPERIMENT_NAME")
        self.assertFalse(self.a["reservation_creation_by_github"])
        self.assertFalse(self.a["reservation_selection_by_github"])
        self.assertFalse(self.a["powder_contact_so_far"])

    def test_activation_pins_exact_control_plane_and_scientific_source(self):
        self.assertEqual(self.a["scientific_source_sha"], "2d7eb744f14ad4d5889909dac3cc29236c667190")
        self.assertEqual(git_blob(WORKFLOW), self.a["workflow_git_blob_sha"])
        self.assertEqual(git_blob(CONTROLLER), self.a["controller_helper_git_blob_sha"])
        self.assertEqual(git_blob(ADAPTER), self.a["module_adapter_git_blob_sha"])

    def test_workflow_is_manual_dispatch_only_with_exact_inputs_and_one_shot_guards(self):
        self.assertIn("workflow_dispatch:", self.w)
        self.assertNotIn("push:", self.w)
        self.assertNotIn("schedule:", self.w)
        self.assertNotIn("pull_request:", self.w)
        for token in ("experiment_id:", "experiment_name:", "authority_id:", "default: P7B-RQ2"):
            self.assertIn(token, self.w)
        self.assertIn('test "$GITHUB_RUN_NUMBER" = 1', self.w)
        self.assertIn('test "$GITHUB_RUN_ATTEMPT" = 1', self.w)
        self.assertIn("cancel-in-progress: false", self.w)

    def test_workflow_has_exact_modular_hci_spine_and_sequential_dependencies(self):
        for name in (
            "00 Freeze — Authority + Source + Contract",
            "10 EFCC — Reservation Identity + Manifest Read-Only",
            "20 Preflight — Stage Frozen Source + Target Native Gates",
            "30 Q0 Baseline — H2 Safe Known-Good Preparation",
            "40 B1 — Same-Implementation Comparator Cell",
            "45 B1 Evidence — Freeze + Off-POWDER Readback",
            "60 W1 — Offline-First Architecture Cell",
            "65 W1 Evidence — Freeze + Off-POWDER Readback",
            "80 B2 — Durable Standard MQTT Cell",
            "85 B2 Evidence — Freeze + Off-POWDER Readback",
            "95 Reconstruct — Non-Scored Physical Qualification Verdict",
            "99 Session Summary — Final Evidence Readback / Stop Before Teardown",
        ):
            self.assertIn(name, self.w)
        self.assertIn("needs: [m0, m1, m2, m3]", self.w)
        self.assertIn("needs: [m0, m1, m2, m4, m5]", self.w)
        self.assertIn("needs: [m0, m1, m2, m6, m7]", self.w)
        self.assertIn("needs: [m0, m1, m2, m8, m9]", self.w)

    def test_cell_modules_are_separate_and_paired_evidence_is_always_attempted(self):
        self.assertEqual(self.w.count("run-module B1"), 1)
        self.assertEqual(self.w.count("run-module W1"), 1)
        self.assertEqual(self.w.count("run-module B2"), 1)
        for label in ("b1", "w1", "b2", "final"):
            self.assertIn(f"pull-evidence {label}", self.w)
        self.assertGreaterEqual(self.w.count("always()"), 3)
        self.assertGreaterEqual(self.w.count("actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f"), 4)
        self.assertGreaterEqual(self.w.count("actions/download-artifact@37930b1c2abaa49bbe596cd826c3c89aef350131"), 4)

    def test_each_live_job_reinitializes_ssh_through_controller_helper(self):
        self.assertIn("setup_ssh(){", self.c)
        self.assertIn('eval "$(ssh-agent -s)"', self.c)
        self.assertIn("setsid -w ssh-add", self.c)
        self.assertIn("-A -o BatchMode=yes", self.c)
        self.assertGreaterEqual(self.w.count("wp2_p7b_rq2_controller.sh run-module"), 5)
        self.assertGreaterEqual(self.w.count("wp2_p7b_rq2_controller.sh pull-evidence"), 4)

    def test_no_reservation_creation_termination_auto_retry_or_teardown_command_surface(self):
        combined = (self.w + "\n" + self.c).lower()
        for forbidden in (
            "portal-cli experiment create",
            "portal-cli experiment terminate",
            "tmux kill-session",
            "killall",
            "cancel-in-progress: true",
        ):
            self.assertNotIn(forbidden, combined)
        self.assertIn("AUTOMATIC_RETRY=NO", self.w)
        self.assertIn("AUTOMATIC_TEARDOWN=NO", self.w)
        self.assertIn("TEARDOWN_AUTHORIZED=NO_MANUAL_T0_REQUIRED", self.w)
        self.assertIn("SCORED_AUTHORIZATION=BLOCKED", self.w)

    def test_m1_is_read_only_portal_and_m2_is_pre_rf_target_preflight(self):
        self.assertIn("portal-cli experiment get --experiment-id", self.c)
        self.assertIn("portal-cli experiment manifests get --experiment-id", self.c)
        self.assertIn("wp2_p7b_target_node_preflight.sh core", self.c)
        self.assertIn("wp2_p7b_target_node_preflight.sh ue", self.c)
        self.assertIn("git archive --format=tar \"$SCIENTIFIC_SOURCE_SHA\"", self.c)
        self.assertIn("a6da96560b6526dc6816761282722c996418fd8c", self.c)

    def test_controller_and_workflow_are_shell_static_safe(self):
        p = subprocess.run(["bash", "-n", str(CONTROLLER)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(self.a["future_dispatch_contract"]["run_number_exact"], 1)
        self.assertEqual(self.a["future_dispatch_contract"]["run_attempt_exact"], 1)
        self.assertFalse(self.a["current_authority"]["automatic_retry"])
        self.assertFalse(self.a["current_authority"]["automatic_teardown"])


if __name__ == "__main__":
    unittest.main()
