import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
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


def write_trial_files(root: Path, summary: dict, received_rows: list[dict]) -> None:
    (root / "sender_summary.json").write_text(json.dumps(summary), encoding="utf-8")
    with (root / "telemetry_generated.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["record_id", "generated_ts_utc", "payload_sha256", "payload_json"],
        )
        writer.writeheader()
        writer.writerow({"record_id": "r1", "generated_ts_utc": "2026-08-26T00:00:08+00:00", "payload_sha256": "a", "payload_json": "{}"})
        writer.writerow({"record_id": "r2", "generated_ts_utc": "2026-08-26T00:00:10+00:00", "payload_sha256": "b", "payload_json": "{}"})
        writer.writerow({"record_id": "r3", "generated_ts_utc": "2026-08-26T00:00:11+00:00", "payload_sha256": "c", "payload_json": "{}"})

    with (root / "telemetry_received.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["record_id", "received_ts_utc", "payload_sha256", "payload_json"],
        )
        writer.writeheader()
        for row in received_rows:
            writer.writerow(row)


class WP2HPilotScriptTests(unittest.TestCase):
    def test_python_pilot_scripts_compile(self):
        for path in PYTHON_SCRIPTS:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")

    def test_broker_shell_script_passes_bash_syntax(self):
        proc = subprocess.run(
            ["bash", "-n", str(ROOT / "powder" / "wp2_h_epc_broker.sh")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_q0_packet_loss_parser_rejects_100_percent_loss(self):
        sender = load_script("h_sender", ROOT / "scripts" / "wp_pwd01_h_sender.py")
        self.assertTrue(sender.has_zero_packet_loss("5 packets transmitted, 5 received, 0% packet loss"))
        self.assertTrue(sender.has_zero_packet_loss("5 packets transmitted, 5 received, 0.0% packet loss"))
        self.assertFalse(sender.has_zero_packet_loss("5 packets transmitted, 0 received, 100% packet loss"))
        self.assertFalse(sender.has_zero_packet_loss("no packet-loss summary"))

    def test_finalizer_reconstructs_conservative_drain_time(self):
        module = load_script("h_finalize", ROOT / "scripts" / "finalize_wp_pwd01_h_calibration.py")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_trial_files(
                root,
                {
                    "run_id": "HCAL-T1",
                    "status": "QUEUE_DRAIN_OBSERVED_PENDING_SINK_RECONSTRUCTION",
                    "cohort_cutoff_utc": "2026-08-26T00:00:10+00:00",
                    "queue_pending_zero_utc": "2026-08-26T00:00:15+00:00",
                },
                [
                    {"record_id": "r1", "received_ts_utc": "2026-08-26T00:00:13+00:00", "payload_sha256": "a", "payload_json": "{}"},
                    {"record_id": "r2", "received_ts_utc": "2026-08-26T00:00:16+00:00", "payload_sha256": "b", "payload_json": "{}"},
                    {"record_id": "r3", "received_ts_utc": "2026-08-26T00:00:12+00:00", "payload_sha256": "c", "payload_json": "{}"},
                ],
            )

            result = module.reconstruct_trial(root)
            self.assertTrue(result["valid"])
            self.assertEqual(result["calibration_outcome"], module.VALID_W1_RECOVERY_SUCCESS)
            self.assertEqual(result["cohort_count"], 2)
            self.assertEqual(result["backlog_drain_time_s"], 6.0)

    def test_missing_cohort_record_is_valid_adverse_outcome_not_invalidity(self):
        module = load_script("h_finalize_failure", ROOT / "scripts" / "finalize_wp_pwd01_h_calibration.py")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_trial_files(
                root,
                {
                    "run_id": "HCAL-LOSS",
                    "status": "QUEUE_DRAIN_OBSERVED_PENDING_SINK_RECONSTRUCTION",
                    "cohort_cutoff_utc": "2026-08-26T00:00:10+00:00",
                    "queue_pending_zero_utc": "2026-08-26T00:00:15+00:00",
                },
                [
                    {"record_id": "r1", "received_ts_utc": "2026-08-26T00:00:13+00:00", "payload_sha256": "a", "payload_json": "{}"},
                ],
            )

            result = module.reconstruct_trial(root)
            self.assertFalse(result["valid"])
            self.assertEqual(result["technical_validity"], "PASS")
            self.assertEqual(result["calibration_outcome"], module.VALID_W1_RECOVERY_FAILURE)
            self.assertFalse(result["replacement_allowed"])
            self.assertEqual(result["missing_count"], 1)

    def test_predefined_sender_technical_failure_remains_replaceable(self):
        module = load_script("h_finalize_invalid", ROOT / "scripts" / "finalize_wp_pwd01_h_calibration.py")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_trial_files(
                root,
                {
                    "run_id": "HCAL-BAD-PATH",
                    "status": "INVALID_POST_Q0_USER_PLANE_HEALTH",
                    "cohort_cutoff_utc": "2026-08-26T00:00:10+00:00",
                    "queue_pending_zero_utc": "2026-08-26T00:00:15+00:00",
                },
                [],
            )

            result = module.reconstruct_trial(root)
            self.assertFalse(result["valid"])
            self.assertEqual(result["calibration_outcome"], module.TECHNICALLY_INVALID)
            self.assertTrue(result["replacement_allowed"])


if __name__ == "__main__":
    unittest.main()
