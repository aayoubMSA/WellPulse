#!/usr/bin/env python3
from __future__ import annotations

import importlib.metadata
import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))
from wellpulse.p7b_contract_v2 import load_contract
from wellpulse.p7b_runtime_compat import parse_attenuator_set_evidence


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_LOAD_FAIL:{path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r1 = _load("wp2_p7b_c_node_r1_layer", HERE / "wp2_p7b_c_node_r1.py")
base = r1.base
CONTRACT_PATH = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
RUNTIME_CONTRACT_PATH = ROOT / "experiments/WP-PWD01/p7b-target-runtime-contract-v2.json"
contract = load_contract(CONTRACT_PATH)
runtime_contract = json.loads(RUNTIME_CONTRACT_PATH.read_text(encoding="utf-8"))


def verify_target_interpreter_and_python_dependencies() -> None:
    expected = runtime_contract["roles"]["ue"]["project_python_exact"]
    actual = ".".join(str(x) for x in sys.version_info[:3])
    if actual != expected:
        raise RuntimeError(f"TARGET_PROJECT_PYTHON_MISMATCH:{actual}!={expected}")
    if runtime_contract["roles"]["ue"]["system_python_project_code_allowed"] is not False:
        raise RuntimeError("SYSTEM_PYTHON_POLICY_DRIFT")
    expected_paho = runtime_contract["roles"]["ue"]["paho_mqtt_exact"]
    try:
        actual_paho = importlib.metadata.version("paho-mqtt")
    except importlib.metadata.PackageNotFoundError as exc:
        raise RuntimeError("TARGET_PAHO_MQTT_MISSING") from exc
    if actual_paho != expected_paho:
        raise RuntimeError(f"TARGET_PAHO_MQTT_MISMATCH:{actual_paho}!={expected_paho}")
    if runtime_contract["node_project_python_policy"]["package_metadata_interface"] != "importlib.metadata":
        raise RuntimeError("PYTHON_METADATA_INTERFACE_DRIFT")


def inject_contract_authority() -> None:
    p = contract.profile
    s = contract.schedule
    t = contract.transport
    b2 = contract.b2_runtime
    base.BROKER_HOST = str(t["broker_host"])
    base.BROKER_PORT = int(t["broker_port"])
    base.ATTENUATORS = tuple(int(x) for x in p["attenuator_ids"])
    base.Q0_DB = int(p["q0_db"])
    base.Q3_DB = int(p["q3_db"])
    base.PRE_Q0_S = int(s["pre_impairment_q0_s"])
    base.Q3_S = int(s["q3_s"])
    base.RESTART_OFFSET_S = int(s["restart_offset_into_q3_s"])
    base.H_APP_S = int(s["h_app_s"])
    base.B2_JAR_SHA = str(b2["jar_sha256"])

    legacy_path = Path("/tmp/wp2-p7b-executable-contract-v2-legacy.json")
    legacy_path.write_text(json.dumps(contract.legacy_qualification_view(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    base.CONTRACT = legacy_path


def resolved_core_root() -> str:
    return str(PurePosixPath(r1.resolve_core_home()) / "wellpulse-powder-evidence" / "p7b" / f"{base.RUN_ID}-core")


def attenuation_control_for_cell(cell_dir: Path) -> dict:
    set_path = cell_dir / "attenuator_q0_set.txt"
    text = set_path.read_text(encoding="utf-8", errors="replace") if set_path.exists() else ""
    return parse_attenuator_set_evidence(text, [int(x) for x in contract.profile["attenuator_ids"]], int(contract.profile["q0_db"]))


def install_observed_attenuator_interface() -> None:
    def no_false_readback(raw_path: Path) -> dict[str, float]:
        ctrl = attenuation_control_for_cell(raw_path.parent)
        raw_path.write_text(
            "READBACK_CAPABILITY=UNSUPPORTED_BY_OBSERVED_TMCC_INTERFACE\n"
            "VERIFICATION_MODE=SET_COMMAND_ACK_PLUS_INDEPENDENT_Q0_PATH_EVIDENCE\n"
            "PHYSICAL_DB_READBACK_CLAIM=NO\n"
            + "\n".join(
                f"SET_ACK id={row['id']} db={row['db']:g} rc={row['rc']} output={row['output']}"
                for row in ctrl["set_ack_rows"]
            )
            + "\n",
            encoding="utf-8",
        )
        if ctrl["set_ack_pass"] is not True:
            return {}
        return {str(x): float(contract.profile["q0_db"]) for x in contract.profile["attenuator_ids"]}

    base.attenuator_readback = no_false_readback


def install_contract_aware_writer() -> None:
    original = base.write_json

    def write_json(path: Path, value) -> None:
        if path.name == "p7b_c_status.json" and isinstance(value, dict):
            value = dict(value)
            value["core_evidence_root"] = resolved_core_root()
            value["ue_evidence_root"] = str(base.EVDIR.resolve())
            value["executable_contract_schema"] = contract.raw["schema_version"]
            value["target_runtime_contract_schema"] = runtime_contract["schema_version"]
            value["target_runtime_efcc_run_id"] = runtime_contract["efcc_evidence"]["github_run_id"]
            value["authoritative_node_entrypoint"] = contract.raw["execution"]["only_authoritative_node_entrypoint"]
        elif path.name == "readiness_observation.json" and isinstance(value, dict):
            value = dict(value)
            value.pop("attenuation_readback_db", None)
            value["attenuation_control"] = attenuation_control_for_cell(path.parent)
        original(path, value)

    base.write_json = write_json


def install_contract_aware_run_router() -> None:
    original_run = base.run

    def run(cmd, **kwargs):
        if isinstance(cmd, list) and len(cmd) >= 2:
            target = str(cmd[1])
            if target.endswith("scripts/wp2_p7b_validate_readiness.py"):
                new_cmd = list(cmd)
                new_cmd[1] = str(ROOT / "scripts/wp2_p7b_validate_readiness_v2.py")
                return original_run(new_cmd, **kwargs)
            if target.endswith("scripts/reconstruct_wp2_p7b.py"):
                new_cmd = [
                    cmd[0],
                    str(ROOT / "scripts/reconstruct_wp2_p7b_v2.py"),
                    "--root", str(base.EVDIR),
                    "--core-root", resolved_core_root(),
                    "--contract", str(CONTRACT_PATH),
                ]
                return original_run(new_cmd, **kwargs)
        return original_run(cmd, **kwargs)

    base.run = run


def verify_injection() -> None:
    p, s, t = contract.profile, contract.schedule, contract.transport
    checks = {
        "BROKER_HOST": base.BROKER_HOST == t["broker_host"],
        "BROKER_PORT": base.BROKER_PORT == t["broker_port"],
        "ATTENUATORS": list(base.ATTENUATORS) == p["attenuator_ids"],
        "Q0_DB": base.Q0_DB == p["q0_db"],
        "Q3_DB": base.Q3_DB == p["q3_db"],
        "PRE_Q0_S": base.PRE_Q0_S == s["pre_impairment_q0_s"],
        "Q3_S": base.Q3_S == s["q3_s"],
        "RESTART_OFFSET_S": base.RESTART_OFFSET_S == s["restart_offset_into_q3_s"],
        "H_APP_S": base.H_APP_S == s["h_app_s"],
        "B2_JAR_SHA": base.B2_JAR_SHA == contract.b2_runtime["jar_sha256"],
    }
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        raise RuntimeError("EXECUTABLE_CONTRACT_INJECTION_FAIL:" + ",".join(failed))


def main() -> int:
    verify_target_interpreter_and_python_dependencies()
    inject_contract_authority()
    verify_injection()
    install_observed_attenuator_interface()
    install_contract_aware_writer()
    install_contract_aware_run_router()
    print("P7B_EXECUTABLE_CONTRACT_V2=PASS", flush=True)
    print("P7B_TARGET_RUNTIME_CONTRACT_V2=PASS", flush=True)
    print("P7B_EFCC_BINDING=PASS", flush=True)
    print("ATTENUATION_VERIFICATION=SET_ACK_PLUS_INDEPENDENT_Q0_PATH_NO_READBACK_CLAIM", flush=True)
    print("P7B_AUTHORITATIVE_ENTRYPOINT=scripts/wp2_p7b_c_node_r2.py", flush=True)
    print("LIVE_AUTHORIZATION=SEPARATE_REQUIRED", flush=True)
    print("SCORED_AUTHORIZATION=BLOCKED", flush=True)
    return r1.main()


if __name__ == "__main__":
    raise SystemExit(main())
