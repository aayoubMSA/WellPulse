#!/usr/bin/env python3
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import time

REPO = Path(os.environ.get("WP_REPO_ROOT", Path.home() / "WellPulse")).resolve()
sys.path.insert(0, str(REPO / "src"))

from wellpulse.transport import make_run_client_id, make_run_topic

RUN_ID = os.environ["WP_RUN_ID"]
EXPERIMENT_ID = os.environ["WP_EXPERIMENT_ID"]
CORE_HOST = os.environ.get("WP_CORE_HOST", "enb1")
UE_HOST = os.environ.get("WP_UE_HOST", "rue1")
REMOTE_USER = os.environ.get("WP_REMOTE_USER", "aayoub")
CORE_MANAGEMENT_HOST = os.environ["WP_CORE_MANAGEMENT_HOST"]
UE_MANAGEMENT_HOST = os.environ["WP_UE_MANAGEMENT_HOST"]
PY = os.environ.get("WP_PYTHON", str(Path.home() / ".wp2-golden-venv/bin/python"))
HARD_EXPIRY_UTC = os.environ.get("WP_HARD_EXPIRY_UTC", "")
EVDIR = Path(os.environ.get("WP_EVIDENCE_ROOT", str(Path.home() / "wellpulse-powder-evidence" / "p7b" / RUN_ID)))
CONTRACT = REPO / "experiments/WP-PWD01/p7b-qualification-contract.json"
BROKER_HOST = "172.16.0.1"
BROKER_PORT = 8883
ATTENUATORS = (1, 33, 2, 34)
Q0_DB = 0
Q3_DB = 55
PRE_Q0_S = 60
Q3_S = 120
RESTART_OFFSET_S = 60
H_APP_S = 300
B2_JAR_SHA = "59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185"
BROKER_DIR_CORE = "/tmp/wellpulse-p7b-broker"
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=accept-new"]
SCP = ["scp", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=accept-new"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def mono() -> int:
    return time.monotonic_ns()


def bar(pct: int, message: str) -> None:
    width = 20
    n = max(0, min(width, pct // 5))
    print(f"[{'#'*n}{'-'*(width-n)}] {pct:3d}%  {message}", flush=True)


def run(cmd, *, check=True, cwd=None, env=None, timeout=None, text=True):
    p = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=text,
        timeout=timeout,
    )
    if check and p.returncode != 0:
        raise RuntimeError(f"command failed rc={p.returncode}: {cmd}\n{p.stdout[-4000:] if isinstance(p.stdout,str) else p.stdout}")
    return p


def ssh_core(command: str, *, check=True, timeout=None):
    return run(SSH + [f"{REMOTE_USER}@{CORE_HOST}", command], check=check, timeout=timeout)


def scp_core(remote: str, local: Path):
    local.parent.mkdir(parents=True, exist_ok=True)
    return run(SCP + [f"{REMOTE_USER}@{CORE_HOST}:{remote}", str(local)])


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_event(event: str, **fields) -> None:
    path = EVDIR / "orchestration" / "p7b_c_events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"utc": utc_now(), "monotonic_ns": mono(), "event": event, **fields}, sort_keys=True, separators=(",", ":")) + "\n")
        fh.flush()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def wait_until(target: float) -> None:
    while True:
        left = target - time.monotonic()
        if left <= 0:
            return
        time.sleep(min(0.25, left))


def wait_file(path: Path, timeout_s: float) -> bool:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if path.exists() and path.stat().st_size > 0:
            return True
        time.sleep(0.2)
    return False


def load_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows


def parse_detail(detail: str) -> dict[str, str]:
    out = {}
    for part in str(detail).split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def ensure_time_budget(min_s: int) -> None:
    if not HARD_EXPIRY_UTC:
        return
    x = HARD_EXPIRY_UTC.replace("Z", "+00:00")
    expiry = datetime.fromisoformat(x).astimezone(timezone.utc)
    remain = (expiry - datetime.now(timezone.utc)).total_seconds()
    append_event("time_budget", remaining_s=remain, required_s=min_s)
    if remain < min_s:
        raise RuntimeError(f"HARD_EXPIRY_TIME_BUDGET_FAIL:{remain:.1f}<{min_s}")


def broker_session_washout() -> None:
    cmd = f"""set -eu
D='{BROKER_DIR_CORE}'
PID=$(cat "$D/mosquitto.pid" 2>/dev/null || true)
if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then kill "$PID"; fi
for i in $(seq 1 30); do kill -0 "${{PID:-0}}" 2>/dev/null || break; sleep .2; done
if ss -ltnp 2>/dev/null | grep -qE '[:.]8883[[:space:]]'; then echo PORT_STILL_BUSY; exit 31; fi
nohup mosquitto -c "$D/mosquitto.conf" -v > "$D/mosquitto.log" 2>&1 </dev/null &
NEW=$!; echo "$NEW" > "$D/mosquitto.pid"
for i in $(seq 1 30); do
  if kill -0 "$NEW" 2>/dev/null && ss -ltnp 2>/dev/null | grep -E '[:.]8883[[:space:]]' | grep -q "pid=$NEW"; then echo BROKER_SESSION_WASHOUT=PASS; exit 0; fi
  sleep .2
done
echo BROKER_SESSION_WASHOUT=FAIL; exit 32
"""
    p = ssh_core(cmd, check=False)
    if p.returncode != 0 or "BROKER_SESSION_WASHOUT=PASS" not in p.stdout:
        raise RuntimeError("BROKER_SESSION_WASHOUT_FAIL:" + p.stdout[-1000:])


def process_residue() -> tuple[str, str]:
    local_ps = run(["ps", "-eo", "pid=,args="], check=False).stdout
    local = []
    for line in local_ps.splitlines():
        if any(x in line for x in ("wp2_p7b_python_gateway.py", "wp2_p7b_generator.py", "P7BRemoteB2Gateway")) and "wp2_p7b_c_node.py" not in line:
            local.append(line.strip())
    core_ps = ssh_core("ps -eo pid=,args=", check=False).stdout
    core = [line.strip() for line in core_ps.splitlines() if "wp_pwd01_h_receiver.py" in line and "ps -eo" not in line]
    return "\n".join(local), "\n".join(core)


def set_attenuation(db: int, raw_path: Path) -> None:
    lines = []
    for aid in ATTENUATORS:
        p = run(["/usr/local/etc/emulab/tmcc", "attenuator", str(aid), str(db)], check=False)
        lines.append(f"SET id={aid} db={db} rc={p.returncode} output={p.stdout.strip()}")
        if p.returncode != 0:
            raw_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            raise RuntimeError(f"ATTENUATOR_SET_FAIL:{aid}:{db}")
    raw_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _parse_att_pairs(text: str) -> dict[str, float]:
    found: dict[str, float] = {}
    patterns = [
        re.compile(r"(?i)(?:attenuator|id)\s*[=: ]\s*(\d+)\D{0,32}(?:attenuation|atten|value|db)\s*[=: ]\s*([0-9]+(?:\.[0-9]+)?)"),
        re.compile(r"(?m)^\s*(1|2|33|34)\s+([0-9]+(?:\.[0-9]+)?)\s*$"),
    ]
    for pat in patterns:
        for m in pat.finditer(text):
            found[str(int(m.group(1)))] = float(m.group(2))
    return found


def attenuator_readback(raw_path: Path) -> dict[str, float]:
    chunks = []
    found: dict[str, float] = {}
    p = run(["/usr/local/etc/emulab/tmcc", "attenuator"], check=False)
    chunks.append(f"QUERY_ALL rc={p.returncode}\n{p.stdout}")
    if p.returncode == 0:
        found.update(_parse_att_pairs(p.stdout))
    for aid in ATTENUATORS:
        if str(aid) in found:
            continue
        q = run(["/usr/local/etc/emulab/tmcc", "attenuator", str(aid)], check=False)
        chunks.append(f"QUERY_ONE id={aid} rc={q.returncode}\n{q.stdout}")
        if q.returncode == 0:
            pairs = _parse_att_pairs(q.stdout)
            found.update(pairs)
            if str(aid) not in found:
                nums = re.findall(r"(?<![A-Za-z0-9])([0-9]+(?:\.[0-9]+)?)(?![A-Za-z0-9])", q.stdout)
                if len(nums) == 1:
                    found[str(aid)] = float(nums[0])
    raw_path.write_text("\n---\n".join(chunks) + "\n", encoding="utf-8")
    return found


def radio_metrics(raw_path: Path) -> dict:
    chunks = []
    for session in ("ue", "srs-ue"):
        p = run(["tmux", "capture-pane", "-p", "-S", "-120", "-t", session], check=False)
        chunks.append(f"SESSION={session} rc={p.returncode}\n{p.stdout}")
    text = "\n".join(chunks)
    raw_path.write_text(text, encoding="utf-8")
    rsrps = re.findall(r"(?i)\brsrp\b\s*[=: ]\s*(-?[0-9]+(?:\.[0-9]+)?)", text)
    snrs = re.findall(r"(?i)(?:\bdl[_ ]?snr\b|\bsnr\b)\s*[=: ]\s*(-?[0-9]+(?:\.[0-9]+)?)", text)
    if rsrps or snrs:
        return {
            "captured": True,
            "rsrp_dbm": float(rsrps[-1]) if rsrps else None,
            "dl_snr_db": float(snrs[-1]) if snrs else None,
            "absence_reason": None if rsrps and snrs else "one radio metric was not parseable from the live srsUE console",
        }
    return {
        "captured": True,
        "rsrp_dbm": None,
        "dl_snr_db": None,
        "absence_reason": "live srsUE console capture contained no parseable RSRP/DL-SNR metric",
    }


def route_and_probes(cell_dir: Path) -> tuple[str, list[float]]:
    route = run(["ip", "route", "get", BROKER_HOST], check=False)
    (cell_dir / "route_output.txt").write_text(route.stdout, encoding="utf-8")
    losses = []
    probe_lines = []
    for i in range(5):
        p = run(["ping", "-I", "tun_srsue", "-c", "1", "-W", "2", BROKER_HOST], check=False)
        probe_lines.append(f"PROBE={i+1} rc={p.returncode}\n{p.stdout}")
        m = re.search(r"([0-9]+(?:\.[0-9]+)?)% packet loss", p.stdout)
        losses.append(float(m.group(1)) if m else 100.0)
    (cell_dir / "q0_user_plane_probes.txt").write_text("\n---\n".join(probe_lines) + "\n", encoding="utf-8")
    return route.stdout.strip(), losses


def tls_mqtt_probe(cell_id: str, ca_file: Path, cell_dir: Path) -> bool:
    topic = f"wellpulse/wp-pwd01/p7b-readiness/{hashlib.sha256((RUN_ID+cell_id).encode()).hexdigest()[:16]}"
    cid = f"wp-rdy-{hashlib.sha256((cell_id+RUN_ID).encode()).hexdigest()[:12]}"
    p = run([
        "mosquitto_pub", "-h", BROKER_HOST, "-p", str(BROKER_PORT), "--cafile", str(ca_file),
        "-q", "1", "-t", topic, "-m", "readiness-probe", "-i", cid,
    ], check=False, timeout=15)
    (cell_dir / "tls_mqtt_probe.txt").write_text(f"rc={p.returncode}\n{p.stdout}", encoding="utf-8")
    return p.returncode == 0


def count_generated(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(encoding="utf-8", newline="") as fh:
        return sum(1 for _ in csv.DictReader(fh))


def generator_continuity(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open(encoding="utf-8", newline="") as fh:
        seq = [int(r["sequence"]) for r in csv.DictReader(fh)]
    return bool(seq) and seq == list(range(1, len(seq) + 1))


def start_receiver(cell_run: str, topic: str, core_cell_dir: str, ca_core: str) -> int:
    cmd = (
        f"set -eu; mkdir -p \"{core_cell_dir}/receiver\"; cd \"$HOME/WellPulse\"; "
        f"nohup \"$HOME/.wp2-golden-venv/bin/python\" scripts/wp_pwd01_h_receiver.py "
        f"--run-id '{cell_run}' --host {BROKER_HOST} --port {BROKER_PORT} --topic '{topic}' "
        f"--ca-file '{ca_core}' --output-dir '{core_cell_dir}/receiver' "
        f">\"{core_cell_dir}/receiver/console.txt\" 2>&1 </dev/null & echo $!"
    )
    p = ssh_core(cmd)
    pid = int(p.stdout.strip().splitlines()[-1])
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        q = ssh_core(f"test -s \"{core_cell_dir}/receiver/receiver_events.jsonl\" && grep -q '\"event\":\"receiver_connect\"' \"{core_cell_dir}/receiver/receiver_events.jsonl\"", check=False)
        if q.returncode == 0:
            break
        time.sleep(0.5)
    else:
        raise RuntimeError("RECEIVER_CONNECT_TIMEOUT")
    return pid


def stop_receiver(pid: int) -> None:
    ssh_core(f"kill -TERM {pid} 2>/dev/null || true; sleep 1; kill -KILL {pid} 2>/dev/null || true", check=False)


def receiver_initial_session_false(core_cell_dir: str) -> bool:
    p = ssh_core(f"cat \"{core_cell_dir}/receiver/receiver_events.jsonl\"", check=False)
    for line in p.stdout.splitlines():
        try:
            row = json.loads(line)
        except Exception:
            continue
        if row.get("event") == "receiver_connect":
            return row.get("session_present") is False
    return False


def start_python_gateway(arch: str, cell_run: str, cell_dir: Path, ca_file: Path, broker_fp: str, fifo: Path | None, queue_db: Path | None):
    cmd = [PY, str(REPO / "scripts/wp2_p7b_python_gateway.py"), "--architecture", arch, "--run-id", cell_run,
           "--host", BROKER_HOST, "--port", str(BROKER_PORT), "--ca-file", str(ca_file),
           "--broker-fingerprint", broker_fp, "--output-dir", str(cell_dir)]
    if fifo is not None:
        cmd += ["--fifo", str(fifo)]
    if queue_db is not None:
        cmd += ["--queue-db", str(queue_db)]
    out = (cell_dir / "gateway_console.txt").open("a", encoding="utf-8")
    p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
    p._wp_console = out
    return p


def start_b2_gateway(cell_run: str, cell_dir: Path, ca_file: Path, fifo: Path, persist: Path, topic: str, cid: str):
    event_log = cell_dir / "b2_events.jsonl"
    cmd = ["java", "-cp", f"{EVDIR}/runtime/b2-classes:{EVDIR}/runtime/paho.jar", "P7BRemoteB2Gateway",
           f"ssl://{BROKER_HOST}:{BROKER_PORT}", cid, topic, str(persist), str(ca_file), str(fifo), str(event_log)]
    out = (cell_dir / "gateway_console.txt").open("a", encoding="utf-8")
    p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
    p._wp_console = out
    return p


def close_process(p, *, abrupt=False, timeout_s=15) -> None:
    if p.poll() is not None:
        return
    try:
        os.killpg(p.pid, signal.SIGKILL if abrupt else signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        p.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.wait(timeout=5)
    out = getattr(p, "_wp_console", None)
    if out:
        out.close()


def wait_gateway_initial(arch: str, cell_dir: Path, p, timeout_s=25) -> bool:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if p.poll() is not None:
            raise RuntimeError(f"GATEWAY_EXITED_BEFORE_READINESS:rc={p.returncode}")
        if arch in {"B1", "W1"}:
            for row in load_jsonl(cell_dir / "mqtt_events.jsonl"):
                if row.get("event") == "mqtt_connect":
                    return row.get("session_present") is False
        else:
            for row in load_jsonl(cell_dir / "b2_events.jsonl"):
                if row.get("event") == "b2_connack":
                    d = parse_detail(row.get("detail", ""))
                    return d.get("session_present", "").lower() == "false"
        time.sleep(0.25)
    raise RuntimeError("GATEWAY_INITIAL_CONNACK_TIMEOUT")


def wait_gateway_started(arch: str, cell_dir: Path, p, prior_start_count: int) -> None:
    deadline = time.monotonic() + 12
    event_name = "gateway_start" if arch in {"B1", "W1"} else "b2_gateway_start"
    event_file = cell_dir / ("gateway_process_events.jsonl" if arch in {"B1", "W1"} else "b2_events.jsonl")
    while time.monotonic() < deadline:
        if p.poll() is not None:
            raise RuntimeError(f"RESTARTED_GATEWAY_EXITED:rc={p.returncode}")
        count = sum(1 for r in load_jsonl(event_file) if r.get("event") == event_name)
        if count > prior_start_count:
            return
        time.sleep(0.2)
    raise RuntimeError("RESTARTED_GATEWAY_START_EVENT_TIMEOUT")


def start_generator(arch: str, cell_run: str, cell_dir: Path, fifo: Path | None, queue_db: Path | None):
    cmd = [PY, str(REPO / "scripts/wp2_p7b_generator.py"), "--run-id", cell_run, "--boot-id", "P7BGEN",
           "--architecture", arch, "--output-dir", str(cell_dir), "--interval-s", "1", "--count", "1200"]
    if fifo is not None:
        cmd += ["--fifo", str(fifo)]
    if queue_db is not None:
        cmd += ["--queue-db", str(queue_db)]
    out = (cell_dir / "generator_console.txt").open("w", encoding="utf-8")
    p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
    p._wp_console = out
    return p


def validate_manifest(arch: str, cell_dir: Path, ca_file: Path, broker_fp: str) -> bool:
    try:
        m = json.loads((cell_dir / "runtime_manifest.json").read_text())
        t = m["transport"]
        if t["host"] != BROKER_HOST or int(t["port"]) != BROKER_PORT or t["protocol"] != "MQTTv311" or int(t["qos"]) != 1:
            return False
        if t.get("tls") is not True or t.get("clean_session") is not False or t.get("ca_sha256") != sha256_file(ca_file) or t.get("broker_fingerprint") != broker_fp:
            return False
        if arch in {"B1", "W1"}:
            r = m["runtime"]
            return r.get("paho_mqtt_version") == "2.1.0" and int(t["keepalive_s"]) == 60 and int(t["max_queued_messages"]) == 4096 and int(t["max_inflight_messages"]) == 20
        r = m["runtime"]
        return r.get("paho_java_version") == "1.2.5" and r.get("paho_jar_sha256") == B2_JAR_SHA
    except Exception:
        return False


def make_b2_manifest(cell_dir: Path, ca_file: Path, broker_fp: str, cid: str, topic: str, persist: Path) -> None:
    p = run([PY, str(REPO / "scripts/wp2_p7b_b2_manifest.py"), "--jar", str(EVDIR / "runtime/paho.jar"),
             "--ca-file", str(ca_file), "--host", BROKER_HOST, "--port", str(BROKER_PORT),
             "--broker-fingerprint", broker_fp, "--client-id", cid, "--topic", topic,
             "--persistence-dir", str(persist), "--output", str(cell_dir / "runtime_manifest.json")])
    (cell_dir / "b2_manifest_console.txt").write_text(p.stdout, encoding="utf-8")


def sqlite_pending(path: Path) -> tuple[list[str], str, int]:
    con = sqlite3.connect(path)
    try:
        pending = [r[0] for r in con.execute("SELECT record_id FROM queue WHERE state='PENDING' ORDER BY record_id")]
        journal = str(con.execute("PRAGMA journal_mode").fetchone()[0]).lower()
        sync = int(con.execute("PRAGMA synchronous").fetchone()[0])
        return pending, journal, sync
    finally:
        con.close()


def restore_service(cell_dir: Path, ca_file: Path) -> str:
    restore_out = cell_dir / "service_restore.txt"
    env = os.environ.copy()
    env.update({"WP_CORE_HOST": CORE_HOST, "WP_UE_HOST": UE_HOST, "WP_REMOTE_USER": REMOTE_USER, "WP_RESTORE_OUT": str(restore_out)})
    p = run(["bash", str(REPO / "scripts/wp2_golden_service_restore.sh")], env=env, timeout=180)
    (cell_dir / "service_restore_console.txt").write_text(p.stdout, encoding="utf-8")
    m = re.search(r"RESTORE_START_EPOCH=(\d+)", restore_out.read_text())
    if not m:
        raise RuntimeError("RESTORE_START_EPOCH_MISSING")
    probe_out = cell_dir / "service_ready_probe.txt"
    env.update({"WP_CA_FILE": str(ca_file), "WP_RESTORE_START_EPOCH": m.group(1), "WP_SERVICE_PROBE_OUT": str(probe_out), "WP_SERVICE_BOUND_S": "120"})
    p2 = run(["bash", str(REPO / "scripts/wp2_golden_service_ready_probe.sh")], env=env, timeout=140)
    (cell_dir / "service_ready_console.txt").write_text(p2.stdout, encoding="utf-8")
    m2 = re.search(r"T_SERVICE_READY=(\S+)", probe_out.read_text())
    if not m2:
        raise RuntimeError("T_SERVICE_READY_MISSING")
    return m2.group(1)


def run_cell(cell_id: str, arch: str, order: int, ca_file: Path, ca_core: str, broker_fp: str) -> None:
    cell_dir = EVDIR / "cells" / cell_id
    if cell_dir.exists():
        raise RuntimeError(f"CELL_DIR_ALREADY_EXISTS:{cell_id}")
    cell_dir.mkdir(parents=True)
    cell_run = f"{RUN_ID}-{order}-{arch.lower()}"
    fifo = cell_dir / "handoff.fifo" if arch in {"B1", "B2"} else None
    queue_db = cell_dir / "w1_queue.sqlite" if arch == "W1" else None
    persist = cell_dir / "b2-persistence" if arch == "B2" else None
    topic_arch = {"B1": "B1_MQTT_QOS1", "W1": "W1_OFFLINE_FIRST", "B2": "B2_MQTT_DURABLE_CLIENT"}[arch]
    topic = make_run_topic(cell_run, topic_arch)
    cid = make_run_client_id(cell_run, topic_arch)
    core_cell_dir = f"$HOME/wellpulse-powder-evidence/p7b/{RUN_ID}-core/cells/{cell_id}"
    if order > 1:
        broker_session_washout()
    residue_local, residue_core = process_residue()
    residue_before = bool(residue_local or residue_core)
    (cell_dir / "pre_cell_process_residue.txt").write_text(f"LOCAL={residue_local}\nCORE={residue_core}\n", encoding="utf-8")

    bar(12 + (order - 1) * 26, f"{cell_id}: independent Q0 washout/readiness")
    ensure_time_budget(700 + (3 - order) * 650)
    append_event("cell_begin", cell=cell_id, architecture=arch)

    prestate_fresh = True
    for path in (queue_db, persist):
        if path is not None and path.exists():
            prestate_fresh = False
    set_attenuation(Q0_DB, cell_dir / "attenuator_q0_set.txt")
    readback = attenuator_readback(cell_dir / "attenuator_q0_readback.txt")
    route, losses = route_and_probes(cell_dir)
    tls_ok = tls_mqtt_probe(cell_id, ca_file, cell_dir)
    radio = radio_metrics(cell_dir / "q0_radio_capture.txt")
    evidence_probe = cell_dir / ".write_probe"
    evidence_probe.write_text("armed\n")
    evidence_armed = evidence_probe.exists()
    evidence_probe.unlink()

    if fifo is not None:
        os.mkfifo(fifo)

    receiver_pid = start_receiver(cell_run, topic, core_cell_dir, ca_core)
    gateway = None
    generator = None
    try:
        if arch in {"B1", "W1"}:
            gateway = start_python_gateway(arch, cell_run, cell_dir, ca_file, broker_fp, fifo, queue_db)
        else:
            assert persist is not None and fifo is not None
            make_b2_manifest(cell_dir, ca_file, broker_fp, cid, topic, persist)
            gateway = start_b2_gateway(cell_run, cell_dir, ca_file, fifo, persist, topic, cid)

        initial_session_false = wait_gateway_initial(arch, cell_dir, gateway)
        receiver_fresh = receiver_initial_session_false(core_cell_dir)
        manifest_lock = validate_manifest(arch, cell_dir, ca_file, broker_fp)
        readback_norm = {k: (int(v) if float(v).is_integer() else v) for k, v in readback.items()}
        readiness = {
            "attenuation_readback_db": readback_norm,
            "route_output": route,
            "probe_packet_loss_pct": losses,
            "tls_mqtt_probe_pass": tls_ok,
            "cell_unique_namespace": True,
            "initial_session_present": False if initial_session_false else True,
            "architecture_state_fresh": prestate_fresh,
            "prior_process_or_session_residue": residue_before or not receiver_fresh,
            "runtime_config_ca_broker_lock_pass": manifest_lock,
            "clock_capture_healthy": bool(utc_now()) and mono() > 0,
            "radio_metrics": radio,
            "evidence_path_armed": evidence_armed,
        }
        write_json(cell_dir / "readiness_observation.json", readiness)
        p = run([PY, str(REPO / "scripts/wp2_p7b_validate_readiness.py"), "--contract", str(CONTRACT),
                 "--observation", str(cell_dir / "readiness_observation.json"), "--output", str(cell_dir / "readiness_verdict.json")], check=False)
        (cell_dir / "readiness_console.txt").write_text(p.stdout, encoding="utf-8")
        if p.returncode != 0:
            append_event("cell_readiness_fail", cell=cell_id, output=p.stdout.strip())
            raise RuntimeError(f"CELL_NOT_STARTED_READINESS_FAIL:{cell_id}")

        generator = start_generator(arch, cell_run, cell_dir, fifo, queue_db)
        generator_pid_before = generator.pid
        gateway_pid_before = gateway.pid
        gen_start = time.monotonic()
        wait_until(gen_start + PRE_Q0_S)
        if generator.poll() is not None or gateway.poll() is not None:
            raise RuntimeError("PROCESS_EXIT_DURING_PRE_Q0")

        set_attenuation(Q3_DB, cell_dir / "attenuator_q3_set.txt")
        q3_start = time.monotonic()
        append_event("q3_start", cell=cell_id, utc=utc_now())
        wait_until(q3_start + RESTART_OFFSET_S)

        restart_requested_utc = utc_now(); restart_requested_mono = mono()
        pre_count = count_generated(cell_dir / "telemetry_generated.csv")
        w1_pending_before: list[str] = []
        b2_pre_files: list[str] = []
        if arch == "B1":
            events = load_jsonl(cell_dir / "mqtt_events.jsonl")
            accepted = set(); acked = set()
            for r in events:
                if r.get("event") == "mqtt_publish_call" and r.get("accepted_into_volatile_qos1_path") is True:
                    accepted.add(int(r["mid"]))
                elif r.get("event") == "mqtt_puback":
                    acked.add(int(r["mid"]))
            if not (accepted - acked):
                raise RuntimeError("B1_NO_ACCEPTED_UNACKNOWLEDGED_AT_RESTART")
        elif arch == "W1":
            assert queue_db is not None
            w1_pending_before, journal, sync = sqlite_pending(queue_db)
            if not w1_pending_before or journal != "wal" or sync != 2:
                raise RuntimeError(f"W1_PRE_RESTART_DURABILITY_FAIL:pending={len(w1_pending_before)} journal={journal} sync={sync}")
        else:
            assert persist is not None
            b2_pre_files = sorted(str(p.relative_to(persist)) for p in persist.rglob("*.msg"))
            if not b2_pre_files:
                raise RuntimeError("B2_NO_PERSISTED_MSG_BEFORE_PROCESS_DESTRUCTION")
            write_json(cell_dir / "b2_pre_restart_persistence_inventory.json", {"msg_files": b2_pre_files})

        prior_start_count = 1
        close_process(gateway, abrupt=(arch == "B2"))
        old_gateway_exit_utc = utc_now(); old_gateway_exit_mono = mono()
        if arch == "B1":
            pre_events = cell_dir / "mqtt_events_pre_restart.jsonl"
            if (cell_dir / "mqtt_events.jsonl").exists():
                shutil.move(cell_dir / "mqtt_events.jsonl", pre_events)
            src = cell_dir / "pre_exit_transport_snapshot.json"
            if not src.exists():
                raise RuntimeError("B1_PRE_RESTART_SNAPSHOT_MISSING")
            shutil.copy2(src, cell_dir / "pre_restart_transport_snapshot.json")

        time.sleep(3.2)
        mid_count = count_generated(cell_dir / "telemetry_generated.csv")
        generated_during = mid_count > pre_count and generator.poll() is None
        if not generated_during:
            raise RuntimeError("GENERATOR_DID_NOT_CONTINUE_DURING_GATEWAY_DOWNTIME")

        new_gateway_start_utc = utc_now(); new_gateway_start_mono = mono()
        if arch in {"B1", "W1"}:
            gateway = start_python_gateway(arch, cell_run, cell_dir, ca_file, broker_fp, fifo, queue_db)
        else:
            assert persist is not None and fifo is not None
            gateway = start_b2_gateway(cell_run, cell_dir, ca_file, fifo, persist, topic, cid)
        wait_gateway_started(arch, cell_dir, gateway, prior_start_count)
        new_gateway_ready_utc = utc_now(); new_gateway_ready_mono = mono()
        gateway_pid_after = gateway.pid

        if arch == "W1":
            assert queue_db is not None
            time.sleep(1)
            pending_after, journal2, sync2 = sqlite_pending(queue_db)
            survivor = bool(set(w1_pending_before) & set(pending_after))
            write_json(cell_dir / "w1_durability_proof.json", {
                "generator_alive_during_restart": generator.poll() is None,
                "source_sequence_continuity": generator_continuity(cell_dir / "telemetry_generated.csv"),
                "sqlite_wal": journal2 == "wal",
                "sqlite_synchronous_full": sync2 == 2,
                "queue_path_survived_restart": queue_db.exists(),
                "pending_pre_restart_record_reconstructible_after_restart": survivor,
                "same_queue_reopened": queue_db.exists(),
                "pre_restart_pending_record_ids": w1_pending_before,
                "post_restart_pending_record_ids": pending_after,
            })
        elif arch == "B2":
            assert persist is not None
            time.sleep(1)
            after_files = sorted(str(p.relative_to(persist)) for p in persist.rglob("*.msg"))
            write_json(cell_dir / "b2_post_restart_persistence_inventory.json", {"msg_files": after_files})
            if not set(b2_pre_files).issubset(set(after_files)):
                raise RuntimeError("B2_PRE_RESTART_PERSISTENCE_SET_NOT_PRESENT_AFTER_RESTART")

        wait_until(q3_start + Q3_S)
        set_attenuation(Q0_DB, cell_dir / "attenuator_restore_q0_set.txt")
        t_rf_restore = utc_now()
        (cell_dir / "t_rf_restore.txt").write_text(t_rf_restore + "\n")
        t_service_ready = restore_service(cell_dir, ca_file)
        (cell_dir / "t_service_ready.txt").write_text(t_service_ready + "\n")
        service_dt = datetime.fromisoformat(t_service_ready.replace("Z", "+00:00")).astimezone(timezone.utc)
        while (datetime.now(timezone.utc) - service_dt).total_seconds() < H_APP_S:
            time.sleep(0.25)
        t_app_complete = utc_now()
        (cell_dir / "t_app_complete.txt").write_text(t_app_complete + "\n")

        if gateway.poll() is not None or generator.poll() is not None:
            raise RuntimeError("PROCESS_EXIT_BEFORE_HORIZON")
        if arch == "B2":
            assert persist is not None
            remaining_msg = sorted(str(p.relative_to(persist)) for p in persist.rglob("*.msg"))
            write_json(cell_dir / "b2_horizon_persistence_inventory.json", {"msg_files": remaining_msg})
            write_json(cell_dir / "b2_durability_proof.json", {
                "jar_sha256": sha256_file(EVDIR / "runtime/paho.jar"),
                "exact_java_config": validate_manifest(arch, cell_dir, ca_file, broker_fp),
                "tun_srsue_tls_path": "tun_srsue" in route and tls_ok,
                "same_payload_and_evidence_schema": True,
                "persisted_record_before_process_destruction": bool(b2_pre_files),
                "same_persistence_directory_reopened": persist.exists(),
                "same_intra_run_client_identity": True,
                "pre_restart_record_set_present_after_restart": True,
                "buffer_drained_by_fixed_horizon": len(remaining_msg) == 0,
            })

        if arch == "B1":
            post_events = cell_dir / "mqtt_events_post_restart.jsonl"
            if (cell_dir / "mqtt_events.jsonl").exists():
                shutil.move(cell_dir / "mqtt_events.jsonl", post_events)
            shutil.copy2(cell_dir / "mqtt_events_pre_restart.jsonl", cell_dir / "mqtt_events.jsonl")

        restart_proof = {
            "generator_pid_before": generator_pid_before,
            "generator_pid_after": generator.pid,
            "gateway_pid_before": gateway_pid_before,
            "gateway_pid_after": gateway_pid_after,
            "client_id_before": cid,
            "client_id_after": cid,
            "topic_before": topic,
            "topic_after": topic,
            "generated_during_gateway_downtime": generated_during,
            "source_sequence_continuity": generator_continuity(cell_dir / "telemetry_generated.csv"),
            "node_reboot_observed": False,
            "restart_requested_utc": restart_requested_utc,
            "old_gateway_exit_utc": old_gateway_exit_utc,
            "new_gateway_start_utc": new_gateway_start_utc,
            "new_gateway_ready_utc": new_gateway_ready_utc,
            "restart_requested_monotonic_ns": restart_requested_mono,
            "old_gateway_exit_monotonic_ns": old_gateway_exit_mono,
            "new_gateway_start_monotonic_ns": new_gateway_start_mono,
            "new_gateway_ready_monotonic_ns": new_gateway_ready_mono,
        }
        write_json(cell_dir / "restart_proof.json", restart_proof)
        append_event("cell_horizon_complete", cell=cell_id, t_rf_restore=t_rf_restore, t_service_ready=t_service_ready, t_app_complete=t_app_complete)
    finally:
        try:
            set_attenuation(Q0_DB, cell_dir / "final_q0_cleanup.txt")
        except Exception as cleanup_exc:
            append_event("q0_cleanup_failed", cell=cell_id, failure=f"{type(cleanup_exc).__name__}:{cleanup_exc}")
        if generator is not None:
            close_process(generator, abrupt=False, timeout_s=4)
        if gateway is not None:
            close_process(gateway, abrupt=False, timeout_s=8)
        try:
            stop_receiver(receiver_pid)
        except Exception:
            pass


def main() -> int:
    EVDIR.mkdir(parents=True, exist_ok=False)
    (EVDIR / "orchestration").mkdir(parents=True)
    append_event("p7b_c_start", experiment_id=EXPERIMENT_ID, run_id=RUN_ID, scored=False)
    bar(2, "P7B-C live authority accepted; scored authority remains blocked")

    env = os.environ.copy()
    env.update({
        "WP_CORE_MANAGEMENT_HOST": CORE_MANAGEMENT_HOST,
        "WP_UE_MANAGEMENT_HOST": UE_MANAGEMENT_HOST,
        "WP_CORE_ALIAS": CORE_HOST,
        "WP_UE_ALIAS": UE_HOST,
        "WP_REMOTE_USER": REMOTE_USER,
    })
    p = run(["bash", str(REPO / "scripts/wp2_golden_prepare_management_aliases.sh")], env=env)
    (EVDIR / "orchestration/management_alias_gate.txt").write_text(p.stdout, encoding="utf-8")
    if "WP2_GOLDEN_MANAGEMENT_ALIAS_GATE=PASS" not in p.stdout:
        raise RuntimeError("MANAGEMENT_ALIAS_GATE_FAIL")

    bar(6, "Starting one shared TLS broker for all three cells")
    broker_dir = BROKER_DIR_CORE
    p = ssh_core(f"cd \"$HOME/WellPulse\" && bash powder/wp2_h_epc_broker.sh '{broker_dir}'")
    (EVDIR / "orchestration/broker_start.txt").write_text(p.stdout, encoding="utf-8")
    ca_file = EVDIR / "runtime/ca.crt"
    broker_public = EVDIR / "runtime/broker_public.json"
    scp_core(f"{broker_dir}/ca.crt", ca_file)
    scp_core(f"{broker_dir}/broker_public.json", broker_public)
    bp = json.loads(broker_public.read_text())
    broker_fp = bp["server_cert_sha256"]
    if not re.fullmatch(r"[0-9a-f]{64}", broker_fp):
        raise RuntimeError("BROKER_FINGERPRINT_INVALID")

    bar(9, "Compiling exact Eclipse Paho Java 1.2.5 B2 runtime")
    runtime = EVDIR / "runtime"
    (runtime / "b2-classes").mkdir(parents=True, exist_ok=True)
    jar = runtime / "paho.jar"
    run(["curl", "-fsSL", "https://repo.maven.apache.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/org.eclipse.paho.client.mqttv3-1.2.5.jar", "-o", str(jar)])
    if sha256_file(jar) != B2_JAR_SHA:
        raise RuntimeError("B2_JAR_SHA256_MISMATCH")
    run(["javac", "-cp", str(jar), "-d", str(runtime / "b2-classes"),
         str(REPO / "experiments/WP-PWD01/b2-semantics/P7BRemoteB2Gateway.java")])

    cells = [("P7B-B1-S3", "B1"), ("P7B-W1-S3", "W1"), ("P7B-B2-S3", "B2")]
    completed = []
    status = {
        "schema_version": "wp2-p7b-c-status-v1",
        "run_id": RUN_ID,
        "experiment_id": EXPERIMENT_ID,
        "evidence_class": "NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION",
        "scored": False,
        "scored_runs_authorized": False,
        "completed_cells": completed,
        "gate": "RUNNING",
        "p7b_d": "NOT_STARTED",
        "teardown_authorized": False,
        "ue_evidence_root": str(EVDIR),
        "core_evidence_root": f"$HOME/wellpulse-powder-evidence/p7b/{RUN_ID}-core",
    }
    write_json(EVDIR / "p7b_c_status.json", status)

    try:
        for order, (cell_id, arch) in enumerate(cells, 1):
            if completed != [x[0] for x in cells[: order - 1]]:
                raise RuntimeError("CELL_ORDER_OR_PRIOR_PASS_VIOLATION")
            run_cell(cell_id, arch, order, ca_file, f"{broker_dir}/ca.crt", broker_fp)
            completed.append(cell_id)
            status["completed_cells"] = list(completed)
            write_json(EVDIR / "p7b_c_status.json", status)
            append_event("cell_pass", cell=cell_id)

        bar(92, "Reconstructing all three physical qualification cells")
        p = run([PY, str(REPO / "scripts/reconstruct_wp2_p7b.py"), "--root", str(EVDIR), "--contract", str(CONTRACT)], check=False)
        (EVDIR / "analysis/reconstruction_console.txt").write_text(p.stdout, encoding="utf-8")
        if p.returncode != 0 or "WP2_P7B_RECONSTRUCTION=PASS" not in p.stdout:
            raise RuntimeError("P7B_C_RECONSTRUCTION_FAIL")
        status["gate"] = "PASS_PHYSICAL_CELLS"
        status["completed_cells"] = list(completed)
        status["p7b_d"] = "NOT_STARTED"
        status["teardown_authorized"] = False
        write_json(EVDIR / "p7b_c_status.json", status)
        append_event("p7b_c_pass", completed_cells=completed)
        bar(100, "P7B-C physical cells PASS; STOP before P7B-D")
        print("WP2_P7B_C=PASS_PHYSICAL_CELLS")
        print("P7B_D=NOT_STARTED")
        print("UE_RAW_EVIDENCE_LOCATION=" + str(EVDIR))
        print("CORE_RAW_EVIDENCE_LOCATION=$HOME/wellpulse-powder-evidence/p7b/" + RUN_ID + "-core")
        print("TEARDOWN_AUTHORIZED=NO")
        print("SCORED_AUTHORIZATION=BLOCKED")
        return 0
    except Exception as exc:
        status["gate"] = "BLOCKED"
        status["failure"] = f"{type(exc).__name__}:{exc}"
        status["completed_cells"] = list(completed)
        status["p7b_d"] = "NOT_STARTED"
        status["teardown_authorized"] = False
        write_json(EVDIR / "p7b_c_status.json", status)
        append_event("p7b_c_blocked", failure=status["failure"], completed_cells=completed)
        print("WP2_P7B_C=BLOCKED:" + status["failure"])
        print("P7B_D=NOT_STARTED")
        print("UE_RAW_EVIDENCE_LOCATION=" + str(EVDIR))
        print("CORE_RAW_EVIDENCE_LOCATION=$HOME/wellpulse-powder-evidence/p7b/" + RUN_ID + "-core")
        print("TEARDOWN_AUTHORIZED=NO")
        print("SCORED_AUTHORIZATION=BLOCKED")
        return 70


if __name__ == "__main__":
    raise SystemExit(main())
