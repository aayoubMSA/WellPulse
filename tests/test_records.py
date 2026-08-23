import sys, unittest, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from wellpulse.records import make_record
from wellpulse.store import DurableQueue
from wellpulse.reconcile import reconcile_ids

class WellPulseKernelTests(unittest.TestCase):
    def test_record_id_is_deterministic(self):
        r = make_record("RUN", "BOOT", 7)
        self.assertEqual(r.record_id, "RUN:BOOT:00000007")

    def test_queue_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            q = DurableQueue(Path(td)/"q.sqlite")
            r = make_record("RUN", "BOOT", 1)
            q.enqueue(r); q.enqueue(r)
            self.assertEqual(q.count(), 1)
            q.close()

    def test_reconciliation_detects_loss_and_duplicate(self):
        m = reconcile_ids(["a","b","c"], ["a","a","c"])
        self.assertEqual(m["duplicates"], 1)
        self.assertEqual(m["missing"], ["b"])

if __name__ == "__main__": unittest.main()
