import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.harness import run_local_scenario


class HarnessTests(unittest.TestCase):
    RECORDS = 6000  # Extends beyond the frozen 3001-5000 outage window.

    def test_w1_recovers_network_outage(self):
        r = run_local_scenario(self.RECORDS, "W1_offline_first", "C1_outage_no_restart")
        self.assertEqual(r["generated"], self.RECORDS)
        self.assertEqual(r["received_unique"], self.RECORDS)
        self.assertEqual(r["duplicates"], 0)
        self.assertEqual(r["missing"], [])

    def test_w1_recovers_outage_and_process_restart(self):
        r = run_local_scenario(self.RECORDS, "W1_offline_first", "C2_outage_restart")
        self.assertEqual(r["generated"], self.RECORDS)
        self.assertEqual(r["received_unique"], self.RECORDS)
        self.assertEqual(r["duplicates"], 0)
        self.assertEqual(r["missing"], [])
        self.assertEqual(r["restart_count"], 1)

    def test_b1_volatile_baseline_recovers_network_only_outage(self):
        r = run_local_scenario(self.RECORDS, "B1_mqtt_qos1_volatile", "C1_outage_no_restart")
        self.assertEqual(r["received_unique"], self.RECORDS)
        self.assertEqual(r["missing"], [])
        self.assertEqual(r["restart_dropped"], 0)

    def test_b1_volatile_baseline_loses_only_pre_restart_pending_state(self):
        r = run_local_scenario(self.RECORDS, "B1_mqtt_qos1_volatile", "C2_outage_restart")
        # Outage begins at 3001; restart occurs after record 4000, so exactly
        # 1000 volatile pending records are lost. Records 4001-5000 queue in
        # the restarted process and are delivered when connectivity returns.
        self.assertEqual(r["received_unique"], self.RECORDS - 1000)
        self.assertEqual(len(r["missing"]), 1000)
        self.assertEqual(r["restart_dropped"], 1000)
        self.assertEqual(r["restart_count"], 1)

    def test_b0_publish_only_loses_entire_outage_window(self):
        r = run_local_scenario(self.RECORDS, "B0_publish_only", "C1_outage_no_restart")
        self.assertEqual(r["received_unique"], self.RECORDS - 2000)
        self.assertEqual(len(r["missing"]), 2000)

    def test_b0_normal_path(self):
        r = run_local_scenario(self.RECORDS, "B0_publish_only", "C0_normal_no_restart")
        self.assertEqual(r["received_unique"], self.RECORDS)
        self.assertEqual(r["missing"], [])


if __name__ == "__main__":
    unittest.main()
