import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.powder_analysis import H_APP_S, reconstruct_primary_endpoint


class PowderAnalysisTests(unittest.TestCase):
    def _write_run(
        self,
        generated,
        received,
        rf_restore="2026-08-24T10:02:00Z",
        service_ready="2026-08-24T10:03:00Z",
        app_complete=None,
        h_app_s=300,
        declared_horizon=None,
    ):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        manifest = {
            "run_id": "TEST-RUN",
            "t_rf_restore_utc": rf_restore,
            "t_service_ready_utc": service_ready,
            "h_app_s": h_app_s,
        }
        if app_complete is not None:
            manifest["t_app_complete_utc"] = app_complete
        if declared_horizon is not None:
            manifest["horizon_end_utc"] = declared_horizon
        (root / "run_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        with (root / "telemetry_generated.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["record_id", "generated_ts_utc", "payload_sha256"])
            w.writeheader(); w.writerows(generated)
        with (root / "telemetry_received.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["record_id", "received_ts_utc", "payload_sha256"])
            w.writeheader(); w.writerows(received)
        self.addCleanup(td.cleanup)
        return root

    def test_rf_restore_freezes_primary_denominator_and_service_ready_anchors_300s_horizon(self):
        generated = [
            {"record_id":"r1","generated_ts_utc":"2026-08-24T10:00:00Z","payload_sha256":"a"},
            {"record_id":"r2","generated_ts_utc":"2026-08-24T10:02:00Z","payload_sha256":"b"},
            {"record_id":"r3","generated_ts_utc":"2026-08-24T10:02:01Z","payload_sha256":"c"},
        ]
        received = [
            {"record_id":"r1","received_ts_utc":"2026-08-24T10:07:59Z","payload_sha256":"a"},
            {"record_id":"r2","received_ts_utc":"2026-08-24T10:08:00Z","payload_sha256":"b"},
            {"record_id":"r3","received_ts_utc":"2026-08-24T10:04:00Z","payload_sha256":"c"},
        ]
        r = reconstruct_primary_endpoint(self._write_run(generated, received))
        self.assertEqual(H_APP_S, 300)
        self.assertEqual(r.cohort_generated, 2)
        self.assertEqual(r.unique_valid_received_by_300, 2)
        self.assertEqual(r.completeness_300, 1.0)
        self.assertEqual(r.horizon_end_utc, "2026-08-24T10:08:00+00:00")
        self.assertEqual(r.T_service_s, 60.0)

    def test_duplicate_corrupt_unexpected_and_post_horizon_attempts_are_separated(self):
        generated = [
            {"record_id":"r1","generated_ts_utc":"2026-08-24T10:00:00Z","payload_sha256":"a"},
            {"record_id":"r2","generated_ts_utc":"2026-08-24T10:01:00Z","payload_sha256":"b"},
            {"record_id":"r3","generated_ts_utc":"2026-08-24T10:02:00Z","payload_sha256":"c"},
        ]
        received = [
            {"record_id":"r2","received_ts_utc":"2026-08-24T10:03:10Z","payload_sha256":"b"},
            {"record_id":"r1","received_ts_utc":"2026-08-24T10:03:20Z","payload_sha256":"a"},
            {"record_id":"r1","received_ts_utc":"2026-08-24T10:03:21Z","payload_sha256":"a"},
            {"record_id":"r3","received_ts_utc":"2026-08-24T10:03:30Z","payload_sha256":"WRONG"},
            {"record_id":"rx","received_ts_utc":"2026-08-24T10:03:40Z","payload_sha256":"x"},
            {"record_id":"r3","received_ts_utc":"2026-08-24T10:08:01Z","payload_sha256":"c"},
        ]
        r = reconstruct_primary_endpoint(self._write_run(generated, received))
        self.assertEqual(r.cohort_generated, 3)
        self.assertEqual(r.unique_valid_received_by_300, 2)
        self.assertAlmostEqual(r.completeness_300, 2/3)
        self.assertEqual(r.missing_count, 1)
        self.assertEqual(r.duplicate_attempt_count, 1)
        self.assertEqual(r.checksum_mismatch_attempt_count, 1)
        self.assertEqual(r.unexpected_record_attempt_count, 1)
        self.assertEqual(r.out_of_order_attempt_count, 1)

    def test_recovery_clocks_are_reported_without_changing_primary_horizon(self):
        generated = [{"record_id":"r1","generated_ts_utc":"2026-08-24T10:02:00Z","payload_sha256":"a"}]
        received = [{"record_id":"r1","received_ts_utc":"2026-08-24T10:04:00Z","payload_sha256":"a"}]
        r = reconstruct_primary_endpoint(self._write_run(
            generated,
            received,
            app_complete="2026-08-24T10:04:30Z",
        ))
        self.assertEqual(r.T_service_s, 60.0)
        self.assertEqual(r.T_app_s, 90.0)
        self.assertEqual(r.T_total_s, 150.0)
        self.assertEqual(r.horizon_end_utc, "2026-08-24T10:08:00+00:00")

    def test_non_300_application_horizon_is_rejected(self):
        generated = [{"record_id":"r1","generated_ts_utc":"2026-08-24T10:01:00Z","payload_sha256":"a"}]
        with self.assertRaises(ValueError):
            reconstruct_primary_endpoint(self._write_run(generated, [], h_app_s=120))

    def test_inconsistent_declared_horizon_is_rejected(self):
        generated = [{"record_id":"r1","generated_ts_utc":"2026-08-24T10:01:00Z","payload_sha256":"a"}]
        with self.assertRaises(ValueError):
            reconstruct_primary_endpoint(self._write_run(
                generated,
                [],
                declared_horizon="2026-08-24T10:05:00Z",
            ))

    def test_empty_primary_cohort_is_invalid(self):
        generated = [{"record_id":"r1","generated_ts_utc":"2026-08-24T10:03:00Z","payload_sha256":"a"}]
        with self.assertRaises(ValueError):
            reconstruct_primary_endpoint(self._write_run(generated, []))


if __name__ == "__main__":
    unittest.main()
