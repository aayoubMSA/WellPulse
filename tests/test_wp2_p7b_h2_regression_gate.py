from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/wp2_p7b_h2_regression_gate.py"
PREFLIGHT = ROOT / "scripts/wp2_p7b_target_node_preflight.sh"
BASE = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
RUNTIME = ROOT / "experiments/WP-PWD01/p7b-target-runtime-contract-v2.json"
MODULAR = ROOT / "experiments/WP-PWD01/p7b-modular-pipeline-contract-v1.json"
ACTIVATION = ROOT / "experiments/WP-PWD01/p7b-rq2-live-authorization-2026-08-28.json"
H25_EVIDENCE = ROOT / "evidence/powder/wp2-p7b-h2-5-regression.json"


class P7BH2RegressionGateTests(unittest.TestCase):
    def test_integrated_regression_gate_passes_offline(self):
        if ACTIVATION.exists():
            data = json.loads(H25_EVIDENCE.read_text(encoding="utf-8"))
            self.assertEqual(data["terminal_verdict"], "H2_5_REGRESSION=PASS")
            self.assertEqual(data["github_qa"]["suite_tests"], 168)
            self.assertEqual(data["integration_findings"]["live_p7b_workflow_present"], False)
            return
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "h2-5.json"
            p = subprocess.run(
                [sys.executable, str(GATE), "--output", str(report)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(p.returncode, 0, p.stdout + "\n" + p.stderr)
            data = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(data["gate"], "PASS")
            self.assertEqual(data["terminal_gate"], "H2_5_REGRESSION=PASS")

    def test_target_preflight_covers_h2_prospective_sources_and_restore(self):
        text = PREFLIGHT.read_text(encoding="utf-8")
        self.assertIn("scripts/wp2_p7b_c_node_h2.py", text)
        self.assertIn("src/wellpulse/p7b_session_ownership.py", text)
        self.assertIn('h2_restore="$REPO/scripts/wp2_p7b_service_restore_h2.sh"', text)
        self.assertIn('bash -n "$h2_restore"', text)
        self.assertIn("H2_DEPENDS_ON_SYSTEM_PYTHON", text)
        self.assertIn("H2_DEPENDS_ON_REMOTE_JQ", text)
        p = subprocess.run(["bash", "-n", str(PREFLIGHT)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)

    def test_frozen_contracts_remain_exact_offline_authority(self):
        base = json.loads(BASE.read_text(encoding="utf-8"))
        runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
        modular = json.loads(MODULAR.read_text(encoding="utf-8"))
        self.assertFalse(base["live_authorized"])
        self.assertFalse(base["scored_runs_authorized"])
        self.assertFalse(base["authority"]["automatic_retry"])
        self.assertFalse(runtime["live_authorized"])
        self.assertFalse(runtime["scored_runs_authorized"])
        self.assertFalse(modular["live_authorized"])
        self.assertFalse(modular["retry_authorized"])
        self.assertFalse(modular["teardown_authorized"])
        self.assertEqual(
            runtime["base_executable_contract"]["git_blob_sha"],
            "233aabeaf3081470bc3ebc1ee04168f8932fc415",
        )

    def test_modular_pipeline_still_requires_h2_and_separate_live_authority(self):
        modular = json.loads(MODULAR.read_text(encoding="utf-8"))
        self.assertEqual(sum(x["weight_pct"] for x in modular["h2_offline_modules"]), 100)
        self.assertEqual(
            modular["architecture"]["workflow_creation_policy"],
            "CREATE_ONLY_AFTER_H2_PASS_AND_SEPARATE_EXPLICIT_USER_LIVE_AUTHORIZATION",
        )
        self.assertFalse(modular["architecture"]["automatic_retry"])
        self.assertFalse(modular["architecture"]["automatic_reservation_create"])
        self.assertFalse(modular["architecture"]["automatic_teardown"])
        self.assertEqual(modular["ci_state_contract"]["ssh_agent_scope"], "PER_JOB_ONLY")

    def test_h2_5_no_live_surface_is_historical_and_post_h2_activation_is_explicit(self):
        actual = {p.name for p in (ROOT / ".github/workflows").glob("*.yml")}
        offline = {
            "local-gate-once.yml",
            "local-unit-tests.yml",
            "wp2-b2-semantics.yml",
            "wp2-golden-offline-qa.yml",
            "wp2-offpowder-artifact-qa.yml",
            "wp2-preintegration-static.yml",
        }
        if not ACTIVATION.exists():
            self.assertEqual(actual, offline)
            self.assertFalse((ROOT / ".github/workflows/wp2-p7b-rq2-session.yml").exists())
            return
        activation = json.loads(ACTIVATION.read_text(encoding="utf-8"))
        self.assertTrue(activation["user_live_authorization_received"])
        self.assertEqual(actual, offline | {"wp2-p7b-rq2-session.yml"})
        workflow = ROOT / ".github/workflows/wp2-p7b-rq2-session.yml"
        self.assertTrue(workflow.exists())
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("push:", text)
        self.assertNotIn("schedule:", text)


if __name__ == "__main__":
    unittest.main()
