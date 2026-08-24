import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.powder_analysis import reconstruct_primary_endpoint


class PowderAnalysisTests(unittest.TestCase):
    def _write_run(self, generated, received, cutoff="2026-08-24T10:02:00Z", horizon="2026-08-24T10:04:00Z"):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "run_manifest.json").write_text(
            json.dumps({
                "run_id": "TEST-RUN",
                "cohort_cutoff_utc": cutoff,
                "horizon_end_utc": horizon,
            }),
            encoding="utf-8",
        )
        with (root / "telemetry_generated.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["record_id", "generated_ts_utc", "payload_sha256"])
            w.writeheader(); w.writerows(generated)
        with (root / "telemetry_received.csv").open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["record_id", "received_ts_utc", "payload_sha256"])
            w.writeheader(); w.writerows(received)
        self.addCleanup(td.cleanup)
        return root

    def test_post_cutoff_generation_is_not_in_primary_denominator(self):
        generated = [
            {"record_id":"r1","generated_ts_utc":"2026-08-24T10:00:00Z","payload_sha256":"a"},
            {"record_id":"r2","generated_ts_utc":"2026-08-24T10:02:00Z","payload_sha256":"b"},
            {"record_id":"r3","generated_ts_utc":"2026-08-24T10:03:00Z","payload_sha256":"c"},
        ]
        received = [
            {"record_id":"r1","received_ts_utc":"2026-08-24T10:03:00Z","payload_sha256":"a"},
            {"record_id":"r2","received_ts_utc":"2026-08-24T10:03:10Z","payload_sha256":"b"},
        ]
        r = reconstruct_primary_endpoint(self._write_run(generated, received))
        self.assertEqual(r.cohort_generated, 2)
        self.assertEqual(r.unique_valid_received_by_h, 2)
        self.assertEqual(r.completeness_h, 1.0)

    def test_duplicate_corrupt_unexpected_and_late_attempts_are_separated(self):
        generated = [
            {"record_id":"r1","generated_ts_utc":"2026-08-24T10:00:00Z","payload_sha256":"a"},
            {"record_id":"r2","generated_ts_utc":"2026-08-24T10:01:00Z","payload_sha256":"b"},
            {"record_id":"r3","generated_ts_utc":"2026-08-24T10:02:00Z","payload_sha256":"c"},
        ]
        received = [
            {"record_id":"r2","received_ts_utc":"2026-08-24T10:02:10Z","payload_sha256":"b"},
            {"record_id":"r1","received_ts_utc":"2026-08-24T10:02:20Z","payload_sha256":"a"},
            {"record_id":"r1","received_ts_utc":"2026-08-24T10:02:21Z","payload_sha256":"a"},
            {"record_id":"r3","received_ts_utc":"2026-08-24T10:02:30Z","payload_sha256":"WRONG"},
            {"record_id":"rx","received_ts_utc":"2026-08-24T10:02:40Z","payload_sha256":"x"},
            {"record_id":"r3","received_ts_utc":"2026-08-24T10:04:01Z","payload_sha256":"c"},
        ]
        r = reconstruct_primary_endpoint(self._write_run(generated, received))
        self.assertEqual(r.cohort_generated, 3)
        self.assertEqual(r.unique_valid_received_by_h, 2)
        self.assertAlmostEqual(r.completeness_h, 2/3)
        self.assertEqual(r.missing_count, 1)
        self.assertEqual(r.duplicate_attempt_count, 1)
        self.assertEqual(r.checksum_mismatch_attempt_count, 1)
        self.assertEqual(r.unexpected_record_attempt_count, 1)
        self.assertEqual(r.out_of_order_attempt_count, 1)

    def test_empty_primary_cohort_is_invalid(self):
        generated = [{"record_id":"r1","generated_ts_utc":"2026-08-24T10:03:00Z","payload_sha256":"a"}]
        with self.assertRaises(ValueError):
            reconstruct_primary_endpoint(self._write_run(generated, []))


if __name__ == "__main__":
    unittest.main()
