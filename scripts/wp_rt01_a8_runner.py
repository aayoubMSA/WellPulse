#!/usr/bin/env python3
"""Python-3.5-compatible FIT A8 execution adapter for WP-RT01.

This adapter preserves the frozen B0/W1 durability semantics while using the
Mosquitto CLI already present on the FIT A8 image. It is an execution adapter,
not a replacement research design.
"""
from __future__ import print_function

import argparse
import datetime
import hashlib
import json
import os
import socket
import sqlite3
import subprocess
import sys
import time


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


def append_json(path, obj):
    with open(path, "a") as fh:
        fh.write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")
        fh.flush()


def write_json_line(fh, obj):
    fh.write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")


def canonical_record(run_id, boot_id, sequence):
    body = {
        "run_id": run_id,
        "boot_id": boot_id,
        "sequence": sequence,
        "generated_at_utc": utc_now(),
        "source": "synthetic_modbus_like",
        "payload": {"register_1": 1000 + sequence, "status": sequence % 4},
        "quality_flag": "OK",
        "record_id": "%s:%s:%08d" % (run_id, boot_id, sequence),
    }
    payload_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
    checksum = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
    return body, payload_json, checksum


class DurableQueue(object):
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=FULL")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS queue ("
            "record_id TEXT PRIMARY KEY, sequence INTEGER NOT NULL, "
            "payload_json TEXT NOT NULL, checksum_sha256 TEXT NOT NULL, "
            "state TEXT NOT NULL DEFAULT 'PENDING')"
        )
        self.conn.commit()

    def enqueue(self, record_id, sequence, payload_json, checksum):
        self.conn.execute(
            "INSERT OR IGNORE INTO queue(record_id,sequence,payload_json,checksum_sha256,state) "
            "VALUES(?,?,?,?, 'PENDING')",
            (record_id, sequence, payload_json, checksum),
        )
        self.conn.commit()

    def pending(self, limit):
        return list(self.conn.execute(
            "SELECT record_id,sequence,payload_json,checksum_sha256 FROM queue "
            "WHERE state='PENDING' ORDER BY sequence LIMIT ?", (limit,)
        ))

    def mark_sent(self, record_ids):
        self.conn.executemany("UPDATE queue SET state='SENT' WHERE record_id=?", [(x,) for x in record_ids])
        self.conn.commit()

    def pending_count(self):
        return self.conn.execute("SELECT COUNT(*) FROM queue WHERE state='PENDING'").fetchone()[0]

    def total_count(self):
        return self.conn.execute("SELECT COUNT(*) FROM queue").fetchone()[0]

    def close(self):
        self.conn.close()


def mqtt_publish_lines(args, payloads, events_path):
    if not payloads:
        return True
    cmd = [
        "mosquitto_pub", "--cafile", args.ca_file,
        "-h", args.broker, "-p", str(args.port),
        "-q", "1", "-t", args.topic, "-l",
    ]
    started = time.time()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate("\n".join(payloads) + "\n")
    ended = time.time()
    append_json(events_path, {
        "event": "mqtt_batch",
        "utc": utc_now(),
        "count": len(payloads),
        "rc": proc.returncode,
        "duration_s": ended - started,
        "stderr": err.strip()[-1000:],
    })
    return proc.returncode == 0


def broker_ipv4(host):
    return socket.gethostbyname(host)


def iptables_rule(ip):
    return ["iptables", "-A", "OUTPUT", "-p", "tcp", "-d", ip,
            "--dport", "8883", "-j", "REJECT"]


def iptables_delete_rule(ip):
    return ["iptables", "-D", "OUTPUT", "-p", "tcp", "-d", ip,
            "--dport", "8883", "-j", "REJECT"]


def rule_present(ip):
    cmd = ["iptables", "-C", "OUTPUT", "-p", "tcp", "-d", ip,
           "--dport", "8883", "-j", "REJECT"]
    return subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


def block_mqtt(ip, events_path):
    if not rule_present(ip):
        subprocess.check_call(iptables_rule(ip))
    if not rule_present(ip):
        raise RuntimeError("iptables MQTT block was not installed")
    append_json(events_path, {"event": "outage_start", "utc": utc_now(), "broker_ipv4": ip,
                              "method": "iptables_OUTPUT_REJECT_tcp_8883"})


def unblock_mqtt(ip, events_path):
    if rule_present(ip):
        subprocess.check_call(iptables_delete_rule(ip))
    if rule_present(ip):
        raise RuntimeError("iptables MQTT block was not removed")
    append_json(events_path, {"event": "outage_end", "utc": utc_now(), "broker_ipv4": ip,
                              "method": "iptables_OUTPUT_REJECT_tcp_8883"})


def in_outage(sequence, condition):
    return condition != "C0_normal_no_restart" and 3001 <= sequence <= 5000


def load_state(path, args):
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    state = {
        "run_id": args.run_id,
        "architecture": args.architecture,
        "condition": args.condition,
        "last_sequence": 0,
        "restart_done": False,
        "outage_active": False,
        "broker_ipv4": broker_ipv4(args.broker),
        "boot_id": "BOOT-001",
        "queue_high_water": 0,
    }
    atomic_json(path, state)
    return state


def drain_queue(queue, args, events_path):
    while True:
        rows = queue.pending(args.batch_size)
        if not rows:
            return
        payloads = [r[2] for r in rows]
        if not mqtt_publish_lines(args, payloads, events_path):
            raise RuntimeError("MQTT batch publish failed while transport should be available")
        queue.mark_sent([r[0] for r in rows])


def should_checkpoint(seq, args):
    return seq % args.batch_size == 0 or seq in (3000, 3001, 4000, 5000, args.records)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run-id", required=True)
    p.add_argument("--architecture", required=True,
                   choices=["B0_publish_only_non_durable", "W1_wellpulse_offline_first"])
    p.add_argument("--condition", required=True,
                   choices=["C0_normal_no_restart", "C1_outage_no_restart", "C2_outage_with_restart"])
    p.add_argument("--records", type=int, default=10000)
    p.add_argument("--batch-size", type=int, default=100)
    p.add_argument("--broker", default="mqtt4.iot-lab.info")
    p.add_argument("--port", type=int, default=8883)
    p.add_argument("--topic", required=True)
    p.add_argument("--ca-file", required=True)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    if args.records != 10000:
        raise SystemExit("WP-RT01 final/dry-run adapter requires exactly 10000 records")

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir)
    state_path = os.path.join(args.out_dir, "controller_state.json")
    events_path = os.path.join(args.out_dir, "edge_events.ndjson")
    generated_path = os.path.join(args.out_dir, "generated_records.ndjson")
    dropped_path = os.path.join(args.out_dir, "baseline_dropped.ndjson")
    queue_path = os.path.join(args.out_dir, "queue.sqlite")
    summary_path = os.path.join(args.out_dir, "edge_summary.json")

    state = load_state(state_path, args)
    if state["run_id"] != args.run_id or state["architecture"] != args.architecture or state["condition"] != args.condition:
        raise SystemExit("Existing controller state does not match requested run")

    ip = state["broker_ipv4"]
    if state.get("outage_active") and not rule_present(ip):
        block_mqtt(ip, events_path)

    queue = DurableQueue(queue_path) if args.architecture == "W1_wellpulse_offline_first" else None
    b0_buffer = []
    if queue is not None:
        state["queue_high_water"] = max(int(state.get("queue_high_water", 0)), queue.pending_count())

    start_seq = int(state.get("last_sequence", 0)) + 1
    append_json(events_path, {"event": "process_start", "utc": utc_now(), "start_sequence": start_seq,
                              "restart_done": bool(state.get("restart_done"))})

    generated_fh = open(generated_path, "a", 1)
    dropped_fh = open(dropped_path, "a", 1) if args.architecture == "B0_publish_only_non_durable" else None

    try:
        for seq in range(start_seq, args.records + 1):
            if seq == 3001 and args.condition != "C0_normal_no_restart" and not state.get("outage_active"):
                block_mqtt(ip, events_path)
                state["outage_active"] = True
                atomic_json(state_path, state)

            body, payload_json, checksum = canonical_record(args.run_id, state["boot_id"], seq)
            write_json_line(generated_fh, {
                "record_id": body["record_id"],
                "sequence": seq,
                "generated_at_utc": body["generated_at_utc"],
                "checksum_sha256": checksum,
                "payload_json": payload_json,
            })

            if args.architecture == "W1_wellpulse_offline_first":
                queue.enqueue(body["record_id"], seq, payload_json, checksum)
                pending_now = queue.pending_count()
                if pending_now > int(state.get("queue_high_water", 0)):
                    state["queue_high_water"] = pending_now
                if not in_outage(seq, args.condition) and pending_now >= args.batch_size:
                    drain_queue(queue, args, events_path)
            else:
                if in_outage(seq, args.condition):
                    write_json_line(dropped_fh, {"record_id": body["record_id"], "sequence": seq,
                                                 "utc": utc_now(), "reason": "transport_blocked_no_durable_queue"})
                else:
                    b0_buffer.append(payload_json)
                    if len(b0_buffer) >= args.batch_size:
                        if not mqtt_publish_lines(args, b0_buffer, events_path):
                            raise RuntimeError("B0 MQTT publish failed outside outage")
                        b0_buffer = []

            state["last_sequence"] = seq
            if should_checkpoint(seq, args):
                atomic_json(state_path, state)

            if args.condition == "C2_outage_with_restart" and seq == 4000 and not state.get("restart_done"):
                state["restart_done"] = True
                atomic_json(state_path, state)
                generated_fh.flush()
                os.fsync(generated_fh.fileno())
                if dropped_fh is not None:
                    dropped_fh.flush()
                    os.fsync(dropped_fh.fileno())
                append_json(events_path, {"event": "gateway_restart_exec", "utc": utc_now(),
                                          "after_sequence": 4000})
                if queue is not None:
                    queue.close()
                generated_fh.close()
                if dropped_fh is not None:
                    dropped_fh.close()
                os.execv(sys.executable, [sys.executable] + sys.argv)

            if seq == 5000 and args.condition != "C0_normal_no_restart" and state.get("outage_active"):
                unblock_mqtt(ip, events_path)
                state["outage_active"] = False
                atomic_json(state_path, state)
                if queue is not None:
                    drain_queue(queue, args, events_path)

        if state.get("outage_active"):
            unblock_mqtt(ip, events_path)
            state["outage_active"] = False
            atomic_json(state_path, state)

        if queue is not None:
            drain_queue(queue, args, events_path)
        elif b0_buffer:
            if not mqtt_publish_lines(args, b0_buffer, events_path):
                raise RuntimeError("B0 final MQTT publish failed")
            b0_buffer = []

        generated_fh.flush()
        os.fsync(generated_fh.fileno())
        if dropped_fh is not None:
            dropped_fh.flush()
            os.fsync(dropped_fh.fileno())

        state["last_sequence"] = args.records
        atomic_json(state_path, state)
        summary = {
            "run_id": args.run_id,
            "architecture": args.architecture,
            "condition": args.condition,
            "generated": args.records,
            "last_sequence": state["last_sequence"],
            "restart_done": state.get("restart_done", False),
            "outage_method": "NONE" if args.condition == "C0_normal_no_restart" else "iptables_OUTPUT_REJECT_tcp_8883",
            "broker_ipv4": ip,
            "queue_total": queue.total_count() if queue is not None else 0,
            "queue_pending": queue.pending_count() if queue is not None else 0,
            "queue_high_water": int(state.get("queue_high_water", 0)),
            "completed_utc": utc_now(),
        }
        atomic_json(summary_path, summary)
        append_json(events_path, {"event": "process_complete", "utc": utc_now()})
        print(json.dumps(summary, sort_keys=True))
    finally:
        if not generated_fh.closed:
            generated_fh.close()
        if dropped_fh is not None and not dropped_fh.closed:
            dropped_fh.close()
        if queue is not None:
            try:
                queue.close()
            except Exception:
                pass
        if state.get("outage_active") and rule_present(ip):
            unblock_mqtt(ip, events_path)


if __name__ == "__main__":
    main()
