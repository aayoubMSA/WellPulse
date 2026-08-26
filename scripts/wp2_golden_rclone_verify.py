#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys


def sha_stream(remote: str) -> str:
    p = subprocess.Popen(["rclone", "cat", remote], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert p.stdout is not None
    h = hashlib.sha256()
    for block in iter(lambda: p.stdout.read(1024 * 1024), b""):
        h.update(block)
    stderr = p.stderr.read().decode("utf-8", errors="replace") if p.stderr else ""
    rc = p.wait()
    if rc != 0:
        raise RuntimeError(f"rclone cat failed rc={rc} remote={remote}: {stderr.strip()}")
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify an rclone remote tree against WellPulse SOURCE_SHA256SUMS.txt")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--remote-root", required=True)
    args = ap.parse_args()

    manifest = Path(args.manifest)
    if not manifest.is_file() or manifest.stat().st_size == 0:
        print("RCLONE_SHA256_VERIFY=FAIL_MANIFEST", file=sys.stderr)
        return 40

    checked = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split(None, 1)
        rel = rel.strip()
        if rel.startswith("*"):
            rel = rel[1:]
        if rel.startswith("./"):
            rel = rel[2:]
        remote = args.remote_root.rstrip("/") + "/" + rel
        actual = sha_stream(remote)
        if actual != expected:
            print(f"RCLONE_SHA256_VERIFY=FAIL path={rel} expected={expected} actual={actual}", file=sys.stderr)
            return 41
        checked += 1

    if checked == 0:
        print("RCLONE_SHA256_VERIFY=FAIL_EMPTY", file=sys.stderr)
        return 42
    print(f"FILES_VERIFIED={checked}")
    print("RCLONE_SHA256_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
