#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import threading
import time

from wellpulse.powder_w1 import DurablePahoReplay
from wellpulse.records import make_record
from wellpulse.store import DurableQueue
from wellpulse.transport import (
    PahoQoS1Config,
    PahoQoS1Session,
    make_run_client_id,
    make_run_topic,
)


ATTENUATOR_IDS = (1, 33, 2, 34)
Q0_DB = 0
Q3_DB = 55
WARMUP_S = 30.0
PRE_IMPAIRMENT_Q0_S = 60.0
Q3_DURATION_S = 120.0
MAX_DRAIN_OBSERVATION_S = 150.0
POST_QUEUE_ZERO_OBSERVATION_S = 10.0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_utc(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError(f"timestamp lacks timezone: {value}")
    return dt.astimezone(timezone.utc)


def run_capture(cmd: list[str], *, check: bool = False) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed rc={proc.returncode}: {' '.join(cmd)}\n{proc.stdout}")
    return proc.returncode, proc.stdout.strip()


def has_zero_packet_loss(output: str) -> bool:
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)% packet loss", output)
    return bool(match and float(match.group(1)) == 0.0)


def main() -> int:
    parser = argparse.ArgumentParser(description="WP-PWD01 W1 non-scored recovery-horizon calibration trial")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--host", default="172.16.0.1")
    parser.add_argument("--port", type=int, default=8883)
    parser.add_argument("--topic", default=None, help="Optional override; default is deterministic run-isolated topic")
    parser.add_argument("--ca-file", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    if importlib.metadata.version("paho-mqtt") != "2.1.0":
        raise RuntimeError("WP-PWD01 requires paho-mqtt==2.1.0")

    mqtt_topic = args.topic or make_run_topic(args.run_id, "HCAL")
    mqtt_client_id = make_run_client_id(args.run_id, "HCTX")

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    generated_path = out / "telemetry_generated.csv"
    attenuation_path = out / "attenuation_timeline.csv"
    queue_timeline_path = out / "queue_timeline.csv"
    events_path = out / "mqtt_events.jsonl"
    summary_path = out / "sender_summary.json"
    manifest_path = out / "calibration_manifest.json"
    queue_path = out / "w1_queue.sqlite"

    def set_attenuation(value_db: int) -> tuple[str, str]:
        start = utc_now()
        for atten_id in ATTENUATOR_IDS:
            run_capture(["/usr/local/etc/emulab/tmcc", "attenuator", str(atten_id), str(value_db)], check=True)
        end = utc_now()
        with attenuation_path.open("a", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow([start, end, value_db, " ".join(map(str, ATTENUATOR_IDS))])
            fh.flush()
        return start, end

    with attenuation_path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerow(["command_start_utc", "command_end_utc", "programmed_attenuation_db", "attenuator_ids"])

    route_rc, route_output = run_capture(["ip", "route", "get", args.host])
    clock_evidence = {}
    for name, cmd in {
        "date_utc": ["date", "-u", "+%Y-%m-%dT%H:%M:%S.%NZ"],
        "ntp_synchronized": ["timedatectl", "show", "-p", "NTPSynchronized", "--value"],
        "chrony_tracking": ["chronyc", "tracking"],
    }.items():
        try:
            rc, output = run_capture(cmd)
            clock_evidence[name] = {"rc": rc, "output": output}
        except FileNotFoundError:
            clock_evidence[name] = {"rc": 127, "output": "not_available"}

    git_rc, git_sha = run_capture(["git", "rev-parse", "HEAD"])
    python_version = sys.version.split()[0]

    config = PahoQoS1Config(
        host=args.host,
        port=args.port,
        topic=mqtt_topic,
        ca_file=args.ca_file,
        tls=True,
        qos=1,
        keepalive_s=60,
        clean_session=False,
        reconnect_min_delay_s=1,
        reconnect_max_delay_s=8,
        max_queued_messages=4096,
        max_inflight_messages=20,
    )

    manifest = {
        "evidence_class": "NON_SCORED_WP2_H_CALIBRATION",
        "run_id": args.run_id,
        "architecture": "W1_OFFLINE_FIRST",
        "protocol_version": "v0.4",
        "h_calibration_plan": "experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md",
        "wellpulse_git_sha": git_sha if git_rc == 0 else "unknown",
        "python_version": python_version,
        "paho_mqtt_version": importlib.metadata.version("paho-mqtt"),
        "sqlite_version": sqlite3.sqlite_version,
        "mqtt": config.public_dict(),
        "mqtt_isolation": {
            "publisher_client_id": mqtt_client_id,
            "topic": mqtt_topic,
            "initial_session_present_required": False,
        },
        "rf": {"Q0_db": Q0_DB, "Q3_db": Q3_DB, "attenuator_ids": list(ATTENUATOR_IDS)},
        "schedule_s": {
            "readiness_warmup": WARMUP_S,
            "pre_impairment_Q0": PRE_IMPAIRMENT_Q0_S,
            "Q3": Q3_DURATION_S,
            "max_drain_observation": MAX_DRAIN_OBSERVATION_S,
        },
        "route_check": {"rc": route_rc, "output": route_output},
        "clock_evidence": clock_evidence,
        "scored": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if route_rc != 0 or "tun_srsue" not in route_output:
        raise RuntimeError(f"experimental LTE route gate failed for {args.host}: {route_output}")

    generator_queue = DurableQueue(queue_path)
    session = PahoQoS1Session(config, client_id=mqtt_client_id, event_log=events_path)
    worker_stop = threading.Event()
    trial_abort = threading.Event()
    q0_restored_event = threading.Event()
    worker_error: list[str] = []
    rf_error: list[str] = []
    shared_lock = threading.Lock()
    shared_snapshot = None
    rf_state: dict[str, object] = {}

    def replay_worker() -> None:
        nonlocal shared_snapshot
        worker_queue = DurableQueue(queue_path)
        replay = DurablePahoReplay(worker_queue, session)
        last_log = 0.0
        try:
            with queue_timeline_path.open("w", encoding="utf-8", newline="") as fh:
                writer = csv.writer(fh)
                writer.writerow(["utc", "connected", "pending_count", "app_inflight_count", "published_calls", "puback_callbacks"])
                while not worker_stop.is_set():
                    snap = replay.pump_once()
                    with shared_lock:
                        shared_snapshot = snap
                    now = time.monotonic()
                    if now - last_log >= 0.5:
                        writer.writerow([
                            utc_now(),
                            snap.connected,
                            snap.pending_count,
                            snap.app_inflight_count,
                            snap.published_calls,
                            snap.puback_callbacks,
                        ])
                        fh.flush()
                        last_log = now
                    worker_stop.wait(0.05)
        except Exception as exc:
            worker_error.append(f"{type(exc).__name__}: {exc}")
            trial_abort.set()
        finally:
            worker_queue.close()

    def wait_until(target_mono: float) -> bool:
        while True:
            if trial_abort.is_set():
                return False
            remaining = target_mono - time.monotonic()
            if remaining <= 0:
                return True
            trial_abort.wait(min(0.1, remaining))

    def rf_controller(start_mono: float) -> None:
        try:
            if not wait_until(start_mono + WARMUP_S + PRE_IMPAIRMENT_Q0_S):
                return
            _q3_command_start, q3_command_end = set_attenuation(Q3_DB)
            q3_effective_mono = time.monotonic()
            with shared_lock:
                rf_state["q3_effective_utc"] = q3_command_end
                rf_state["q3_effective_mono"] = q3_effective_mono

            if not wait_until(q3_effective_mono + Q3_DURATION_S):
                return
            q0_command_start_mono = time.monotonic()
            q0_command_start, q0_command_end = set_attenuation(Q0_DB)
            cutoff_mono = time.monotonic()
            with shared_lock:
                rf_state["q0_restore_command_start_utc"] = q0_command_start
                rf_state["cohort_cutoff_utc"] = q0_command_end
                rf_state["cohort_cutoff_mono"] = cutoff_mono
                rf_state["q3_full_state_duration_s"] = q0_command_start_mono - q3_effective_mono
            q0_restored_event.set()
        except Exception as exc:
            rf_error.append(f"{type(exc).__name__}: {exc}")
            trial_abort.set()

    summary = {
        "run_id": args.run_id,
        "status": "STARTING",
        "scored": False,
        "mqtt_client_id": mqtt_client_id,
        "mqtt_topic": mqtt_topic,
        "initial_session_present": None,
        "route_output": route_output,
        "q0_readiness_pre": None,
        "q0_health_post": None,
        "q3_effective_utc": None,
        "q3_full_state_duration_s": None,
        "cohort_cutoff_utc": None,
        "queue_pending_zero_utc": None,
        "cohort_record_count": None,
        "generated_record_count": 0,
        "generation_max_lag_s": 0.0,
        "worker_error": None,
        "rf_error": None,
    }

    worker = None
    rf_thread = None
    generated_meta: list[tuple[str, str]] = []
    cutoff_ids: set[str] = set()
    try:
        set_attenuation(Q0_DB)
        ping_rc, ping_output = run_capture(["ping", "-I", "tun_srsue", "-c", "5", "-W", "2", args.host])
        summary["q0_readiness_pre"] = {"rc": ping_rc, "output": ping_output}
        if ping_rc != 0 or not has_zero_packet_loss(ping_output):
            raise RuntimeError("mandatory Q0 LTE user-plane readiness gate failed")

        session.connect()
        connected_deadline = time.monotonic() + 20.0
        while time.monotonic() < connected_deadline and not session.snapshot()["connected"]:
            time.sleep(0.1)
        initial_snapshot = session.snapshot()
        if not initial_snapshot["connected"]:
            raise RuntimeError("MQTT session did not connect at healthy Q0")
        summary["initial_session_present"] = initial_snapshot["session_present"]
        if initial_snapshot["session_present"] is not False:
            raise RuntimeError(
                "run-isolation gate failed: fresh H-calibration publisher unexpectedly resumed an existing MQTT session"
            )

        worker = threading.Thread(target=replay_worker, name="w1-replay", daemon=True)
        worker.start()

        with generated_path.open("w", encoding="utf-8", newline="") as gen_fh:
            gen_writer = csv.DictWriter(
                gen_fh,
                fieldnames=["record_id", "generated_ts_utc", "payload_sha256", "payload_json"],
            )
            gen_writer.writeheader()
            gen_fh.flush()

            start_mono = time.monotonic()
            rf_thread = threading.Thread(target=rf_controller, args=(start_mono,), name="rf-controller", daemon=True)
            rf_thread.start()
            next_record_mono = start_mono
            queue_zero_mono = None
            cutoff_mono = None
            cutoff_seen = False
            sequence = 0

            while True:
                if worker_error:
                    raise RuntimeError("replay worker failed: " + worker_error[-1])
                if rf_error:
                    raise RuntimeError("RF controller failed: " + rf_error[-1])

                if q0_restored_event.is_set() and not cutoff_seen:
                    with shared_lock:
                        cutoff_text = str(rf_state["cohort_cutoff_utc"])
                        cutoff_mono = float(rf_state["cohort_cutoff_mono"])
                        summary["q3_effective_utc"] = str(rf_state["q3_effective_utc"])
                        summary["q3_full_state_duration_s"] = float(rf_state["q3_full_state_duration_s"])
                    summary["cohort_cutoff_utc"] = cutoff_text
                    cutoff_dt = parse_utc(cutoff_text)
                    cutoff_ids = {rid for rid, ts in generated_meta if parse_utc(ts) <= cutoff_dt}
                    summary["cohort_record_count"] = len(cutoff_ids)
                    cutoff_seen = True

                now = time.monotonic()
                if now >= next_record_mono:
                    lag = max(0.0, now - next_record_mono)
                    summary["generation_max_lag_s"] = max(float(summary["generation_max_lag_s"]), lag)
                    sequence += 1
                    record = make_record(args.run_id, "BOOT-001", sequence)
                    payload_json = record.canonical_payload()
                    generator_queue.enqueue(record)
                    generated_meta.append((record.record_id, record.generated_at_utc))
                    gen_writer.writerow(
                        {
                            "record_id": record.record_id,
                            "generated_ts_utc": record.generated_at_utc,
                            "payload_sha256": record.checksum_sha256,
                            "payload_json": payload_json,
                        }
                    )
                    gen_fh.flush()
                    next_record_mono += 1.0

                if cutoff_seen:
                    pending_now = {row[0] for row in generator_queue.pending_rows()}
                    cohort_pending = pending_now.intersection(cutoff_ids)
                    if not cohort_pending and queue_zero_mono is None:
                        queue_zero_mono = time.monotonic()
                        summary["queue_pending_zero_utc"] = utc_now()
                    if queue_zero_mono is not None and time.monotonic() - queue_zero_mono >= POST_QUEUE_ZERO_OBSERVATION_S:
                        summary["status"] = "QUEUE_DRAIN_OBSERVED_PENDING_SINK_RECONSTRUCTION"
                        break
                    if cutoff_mono is not None and time.monotonic() - cutoff_mono > MAX_DRAIN_OBSERVATION_S and cohort_pending:
                        summary["status"] = "STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S"
                        break

                sleep_for = max(0.005, min(0.05, next_record_mono - time.monotonic()))
                time.sleep(sleep_for)

        summary["generated_record_count"] = len(generated_meta)
        trial_abort.set()
        if rf_thread is not None:
            rf_thread.join(timeout=5)
        worker_stop.set()
        if worker is not None:
            worker.join(timeout=5)
        with shared_lock:
            if shared_snapshot is not None:
                summary["final_replay_snapshot"] = {
                    "connected": shared_snapshot.connected,
                    "pending_count": shared_snapshot.pending_count,
                    "app_inflight_count": shared_snapshot.app_inflight_count,
                    "published_calls": shared_snapshot.published_calls,
                    "puback_callbacks": shared_snapshot.puback_callbacks,
                }
        session.close_at_horizon()

        post_rc, post_output = run_capture(["ping", "-I", "tun_srsue", "-c", "3", "-W", "2", args.host])
        summary["q0_health_post"] = {"rc": post_rc, "output": post_output}
        if summary["status"] == "QUEUE_DRAIN_OBSERVED_PENDING_SINK_RECONSTRUCTION" and (
            post_rc != 0 or not has_zero_packet_loss(post_output)
        ):
            summary["status"] = "INVALID_POST_Q0_USER_PLANE_HEALTH"

    except Exception as exc:
        summary["status"] = "INVALID_TECHNICAL_FAILURE"
        summary["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        trial_abort.set()
        worker_stop.set()
        if rf_thread is not None and rf_thread.is_alive():
            rf_thread.join(timeout=5)
        if worker is not None and worker.is_alive():
            worker.join(timeout=5)
        try:
            set_attenuation(Q0_DB)
        except Exception as reset_exc:
            summary["q0_reset_error"] = f"{type(reset_exc).__name__}: {reset_exc}"
        try:
            if session.snapshot()["connected"]:
                session.close_at_horizon()
        except Exception:
            pass
        generator_queue.close()
        if worker_error:
            summary["worker_error"] = worker_error[-1]
        if rf_error:
            summary["rf_error"] = rf_error[-1]
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0 if summary["status"] == "QUEUE_DRAIN_OBSERVED_PENDING_SINK_RECONSTRUCTION" else 20


if __name__ == "__main__":
    raise SystemExit(main())