#!/usr/bin/env python3
"""Python-3.5-compatible FIT execution adapter for WP-RT01.

This adapter preserves the frozen WP-RT01 experiment semantics while avoiding
modern-Python-only syntax/dependencies on the FIT A8 image. It is not a second
scientific implementation: record identity, durable SQLite queue semantics,
condition windows, QoS1 MQTT delivery, and reconciliation inputs remain fixed.
"""
from __future__ import print_function

import argparse
import datetime
import hashlib
import json
import os
import socket
import sqlite3
import ssl
import subprocess
import sys
import time

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

BROKER = "mqtt4.iot-lab.info"
PORT = 8883
OUTAGE_START = 3001
OUTAGE_END = 5000
RESTART_AT = 4000


def utc_now():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def make_payload(run_id, boot_id, sequence):
    body = {
        "run_id": run_id,
        "boot_id": boot_id,
        "sequence": sequence,
        "generated_at_utc": utc_now(),
        "source": "synthetic_modbus_like",
        "payload": {"register_1": 1000 + sequence, "status": sequence % 4},
        "quality_flag": "OK",
    }
    record_id = "%s:%s:%08d" % (run_id, boot_id, sequence)
    body["record_id"] = record_id
    payload_json = json.dumps(body, sort_keys=True, separators=(",", ":"))
    checksum = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
    return record_id, payload_json, checksum


class DurableQueue(object):
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=FULL")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS queue ("
            "record_id TEXT PRIMARY KEY,"
            "payload_json TEXT NOT NULL,"
            "checksum_sha256 TEXT NOT NULL,"
            "state TEXT NOT NULL DEFAULT 'PENDING')"
        )
        self.conn.commit()

    def enqueue(self, record_id, payload_json, checksum):
        self.conn.execute(
            "INSERT OR IGNORE INTO queue(record_id,payload_json,checksum_sha256,state) "
            "VALUES(?,?,?,'PENDING')",
            (record_id, payload_json, checksum),
        )
        self.conn.commit()

    def pending_rows(self):
        return list(self.conn.execute(
            "SELECT record_id,payload_json,checksum_sha256,state FROM queue "
            "WHERE state='PENDING' ORDER BY record_id"
        ))

    def mark_sent(self, record_id, commit=True):
        self.conn.execute("UPDATE queue SET state='SENT' WHERE record_id=?", (record_id,))
        if commit:
            self.conn.commit()

    def commit_state(self):
        self.conn.commit()

    def count(self):
        return self.conn.execute("SELECT COUNT(*) FROM queue").fetchone()[0]

    def pending_count(self):
        return self.conn.execute("SELECT COUNT(*) FROM queue WHERE state='PENDING'").fetchone()[0]

    def close(self):
        self.conn.close()


class Publisher(object):
    def __init__(self, username, password, ca_file, client_id, log):
        if mqtt is None:
            raise RuntimeError("paho-mqtt is not available")
        self.log = log
        self.connected = False
        self.client = mqtt.Client(client_id=client_id, clean_session=True)
        self.client.username_pw_set(username, password)
        self.client.tls_set(ca_certs=ca_file, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        self.connected = (rc == 0)

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False

    def connect(self, timeout=10.0):
        started = time.time()
        self.client.connect(BROKER, PORT, keepalive=20)
        while not self.connected and (time.time() - started) < timeout:
            time.sleep(0.05)
        if not self.connected:
            raise RuntimeError("MQTT connect timeout")
        return time.time() - started

    def publish(self, topic, payload_json, timeout=5.0):
        info = self.client.publish(topic, payload_json, qos=1, retain=False)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            return False
        started = time.time()
        while not info.is_published() and (time.time() - started) < timeout:
            time.sleep(0.01)
        return info.is_published()

    def close(self):
        try:
            self.client.disconnect()
        except Exception:
            pass
        try:
            self.client.loop_stop()
        except Exception:
            pass
        self.connected = False


def run_cmd(args, log, check=True):
    log.write("CMD %s\n" % " ".join(args))
    log.flush()
    rc = subprocess.call(args)
    log.write("RC %d\n" % rc)
    log.flush()
    if check and rc != 0:
        raise RuntimeError("command failed: %s" % " ".join(args))
    return rc


def resolve_broker_ipv4():
    return socket.gethostbyname(BROKER)


def set_outage(broker_ip, enabled, log):
    rule = ["iptables", "-p", "tcp", "-d", broker_ip, "--dport", str(PORT), "-j", "REJECT"]
    if enabled:
        run_cmd(["iptables", "-I", "OUTPUT", "1"] + rule, log)
    else:
        run_cmd(["iptables", "-D", "OUTPUT"] + rule, log)


def assert_blocked(log):
    started = time.time()
    blocked = False
    try:
        sock = socket.create_connection((BROKER, PORT), 2.0)
        sock.close()
    except Exception:
        blocked = True
    elapsed = time.time() - started
    log.write("outage_socket_blocked=%s elapsed_s=%.6f\n" % ("PASS" if blocked else "FAIL", elapsed))
    log.flush()
    if not blocked:
        raise RuntimeError("iptables outage did not block broker TCP 8883")


def load_auth(path):
    with open(path, "r") as fh:
        data = json.load(fh)
    return data["username"], data["password"]


def write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, sort_keys=True, indent=2)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.rename(tmp, path)


def append_line(path, line):
    with open(path, "a") as fh:
        fh.write(line + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--architecture", choices=["B0", "W1"], required=True)
    parser.add_argument("--condition", choices=["C0", "C1", "C2"], required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--auth-file", required=True)
    parser.add_argument("--ca-file", required=True)
    parser.add_argument("--work-dir", required=True)
    parser.add_argument("--records", type=int, default=10000)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if args.records != 10000:
        raise SystemExit("WP-RT01 dry/final runner requires exactly 10000 records")

    if not os.path.isdir(args.work_dir):
        os.makedirs(args.work_dir)
    log_path = os.path.join(args.work_dir, "edge_events.log")
    generated_path = os.path.join(args.work_dir, "generated.jsonl")
    state_path = os.path.join(args.work_dir, "control_state.json")
    queue_path = os.path.join(args.work_dir, "queue.sqlite")
    metrics_path = os.path.join(args.work_dir, "edge_metrics.json")

    log = open(log_path, "a", 1)
    username, password = load_auth(args.auth_file)
    broker_ip = resolve_broker_ipv4()

    if args.resume:
        with open(state_path, "r") as fh:
            state = json.load(fh)
        start_seq = int(state["next_sequence"])
        boot_no = int(state["boot_no"]) + 1
        outage_active = bool(state["outage_active"])
        generated = int(state["generated"])
        published = int(state["published"])
        reconnect_s = state.get("reconnect_s")
        restart_count = int(state.get("restart_count", 0)) + 1
        log.write("resume_utc=%s next_sequence=%d boot_no=%d\n" % (utc_now(), start_seq, boot_no))
    else:
        start_seq = 1
        boot_no = 1
        outage_active = False
        generated = 0
        published = 0
        reconnect_s = None
        restart_count = 0
        for path in (generated_path, state_path, metrics_path):
            try:
                os.remove(path)
            except OSError:
                pass
        if args.architecture == "W1":
            try:
                os.remove(queue_path)
            except OSError:
                pass

    queue = DurableQueue(queue_path) if args.architecture == "W1" else None
    publisher = Publisher(username, password, args.ca_file,
                          "wp-%s-%d" % (args.run_id[-12:], boot_no), log)

    if not outage_active:
        connect_s = publisher.connect()
        log.write("mqtt_connect_utc=%s connect_s=%.6f\n" % (utc_now(), connect_s))
    else:
        log.write("resume_during_outage=YES\n")

    try:
        seq = start_seq
        while seq <= args.records:
            if args.condition in ("C1", "C2") and seq == OUTAGE_START and not outage_active:
                publisher.close()
                set_outage(broker_ip, True, log)
                outage_active = True
                log.write("outage_start_utc=%s sequence=%d broker_ip=%s\n" % (utc_now(), seq, broker_ip))
                assert_blocked(log)

            if args.condition in ("C1", "C2") and seq == OUTAGE_END + 1 and outage_active:
                set_outage(broker_ip, False, log)
                outage_active = False
                started = time.time()
                publisher = Publisher(username, password, args.ca_file,
                                      "wp-%s-%d-r" % (args.run_id[-10:], boot_no), log)
                publisher.connect()
                reconnect_s = time.time() - started
                log.write("outage_end_utc=%s sequence=%d reconnect_s=%.6f\n" %
                          (utc_now(), seq, reconnect_s))
                if queue is not None:
                    drain_started = time.time()
                    for row in queue.pending_rows():
                        if not publisher.publish(args.topic, row[1]):
                            raise RuntimeError("failed to drain queued record %s" % row[0])
                        queue.mark_sent(row[0], commit=False)
                        published += 1
                    queue.commit_state()
                    log.write("backlog_drain_s=%.6f\n" % (time.time() - drain_started))

            boot_id = "BOOT-%03d" % boot_no
            record_id, payload_json, checksum = make_payload(args.run_id, boot_id, seq)
            append_line(generated_path, payload_json)
            generated += 1

            if queue is not None:
                queue.enqueue(record_id, payload_json, checksum)
                if not outage_active:
                    if not publisher.publish(args.topic, payload_json):
                        raise RuntimeError("publish failed for %s" % record_id)
                    queue.mark_sent(record_id, commit=False)
                    published += 1
                    if seq % 100 == 0:
                        queue.commit_state()
            else:
                if not outage_active:
                    if not publisher.publish(args.topic, payload_json):
                        raise RuntimeError("baseline publish failed for %s" % record_id)
                    published += 1

            if args.condition == "C2" and seq == RESTART_AT and restart_count == 0:
                if queue is not None:
                    queue.commit_state()
                    queue.close()
                state = {
                    "next_sequence": seq + 1,
                    "boot_no": boot_no,
                    "outage_active": outage_active,
                    "generated": generated,
                    "published": published,
                    "reconnect_s": reconnect_s,
                    "restart_count": restart_count,
                }
                write_json(state_path, state)
                log.write("gateway_process_restart_utc=%s after_sequence=%d\n" % (utc_now(), seq))
                log.flush()
                publisher.close()
                os.execv(sys.executable, [sys.executable, os.path.abspath(__file__),
                    "--run-id", args.run_id,
                    "--architecture", args.architecture,
                    "--condition", args.condition,
                    "--topic", args.topic,
                    "--auth-file", args.auth_file,
                    "--ca-file", args.ca_file,
                    "--work-dir", args.work_dir,
                    "--records", str(args.records),
                    "--resume"])

            seq += 1

        if queue is not None:
            if queue.pending_count() != 0:
                raise RuntimeError("W1 finished with pending queue records")
            queue.commit_state()

        metrics = {
            "evidence_class": "PREFINAL_REAL_A8_DRY_RUN_NOT_FINAL_EXPERIMENT",
            "run_id": args.run_id,
            "architecture": args.architecture,
            "condition": args.condition,
            "records": args.records,
            "generated": generated,
            "published_qos1_acked": published,
            "queue_count": queue.count() if queue is not None else 0,
            "queue_pending": queue.pending_count() if queue is not None else 0,
            "restart_count": restart_count,
            "reconnect_s": reconnect_s,
            "outage_method": "iptables_REJECT_tcp_8883_records_3001_5000" if args.condition != "C0" else "none",
            "restart_definition": "WellPulse_gateway_process_exec_restart_after_record_4000" if args.condition == "C2" else "none",
            "completed_utc": utc_now(),
        }
        write_json(metrics_path, metrics)
        print(json.dumps(metrics, sort_keys=True))
    finally:
        try:
            publisher.close()
        except Exception:
            pass
        if outage_active:
            try:
                set_outage(broker_ip, False, log)
            except Exception:
                pass
        if queue is not None:
            try:
                queue.close()
            except Exception:
                pass
        log.close()


if __name__ == "__main__":
    main()
