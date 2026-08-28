#!/usr/bin/env python3
from __future__ import annotations

import atexit
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))
from wellpulse.p7b_session_ownership import evaluate_controller_identity


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_LOAD_FAIL:{path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r2 = _load("wp2_p7b_c_node_r2_h2_base", HERE / "wp2_p7b_c_node_r2.py")
base = r2.base
_FRONTIER_STATE: dict[str, dict] = {}
_EXIT_HOOKS_INSTALLED = False


def _durable_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    data = json.dumps(value, indent=2, sort_keys=True) + "\n"
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)
    try:
        dfd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    except OSError:
        pass


def _durable_jsonl(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(fd, line.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)


def _frontier_row(phase: str, status: str) -> dict:
    return {
        "phase": phase,
        "utc": base.utc_now(),
        "monotonic": base.mono(),
        "status": status,
    }


def controller_identity() -> dict:
    pid = os.getpid()
    comm_path = Path("/proc/self/comm")
    process_name = comm_path.read_text(encoding="utf-8").strip() if comm_path.exists() else Path(sys.executable).name
    if os.environ.get("TMUX"):
        p = base.run(["tmux", "display-message", "-p", "#S"], check=False)
        session = p.stdout.strip() if p.returncode == 0 else ""
        if not session:
            raise RuntimeError("CONTROLLER_TMUX_SESSION_UNKNOWN")
    else:
        session = "NONE"
    host_role = os.environ.get("WP_CONTROLLER_HOST_ROLE", "UE").strip().upper()
    result = evaluate_controller_identity(
        controller_pid=pid,
        controller_session=session,
        controller_process_name=process_name,
        controller_host_role=host_role,
    )
    if result["gate"] != "PASS":
        raise RuntimeError("CONTROLLER_OWNERSHIP_GATE_BLOCKED:" + ",".join(result["failures"]))
    return result


def _state(cell_dir: Path) -> dict:
    key = str(cell_dir.resolve())
    return _FRONTIER_STATE.setdefault(key, {"cell_dir": cell_dir, "gateway_start_count": 0, "transition_written": False})


def install_h2_frontier_instrumentation() -> None:
    original_start_generator = base.start_generator
    original_start_python_gateway = base.start_python_gateway
    original_start_b2_gateway = base.start_b2_gateway
    original_close_process = base.close_process
    original_wait_gateway_started = base.wait_gateway_started

    def start_generator(arch: str, cell_run: str, cell_dir: Path, fifo, queue_db):
        p = original_start_generator(arch, cell_run, cell_dir, fifo, queue_db)
        st = _state(cell_dir)
        st["generator"] = p
        st["generator_pid_before"] = p.pid
        st["arch"] = arch
        st["cell_run"] = cell_run
        return p

    def _record_gateway_start(st: dict, arch: str, cell_run: str, p, *, cid: str | None = None, topic: str | None = None) -> None:
        st["gateway_start_count"] += 1
        if cid is None or topic is None:
            topic_arch = {"B1": "B1_MQTT_QOS1", "W1": "W1_OFFLINE_FIRST"}[arch]
            cid = base.make_run_client_id(cell_run, topic_arch)
            topic = base.make_run_topic(cell_run, topic_arch)
        st["client_identity"] = cid
        st["topic_identity"] = topic
        if st["gateway_start_count"] == 1:
            st["old_gateway_pid"] = p.pid
        elif st["gateway_start_count"] == 2:
            st["new_gateway_pid"] = p.pid
            st["new_gateway_start_observed"] = True
            st["new_start_utc"] = base.utc_now()
            st["new_start_monotonic"] = base.mono()

    def start_python_gateway(arch: str, cell_run: str, cell_dir: Path, ca_file: Path, broker_fp: str, fifo, queue_db):
        p = original_start_python_gateway(arch, cell_run, cell_dir, ca_file, broker_fp, fifo, queue_db)
        _record_gateway_start(_state(cell_dir), arch, cell_run, p)
        return p

    def start_b2_gateway(cell_run: str, cell_dir: Path, ca_file: Path, fifo: Path, persist: Path, topic: str, cid: str):
        p = original_start_b2_gateway(cell_run, cell_dir, ca_file, fifo, persist, topic, cid)
        _record_gateway_start(_state(cell_dir), "B2", cell_run, p, cid=cid, topic=topic)
        return p

    def close_process(p, *, abrupt=False, timeout_s=15) -> None:
        match = None
        for st in _FRONTIER_STATE.values():
            if st.get("gateway_start_count") == 1 and st.get("old_gateway_pid") == getattr(p, "pid", None) and "old_exit_utc" not in st:
                match = st
                break
        if match is not None:
            match["restart_request_utc"] = base.utc_now()
            match["restart_request_monotonic"] = base.mono()
        original_close_process(p, abrupt=abrupt, timeout_s=timeout_s)
        if match is not None:
            match["old_gateway_exit_observed"] = p.poll() is not None
            match["old_exit_utc"] = base.utc_now()
            match["old_exit_monotonic"] = base.mono()

    def wait_gateway_started(arch: str, cell_dir: Path, p, prior_start_count: int) -> None:
        original_wait_gateway_started(arch, cell_dir, p, prior_start_count)
        st = _state(cell_dir)
        if st.get("gateway_start_count") < 2 or st.get("transition_written"):
            return
        st["new_ready_utc"] = base.utc_now()
        st["new_ready_monotonic"] = base.mono()
        generator = st.get("generator")
        generator_alive = generator is not None and generator.poll() is None
        source_continuity = generator_alive and base.generator_continuity(cell_dir / "telemetry_generated.csv")
        transition = {
            "generator_pid_before": st.get("generator_pid_before"),
            "generator_pid_after": getattr(generator, "pid", None),
            "old_gateway_pid": st.get("old_gateway_pid"),
            "old_gateway_exit_observed": bool(st.get("old_gateway_exit_observed")),
            "new_gateway_pid": st.get("new_gateway_pid"),
            "new_gateway_start_observed": bool(st.get("new_gateway_start_observed")),
            "client_identity": st.get("client_identity"),
            "topic_identity": st.get("topic_identity"),
            "restart_request_utc": st.get("restart_request_utc"),
            "restart_request_monotonic": st.get("restart_request_monotonic"),
            "old_exit_utc": st.get("old_exit_utc"),
            "old_exit_monotonic": st.get("old_exit_monotonic"),
            "new_start_utc": st.get("new_start_utc"),
            "new_start_monotonic": st.get("new_start_monotonic"),
            "new_ready_utc": st.get("new_ready_utc"),
            "new_ready_monotonic": st.get("new_ready_monotonic"),
            "source_generation_continuity_status": "PASS" if source_continuity else "BLOCKED",
        }
        _durable_json(cell_dir / "restart_transition.json", transition)
        st["transition_written"] = True
        required = [
            "generator_pid_before", "generator_pid_after", "old_gateway_pid", "new_gateway_pid",
            "client_identity", "topic_identity", "restart_request_utc", "restart_request_monotonic",
            "old_exit_utc", "old_exit_monotonic", "new_start_utc", "new_start_monotonic",
            "new_ready_utc", "new_ready_monotonic",
        ]
        if any(transition.get(k) in (None, "") for k in required):
            raise RuntimeError("RESTART_TRANSITION_REQUIRED_FIELD_MISSING")
        if not transition["old_gateway_exit_observed"] or not transition["new_gateway_start_observed"]:
            raise RuntimeError("RESTART_TRANSITION_PROCESS_OBSERVATION_FAIL")
        if transition["source_generation_continuity_status"] != "PASS":
            raise RuntimeError("RESTART_TRANSITION_SOURCE_CONTINUITY_FAIL")

    base.start_generator = start_generator
    base.start_python_gateway = start_python_gateway
    base.start_b2_gateway = start_b2_gateway
    base.close_process = close_process
    base.wait_gateway_started = wait_gateway_started


def install_h2_safe_restore(identity: dict) -> None:
    def restore_service(cell_dir: Path, ca_file: Path) -> str:
        restore_out = cell_dir / "service_restore.txt"
        frontier = cell_dir / "restoration_frontier.jsonl"
        env = os.environ.copy()
        env.update(
            {
                "WP_CORE_HOST": base.CORE_HOST,
                "WP_UE_HOST": base.UE_HOST,
                "WP_REMOTE_USER": base.REMOTE_USER,
                "WP_RESTORE_OUT": str(restore_out),
                "WP_RESTORE_FRONTIER": str(frontier),
                "WP_CONTROLLER_PID": str(identity["controller_pid"]),
                "WP_CONTROLLER_SESSION": str(identity["controller_session"]),
                "WP_CONTROLLER_HOST_ROLE": str(identity["controller_host_role"]),
            }
        )
        p = base.run(["bash", str(ROOT / "scripts/wp2_p7b_service_restore_h2.sh")], env=env, timeout=180)
        (cell_dir / "service_restore_console.txt").write_text(p.stdout, encoding="utf-8")
        text = restore_out.read_text(encoding="utf-8")
        if "CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS" not in text:
            raise RuntimeError("CONTROLLER_SESSION_DISJOINTNESS_MARKER_MISSING")
        if "CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION=PASS" not in text:
            raise RuntimeError("CONTROLLER_FAILURE_DOMAIN_MARKER_MISSING")
        if "DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO" not in text:
            raise RuntimeError("TMUX_DESTRUCTIVE_POLICY_MARKER_MISSING")
        m = re.search(r"RESTORE_START_EPOCH=(\d+)", text)
        if not m:
            raise RuntimeError("RESTORE_START_EPOCH_MISSING")
        probe_out = cell_dir / "service_ready_probe.txt"
        env.update(
            {
                "WP_CA_FILE": str(ca_file),
                "WP_RESTORE_START_EPOCH": m.group(1),
                "WP_SERVICE_PROBE_OUT": str(probe_out),
                "WP_SERVICE_BOUND_S": "120",
            }
        )
        _durable_jsonl(frontier, _frontier_row("SERVICE_READY_PROBE_BEGIN", "BEGIN"))
        p2 = base.run(["bash", str(ROOT / "scripts/wp2_golden_service_ready_probe.sh")], env=env, timeout=140, check=False)
        (cell_dir / "service_ready_console.txt").write_text(p2.stdout, encoding="utf-8")
        _durable_jsonl(frontier, _frontier_row("SERVICE_READY_PROBE_END", "PASS" if p2.returncode == 0 else "FAIL"))
        if p2.returncode != 0:
            raise RuntimeError(f"SERVICE_READY_PROBE_FAIL:rc={p2.returncode}")
        m2 = re.search(r"T_SERVICE_READY=(\S+)", probe_out.read_text(encoding="utf-8"))
        if not m2:
            raise RuntimeError("T_SERVICE_READY_MISSING")
        return m2.group(1)

    base.restore_service = restore_service


def _supplementary_exit_marker(reason: str, signum: int | None = None) -> None:
    try:
        path = base.EVDIR / "orchestration" / "controller_survival_frontier.jsonl"
        if not path.parent.exists():
            return
        _durable_jsonl(path, {
            "phase": "CONTROLLER_EXIT_OBSERVED",
            "utc": base.utc_now(),
            "monotonic": base.mono(),
            "status": reason,
            "signal": signum,
            "supplementary_only": True,
        })
    except Exception:
        pass


def install_supplementary_exit_hooks() -> None:
    global _EXIT_HOOKS_INSTALLED
    if _EXIT_HOOKS_INSTALLED:
        return
    _EXIT_HOOKS_INSTALLED = True
    atexit.register(_supplementary_exit_marker, "EXIT", None)

    def handler(signum, _frame):
        _supplementary_exit_marker(signal.Signals(signum).name, signum)
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGHUP, handler)


def main() -> int:
    identity = controller_identity()
    print("CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS", flush=True)
    print("CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION=PASS", flush=True)
    print("DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO", flush=True)
    print(f"CONTROLLER_SESSION={identity['controller_session']}", flush=True)
    install_h2_frontier_instrumentation()
    install_h2_safe_restore(identity)
    install_supplementary_exit_hooks()
    print("P7B_H2_RESTART_TRANSITION_EVIDENCE=ARMED", flush=True)
    print("P7B_H2_RESTORATION_FRONTIER_EVIDENCE=ARMED", flush=True)
    print("P7B_H2_PARENT_EXIT_HOOKS=SUPPLEMENTARY_ONLY", flush=True)
    print("P7B_H2_PROSPECTIVE_ENTRYPOINT=scripts/wp2_p7b_c_node_h2.py", flush=True)
    print("LIVE_AUTHORIZATION=SEPARATE_REQUIRED", flush=True)
    print("SCORED_AUTHORIZATION=BLOCKED", flush=True)
    return r2.main()


if __name__ == "__main__":
    raise SystemExit(main())
