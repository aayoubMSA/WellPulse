import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "experiments" / "WP-PWD01" / "p7b-qualification-contract.json"

import sys
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.p7b import (
    compare_b1_w1_manifests,
    enforce_cell_sequence,
    evaluate_b1_pre_restart,
    evaluate_readiness,
    evaluate_restart_proof,
    load_contract,
    reconstruct_accepted_unacked,
)


def manifest(architecture):
    return {
        "architecture": architecture,
        "runtime": {
            "python_version": "3.12.14",
            "platform": "linux-p7b",
            "paho_mqtt_version": "2.1.0",
        },
        "transport": {
            "host": "172.16.0.1",
            "port": 8883,
            "protocol": "MQTTv311",
            "qos": 1,
            "tls": True,
            "clean_session": False,
            "keepalive_s": 60,
            "reconnect_min_delay_s": 1,
            "reconnect_max_delay_s": 8,
            "max_queued_messages": 4096,
            "max_inflight_messages": 20,
            "ca_sha256": "a" * 64,
            "broker_fingerprint": "b" * 64,
            "client_id": "intentionally-arm-specific",
            "topic": "intentionally-arm-specific",
        },
        "application": {
            "persistence_enabled": architecture == "W1_OFFLINE_FIRST",
            "store": (
                "WellPulse SQLite WAL synchronous=FULL"
                if architecture == "W1_OFFLINE_FIRST"
                else "NONE"
            ),
        },
    }


def pass_readiness():
    return {
        "attenuation_readback_db": {"1": 0, "33": 0, "2": 0, "34": 0},
        "route_output": "172.16.0.1 dev tun_srsue src 192.168.3.2",
        "probe_packet_loss_pct": [0, 0, 0, 0, 0],
        "tls_mqtt_probe_pass": True,
        "cell_unique_namespace": True,
        "initial_session_present": False,
        "architecture_state_fresh": True,
        "prior_process_or_session_residue": False,
        "runtime_config_ca_broker_lock_pass": True,
        "clock_capture_healthy": True,
        "radio_metrics": {"captured": True, "rsrp_dbm": -60, "dl_snr_db": 42},
        "evidence_path_armed": True,
    }


class P7BRuntimeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_contract(CONTRACT_PATH)

    def test_b1_event_reconstruction_is_exact_and_claim_bounded(self):
        events = [
            {"event": "mqtt_publish_call", "mid": 10, "rc": 4, "accepted_into_volatile_qos1_path": True},
            {"event": "mqtt_publish_call", "mid": 11, "rc": 4, "accepted_into_volatile_qos1_path": True},
            {"event": "mqtt_puback", "mid": 10},
        ]
        result = reconstruct_accepted_unacked(events)
        self.assertEqual(result["accepted_unacknowledged_mids"], [11])
        self.assertEqual(result["accepted_unacknowledged_count"], 1)
        self.assertIn("not exact internal", result["claim_boundary"])

    def test_b1_pre_restart_requires_nonempty_exact_mid_set(self):
        events = [
            {"event": "mqtt_publish_call", "mid": 7, "rc": 4, "accepted_into_volatile_qos1_path": True}
        ]
        snapshot = {
            "accepted_unacked_mids": [7],
            "unacked_accepted_count": 1,
            "exact_internal_queue_occupancy_claim": False,
        }
        self.assertTrue(evaluate_b1_pre_restart(events, snapshot).passed)
        snapshot["accepted_unacked_mids"] = []
        self.assertFalse(evaluate_b1_pre_restart(events, snapshot).passed)

    def test_b1_w1_match_accepts_only_intended_application_difference(self):
        b1 = manifest("B1_MQTT_QOS1")
        w1 = manifest("W1_OFFLINE_FIRST")
        self.assertTrue(compare_b1_w1_manifests(b1, w1).passed)
        w1["transport"]["keepalive_s"] = 59
        verdict = compare_b1_w1_manifests(b1, w1)
        self.assertFalse(verdict.passed)
        self.assertIn("MISMATCH:transport.keepalive_s", verdict.failures)

    def test_readiness_pass_and_first_actionable_failures(self):
        obs = pass_readiness()
        self.assertTrue(evaluate_readiness(obs, self.contract).passed)
        obs["route_output"] = "172.16.0.1 dev eth0"
        self.assertIn(
            "EXPERIMENTAL_ROUTE_NOT_TUN_SRSUE",
            evaluate_readiness(obs, self.contract).failures,
        )

    def test_readiness_fails_closed_on_residue_session_radio_or_evidence(self):
        for field, value in (
            ("initial_session_present", True),
            ("prior_process_or_session_residue", True),
            ("evidence_path_armed", False),
        ):
            with self.subTest(field=field):
                obs = pass_readiness()
                obs[field] = value
                self.assertFalse(evaluate_readiness(obs, self.contract).passed)
        obs = pass_readiness()
        obs["radio_metrics"]["rsrp_dbm"] = -90
        self.assertIn("Q0_RSRP_OUTSIDE_ENVELOPE", evaluate_readiness(obs, self.contract).failures)

    def test_exposed_radio_metric_absence_requires_reason(self):
        obs = pass_readiness()
        obs["radio_metrics"] = {"captured": True, "rsrp_dbm": None, "dl_snr_db": None}
        self.assertFalse(evaluate_readiness(obs, self.contract).passed)
        obs["radio_metrics"]["absence_reason"] = "profile did not expose metric"
        self.assertTrue(evaluate_readiness(obs, self.contract).passed)

    def test_restart_domain_proof(self):
        proof = {
            "generator_pid_before": 100,
            "generator_pid_after": 100,
            "gateway_pid_before": 200,
            "gateway_pid_after": 201,
            "client_id_before": "same",
            "client_id_after": "same",
            "topic_before": "same-topic",
            "topic_after": "same-topic",
            "generated_during_gateway_downtime": True,
            "source_sequence_continuity": True,
            "node_reboot_observed": False,
        }
        for field in (
            "restart_requested_utc",
            "old_gateway_exit_utc",
            "new_gateway_start_utc",
            "new_gateway_ready_utc",
        ):
            proof[field] = "2026-08-27T00:00:00+00:00"
        for field in (
            "restart_requested_monotonic_ns",
            "old_gateway_exit_monotonic_ns",
            "new_gateway_start_monotonic_ns",
            "new_gateway_ready_monotonic_ns",
        ):
            proof[field] = 1
        self.assertTrue(evaluate_restart_proof(proof).passed)
        proof["gateway_pid_after"] = 200
        self.assertFalse(evaluate_restart_proof(proof).passed)

    def test_cell_sequence_stops_later_cells(self):
        self.assertTrue(enforce_cell_sequence([], "P7B-B1-S3", self.contract).passed)
        self.assertTrue(
            enforce_cell_sequence(["P7B-B1-S3"], "P7B-W1-S3", self.contract).passed
        )
        self.assertFalse(enforce_cell_sequence([], "P7B-B2-S3", self.contract).passed)

    def test_generator_and_gateway_scripts_are_syntax_valid_and_separated(self):
        paths = (
            ROOT / "scripts" / "wp2_p7b_generator.py",
            ROOT / "scripts" / "wp2_p7b_python_gateway.py",
            ROOT / "scripts" / "wp2_p7b_validate_readiness.py",
            ROOT / "scripts" / "wp2_p7b_compare_manifests.py",
        )
        for path in paths:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        generator = paths[0].read_text(encoding="utf-8")
        gateway = paths[1].read_text(encoding="utf-8")
        self.assertNotIn("PahoQoS1Session", generator)
        self.assertNotIn("tmcc", generator)
        self.assertNotIn("portal-cli", generator)
        self.assertIn("gateway_process_events.jsonl", gateway)

    def test_generator_fifo_handoff_is_explicitly_non_durable(self):
        path = ROOT / "scripts" / "wp2_p7b_generator.py"
        spec = importlib.util.spec_from_file_location("p7b_generator", path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as td:
            absent = Path(td) / "no-reader.fifo"
            self.assertEqual(
                module.fifo_handoff(absent, "{}"),
                "NO_GATEWAY_READER_DROPPED",
            )


if __name__ == "__main__":
    unittest.main()
