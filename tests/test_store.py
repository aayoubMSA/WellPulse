import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.records import Record, make_record
from wellpulse.store import DurableQueue


class DurableQueueIntegrityTests(unittest.TestCase):
    def test_exact_duplicate_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            queue = DurableQueue(Path(td) / "queue.sqlite")
            record = make_record("RUN-1", "BOOT-1", 1)
            self.assertTrue(queue.enqueue(record))
            self.assertFalse(queue.enqueue(record))
            self.assertEqual(queue.count(), 1)
            queue.close()

    def test_conflicting_duplicate_record_id_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            queue = DurableQueue(Path(td) / "queue.sqlite")
            original = Record(
                run_id="RUN-1",
                boot_id="BOOT-1",
                sequence=1,
                generated_at_utc="2026-08-26T08:00:00+00:00",
                source="sensor",
                payload={"value": 1},
            )
            conflicting = Record(
                run_id="RUN-1",
                boot_id="BOOT-1",
                sequence=1,
                generated_at_utc="2026-08-26T08:00:00+00:00",
                source="sensor",
                payload={"value": 2},
            )
            self.assertTrue(queue.enqueue(original))
            with self.assertRaisesRegex(ValueError, "record_id collision"):
                queue.enqueue(conflicting)
            self.assertEqual(queue.count(), 1)
            queue.close()


if __name__ == "__main__":
    unittest.main()
