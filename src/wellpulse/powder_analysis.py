from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable


def _parse_utc(value: str) -> datetime:
    if not value:
        raise ValueError("empty UTC timestamp")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError(f"timestamp lacks timezone: {value}")
    return dt.astimezone(timezone.utc)


@dataclass(frozen=True)
class RunEndpointResult:
    run_id: str
    cohort_generated: int
    unique_valid_received_by_h: int
    completeness_h: float
    missing_count: int
    duplicate_attempt_count: int
    checksum_mismatch_attempt_count: int
    unexpected_record_attempt_count: int
    out_of_order_attempt_count: int
    cohort_cutoff_utc: str
    horizon_end_utc: str

    def to_dict(self) -> dict:
        return asdict(self)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def reconstruct_primary_endpoint(run_dir: str | Path) -> RunEndpointResult:
    """Reconstruct WP-PWD01 run-level completeness from immutable run evidence.

    The confirmatory cohort contains records generated no later than the final
    Q0-restoration (or the analogous pseudo-restoration point in S0). Post-
    restoration generation continues to impose load but is not included in the
    primary denominator, avoiding unequal right-censoring at the observation
    horizon H.
    """

    root = Path(run_dir)
    manifest = json.loads((root / "run_manifest.json").read_text(encoding="utf-8"))
    run_id = str(manifest["run_id"])
    cutoff_text = str(manifest["cohort_cutoff_utc"])
    horizon_text = str(manifest["horizon_end_utc"])
    cutoff = _parse_utc(cutoff_text)
    horizon = _parse_utc(horizon_text)
    if horizon <= cutoff:
        raise ValueError("horizon_end_utc must be after cohort_cutoff_utc")

    generated = _read_csv(root / "telemetry_generated.csv")
    received = _read_csv(root / "telemetry_received.csv")

    required_generated = {"record_id", "generated_ts_utc", "payload_sha256"}
    required_received = {"record_id", "received_ts_utc", "payload_sha256"}
    if generated and not required_generated.issubset(generated[0]):
        raise ValueError(f"telemetry_generated.csv missing fields: {sorted(required_generated - set(generated[0]))}")
    if received and not required_received.issubset(received[0]):
        raise ValueError(f"telemetry_received.csv missing fields: {sorted(required_received - set(received[0]))}")

    cohort: dict[str, str] = {}
    for row in generated:
        rid = row["record_id"]
        generated_at = _parse_utc(row["generated_ts_utc"])
        if generated_at <= cutoff:
            if rid in cohort:
                raise ValueError(f"duplicate generated record_id in cohort: {rid}")
            cohort[rid] = row["payload_sha256"]

    if not cohort:
        raise ValueError("primary cohort is empty")

    seen_valid: set[str] = set()
    duplicate_attempts = 0
    checksum_mismatches = 0
    unexpected_attempts = 0
    out_of_order = 0
    previous_first_seen_generation_index = -1
    generation_index = {rid: idx for idx, rid in enumerate(cohort)}

    # Preserve file order as receiver attempt order; rows after H are ignored for
    # the confirmatory endpoint but remain available for exploratory diagnostics.
    for row in received:
        received_at = _parse_utc(row["received_ts_utc"])
        if received_at > horizon:
            continue
        rid = row["record_id"]
        expected_checksum = cohort.get(rid)
        if expected_checksum is None:
            unexpected_attempts += 1
            continue
        if row["payload_sha256"] != expected_checksum:
            checksum_mismatches += 1
            continue
        if rid in seen_valid:
            duplicate_attempts += 1
            continue
        idx = generation_index[rid]
        if idx < previous_first_seen_generation_index:
            out_of_order += 1
        previous_first_seen_generation_index = idx
        seen_valid.add(rid)

    total = len(cohort)
    valid = len(seen_valid)
    return RunEndpointResult(
        run_id=run_id,
        cohort_generated=total,
        unique_valid_received_by_h=valid,
        completeness_h=valid / total,
        missing_count=total - valid,
        duplicate_attempt_count=duplicate_attempts,
        checksum_mismatch_attempt_count=checksum_mismatches,
        unexpected_record_attempt_count=unexpected_attempts,
        out_of_order_attempt_count=out_of_order,
        cohort_cutoff_utc=cutoff_text,
        horizon_end_utc=horizon_text,
    )
