from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path


H_APP_S = 300


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
    unique_valid_received_by_300: int
    completeness_300: float
    missing_count: int
    duplicate_attempt_count: int
    checksum_mismatch_attempt_count: int
    unexpected_record_attempt_count: int
    out_of_order_attempt_count: int
    t_rf_restore_utc: str
    t_service_ready_utc: str
    horizon_end_utc: str
    h_app_s: int
    t_app_complete_utc: str | None
    T_service_s: float
    T_app_s: float | None
    T_total_s: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def reconstruct_primary_endpoint(run_dir: str | Path) -> RunEndpointResult:
    """Reconstruct the amended WP-PWD01 run-level primary endpoint.

    Authority is RECOVERY_SEMANTICS_AMENDMENT_v1. The primary cohort is frozen at
    the physical RF-restoration clock ``t_rf_restore_utc``. Application outcome
    observation starts only after the architecture-blind service-ready gate and
    ends at ``t_service_ready_utc + 300 s``. The 300 s application horizon is a
    prospective constant; it is never estimated from W1 or from scored outcomes.
    """

    root = Path(run_dir)
    manifest = json.loads((root / "run_manifest.json").read_text(encoding="utf-8"))
    run_id = str(manifest["run_id"])

    rf_restore_text = str(manifest["t_rf_restore_utc"])
    service_ready_text = str(manifest["t_service_ready_utc"])
    rf_restore = _parse_utc(rf_restore_text)
    service_ready = _parse_utc(service_ready_text)
    if service_ready < rf_restore:
        raise ValueError("t_service_ready_utc must not precede t_rf_restore_utc")

    h_app_s = int(manifest.get("h_app_s", H_APP_S))
    if h_app_s != H_APP_S:
        raise ValueError(f"h_app_s must equal frozen {H_APP_S} s")
    horizon = service_ready + timedelta(seconds=H_APP_S)
    horizon_text = horizon.isoformat()

    declared_horizon = manifest.get("horizon_end_utc")
    if declared_horizon is not None and _parse_utc(str(declared_horizon)) != horizon:
        raise ValueError("horizon_end_utc must equal t_service_ready_utc + 300 s")

    app_complete_text = manifest.get("t_app_complete_utc")
    app_complete = _parse_utc(str(app_complete_text)) if app_complete_text else None
    if app_complete is not None and app_complete < service_ready:
        raise ValueError("t_app_complete_utc must not precede t_service_ready_utc")

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
        if generated_at <= rf_restore:
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

    # Preserve file order as receiver attempt order. Rows after the fixed 300 s
    # application horizon remain raw evidence but do not enter the confirmatory
    # completeness endpoint.
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
    t_service = (service_ready - rf_restore).total_seconds()
    t_app = (app_complete - service_ready).total_seconds() if app_complete else None
    t_total = (app_complete - rf_restore).total_seconds() if app_complete else None

    return RunEndpointResult(
        run_id=run_id,
        cohort_generated=total,
        unique_valid_received_by_300=valid,
        completeness_300=valid / total,
        missing_count=total - valid,
        duplicate_attempt_count=duplicate_attempts,
        checksum_mismatch_attempt_count=checksum_mismatches,
        unexpected_record_attempt_count=unexpected_attempts,
        out_of_order_attempt_count=out_of_order,
        t_rf_restore_utc=rf_restore_text,
        t_service_ready_utc=service_ready_text,
        horizon_end_utc=horizon_text,
        h_app_s=H_APP_S,
        t_app_complete_utc=str(app_complete_text) if app_complete_text else None,
        T_service_s=t_service,
        T_app_s=t_app,
        T_total_s=t_total,
    )
