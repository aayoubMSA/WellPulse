#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_LOAD_FAIL:{path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


h2 = _load("wp2_p7b_c_node_h2_rq2_adapter", HERE / "wp2_p7b_c_node_h2.py")
r2 = h2.r2
r1 = r2.r1
base = h2.base

AUTHORITY_ID = "P7B-RQ2"
CELLS = {
    "B1": ("P7B-B1-S3", "B1", 1, []),
    "W1": ("P7B-W1-S3", "W1", 2, ["P7B-B1-S3"]),
    "B2": ("P7B-B2-S3", "B2", 3, ["P7B-B1-S3", "P7B-W1-S3"]),
}
EXPECTED_BLOBS = {
    "scripts/wp2_p7b_c_node_h2.py": "d66bc791455127ef87497cea3e912ee6f46e685b",
    "scripts/wp2_p7b_c_node_r2.py": "fa506e661f90fe9c21418fd2f86c8ca0a9230175",
    "src/wellpulse/p7b_session_ownership.py": "7810d1ed603fc305bd419c91a2b14bcca2e95e24",
    "scripts/wp2_p7b_service_restore_h2.sh": "72f465f274c86d7ec514f358023074aa26f96551",
    "scripts/wp2_p7b_target_node_preflight.sh": "b8c729cb077252ef6ce1ec2a7672f2ca4051e210",
    "experiments/WP-PWD01/p7b-executable-contract-v2.json": "233aabeaf3081470bc3ebc1ee04168f8932fc415",
    "experiments/WP-PWD01/p7b-target-runtime-contract-v2.json": "9531893989effb142e694294b95c0c7146353742",
    "experiments/WP-PWD01/p7b-modular-pipeline-contract-v1.json": "2c85af21f502c092c2da0ecb1bf615c8f705069b",
    "experiments/WP-PWD01/p7b-h2-requalification-authority-v1.json": "76522aa16d9af09d2f3d779a256236f752850245",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_env(name: str) -> str:
    value = str(os.environ.get(name, "")).strip()
    if not value:
        raise RuntimeError(f"REQUIRED_ENV_MISSING:{name}")
    return value


def verify_authority_and_sources() -> dict:
    authority = require_env("WP_AUTHORITY_ID")
    if authority != AUTHORITY_ID:
        raise RuntimeError(f"AUTHORITY_ID_MISMATCH:{authority}")
    source_sha = require_env("WP_SCIENTIFIC_SOURCE_SHA")
    if not re.fullmatch(r"[0-9a-f]{40}", source_sha):
        raise RuntimeError("SCIENTIFIC_SOURCE_SHA_INVALID")
    observed = {}
    for rel, expected in EXPECTED_BLOBS.items():
        path = ROOT / rel
        if not path.is_file():
            raise RuntimeError(f"PINNED_SOURCE_MISSING:{rel}")
        actual = git_blob_sha(path)
        observed[rel] = actual
        if actual != expected:
            raise RuntimeError(f"PINNED_BLOB_MISMATCH:{rel}:{actual}!={expected}")
    return {"authority_id": authority, "scientific_source_sha": source_sha, "pinned_blobs": observed}


def install_prospective_layers() -> dict:
    identity = h2.controller_identity()
    h2.install_h2_frontier_instrumentation()
    h2.install_h2_safe_restore(identity)
    h2.install_supplementary_exit_hooks()

    r2.verify_target_interpreter_and_python_dependencies()
    r2.inject_contract_authority()
    r2.verify_injection()
    r2.install_observed_attenuator_interface()
    r2.install_contract_aware_writer()
    r2.install_contract_aware_run_router()

    # Reproduce the frozen r1 receiver/path repair without calling r1.main(),
    # because this adapter owns module boundaries rather than the monolithic loop.
    base.start_receiver = r1.start_receiver
    base.receiver_initial_session_false = r1.receiver_initial_session_false
    base.run_cell = r1.run_cell
    return identity


def status_path() -> Path:
    return base.EVDIR / "p7b_c_status.json"


def load_status() -> dict:
    path = status_path()
    if not path.is_file():
        raise RuntimeError("SESSION_STATUS_MISSING")
    return json.loads(path.read_text(encoding="utf-8"))


def write_status(status: dict) -> None:
    base.write_json(status_path(), status)


def module_result(module_id: str, started_utc: str, gate: str, first_cause: str | None, authority: dict) -> None:
    out = base.EVDIR / "orchestration" / "module-results" / f"{module_id}.json"
    inputs = {
        "authority_id": authority["authority_id"],
        "scientific_source_sha": authority["scientific_source_sha"],
        "experiment_id": base.EXPERIMENT_ID,
        "run_id": base.RUN_ID,
    }
    status_sha = sha256_file(status_path()) if status_path().is_file() else None
    base.write_json(out, {
        "schema_version": "wp2-p7b-rq2-module-result-v1",
        "module_id": module_id,
        "run_id": base.RUN_ID,
        "experiment_id": base.EXPERIMENT_ID,
        "authority_id": authority["authority_id"],
        "scientific_source_sha": authority["scientific_source_sha"],
        "started_utc": started_utc,
        "ended_utc": utc_now(),
        "gate": gate,
        "first_cause": first_cause,
        "evidence_class": "NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION",
        "scored": False,
        "input_digest_sha256": hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest(),
        "status_digest_sha256": status_sha,
    })


def prepare_session(authority: dict) -> None:
    started = utc_now()
    module_id = "M3_Q0_BASELINE"
    try:
        if base.EVDIR.exists():
            raise RuntimeError("EVIDENCE_ROOT_ALREADY_EXISTS")
        base.EVDIR.mkdir(parents=True, exist_ok=False)
        (base.EVDIR / "orchestration").mkdir(parents=True)
        base.append_event("rq2_module_session_start", experiment_id=base.EXPERIMENT_ID, run_id=base.RUN_ID, scored=False)

        env = os.environ.copy()
        env.update({
            "WP_CORE_MANAGEMENT_HOST": base.CORE_MANAGEMENT_HOST,
            "WP_UE_MANAGEMENT_HOST": base.UE_MANAGEMENT_HOST,
            "WP_CORE_ALIAS": base.CORE_HOST,
            "WP_UE_ALIAS": base.UE_HOST,
            "WP_REMOTE_USER": base.REMOTE_USER,
        })
        p = base.run(["bash", str(ROOT / "scripts/wp2_golden_prepare_management_aliases.sh")], env=env)
        (base.EVDIR / "orchestration/management_alias_gate.txt").write_text(p.stdout, encoding="utf-8")
        if "WP2_GOLDEN_MANAGEMENT_ALIAS_GATE=PASS" not in p.stdout:
            raise RuntimeError("MANAGEMENT_ALIAS_GATE_FAIL")

        broker_dir = base.BROKER_DIR_CORE
        p = base.ssh_core(f"cd \"$HOME/WellPulse\" && bash powder/wp2_h_epc_broker.sh '{broker_dir}'")
        (base.EVDIR / "orchestration/broker_start.txt").write_text(p.stdout, encoding="utf-8")
        runtime = base.EVDIR / "runtime"
        runtime.mkdir(parents=True, exist_ok=True)
        ca_file = runtime / "ca.crt"
        broker_public = runtime / "broker_public.json"
        base.scp_core(f"{broker_dir}/ca.crt", ca_file)
        base.scp_core(f"{broker_dir}/broker_public.json", broker_public)
        broker_fp = json.loads(broker_public.read_text(encoding="utf-8"))["server_cert_sha256"]
        if not re.fullmatch(r"[0-9a-f]{64}", broker_fp):
            raise RuntimeError("BROKER_FINGERPRINT_INVALID")

        staged_jar = Path(require_env("WP_B2_JAR_STAGED")).resolve()
        if not staged_jar.is_file():
            raise RuntimeError("B2_STAGED_JAR_MISSING")
        jar = runtime / "paho.jar"
        shutil.copy2(staged_jar, jar)
        if base.sha256_file(jar) != base.B2_JAR_SHA:
            raise RuntimeError("B2_JAR_SHA256_MISMATCH")
        (runtime / "b2-classes").mkdir(parents=True, exist_ok=True)
        base.run(["javac", "-cp", str(jar), "-d", str(runtime / "b2-classes"),
                  str(ROOT / "experiments/WP-PWD01/b2-semantics/P7BRemoteB2Gateway.java")])

        status = {
            "schema_version": "wp2-p7b-c-status-v1",
            "run_id": base.RUN_ID,
            "experiment_id": base.EXPERIMENT_ID,
            "evidence_class": "NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION",
            "scored": False,
            "scored_runs_authorized": False,
            "completed_cells": [],
            "gate": "M3_Q0_BASELINE_RUNNING",
            "p7b_d": "NOT_STARTED",
            "teardown_authorized": False,
            "authority_id": authority["authority_id"],
            "scientific_source_sha": authority["scientific_source_sha"],
        }
        write_status(status)

        baseline = base.EVDIR / "orchestration" / "q0-baseline"
        baseline.mkdir(parents=True, exist_ok=False)
        base.set_attenuation(base.Q0_DB, baseline / "attenuator_q0_set.txt")
        t_service_ready = base.restore_service(baseline, ca_file)
        (baseline / "t_service_ready.txt").write_text(t_service_ready + "\n", encoding="utf-8")
        route, losses = base.route_and_probes(baseline)
        tls_ok = base.tls_mqtt_probe("P7B-RQ2-M3", ca_file, baseline)
        baseline_ok = "tun_srsue" in route and bool(losses) and max(losses) == 0.0 and tls_ok
        base.write_json(baseline / "q0_baseline_result.json", {
            "route_uses_tun_srsue": "tun_srsue" in route,
            "probe_losses_pct": losses,
            "tls_mqtt_qos1": tls_ok,
            "t_service_ready": t_service_ready,
            "gate": "PASS" if baseline_ok else "BLOCKED",
        })
        if not baseline_ok:
            raise RuntimeError("Q0_KNOWN_GOOD_BASELINE_FAIL")

        status["gate"] = "M3_Q0_BASELINE_PASS"
        write_status(status)
        base.append_event("rq2_m3_pass")
        module_result(module_id, started, "PASS", None, authority)
        print("WP2_P7B_RQ2_M3=PASS_Q0_KNOWN_GOOD_BASELINE")
    except Exception as exc:
        if status_path().is_file():
            status = load_status()
            status["gate"] = "BLOCKED"
            status["failure"] = f"{type(exc).__name__}:{exc}"
            status["teardown_authorized"] = False
            write_status(status)
        module_result(module_id, started, "BLOCKED", f"{type(exc).__name__}:{exc}", authority)
        raise


def run_one_cell(cell_key: str, authority: dict) -> None:
    cell_id, arch, order, required_completed = CELLS[cell_key]
    module_id = {"B1": "M4_B1", "W1": "M6_W1", "B2": "M8_B2"}[cell_key]
    started = utc_now()
    try:
        status = load_status()
        if status.get("authority_id") != authority["authority_id"] or status.get("scientific_source_sha") != authority["scientific_source_sha"]:
            raise RuntimeError("SESSION_AUTHORITY_FREEZE_MISMATCH")
        if status.get("completed_cells") != required_completed:
            raise RuntimeError(f"CELL_ORDER_OR_PRIOR_PASS_VIOLATION:{status.get('completed_cells')}!={required_completed}")
        if order == 1 and status.get("gate") != "M3_Q0_BASELINE_PASS":
            raise RuntimeError("M3_Q0_BASELINE_NOT_PASS")

        ca_file = base.EVDIR / "runtime" / "ca.crt"
        broker_public = base.EVDIR / "runtime" / "broker_public.json"
        if not ca_file.is_file() or not broker_public.is_file():
            raise RuntimeError("SESSION_RUNTIME_EVIDENCE_MISSING")
        broker_fp = json.loads(broker_public.read_text(encoding="utf-8"))["server_cert_sha256"]
        jar = base.EVDIR / "runtime" / "paho.jar"
        if not jar.is_file() or base.sha256_file(jar) != base.B2_JAR_SHA:
            raise RuntimeError("B2_RUNTIME_JAR_MISSING_OR_DRIFTED")

        base.run_cell(cell_id, arch, order, ca_file, f"{base.BROKER_DIR_CORE}/ca.crt", broker_fp)
        status = load_status()
        status["completed_cells"] = required_completed + [cell_id]
        status["gate"] = f"{module_id}_PASS"
        status.pop("failure", None)
        write_status(status)
        base.append_event("cell_pass", cell=cell_id)
        module_result(module_id, started, "PASS", None, authority)
        print(f"WP2_P7B_RQ2_{cell_key}=PASS")
    except Exception as exc:
        if status_path().is_file():
            status = load_status()
            status["gate"] = "BLOCKED"
            status["failure"] = f"{type(exc).__name__}:{exc}"
            status["teardown_authorized"] = False
            write_status(status)
        module_result(module_id, started, "BLOCKED", f"{type(exc).__name__}:{exc}", authority)
        raise


def reconstruct(authority: dict) -> None:
    started = utc_now()
    module_id = "M10_RECONSTRUCT"
    try:
        status = load_status()
        expected = ["P7B-B1-S3", "P7B-W1-S3", "P7B-B2-S3"]
        if status.get("completed_cells") != expected:
            raise RuntimeError("RECONSTRUCTION_REQUIRES_ALL_THREE_CELLS")
        core_root = r2.resolved_core_root()
        out = base.EVDIR / "analysis" / "reconstruction_console.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        p = base.run([
            base.PY,
            str(ROOT / "scripts/reconstruct_wp2_p7b_v2.py"),
            "--root", str(base.EVDIR),
            "--core-root", core_root,
            "--contract", str(r2.CONTRACT_PATH),
        ], check=False)
        out.write_text(p.stdout, encoding="utf-8")
        if p.returncode != 0 or "WP2_P7B_RECONSTRUCTION=PASS" not in p.stdout:
            raise RuntimeError("P7B_RQ2_RECONSTRUCTION_FAIL")
        status["gate"] = "PASS_NON_SCORED_PHYSICAL_QUALIFICATION"
        status["teardown_authorized"] = False
        status["teardown_ready"] = False
        write_status(status)
        base.append_event("rq2_reconstruction_pass")
        module_result(module_id, started, "PASS", None, authority)
        print("WP2_P7B_RQ2_M10=PASS_NON_SCORED_RECONSTRUCTION")
        print("SCORED_AUTHORIZATION=BLOCKED")
        print("TEARDOWN_AUTHORIZED=NO")
    except Exception as exc:
        if status_path().is_file():
            status = load_status()
            status["gate"] = "BLOCKED"
            status["failure"] = f"{type(exc).__name__}:{exc}"
            status["teardown_authorized"] = False
            write_status(status)
        module_result(module_id, started, "BLOCKED", f"{type(exc).__name__}:{exc}", authority)
        raise


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("module", choices=["prepare", "B1", "W1", "B2", "reconstruct"])
    return p.parse_args()


def main() -> int:
    args = parse_args()
    authority = verify_authority_and_sources()
    identity = install_prospective_layers()
    print("P7B_RQ2_AUTHORITY_ID=PASS:P7B-RQ2", flush=True)
    print("CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS", flush=True)
    print(f"CONTROLLER_SESSION={identity['controller_session']}", flush=True)
    print("AUTOMATIC_RETRY=NO", flush=True)
    print("SCORED_AUTHORIZATION=BLOCKED", flush=True)
    print("TEARDOWN_AUTHORIZED=NO", flush=True)

    if args.module == "prepare":
        prepare_session(authority)
    elif args.module in CELLS:
        run_one_cell(args.module, authority)
    else:
        reconstruct(authority)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
