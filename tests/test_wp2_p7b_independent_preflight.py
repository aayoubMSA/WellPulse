from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "scripts" / "wp2_p7b_independent_preflight.sh"


class IndependentPreflightTests(unittest.TestCase):
    def text(self) -> str:
        return PROBE.read_text(encoding="utf-8")

    def test_probe_is_shell_syntax_valid(self):
        subprocess.run(["bash", "-n", str(PROBE)], check=True)

    def test_probe_has_no_portal_or_scientific_authority(self):
        text = self.text()
        for token in (
            "portal-cli experiment create",
            "portal-cli experiment terminate",
            "portal-cli experiment start",
            "tmcc attenuator ",
            "P7B-B1-S3",
            "P7B-W1-S3",
            "P7B-B2-S3",
        ):
            self.assertNotIn(token, text)

    def test_probe_does_not_call_existing_p7b_control_stack(self):
        text = self.text()
        for token in (
            "powder/wp2_p7b_r3_execute.sh",
            "scripts/wp2_p7b_target_node_preflight.sh",
            "scripts/wp2_portal_client_bootstrap.sh",
            "scripts/wp2_p7b_validate_readiness",
            "scripts/wp2_p7b_r2_validate_controller.py",
        ):
            self.assertNotIn(token, text)

    def test_probe_keeps_ssh_agent_and_remote_checks_in_one_process(self):
        text = self.text()
        self.assertIn('eval "$(ssh-agent -s)"', text)
        self.assertIn("setsid -w ssh-add", text)
        self.assertIn("probe_node core", text)
        self.assertIn("probe_node ue", text)

    def test_remote_defaults_are_resolved_on_target_not_github_runner(self):
        text = self.text()
        local_prefix = text.split("<<'REMOTE'", 1)[0]
        self.assertNotIn('$HOME/WellPulse', local_prefix)
        self.assertNotIn('$HOME/.wp2-golden-venv/bin/python', local_prefix)
        self.assertIn('REMOTE_REPO="${REMOTE_REPO_OVERRIDE:-$HOME/WellPulse}"', text)
        self.assertIn('REMOTE_PINNED_PYTHON="${REMOTE_PINNED_PYTHON_OVERRIDE:-$HOME/.wp2-golden-venv/bin/python}"', text)
        self.assertIn('REMOTE_REPO_UNRESOLVED_TOKEN', text)
        self.assertIn('REMOTE_PINNED_PYTHON_UNRESOLVED_TOKEN', text)

    def test_probe_checks_exact_pinned_runtime_and_shell_preservation(self):
        text = self.text()
        self.assertIn('EXPECTED_PINNED_PYTHON="${EXPECTED_PINNED_PYTHON:-3.11.13}"', text)
        self.assertIn("PINNED_PYTHON=", text)
        self.assertIn("paho-mqtt", text)
        self.assertIn("SHELL_PRESERVATION_ROUNDTRIP", text)
        self.assertIn("sha256sum -c SHA256SUMS", text)
        self.assertIn("/proj/WellPulse/.p7b-preflight-", text)

    def test_probe_does_not_self_parse_for_authority(self):
        text = self.text()
        self.assertNotIn('SELF="$0"', text)
        self.assertNotIn('for banned in', text)
        self.assertIn('INDEPENDENCE_STATIC_AUDIT=OFFLINE_QA', text)

    def test_probe_has_no_workflow_or_trigger(self):
        workflows = ROOT / ".github" / "workflows"
        names = [p.name for p in workflows.glob("*independent*preflight*.yml")]
        self.assertEqual(names, [])
        triggers = list(ROOT.glob(".*independent*preflight*trigger*"))
        self.assertEqual(triggers, [])


if __name__ == "__main__":
    unittest.main()
