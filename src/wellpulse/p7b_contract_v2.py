from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


SCHEMA = "wp2-p7b-executable-contract-v2"
EXPECTED_CELL_SEQUENCE = ("P7B-B1-S3", "P7B-W1-S3", "P7B-B2-S3")


@dataclass(frozen=True)
class ContractV2:
    raw: dict[str, Any]

    @property
    def profile(self) -> dict[str, Any]:
        return self.raw["profile"]

    @property
    def schedule(self) -> dict[str, Any]:
        return self.raw["schedule"]

    @property
    def transport(self) -> dict[str, Any]:
        return self.raw["transport"]

    @property
    def b2_runtime(self) -> dict[str, Any]:
        return self.raw["b2_runtime"]

    @property
    def cell_sequence(self) -> tuple[str, ...]:
        return tuple(self.schedule["cell_sequence"])

    def render_root(self, which: str, **values: str) -> str:
        template = self.raw["evidence_layout"]["roots"][which]
        value = template.format(**values)
        if "$HOME" in value or "~/" in value or value.startswith("~"):
            raise ValueError(f"unresolved shell token in {which} root")
        if not value.startswith("/"):
            raise ValueError(f"non-absolute {which} root")
        return value

    def legacy_qualification_view(self) -> dict[str, Any]:
        p = self.profile
        s = self.schedule
        b1w1 = self.raw["b1_w1_runtime"]
        b2 = self.raw["b2_runtime"]
        readiness = self.raw["readiness"]
        return {
            "schema_version": "wp2-p7b-contract-v1",
            "evidence_class": self.raw["evidence_class"],
            "scored": False,
            "scored_runs_authorized": False,
            "profile": {
                "name": p["name"],
                "revision": p["revision"],
                "attenuator_ids": list(p["attenuator_ids"]),
                "q0_db": p["q0_db"],
                "q3_db": p["q3_db"],
            },
            "schedule": {
                "pre_impairment_q0_s": s["pre_impairment_q0_s"],
                "q3_s": s["q3_s"],
                "restart_offset_into_q3_s": s["restart_offset_into_q3_s"],
                "h_app_s": s["h_app_s"],
                "h_app_anchor": s["h_app_anchor"],
                "cohort_cutoff": s["cohort_cutoff"],
            },
            "cells": [dict(x) for x in self.raw["cells"]],
            "restart_domain": dict(self.raw["restart_domain"]),
            "b1_w1_matched_transport": {
                "package": f"paho-mqtt=={b1w1['paho_mqtt_version']}",
                "protocol": self.transport["protocol"],
                "qos": self.transport["qos"],
                "tls": self.transport["tls"],
                "clean_session": self.transport["clean_session"],
                "keepalive_s": self.transport["keepalive_s"],
                "reconnect_min_delay_s": b1w1["reconnect_min_delay_s"],
                "reconnect_max_delay_s": b1w1["reconnect_max_delay_s"],
                "max_queued_messages": b1w1["max_queued_messages"],
                "max_inflight_messages": b1w1["max_inflight_messages"],
                "only_intended_difference": b1w1["only_intended_difference"],
            },
            "b2_runtime": {
                "implementation": b2["implementation"],
                "jar_sha256": b2["jar_sha256"],
                "protocol": self.transport["protocol"],
                "qos": self.transport["qos"],
                "tls": self.transport["tls"],
                "clean_session": self.transport["clean_session"],
                "keepalive_s": self.transport["keepalive_s"],
                "automatic_reconnect": b2["automatic_reconnect"],
                "connection_timeout_s": b2["connection_timeout_s"],
                "persistence": b2["persistence"],
                "disconnected_buffer": dict(b2["disconnected_buffer"]),
            },
            "q0_radio_envelope_when_exposed": dict(readiness["q0_radio_envelope_when_exposed"]),
        }


def _require(cond: bool, message: str) -> None:
    if not cond:
        raise ValueError(message)


def validate_contract(raw: dict[str, Any]) -> None:
    _require(raw.get("schema_version") == SCHEMA, "unsupported executable contract schema")
    _require(raw.get("scored") is False, "contract must remain non-scored")
    _require(raw.get("scored_runs_authorized") is False, "scored authority prohibited")
    _require(raw.get("live_authorized") is False, "R3B contract must not carry live authority")
    a = raw["authority"]
    _require(a["authority_id"] == "P7B-RQ1", "authority id drift")
    _require(a["maximum_new_reservations"] == 1, "reservation limit drift")
    _require(a["automatic_retry"] is False, "automatic retry prohibited")
    _require(a["automatic_new_reservation"] is False, "automatic new reservation prohibited")
    _require(a["second_replacement_authorized"] is False, "second replacement prohibited")
    _require(a["requires_fresh_explicit_live_authorization_after_r3b"] is True, "fresh live authorization required")

    p = raw["profile"]
    _require(p["attenuator_ids"] == [1, 33, 2, 34], "attenuator set/order drift")
    _require(p["q0_db"] == 0 and p["q1_db"] == 40 and p["q2_db"] == 52 and p["q3_db"] == 55, "RF level drift")
    s = raw["schedule"]
    _require(tuple(s["cell_sequence"]) == EXPECTED_CELL_SEQUENCE, "cell sequence drift")
    _require(s["pre_impairment_q0_s"] == 60, "pre-Q0 drift")
    _require(s["q3_s"] == 120 and s["restart_offset_into_q3_s"] == 60, "Q3 schedule drift")
    _require(s["h_app_s"] == 300 and s["h_app_anchor"] == "t_service_ready", "H_app drift")
    _require(s["cohort_cutoff"] == "t_rf_restore", "cohort cutoff drift")

    cells = raw["cells"]
    _require(tuple(x["id"] for x in cells) == EXPECTED_CELL_SEQUENCE, "cells/schedule mismatch")
    _require([x["order"] for x in cells] == [1, 2, 3], "cell order fields invalid")
    _require(len({x["id"] for x in cells}) == 3, "duplicate cell id")

    roots = raw["evidence_layout"]["roots"]
    for name, template in roots.items():
        _require("$HOME" not in template and "~/" not in template and not template.startswith("~"), f"literal shell token in {name} root template")
    _require(roots["escrow"].startswith("/proj/WellPulse/"), "escrow root drift")

    execution = raw["execution"]
    _require(execution["only_authoritative_node_entrypoint"] == "scripts/wp2_p7b_c_node_r2.py", "authoritative entrypoint drift")
    _require("scripts/wp2_p7b_c_node.py" in execution["legacy_entrypoints_prohibited"], "base legacy runner must be prohibited")
    _require("scripts/wp2_p7b_c_node_r1.py" in execution["legacy_entrypoints_prohibited"], "R1 runner must be historical only")

    required_signals = set(raw["evidence_survival"]["teardown_requires"])
    _require(required_signals == {"EVIDENCE_CONTRACT_GATE=PASS", "EVIDENCE_ESCROW_GATE=PASS", "CONTROLLER_OFFPOWDER_GATE=PASS"}, "teardown gate set drift")
    _require(raw["evidence_survival"]["on_failure"] == "LEAVE_EXPERIMENT_LIVE_AND_STOP", "evidence failure policy drift")


def load_contract(path: str | Path) -> ContractV2:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_contract(raw)
    return ContractV2(raw)
