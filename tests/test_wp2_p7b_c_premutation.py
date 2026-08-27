from pathlib import Path
import subprocess
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

    def test_temporary_workflow_is_sentinel_only_and_fail_closed(self):
        text = (ROOT / ".github" / "workflows" / "wp2-p7b-c-live.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn('      - ".wp2-p7b-c-live-trigger"', text)
        self.assertIn("execute=WP2_P7B_C_LIVE_ONCE", text)
        self.assertIn("reservation_limit=1", text)
        self.assertIn("cells=P7B-B1-S3,P7B-W1-S3,P7B-B2-S3", text)
        self.assertIn("P7B-D: **NOT STARTED**", text)
        # The workflow may mention the forbidden command only as a negative
        # grep guard. Actual reservation/teardown authority lives in the
        # controller, which is checked independently above.
        self.assertIn(
            "! grep -q --fixed-strings 'portal-cli experiment terminate' powder/wp2_p7b_c_execute.sh",
            text,
        )
        self.assertNotIn("upload-artifact", text)


if __name__ == "__main__":
    unittest.main()
