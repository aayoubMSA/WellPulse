#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments/WP-PWD01"
BASE = EXP / "p7b-executable-contract-v2.json"
RUNTIME = EXP / "p7b-target-runtime-contract-v2.json"
MODULAR = EXP / "p7b-modular-pipeline-contract-v1.json"
DELTA = EXP / "p7b-h2-controller-restore-contract-delta-v1.json"
H24 = ROOT / "evidence/powder/wp2-p7b-h2-4-adversarial-qa.json"
PREFLIGHT = ROOT / "scripts/wp2_p7b_target_node_preflight.sh"
H2_ENTRY = ROOT / "scripts/wp2_p7b_c_node_h2.py"
H2_RESTORE = ROOT / "scripts/wp2_p7b_service_restore_h2.sh"
H2_OWNERSHIP = ROOT / "src/wellpulse/p7b_session_ownership.py"
GOLDEN_RESTORE = ROOT / "scripts/wp2_golden_service_restore.sh"

EXPECTED_FROZEN_BLOBS = {
    "base": "233aabeaf3081470bc3ebc1ee04168f8932fc415",
    "runtime": "9531893989effb142e694294b95c0c7146353742",
    "modular": "2c85af21f502c092c2da0ecb1bf615c8f705069b",
    "historical_golden_restore": "cdf865eaaaf1c08bc8f7a8896d7f705739e60b9c",
}
ALLOWED_WORKFLOWS = {
    "local-gate-once.yml",
    "local-unit-tests.yml",
    "wp2-b2-semantics.yml",
    "wp2-golden-offline-qa.yml",
    "wp2-offpowder-artifact-qa.yml",
    "wp2-preintegration-static.yml",
}
AUTH_FALSE_KEYS = (
    "live_authorized",
    "reservation_creation_authorized",
    "rf_authorized",
    "retry_authorized",
    "w1_b2_authorized",
    "teardown_authorized",
    "scored_authorized",
    "wp3_authorized",
    "automatic_retry",
    "automatic_new_reservation",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise AssertionError(reason)


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def shell_syntax(path: Path) -> None:
    p = subprocess.run(["bash", "-n", str(path)], cwd=ROOT, capture_output=True, text=True)
    require(p.returncode == 0, f"BASH_SYNTAX:{path.name}:{p.stderr}")


def check_frozen_integrity() -> dict:
    actual = {
        "base": git_blob_sha(BASE),
        "runtime": git_blob_sha(RUNTIME),
        "modular": git_blob_sha(MODULAR),
        "historical_golden_restore": git_blob_sha(GOLDEN_RESTORE),
    }
    require(actual == EXPECTED_FROZEN_BLOBS, f"FROZEN_BLOB_DRIFT:{actual}")
    return actual


def base_science(base: dict) -> dict:
    return {
        "q0_db": base["profile"]["q0_db"],
        "q1_db": base["profile"]["q1_db"],
        "q2_db": base["profile"]["q2_db"],
        "q3_db": base["profile"]["q3_db"],
        "attenuator_ids": base["profile"]["attenuator_ids"],
        "pre_impairment_q0_s": base["schedule"]["pre_impairment_q0_s"],
        "q3_s": base["schedule"]["q3_s"],
        "restart_offset_into_q3_s": base["schedule"]["restart_offset_into_q3_s"],
        "h_app_s": base["schedule"]["h_app_s"],
        "h_app_anchor": base["schedule"]["h_app_anchor"],
        "cohort_cutoff": base["schedule"]["cohort_cutoff"],
        "cell_sequence": base["schedule"]["cell_sequence"],
        "generator_outside_restart_domain": base["restart_domain"]["telemetry_generator_outside_restart_domain"],
        "automatic_scientific_retry": base["authority"]["automatic_retry"],
    }


def check_science_equivalence(base: dict, delta: dict, modular: dict) -> dict:
    b = base_science(base)
    d = delta["frozen_scientific_controls"]
    for key, value in b.items():
        require(d[key] == value, f"DELTA_SCIENCE_DRIFT:{key}")
    m = modular["frozen_scientific_controls"]
    require(m["q_db"] == [b["q0_db"], b["q1_db"], b["q2_db"], b["q3_db"]], "MODULAR_Q_DRIFT")
    require(m["attenuator_ids"] == b["attenuator_ids"], "MODULAR_ATTENUATOR_DRIFT")
    require(m["pre_q0_s"] == b["pre_impairment_q0_s"], "MODULAR_PRE_Q0_DRIFT")
    require(m["q3_s"] == b["q3_s"], "MODULAR_Q3_DRIFT")
    require(m["restart_offset_into_q3_s"] == b["restart_offset_into_q3_s"], "MODULAR_RESTART_DRIFT")
    require(m["cell_order"] == b["cell_sequence"], "MODULAR_CELL_ORDER_DRIFT")
    require(m["cohort_cutoff"] == b["cohort_cutoff"], "MODULAR_COHORT_DRIFT")
    require(m["h_app_s"] == b["h_app_s"] and m["h_app_anchor"] == b["h_app_anchor"], "MODULAR_H_APP_DRIFT")
    require(m["generator_outside_restart_domain"] is True, "MODULAR_GENERATOR_DOMAIN_DRIFT")
    require(m["automatic_scientific_retry"] is False, "MODULAR_AUTO_RETRY_DRIFT")
    require(m["clocks_distinct"] == ["t_rf_restore", "t_service_ready", "t_app_complete"], "MODULAR_CLOCK_DRIFT")
    require(delta["scientific_change"] is False, "H2_DELTA_SCIENTIFIC_CHANGE_TRUE")
    return b


def check_runtime_binding(base: dict, runtime: dict, delta: dict) -> dict:
    require(runtime["base_executable_contract"]["git_blob_sha"] == EXPECTED_FROZEN_BLOBS["base"], "RUNTIME_BASE_SHA_DRIFT")
    require(delta["base_contract"]["git_blob_sha"] == EXPECTED_FROZEN_BLOBS["base"], "DELTA_BASE_SHA_DRIFT")
    p = base["profile"]
    ti = runtime["target_image"]
    require(ti["profile"] == p["name"], "PROFILE_NAME_DRIFT")
    require(ti["profile_revision"] == p["revision"], "PROFILE_REVISION_DRIFT")
    require(ti["hardware_type"] == p["hardware_type"], "HARDWARE_DRIFT")
    require(ti["image"] == p["image"], "IMAGE_DRIFT")
    require(runtime["roles"]["core"]["node_binding"] == p["bindings"]["enb_node"] == "nuc1", "CORE_BINDING_DRIFT")
    require(runtime["roles"]["ue"]["node_binding"] == p["bindings"]["ue_node"] == "nuc2", "UE_BINDING_DRIFT")
    require(runtime["roles"]["ue"]["project_python_exact"] == "3.11.13", "UE_PYTHON_DRIFT")
    require(runtime["roles"]["core"]["project_python_exact"] == "3.11.13", "CORE_PYTHON_DRIFT")
    require(runtime["roles"]["ue"]["paho_mqtt_exact"] == base["b1_w1_runtime"]["paho_mqtt_version"] == "2.1.0", "PAHO_DRIFT")
    require(runtime["b2_java_dependency"]["jar_sha256"] == base["b2_runtime"]["jar_sha256"], "B2_JAR_DRIFT")
    require(runtime["roles"]["ue"]["system_python_project_code_allowed"] is False, "UE_SYSTEM_PYTHON_POLICY_DRIFT")
    require(runtime["roles"]["core"]["system_python_project_code_allowed"] is False, "CORE_SYSTEM_PYTHON_POLICY_DRIFT")
    require(runtime["role_specific_dependency_policy"]["remote_jq_dependency_prohibited"] is True, "REMOTE_JQ_POLICY_DRIFT")
    return {"profile_revision": p["revision"], "python": "3.11.13", "paho": "2.1.0"}


def check_h2_runtime_preflight(runtime: dict, delta: dict) -> dict:
    text = PREFLIGHT.read_text(encoding="utf-8")
    for rel in (
        "scripts/wp2_p7b_c_node_h2.py",
        "src/wellpulse/p7b_session_ownership.py",
    ):
        require(rel in text, f"H2_SOURCE_NOT_BOUND_TO_TARGET_PREFLIGHT:{rel}")
    require('h2_restore="$REPO/scripts/wp2_p7b_service_restore_h2.sh"' in text, "H2_RESTORE_NOT_BOUND_TO_PREFLIGHT")
    require('bash -n "$h2_restore"' in text, "H2_RESTORE_SHELL_GATE_MISSING")
    require("H2_DEPENDS_ON_SYSTEM_PYTHON" in text, "H2_SYSTEM_PYTHON_GUARD_MISSING")
    require("H2_DEPENDS_ON_REMOTE_JQ" in text, "H2_REMOTE_JQ_GUARD_MISSING")
    for cmd in ("tmux", "pgrep", "bash", "sha256sum"):
        require(re.search(r"for cmd in [^\n]*\b" + re.escape(cmd) + r"\b", text) is not None, f"PREFLIGHT_COMMAND_GATE_MISSING:{cmd}")
    require(runtime["roles"]["core"]["coreutils_sha256sum_observed"] == "8.28", "COREUTILS_BASELINE_DRIFT")
    require(delta["h2_3_implementation"]["durability"]["frontier"].startswith("APPEND_PLUS_FSYNC_OR_SYNC"), "H2_FRONTIER_DURABILITY_DRIFT")
    shell_syntax(PREFLIGHT)
    shell_syntax(H2_RESTORE)
    return {"h2_python_sources_target_compiled": 2, "h2_restore_bash_n": True}


def check_h2_layering(base: dict, runtime: dict, delta: dict) -> dict:
    entry = H2_ENTRY.read_text(encoding="utf-8")
    require(base["execution"]["only_authoritative_node_entrypoint"] == "scripts/wp2_p7b_c_node_r2.py", "BASE_ENTRYPOINT_DRIFT")
    require(runtime["future_execution"]["authoritative_entrypoint"] == "scripts/wp2_p7b_c_node_r2.py", "RUNTIME_ENTRYPOINT_DRIFT")
    require(delta["h2_2_implementation"]["prospective_entrypoint"] == "scripts/wp2_p7b_c_node_h2.py", "H2_PROSPECTIVE_ENTRYPOINT_DRIFT")
    require('r2 = _load("wp2_p7b_c_node_r2_h2_base"' in entry, "H2_NO_R2_LAYERING")
    require(entry.index("identity = controller_identity()") < entry.index("return r2.main()"), "A1_A3_NOT_BEFORE_R2_MAIN")
    require(entry.index("install_h2_frontier_instrumentation()") < entry.index("return r2.main()"), "A4_A6_NOT_BEFORE_R2_MAIN")
    require(entry.index("install_h2_safe_restore(identity)") < entry.index("return r2.main()"), "H2_SAFE_RESTORE_NOT_BOUND")
    for key in AUTH_FALSE_KEYS:
        require(delta["authority"][key] is False, f"H2_AUTHORITY_DRIFT:{key}")
    require(delta["authority"]["future_live_action_requires_separate_explicit_user_authorization"] is True, "FRESH_USER_AUTHORITY_POLICY_DRIFT")
    return {"base_authority_entrypoint": "r2", "prospective_h2_wrapper": "h2", "live_promoted": False}


def check_modular_pipeline(base: dict, modular: dict) -> dict:
    require(sum(int(x["weight_pct"]) for x in modular["h2_offline_modules"]) == 100, "H2_WEIGHT_SUM_DRIFT")
    require(modular["architecture"]["workflow_creation_policy"] == "CREATE_ONLY_AFTER_H2_PASS_AND_SEPARATE_EXPLICIT_USER_LIVE_AUTHORIZATION", "WORKFLOW_CREATION_POLICY_DRIFT")
    require(modular["architecture"]["automatic_retry"] is False, "MODULAR_AUTO_RETRY_ENABLED")
    require(modular["architecture"]["automatic_reservation_create"] is False, "MODULAR_AUTO_RESERVATION_ENABLED")
    require(modular["architecture"]["automatic_teardown"] is False, "MODULAR_AUTO_TEARDOWN_ENABLED")
    require(modular["ci_state_contract"]["ssh_agent_scope"] == "PER_JOB_ONLY", "SSH_AGENT_SCOPE_DRIFT")
    require(modular["ci_state_contract"]["cross_job_process_state"] == "PROHIBITED", "CROSS_JOB_PROCESS_STATE_DRIFT")
    live = {m["id"]: m for m in modular["live_modules"]}
    require("CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS" in live["M2"]["required_gates"], "M2_A1_GATE_MISSING")
    require("H2-safe ownership logic" in live["M3"]["purpose"], "M3_H2_OWNERSHIP_BINDING_MISSING")
    require([live[x]["cell"] for x in ("M4", "M6", "M8")] == base["schedule"]["cell_sequence"], "MODULAR_SCIENTIFIC_CELL_ORDER_DRIFT")
    for mid in ("M5", "M7", "M9"):
        require(live[mid]["failure_action"] == "LEAVE_EXPERIMENT_LIVE_AND_STOP", f"EVIDENCE_FAILURE_POLICY_DRIFT:{mid}")
    require(modular["transition_rules"]["automatic_retry"] == "PROHIBITED", "TRANSITION_AUTO_RETRY_DRIFT")
    require(modular["transition_rules"]["teardown_before_readback"] == "PROHIBITED", "TEARDOWN_READBACK_DRIFT")
    return {"h2_weight_pct": 100, "live_cells": [live[x]["cell"] for x in ("M4", "M6", "M8")]}


def check_h24_evidence() -> dict:
    data = load(H24)
    require(data["terminal_verdict"] == "H2_4_ADVERSARIAL_QA=PASS", "H2_4_VERDICT_MISSING")
    require(data["final_qa"]["suite_result"] == "PASS", "H2_4_SUITE_NOT_PASS")
    require(data["final_qa"]["adversarial_harness_required_cases"] == 7, "H2_4_CASE_COUNT_DRIFT")
    require(data["final_qa"]["adversarial_harness_required_cases_passed"] == 7, "H2_4_CASE_PASS_DRIFT")
    require(all(v == "PASS" for v in data["required_cases"].values()), "H2_4_CASE_REGRESSION")
    for key in data["authority"]:
        require(data["authority"][key] is False, f"H2_4_AUTHORITY_DRIFT:{key}")
    return {"suite_tests": data["final_qa"]["suite_tests"], "a7_cases": 7}


def check_no_live_surface() -> dict:
    wf_dir = ROOT / ".github/workflows"
    actual = {p.name for p in wf_dir.glob("*.yml")}
    require(actual == ALLOWED_WORKFLOWS, f"WORKFLOW_SURFACE_DRIFT:{sorted(actual)}")
    require(not (wf_dir / "wp2-p7b-rq2-session.yml").exists(), "LIVE_P7B_WORKFLOW_EXISTS")
    return {"workflow_count": len(actual), "live_p7b_workflow": False}


def run_gate() -> dict:
    base = load(BASE)
    runtime = load(RUNTIME)
    modular = load(MODULAR)
    delta = load(DELTA)
    checks = {
        "frozen_integrity": check_frozen_integrity(),
        "science_equivalence": check_science_equivalence(base, delta, modular),
        "runtime_binding": check_runtime_binding(base, runtime, delta),
        "h2_runtime_preflight": check_h2_runtime_preflight(runtime, delta),
        "h2_layering": check_h2_layering(base, runtime, delta),
        "modular_pipeline": check_modular_pipeline(base, modular),
        "h2_4_evidence": check_h24_evidence(),
        "no_live_surface": check_no_live_surface(),
    }
    return {
        "schema_version": "wp2-p7b-h2-regression-gate-v1",
        "gate": "PASS",
        "checks": checks,
        "powder_contact": False,
        "network_contact": False,
        "live_service_mutation": False,
        "rf_mutation": False,
        "retry": False,
        "w1_b2": False,
        "scored": False,
        "teardown": False,
        "wp3": False,
        "base_executable_contract_mutated": False,
        "target_runtime_contract_mutated": False,
        "modular_pipeline_contract_mutated": False,
        "prospective_h2_entrypoint_promoted_to_live_authority": False,
        "terminal_gate": "H2_5_REGRESSION=PASS",
        "next_patch": "WP2-P7B-H2.6_REQUALIFICATION_AUTHORITY_DECISION_CANONICAL_CLOSURE",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    try:
        report = run_gate()
    except Exception as exc:
        report = {
            "schema_version": "wp2-p7b-h2-regression-gate-v1",
            "gate": "BLOCKED",
            "first_reason": f"{type(exc).__name__}:{exc}",
            "powder_contact": False,
            "network_contact": False,
            "terminal_gate": f"H2_5_REGRESSION=BLOCKED:{type(exc).__name__}:{exc}",
        }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(report["terminal_gate"])
    return 0 if report["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
