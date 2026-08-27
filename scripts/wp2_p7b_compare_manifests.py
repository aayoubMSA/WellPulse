#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from wellpulse.p7b import compare_b1_w1_manifests


def main() -> int:
    ap = argparse.ArgumentParser(description="WP2-P7B exact B1/W1 low-level manifest comparator")
    ap.add_argument("--b1", required=True)
    ap.add_argument("--w1", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    b1 = json.loads(Path(args.b1).read_text(encoding="utf-8"))
    w1 = json.loads(Path(args.w1).read_text(encoding="utf-8"))
    verdict = compare_b1_w1_manifests(b1, w1).public_dict()
    verdict["scored"] = False
    Path(args.output).write_text(
        json.dumps(verdict, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"P7B_B1_W1_MATCH={verdict['gate']}")
    return 0 if verdict["gate"] == "PASS" else 20


if __name__ == "__main__":
    raise SystemExit(main())
