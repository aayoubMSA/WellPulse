from pathlib import Path
import json
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class P7BCPremutationSafetyTests(unittest.TestCase):
    def test_live_node_runner_is_bounded_and_non_scored(self):
        path = ROOT / "scripts" / "wp2_p7b_c_node.py"
        text = path.read_text(encoding="utf-8")
        compile(text, str(path), "exec")
        expected = ["P7B-B1-S3", "P7B-W1-S3", "P7B-B2-S3"]
        positions = [text.index(cell) for cell in expected]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('print("P7B_D=NOT_STARTED")', text)
        self.assertIn('print("TEARDOWN_AUTHORIZED=NO")', text)
        self.assertIn('"scored_runs_authorized": False', text)
        self.assertNotIn("/proj/WellPulse/evidence-escrow", text)
        self.assertNotIn("portal-cli experiment create", text)
        self.assertNotIn("portal-cli experiment terminate", text)
        self.assertNotIn("scored_runs_authorized=true", text)

    def test_python_gateway_can_restart_during_q3_outage(self):
        path = ROOT / "scripts" / "wp2_p7b_python_gateway.py"
        text = path.read_text(encoding="utf-8")
        compile(text, str(path), "exec")
        self.assertIn("session.client.connect_async", text)
        self.assertNotIn("session.connect()", text)
        self.assertIn("gateway_async_connect_armed", text)

    def test_b2_exposes_connack_session_state_and_buffer_count(self):
        text = (
            ROOT
            / "experiments"
            / "WP-PWD01"
            / "b2-semantics"
            / "P7BRemoteB2Gateway.java"
        ).read_text(encoding="utf-8")
        self.assertIn("getSessionPresent()", text)
        self.assertIn('"b2_connack"', text)
        self.assertIn("getBufferedMessageCount()", text)
        self.assertIn('private static final String PAHO_VERSION = "1.2.5"', text)

    def test_controller_has_one_reservation_and_no_teardown_authority(self):
        path = ROOT / "powder" / "wp2_p7b_c_execute.sh"
        text = path.read_text(encoding="utf-8")
        result = subprocess.run(
            ["bash", "-n", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(text.count("portal-cli experiment create"), 1)
        self.assertNotIn("portal-cli experiment terminate", text)
        self.assertIn("--duration 2", text)
        self.assertIn("P7B_D=NOT_STARTED", text)
        self.assertIn("TEARDOWN_AUTHORIZED=NO", text)
        self.assertNotIn("scored_runs_authorized=true", text)

    def test_p7b_live_workflow_is_retired_and_r1_has_no_authority(self):
        self.assertFalse((ROOT / ".github" / "workflows" / "wp2-p7b-c-live.yml").exists())
        path = ROOT / "scripts" / "wp2_p7b_c_node_r1.py"
        text = path.read_text(encoding="utf-8")
        compile(text, str(path), "exec")
        self.assertIn("base.start_receiver = start_receiver", text)
        self.assertIn("base.receiver_initial_session_false = receiver_initial_session_false", text)
        self.assertIn("base.run_cell = run_cell", text)
        self.assertNotIn("portal-cli experiment create", text)
        self.assertNotIn("portal-cli experiment terminate", text)
        self.assertNotIn("scored_runs_authorized=true", text)

    def test_r1_receiver_path_contract_rejects_literal_home_and_matches_paths(self):
        script = ROOT / "scripts" / "wp2_p7b_path_contract.py"
        good = subprocess.run(
            [
                sys.executable,
                str(script),
                "receiver",
                "--core-cell-dir",
                "/users/aayoub/wellpulse-powder-evidence/p7b/run-core/cells/P7B-B1-S3",
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        self.assertEqual(good.returncode, 0, good.stdout)
        first = good.stdout.splitlines()[0]
        contract = json.loads(first)
        self.assertTrue(contract["writer_watcher_path_equal"])
        self.assertFalse(contract["contains_unexpanded_shell_token"])
        self.assertEqual(
            contract["receiver_event_writer_path"],
            contract["receiver_event_watcher_path"],
        )
        self.assertNotIn("$HOME", json.dumps(contract))

        bad = subprocess.run(
            [sys.executable, str(script), "validate", "--path", "$HOME/bad"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("REMOTE_PATH_UNEXPANDED_SHELL_TOKEN", bad.stdout)

    def test_r1_receiver_startup_is_fail_fast_and_diagnostics_are_bounded(self):
        path = ROOT / "scripts" / "wp2_p7b_c_node_r1.py"
        text = path.read_text(encoding="utf-8")
        self.assertIn("kill -0", text)
        self.assertIn("RECEIVER_EXITED_BEFORE_CONNECT", text)
        self.assertIn("RECEIVER_CONNECT_TIMEOUT", text)
        for required in (
            "receiver process state",
            "receiver console tail",
            "receiver events tail",
            "broker log tail",
            "route",
            "Q0 probes",
            "TLS/MQTT probe",
            "runtime/version locks",
            "PAHO_MQTT",
            "PAHO_JAVA_JAR_SHA256",
        ):
            self.assertIn(required, text)
        self.assertIn("tail -n 100", text)
        self.assertIn("tail -n 120", text)

    def test_r1_preservation_helpers_fail_closed_on_unexpanded_paths(self):
        helper = ROOT / "scripts" / "wp2_p7b_preservation_helpers.sh"
        syntax = subprocess.run(
            ["bash", "-n", str(helper)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        self.assertEqual(syntax.returncode, 0, syntax.stdout)

        good = subprocess.run(
            [
                "bash",
                "-lc",
                "source scripts/wp2_p7b_preservation_helpers.sh; "
                "p7b_require_absolute_remote_path /users/aayoub/evidence",
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        self.assertEqual(good.returncode, 0, good.stdout)

        bad = subprocess.run(
            [
                "bash",
                "-lc",
                "source scripts/wp2_p7b_preservation_helpers.sh; "
                "p7b_require_absolute_remote_path '$HOME/evidence'",
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        self.assertNotEqual(bad.returncode, 0)

    def test_r1_is_operational_only_and_preserves_frozen_science(self):
        wrapper = (ROOT / "scripts" / "wp2_p7b_c_node_r1.py").read_text(encoding="utf-8")
        base = (ROOT / "scripts" / "wp2_p7b_c_node.py").read_text(encoding="utf-8")
        self.assertIn("Scientific cell", wrapper)
        self.assertIn("return base.main()", wrapper)
        for frozen in (
            "Q0_DB = 0",
            "Q3_DB = 55",
            "PRE_Q0_S = 60",
            "Q3_S = 120",
            "RESTART_OFFSET_S = 60",
            "H_APP_S = 300",
        ):
            self.assertIn(frozen, base)
        for forbidden in (
            "Q0_DB =",
            "Q3_DB =",
            "H_APP_S =",
            "portal-cli",
            "scored_runs_authorized=true",
        ):
            self.assertNotIn(forbidden, wrapper)


if __name__ == "__main__":
    unittest.main()
