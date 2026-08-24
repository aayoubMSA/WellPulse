#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from wellpulse.powder_analysis import reconstruct_primary_endpoint


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconstruct frozen WP-PWD01 run-level endpoints")
    parser.add_argument("run_dir", help="Immutable WP-PWD01 run evidence directory")
    parser.add_argument("--out", help="Optional JSON output path")
    args = parser.parse_args()

    result = reconstruct_primary_endpoint(args.run_dir).to_dict()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
