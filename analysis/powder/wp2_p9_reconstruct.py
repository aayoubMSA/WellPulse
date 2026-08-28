#!/usr/bin/env python3
"""WP2-P9 raw-evidence reconstruction helpers.

Offline only. This script never contacts POWDER and never mutates raw evidence.
It parses frozen extracted raw logs and emits metrics from raw content.
"""
from pathlib import Path
import re, json

PING_TXRX = re.compile(r"(\d+) packets transmitted,\s*(\d+) received")
PING_LOSS = re.compile(r"([\d.]+)% packet loss")
PING_RTT = re.compile(r"=\s*[\d.]+/([\d.]+)/")


def parse_ping(path):
    text = Path(path).read_text(errors="replace")
    txrx = PING_TXRX.search(text)
    loss = PING_LOSS.search(text)
    rtt = PING_RTT.search(text)
    if not txrx or not loss:
        raise ValueError(f"unparseable ping summary: {path}")
    return {
        "tx": int(txrx.group(1)),
        "rx": int(txrx.group(2)),
        "loss_pct": float(loss.group(1)),
        "rtt_avg_ms": float(rtt.group(1)) if rtt else None,
    }


SEQ_PATTERNS = [
    re.compile(r"(?:seq|sequence)[= :]+(\d+)", re.I),
    re.compile(r'"seq"\s*:\s*(\d+)', re.I),
]


def unique_sequences(path):
    vals = []
    for line in Path(path).read_text(errors="replace").splitlines():
        found = None
        for pattern in SEQ_PATTERNS:
            match = pattern.search(line)
            if match:
                found = int(match.group(1))
                break
        if found is not None:
            vals.append(found)
    return vals, sorted(set(vals))


def mqtt_reconcile(sent_path, received_path):
    sent_lines, sent_unique = unique_sequences(sent_path)
    recv_lines, recv_unique = unique_sequences(received_path)
    sent = set(sent_unique)
    received = set(recv_unique)
    return {
        "sent_lines_with_seq": len(sent_lines),
        "sent_unique": len(sent),
        "received_lines_with_seq": len(recv_lines),
        "received_unique": len(received),
        "missing_ids": sorted(sent - received),
        "unexpected_received_ids": sorted(received - sent),
        "completeness_pct": (100.0 * len(received & sent) / len(sent)) if sent else None,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    ping = sub.add_parser("ping")
    ping.add_argument("path")
    mqtt = sub.add_parser("mqtt")
    mqtt.add_argument("sent")
    mqtt.add_argument("received")
    args = parser.parse_args()
    result = parse_ping(args.path) if args.cmd == "ping" else mqtt_reconcile(args.sent, args.received)
    print(json.dumps(result, indent=2))
