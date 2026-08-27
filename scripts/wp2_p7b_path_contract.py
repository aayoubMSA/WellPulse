#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import PurePosixPath


def require_absolute_remote_path(value: str) -> str:
    """Return a normalized absolute POSIX path or fail closed.

    Runtime paths must already be resolved. Shell expansion tokens are rejected so
    writer and watcher cannot silently disagree about what $HOME or ~ means.
    """
    if not value:
        raise ValueError("REMOTE_PATH_EMPTY")
    if any(ch in value for ch in ("\x00", "\n", "\r")):
        raise ValueError("REMOTE_PATH_CONTROL_CHARACTER")
    if "$" in value or "~" in value:
        raise ValueError("REMOTE_PATH_UNEXPANDED_SHELL_TOKEN")
    path = PurePosixPath(value)
    if not path.is_absolute():
        raise ValueError("REMOTE_PATH_NOT_ABSOLUTE")
    normalized = str(path)
    if not normalized.startswith("/"):
        raise ValueError("REMOTE_PATH_NOT_ABSOLUTE")
    return normalized


def join_remote(base: str, *parts: str) -> str:
    root = PurePosixPath(require_absolute_remote_path(base))
    for part in parts:
        if not part or part in {".", ".."} or "/" in part or "$" in part or "~" in part:
            raise ValueError(f"REMOTE_PATH_UNSAFE_COMPONENT:{part}")
        root = root / part
    return require_absolute_remote_path(str(root))


def receiver_path_contract(core_cell_dir: str) -> dict[str, str | bool]:
    cell = require_absolute_remote_path(core_cell_dir)
    receiver_dir = require_absolute_remote_path(str(PurePosixPath(cell) / "receiver"))
    writer_event = require_absolute_remote_path(
        str(PurePosixPath(receiver_dir) / "receiver_events.jsonl")
    )
    watcher_event = require_absolute_remote_path(
        str(PurePosixPath(receiver_dir) / "receiver_events.jsonl")
    )
    console = require_absolute_remote_path(
        str(PurePosixPath(receiver_dir) / "console.txt")
    )
    return {
        "core_cell_dir": cell,
        "receiver_output_dir": receiver_dir,
        "receiver_event_writer_path": writer_event,
        "receiver_event_watcher_path": watcher_event,
        "receiver_console_path": console,
        "writer_watcher_path_equal": writer_event == watcher_event,
        "contains_unexpanded_shell_token": any(
            "$" in p or "~" in p
            for p in (cell, receiver_dir, writer_event, watcher_event, console)
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="WP2-P7B R1 absolute remote-path contract")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--path", required=True)

    p_receiver = sub.add_parser("receiver")
    p_receiver.add_argument("--core-cell-dir", required=True)

    p_join = sub.add_parser("join")
    p_join.add_argument("--base", required=True)
    p_join.add_argument("parts", nargs="+")

    args = ap.parse_args()
    try:
        if args.cmd == "validate":
            value = require_absolute_remote_path(args.path)
            print(value)
        elif args.cmd == "receiver":
            contract = receiver_path_contract(args.core_cell_dir)
            if not contract["writer_watcher_path_equal"]:
                raise ValueError("RECEIVER_WRITER_WATCHER_PATH_MISMATCH")
            if contract["contains_unexpanded_shell_token"]:
                raise ValueError("RECEIVER_PATH_UNEXPANDED_SHELL_TOKEN")
            print(json.dumps(contract, sort_keys=True))
        else:
            print(join_remote(args.base, *args.parts))
    except ValueError as exc:
        print(f"P7B_R1_PATH_CONTRACT=FAIL:{exc}")
        return 20
    print("P7B_R1_PATH_CONTRACT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
