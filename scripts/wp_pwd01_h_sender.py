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
from wellpulse.transport import PahoQoS1Config, PahoQoS1Session


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


def run_capture(cmd: list[str], *, check: bool = False) -> tuple[int, str]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed rc={proc.returncode}: {' '.join(cmd)}\n{proc.stdout}")
    return proc.returncode, proc.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="WP-PWD01 W1 non-scored recovery-horizon calibration trial")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--host", default="172.16.0.1")
    parser.add_argument("--port", type=int, default=8883)
    parser.add_argument("--topic", default="wellpulse/records")
    parser.add_argument("--ca-file", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    if importlib.metadata.version("paho-mqtt") != "2.1.0":
        raise RuntimeError("WP-PWD01 requires paho-mqtt==2.1.0")

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
        topic=args.topic,
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
    session = PahoQoS1Session(config, client_id=("wp-h-tx-" + args.run_id)[-64:], event_log=events_path)
    worker_stop = threading.Event()
    worker_error: list[str] = []
    shared_lock = threading.Lock()
    shared_pending_ids: set[str] = set()
    shared_snapshot = None

    def replay_worker() -> None:
        nonlocal shared_pending_ids, shared_snapshot
        worker_queue = DurableQueue(queue_path)
        replay = DurablePahoReplay(worker_queue, session)
        last_log = 0.0
        try:
            with queue_timeline_path.open("w", encoding="utf-8", newline="") as fh:
                writer = csv.writer(fh)
                writer.writerow(["utc", "connected", "pending_count", "app_inflight_count", "published_calls", "puback_callbacks"])
                while not worker_stop.is_set():
                    snap = replay.pump_once()
                    pending_ids = replay.pending_record_ids()
                    with shared_lock:
                        shared_pending_ids = pending_ids
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
        finally:
            worker_queue.close()

    summary = {
        "run_id": args.run_id,
        "status": "STARTING",
        "scored": False,
        "route_output": route_output,
        "q0_readiness_pre": None,
        "q0_health_post": None,
        "q3_start_utc": None,
        "cohort_cutoff_utc": None,
        "queue_pending_zero_utc": None,
        "cohort_record_count": None,
        "generated_record_count": 0,
        "worker_error": None,
    }

    worker = None
    generated_ids: list[str] = []
    cutoff_ids: set[str] = set()
    try:
        set_attenuation(Q0_DB)
        ping_rc, ping_output = run_capture(["ping", "-I", "tun_srsue", "-c", "5", "-W", "2", args.host])
        summary["q0_readiness_pre"] = {"rc": ping_rc, "output": ping_output}
        if ping_rc != 0 or not re.search(r"0(?:\.0+)?% packet loss", ping_output):
            raise RuntimeError("mandatory Q0 LTE user-plane readiness gate failed")

        session.connect()
        connected_deadline = time.monotonic() + 20.0
        while time.monotonic() < connected_deadline and not session.snapshot()["connected"]:
            time.sleep(0.1)
        if not session.snapshot()["connected"]:
            raise RuntimeError("MQTT session did not connect at healthy Q0")

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
            next_record_mono = start_mono
            q3_applied = False
            q0_restored = False
            cutoff_mono = None
            queue_zero_mono = None
            sequence = 0

            while True:
                if worker_error:
                    raise RuntimeError("replay worker failed: " + worker_error[-1])

                now = time.monotonic()
                elapsed = now - start_mono

                if not q3_applied and elapsed >= WARMUP_S + PRE_IMPAIRMENT_Q0_S:
                    q3_start, _ = set_attenuation(Q3_DB)
                    summary["q3_start_utc"] = q3_start
                    q3_applied = True

                if not q0_restored and elapsed >= WARMUP_S + PRE_IMPAIRMENT_Q0_S + Q3_DURATION_S:
                    _restore_start, restore_end = set_attenuation(Q0_DB)
                    summary["cohort_cutoff_utc"] = restore_end
                    cutoff_mono = time.monotonic()
                    cutoff_ids = set(generated_ids)
                    summary["cohort_record_count"] = len(cutoff_ids)
                    q0_restored = True

                if now >= next_record_mono:
                    sequence += 1
                    record = make_record(args.run_id, "BOOT-001", sequence)
                    payload_json = record.canonical_payload()
                    generator_queue.enqueue(record)
                    generated_ids.append(record.record_id)
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

                if q0_restored:
                    with shared_lock:
                        pending_now = set(shared_pending_ids)
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

                sleep_for = max(0.01, min(0.1, next_record_mono - time.monotonic()))
                time.sleep(sleep_for)

        summary["generated_record_count"] = len(generated_ids)
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
            post_rc != 0 or not re.search(r"0(?:\.0+)?% packet loss", post_output)
        ):
            summary["status"] = "INVALID_POST_Q0_USER_PLANE_HEALTH"

    except Exception as exc:
        summary["status"] = "INVALID_TECHNICAL_FAILURE"
        summary["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        worker_stop.set()
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
        summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0 if summary["status"] == "QUEUE_DRAIN_OBSERVED_PENDING_SINK_RECONSTRUCTION" else 20


if __name__ == "__main__":
    raise SystemExit(main())
