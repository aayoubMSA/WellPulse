#!/usr/bin/env python3
"""Fail-closed time-budget gate for a WellPulse POWDER Golden rehearsal.

This script does not contact POWDER. The caller must supply an expiration timestamp
obtained from an authoritative experiment/reservation source immediately before
launch. Unknown/malformed expiry blocks the launch.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

DEFAULT_MIN_REMAINING_S = 45 * 60


def parse_utc(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone/UTC offset")
    return dt.astimezone(timezone.utc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expires-utc", required=True)
    parser.add_argument("--now-utc", default=None, help="Test/replay override; default is current UTC")
    parser.add_argument("--min-remaining-s", type=int, default=DEFAULT_MIN_REMAINING_S)
    args = parser.parse_args()

    if args.min_remaining_s <= 0:
        print("PRELAUNCH_TIME_GATE=BLOCKED:INVALID_MINIMUM")
        return 2

    try:
        expires = parse_utc(args.expires_utc)
        now = parse_utc(args.now_utc) if args.now_utc else datetime.now(timezone.utc)
    except Exception as exc:
        print(f"PRELAUNCH_TIME_GATE=BLOCKED:INVALID_TIMESTAMP:{type(exc).__name__}")
        return 2

    remaining_s = int((expires - now).total_seconds())
    print(f"EXPIRES_UTC={expires.isoformat().replace('+00:00', 'Z')}")
    print(f"CHECKED_UTC={now.isoformat().replace('+00:00', 'Z')}")
    print(f"REMAINING_S={remaining_s}")
    print(f"MIN_REQUIRED_S={args.min_remaining_s}")

    if remaining_s < args.min_remaining_s:
        print("PRELAUNCH_TIME_GATE=BLOCKED:INSUFFICIENT_REMAINING_TIME")
        print("GOLDEN_LAUNCH_AUTHORIZED=NO")
        return 3

    print("PRELAUNCH_TIME_GATE=PASS")
    print("GOLDEN_LAUNCH_AUTHORIZED=TIME_ONLY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
