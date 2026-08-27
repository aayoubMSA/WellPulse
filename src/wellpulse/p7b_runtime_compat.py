from __future__ import annotations

import re
from typing import Any

from .p7b import GateVerdict

SET_RE = re.compile(r"^SET id=(\d+) db=(-?\d+(?:\.\d+)?) rc=(\d+) output=(.*)$")
VERIFICATION_MODE = "SET_COMMAND_ACK_PLUS_INDEPENDENT_Q0_PATH_EVIDENCE"


def parse_attenuator_set_evidence(text: str, expected_ids: list[int], expected_db: int | float) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        m = SET_RE.match(line.strip())
        if not m:
            continue
        rows.append({
            "id": int(m.group(1)),
            "db": float(m.group(2)),
            "rc": int(m.group(3)),
            "output": m.group(4).strip(),
        })
    ids = [r["id"] for r in rows]
    ok = (
        ids == expected_ids
        and len(rows) == len(expected_ids)
        and all(r["db"] == float(expected_db) for r in rows)
        and all(r["rc"] == 0 for r in rows)
        and all("changing attenuation" in r["output"].lower() for r in rows)
    )
    return {
        "verification_mode": VERIFICATION_MODE,
        "physical_db_readback_supported": False,
        "physical_db_readback_claim": False,
        "requested_db": float(expected_db),
        "expected_ids": expected_ids,
        "set_ack_rows": rows,
        "set_ack_pass": ok,
    }


def evaluate_readiness_v2(observation: dict[str, Any], contract: dict[str, Any]) -> GateVerdict:
    failures: list[str] = []
    ctrl = observation.get("attenuation_control")
    expected_ids = [int(x) for x in contract["profile"]["attenuator_ids"]]
    q0 = float(contract["profile"]["q0_db"])
    if not isinstance(ctrl, dict):
        failures.append("ATTENUATION_CONTROL_EVIDENCE_MISSING")
    else:
        if ctrl.get("verification_mode") != VERIFICATION_MODE:
            failures.append("ATTENUATION_VERIFICATION_MODE")
        if ctrl.get("physical_db_readback_supported") is not False:
            failures.append("UNSUPPORTED_ATTENUATION_READBACK_CLAIM")
        if ctrl.get("physical_db_readback_claim") is not False:
            failures.append("PHYSICAL_DB_READBACK_CLAIM_PROHIBITED")
        if ctrl.get("set_ack_pass") is not True:
            failures.append("ATTENUATOR_SET_ACK")
        if [int(x) for x in ctrl.get("expected_ids", [])] != expected_ids:
            failures.append("ATTENUATOR_ID_SET")
        if float(ctrl.get("requested_db", 1e99)) != q0:
            failures.append("ATTENUATOR_REQUESTED_DB_NOT_Q0")

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
