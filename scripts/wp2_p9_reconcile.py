#!/usr/bin/env python3
"""WP2-P9 offline forensic reconstruction helper.

Reads extracted immutable P8 archives only. It contains no POWDER, SSH, RF,
service-control, or live-testbed logic.
"""
from pathlib import Path
from datetime import datetime
import re


def parse_ping(path):
    text = Path(path).read_text(errors="replace")
    m = re.search(r"(\d+) packets transmitted, (\d+) received, ([\d.]+)% packet loss", text)
    if not m:
        raise ValueError(f"no ping summary: {path}")
    return {"tx": int(m.group(1)), "rx": int(m.group(2)), "loss_pct": float(m.group(3))}


def parse_kv_log(path):
    rows = []
    for line in Path(path).read_text(errors="replace").splitlines():
        row = {k.lower(): v for k, v in re.findall(r"([A-Za-z_]+)=([^\s]+)", line)}
        if row:
            rows.append(row)
    return rows


def sequence_reconcile(sent_rows, received_rows):
    sent = [r["seq"] for r in sent_rows if "seq" in r]
    received = [r["seq"] for r in received_rows if "seq" in r]
    return {
        "sent_rows": len(sent),
        "sent_unique": len(set(sent)),
        "received_rows": len(received),
        "received_unique": len(set(received)),
        "missing": sorted(set(sent) - set(received), key=lambda x: int(x)),
        "received_duplicates": len(received) - len(set(received)),
    }


def seconds_between(a, b):
    parse = lambda x: datetime.fromisoformat(x.replace("Z", "+00:00"))
    return (parse(b) - parse(a)).total_seconds()
