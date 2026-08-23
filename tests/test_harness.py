import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from wellpulse.harness import run_local_scenario

class HarnessTests(unittest.TestCase):
    def test_w1_recovers_outage_restart(self):
        r = run_local_scenario(1000, "W1_offline_first", "C2_outage_restart")
        self.assertEqual(r["generated"], 1000)
        self.assertEqual(r["received_unique"], 1000)
        self.assertEqual(r["duplicates"], 0)
        self.assertEqual(r["missing"], [])

    def test_b0_normal_path(self):
        r = run_local_scenario(1000, "B0_publish_only", "C0_normal_no_restart")
        self.assertEqual(r["received_unique"], 1000)
        self.assertEqual(r["missing"], [])

if __name__ == "__main__":
    unittest.main()
