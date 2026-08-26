import tempfile
import unittest
from pathlib import Path

from wellpulse.powder_w1 import DurablePahoReplay
from wellpulse.records import make_record
from wellpulse.store import DurableQueue


class FakeInfo:
    def __init__(self):
        self.done = False

    def is_published(self):
        return self.done


class FakeConfig:
    max_inflight_messages = 2


class FakeSession:
    def __init__(self):
        self.config = FakeConfig()
        self.connected = False
        self.published = []
        self.acks = 0

    def snapshot(self):
        return {
            "connected": self.connected,
            "published_calls": len(self.published),
            "puback_callbacks": self.acks,
        }

    def publish_async(self, payload_json):
        info = FakeInfo()
        self.published.append((payload_json, info))
        return info

    def close_at_horizon(self):
        pass


class DurablePahoReplayTests(unittest.TestCase):
    def test_does_not_hand_durable_backlog_to_paho_while_disconnected(self):
        with tempfile.TemporaryDirectory() as td:
            queue = DurableQueue(Path(td) / "q.sqlite")
            for seq in range(1, 4):
                queue.enqueue(make_record("R", "B", seq))
            session = FakeSession()
            replay = DurablePahoReplay(queue, session)

            snap = replay.pump_once()
            self.assertEqual(snap.pending_count, 3)
            self.assertEqual(snap.app_inflight_count, 0)
            self.assertEqual(len(session.published), 0)
            queue.close()

    def test_inflight_is_bounded_and_sent_only_after_ack(self):
        with tempfile.TemporaryDirectory() as td:
            queue = DurableQueue(Path(td) / "q.sqlite")
            for seq in range(1, 4):
                queue.enqueue(make_record("R", "B", seq))
            session = FakeSession()
            session.connected = True
            replay = DurablePahoReplay(queue, session)

            first = replay.pump_once()
            self.assertEqual(first.pending_count, 3)
            self.assertEqual(first.app_inflight_count, 2)
            self.assertEqual(len(session.published), 2)

            session.published[0][1].done = True
            session.acks = 1
            second = replay.pump_once()
            self.assertEqual(second.pending_count, 2)
            self.assertEqual(second.app_inflight_count, 2)
            self.assertEqual(len(session.published), 3)

            session.published[1][1].done = True
            session.published[2][1].done = True
            session.acks = 3
            final = replay.pump_once()
            self.assertEqual(final.pending_count, 0)
            self.assertEqual(final.app_inflight_count, 0)
            queue.close()


if __name__ == "__main__":
    unittest.main()
