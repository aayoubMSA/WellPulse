from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil
from typing import Iterable


@dataclass(frozen=True)
class RecoveryHorizonResult:
    drain_times_s: tuple[float, ...]
    p95_drain_s: float
    recovery_horizon_s: int
    stop_and_investigate: bool

    def to_dict(self) -> dict:
        return asdict(self)


def _validated(values: Iterable[float]) -> tuple[float, ...]:
    xs = tuple(float(v) for v in values)
    if not xs:
        raise ValueError("at least one valid backlog-drain time is required")
    if any(v < 0 for v in xs):
        raise ValueError("backlog-drain times must be non-negative")
    return xs


def nearest_rank_percentile(values: Iterable[float], percentile: float) -> float:
    """Return an empirical nearest-rank percentile.

    WP-PWD01 H calibration freezes p95 using this estimator before pilot
    execution. For the three required valid trials, p95 is the maximum observed
    valid backlog-drain time.
    """

    xs = sorted(_validated(values))
    if not 0 < percentile <= 1:
        raise ValueError("percentile must be in (0, 1]")
    rank = max(1, ceil(percentile * len(xs)))
    return xs[rank - 1]


def ceil_to_30s(value_s: float) -> int:
    if value_s < 0:
        raise ValueError("duration must be non-negative")
    return int(30 * ceil(float(value_s) / 30.0))


def compute_recovery_horizon(drain_times_s: Iterable[float]) -> RecoveryHorizonResult:
    """Apply the frozen protocol v0.4 H rule exactly.

    H = max(120 s, ceil_to_30s(2 * p95 observed W1 backlog-drain time)).
    Any result above 300 s is returned with stop_and_investigate=True; callers
    must not silently cap it.
    """

    xs = _validated(drain_times_s)
    p95 = nearest_rank_percentile(xs, 0.95)
    horizon = max(120, ceil_to_30s(2.0 * p95))
    return RecoveryHorizonResult(
        drain_times_s=xs,
        p95_drain_s=p95,
        recovery_horizon_s=horizon,
        stop_and_investigate=horizon > 300,
    )
