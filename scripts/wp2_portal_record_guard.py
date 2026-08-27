#!/usr/bin/env python3
"""Fail-closed validator for a Portal API experiment JSON record.

The validator is intentionally conservative. It never contacts POWDER. A caller
must first obtain JSON from the frozen portal-cli client, then pass the record
here before any live preparation can proceed.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Tuple

EXPIRY_KEYS = {
    "expires",
    "expires_at",
    "expiration",
    "expiration_at",
    "expiration_time",
    "end_at",
    "end_time",
}


def parse_dt(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return None
    return dt.astimezone(timezone.utc)


def walk(obj: Any, path: str = "$") -> Iterator[Tuple[str, str | None, Any]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            child = f"{path}.{key}"
            yield child, str(key), value
            yield from walk(value, child)
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            child = f"{path}[{idx}]"
            yield child, None, value
            yield from walk(value, child)


def fail(reason: str, rc: int) -> int:
    print(f"PORTAL_RECORD_GATE=BLOCKED:{reason}")
    print("LIVE_PREPARATION_AUTHORIZED=NO")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, dest="json_path")
    ap.add_argument("--expected-experiment-id", required=True)
    ap.add_argument("--ready-status", default="ready")
    args = ap.parse_args()

    try:
        obj = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"INVALID_JSON:{type(exc).__name__}", 2)
    if not isinstance(obj, dict):
        return fail("ROOT_NOT_OBJECT", 2)

    status = obj.get("status")
    if not isinstance(status, str) or not status.strip():
        return fail("STATUS_MISSING", 3)
    status = status.strip()
    print(f"PORTAL_STATUS={status}")
    if status != args.ready_status:
        return fail(f"STATUS_NOT_READY:{status}", 4)

    expected = args.expected_experiment_id
    id_paths = []
    for path, _key, value in walk(obj):
        if isinstance(value, str) and value == expected:
            id_paths.append(path)
    if not id_paths:
        return fail("EXPERIMENT_ID_NOT_BOUND", 5)
    print(f"EXPERIMENT_ID_MATCH_PATHS={','.join(id_paths)}")

    expiry = []
    for path, key, value in walk(obj):
        if key and key.lower() in EXPIRY_KEYS:
            dt = parse_dt(value)
            if dt is not None:
                expiry.append((path, dt))

    # An ambiguous schema is not silently guessed. Duplicate paths that resolve
    # to the exact same UTC value are still reported as ambiguous because the
    # field authority would remain unclear.
    if not expiry:
        return fail("EXPIRY_FIELD_NOT_FOUND", 6)
    if len(expiry) != 1:
        print("EXPIRY_CANDIDATE_PATHS=" + ",".join(path for path, _ in expiry))
        return fail("EXPIRY_FIELD_AMBIGUOUS", 7)

    expiry_path, expires = expiry[0]
    expires_text = expires.isoformat().replace("+00:00", "Z")
    print(f"EXPIRY_FIELD_PATH={expiry_path}")
    print(f"EXPIRES_UTC={expires_text}")
    print("PORTAL_RECORD_GATE=PASS")
    print("LIVE_PREPARATION_AUTHORIZED=PORTAL_RECORD_ONLY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
