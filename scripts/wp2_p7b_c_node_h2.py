#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import re
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


def install_h2_safe_restore(identity: dict) -> None:
    def restore_service(cell_dir: Path, ca_file: Path) -> str:
        restore_out = cell_dir / "service_restore.txt"
        env = os.environ.copy()
        env.update(
            {
                "WP_CORE_HOST": base.CORE_HOST,
                "WP_UE_HOST": base.UE_HOST,
                "WP_REMOTE_USER": base.REMOTE_USER,
                "WP_RESTORE_OUT": str(restore_out),
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
        p2 = base.run(["bash", str(ROOT / "scripts/wp2_golden_service_ready_probe.sh")], env=env, timeout=140)
        (cell_dir / "service_ready_console.txt").write_text(p2.stdout, encoding="utf-8")
        m2 = re.search(r"T_SERVICE_READY=(\S+)", probe_out.read_text(encoding="utf-8"))
        if not m2:
            raise RuntimeError("T_SERVICE_READY_MISSING")
        return m2.group(1)

    base.restore_service = restore_service


def main() -> int:
    identity = controller_identity()
    print("CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS", flush=True)
    print("CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION=PASS", flush=True)
    print("DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO", flush=True)
    print(f"CONTROLLER_SESSION={identity['controller_session']}", flush=True)
    install_h2_safe_restore(identity)
    print("P7B_H2_PROSPECTIVE_ENTRYPOINT=scripts/wp2_p7b_c_node_h2.py", flush=True)
    print("LIVE_AUTHORIZATION=SEPARATE_REQUIRED", flush=True)
    print("SCORED_AUTHORIZATION=BLOCKED", flush=True)
    return r2.main()


if __name__ == "__main__":
    raise SystemExit(main())
