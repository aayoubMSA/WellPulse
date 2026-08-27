#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import errno
import json
import os
from pathlib import Path
import time

from wellpulse.records import make_record
from wellpulse.store import DurableQueue


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit_event(path: Path, event: str, **fields) -> None:
    row = {
        "utc": utc_now(),
        "monotonic_ns": time.monotonic_ns(),
        "event": event,
        **fields,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        fh.flush()


def fifo_handoff(path: Path, payload: str) -> str:
    try:
        fd = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
    except OSError as exc:
        if exc.errno in (errno.ENXIO, errno.ENOENT):
            return "NO_GATEWAY_READER_DROPPED"
        raise
    try:
        os.write(fd, payload.encode("utf-8") + b"\n")
        return "HANDED_TO_GATEWAY"
    finally:
        os.close(fd)


def main() -> int:
    ap = argparse.ArgumentParser(description="WP2-P7B separated non-scored telemetry generator")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--boot-id", default="P7BGEN")
    ap.add_argument("--architecture", required=True, choices=("B1", "W1", "B2"))
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--fifo")
    ap.add_argument("--queue-db")
    ap.add_argument("--interval-s", type=float, default=1.0)
    ap.add_argument("--count", type=int, required=True)
    args = ap.parse_args()
    if args.count <= 0 or args.interval_s <= 0:
        raise ValueError("count and interval must be positive")
    if args.architecture == "W1" and not args.queue_db:
        raise ValueError("W1 requires --queue-db")
    if args.architecture in {"B1", "B2"} and not args.fifo:
        raise ValueError("B1/B2 require --fifo non-durable handoff")

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    ledger = out / "telemetry_generated.csv"
    events = out / "generator_events.jsonl"
    queue = DurableQueue(args.queue_db) if args.architecture == "W1" else None
    emit_event(events, "generator_start", pid=os.getpid(), architecture=args.architecture)

    try:
        with ledger.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=[
                    "record_id",
                    "sequence",
                    "generated_ts_utc",
                    "payload_sha256",
                    "payload_json",
                    "handoff_status",
                ],
            )
            writer.writeheader()
            next_at = time.monotonic()
            for sequence in range(1, args.count + 1):
                delay = next_at - time.monotonic()
                if delay > 0:
                    time.sleep(delay)
                record = make_record(args.run_id, args.boot_id, sequence)
                payload = record.canonical_payload()
                if queue is not None:
                    queue.enqueue(record)
                    handoff = "DURABLY_ENQUEUED"
                else:
                    handoff = fifo_handoff(Path(args.fifo), payload)
                writer.writerow(
                    {
                        "record_id": record.record_id,
                        "sequence": sequence,
                        "generated_ts_utc": record.generated_at_utc,
                        "payload_sha256": record.checksum_sha256,
                        "payload_json": payload,
                        "handoff_status": handoff,
                    }
                )
                fh.flush()
                emit_event(
                    events,
                    "record_generated",
                    pid=os.getpid(),
                    sequence=sequence,
                    record_id=record.record_id,
                    handoff_status=handoff,
                )
                next_at += args.interval_s
    finally:
        if queue is not None:
            queue.close()
        emit_event(events, "generator_stop", pid=os.getpid(), generated_count=args.count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
