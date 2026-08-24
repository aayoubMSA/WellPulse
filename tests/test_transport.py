import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.transport import PahoQoS1Config, PahoQoS1Session


class PahoTransportTests(unittest.TestCase):
    """Broker-free checks for the frozen WP-PWD01 low-level transport contract."""

    def test_frozen_public_config_is_reproducible_and_secret_safe(self):
        cfg = PahoQoS1Config(
            host="broker.example",
            username="user",
            password="secret-value",
            tls=False,
        )
        d = cfg.public_dict()
        self.assertEqual(d["paho_mqtt_version"], "2.1.0")
        self.assertEqual(d["mqtt_protocol"], "MQTTv311")
        self.assertEqual(d["qos"], 1)
        self.assertFalse(d["clean_session"])
        self.assertEqual(d["reconnect_min_delay_s"], 1)
        self.assertEqual(d["reconnect_max_delay_s"], 8)
        self.assertEqual(d["max_queued_messages"], 4096)
        self.assertEqual(d["max_inflight_messages"], 20)
        self.assertEqual(d["password"], "SET")
        self.assertNotIn("secret-value", json.dumps(d))

    def test_session_constructs_with_explicit_volatile_queue(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = PahoQoS1Config(host="127.0.0.1", port=1883, tls=False)
            session = PahoQoS1Session(
                cfg,
                client_id="wp-pwd01-test",
                event_log=Path(td) / "events.ndjson",
            )
            self.assertEqual(session.client.max_queued_messages, 4096)
            self.assertEqual(session.client.max_inflight_messages, 20)
            snap = session.snapshot()
            self.assertFalse(snap["connected"])
            self.assertEqual(snap["published_calls"], 0)
            self.assertEqual(snap["outstanding_mid_count"], 0)

    def test_unbounded_queue_is_rejected(self):
        cfg = PahoQoS1Config(host="127.0.0.1", tls=False, max_queued_messages=0)
        with self.assertRaises(ValueError):
            PahoQoS1Session(cfg, client_id="wp-pwd01-bad")


if __name__ == "__main__":
    unittest.main()
