from __future__ import annotations

from pathlib import Path
import subprocess
import unittest

from wellpulse.p7b_session_ownership import (
    evaluate_controller_identity,
    evaluate_pid_ownership,
)

ROOT = Path(__file__).resolve().parents[1]
SAFE_RESTORE = ROOT / "scripts/wp2_p7b_service_restore_h2.sh"
H2_ENTRY = ROOT / "scripts/wp2_p7b_c_node_h2.py"
GOLDEN_RESTORE = ROOT / "scripts/wp2_golden_service_restore.sh"


class P7BH2SessionOwnershipTests(unittest.TestCase):
    def test_controller_in_ue_session_is_rejected(self):
        result = evaluate_controller_identity(
            controller_pid=4242,
            controller_session="ue",
            controller_process_name="python3.11",
            controller_host_role="UE",
        )
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertIn("CONTROLLER_IN_SERVICE_CLEANUP_SESSION:ue", result["failures"])

    def test_plain_ssh_or_external_controller_passes(self):
        for role in ("UE", "EXTERNAL"):
            result = evaluate_controller_identity(
                controller_pid=4242,
                controller_session="NONE",
                controller_process_name="python3.11",
                controller_host_role=role,
            )
            self.assertEqual(result["gate"], "PASS", result)
            self.assertEqual(result["CONTROLLER_SERVICE_SESSION_DISJOINTNESS"], "PASS")
            self.assertEqual(result["CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION"], "PASS")

    def test_controller_process_cannot_be_target_service(self):
        result = evaluate_controller_identity(
            controller_pid=4242,
            controller_session="NONE",
            controller_process_name="srsue",
            controller_host_role="UE",
        )
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertIn("CONTROLLER_PROCESS_COLLIDES_WITH_SERVICE:srsue", result["failures"])

    def test_pid_ownership_blocks_controller_collision(self):
        result = evaluate_pid_ownership(
            controller_pid=4242,
            controller_host_role="UE",
            target_host_role="UE",
            service_pids_by_name={"srsue": [4000, 4242]},
        )
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertTrue(any(x.startswith("CONTROLLER_PID_SELECTED_FOR_SERVICE_CLEANUP") for x in result["failures"]))
        self.assertFalse(result["DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED"])

    def test_pid_ownership_accepts_disjoint_exact_service_pids(self):
        result = evaluate_pid_ownership(
            controller_pid=4242,
            controller_host_role="UE",
            target_host_role="UE",
            service_pids_by_name={"srsue": [4000, 4001]},
        )
        self.assertEqual(result["gate"], "PASS", result)
        self.assertEqual(result["SERVICE_PID_OWNERSHIP_PROOF"], "PASS")

    def test_unapproved_process_target_is_rejected(self):
        result = evaluate_pid_ownership(
            controller_pid=4242,
            controller_host_role="EXTERNAL",
            target_host_role="CORE",
            service_pids_by_name={"python3": [9000]},
        )
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertIn("UNAPPROVED_SERVICE_PROCESS_TARGET:python3", result["failures"])

    def test_safe_restore_is_shell_syntax_valid(self):
        p = subprocess.run(["bash", "-n", str(SAFE_RESTORE)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_safe_restore_has_no_tmux_kill_session(self):
        text = SAFE_RESTORE.read_text(encoding="utf-8")
        self.assertNotIn("tmux kill-session", text)
        self.assertIn("DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO", text)
        self.assertIn("STALE_SERVICE_TMUX_SESSION", text)

    def test_safe_restore_uses_exact_pid_scoped_service_targets(self):
        text = SAFE_RESTORE.read_text(encoding="utf-8")
        self.assertIn("pgrep -x", text)
        self.assertIn("sudo kill -TERM", text)
        self.assertIn("sudo kill -KILL", text)
        self.assertIn("SERVICE_PID_OWNERSHIP_PROOF=PASS", text)
        for proc in ("srsue", "srsenb", "srsepc"):
            self.assertIn(proc, text)
        for dangerous in ("pkill -f", "killall", "pkill -TERM -x python", "pkill -KILL -x python"):
            self.assertNotIn(dangerous, text)

    def test_h2_entrypoint_binds_safe_restore_before_r2_main(self):
        text = H2_ENTRY.read_text(encoding="utf-8")
        bind = text.index("install_h2_safe_restore(identity)")
        run = text.index("return r2.main()")
        self.assertLess(bind, run)
        self.assertIn("wp2_p7b_service_restore_h2.sh", text)
        self.assertIn("CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS", text)
        self.assertIn("LIVE_AUTHORIZATION=SEPARATE_REQUIRED", text)
        self.assertIn("SCORED_AUTHORIZATION=BLOCKED", text)

    def test_historical_golden_restore_is_retained_as_provenance(self):
        text = GOLDEN_RESTORE.read_text(encoding="utf-8")
        self.assertIn("tmux kill-session -t ue", text)
        h2 = SAFE_RESTORE.read_text(encoding="utf-8")
        self.assertNotIn("tmux kill-session -t ue", h2)

    def test_h2_new_files_do_not_embed_frozen_rf_or_cell_controls(self):
        combined = SAFE_RESTORE.read_text(encoding="utf-8") + H2_ENTRY.read_text(encoding="utf-8")
        for token in ("Q0_DB", "Q1_DB", "Q2_DB", "Q3_DB", "ATTENUATORS", "P7B-B1-S3", "P7B-W1-S3", "P7B-B2-S3"):
            self.assertNotIn(token, combined)


if __name__ == "__main__":
    unittest.main()
