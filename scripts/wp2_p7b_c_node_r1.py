#!/usr/bin/env python3
from __future__ import annotations

import importlib.metadata
import importlib.util
import json
from pathlib import Path, PurePosixPath
import shlex
import sys
import time

HERE = Path(__file__).resolve().parent


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_LOAD_FAIL:{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = _load_module("wp2_p7b_c_node_base", HERE / "wp2_p7b_c_node.py")
paths = _load_module("wp2_p7b_path_contract", HERE / "wp2_p7b_path_contract.py")

_CORE_HOME: str | None = None
_DIAGNOSTIC_CELLS: set[str] = set()


def _q(value: str) -> str:
    return shlex.quote(value)


def resolve_core_home() -> str:
    global _CORE_HOME
    if _CORE_HOME is not None:
        return _CORE_HOME
    p = base.ssh_core('printf "%s" "$HOME"', check=False, timeout=15)
    if p.returncode != 0:
        raise RuntimeError("CORE_HOME_RESOLUTION_FAIL")
    home = paths.require_absolute_remote_path(p.stdout.strip())
    _CORE_HOME = home
    return home


def resolve_core_cell_dir(core_cell_dir: str) -> str:
    if core_cell_dir.startswith("$HOME/"):
        suffix = core_cell_dir[len("$HOME/") :]
        if not suffix or "$" in suffix or "~" in suffix:
            raise RuntimeError("CORE_CELL_DIR_UNSAFE_SUFFIX")
        value = str(PurePosixPath(resolve_core_home()) / PurePosixPath(suffix))
    else:
        value = core_cell_dir
    return paths.require_absolute_remote_path(value)


def _print_local_tail(label: str, path: Path, max_lines: int = 120) -> None:
    print(f"--- {label} ---", flush=True)
    if not path.exists():
        print("MISSING", flush=True)
        return
    text = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in text[-max_lines:]:
        print(line, flush=True)


def emit_failure_diagnostics(cell_id: str, core_cell_dir: str, receiver_pid: int | None = None) -> None:
    if cell_id in _DIAGNOSTIC_CELLS:
        return
    _DIAGNOSTIC_CELLS.add(cell_id)
    local_cell = base.EVDIR / "cells" / cell_id
    try:
        resolved = resolve_core_cell_dir(core_cell_dir)
        contract = paths.receiver_path_contract(resolved)
    except Exception as exc:
        resolved = "UNRESOLVED"
        contract = {"path_contract_error": f"{type(exc).__name__}:{exc}"}

    print(f"::group::P7B-R1 bounded raw diagnostics — {cell_id}", flush=True)
    print("P7B_R1_DIAGNOSTICS_BEGIN", flush=True)
    print("CELL_ID=" + cell_id, flush=True)
    print("CORE_CELL_DIR_RESOLVED=" + resolved, flush=True)
    print("RECEIVER_PATH_CONTRACT=" + json.dumps(contract, sort_keys=True), flush=True)
    print("RECEIVER_PID=" + (str(receiver_pid) if receiver_pid is not None else "UNKNOWN"), flush=True)

    print("--- runtime/version locks ---", flush=True)
    print("PYTHON=" + sys.version.replace("\n", " "), flush=True)
    try:
        print("PAHO_MQTT=" + importlib.metadata.version("paho-mqtt"), flush=True)
    except Exception as exc:
        print(f"PAHO_MQTT=UNAVAILABLE:{type(exc).__name__}", flush=True)
    java = base.run(["java", "-version"], check=False, timeout=10)
    print("JAVA_VERSION_RC=" + str(java.returncode), flush=True)
    print((java.stdout or "")[-2000:], flush=True)
    jar = base.EVDIR / "runtime" / "paho.jar"
    if jar.exists():
        print("PAHO_JAVA_JAR_SHA256=" + base.sha256_file(jar), flush=True)
    else:
        print("PAHO_JAVA_JAR_SHA256=MISSING", flush=True)
    broker_public = base.EVDIR / "runtime" / "broker_public.json"
    if broker_public.exists():
        try:
            obj = json.loads(broker_public.read_text(encoding="utf-8"))
            print("BROKER_SERVER_CERT_SHA256=" + str(obj.get("server_cert_sha256", "MISSING")), flush=True)
        except Exception:
            print("BROKER_SERVER_CERT_SHA256=UNPARSEABLE", flush=True)

    _print_local_tail("route", local_cell / "route_output.txt", 40)
    _print_local_tail("Q0 probes", local_cell / "q0_user_plane_probes.txt", 120)
    _print_local_tail("TLS/MQTT probe", local_cell / "tls_mqtt_probe.txt", 40)
    _print_local_tail("Q0 radio capture", local_cell / "q0_radio_capture.txt", 80)
    _print_local_tail("runtime manifest", local_cell / "runtime_manifest.json", 120)
    _print_local_tail("readiness observation", local_cell / "readiness_observation.json", 120)
    _print_local_tail("readiness verdict", local_cell / "readiness_verdict.json", 120)

    if resolved != "UNRESOLVED":
        receiver_dir = str(PurePosixPath(resolved) / "receiver")
        console = str(PurePosixPath(receiver_dir) / "console.txt")
        events = str(PurePosixPath(receiver_dir) / "receiver_events.jsonl")
        pid_expr = str(receiver_pid) if receiver_pid is not None else ""
        remote = f"""set +e
printf '%s\n' '--- receiver process state ---'
if [ -n '{pid_expr}' ]; then ps -p '{pid_expr}' -o pid=,ppid=,stat=,etime=,args= 2>&1 || true; else pgrep -af 'wp_pwd01_h_receiver.py' | tail -20 || true; fi
printf '%s\n' '--- receiver console tail ---'
tail -n 100 {_q(console)} 2>&1 || true
printf '%s\n' '--- receiver events tail ---'
tail -n 100 {_q(events)} 2>&1 || true
printf '%s\n' '--- broker log tail ---'
tail -n 120 {_q(base.BROKER_DIR_CORE + '/mosquitto.log')} 2>&1 || true
"""
        rp = base.ssh_core(remote, check=False, timeout=20)
        print((rp.stdout or "")[-16000:], flush=True)
        print("CORE_DIAGNOSTIC_RC=" + str(rp.returncode), flush=True)

    print("P7B_R1_DIAGNOSTICS_END", flush=True)
    print("::endgroup::", flush=True)


def start_receiver(cell_run: str, topic: str, core_cell_dir: str, ca_core: str) -> int:
    resolved_cell = resolve_core_cell_dir(core_cell_dir)
    contract = paths.receiver_path_contract(resolved_cell)
    if contract["writer_watcher_path_equal"] is not True:
        raise RuntimeError("RECEIVER_WRITER_WATCHER_PATH_MISMATCH")
    if contract["contains_unexpanded_shell_token"] is not False:
        raise RuntimeError("RECEIVER_PATH_UNEXPANDED_SHELL_TOKEN")

    cell_id = PurePosixPath(resolved_cell).name
    local_cell = base.EVDIR / "cells" / cell_id
    local_cell.mkdir(parents=True, exist_ok=True)
    base.write_json(local_cell / "receiver_path_contract.json", contract)

    receiver_dir = str(contract["receiver_output_dir"])
    event_path = str(contract["receiver_event_writer_path"])
    console_path = str(contract["receiver_console_path"])
    home = resolve_core_home()
    repo_dir = str(PurePosixPath(home) / "WellPulse")
    py = str(PurePosixPath(home) / ".wp2-golden-venv" / "bin" / "python")

    cmd = (
        "set -eu; "
        f"mkdir -p {_q(receiver_dir)}; cd {_q(repo_dir)}; "
        f"nohup {_q(py)} scripts/wp_pwd01_h_receiver.py "
        f"--run-id {_q(cell_run)} --host {_q(base.BROKER_HOST)} --port {base.BROKER_PORT} "
        f"--topic {_q(topic)} --ca-file {_q(ca_core)} --output-dir {_q(receiver_dir)} "
        f">{_q(console_path)} 2>&1 </dev/null & echo $!"
    )
    p = base.ssh_core(cmd)
    pid = int(p.stdout.strip().splitlines()[-1])
    deadline = time.monotonic() + 20
    connected_marker = '"event":"receiver_connect"'
    while time.monotonic() < deadline:
        probe = (
            "set +e; "
            f"if test -s {_q(event_path)} && grep -q {_q(connected_marker)} {_q(event_path)}; then echo CONNECTED; "
            f"elif kill -0 {pid} 2>/dev/null; then echo ALIVE; else echo EXITED; fi"
        )
        q = base.ssh_core(probe, check=False, timeout=10)
        state = (q.stdout or "").strip().splitlines()[-1] if (q.stdout or "").strip() else "UNKNOWN"
        if state == "CONNECTED":
            return pid
        if state == "EXITED":
            emit_failure_diagnostics(cell_id, resolved_cell, pid)
            raise RuntimeError(f"RECEIVER_EXITED_BEFORE_CONNECT:pid={pid}")
        time.sleep(0.5)

    emit_failure_diagnostics(cell_id, resolved_cell, pid)
    raise RuntimeError(f"RECEIVER_CONNECT_TIMEOUT:pid={pid}")


def receiver_initial_session_false(core_cell_dir: str) -> bool:
    resolved = resolve_core_cell_dir(core_cell_dir)
    event_path = str(PurePosixPath(resolved) / "receiver" / "receiver_events.jsonl")
    p = base.ssh_core(f"cat {_q(event_path)}", check=False)
    for line in p.stdout.splitlines():
        try:
            row = json.loads(line)
        except Exception:
            continue
        if row.get("event") == "receiver_connect":
            return row.get("session_present") is False
    return False


_original_run_cell = base.run_cell


def run_cell(cell_id: str, arch: str, order: int, ca_file: Path, ca_core: str, broker_fp: str) -> None:
    core_literal = f"$HOME/wellpulse-powder-evidence/p7b/{base.RUN_ID}-core/cells/{cell_id}"
    try:
        return _original_run_cell(cell_id, arch, order, ca_file, ca_core, broker_fp)
    except Exception:
        emit_failure_diagnostics(cell_id, core_literal, None)
        raise


def main() -> int:
    # Monkey-patch only the operational receiver/path surface. Scientific cell
    # schedule, RF values, clocks, workload, reconstruction and stop rules stay
    # in the frozen base runner unchanged.
    base.start_receiver = start_receiver
    base.receiver_initial_session_false = receiver_initial_session_false
    base.run_cell = run_cell
    print("P7B_R1_RUNNER=REPAIRED_RECEIVER_PATH_AND_OBSERVABILITY", flush=True)
    print("SCORED_AUTHORIZATION=BLOCKED", flush=True)
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
