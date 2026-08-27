#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


SCHEMA_VERSION = "wp2-hci-v1"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Emit one non-authoritative passive WP2 Golden HCI event"
    )
    ap.add_argument("--output", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--experiment-id", required=True)
    ap.add_argument("--gate", required=True)
    ap.add_argument("--phase", required=True)
    ap.add_argument("--status", required=True)
    ap.add_argument("--progress-pct", required=True, type=int)
    ap.add_argument("--code-commit", default="")
    ap.add_argument("--hard-expiry-utc", default="")
    ap.add_argument("--evidence-state", default="NOT_STARTED")
    ap.add_argument("--persistent-copy-state", default="NOT_STARTED")
    ap.add_argument("--off-powder-copy-state", default="NOT_STARTED")
    ap.add_argument("--teardown-authorized", choices=("YES", "NO"), default="NO")
    args = ap.parse_args()

    if not 0 <= args.progress_pct <= 100:
        raise SystemExit("progress_pct must be between 0 and 100")

    event = {
        "schema_version": SCHEMA_VERSION,
        "utc": datetime.now(timezone.utc).isoformat(),
        "run_id": args.run_id,
        "experiment_id": args.experiment_id,
        "gate": args.gate,
        "phase": args.phase,
        "status": args.status,
        "progress_pct": args.progress_pct,
        "scored_run": False,
        "hci_control_actions_enabled": False,
        "independent_probes": "DISABLED",
        "compatibility_gate": "PASS",
        "evidence_state": args.evidence_state,
        "persistent_copy_state": args.persistent_copy_state,
        "off_powder_copy_state": args.off_powder_copy_state,
        "teardown_authorized": args.teardown_authorized,
        "fail_closed": True,
    }
    if args.code_commit:
        event["code_commit"] = args.code_commit
    if args.hard_expiry_utc:
        event["hard_expiry_utc"] = args.hard_expiry_utc

    payload = json.dumps(event, sort_keys=True, separators=(",", ":"))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as fh:
        fh.write(payload + "\n")

    # GitHub Actions live logs are the zero-extra-probe fallback cockpit.
    print("HCI_EVENT=" + payload, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
