#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from wellpulse.p7b_session_ownership import evaluate_controller_identity, evaluate_pid_ownership

DELTA = ROOT / "experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json"
BASE_CONTRACT = ROOT / "experiments/WP-PWD01/p7b-executable-contract-v2.json"
H2_ENTRY = ROOT / "scripts/wp2_p7b_c_node_h2.py"
SAFE_RESTORE = ROOT / "scripts/wp2_p7b_service_restore_h2.sh"

REQUIRED_CASES = (
    "CONTROLLER_IN_TMUX_UE_REJECTED_BEFORE_RF",
    "ALLOWED_CONTROLLER_SURVIVES_SERVICE_CLEANUP",
    "SERVICE_OWNERSHIP_SELECTION_CANNOT_MATCH_CONTROLLER_PID_OR_SESSION",
    "RESTART_TRANSITION_SURVIVES_SYNTHETIC_FAILURE_AFTER_GATEWAY_RESTART",
    "EACH_RESTORE_PHASE_FAILURE_PRESERVES_LAST_FRONTIER",
    "FROZEN_SCIENTIFIC_CONTROLS_UNCHANGED",
    "AUTOMATIC_RETRY_NOT_INTRODUCED",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _run(cmd: list[str], *, env: dict[str, str] | None = None, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=timeout)


def case_controller_in_tmux_ue_rejected() -> dict:
    result = evaluate_controller_identity(
        controller_pid=4242,
        controller_session="ue",
        controller_process_name="python3",
        controller_host_role="UE",
    )
    _require(result["gate"] == "BLOCKED", result)
    _require("CONTROLLER_IN_SERVICE_CLEANUP_SESSION:ue" in result["failures"], result["failures"])
    main_text = H2_ENTRY.read_text(encoding="utf-8")
    _require(main_text.index("identity = controller_identity()") < main_text.index("return r2.main()"), "controller gate must precede inherited live path")
    return {"gate": result["gate"], "failure": "CONTROLLER_IN_SERVICE_CLEANUP_SESSION:ue"}


def case_allowed_controller_survives_cleanup() -> dict:
    identity = evaluate_controller_identity(
        controller_pid=4242,
        controller_session="NONE",
        controller_process_name="python3",
        controller_host_role="UE",
    )
    _require(identity["gate"] == "PASS", identity)
    ownership = evaluate_pid_ownership(
        controller_pid=4242,
        controller_host_role="UE",
        target_host_role="UE",
        service_pids_by_name={"srsue": [5001, 5002]},
    )
    _require(ownership["gate"] == "PASS", ownership)
    _require(ownership["DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED"] is False, ownership)
    shell = SAFE_RESTORE.read_text(encoding="utf-8")
    _require("tmux kill-session" not in shell, "unsafe tmux kill-session reintroduced")
    _require("killall" not in shell and "pkill -f" not in shell, "generic destructive cleanup reintroduced")
    return {"identity_gate": "PASS", "ownership_gate": "PASS", "controller_pid": 4242}


def case_service_ownership_collision_blocks() -> dict:
    collision = evaluate_pid_ownership(
        controller_pid=4242,
        controller_host_role="UE",
        target_host_role="UE",
        service_pids_by_name={"srsue": [4242, 5001]},
    )
    _require(collision["gate"] == "BLOCKED", collision)
    _require(any(x.startswith("CONTROLLER_PID_SELECTED_FOR_SERVICE_CLEANUP:srsue:4242") for x in collision["failures"]), collision["failures"])
    session = evaluate_controller_identity(
        controller_pid=4242,
        controller_session="srs-ue",
        controller_process_name="python3",
        controller_host_role="UE",
    )
    _require(session["gate"] == "BLOCKED", session)
    return {"pid_collision": "BLOCKED", "session_collision": "BLOCKED"}


RESTART_HARNESS = r"""
import importlib.util
import json
import os
from pathlib import Path
import tempfile

root = Path(os.environ["WP_REPO_ROOT"])
entry = root / "scripts/wp2_p7b_c_node_h2.py"
spec = importlib.util.spec_from_file_location("h2_adversarial_entry", entry)
if spec is None or spec.loader is None:
    raise RuntimeError("H2_IMPORT_FAIL")
h2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h2)
base = h2.base

class Proc:
    def __init__(self, pid):
        self.pid = pid
        self.done = False
    def poll(self):
        return 0 if self.done else None

gw_counter = {"n": 0}
clock = {"n": 0}
def tick():
    clock["n"] += 1
    return clock["n"]

def start_generator(arch, cell_run, cell_dir, fifo, queue_db):
    return Proc(1001)

def start_python_gateway(arch, cell_run, cell_dir, ca_file, broker_fp, fifo, queue_db):
    gw_counter["n"] += 1
    return Proc(2000 + gw_counter["n"])

def start_b2_gateway(cell_run, cell_dir, ca_file, fifo, persist, topic, cid):
    gw_counter["n"] += 1
    return Proc(3000 + gw_counter["n"])

def close_process(p, *, abrupt=False, timeout_s=15):
    p.done = True

def wait_gateway_started(arch, cell_dir, p, prior_start_count):
    return None

base.start_generator = start_generator
base.start_python_gateway = start_python_gateway
base.start_b2_gateway = start_b2_gateway
base.close_process = close_process
base.wait_gateway_started = wait_gateway_started
base.generator_continuity = lambda path: True
base.utc_now = lambda: f"2026-08-28T00:00:{tick():02d}+00:00"
base.mono = lambda: tick()
base.make_run_client_id = lambda run_id, arch: f"cid-{run_id}-{arch}"
base.make_run_topic = lambda run_id, arch: f"topic/{run_id}/{arch}"
h2._FRONTIER_STATE.clear()
h2.install_h2_frontier_instrumentation()

with tempfile.TemporaryDirectory() as td:
    cell = Path(td) / "cell"
    cell.mkdir(parents=True)
    gen = base.start_generator("B1", "run", cell, None, None)
    old = base.start_python_gateway("B1", "run", cell, Path("/tmp/ca"), "fp", None, None)
    base.close_process(old)
    new = base.start_python_gateway("B1", "run", cell, Path("/tmp/ca"), "fp", None, None)
    base.wait_gateway_started("B1", cell, new, 1)
    transition = cell / "restart_transition.json"
    if not transition.exists():
        raise RuntimeError("TRANSITION_MISSING")
    obj = json.loads(transition.read_text(encoding="utf-8"))
    if obj["old_gateway_pid"] == obj["new_gateway_pid"]:
        raise RuntimeError("PID_DID_NOT_CHANGE")
    if obj["source_generation_continuity_status"] != "PASS":
        raise RuntimeError("SOURCE_CONTINUITY_NOT_PASS")
    if (cell / "restart_proof.json").exists():
        raise RuntimeError("FINAL_PROOF_SHOULD_NOT_EXIST_IN_SYNTHETIC_FRONTIER_TEST")
    try:
        raise RuntimeError("SYNTHETIC_FAILURE_AFTER_RESTART_TRANSITION")
    except RuntimeError:
        pass
    obj2 = json.loads(transition.read_text(encoding="utf-8"))
    if obj2 != obj:
        raise RuntimeError("TRANSITION_CHANGED_AFTER_SYNTHETIC_FAILURE")
    print(json.dumps({"transition_survived": True, "old_gateway_pid": obj["old_gateway_pid"], "new_gateway_pid": obj["new_gateway_pid"]}))
"""


def case_restart_transition_survives() -> dict:
    env = os.environ.copy()
    env.update(
        {
            "WP_REPO_ROOT": str(ROOT),
            "WP_RUN_ID": "h2-adversarial",
            "WP_EXPERIMENT_ID": "offline-no-powder",
            "WP_CORE_MANAGEMENT_HOST": "core.invalid",
            "WP_UE_MANAGEMENT_HOST": "ue.invalid",
        }
    )
    p = _run([sys.executable, "-c", RESTART_HARNESS], env=env, timeout=30)
    _require(p.returncode == 0, f"restart harness rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    row = json.loads(p.stdout.strip().splitlines()[-1])
    _require(row["transition_survived"] is True, row)
    _require(row["old_gateway_pid"] != row["new_gateway_pid"], row)
    return row


FAKE_SSH = r"""#!/usr/bin/env python3
import os
import sys

host = sys.argv[-2] if len(sys.argv) >= 2 else ""
cmd = sys.argv[-1] if sys.argv else ""
fault = os.environ.get("H2_FAULT_POINT", "")

if "tmux has-session" in cmd:
    raise SystemExit(1)

if fault == "UE_CLEANUP" and "NAMES=' srsue'" in cmd:
    raise SystemExit(91)
if fault == "CORE_CLEANUP" and "NAMES=' srsenb srsepc'" in cmd:
    raise SystemExit(92)
if fault == "CORE_START" and "core.invalid" in host and "/local/repository/bin/start.sh" in cmd:
    raise SystemExit(93)
if fault == "CORE_STABLE" and "core.invalid" in host and "stable=0" in cmd:
    raise SystemExit(94)
if fault == "UE_START" and "ue.invalid" in host and "/local/repository/bin/start.sh" in cmd:
    raise SystemExit(95)
if fault == "UE_READY" and "ue.invalid" in host and "deadline=" in cmd and "pgrep -x srsue" in cmd:
    raise SystemExit(96)

raise SystemExit(0)
"""


PROBE_HARNESS = r"""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace

root = Path(os.environ["WP_REPO_ROOT"])
entry = root / "scripts/wp2_p7b_c_node_h2.py"
spec = importlib.util.spec_from_file_location("h2_probe_adversarial_entry", entry)
if spec is None or spec.loader is None:
    raise RuntimeError("H2_IMPORT_FAIL")
h2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h2)
base = h2.base
clock = {"n": 0}
def tick():
    clock["n"] += 1
    return clock["n"]
base.utc_now = lambda: f"2026-08-28T00:01:{tick():02d}+00:00"
base.mono = lambda: tick()

with tempfile.TemporaryDirectory() as td:
    cell = Path(td) / "cell"
    cell.mkdir(parents=True)
    calls = {"n": 0}
    def fake_run(cmd, *, env=None, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            restore_out = Path(env["WP_RESTORE_OUT"])
            restore_out.write_text(
                "CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS\n"
                "CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION=PASS\n"
                "DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO\n"
                "RESTORE_START_EPOCH=123\n",
                encoding="utf-8",
            )
            frontier = Path(env["WP_RESTORE_FRONTIER"])
            frontier.write_text('{"phase":"UE_PROCESS_READY","utc":"x","monotonic":"1","status":"PASS"}\n', encoding="utf-8")
            return SimpleNamespace(returncode=0, stdout="safe restore synthetic pass")
        return SimpleNamespace(returncode=37, stdout="synthetic probe failure")
    base.run = fake_run
    base.CORE_HOST = "core.invalid"
    base.UE_HOST = "ue.invalid"
    base.REMOTE_USER = "offline"
    h2.install_h2_safe_restore({
        "controller_pid": 4242,
        "controller_session": "NONE",
        "controller_host_role": "UE",
    })
    try:
        base.restore_service(cell, Path("/tmp/ca"))
        raise RuntimeError("PROBE_FAILURE_WAS_NOT_RAISED")
    except RuntimeError as exc:
        if "SERVICE_READY_PROBE_FAIL:rc=37" not in str(exc):
            raise
    rows = [json.loads(x) for x in (cell / "restoration_frontier.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    if rows[-1]["phase"] != "SERVICE_READY_PROBE_END" or rows[-1]["status"] != "FAIL":
        raise RuntimeError(f"BAD_LAST_PROBE_FRONTIER:{rows[-1]}")
    print(json.dumps({"last_phase": rows[-1]["phase"], "last_status": rows[-1]["status"]}))
"""


def _frontier_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def case_each_restore_phase_failure_preserves_frontier() -> dict:
    expected = {
        "UE_CLEANUP": "UE_CLEANUP_BEGIN",
        "CORE_CLEANUP": "CORE_CLEANUP_BEGIN",
        "CORE_START": "CORE_START_BEGIN",
        "CORE_STABLE": "CORE_START_END",
        "UE_START": "UE_START_BEGIN",
        "UE_READY": "UE_START_END",
    }
    observed: dict[str, str] = {}
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        fake_bin = td_path / "bin"
        fake_bin.mkdir()
        fake_ssh = fake_bin / "ssh"
        fake_ssh.write_text(FAKE_SSH, encoding="utf-8")
        fake_ssh.chmod(0o755)
        for fault, last_expected in expected.items():
            frontier = td_path / f"{fault}.jsonl"
            out = td_path / f"{fault}.txt"
            env = os.environ.copy()
            env.update(
                {
                    "PATH": str(fake_bin) + os.pathsep + env.get("PATH", ""),
                    "H2_FAULT_POINT": fault,
                    "WP_CORE_HOST": "core.invalid",
                    "WP_UE_HOST": "ue.invalid",
                    "WP_REMOTE_USER": "offline",
                    "WP_CONTROLLER_PID": "4242",
                    "WP_CONTROLLER_SESSION": "NONE",
                    "WP_CONTROLLER_HOST_ROLE": "UE",
                    "WP_RESTORE_OUT": str(out),
                    "WP_RESTORE_FRONTIER": str(frontier),
                }
            )
            p = _run(["bash", str(SAFE_RESTORE)], env=env, timeout=20)
            _require(p.returncode != 0, f"{fault} unexpectedly passed")
            rows = _frontier_rows(frontier)
            _require(rows, f"{fault} wrote no frontier")
            last = rows[-1]["phase"]
            _require(last == last_expected, f"{fault}: last={last} expected={last_expected}; rows={rows}")
            observed[fault] = last

    env = os.environ.copy()
    env.update(
        {
            "WP_REPO_ROOT": str(ROOT),
            "WP_RUN_ID": "h2-probe-adversarial",
            "WP_EXPERIMENT_ID": "offline-no-powder",
            "WP_CORE_MANAGEMENT_HOST": "core.invalid",
            "WP_UE_MANAGEMENT_HOST": "ue.invalid",
        }
    )
    p = _run([sys.executable, "-c", PROBE_HARNESS], env=env, timeout=30)
    _require(p.returncode == 0, f"probe harness rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    probe = json.loads(p.stdout.strip().splitlines()[-1])
    _require(probe == {"last_phase": "SERVICE_READY_PROBE_END", "last_status": "FAIL"}, probe)
    observed["SERVICE_READY_PROBE"] = probe["last_phase"]
    return observed


def case_frozen_science_unchanged() -> dict:
    base = _load_json(BASE_CONTRACT)
    delta = _load_json(DELTA)
    frozen = delta["frozen_scientific_controls"]
    expected = {
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
    for key, value in expected.items():
        _require(frozen[key] == value, f"science drift {key}: {frozen[key]!r} != {value!r}")
    _require(frozen["clocks_distinct"] == ["t_rf_restore", "t_service_ready", "t_app_complete"], frozen["clocks_distinct"])
    return {"matched_fields": len(expected) + 1, "scientific_change": delta["scientific_change"]}


def case_automatic_retry_not_introduced() -> dict:
    base = _load_json(BASE_CONTRACT)
    delta = _load_json(DELTA)
    authority = delta["authority"]
    for key in (
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
    ):
        _require(authority[key] is False, f"authority drift {key}=true")
    _require(base["authority"]["automatic_retry"] is False, "base contract auto retry drift")
    combined = H2_ENTRY.read_text(encoding="utf-8") + SAFE_RESTORE.read_text(encoding="utf-8")
    for forbidden in ("AUTOMATIC_RETRY=YES", "scored_runs_authorized=true", "portal-cli experiment create", "portal-cli experiment terminate"):
        _require(forbidden not in combined, f"forbidden live/retry surface present: {forbidden}")
    return {"automatic_retry": False, "live_authority": False}


CASES = {
    "CONTROLLER_IN_TMUX_UE_REJECTED_BEFORE_RF": case_controller_in_tmux_ue_rejected,
    "ALLOWED_CONTROLLER_SURVIVES_SERVICE_CLEANUP": case_allowed_controller_survives_cleanup,
    "SERVICE_OWNERSHIP_SELECTION_CANNOT_MATCH_CONTROLLER_PID_OR_SESSION": case_service_ownership_collision_blocks,
    "RESTART_TRANSITION_SURVIVES_SYNTHETIC_FAILURE_AFTER_GATEWAY_RESTART": case_restart_transition_survives,
    "EACH_RESTORE_PHASE_FAILURE_PRESERVES_LAST_FRONTIER": case_each_restore_phase_failure_preserves_frontier,
    "FROZEN_SCIENTIFIC_CONTROLS_UNCHANGED": case_frozen_science_unchanged,
    "AUTOMATIC_RETRY_NOT_INTRODUCED": case_automatic_retry_not_introduced,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    delta = _load_json(DELTA)
    required = tuple(delta["controls"]["A7"]["required_cases"])
    _require(required == REQUIRED_CASES, f"A7 required case drift: {required!r}")
    _require(delta["controls"]["A7"]["live_powder_contact_for_qa_prohibited"] is True, "A7 live POWDER QA prohibition drift")

    results: dict[str, dict] = {}
    gate = "PASS"
    for name in REQUIRED_CASES:
        try:
            detail = CASES[name]()
            results[name] = {"gate": "PASS", "detail": detail}
            print(f"{name}=PASS")
        except Exception as exc:
            gate = "BLOCKED"
            results[name] = {"gate": "BLOCKED", "failure": f"{type(exc).__name__}:{exc}"}
            print(f"{name}=BLOCKED:{type(exc).__name__}:{exc}")

    report = {
        "schema_version": "wp2-p7b-h2-adversarial-qa-v1",
        "gate": gate,
        "required_cases": list(REQUIRED_CASES),
        "cases": results,
        "powder_contact": False,
        "network_contact": False,
        "live_service_mutation": False,
        "rf_mutation": False,
        "retry": False,
        "scored": False,
        "teardown": False,
        "terminal_gate": "H2_4_ADVERSARIAL_QA=PASS" if gate == "PASS" else "H2_4_ADVERSARIAL_QA=BLOCKED",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"H2_4_ADVERSARIAL_QA={gate}")
    return 0 if gate == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
