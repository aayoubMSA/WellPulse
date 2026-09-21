#!/usr/bin/env python3
"""Deterministic per-run adjudicator for WellPulse R5 Stage A.

Authority:
- R4 Amendment A1: primary object is semantic endpoint misclassification.
- R5a Amendment A2: a same-receiver causal witness may establish M3 > M2
  without cross-host timestamp subtraction when a post-M2 live record is
  received before at least one historical-backlog record.

This script performs no experiment. It only adjudicates one frozen scored T1
evidence package.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

H_FIRST = 3001
H_LAST = 5000
LIVE_WITNESS_SEQ = 5001
EXPECTED_RECORDS = 10000
EXPECTED_H = H_LAST - H_FIRST + 1
CENSOR_S = 300.0


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_ndjson(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as exc:
                raise RuntimeError(f"{path}:{lineno}: invalid JSON: {exc}")
    return rows


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_generated(path: Path, run_id: str) -> tuple[dict[str, dict[str, Any]], dict[int, str], list[str]]:
    by_id: dict[str, dict[str, Any]] = {}
    by_seq: dict[int, str] = {}
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            wire = line.rstrip("\r\n")
            if not wire:
                continue
            try:
                obj = json.loads(wire)
            except Exception as exc:
                errors.append(f"generated_line_{lineno}_json:{exc}")
                continue
            if obj.get("run_id") != run_id:
                errors.append(f"generated_line_{lineno}_foreign_run")
                continue
            rid = obj.get("record_id")
            seq = obj.get("sequence")
            if not isinstance(rid, str) or not isinstance(seq, int):
                errors.append(f"generated_line_{lineno}_identity")
                continue
            if rid in by_id:
                errors.append(f"duplicate_generated_record_id:{rid}")
                continue
            if seq in by_seq:
                errors.append(f"duplicate_generated_sequence:{seq}")
                continue
            by_id[rid] = {
                "record_id": rid,
                "sequence": seq,
                "wire": wire,
                "wire_sha256": sha256_text(wire),
            }
            by_seq[seq] = rid
    return by_id, by_seq, errors


def load_receiver(path: Path, run_id: str) -> dict[str, Any]:
    first_by_id: dict[str, dict[str, Any]] = {}
    arrivals: list[dict[str, Any]] = []
    parse_errors: list[str] = []
    foreign = 0
    duplicates = 0
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        arrival_index = 0
        for lineno, line in enumerate(fh, 1):
            line = line.rstrip("\r\n")
            if not line:
                continue
            if "\t" not in line:
                parse_errors.append(f"receiver_line_{lineno}_missing_tab")
                continue
            ts_text, wire = line.split("\t", 1)
            try:
                ts = float(ts_text)
                obj = json.loads(wire)
            except Exception as exc:
                parse_errors.append(f"receiver_line_{lineno}_parse:{exc}")
                continue
            if obj.get("run_id") != run_id:
                foreign += 1
                continue
            rid = obj.get("record_id")
            seq = obj.get("sequence")
            if not isinstance(rid, str) or not isinstance(seq, int):
                parse_errors.append(f"receiver_line_{lineno}_identity")
                continue
            arrival_index += 1
            row = {
                "arrival_index": arrival_index,
                "record_id": rid,
                "sequence": seq,
                "receive_epoch_s": ts,
                "wire": wire,
                "wire_sha256": sha256_text(wire),
            }
            arrivals.append(row)
            if rid in first_by_id:
                duplicates += 1
            else:
                first_by_id[rid] = row
    return {
        "first_by_id": first_by_id,
        "arrivals": arrivals,
        "parse_errors": parse_errors,
        "foreign": foreign,
        "duplicates": duplicates,
    }


def best_offset_interval(clock: dict[str, Any], host: str) -> tuple[float, float]:
    best = clock[host]["best"]
    est = float(best["offset_remote_minus_controller_s"])
    bound = float(best["midpoint_bound_s"])
    return est - bound, est + bound


def host_hull(pre: dict[str, Any], post: dict[str, Any], host: str) -> tuple[float, float]:
    p0 = best_offset_interval(pre, host)
    p1 = best_offset_interval(post, host)
    return min(p0[0], p1[0]), max(p0[1], p1[1])


def relative_receiver_minus_source_interval(
    pre: dict[str, Any], post: dict[str, Any]
) -> tuple[float, float]:
    s_lo, s_hi = host_hull(pre, post, "source")
    r_lo, r_hi = host_hull(pre, post, "receiver")
    return r_lo - s_hi, r_hi - s_lo


def first_after(rows: list[dict[str, Any]], event_type: str, utc_after: float | None = None) -> dict[str, Any] | None:
    candidates = []
    for row in rows:
        if row.get("event_type") != event_type:
            continue
        if utc_after is not None and float(row.get("utc_epoch_s", -math.inf)) <= utc_after:
            continue
        candidates.append(row)
    if not candidates:
        return None
    return min(candidates, key=lambda x: float(x["utc_epoch_s"]))


def adjudicate_primary(
    *,
    invalid: list[str],
    causal_positive: bool,
    clock_positive: bool,
    censored_positive: bool,
    m3_observed: bool,
    reversal: bool,
) -> str:
    if invalid:
        return "INVALID"
    if causal_positive and not m3_observed:
        return "CENSORED_POSITIVE_CAUSAL"
    if causal_positive and clock_positive:
        return "POSITIVE_CAUSAL_AND_CLOCK"
    if causal_positive:
        return "POSITIVE_CAUSAL"
    if censored_positive:
        return "CENSORED_POSITIVE"
    if clock_positive:
        return "POSITIVE_CLOCK"
    if reversal:
        return "REVERSAL"
    return "UNRESOLVED"


def classify_run(run_dir: Path, run_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source_dir = run_dir / "source"
    generated_path = source_dir / "generated.jsonl"
    source_events_path = source_dir / "q0_source_generation.ndjson"
    mqtt_path = source_dir / "q0_mqtt_events.ndjson"
    transport_path = source_dir / "q0_transport_events.ndjson"
    metrics_path = source_dir / "edge_metrics.json"
    receiver_path = run_dir / "receiver_raw.tsv"
    pre_clock_path = run_dir / "clock_pre.json"
    post_clock_path = run_dir / "clock_post.json"

    required = [
        generated_path, source_events_path, mqtt_path, transport_path, metrics_path,
        receiver_path, pre_clock_path, post_clock_path,
    ]
    missing_files = [str(p.relative_to(run_dir)) for p in required if not p.exists()]
    if missing_files:
        return {
            "run_id": run_id,
            "valid": False,
            "invalid_reasons": ["missing_files:" + ",".join(missing_files)],
            "primary_class": "INVALID",
        }, []

    generated, by_seq, gen_errors = load_generated(generated_path, run_id)
    source_events = load_ndjson(source_events_path)
    mqtt = load_ndjson(mqtt_path)
    transport = load_ndjson(transport_path)
    metrics = load_json(metrics_path)
    receiver = load_receiver(receiver_path, run_id)
    pre_clock = load_json(pre_clock_path)
    post_clock = load_json(post_clock_path)

    invalid: list[str] = []
    invalid.extend(gen_errors)
    invalid.extend(receiver["parse_errors"])

    expected_seqs = set(range(1, EXPECTED_RECORDS + 1))
    if set(by_seq) != expected_seqs:
        invalid.append(
            f"generated_sequence_set_mismatch:observed={len(by_seq)}"
        )

    h_ids = {by_seq[s] for s in range(H_FIRST, H_LAST + 1) if s in by_seq}
    if len(h_ids) != EXPECTED_H:
        invalid.append(f"H_size:{len(h_ids)}")

    if metrics.get("architecture") != "W1" or metrics.get("condition") != "C1":
        invalid.append("metrics_not_W1_C1")
    if int(metrics.get("restart_count", -1)) != 0:
        invalid.append("unexpected_restart")
    if int(metrics.get("queue_pending", -1)) != 0:
        invalid.append("queue_not_drained")

    restore = first_after(transport, "RESTORE_APPLY")
    outage_confirmed = first_after(transport, "OUTAGE_CONFIRMED")
    m0_row = None
    if restore is not None:
        m0_row = first_after(transport, "PROBE_SUCCESS", float(restore["utc_epoch_s"]))
    if outage_confirmed is None:
        invalid.append("missing_OUTAGE_CONFIRMED")
    if restore is None:
        invalid.append("missing_RESTORE_APPLY")
    if m0_row is None:
        invalid.append("missing_M0_PROBE_SUCCESS")

    m1_row = None
    if restore is not None:
        m1_row = first_after(mqtt, "CONNACK_OK", float(restore["utc_epoch_s"]))
    if m1_row is None:
        invalid.append("missing_post_restore_M1_CONNACK")

    puback_first: dict[str, dict[str, Any]] = {}
    unresolved_pubacks = 0
    for row in mqtt:
        if row.get("event_type") != "PUBACK":
            continue
        rid = row.get("record_id")
        if rid == "UNRESOLVED" or rid is None:
            unresolved_pubacks += 1
            continue
        if rid not in puback_first:
            puback_first[rid] = row

    acked_h = h_ids & set(puback_first)
    if len(acked_h) != EXPECTED_H:
        invalid.append(f"H_puback_coverage:{len(acked_h)}/{EXPECTED_H}")

    m2_row = None
    if len(acked_h) == EXPECTED_H:
        m2_row = max(
            (puback_first[rid] for rid in h_ids),
            key=lambda x: float(x["mono_s"]),
        )

    source_event_by_seq: dict[int, dict[str, Any]] = {}
    for row in source_events:
        if row.get("event_type") != "SOURCE_GENERATED":
            continue
        seq = row.get("sequence")
        if isinstance(seq, int) and seq not in source_event_by_seq:
            source_event_by_seq[seq] = row

    for seq in (H_FIRST, H_LAST, LIVE_WITNESS_SEQ):
        if seq not in source_event_by_seq:
            invalid.append(f"missing_source_generation_event:{seq}")

    if outage_confirmed is not None and H_FIRST in source_event_by_seq:
        if float(source_event_by_seq[H_FIRST]["mono_s"]) < float(outage_confirmed["mono_s"]):
            invalid.append("H_starts_before_outage_confirmed")
    if restore is not None and H_LAST in source_event_by_seq:
        if float(source_event_by_seq[H_LAST]["mono_s"]) > float(restore["mono_s"]):
            invalid.append("H_extends_after_restore")

    causal_program_order = False
    if m2_row is not None and LIVE_WITNESS_SEQ in source_event_by_seq:
        causal_program_order = (
            float(source_event_by_seq[LIVE_WITNESS_SEQ]["mono_s"])
            > float(m2_row["mono_s"])
        )
        if not causal_program_order:
            invalid.append("live_witness_not_after_M2_on_source_monotonic_clock")

    first_recv = receiver["first_by_id"]
    common = set(generated) & set(first_recv)
    payload_mismatch = sum(
        1 for rid in common
        if generated[rid]["wire_sha256"] != first_recv[rid]["wire_sha256"]
    )
    if payload_mismatch:
        invalid.append(f"receiver_payload_mismatch:{payload_mismatch}")

    first_h_rows = [first_recv[rid] for rid in h_ids if rid in first_recv]
    missing_h = sorted(h_ids - set(first_recv))
    m3_row = None
    if len(first_h_rows) == EXPECTED_H:
        m3_row = max(first_h_rows, key=lambda x: int(x["arrival_index"]))

    witness_rid = by_seq.get(LIVE_WITNESS_SEQ)
    witness_recv = first_recv.get(witness_rid) if witness_rid else None
    h_after_witness = []
    causal_positive = False
    if causal_program_order and witness_recv is not None:
        widx = int(witness_recv["arrival_index"])
        h_after_witness = sorted(
            [
                {
                    "record_id": rid,
                    "sequence": generated[rid]["sequence"],
                    "arrival_index": int(first_recv[rid]["arrival_index"]),
                }
                for rid in h_ids
                if rid in first_recv and int(first_recv[rid]["arrival_index"]) > widx
            ],
            key=lambda x: x["arrival_index"],
        )
        causal_positive = bool(h_after_witness or missing_h)

    rel_lo, rel_hi = relative_receiver_minus_source_interval(pre_clock, post_clock)
    m2_utc = float(m2_row["utc_epoch_s"]) if m2_row is not None else None
    m3_utc = float(m3_row["receive_epoch_s"]) if m3_row is not None else None
    d23_raw = None
    d23_lo = None
    d23_hi = None
    clock_positive = False
    reversal = False
    if m2_utc is not None and m3_utc is not None:
        d23_raw = m3_utc - m2_utc
        d23_lo = d23_raw - rel_hi
        d23_hi = d23_raw - rel_lo
        clock_positive = d23_lo > 0.0
        reversal = d23_hi < 0.0

    capture_last = (
        max((float(x["receive_epoch_s"]) for x in receiver["arrivals"]), default=None)
    )
    censored_positive = False
    censor_receiver_upper = None
    if m1_row is not None and m2_utc is not None:
        m1_utc = float(m1_row["utc_epoch_s"])
        censor_receiver_upper = m1_utc + CENSOR_S + rel_hi
        if missing_h and capture_last is not None:
            if capture_last > censor_receiver_upper and m2_utc < m1_utc + CENSOR_S:
                censored_positive = True

    primary_class = adjudicate_primary(
        invalid=invalid,
        causal_positive=causal_positive,
        clock_positive=clock_positive,
        censored_positive=censored_positive,
        m3_observed=m3_row is not None,
        reversal=reversal,
    )

    positive_classes = {
        "POSITIVE_CAUSAL_AND_CLOCK",
        "POSITIVE_CAUSAL",
        "POSITIVE_CLOCK",
        "CENSORED_POSITIVE_CAUSAL",
        "CENSORED_POSITIVE",
    }

    generation_gap_5000_5001_s = None
    if H_LAST in source_event_by_seq and LIVE_WITNESS_SEQ in source_event_by_seq:
        generation_gap_5000_5001_s = (
            float(source_event_by_seq[LIVE_WITNESS_SEQ]["mono_s"])
            - float(source_event_by_seq[H_LAST]["mono_s"])
        )

    stale_arrival_events = 0
    max_seen_seq = -1
    for row in receiver["arrivals"]:
        seq = int(row["sequence"])
        if seq < max_seen_seq:
            stale_arrival_events += 1
        if seq > max_seen_seq:
            max_seen_seq = seq

    result = {
        "run_id": run_id,
        "valid": not invalid,
        "invalid_reasons": invalid,
        "primary_class": primary_class,
        "positive_for_stage_rule": primary_class in positive_classes,
        "evidence_class": metrics.get("evidence_class"),
        "generated_unique": len(generated),
        "receiver_unique": len(first_recv),
        "receiver_duplicates": int(receiver["duplicates"]),
        "foreign_receiver_rows": int(receiver["foreign"]),
        "payload_mismatch_count": payload_mismatch,
        "H_size": len(h_ids),
        "H_receiver_unique": EXPECTED_H - len(missing_h),
        "H_missing_count": len(missing_h),
        "H_puback_unique": len(acked_h),
        "unresolved_pubacks_all": unresolved_pubacks,
        "M0_source_epoch_s": float(m0_row["utc_epoch_s"]) if m0_row else None,
        "M1_source_epoch_s": float(m1_row["utc_epoch_s"]) if m1_row else None,
        "M2_source_epoch_s": m2_utc,
        "M3_receiver_epoch_s": m3_utc,
        "relative_receiver_minus_source_offset_interval_s": [rel_lo, rel_hi],
        "D23_raw_cross_clock_s": d23_raw,
        "D23_lower_bound_s": d23_lo,
        "D23_upper_bound_s": d23_hi,
        "clock_resolved_positive": clock_positive,
        "receiver_causal_positive": causal_positive,
        "causal_witness_sequence": LIVE_WITNESS_SEQ,
        "causal_witness_receiver_index": (
            int(witness_recv["arrival_index"]) if witness_recv else None
        ),
        "historical_records_after_causal_witness": len(h_after_witness),
        "censored_positive": censored_positive,
        "censor_receiver_upper_epoch_s": censor_receiver_upper,
        "receiver_capture_last_epoch_s": capture_last,
        "generation_gap_5000_5001_s": generation_gap_5000_5001_s,
        "stale_arrival_event_count": stale_arrival_events,
        "clock_method": "pre_post_midpoint_interval_hull",
        "causal_rule_note": (
            "seq 5001 is generated only after complete H PUBACK closure in the "
            "frozen W1 program order; any H arrival after receiver observation "
            "of seq 5001 proves receiver incompleteness after M2 without "
            "cross-host clock subtraction."
        ),
    }

    reconciliation_rows = []
    for seq in range(1, EXPECTED_RECORDS + 1):
        rid = by_seq.get(seq)
        recv = first_recv.get(rid) if rid else None
        reconciliation_rows.append({
            "sequence": seq,
            "record_id": rid,
            "in_H": H_FIRST <= seq <= H_LAST,
            "source_wire_sha256": generated[rid]["wire_sha256"] if rid else None,
            "receiver_first_seen_epoch_s": recv["receive_epoch_s"] if recv else None,
            "receiver_first_arrival_index": recv["arrival_index"] if recv else None,
            "receiver_wire_sha256": recv["wire_sha256"] if recv else None,
            "status": "RECEIVED" if recv else "MISSING",
        })
    return result, reconciliation_rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reconciliation", required=True)
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    result, rows = classify_run(run_dir, args.run_id)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    rec = Path(args.reconciliation)
    rec.parent.mkdir(parents=True, exist_ok=True)
    with rec.open("w", newline="", encoding="utf-8") as fh:
        fields = [
            "sequence", "record_id", "in_H", "source_wire_sha256",
            "receiver_first_seen_epoch_s", "receiver_first_arrival_index",
            "receiver_wire_sha256", "status",
        ]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("valid") else 2


if __name__ == "__main__":
    raise SystemExit(main())
