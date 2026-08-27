#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))
from wellpulse.p7b_contract_v2 import load_contract


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
contract = load_contract(CONTRACT_PATH)


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


def install_contract_aware_status_writer() -> None:
    original = base.write_json

    def write_json(path: Path, value) -> None:
        if path.name == "p7b_c_status.json" and isinstance(value, dict):
            value = dict(value)
            value["core_evidence_root"] = resolved_core_root()
            value["ue_evidence_root"] = str(base.EVDIR.resolve())
            value["executable_contract_schema"] = contract.raw["schema_version"]
            value["authoritative_node_entrypoint"] = contract.raw["execution"]["only_authoritative_node_entrypoint"]
        original(path, value)

    base.write_json = write_json


def install_contract_aware_reconstruction() -> None:
    original_run = base.run

    def run(cmd, **kwargs):
        if isinstance(cmd, list) and len(cmd) >= 2 and str(cmd[1]).endswith("scripts/reconstruct_wp2_p7b.py"):
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
    inject_contract_authority()
    verify_injection()
    install_contract_aware_status_writer()
    install_contract_aware_reconstruction()
    print("P7B_EXECUTABLE_CONTRACT_V2=PASS", flush=True)
    print("P7B_AUTHORITATIVE_ENTRYPOINT=scripts/wp2_p7b_c_node_r2.py", flush=True)
    print("LIVE_AUTHORIZATION=SEPARATE_REQUIRED", flush=True)
    print("SCORED_AUTHORIZATION=BLOCKED", flush=True)
    return r1.main()


if __name__ == "__main__":
    raise SystemExit(main())
