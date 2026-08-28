from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "scripts/wp2_p7b_h2_adversarial_qa.py"
DELTA = ROOT / "experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json"


class P7BH2AdversarialQATests(unittest.TestCase):
    def test_adversarial_qa_script_passes_all_a7_cases_offline(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "report.json"
            p = subprocess.run(
                [sys.executable, str(QA), "--output", str(report)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=90,
            )
            self.assertEqual(p.returncode, 0, p.stdout + "\n" + p.stderr)
            data = json.loads(report.read_text(encoding="utf-8"))
            required = json.loads(DELTA.read_text(encoding="utf-8"))["controls"]["A7"]["required_cases"]
            self.assertEqual(data["required_cases"], required)
            self.assertEqual(data["gate"], "PASS")
            self.assertEqual(data["terminal_gate"], "H2_4_ADVERSARIAL_QA=PASS")
            self.assertEqual(set(data["cases"]), set(required))
            for case in required:
                self.assertEqual(data["cases"][case]["gate"], "PASS", case)
            self.assertFalse(data["powder_contact"])
            self.assertFalse(data["network_contact"])
            self.assertFalse(data["live_service_mutation"])
            self.assertFalse(data["rf_mutation"])
            self.assertFalse(data["retry"])
            self.assertFalse(data["scored"])
            self.assertFalse(data["teardown"])
            self.assertIn("H2_4_ADVERSARIAL_QA=PASS", p.stdout)

    def test_adversarial_qa_has_no_live_powder_authority_surface(self):
        text = QA.read_text(encoding="utf-8")
        self.assertNotIn("portal-cli experiment create", text)
        self.assertNotIn("portal-cli experiment terminate", text)
        self.assertNotIn("AUTOMATIC_RETRY=YES", text)
        self.assertNotIn("scored_runs_authorized=true", text)
        self.assertIn('"network_contact": False', text)
        self.assertIn('"powder_contact": False', text)

    def test_restore_fault_matrix_covers_every_destructive_or_start_phase_plus_probe(self):
        text = QA.read_text(encoding="utf-8")
        for fault in ("UE_CLEANUP", "CORE_CLEANUP", "CORE_START", "CORE_STABLE", "UE_START", "UE_READY", "SERVICE_READY_PROBE"):
            self.assertIn(fault, text)

    def test_restart_adversarial_case_uses_real_h2_instrumentation_and_requires_pid_change(self):
        text = QA.read_text(encoding="utf-8")
        self.assertIn("install_h2_frontier_instrumentation()", text)
        self.assertIn('"restart_transition.json"', text)
        self.assertIn('obj["old_gateway_pid"] == obj["new_gateway_pid"]', text)
        self.assertIn("SYNTHETIC_FAILURE_AFTER_RESTART_TRANSITION", text)


if __name__ == "__main__":
    unittest.main()
