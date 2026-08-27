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
        forbidden_runtime_tokens = (
            "portal-cli experiment create",
            "portal-cli experiment terminate",
            "portal-cli experiment start",
            "tmcc attenuator ",
        )
        executable_lines = []
        in_heredoc = False
        for raw in text.splitlines():
            line = raw.strip()
            if line == "REMOTE":
                in_heredoc = False
                continue
            if "<<'REMOTE'" in raw:
                in_heredoc = True
            if not line or line.startswith("#"):
                continue
            executable_lines.append(raw)
        runtime = "\n".join(executable_lines)
        for token in forbidden_runtime_tokens:
            self.assertNotIn(token, runtime)

    def test_probe_does_not_call_existing_p7b_control_stack(self):
        text = self.text()
        called = []
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            called.append(line)
        runtime = "\n".join(called)
        for token in (
            "powder/wp2_p7b_r3_execute.sh",
            "scripts/wp2_p7b_target_node_preflight.sh",
            "scripts/wp2_portal_client_bootstrap.sh",
            "scripts/wp2_p7b_validate_readiness",
            "scripts/wp2_p7b_r2_validate_controller.py",
        ):
            self.assertNotIn(token, runtime)

    def test_probe_keeps_ssh_agent_and_remote_checks_in_one_process(self):
        text = self.text()
        self.assertIn('eval "$(ssh-agent -s)"', text)
        self.assertIn("setsid -w ssh-add", text)
        self.assertIn("probe_node core", text)
        self.assertIn("probe_node ue", text)

    def test_probe_checks_exact_pinned_runtime_and_shell_preservation(self):
        text = self.text()
        self.assertIn('EXPECTED_PINNED_PYTHON="${EXPECTED_PINNED_PYTHON:-3.11.13}"', text)
        self.assertIn("PINNED_PYTHON=", text)
        self.assertIn("paho-mqtt", text)
        self.assertIn("SHELL_PRESERVATION_ROUNDTRIP", text)
        self.assertIn("sha256sum -c SHA256SUMS", text)

    def test_probe_has_no_workflow_or_trigger(self):
        workflows = ROOT / ".github" / "workflows"
        names = [p.name for p in workflows.glob("*independent*preflight*.yml")]
        self.assertEqual(names, [])
        triggers = list(ROOT.glob(".*independent*preflight*trigger*"))
        self.assertEqual(triggers, [])


if __name__ == "__main__":
    unittest.main()
