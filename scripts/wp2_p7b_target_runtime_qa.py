#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "experiments/WP-PWD01/p7b-target-runtime-contract-v2.json"
EXEC = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
MATRIX = ROOT / "docs/WP2_POWDER_RUNTIME_COMPATIBILITY_MATRIX_2026-08-28.md"
PREFLIGHT = ROOT / "scripts/wp2_p7b_target_node_preflight.sh"
PRESERVE = ROOT / "scripts/wp2_p7b_preservation_helpers_v2.sh"
R2 = ROOT / "scripts/wp2_p7b_c_node_r2.py"


def fail(code: str) -> None:
    print(f"WP2_P7B_TARGET_RUNTIME_QA=BLOCKED:{code}")
    raise SystemExit(20)


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def shell_executable_text(text: str) -> str:
    return "\n".join(raw for raw in text.splitlines() if raw.strip() and not raw.lstrip().startswith("#"))


def main() -> int:
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    if runtime.get("schema_version") != "wp2-p7b-target-runtime-contract-v2": fail("SCHEMA")
    if runtime.get("live_authorized") is not False or runtime.get("scored_runs_authorized") is not False: fail("AUTHORITY_DRIFT")
    if runtime["supersession"]["historical_runtime_contract_retained"] != "experiments/WP-PWD01/p7b-target-runtime-contract-v1.json": fail("SUPERSESSION_PROVENANCE")
    if runtime["supersession"]["prospective_runtime_contract"] != "experiments/WP-PWD01/p7b-target-runtime-contract-v2.json": fail("SUPERSESSION_ACTIVE")

    expected_blob = runtime["base_executable_contract"]["git_blob_sha"]
    if git_blob_sha(EXEC) != expected_blob: fail("BASE_EXECUTABLE_CONTRACT_BLOB_DRIFT")

    efcc = runtime["efcc_evidence"]
    matrix = MATRIX.read_text(encoding="utf-8")
    expected_markers = {
        "github_run_id": "33124645486",
        "artifact_id": "9667857505",
        "artifact_zip_sha256": "e0a1923af8ff1ffbbdf5bb20641f01ec9f81e5d96c67b0328260063f14848245",
        "inner_inventory_tar_sha256": "b94c958a0b23bf812892680372485e6710b8f74b8368ea1c5c109e9f34d5541d",
    }
    for key, value in expected_markers.items():
        if str(efcc[key]) != value: fail("EFCC_EVIDENCE_" + key.upper())
        if value not in matrix: fail("EFCC_MATRIX_MISSING_" + key.upper())
    if efcc["collection_verdict"] != "WP2_POWDER_SSH_ENV_INVENTORY_WORKFLOW=PASS_COLLECTION_COMPLETE": fail("EFCC_COLLECTION_VERDICT")
    for flag in ("read_only",):
        if efcc[flag] is not True: fail("EFCC_READ_ONLY")
    for flag in ("new_reservation", "rf_mutation", "cells", "restart", "teardown", "scored"):
        if efcc[flag] is not False: fail("EFCC_SCOPE_" + flag.upper())

    image = runtime["target_image"]
    if image["os_id"] != "ubuntu" or image["os_version"] != "18.04": fail("TARGET_OS")
    if image["profile_revision"] != "a6da96560b6526dc6816761282722c996418fd8c": fail("PROFILE_REVISION")

    for role in ("ue", "core"):
        r = runtime["roles"][role]
        if r["system_python_observed"] != "3.6.9": fail(f"SYSTEM_PYTHON_OBSERVATION_{role.upper()}")
        if r["system_python_project_code_allowed"] is not False: fail(f"SYSTEM_PYTHON_ALLOWED_{role.upper()}")
        if r["project_python_exact"] != "3.11.13": fail(f"PINNED_PYTHON_{role.upper()}")
        if r["paho_mqtt_exact"] != "2.1.0": fail(f"PAHO_MQTT_{role.upper()}")
        if r["python_metadata_interface"] != "importlib.metadata": fail(f"METADATA_INTERFACE_{role.upper()}")
        if r["pkg_resources_required"] is not False: fail(f"PKG_RESOURCES_{role.upper()}")
        if r["remote_jq_dependency_prohibited"] is not True: fail(f"REMOTE_JQ_{role.upper()}")
    if runtime["roles"]["ue"]["java_major"] != 11 or runtime["roles"]["core"]["java_required"] is not False: fail("ROLE_JAVA")
    if runtime["roles"]["core"]["mosquitto_version_observed"] != "1.4.15" or runtime["roles"]["ue"]["mosquitto_daemon_required"] is not False: fail("ROLE_MOSQUITTO")

    if runtime["b2_java_dependency"]["jar_sha256"] != "59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185": fail("B2_JAR_SHA")
    if runtime["b2_java_dependency"]["pre_rf_hash_verification_required"] is not True: fail("B2_JAR_PREFLIGHT")

    ptxt = PRESERVE.read_text(encoding="utf-8")
    pexec = shell_executable_text(ptxt)
    if re.search(r"(^|[;&|()\s])python3([;&|()\s]|$)", pexec): fail("PRESERVATION_SYSTEM_PYTHON_DEPENDENCY")
    if re.search(r"(^|[;&|()\s])jq([;&|()\s]|$)", pexec): fail("PRESERVATION_REMOTE_JQ_DEPENDENCY")
    if "p7b_copy_tree_with_hash_manifest_v2" not in ptxt: fail("PRESERVATION_V2_FUNCTION_MISSING")
    q = subprocess.run(["bash", "-n", str(PRESERVE)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if q.returncode: fail("PRESERVATION_SHELL_SYNTAX")

    pre = PREFLIGHT.read_text(encoding="utf-8")
    for token in (
        "PAHO_MQTT=", "B2_JAR_PATH_NOT_SUPPLIED", "REMOTE_JQ_DEPENDENCY=PROHIBITED",
        "PYTHON_METADATA_INTERFACE=importlib.metadata", "EFCC_RUNTIME_BINDING=PASS",
        "PROJECT_CODE_SYSTEM_PYTHON=PROHIBITED", "FIXTURE_ONLY_NO_LIVE_TMCC_READBACK", "compile(",
    ):
        if token not in pre: fail("PREFLIGHT_MARKER_" + re.sub(r"\W+", "_", token))
    if re.search(r"tmcc\s+attenuator\s+['\"$0-9]", shell_executable_text(pre)): fail("PREFLIGHT_LIVE_ATTENUATOR_CALL")
    q = subprocess.run(["bash", "-n", str(PREFLIGHT)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if q.returncode: fail("PREFLIGHT_SHELL_SYNTAX")

    r2 = R2.read_text(encoding="utf-8")
    for token in (
        "p7b-target-runtime-contract-v2.json", "TARGET_PROJECT_PYTHON_MISMATCH", "TARGET_PAHO_MQTT_MISMATCH",
        "importlib.metadata", "wp2_p7b_validate_readiness_v2.py",
        "READBACK_CAPABILITY=UNSUPPORTED_BY_OBSERVED_TMCC_INTERFACE", "PHYSICAL_DB_READBACK_CLAIM=NO",
        "P7B_EFCC_BINDING=PASS",
    ):
        if token not in r2: fail("R2_RUNTIME_LAYER_MISSING_" + re.sub(r"\W+", "_", token))
    if "p7b-target-runtime-contract-v1.json" in r2: fail("R2_STILL_BINDS_RUNTIME_V1")

    for path in (
        ROOT / ".github/workflows/wp2-p7b-r3-same-reservation-rescue.yml",
        ROOT / ".wp2-p7b-r3-same-reservation-rescue-trigger",
        ROOT / ".github/workflows/wp2-p7b-r3-evidence-salvage.yml",
        ROOT / ".wp2-p7b-r3-evidence-salvage-trigger",
    ):
        if path.exists(): fail("RETIRED_LIVE_SURFACE_PRESENT")

    portal = runtime["portal_policy"]
    if portal["generic_get_error_semantic"] != "UNKNOWN_CONTROL_PLANE_STATE": fail("PORTAL_GET_ERROR_SEMANTIC")
    if portal["generic_get_error_may_not_confirm_teardown"] is not True: fail("PORTAL_TEARDOWN_SEMANTIC")

    attenuation = runtime["attenuation_control"]
    if attenuation["readback_supported_by_observed_tmcc_interface"] is not False: fail("FALSE_ATTENUATOR_READBACK_CAPABILITY")
    if attenuation["physical_db_readback_claim_prohibited"] is not True: fail("READBACK_CLAIM_BOUNDARY")

    gate = runtime["efcc_gate"]
    required_states = {"MISSING", "UNKNOWN", "VERSION_INCOMPATIBLE", "ROLE_MISMATCH", "UNTESTED"}
    if set(gate["blocks_live_on_required_dependency_states"]) != required_states: fail("EFCC_BLOCK_STATES")
    if gate["target_runtime_is_compatibility_baseline"] is not True or gate["contract_delta_audit_only"] is not True: fail("EFCC_DOCTRINE")

    print("WP2_P7B_TARGET_RUNTIME_QA=PASS")
    print("EFCC_CONTRACT_DELTA=PASS")
    print("LIVE_AUTHORIZATION=BLOCKED")
    print("SCORED_AUTHORIZATION=BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
