#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import math
import os
import sqlite3
import sys


def percentile(values, p):
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    k = (len(xs) - 1) * (p / 100.0)
    lo = int(math.floor(k))
    hi = int(math.ceil(k))
    if lo == hi:
        return xs[lo]
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def verify_wire(obj):
    expected = obj.get("checksum_sha256")
    body = dict(obj)
    body.pop("checksum_sha256", None)
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    actual = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return expected == actual


def load_generated(path):
    rows = {}
    checksum_errors = 0
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            obj = json.loads(line)
            if not verify_wire(obj):
                checksum_errors += 1
            rid = obj["record_id"]
            if rid in rows:
                raise RuntimeError("duplicate generated record_id: %s" % rid)
            rows[rid] = obj
    return rows, checksum_errors


def load_events(path):
    events = []
    if not os.path.exists(path):
        return events
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                events.append(json.loads(line))
    return events


def first_numeric(events, event_name, field):
    for e in events:
        if e.get("event") == event_name and e.get(field) is not None:
            return float(e[field])
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--architecture", required=True)
    ap.add_argument("--condition", required=True)
    ap.add_argument("--generated", required=True)
    ap.add_argument("--receiver-raw", required=True)
    ap.add_argument("--events", required=True)
    ap.add_argument("--queue-db")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--require-complete", action="store_true")
    ap.add_argument("--require-baseline-loss", action="store_true")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    generated, generated_checksum_errors = load_generated(args.generated)
    if len(generated) != 10000:
        raise RuntimeError("expected exactly 10000 generated records, got %d" % len(generated))

    receiver_db = os.path.join(args.outdir, "receiver.sqlite")
    conn = sqlite3.connect(receiver_db)
    conn.execute(
        """CREATE TABLE received (
            record_id TEXT PRIMARY KEY,
            wire_json TEXT NOT NULL,
            first_seen_epoch REAL NOT NULL,
            seen_count INTEGER NOT NULL DEFAULT 1
        )"""
    )

    raw_received = 0
    receiver_checksum_errors = 0
    foreign_records_ignored = 0
    with open(args.receiver_raw, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\r\n")
            if not line or "\t" not in line:
                continue
            ts_text, wire = line.split("\t", 1)
            try:
                arrival = float(ts_text)
                obj = json.loads(wire)
            except Exception:
                continue
            if obj.get("run_id") != args.run_id:
                foreign_records_ignored += 1
                continue
            raw_received += 1
            if not verify_wire(obj):
                receiver_checksum_errors += 1
            rid = obj.get("record_id")
            cur = conn.execute("SELECT seen_count FROM received WHERE record_id=?", (rid,))
            row = cur.fetchone()
            if row is None:
                conn.execute(
                    "INSERT INTO received(record_id,wire_json,first_seen_epoch,seen_count) VALUES(?,?,?,1)",
                    (rid, wire, arrival),
                )
            else:
                conn.execute(
                    "UPDATE received SET seen_count=seen_count+1 WHERE record_id=?",
                    (rid,),
                )
    conn.commit()

    received = {}
    for rid, first_seen, seen_count in conn.execute(
        "SELECT record_id,first_seen_epoch,seen_count FROM received ORDER BY record_id"
    ):
        received[rid] = (float(first_seen), int(seen_count))

    gen_ids = set(generated)
    recv_ids = set(received)
    missing = sorted(gen_ids - recv_ids)
    unexpected = sorted(recv_ids - gen_ids)
    transport_duplicates = sum(max(0, x[1] - 1) for x in received.values())

    latencies = []
    negative_latency_count = 0
    rows_out = []
    for rid in sorted(gen_ids | recv_ids):
        if rid in generated and rid in received:
            latency_ms = (received[rid][0] - float(generated[rid]["generated_at_epoch"])) * 1000.0
            if latency_ms < 0:
                negative_latency_count += 1
            latencies.append(latency_ms)
            status = "RECEIVED"
            seen_count = received[rid][1]
            first_seen = received[rid][0]
        elif rid in generated:
            latency_ms = None
            status = "MISSING"
            seen_count = 0
            first_seen = None
        else:
            latency_ms = None
            status = "UNEXPECTED"
            seen_count = received[rid][1]
            first_seen = received[rid][0]
        rows_out.append((rid, status, first_seen, latency_ms, seen_count))

    with open(os.path.join(args.outdir, "reconciliation.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["record_id", "status", "first_seen_epoch", "latency_ms", "seen_count"])
        w.writerows(rows_out)

    local_committed = 0
    pending_final = 0
    if args.queue_db and os.path.exists(args.queue_db):
        q = sqlite3.connect(args.queue_db)
        local_committed = q.execute("SELECT COUNT(*) FROM queue").fetchone()[0]
        pending_final = q.execute("SELECT COUNT(*) FROM queue WHERE state='PENDING'").fetchone()[0]
        q.close()

    events = load_events(args.events)
    reconnect_s = first_numeric(events, "outage_off", "reconnect_s")
    backlog_drain_s = first_numeric(events, "backlog_drained", "backlog_drain_s")
    restart_entry_count = sum(1 for e in events if e.get("event") == "restart_entry_outage_verified")

    metrics = {
        "run_id": args.run_id,
        "architecture": args.architecture,
        "condition": args.condition,
        "generated_records": len(generated),
        "local_committed": local_committed,
        "raw_received": raw_received,
        "cloud_unique": len(gen_ids & recv_ids),
        "permanent_missing": len(missing),
        "unexpected_records": len(unexpected),
        "transport_duplicate_deliveries": transport_duplicates,
        "final_duplicates": 0,
        "completeness_pct": round(100.0 * len(gen_ids & recv_ids) / len(generated), 6),
        "generated_checksum_errors": generated_checksum_errors,
        "receiver_checksum_errors": receiver_checksum_errors,
        "foreign_records_ignored": foreign_records_ignored,
        "reconnect_s": reconnect_s,
        "backlog_drain_s": backlog_drain_s,
        "latency_p50_ms": percentile(latencies, 50),
        "latency_p95_ms": percentile(latencies, 95),
        "latency_p99_ms": percentile(latencies, 99),
        "negative_latency_count": negative_latency_count,
        "restart_entry_count": restart_entry_count,
        "pending_final": pending_final,
        "latency_note": "Wall-clock latency is provisional until FIT A8/frontend clock-offset characterization is frozen.",
    }

    with open(os.path.join(args.outdir, "metrics.json"), "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(metrics, indent=2, sort_keys=True))

    failures = []
    if generated_checksum_errors or receiver_checksum_errors:
        failures.append("checksum errors")
    if unexpected:
        failures.append("unexpected records")
    if args.condition == "C2_outage_restart" and restart_entry_count < 1:
        failures.append("restart-entry outage verification missing")
    if args.require_complete:
        if len(generated) != 10000 or len(missing) != 0 or metrics["final_duplicates"] != 0 or pending_final != 0:
            failures.append("complete-reconciliation gate failed")
    if args.require_baseline_loss and len(missing) == 0:
        failures.append("baseline-loss gate failed")
    conn.close()
    if failures:
        print("GATE_FAIL: " + "; ".join(failures), file=sys.stderr)
        return 2
    print("GATE_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
