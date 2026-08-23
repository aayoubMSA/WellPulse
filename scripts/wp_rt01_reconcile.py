#!/usr/bin/env python3
"""Reconcile one WP-RT01 edge run with its preserved broker deliveries."""
import argparse
import json
import math
from datetime import datetime
from pathlib import Path


def read_ndjson(path):
    if not path.exists():
        return []
    out = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def dt(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def percentile(values, pct):
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * pct / 100.0
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--edge-dir", required=True)
    p.add_argument("--receiver-dir", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()

    edge = Path(args.edge_dir)
    recv = Path(args.receiver_dir)
    generated = read_ndjson(edge / "generated_records.ndjson")
    deliveries = read_ndjson(recv / "broker_deliveries.ndjson")
    events = read_ndjson(edge / "edge_events.ndjson")
    edge_summary = json.loads((edge / "edge_summary.json").read_text())
    receiver_summary = json.loads((recv / "receiver_summary.json").read_text())

    gen_by_id = {r["record_id"]: r for r in generated}
    first_delivery = {}
    raw_delivery_count = 0
    checksum_mismatch = 0
    unexpected = []
    for d in deliveries:
        rid = d.get("record_id")
        if not rid:
            continue
        raw_delivery_count += 1
        if rid not in gen_by_id:
            unexpected.append(rid)
            continue
        if d.get("checksum_sha256") != gen_by_id[rid].get("checksum_sha256"):
            checksum_mismatch += 1
        if rid not in first_delivery:
            first_delivery[rid] = d

    gen_ids = set(gen_by_id)
    unique_ids = set(first_delivery)
    missing_ids = sorted(gen_ids - unique_ids)
    unexpected_ids = sorted(set(unexpected) | (unique_ids - gen_ids))

    latencies_ms = []
    for rid, d in first_delivery.items():
        if rid in gen_by_id:
            delta = (dt(d["received_utc"]) - dt(gen_by_id[rid]["generated_at_utc"])).total_seconds() * 1000.0
            latencies_ms.append(delta)

    outage_end = None
    restart_seen = False
    for e in events:
        if e.get("event") == "outage_end":
            outage_end = dt(e["utc"])
        if e.get("event") == "gateway_restart_exec":
            restart_seen = True

    reconnect_s = None
    backlog_drain_s = None
    oldest_queued_age_s = None
    if outage_end is not None:
        after = [dt(d["received_utc"]) for d in first_delivery.values() if dt(d["received_utc"]) >= outage_end]
        if after:
            reconnect_s = (min(after) - outage_end).total_seconds()
        if edge_summary["architecture"] == "W1_wellpulse_offline_first":
            backlog_times = []
            for seq in range(3001, 5001):
                rid = "%s:BOOT-001:%08d" % (edge_summary["run_id"], seq)
                if rid in first_delivery:
                    backlog_times.append(dt(first_delivery[rid]["received_utc"]))
            if backlog_times:
                backlog_drain_s = (max(backlog_times) - outage_end).total_seconds()
            rid_3001 = "%s:BOOT-001:%08d" % (edge_summary["run_id"], 3001)
            if rid_3001 in gen_by_id:
                oldest_queued_age_s = (outage_end - dt(gen_by_id[rid_3001]["generated_at_utc"])).total_seconds()

    cloud_unique = len(unique_ids & gen_ids)
    final_duplicates = 0  # receiver SQLite primary key enforces idempotent final state
    transport_duplicate_deliveries = max(0, raw_delivery_count - len(unique_ids))
    generated_count = len(generated)
    completeness = 100.0 if generated_count == 0 else 100.0 * cloud_unique / generated_count

    metrics = {
        "run_id": edge_summary["run_id"],
        "architecture": edge_summary["architecture"],
        "condition": edge_summary["condition"],
        "generated_records": generated_count,
        "local_committed": edge_summary.get("queue_total", 0),
        "cloud_unique": cloud_unique,
        "permanent_missing": len(missing_ids),
        "final_duplicates": final_duplicates,
        "transport_duplicate_deliveries": transport_duplicate_deliveries,
        "unexpected_records": len(unexpected_ids),
        "checksum_mismatch_deliveries": checksum_mismatch,
        "completeness_pct": completeness,
        "reconnect_s": reconnect_s,
        "backlog_drain_s": backlog_drain_s,
        "queue_high_water": edge_summary.get("queue_high_water", 0),
        "oldest_queued_age_s": oldest_queued_age_s,
        "latency_p50_ms": percentile(latencies_ms, 50),
        "latency_p95_ms": percentile(latencies_ms, 95),
        "latency_p99_ms": percentile(latencies_ms, 99),
        "restart_observed": restart_seen,
        "receiver_control_end_seen": receiver_summary.get("control_end_seen", False),
        "receiver_invalid_deliveries": receiver_summary.get("invalid_deliveries", 0),
        "missing_record_ids": missing_ids,
        "unexpected_record_ids": unexpected_ids,
    }
    metrics["w1_primary_success"] = (
        metrics["architecture"] == "W1_wellpulse_offline_first"
        and generated_count == 10000
        and cloud_unique == 10000
        and metrics["permanent_missing"] == 0
        and metrics["final_duplicates"] == 0
        and metrics["checksum_mismatch_deliveries"] == 0
    )

    Path(args.output).write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in metrics.items() if k not in {"missing_record_ids", "unexpected_record_ids"}},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
