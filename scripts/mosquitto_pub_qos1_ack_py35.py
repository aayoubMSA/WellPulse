#!/usr/bin/env python3
"""Compatibility wrapper for FIT A8 Mosquitto 1.5.x stdin-line QoS1 publishing.

The real /usr/bin/mosquitto_pub is retained. For `-l -q 1` calls, this wrapper
keeps its stdin open until the debug stream confirms one PUBACK per supplied
message, then closes stdin and lets the client disconnect cleanly. This avoids
the old client's EOF-before-outstanding-PUBACK drain behavior.
"""
from __future__ import print_function

import os
import pty
import select
import subprocess
import sys
import time

REAL = "/usr/bin/mosquitto_pub"
PUBACK_TOKEN = "received PUBACK"


def terminate(proc):
    try:
        proc.terminate()
    except Exception:
        pass
    try:
        proc.wait(timeout=2.0)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass
        try:
            proc.wait()
        except Exception:
            pass


def main():
    args = sys.argv[1:]
    if "-l" not in args or "-q" not in args:
        os.execv(REAL, [REAL] + args)
    try:
        qidx = args.index("-q")
        qos = int(args[qidx + 1])
    except Exception:
        qos = -1
    if qos != 1:
        os.execv(REAL, [REAL] + args)

    raw = sys.stdin.buffer.read()
    messages = [line for line in raw.splitlines() if line]
    if not messages:
        return 0

    master_fd, slave_fd = pty.openpty()
    proc = subprocess.Popen(
        [REAL] + args + ["-d"],
        stdin=subprocess.PIPE,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
    )
    os.close(slave_fd)
    transcript = b""
    ack_count = 0
    expected = len(messages)
    deadline = time.time() + max(15.0, min(60.0, expected * 0.5))

    try:
        proc.stdin.write(b"\n".join(messages) + b"\n")
        proc.stdin.flush()

        while ack_count < expected:
            if time.time() >= deadline:
                sys.stderr.write(
                    "PUBACK_TIMEOUT expected=%d observed=%d\n" % (expected, ack_count)
                )
                terminate(proc)
                return 124

            ready, _, _ = select.select([master_fd], [], [], 0.25)
            if ready:
                try:
                    chunk = os.read(master_fd, 8192)
                except OSError:
                    chunk = b""
                if chunk:
                    transcript += chunk
                    ack_count = transcript.count(PUBACK_TOKEN.encode("ascii"))
                    if len(transcript) > 262144:
                        transcript = transcript[-131072:]
                elif proc.poll() is not None:
                    break
            elif proc.poll() is not None:
                break

        if ack_count != expected:
            sys.stderr.write(
                "PUBACK_INCOMPLETE expected=%d observed=%d rc=%s\n"
                % (expected, ack_count, proc.poll())
            )
            tail = transcript[-4000:].decode("utf-8", "replace")
            if tail:
                sys.stderr.write(tail + "\n")
            terminate(proc)
            return proc.returncode if proc.returncode not in (None, 0) else 125

        proc.stdin.close()
        try:
            rc = proc.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            terminate(proc)
            rc = proc.returncode if proc.returncode is not None else 126
        sys.stderr.write("PUBACK_COMPLETE expected=%d observed=%d rc=%s\n" % (expected, ack_count, rc))
        if rc != 0:
            tail = transcript[-4000:].decode("utf-8", "replace")
            if tail:
                sys.stderr.write(tail + "\n")
        return rc
    finally:
        try:
            os.close(master_fd)
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())
