from __future__ import annotations

from math import ceil
from typing import Iterable


H_APP_S = 300
SUPERSESSION_AUTHORITY = "experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md"


def frozen_application_horizon_s() -> int:
    """Return the prospective application observation horizon frozen by amendment v1."""
    return H_APP_S


def _validated(values: Iterable[float]) -> tuple[float, ...]:
    """Historical helper retained only for reproducibility of pre-amendment records."""
    xs = tuple(float(v) for v in values)
    if not xs:
        raise ValueError("at least one value is required")
    if any(v < 0 for v in xs):
        raise ValueError("values must be non-negative")
    return xs


def nearest_rank_percentile(values: Iterable[float], percentile: float) -> float:
    """Historical mathematical helper; it no longer selects a WP-PWD01 horizon."""
    xs = sorted(_validated(values))
    if not 0 < percentile <= 1:
        raise ValueError("percentile must be in (0, 1]")
    rank = max(1, ceil(percentile * len(xs)))
    return xs[rank - 1]


def ceil_to_30s(value_s: float) -> int:
    """Historical mathematical helper retained for provenance only."""
    if value_s < 0:
        raise ValueError("duration must be non-negative")
    return int(30 * ceil(float(value_s) / 30.0))


def compute_recovery_horizon(drain_times_s: Iterable[float]):
    """Fail closed: W1/outcome-derived H selection is superseded and prohibited."""
    # Materialize only to preserve normal argument validation side effects; the
    # values can never affect the prospective application observation horizon.
    _validated(drain_times_s)
    raise RuntimeError(
        "WP-PWD01 outcome-derived recovery-horizon calibration is superseded; "
        f"use H_app={H_APP_S}s from t_service_ready per {SUPERSESSION_AUTHORITY}"
    )
