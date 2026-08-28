from __future__ import annotations

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "scripts/wp2_p7b_rq2_module_adapter.py"


class P7BRQ2ModuleAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = ADAPTER.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.text, filename=str(ADAPTER))

    def test_adapter_is_python_syntax_valid_and_has_exact_five_module_choices(self):
        compile(self.text, str(ADAPTER), "exec")
        self.assertIn('choices=["prepare", "B1", "W1", "B2", "reconstruct"]', self.text)
        self.assertIn('"B1": ("P7B-B1-S3", "B1", 1, [])', self.text)
        self.assertIn('"W1": ("P7B-W1-S3", "W1", 2, ["P7B-B1-S3"])', self.text)
        self.assertIn('"B2": ("P7B-B2-S3", "B2", 3, ["P7B-B1-S3", "P7B-W1-S3"])', self.text)

    def test_adapter_reuses_h2_r2_r1_layers_instead_of_copying_science(self):
        required = [
            "h2.install_h2_frontier_instrumentation()",
            "h2.install_h2_safe_restore(identity)",
            "h2.install_supplementary_exit_hooks()",
            "r2.verify_target_interpreter_and_python_dependencies()",
            "r2.inject_contract_authority()",
            "r2.verify_injection()",
            "r2.install_observed_attenuator_interface()",
            "r2.install_contract_aware_writer()",
            "r2.install_contract_aware_run_router()",
            "base.start_receiver = r1.start_receiver",
            "base.receiver_initial_session_false = r1.receiver_initial_session_false",
            "base.run_cell = r1.run_cell",
        ]
        for token in required:
            self.assertIn(token, self.text)

    def test_adapter_pins_h2_and_frozen_contract_blobs(self):
        expected = {
            "d66bc791455127ef87497cea3e912ee6f46e685b",
            "fa506e661f90fe9c21418fd2f86c8ca0a9230175",
            "7810d1ed603fc305bd419c91a2b14bcca2e95e24",
            "72f465f274c86d7ec514f358023074aa26f96551",
            "233aabeaf3081470bc3ebc1ee04168f8932fc415",
            "9531893989effb142e694294b95c0c7146353742",
            "2c85af21f502c092c2da0ecb1bf615c8f705069b",
            "76522aa16d9af09d2f3d779a256236f752850245",
        }
        for sha in expected:
            self.assertIn(sha, self.text)

    def test_prepare_is_m3_known_good_q0_and_uses_pre_staged_b2_jar(self):
        for token in (
            'module_id = "M3_Q0_BASELINE"',
            "base.set_attenuation(base.Q0_DB",
            "base.restore_service(baseline, ca_file)",
            "base.route_and_probes(baseline)",
            'base.tls_mqtt_probe("P7B-RQ2-M3"',
            'require_env("WP_B2_JAR_STAGED")',
            '"M3_Q0_BASELINE_PASS"',
        ):
            self.assertIn(token, self.text)
        self.assertNotIn("repo.maven.apache.org", self.text)

    def test_each_scientific_module_calls_frozen_run_cell_once_and_preserves_order(self):
        fn = next(n for n in self.tree.body if isinstance(n, ast.FunctionDef) and n.name == "run_one_cell")
        calls = [
            n for n in ast.walk(fn)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and isinstance(n.func.value, ast.Name)
            and n.func.value.id == "base"
            and n.func.attr == "run_cell"
        ]
        self.assertEqual(len(calls), 1)
        self.assertIn("CELL_ORDER_OR_PRIOR_PASS_VIOLATION", self.text)
        self.assertIn("M3_Q0_BASELINE_NOT_PASS", self.text)

    def test_reconstruction_is_v2_non_scored_and_does_not_authorize_teardown(self):
        self.assertIn('str(ROOT / "scripts/reconstruct_wp2_p7b_v2.py")', self.text)
        self.assertIn('"PASS_NON_SCORED_PHYSICAL_QUALIFICATION"', self.text)
        self.assertIn('status["teardown_authorized"] = False', self.text)
        self.assertIn('print("SCORED_AUTHORIZATION=BLOCKED")', self.text)
        self.assertIn('print("TEARDOWN_AUTHORIZED=NO")', self.text)

    def test_adapter_contains_no_reservation_or_teardown_command_surface(self):
        lowered = self.text.lower()
        for forbidden in (
            "portal-cli experiment create",
            "portal-cli experiment terminate",
            "tmux kill-session",
            "killall",
            "automatic_retry=yes",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_module_results_are_machine_readable_and_authority_bound(self):
        for token in (
            '"schema_version": "wp2-p7b-rq2-module-result-v1"',
            '"authority_id": authority["authority_id"]',
            '"scientific_source_sha": authority["scientific_source_sha"]',
            '"evidence_class": "NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION"',
            '"scored": False',
            '"input_digest_sha256"',
            '"status_digest_sha256"',
        ):
            self.assertIn(token, self.text)


if __name__ == "__main__":
    unittest.main()
