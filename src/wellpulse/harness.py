from pathlib import Path
import tempfile
from .baseline import PublishOnlyBaseline, VolatileReconnectBaseline
from .receiver import IdempotentReceiver
from .records import make_record
from .reconcile import reconcile_ids
from .store import DurableQueue


def _link_up(sequence: int, condition: str) -> bool:
    if condition == "C0_normal_no_restart":
        return True
    if condition in {"C1_outage_no_restart", "C2_outage_restart"}:
        return not (3001 <= sequence <= 5000)
    raise ValueError(f"unknown condition: {condition}")


def run_local_scenario(record_count: int, architecture: str, condition: str) -> dict:
    run_id = f"LOCAL-{architecture}-{condition}"
    boot_id = "BOOT-001"
    generated_ids = []
    restart_count = 0
    restart_dropped = 0

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        receiver = IdempotentReceiver(td / "receiver.sqlite")

        if architecture == "B0_publish_only":
            baseline = PublishOnlyBaseline(receiver)
            for seq in range(1, record_count + 1):
                record = make_record(run_id, boot_id, seq)
                generated_ids.append(record.record_id)
                baseline.submit(record, _link_up(seq, condition))

        elif architecture == "B1_mqtt_qos1_volatile":
            baseline = VolatileReconnectBaseline(receiver)
            for seq in range(1, record_count + 1):
                record = make_record(run_id, boot_id, seq)
                generated_ids.append(record.record_id)
                baseline.submit(record, _link_up(seq, condition))
                if condition == "C2_outage_restart" and seq == 4000:
                    restart_dropped += baseline.restart()
                    restart_count += 1
            # The frozen local scenarios always restore connectivity before the
            # final record when record_count extends past the outage window.
            if _link_up(record_count, condition):
                baseline.flush()

        elif architecture == "W1_offline_first":
            queue_path = td / "queue.sqlite"
            queue = DurableQueue(queue_path)
            for seq in range(1, record_count + 1):
                record = make_record(run_id, boot_id, seq)
                generated_ids.append(record.record_id)
                queue.enqueue(record)
                if condition == "C2_outage_restart" and seq == 4000:
                    queue.close()
                    queue = DurableQueue(queue_path)
                    restart_count += 1
                if _link_up(seq, condition):
                    for row in queue.pending_rows():
                        record_id, payload_json, checksum, _state = row
                        receiver.ingest(record_id, payload_json, checksum)
                        queue.mark_sent(record_id, commit=False)
                    if seq % 100 == 0:
                        queue.commit_state()
            for row in queue.pending_rows():
                record_id, payload_json, checksum, _state = row
                receiver.ingest(record_id, payload_json, checksum)
                queue.mark_sent(record_id, commit=False)
            queue.commit_state()
            queue.close()

        else:
            raise ValueError(f"unknown architecture: {architecture}")

        metrics = reconcile_ids(generated_ids, receiver.ids())
        receiver.close()
        metrics.update(
            {
                "architecture": architecture,
                "condition": condition,
                "record_count": record_count,
                "restart_count": restart_count,
                "restart_dropped": restart_dropped,
            }
        )
        return metrics
