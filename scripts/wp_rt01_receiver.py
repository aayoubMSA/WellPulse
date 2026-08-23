#!/usr/bin/env python3
"""Line-oriented idempotent MQTT sink for WP-RT01.

Reads one canonical WellPulse JSON payload per stdin line, preserves every raw
broker delivery, and stores the first occurrence of each record_id in SQLite.
A control payload with `_wellpulse_control=END` terminates the sink without
being counted as an experimental record.
"""
from __future__ import print_function

import argparse
import datetime
import hashlib
import json
import os
import sqlite3
import sys


def utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()


def atomic_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, sort_keys=True, separators=(",", ":"))
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.rename(tmp, path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run-id", required=True)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir)
    raw_path = os.path.join(args.out_dir, "broker_deliveries.ndjson")
    db_path = os.path.join(args.out_dir, "received.sqlite")
    summary_path = os.path.join(args.out_dir, "receiver_summary.json")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS received ("
        "record_id TEXT PRIMARY KEY, payload_json TEXT NOT NULL, "
        "checksum_sha256 TEXT NOT NULL, first_seen_utc TEXT NOT NULL)"
    )
    conn.commit()

    total = 0
    invalid = 0
    control_seen = False
    started = utc_now()

    with open(raw_path, "a") as raw:
        for line in sys.stdin:
            payload_json = line.rstrip("\r\n")
            if not payload_json:
                continue
            try:
                obj = json.loads(payload_json)
            except Exception:
                invalid += 1
                raw.write(json.dumps({"received_utc": utc_now(), "invalid_payload": payload_json},
                                     sort_keys=True, separators=(",", ":")) + "\n")
                raw.flush()
                continue

            if obj.get("_wellpulse_control") == "END" and obj.get("run_id") == args.run_id:
                control_seen = True
                break

            total += 1
            received_utc = utc_now()
            record_id = obj.get("record_id")
            if not record_id:
                invalid += 1
                raw.write(json.dumps({"received_utc": received_utc, "invalid_payload": payload_json},
                                     sort_keys=True, separators=(",", ":")) + "\n")
                raw.flush()
                continue
            checksum = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
            raw.write(json.dumps({
                "received_utc": received_utc,
                "record_id": record_id,
                "checksum_sha256": checksum,
                "payload_json": payload_json,
            }, sort_keys=True, separators=(",", ":")) + "\n")
            raw.flush()
            conn.execute(
                "INSERT OR IGNORE INTO received(record_id,payload_json,checksum_sha256,first_seen_utc) "
                "VALUES(?,?,?,?)",
                (record_id, payload_json, checksum, received_utc),
            )
            conn.commit()

    unique = conn.execute("SELECT COUNT(*) FROM received").fetchone()[0]
    summary = {
        "run_id": args.run_id,
        "started_utc": started,
        "completed_utc": utc_now(),
        "broker_deliveries_total": total,
        "received_unique": unique,
        "duplicate_deliveries": total - unique,
        "invalid_deliveries": invalid,
        "control_end_seen": control_seen,
    }
    atomic_json(summary_path, summary)
    conn.close()
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
