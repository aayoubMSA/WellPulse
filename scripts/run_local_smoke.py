from pathlib import Path
import json, sys, tempfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from wellpulse.records import make_record
from wellpulse.store import DurableQueue
from wellpulse.reconcile import reconcile_ids

run_id = "LOCAL-SMOKE"
boot_id = "BOOT-001"
with tempfile.TemporaryDirectory() as td:
    q = DurableQueue(Path(td)/"queue.sqlite")
    records = [make_record(run_id, boot_id, i) for i in range(1, 101)]
    for r in records:
        q.enqueue(r)
    generated = [r.record_id for r in records]
    received = [row[0] for row in q.rows()]  # local plumbing stand-in, not remote evidence
    metrics = reconcile_ids(generated, received)
    q.close()
print(json.dumps(metrics, indent=2))
assert metrics["generated"] == 100
assert metrics["received_unique"] == 100
assert not metrics["missing"]
assert metrics["duplicates"] == 0
