#!/usr/bin/env python3
"""Offline, read-only reconstruction of the WP2 H1 sender-side evidence.

This tool is part of the WP2 Recovery-Semantics Amendment Consortium RS-1 gate.
It does not issue RF, LTE, MQTT, or other live testbed commands. It reads only
preserved H1 artifacts and emits a deterministic text reconstruction plus its
SHA-256 digest.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

TARGETS = [
    "sender_summary.json",
    "calibration_manifest.json",
    "attenuation_timeline.csv",
    "telemetry_generated.csv",
    "queue_timeline.csv",
    "mqtt_events.jsonl",
    "w1_queue.sqlite",
]


def progress(p: int, text: str) -> None:
    n = p // 5
    print(
        "\r[" + "#" * n + "-" * (20 - n) + f"] {p:3d}%  {text:<48}",
        end="",
        flush=True,
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_utc(value: object) -> datetime | None:
    if value is None or value == "":
        return None
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError(f"timestamp lacks timezone: {value}")
    return dt.astimezone(timezone.utc)


def find_one(root: Path, name: str) -> Path | None:
    matches = list(root.rglob(name))
    if not matches:
        return None
    matches.sort(key=lambda p: (len(str(p)), str(p)))
    return matches[0]


def nearest(rows: list[dict], target: datetime | None, ts_key: str = "utc"):
    if target is None or not rows:
        return None
    candidates = []
    for row in rows:
        try:
            ts = parse_utc(row[ts_key])
            if ts is not None:
                candidates.append((abs((ts - target).total_seconds()), ts, row))
        except Exception:
            pass
    return min(candidates, key=lambda item: item[0]) if candidates else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only RS-1A reconstruction of preserved H1 sender evidence"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=(
            Path.home()
            / "wellpulse-powder-evidence"
            / "wp2-h1-valid-failure-20260826"
            / "nuc2"
        ),
        help="Root directory containing the preserved H1 nuc2 evidence",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=(
            Path.home()
            / "wellpulse-powder-evidence"
            / "wp2-rs1-reconstruction-20260826"
        ),
        help="Directory for the reconstruction artifact",
    )
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    outdir = args.output_dir.expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "RS1A_sender_reconstruction_nuc2.txt"

    lines: list[str] = []

    def emit(value: object = "") -> None:
        text = str(value)
        lines.append(text)
        print(text)

    progress(5, "Locating preserved H1 sender artifacts")
    print()

    paths = {name: find_one(root, name) for name in TARGETS}
    missing = [name for name, path in paths.items() if path is None]
    if missing:
        print("RS1A=BLOCKED")
        print("MISSING=" + ",".join(missing))
        return 20

    typed_paths = {name: path for name, path in paths.items() if path is not None}

    emit("=== RS-1A H1 SENDER-SIDE RAW RECONSTRUCTION ===")
    emit(f"ROOT={root}")
    emit("EVIDENCE_CLASS=POST_H1_OFFLINE_RECONSTRUCTION")
    emit("H1_CLASSIFICATION=VALID_W1_RECOVERY_FAILURE")
    emit("H=UNFROZEN")
    emit("SCORED_RUNS_AUTHORIZED=false")
    emit()

    progress(12, "Hashing admitted raw artifacts")
    print()
    emit("=== RAW ARTIFACT INTEGRITY ===")
    for name in TARGETS:
        path = typed_paths[name]
        emit(
            f"{name}\tSIZE={path.stat().st_size}\tSHA256={sha256(path)}\tPATH={path}"
        )
    emit()

    progress(22, "Reading sender summary and RF timestamps")
    print()
    summary = json.loads(typed_paths["sender_summary.json"].read_text(encoding="utf-8"))
    _manifest = json.loads(
        typed_paths["calibration_manifest.json"].read_text(encoding="utf-8")
    )

    q3 = parse_utc(summary.get("q3_effective_utc"))
    q0 = parse_utc(summary.get("cohort_cutoff_utc"))

    emit("=== T1 CORE EVENT TIMELINE — SENDER ===")
    emit(f"RUN_ID={summary.get('run_id')}")
    emit(f"MQTT_CLIENT_ID={summary.get('mqtt_client_id')}")
    emit(f"MQTT_TOPIC={summary.get('mqtt_topic')}")
    emit(f"INITIAL_SESSION_PRESENT={summary.get('initial_session_present')}")
    emit(f"Q3_EFFECTIVE_UTC={summary.get('q3_effective_utc')}")
    emit(f"Q3_FULL_STATE_DURATION_S={summary.get('q3_full_state_duration_s')}")
    emit(f"T_RF_RESTORE={summary.get('cohort_cutoff_utc')}")
    emit(f"QUEUE_PENDING_ZERO_UTC={summary.get('queue_pending_zero_utc')}")
    emit(f"STATUS={summary.get('status')}")
    emit(f"WORKER_ERROR={summary.get('worker_error')}")
    emit(f"RF_ERROR={summary.get('rf_error')}")
    emit()

    progress(32, "Reconstructing attenuation schedule")
    print()
    with typed_paths["attenuation_timeline.csv"].open(newline="", encoding="utf-8") as fh:
        attenuation_rows = list(csv.DictReader(fh))

    emit("=== RF COMMAND TIMELINE ===")
    for index, row in enumerate(attenuation_rows, 1):
        emit(
            f"RF{index}: start={row.get('command_start_utc')} "
            f"end={row.get('command_end_utc')} "
            f"db={row.get('programmed_attenuation_db')} "
            f"ids={row.get('attenuator_ids')}"
        )
    emit()

    progress(43, "Reconstructing generated-record ledger")
    print()
    with typed_paths["telemetry_generated.csv"].open(newline="", encoding="utf-8") as fh:
        generated = list(csv.DictReader(fh))

    ids = [row["record_id"] for row in generated]
    id_counts = Counter(ids)
    duplicates = sorted(record_id for record_id, count in id_counts.items() if count > 1)
    generated_times = [
        parse_utc(row["generated_ts_utc"])
        for row in generated
        if row.get("generated_ts_utc")
    ]
    generated_times = [value for value in generated_times if value is not None]
    cutoff_generated = (
        [
            row
            for row in generated
            if (parse_utc(row["generated_ts_utc"]) or datetime.max.replace(tzinfo=timezone.utc))
            <= q0
        ]
        if q0 is not None
        else []
    )

    emit("=== T2 GENERATED RECORD RECONCILIATION — SENDER ===")
    emit(f"GENERATED_ROWS={len(generated)}")
    emit(f"GENERATED_UNIQUE_IDS={len(set(ids))}")
    emit(f"GENERATED_DUPLICATE_ID_COUNT={len(duplicates)}")
    emit(f"GENERATED_FIRST_UTC={min(generated_times).isoformat() if generated_times else None}")
    emit(f"GENERATED_LAST_UTC={max(generated_times).isoformat() if generated_times else None}")
    emit(f"COHORT_GENERATED_AT_OR_BEFORE_RF_RESTORE={len(cutoff_generated)}")
    emit(f"SUMMARY_COHORT_RECORD_COUNT={summary.get('cohort_record_count')}")
    emit()

    progress(55, "Reconstructing queue trajectory")
    print()
    with typed_paths["queue_timeline.csv"].open(newline="", encoding="utf-8") as fh:
        queue_rows = list(csv.DictReader(fh))

    for row in queue_rows:
        for key in (
            "pending_count",
            "app_inflight_count",
            "published_calls",
            "puback_callbacks",
        ):
            try:
                row[key] = int(row[key])
            except Exception:
                pass
        row["connected_norm"] = str(row.get("connected", "")).lower() in (
            "true",
            "1",
            "yes",
        )

    max_pending = max(queue_rows, key=lambda row: row["pending_count"]) if queue_rows else None
    near_q3 = nearest(queue_rows, q3)
    near_q0 = nearest(queue_rows, q0)

    first_disconnected_after_q3 = None
    if q3 is not None:
        for row in queue_rows:
            try:
                row_time = parse_utc(row["utc"])
                if row_time is not None and row_time >= q3 and not row["connected_norm"]:
                    first_disconnected_after_q3 = row
                    break
            except Exception:
                pass

    emit("=== T3 QUEUE / MQTT STATE ===")
    emit(f"QUEUE_TIMELINE_ROWS={len(queue_rows)}")

    if queue_rows:
        row = queue_rows[0]
        emit(
            "QUEUE_FIRST="
            f"utc={row['utc']} connected={row['connected']} "
            f"pending={row['pending_count']} inflight={row['app_inflight_count']} "
            f"published={row['published_calls']} puback={row['puback_callbacks']}"
        )

    if near_q3:
        delta, _time, row = near_q3
        emit(
            "QUEUE_NEAREST_Q3="
            f"utc={row['utc']} delta_s={delta:.3f} connected={row['connected']} "
            f"pending={row['pending_count']} inflight={row['app_inflight_count']} "
            f"published={row['published_calls']} puback={row['puback_callbacks']}"
        )

    if first_disconnected_after_q3:
        row = first_disconnected_after_q3
        emit(
            "FIRST_DISCONNECTED_SAMPLE_AFTER_Q3="
            f"utc={row['utc']} pending={row['pending_count']} "
            f"inflight={row['app_inflight_count']}"
        )

    if near_q0:
        delta, _time, row = near_q0
        emit(
            "QUEUE_NEAREST_RF_RESTORE="
            f"utc={row['utc']} delta_s={delta:.3f} connected={row['connected']} "
            f"pending={row['pending_count']} inflight={row['app_inflight_count']} "
            f"published={row['published_calls']} puback={row['puback_callbacks']}"
        )

    if max_pending:
        emit(
            "QUEUE_PEAK="
            f"utc={max_pending['utc']} pending={max_pending['pending_count']} "
            f"connected={max_pending['connected']}"
        )

    if queue_rows:
        row = queue_rows[-1]
        emit(
            "QUEUE_FINAL="
            f"utc={row['utc']} connected={row['connected']} "
            f"pending={row['pending_count']} inflight={row['app_inflight_count']} "
            f"published={row['published_calls']} puback={row['puback_callbacks']}"
        )
    emit()

    progress(68, "Reading MQTT event transitions")
    print()
    events = []
    with typed_paths["mqtt_events.jsonl"].open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except Exception:
                pass

    event_counts = Counter(str(event.get("event")) for event in events)
    emit("=== MQTT EVENT COUNTS ===")
    for name in sorted(event_counts):
        emit(f"{name}={event_counts[name]}")

    emit()
    emit("=== MQTT TRANSITION TIMELINE ===")
    for event in events:
        name = str(event.get("event", ""))
        if "message" not in name.lower() and "payload" not in name.lower():
            safe = {
                key: value
                for key, value in event.items()
                if key not in ("payload", "payload_json", "raw", "body")
            }
            emit(json.dumps(safe, sort_keys=True, separators=(",", ":")))
    emit()

    progress(80, "Auditing final durable SQLite state")
    print()
    db_uri = f"file:{typed_paths['w1_queue.sqlite']}?mode=ro"
    connection = sqlite3.connect(db_uri, uri=True)
    try:
        tables = [
            row[0]
            for row in connection.execute(
                "select name from sqlite_master where type='table' order by name"
            )
        ]
        emit("=== SQLITE DURABLE QUEUE ===")
        emit("TABLES=" + ",".join(tables))

        if "queue" in tables:
            total = connection.execute("select count(*) from queue").fetchone()[0]
            states = list(
                connection.execute(
                    "select state,count(*) from queue group by state order by state"
                )
            )
            unique_ids = connection.execute(
                "select count(distinct record_id) from queue"
            ).fetchone()[0]
            distinct_checksums = connection.execute(
                "select count(distinct checksum_sha256) from queue"
            ).fetchone()[0]

            emit(f"SQLITE_QUEUE_ROWS={total}")
            emit(f"SQLITE_UNIQUE_RECORD_IDS={unique_ids}")
            emit(f"SQLITE_DISTINCT_CHECKSUMS={distinct_checksums}")
            for state, count in states:
                emit(f"SQLITE_STATE_{state}={count}")
    finally:
        connection.close()
    emit()

    progress(90, "Cross-checking sender-summary consistency")
    print()
    snapshot = summary.get("final_replay_snapshot") or {}
    emit("=== SUMMARY FINAL SNAPSHOT ===")
    for key in (
        "connected",
        "pending_count",
        "app_inflight_count",
        "published_calls",
        "puback_callbacks",
    ):
        emit(f"SUMMARY_FINAL_{key.upper()}={snapshot.get(key)}")

    emit(f"SUMMARY_GENERATED_RECORD_COUNT={summary.get('generated_record_count')}")
    emit(f"SUMMARY_GENERATION_MAX_LAG_S={summary.get('generation_max_lag_s')}")
    emit()

    progress(96, "Freezing RS-1A reconstruction artifact")
    print()
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    digest = sha256(out)
    digest_path = Path(str(out) + ".sha256")
    digest_path.write_text(f"{digest}  {out}\n", encoding="utf-8")

    progress(100, "RS-1A sender reconstruction complete")
    print()
    print()
    print(f"RS1A_OUTPUT={out}")
    print(f"RS1A_SHA256={digest}")
    print("RS1A_SENDER_RECONSTRUCTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
