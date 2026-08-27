from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable


MATCHED_MANIFEST_PATHS = (
    "runtime.python_version",
    "runtime.platform",
    "runtime.paho_mqtt_version",
    "transport.host",
    "transport.port",
    "transport.protocol",
    "transport.qos",
    "transport.tls",
    "transport.clean_session",
    "transport.keepalive_s",
    "transport.reconnect_min_delay_s",
    "transport.reconnect_max_delay_s",
    "transport.max_queued_messages",
    "transport.max_inflight_messages",
    "transport.ca_sha256",
    "transport.broker_fingerprint",
)


@dataclass(frozen=True)
class GateVerdict:
    passed: bool
    failures: tuple[str, ...]

    def public_dict(self) -> dict[str, Any]:
        return {
            "gate": "PASS" if self.passed else "FAIL",
            "failures": list(self.failures),
        }


def load_contract(path: str | Path) -> dict[str, Any]:
    contract = json.loads(Path(path).read_text(encoding="utf-8"))
    if contract.get("schema_version") != "wp2-p7b-contract-v1":
        raise ValueError("unsupported P7B contract schema")
    if contract.get("scored") is not False or contract.get("scored_runs_authorized") is not False:
        raise ValueError("P7B qualification contract must remain non-scored and unauthorized")
    return contract


def _get_path(value: dict[str, Any], dotted: str) -> Any:
    current: Any = value
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(dotted)
        current = current[part]
    return current


def compare_b1_w1_manifests(
    b1: dict[str, Any], w1: dict[str, Any]
) -> GateVerdict:
    failures: list[str] = []
    if b1.get("architecture") != "B1_MQTT_QOS1":
        failures.append("B1_ARCHITECTURE_LABEL")
    if w1.get("architecture") != "W1_OFFLINE_FIRST":
        failures.append("W1_ARCHITECTURE_LABEL")

    for dotted in MATCHED_MANIFEST_PATHS:
        try:
            left = _get_path(b1, dotted)
            right = _get_path(w1, dotted)
        except KeyError:
            failures.append(f"MISSING_MATCHED_FIELD:{dotted}")
            continue
        if left != right:
            failures.append(f"MISMATCH:{dotted}")

    b1_app = b1.get("application", {})
    w1_app = w1.get("application", {})
    if b1_app.get("persistence_enabled") is not False:
        failures.append("B1_APPLICATION_PERSISTENCE_NOT_DISABLED")
    if w1_app.get("persistence_enabled") is not True:
        failures.append("W1_APPLICATION_PERSISTENCE_NOT_ENABLED")
    if w1_app.get("store") != "WellPulse SQLite WAL synchronous=FULL":
        failures.append("W1_STORE_LOCK_MISMATCH")
    return GateVerdict(not failures, tuple(failures))


def reconstruct_accepted_unacked(
    events: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    accepted: dict[int, dict[str, Any]] = {}
    publish_calls = 0
    accepted_calls = 0
    pubacks = 0
    for index, event in enumerate(events):
        name = event.get("event")
        if name == "mqtt_publish_call":
            publish_calls += 1
            if event.get("accepted_into_volatile_qos1_path") is True:
                mid = int(event["mid"])
                accepted_calls += 1
                accepted[mid] = {
                    "mid": mid,
                    "publish_event_index": index,
                    "utc": event.get("utc"),
                    "rc": int(event["rc"]),
                }
        elif name == "mqtt_puback":
            pubacks += 1
            accepted.pop(int(event["mid"]), None)

    mids = sorted(accepted)
    return {
        "published_calls": publish_calls,
        "accepted_publish_calls": accepted_calls,
        "puback_callbacks": pubacks,
        "accepted_unacknowledged_mids": mids,
        "accepted_unacknowledged_count": len(mids),
        "claim_boundary": "accepted-but-unacknowledged; not exact internal Paho queue occupancy",
    }


def evaluate_b1_pre_restart(
    events: Iterable[dict[str, Any]], snapshot: dict[str, Any]
) -> GateVerdict:
    reconstructed = reconstruct_accepted_unacked(events)
    failures: list[str] = []
    mids = reconstructed["accepted_unacknowledged_mids"]
    if not mids:
        failures.append("NO_ACCEPTED_UNACKNOWLEDGED_MESSAGE")
    snapshot_mids = sorted(int(x) for x in snapshot.get("accepted_unacked_mids", []))
    if snapshot_mids != mids:
        failures.append("EVENT_SNAPSHOT_MID_SET_MISMATCH")
    if int(snapshot.get("unacked_accepted_count", -1)) != len(mids):
        failures.append("EVENT_SNAPSHOT_COUNT_MISMATCH")
    if snapshot.get("exact_internal_queue_occupancy_claim") is not False:
        failures.append("INTERNAL_QUEUE_OCCUPANCY_CLAIM_NOT_PROHIBITED")
    return GateVerdict(not failures, tuple(failures))


def evaluate_readiness(
    observation: dict[str, Any], contract: dict[str, Any]
) -> GateVerdict:
    failures: list[str] = []
    expected_ids = [str(x) for x in contract["profile"]["attenuator_ids"]]
    readback = observation.get("attenuation_readback_db", {})
    if sorted(readback) != sorted(expected_ids):
        failures.append("ATTENUATOR_ID_SET")
    else:
        q0 = contract["profile"]["q0_db"]
        if any(readback[x] != q0 for x in expected_ids):
            failures.append("ATTENUATORS_NOT_Q0")

    if "tun_srsue" not in str(observation.get("route_output", "")):
        failures.append("EXPERIMENTAL_ROUTE_NOT_TUN_SRSUE")
    losses = observation.get("probe_packet_loss_pct")
    if not isinstance(losses, list) or len(losses) != 5 or any(float(x) != 0.0 for x in losses):
        failures.append("FIVE_ZERO_LOSS_PROBES")
    for field, code in (
        ("tls_mqtt_probe_pass", "TLS_MQTT_PROBE"),
        ("cell_unique_namespace", "CELL_UNIQUE_NAMESPACE"),
        ("architecture_state_fresh", "ARCHITECTURE_STATE_NOT_FRESH"),
        ("runtime_config_ca_broker_lock_pass", "RUNTIME_CONFIG_LOCK"),
        ("clock_capture_healthy", "CLOCK_CAPTURE"),
        ("evidence_path_armed", "EVIDENCE_PATH_NOT_ARMED"),
    ):
        if observation.get(field) is not True:
            failures.append(code)
    if observation.get("initial_session_present") is not False:
        failures.append("INITIAL_SESSION_PRESENT_NOT_FALSE")
    if observation.get("prior_process_or_session_residue") is not False:
        failures.append("PRIOR_PROCESS_OR_SESSION_RESIDUE")

    radio = observation.get("radio_metrics")
    if not isinstance(radio, dict) or radio.get("captured") is not True:
        failures.append("Q0_RADIO_METRICS_NOT_CAPTURED")
    else:
        env = contract["q0_radio_envelope_when_exposed"]
        rsrp = radio.get("rsrp_dbm")
        snr = radio.get("dl_snr_db")
        if rsrp is None and snr is None and not radio.get("absence_reason"):
            failures.append("Q0_RADIO_METRIC_ABSENCE_UNEXPLAINED")
        if rsrp is not None and not (env["rsrp_dbm_min"] <= float(rsrp) <= env["rsrp_dbm_max"]):
            failures.append("Q0_RSRP_OUTSIDE_ENVELOPE")
        if snr is not None and not (env["dl_snr_db_min"] <= float(snr) <= env["dl_snr_db_max"]):
            failures.append("Q0_SNR_OUTSIDE_ENVELOPE")
    return GateVerdict(not failures, tuple(failures))


def evaluate_restart_proof(proof: dict[str, Any]) -> GateVerdict:
    failures: list[str] = []
    if proof.get("generator_pid_before") != proof.get("generator_pid_after"):
        failures.append("GENERATOR_PID_CHANGED")
    if proof.get("gateway_pid_before") == proof.get("gateway_pid_after"):
        failures.append("GATEWAY_PID_DID_NOT_CHANGE")
    if proof.get("client_id_before") != proof.get("client_id_after"):
        failures.append("INTRA_RUN_CLIENT_ID_CHANGED")
    if proof.get("topic_before") != proof.get("topic_after"):
        failures.append("INTRA_RUN_TOPIC_CHANGED")
    if proof.get("generated_during_gateway_downtime") is not True:
        failures.append("NO_GENERATION_DURING_GATEWAY_DOWNTIME")
    if proof.get("source_sequence_continuity") is not True:
        failures.append("SOURCE_SEQUENCE_DISCONTINUITY")
    if proof.get("node_reboot_observed") is not False:
        failures.append("NODE_REBOOT_OR_UNKNOWN")
    for field in (
        "restart_requested_utc",
        "old_gateway_exit_utc",
        "new_gateway_start_utc",
        "new_gateway_ready_utc",
        "restart_requested_monotonic_ns",
        "old_gateway_exit_monotonic_ns",
        "new_gateway_start_monotonic_ns",
        "new_gateway_ready_monotonic_ns",
    ):
        if proof.get(field) in (None, ""):
            failures.append(f"MISSING_RESTART_FIELD:{field}")
    return GateVerdict(not failures, tuple(failures))


def enforce_cell_sequence(
    completed_cells: list[str], requested_cell: str, contract: dict[str, Any]
) -> GateVerdict:
    order = [cell["id"] for cell in contract["cells"]]
    failures: list[str] = []
    if requested_cell not in order:
        failures.append("UNKNOWN_CELL")
    else:
        expected_prefix = order[: order.index(requested_cell)]
        if completed_cells != expected_prefix:
            failures.append("CELL_ORDER_OR_PRIOR_PASS_VIOLATION")
    return GateVerdict(not failures, tuple(failures))
