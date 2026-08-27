#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "experiments/WP-PWD01/p7b-target-runtime-contract-v1.json"
EXEC = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
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
    """Return non-empty, non-comment shell lines for dependency checks."""
    return "\n".join(
        raw for raw in text.splitlines()
        if raw.strip() and not raw.lstrip().startswith("#")
    )


def main() -> int:
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    if runtime.get("schema_version") != "wp2-p7b-target-runtime-contract-v1": fail("SCHEMA")
    if runtime.get("live_authorized") is not False or runtime.get("scored_runs_authorized") is not False: fail("AUTHORITY_DRIFT")
    expected_blob = runtime["base_executable_contract"]["git_blob_sha"]
    if git_blob_sha(EXEC) != expected_blob: fail("BASE_EXECUTABLE_CONTRACT_BLOB_DRIFT")

    for role in ("ue", "core"):
        r = runtime["roles"][role]
        if r["system_python_project_code_allowed"] is not False: fail(f"SYSTEM_PYTHON_ALLOWED_{role.upper()}")
        if r["project_python_exact"] != "3.11.13": fail(f"PINNED_PYTHON_{role.upper()}")

    ptxt = PRESERVE.read_text(encoding="utf-8")
    pexec = shell_executable_text(ptxt)
    if re.search(r"(^|[;&|()\s])python3([;&|()\s]|$)", pexec):
        fail("PRESERVATION_SYSTEM_PYTHON_DEPENDENCY")
    if "p7b_copy_tree_with_hash_manifest_v2" not in ptxt: fail("PRESERVATION_V2_FUNCTION_MISSING")
    q = subprocess.run(["bash", "-n", str(PRESERVE)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if q.returncode: fail("PRESERVATION_SHELL_SYNTAX")

    pre = PREFLIGHT.read_text(encoding="utf-8")
    for token in ("PINNED_PYTHON_VERSION", "PROJECT_CODE_SYSTEM_PYTHON=PROHIBITED", "FIXTURE_ONLY_NO_LIVE_TMCC_READBACK", "compile("):
        if token not in pre: fail("PREFLIGHT_MARKER_" + re.sub(r"\W+", "_", token))
    if re.search(r"tmcc\s+attenuator\s+['\"$0-9]", shell_executable_text(pre)):
        fail("PREFLIGHT_LIVE_ATTENUATOR_CALL")
    q = subprocess.run(["bash", "-n", str(PREFLIGHT)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if q.returncode: fail("PREFLIGHT_SHELL_SYNTAX")

    r2 = R2.read_text(encoding="utf-8")
    for token in (
        "p7b-target-runtime-contract-v1.json",
        "TARGET_PROJECT_PYTHON_MISMATCH",
        "wp2_p7b_validate_readiness_v2.py",
        "READBACK_CAPABILITY=UNSUPPORTED_BY_OBSERVED_TMCC_INTERFACE",
        "PHYSICAL_DB_READBACK_CLAIM=NO",
    ):
        if token not in r2: fail("R2_RUNTIME_LAYER_MISSING")

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

    print("WP2_P7B_TARGET_RUNTIME_QA=PASS")
    print("LIVE_AUTHORIZATION=BLOCKED")
    print("SCORED_AUTHORIZATION=BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
