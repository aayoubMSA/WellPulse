from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

from wellpulse.p7b_contract_v2 import load_contract
from wellpulse.p7b_runtime_compat import parse_attenuator_set_evidence, evaluate_readiness_v2

ROOT = Path(__file__).resolve().parents[1]
EXEC = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
RUNTIME = ROOT / "experiments/WP-PWD01/p7b-target-runtime-contract-v2.json"
MATRIX = ROOT / "docs/WP2_POWDER_RUNTIME_COMPATIBILITY_MATRIX_2026-08-28.md"


def shell_executable_text(text: str) -> str:
    return "\n".join(raw for raw in text.splitlines() if raw.strip() and not raw.lstrip().startswith("#"))


class P7BR3CTargetRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exec_contract = load_contract(EXEC)
        cls.runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
        cls.matrix = MATRIX.read_text(encoding="utf-8")

    def test_efcc_evidence_is_pinned(self):
        efcc = self.runtime["efcc_evidence"]
        self.assertEqual(efcc["github_run_id"], 33124645486)
        self.assertEqual(efcc["artifact_id"], 9667857505)
        self.assertEqual(efcc["artifact_zip_sha256"], "e0a1923af8ff1ffbbdf5bb20641f01ec9f81e5d96c67b0328260063f14848245")
        self.assertEqual(efcc["inner_inventory_tar_sha256"], "b94c958a0b23bf812892680372485e6710b8f74b8368ea1c5c109e9f34d5541d")
        for value in (str(efcc["github_run_id"]), str(efcc["artifact_id"]), efcc["artifact_zip_sha256"], efcc["inner_inventory_tar_sha256"]):
            self.assertIn(value, self.matrix)
        self.assertTrue(efcc["read_only"])
        for flag in ("new_reservation", "rf_mutation", "cells", "restart", "teardown", "scored"):
            self.assertFalse(efcc[flag])

    def test_runtime_contract_supersedes_v1_only_prospectively(self):
        sup = self.runtime["supersession"]
        self.assertEqual(sup["historical_runtime_contract_retained"], "experiments/WP-PWD01/p7b-target-runtime-contract-v1.json")
        self.assertEqual(sup["prospective_runtime_contract"], "experiments/WP-PWD01/p7b-target-runtime-contract-v2.json")
        self.assertFalse(self.runtime["live_authorized"])
        self.assertFalse(self.runtime["scored_runs_authorized"])

    def test_observed_system_python_is_prohibited_and_pinned_runtime_required(self):
        for role in ("ue", "core"):
            r = self.runtime["roles"][role]
            self.assertEqual(r["system_python_observed"], "3.6.9")
            self.assertFalse(r["system_python_project_code_allowed"])
            self.assertEqual(r["project_python_exact"], "3.11.13")
            self.assertEqual(r["paho_mqtt_exact"], "2.1.0")
            self.assertEqual(r["python_metadata_interface"], "importlib.metadata")
            self.assertFalse(r["pkg_resources_required"])
            self.assertTrue(r["remote_jq_dependency_prohibited"])

    def test_role_specific_tools_are_not_assumed_symmetric(self):
        ue = self.runtime["roles"]["ue"]
        core = self.runtime["roles"]["core"]
        self.assertTrue(ue["java_required"])
        self.assertEqual(ue["java_major"], 11)
        self.assertFalse(core["java_required"])
        self.assertFalse(ue["mosquitto_daemon_required"])
        self.assertTrue(core["mosquitto_daemon_required"])
        self.assertEqual(core["mosquitto_version_observed"], "1.4.15")

    def test_b2_java_jar_is_pre_rf_hash_gated(self):
        b2 = self.runtime["b2_java_dependency"]
        self.assertEqual(b2["role"], "ue")
        self.assertTrue(b2["pre_rf_hash_verification_required"])
        self.assertEqual(b2["jar_sha256"], "59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185")

    def test_shell_preservation_helper_has_zero_python_or_jq_dependency(self):
        helper = ROOT / "scripts/wp2_p7b_preservation_helpers_v2.sh"
        executable = shell_executable_text(helper.read_text(encoding="utf-8"))
        self.assertNotRegex(executable, r"(^|[;&|()\s])python3([;&|()\s]|$)")
        self.assertNotRegex(executable, r"(^|[;&|()\s])jq([;&|()\s]|$)")
        p = subprocess.run(["bash", "-n", str(helper)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_real_failed_run_set_fixture_is_accepted_without_readback_claim(self):
        fixture = "\n".join([
            "SET id=1 db=0 rc=0 output=changing attenuation",
            "SET id=33 db=0 rc=0 output=changing attenuation",
            "SET id=2 db=0 rc=0 output=changing attenuation",
            "SET id=34 db=0 rc=0 output=changing attenuation",
        ])
        result = parse_attenuator_set_evidence(fixture, [1, 33, 2, 34], 0)
        self.assertTrue(result["set_ack_pass"])
        self.assertFalse(result["physical_db_readback_supported"])
        self.assertFalse(result["physical_db_readback_claim"])

    def test_bad_attenuator_id_or_db_fails_closed(self):
        bad = "SET id=1 db=0 rc=0 output=changing attenuation\nSET id=33 db=0 rc=0 output=changing attenuation\nSET id=2 db=0 rc=0 output=changing attenuation\nSET id=99 db=0 rc=0 output=changing attenuation\n"
        self.assertFalse(parse_attenuator_set_evidence(bad, [1, 33, 2, 34], 0)["set_ack_pass"])
        wrong_db = bad.replace("id=99 db=0", "id=34 db=55")
        self.assertFalse(parse_attenuator_set_evidence(wrong_db, [1, 33, 2, 34], 0)["set_ack_pass"])

    def test_synthetic_readiness_passes_with_set_ack_plus_independent_q0_evidence(self):
        fixture = "\n".join(f"SET id={i} db=0 rc=0 output=changing attenuation" for i in [1, 33, 2, 34])
        control = parse_attenuator_set_evidence(fixture, [1, 33, 2, 34], 0)
        obs = {
            "attenuation_control": control,
            "route_output": "172.16.0.1 dev tun_srsue src 172.16.0.2",
            "probe_packet_loss_pct": [0.0] * 5,
            "tls_mqtt_probe_pass": True,
            "cell_unique_namespace": True,
            "initial_session_present": False,
            "architecture_state_fresh": True,
            "prior_process_or_session_residue": False,
            "runtime_config_ca_broker_lock_pass": True,
            "clock_capture_healthy": True,
            "evidence_path_armed": True,
            "radio_metrics": {"captured": True, "rsrp_dbm": None, "dl_snr_db": None, "absence_reason": "not exposed by live console"},
        }
        verdict = evaluate_readiness_v2(obs, self.exec_contract.legacy_qualification_view())
        self.assertTrue(verdict.passed, verdict.failures)

    def test_r2_entrypoint_enforces_efcc_runtime_v2(self):
        text = (ROOT / "scripts/wp2_p7b_c_node_r2.py").read_text(encoding="utf-8")
        for marker in (
            "TARGET_PROJECT_PYTHON_MISMATCH", "TARGET_PAHO_MQTT_MISMATCH", "importlib.metadata",
            "wp2_p7b_validate_readiness_v2.py", "READBACK_CAPABILITY=UNSUPPORTED_BY_OBSERVED_TMCC_INTERFACE",
            "PHYSICAL_DB_READBACK_CLAIM=NO", "p7b-target-runtime-contract-v2.json", "P7B_EFCC_BINDING=PASS",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("p7b-target-runtime-contract-v1.json", text)

    def test_preflight_encodes_observed_target_delta(self):
        script = (ROOT / "scripts/wp2_p7b_target_node_preflight.sh").read_text(encoding="utf-8")
        for marker in (
            "3.6.9", "3.11.13", "PAHO_MQTT=", "B2_JAR_PATH_NOT_SUPPLIED", "REMOTE_JQ_DEPENDENCY=PROHIBITED",
            "PYTHON_METADATA_INTERFACE=importlib.metadata", "EFCC_RUNTIME_BINDING=PASS", "FIXTURE_ONLY_NO_LIVE_TMCC_READBACK",
        ):
            self.assertIn(marker, script)
        self.assertNotIn("/usr/local/etc/emulab/tmcc attenuator", script)
        p = subprocess.run(["bash", "-n", str(ROOT / "scripts/wp2_p7b_target_node_preflight.sh")], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.returncode, 0, p.stdout)

    def test_portal_and_cross_step_semantics_are_fail_closed(self):
        portal = self.runtime["portal_policy"]
        self.assertEqual(portal["generic_get_error_semantic"], "UNKNOWN_CONTROL_PLANE_STATE")
        self.assertTrue(portal["generic_get_error_may_not_confirm_teardown"])
        gha = self.runtime["github_actions_policy"]
        self.assertTrue(gha["ssh_agent_cross_step_persistence_prohibited"])
        self.assertTrue(gha["background_process_cross_step_persistence_prohibited"])

    def test_efcc_blocks_live_on_unknown_or_mismatch(self):
        gate = self.runtime["efcc_gate"]
        self.assertTrue(gate["target_runtime_is_compatibility_baseline"])
        self.assertTrue(gate["contract_delta_audit_only"])
        self.assertEqual(set(gate["blocks_live_on_required_dependency_states"]), {"MISSING", "UNKNOWN", "VERSION_INCOMPATIBLE", "ROLE_MISMATCH", "UNTESTED"})

    def test_target_runtime_contract_is_pinned_to_scientific_contract_blob(self):
        expected = self.runtime["base_executable_contract"]["git_blob_sha"]
        p = subprocess.run(["git", "hash-object", str(EXEC)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertEqual(p.stdout.strip(), expected)

    def test_static_target_runtime_qa_script_passes(self):
        p = subprocess.run(["python3", str(ROOT / "scripts/wp2_p7b_target_runtime_qa.py")], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn("WP2_P7B_TARGET_RUNTIME_QA=PASS", p.stdout)
        self.assertIn("EFCC_CONTRACT_DELTA=PASS", p.stdout)
        self.assertIn("LIVE_AUTHORIZATION=BLOCKED", p.stdout)


if __name__ == "__main__":
    unittest.main()
