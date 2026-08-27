import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.p7b import load_contract


def load_script(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def matched_manifest(architecture):
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


def readiness():
    return {
        "attenuation_readback_db": {"1": 0, "33": 0, "2": 0, "34": 0},
        "route_output": "172.16.0.1 dev tun_srsue",
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


def restart():
    value = {
        "generator_pid_before": 10,
        "generator_pid_after": 10,
        "gateway_pid_before": 20,
        "gateway_pid_after": 21,
        "client_id_before": "same",
        "client_id_after": "same",
        "topic_before": "same",
        "topic_after": "same",
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
        value[field] = "2026-08-27T00:00:00+00:00"
    for field in (
        "restart_requested_monotonic_ns",
        "old_gateway_exit_monotonic_ns",
        "new_gateway_start_monotonic_ns",
        "new_gateway_ready_monotonic_ns",
    ):
        value[field] = 1
    return value


class P7BReconstructionTests(unittest.TestCase):
    def setUp(self):
        self.contract = load_contract(
            ROOT / "experiments" / "WP-PWD01" / "p7b-qualification-contract.json"
        )
        self.reconstruct_module = load_script(
            "p7b_reconstruct", ROOT / "scripts" / "reconstruct_wp2_p7b.py"
        )

    def build_tree(self, root):
        for cell in self.contract["cells"]:
            path = root / "cells" / cell["id"]
            path.mkdir(parents=True)
            (path / "readiness_observation.json").write_text(json.dumps(readiness()))
            (path / "restart_proof.json").write_text(json.dumps(restart()))
            (path / "runtime_manifest.json").write_text(
                json.dumps(matched_manifest(cell["architecture"]))
            )
            if cell["architecture"] == "B1_MQTT_QOS1":
                event = {
                    "event": "mqtt_publish_call",
                    "mid": 1,
                    "rc": 4,
                    "accepted_into_volatile_qos1_path": True,
                }
                (path / "mqtt_events.jsonl").write_text(json.dumps(event) + "\n")
                (path / "pre_restart_transport_snapshot.json").write_text(
                    json.dumps(
                        {
                            "accepted_unacked_mids": [1],
                            "unacked_accepted_count": 1,
                            "exact_internal_queue_occupancy_claim": False,
                        }
                    )
                )
            elif cell["architecture"] == "W1_OFFLINE_FIRST":
                (path / "w1_durability_proof.json").write_text(
                    json.dumps(
                        {
                            "generator_alive_during_restart": True,
                            "source_sequence_continuity": True,
                            "sqlite_wal": True,
                            "sqlite_synchronous_full": True,
                            "queue_path_survived_restart": True,
                            "pending_pre_restart_record_reconstructible_after_restart": True,
                            "same_queue_reopened": True,
                        }
                    )
                )
            else:
                proof = {
                    "jar_sha256": self.contract["b2_runtime"]["jar_sha256"],
                    "exact_java_config": True,
                    "tun_srsue_tls_path": True,
                    "same_payload_and_evidence_schema": True,
                    "persisted_record_before_process_destruction": True,
                    "same_persistence_directory_reopened": True,
                    "same_intra_run_client_identity": True,
                    "pre_restart_record_set_present_after_restart": True,
                    "buffer_drained_by_fixed_horizon": True,
                }
                (path / "b2_durability_proof.json").write_text(json.dumps(proof))

    def test_complete_synthetic_bundle_passes_without_scored_authority(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.build_tree(root)
            result = self.reconstruct_module.reconstruct(root, self.contract)
            self.assertEqual(result["gate"], "PASS")
            self.assertFalse(result["scored"])
            self.assertFalse(result["scored_runs_authorized"])
            self.assertIn("qualification mechanics only", result["claim_boundary"])

    def test_readiness_corruption_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.build_tree(root)
            target = root / "cells" / "P7B-W1-S3" / "readiness_observation.json"
            bad = json.loads(target.read_text())
            bad["route_output"] = "dev eth0"
            target.write_text(json.dumps(bad))
            result = self.reconstruct_module.reconstruct(root, self.contract)
            self.assertEqual(result["gate"], "FAIL")
            self.assertTrue(
                any("EXPERIMENTAL_ROUTE_NOT_TUN_SRSUE" in x for x in result["failures"])
            )

    def test_b2_hash_or_durability_failure_is_not_tolerated(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.build_tree(root)
            target = root / "cells" / "P7B-B2-S3" / "b2_durability_proof.json"
            bad = json.loads(target.read_text())
            bad["jar_sha256"] = "0" * 64
            bad["buffer_drained_by_fixed_horizon"] = False
            target.write_text(json.dumps(bad))
            result = self.reconstruct_module.reconstruct(root, self.contract)
            self.assertEqual(result["gate"], "FAIL")
            self.assertTrue(any("B2:JAR_SHA256" in x for x in result["failures"]))

    def test_b2_java_and_evidence_inventory_are_contract_complete(self):
        java = (
            ROOT
            / "experiments"
            / "WP-PWD01"
            / "b2-semantics"
            / "P7BRemoteB2Gateway.java"
        ).read_text(encoding="utf-8")
        for marker in (
            "setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1_1)",
            "setCleanSession(false)",
            "setAutomaticReconnect(false)",
            "setKeepAliveInterval(60)",
            "setConnectionTimeout(5)",
            "MqttDefaultFilePersistence",
            "setPersistBuffer(true)",
            "setDeleteOldestMessages(false)",
        ):
            self.assertIn(marker, java)
        inventory = (
            ROOT / "experiments" / "WP-PWD01" / "evidence_inventory_p7b_v1.txt"
        ).read_text(encoding="utf-8")
        for cell in ("P7B-B1-S3", "P7B-W1-S3", "P7B-B2-S3"):
            self.assertIn(cell, inventory)
        self.assertIn("EVIDENCE_ESCROW_GATE=PASS", inventory)
        self.assertIn("TEARDOWN_AUTHORIZED=YES", inventory)

    def test_no_new_script_contains_reservation_authority(self):
        paths = [
            ROOT / "scripts" / "reconstruct_wp2_p7b.py",
            ROOT / "scripts" / "wp2_p7b_b2_manifest.py",
        ]
        forbidden = ("portal-cli experiment create", "experiment create", "powder reservation")
        for path in paths:
            text = path.read_text(encoding="utf-8").lower()
            for term in forbidden:
                self.assertNotIn(term, text)


if __name__ == "__main__":
    unittest.main()
