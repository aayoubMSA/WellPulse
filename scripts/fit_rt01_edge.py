#!/usr/bin/env python3
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

OUTAGE_START = 3001
OUTAGE_END = 5000
RESTART_AT = 4000


def utc_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"


def append_json(path, obj):
    with open(path, "a") as fh:
        fh.write(json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n")
        fh.flush()


def log_event(path, event, **extra):
    row = {"event": event, "utc": utc_iso(), "epoch": time.time()}
    row.update(extra)
    append_json(path, row)


def make_wire_record(run_id, boot_id, sequence):
    body = {
        "run_id": run_id,
        "boot_id": boot_id,
        "sequence": sequence,
        "record_id": "%s:%s:%08d" % (run_id, boot_id, sequence),
        "generated_at_utc": utc_iso(),
        "generated_at_epoch": time.time(),
        "source": "synthetic_modbus_like",
        "payload": {"register_1": 1000 + sequence, "status": sequence % 4},
        "quality_flag": "OK",
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    body["checksum_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return json.dumps(body, sort_keys=True, separators=(",", ":"))


class DurableQueue(object):
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=DELETE")
        self.conn.execute("PRAGMA synchronous=FULL")
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS queue (
                record_id TEXT PRIMARY KEY,
                wire_json TEXT NOT NULL,
                checksum_sha256 TEXT NOT NULL,
                state TEXT NOT NULL DEFAULT 'PENDING'
            )"""
        )
        self.conn.commit()

    def enqueue_wire(self, wire_json):
        obj = json.loads(wire_json)
        self.conn.execute(
            "INSERT OR IGNORE INTO queue(record_id,wire_json,checksum_sha256,state) VALUES(?,?,?,'PENDING')",
            (obj["record_id"], wire_json, obj["checksum_sha256"]),
        )
        self.conn.commit()

    def pending_batch(self, limit):
        return list(
            self.conn.execute(
                "SELECT record_id,wire_json FROM queue WHERE state='PENDING' ORDER BY rowid LIMIT ?",
                (limit,),
            )
        )

    def mark_sent(self, record_ids):
        self.conn.executemany(
            "UPDATE queue SET state='SENT' WHERE record_id=?",
            [(record_id,) for record_id in record_ids],
        )
        self.conn.commit()

    def counts(self):
        total = self.conn.execute("SELECT COUNT(*) FROM queue").fetchone()[0]
        pending = self.conn.execute(
            "SELECT COUNT(*) FROM queue WHERE state='PENDING'"
        ).fetchone()[0]
        return total, pending

    def close(self):
        self.conn.close()


def decode(data):
    if not data:
        return ""
    try:
        return data.decode("utf-8", "replace")
    except AttributeError:
        return str(data)


def publish_lines(messages, broker, port, topic, ca_path):
    if not messages:
        return 0, ""
    cmd = [
        "mosquitto_pub",
        "--cafile",
        ca_path,
        "-h",
        broker,
        "-p",
        str(port),
        "-q",
        "1",
        "-t",
        topic,
        "-l",
    ]
    proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    payload = ("\n".join(messages) + "\n").encode("utf-8")
    out, err = proc.communicate(payload)
    return proc.returncode, decode(err) + decode(out)


def rule_args(broker_ip, port):
    return [
        "-p",
        "tcp",
        "-d",
        broker_ip,
        "--dport",
        str(port),
        "-j",
        "REJECT",
    ]


def remove_outage_rule(broker_ip, port):
    args = rule_args(broker_ip, port)
    removed = 0
    while True:
        rc = subprocess.call(
            ["iptables", "-D", "OUTPUT"] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if rc != 0:
            break
        removed += 1
    return removed


def enable_outage_rule(broker_ip, port):
    remove_outage_rule(broker_ip, port)
    rc = subprocess.call(
        ["iptables", "-I", "OUTPUT", "1"] + rule_args(broker_ip, port),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if rc != 0:
        raise RuntimeError("failed to install deterministic outage rule")


def probe_transport(broker, port, topic, ca_path, expect_up):
    msg = json.dumps(
        {"probe": "WP_RT01_TRANSPORT_PROBE", "epoch": time.time()},
        sort_keys=True,
        separators=(",", ":"),
    )
    rc, text = publish_lines([msg], broker, port, topic, ca_path)
    ok = rc == 0
    if ok != expect_up:
        raise RuntimeError(
            "transport probe mismatch expect_up=%s rc=%s detail=%s"
            % (expect_up, rc, text[-400:])
        )
    return rc, text


def drain_queue(queue, batch_size, broker, port, topic, ca_path, events_path):
    delivered = 0
    while True:
        rows = queue.pending_batch(batch_size)
        if not rows:
            break
        ids = [row[0] for row in rows]
        messages = [row[1] for row in rows]
        started = time.time()
        rc, text = publish_lines(messages, broker, port, topic, ca_path)
        log_event(
            events_path,
            "publish_batch",
            count=len(messages),
            rc=rc,
            duration_s=time.time() - started,
        )
        if rc != 0:
            raise RuntimeError("unexpected MQTT publish failure: %s" % text[-500:])
        queue.mark_sent(ids)
        delivered += len(ids)
    return delivered


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--architecture", choices=["B0_publish_only", "W1_offline_first"], required=True)
    ap.add_argument(
        "--condition",
        choices=["C0_normal_no_restart", "C1_outage_no_restart", "C2_outage_restart"],
        required=True,
    )
    ap.add_argument("--start-seq", type=int, required=True)
    ap.add_argument("--end-seq", type=int, required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--probe-topic", required=True)
    ap.add_argument("--broker", default="mqtt4.iot-lab.info")
    ap.add_argument("--port", type=int, default=8883)
    ap.add_argument("--ca", required=True)
    ap.add_argument("--batch-size", type=int, default=50)
    ap.add_argument("--leave-outage-active", action="store_true")
    args = ap.parse_args()

    if args.start_seq < 1 or args.end_seq > 10000 or args.start_seq > args.end_seq:
        raise SystemExit("invalid sequence range")
    if args.condition != "C2_outage_restart" and args.start_seq != 1:
        raise SystemExit("only C2 may resume from a later sequence")
    if args.condition == "C2_outage_restart" and args.start_seq not in (1, RESTART_AT + 1):
        raise SystemExit("C2 segment must start at 1 or 4001")

    if not os.path.isdir(args.workdir):
        os.makedirs(args.workdir)

    generated_path = os.path.join(args.workdir, "generated.jsonl")
    events_path = os.path.join(args.workdir, "edge_events.jsonl")
    queue_path = os.path.join(args.workdir, "queue.sqlite")
    segment_summary = os.path.join(
        args.workdir, "segment_%05d_%05d_summary.json" % (args.start_seq, args.end_seq)
    )

    broker_ip = socket.gethostbyname(args.broker)
    queue = None
    if args.architecture == "W1_offline_first":
        queue = DurableQueue(queue_path)

    boot_id = "BOOT-002" if (
        args.condition == "C2_outage_restart" and args.start_seq > RESTART_AT
    ) else "BOOT-001"

    transport_up = True
    reconnect_s = None
    backlog_drain_s = None
    baseline_dropped = 0
    published_current = 0
    batch = []

    log_event(
        events_path,
        "segment_start",
        run_id=args.run_id,
        architecture=args.architecture,
        condition=args.condition,
        start_seq=args.start_seq,
        end_seq=args.end_seq,
        boot_id=boot_id,
        broker_ip=broker_ip,
        batch_size=args.batch_size,
    )

    try:
        if args.start_seq == 1:
            remove_outage_rule(broker_ip, args.port)
        elif args.condition == "C2_outage_restart":
            transport_up = False
            probe_transport(
                args.broker, args.port, args.probe_topic, args.ca, expect_up=False
            )
            log_event(events_path, "restart_entry_outage_verified", sequence=args.start_seq)

        for seq in range(args.start_seq, args.end_seq + 1):
            if (
                args.condition in ("C1_outage_no_restart", "C2_outage_restart")
                and seq == OUTAGE_START
            ):
                if batch:
                    if args.architecture == "B0_publish_only":
                        rc, text = publish_lines(
                            batch, args.broker, args.port, args.topic, args.ca
                        )
                        if rc != 0:
                            raise RuntimeError("pre-outage publish failed: %s" % text[-500:])
                        published_current += len(batch)
                    else:
                        drain_queue(
                            queue,
                            args.batch_size,
                            args.broker,
                            args.port,
                            args.topic,
                            args.ca,
                            events_path,
                        )
                    batch = []
                enable_outage_rule(broker_ip, args.port)
                transport_up = False
                probe_transport(
                    args.broker, args.port, args.probe_topic, args.ca, expect_up=False
                )
                log_event(events_path, "outage_on", sequence=seq)

            if (
                args.condition in ("C1_outage_no_restart", "C2_outage_restart")
                and seq == OUTAGE_END + 1
            ):
                recovery_started = time.time()
                remove_outage_rule(broker_ip, args.port)
                deadline = time.time() + 15.0
                while True:
                    rc, text = publish_lines(
                        [
                            json.dumps(
                                {"probe": "WP_RT01_RECOVERY", "epoch": time.time()},
                                sort_keys=True,
                                separators=(",", ":"),
                            )
                        ],
                        args.broker,
                        args.port,
                        args.probe_topic,
                        args.ca,
                    )
                    if rc == 0:
                        break
                    if time.time() >= deadline:
                        raise RuntimeError("transport did not recover: %s" % text[-500:])
                    time.sleep(0.25)
                reconnect_s = time.time() - recovery_started
                transport_up = True
                log_event(
                    events_path, "outage_off", sequence=seq, reconnect_s=reconnect_s
                )
                if queue is not None:
                    drain_started = time.time()
                    drain_queue(
                        queue,
                        args.batch_size,
                        args.broker,
                        args.port,
                        args.topic,
                        args.ca,
                        events_path,
                    )
                    backlog_drain_s = time.time() - drain_started
                    log_event(
                        events_path,
                        "backlog_drained",
                        sequence=seq,
                        backlog_drain_s=backlog_drain_s,
                    )

            wire = make_wire_record(args.run_id, boot_id, seq)
            append_json(generated_path, json.loads(wire))

            if queue is not None:
                queue.enqueue_wire(wire)
            elif not transport_up:
                baseline_dropped += 1

            batch.append(wire)
            if len(batch) >= args.batch_size:
                if transport_up:
                    if queue is not None:
                        drain_queue(
                            queue,
                            args.batch_size,
                            args.broker,
                            args.port,
                            args.topic,
                            args.ca,
                            events_path,
                        )
                    else:
                        started = time.time()
                        rc, text = publish_lines(
                            batch, args.broker, args.port, args.topic, args.ca
                        )
                        log_event(
                            events_path,
                            "publish_batch",
                            count=len(batch),
                            rc=rc,
                            duration_s=time.time() - started,
                        )
                        if rc != 0:
                            raise RuntimeError(
                                "unexpected baseline MQTT publish failure: %s"
                                % text[-500:]
                            )
                        published_current += len(batch)
                batch = []

        if batch:
            if transport_up:
                if queue is not None:
                    drain_queue(
                        queue,
                        args.batch_size,
                        args.broker,
                        args.port,
                        args.topic,
                        args.ca,
                        events_path,
                    )
                else:
                    rc, text = publish_lines(
                        batch, args.broker, args.port, args.topic, args.ca
                    )
                    if rc != 0:
                        raise RuntimeError(
                            "unexpected final baseline MQTT publish failure: %s"
                            % text[-500:]
                        )
                    published_current += len(batch)
            batch = []

        if (
            args.condition == "C2_outage_restart"
            and args.end_seq == RESTART_AT
            and args.leave_outage_active
        ):
            log_event(events_path, "restart_exit", sequence=RESTART_AT)
        else:
            if queue is not None and transport_up:
                drain_queue(
                    queue,
                    args.batch_size,
                    args.broker,
                    args.port,
                    args.topic,
                    args.ca,
                    events_path,
                )
            remove_outage_rule(broker_ip, args.port)

        total_committed = 0
        pending_final = 0
        if queue is not None:
            total_committed, pending_final = queue.counts()

        summary = {
            "run_id": args.run_id,
            "architecture": args.architecture,
            "condition": args.condition,
            "start_seq": args.start_seq,
            "end_seq": args.end_seq,
            "boot_id": boot_id,
            "baseline_dropped_segment": baseline_dropped,
            "baseline_published_segment": published_current,
            "local_committed": total_committed,
            "pending_final": pending_final,
            "reconnect_s": reconnect_s,
            "backlog_drain_s": backlog_drain_s,
            "finished_utc": utc_iso(),
        }
        with open(segment_summary, "w") as fh:
            json.dump(summary, fh, indent=2, sort_keys=True)
            fh.write("\n")
        log_event(events_path, "segment_complete", **summary)
        return 0
    except Exception as exc:
        log_event(events_path, "segment_error", error=str(exc))
        if not args.leave_outage_active:
            remove_outage_rule(broker_ip, args.port)
        raise
    finally:
        if queue is not None:
            queue.close()


if __name__ == "__main__":
    sys.exit(main())
