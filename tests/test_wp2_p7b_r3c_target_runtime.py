from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

from wellpulse.p7b_contract_v2 import load_contract
from wellpulse.p7b_runtime_compat import parse_attenuator_set_evidence, evaluate_readiness_v2

ROOT = Path(__file__).resolve().parents[1]
EXEC = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
RUNTIME = ROOT / "experiments/WP-PWD01/p7b-target-runtime-contract-v1.json"
PROBE = ROOT / "evidence/powder/wp2-p7b-r3-target-runtime-probe-2026-08-28.json"


class P7BR3CTargetRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exec_contract = load_contract(EXEC)
        cls.runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
        cls.probe = json.loads(PROBE.read_text(encoding="utf-8"))

    def test_observed_system_python_is_explicitly_prohibited_for_project_code(self):
        for role in ("ue", "core"):
            self.assertEqual(self.runtime["roles"][role]["system_python_observed"], "3.6.9")
            self.assertFalse(self.runtime["roles"][role]["system_python_project_code_allowed"])
            self.assertEqual(self.runtime["roles"][role]["project_python_exact"], "3.11.13")
        self.assertIn("SYSTEM_PYTHON_3_6_9_INCOMPATIBLE_WITH_FROM_FUTURE_ANNOTATIONS", self.probe["confirmed_failure_modes"])

    def test_shell_preservation_helper_has_zero_python_dependency(self):
        helper = ROOT / "scripts/wp2_p7b_preservation_helpers_v2.sh"
        text = helper.read_text(encoding="utf-8")
        self.assertNotIn("python3", text)
        self.assertNotIn("$HOME", "\n".join(line for line in text.splitlines() if line.strip().startswith("p7b_require_absolute_remote_path")))
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

    def test_r2_entrypoint_enforces_target_python_and_v2_readiness_router(self):
        text = (ROOT / "scripts/wp2_p7b_c_node_r2.py").read_text(encoding="utf-8")
        for marker in (
            "TARGET_PROJECT_PYTHON_MISMATCH",
            "wp2_p7b_validate_readiness_v2.py",
            "READBACK_CAPABILITY=UNSUPPORTED_BY_OBSERVED_TMCC_INTERFACE",
            "PHYSICAL_DB_READBACK_CLAIM=NO",
            "p7b-target-runtime-contract-v1.json",
        ):
            self.assertIn(marker, text)

    def test_preflight_prohibits_tmcc_as_presumed_readback(self):
        text = (ROOT / "experiments/WP-PWD01/P7B_10MIN_PREFLIGHT_CONTRACT_v1.md").read_text(encoding="utf-8")
        self.assertIn("MUST NOT", text)
        self.assertIn("invoke `tmcc attenuator` as a presumed readback probe", text)
        self.assertIn("generic `GET_ERROR` means unknown control-plane state", text)

    def test_portal_and_cross_step_semantics_are_fail_closed(self):
        portal = self.runtime["portal_policy"]
        self.assertEqual(portal["generic_get_error_semantic"], "UNKNOWN_CONTROL_PLANE_STATE")
        self.assertTrue(portal["generic_get_error_may_not_confirm_teardown"])
        gha = self.runtime["github_actions_policy"]
        self.assertTrue(gha["ssh_agent_cross_step_persistence_prohibited"])
        self.assertTrue(gha["background_process_cross_step_persistence_prohibited"])

    def test_role_specific_tools_are_not_assumed_symmetric(self):
        self.assertEqual(self.probe["ue"]["mosquitto_daemon"], "ABSENT")
        self.assertEqual(self.probe["core"]["java"], "ABSENT")
        self.assertTrue(self.runtime["roles"]["ue"]["java_required"])
        self.assertFalse(self.runtime["roles"]["core"]["java_required"])
        self.assertFalse(self.runtime["roles"]["ue"]["mosquitto_daemon_required"])
        self.assertTrue(self.runtime["roles"]["core"]["mosquitto_daemon_required"])

    def test_rescue_and_salvage_live_surfaces_are_retired(self):
        for path in (
            ROOT / ".github/workflows/wp2-p7b-r3-same-reservation-rescue.yml",
            ROOT / ".wp2-p7b-r3-same-reservation-rescue-trigger",
            ROOT / ".github/workflows/wp2-p7b-r3-evidence-salvage.yml",
            ROOT / ".wp2-p7b-r3-evidence-salvage-trigger",
        ):
            self.assertFalse(path.exists(), str(path))

    def test_target_runtime_contract_is_pinned_to_current_scientific_contract_blob(self):
        expected = self.runtime["base_executable_contract"]["git_blob_sha"]
        p = subprocess.run(["git", "hash-object", str(EXEC)], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertEqual(p.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main()
