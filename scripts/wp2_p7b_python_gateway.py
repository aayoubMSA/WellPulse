#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import signal
import time

from wellpulse.powder_w1 import DurablePahoReplay
from wellpulse.store import DurableQueue
from wellpulse.transport import PahoQoS1Config, PahoQoS1Session, make_run_client_id, make_run_topic


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def runtime_manifest(
    architecture: str,
    host: str,
    port: int,
    ca_file: str,
    broker_fingerprint: str,
    client_id: str,
    topic: str,
) -> dict:
    return {
        "evidence_class": "NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION",
        "scored": False,
        "architecture": architecture,
        "runtime": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "paho_mqtt_version": importlib.metadata.version("paho-mqtt"),
        },
        "transport": {
            "host": host,
            "port": port,
            "protocol": "MQTTv311",
            "qos": 1,
            "tls": True,
            "clean_session": False,
            "keepalive_s": 60,
            "reconnect_min_delay_s": 1,
            "reconnect_max_delay_s": 8,
            "max_queued_messages": 4096,
            "max_inflight_messages": 20,
            "ca_sha256": sha256_file(ca_file),
            "broker_fingerprint": broker_fingerprint,
            "client_id": client_id,
            "topic": topic,
        },
        "application": {
            "persistence_enabled": architecture == "W1_OFFLINE_FIRST",
            "store": (
                "WellPulse SQLite WAL synchronous=FULL"
                if architecture == "W1_OFFLINE_FIRST"
                else "NONE"
            ),
        },
    }


def emit(path: Path, event: str, **fields) -> None:
    row = {
        "utc": utc_now(),
        "monotonic_ns": time.monotonic_ns(),
        "event": event,
        **fields,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        fh.flush()


def main() -> int:
    ap = argparse.ArgumentParser(description="WP2-P7B separated B1/W1 gateway process")
    ap.add_argument("--architecture", required=True, choices=("B1", "W1"))
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, default=8883)
    ap.add_argument("--ca-file", required=True)
    ap.add_argument("--broker-fingerprint", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--fifo")
    ap.add_argument("--queue-db")
    args = ap.parse_args()
    if importlib.metadata.version("paho-mqtt") != "2.1.0":
        raise RuntimeError("WP2-P7B requires paho-mqtt==2.1.0")
    if args.architecture == "B1" and not args.fifo:
        raise ValueError("B1 requires --fifo")
    if args.architecture == "W1" and not args.queue_db:
        raise ValueError("W1 requires --queue-db")

    architecture = "B1_MQTT_QOS1" if args.architecture == "B1" else "W1_OFFLINE_FIRST"
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    process_events = out / "gateway_process_events.jsonl"
    mqtt_events = out / "mqtt_events.jsonl"
    topic = make_run_topic(args.run_id, architecture)
    client_id = make_run_client_id(args.run_id, architecture)
    manifest = runtime_manifest(
        architecture,
        args.host,
        args.port,
        args.ca_file,
        args.broker_fingerprint,
        client_id,
        topic,
    )
    (out / "runtime_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    config = PahoQoS1Config(
        host=args.host,
        port=args.port,
        topic=topic,
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
    session = PahoQoS1Session(config, client_id=client_id, event_log=mqtt_events)
    stop = False

    def request_stop(signum, frame):
        nonlocal stop
        emit(process_events, "gateway_stop_requested", pid=os.getpid(), signal=int(signum))
        stop = True

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    emit(
        process_events,
        "gateway_start",
        pid=os.getpid(),
        architecture=architecture,
        client_id=client_id,
        topic=topic,
    )
    session.connect()
    queue = DurableQueue(args.queue_db) if args.architecture == "W1" else None
    replay = DurablePahoReplay(queue, session) if queue is not None else None
    fifo_fd = None
    fifo_buffer = b""
    try:
        if args.architecture == "B1":
            fifo_fd = os.open(args.fifo, os.O_RDONLY | os.O_NONBLOCK)
        while not stop:
            if replay is not None:
                replay.pump_once()
            else:
                try:
                    chunk = os.read(fifo_fd, 65536)
                except BlockingIOError:
                    chunk = b""
                if chunk:
                    fifo_buffer += chunk
                    while b"\n" in fifo_buffer:
                        raw, fifo_buffer = fifo_buffer.split(b"\n", 1)
                        if raw:
                            session.publish_async(raw.decode("utf-8"))
                elif chunk == b"":
                    time.sleep(0.05)
            time.sleep(0.01)
    finally:
        snapshot = session.snapshot()
        snapshot["exact_internal_queue_occupancy_claim"] = False
        (out / "pre_exit_transport_snapshot.json").write_text(
            json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        emit(
            process_events,
            "gateway_exit",
            pid=os.getpid(),
            client_id=client_id,
            topic=topic,
        )
        try:
            session.close_at_horizon()
        finally:
            if fifo_fd is not None:
                os.close(fifo_fd)
            if queue is not None:
                queue.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
