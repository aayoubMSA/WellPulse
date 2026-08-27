import importlib.util
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
PYTHON_SCRIPTS = [
    ROOT / "scripts" / "wp_pwd01_h_receiver.py",
    ROOT / "scripts" / "wp_pwd01_h_sender.py",
    ROOT / "scripts" / "finalize_wp_pwd01_h_calibration.py",
]


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WP2HistoricalHPilotScriptTests(unittest.TestCase):
    def test_historical_python_scripts_remain_syntax_valid(self):
        for path in PYTHON_SCRIPTS:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")

    def test_historical_broker_shell_script_remains_syntax_valid(self):
        proc = subprocess.run(
            ["bash", "-n", str(ROOT / "powder" / "wp2_h_epc_broker.sh")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_historical_q0_packet_loss_parser_is_preserved_for_provenance(self):
        sender = load_script("h_sender", ROOT / "scripts" / "wp_pwd01_h_sender.py")
        self.assertTrue(sender.has_zero_packet_loss("5 packets transmitted, 5 received, 0% packet loss"))
        self.assertFalse(sender.has_zero_packet_loss("5 packets transmitted, 0 received, 100% packet loss"))

    def test_h_calibration_finalizer_is_fail_closed_after_amendment(self):
        module = load_script("h_finalize", ROOT / "scripts" / "finalize_wp_pwd01_h_calibration.py")
        self.assertEqual(module.H_APP_S, 300)
        self.assertEqual(module.main(), 64)

    def test_h_calibration_cli_refuses_execution(self):
        proc = subprocess.run(
            ["python", str(ROOT / "scripts" / "finalize_wp_pwd01_h_calibration.py")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(proc.returncode, 64, proc.stdout)
        self.assertIn("H_CALIBRATION_FINALIZER=BLOCKED_SUPERSEDED", proc.stdout)
        self.assertIn("OUTCOME_DERIVED_H_REESTIMATION=PROHIBITED", proc.stdout)


if __name__ == "__main__":
    unittest.main()
