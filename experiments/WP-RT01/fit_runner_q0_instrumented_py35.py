#!/usr/bin/env python3
"""Q0 instrumentation wrapper for frozen WP-RT01 FIT runner.

This wrapper does not replace the frozen recovery algorithm. It imports
fit_runner_py35.py, preserves its main(), Publisher.publish() control flow,
outage sequencing, queue semantics, and payload bytes, and adds sidecar-only
observability required for R4/Q0.
"""
from __future__ import print_function

import atexit
import json
import os
import socket
import sys
import threading
import time

import fit_runner_py35 as frozen


def _arg_value(name, default=None):
    try:
        i = sys.argv.index(name)
        return sys.argv[i + 1]
    except Exception:
        return default


WORK_DIR = _arg_value("--work-dir", ".")
if not os.path.isdir(WORK_DIR):
    os.makedirs(WORK_DIR)

MQTT_EVENTS = os.path.join(WORK_DIR, "q0_mqtt_events.ndjson")
SOURCE_EVENTS = os.path.join(WORK_DIR, "q0_source_generation.ndjson")
TRANSPORT_EVENTS = os.path.join(WORK_DIR, "q0_transport_events.ndjson")

_emit_lock = threading.Lock()
_emit_handles = {}


def _close_emit_handles():
    for fh in list(_emit_handles.values()):
        try:
            fh.close()
        except Exception:
            pass
    _emit_handles.clear()


atexit.register(_close_emit_handles)


def _emit(path, obj):
    row = dict(obj)
    row.setdefault("utc_epoch_s", time.time())
    row.setdefault("mono_s", time.monotonic())
    line = json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
    with _emit_lock:
        fh = _emit_handles.get(path)
        if fh is None:
            fh = open(path, "a", 1)
            _emit_handles[path] = fh
        fh.write(line)


_FrozenPublisher = frozen.Publisher


class InstrumentedPublisher(_FrozenPublisher):
    """Sidecar observer around the frozen Publisher implementation.

    The inherited publish() method is intentionally not overridden. Instead,
    only the underlying paho client.publish callable is wrapped so the frozen
    wait-for-PUBACK behavior remains unchanged.
    """

    def __init__(self, user, password, ca, client_id):
        self._q0_session_id = client_id
        self._q0_mid_map = {}
        self._q0_attempts = {}
        self._q0_lock = threading.Lock()
        _FrozenPublisher.__init__(self, user, password, ca, client_id)
        self.client.on_publish = self._q0_on_publish
        original_publish = self.client.publish

        def wrapped_publish(topic, payload, *args, **kwargs):
            # Holding the same lock used by on_publish prevents an early PUBACK
            # callback from racing ahead of the record_id -> packet-id mapping.
            with self._q0_lock:
                info = original_publish(topic, payload, *args, **kwargs)
                record_id = None
                try:
                    record_id = json.loads(payload).get("record_id")
                except Exception:
                    pass
                if record_id is None:
                    record_id = "UNRESOLVED"
                attempt = int(self._q0_attempts.get(record_id, 0)) + 1
                self._q0_attempts[record_id] = attempt
                self._q0_mid_map[int(info.mid)] = {
                    "record_id": record_id,
                    "publish_attempt": attempt,
                    "topic": topic,
                }
                _emit(MQTT_EVENTS, {
                    "event_type": "PUBLISH_QOS1",
                    "session_id": self._q0_session_id,
                    "record_id": record_id,
                    "mqtt_packet_id": int(info.mid),
                    "publish_attempt": attempt,
                    "topic": topic,
                })
                return info

        self.client.publish = wrapped_publish

    def _on_connect(self, client, userdata, flags, rc):
        _FrozenPublisher._on_connect(self, client, userdata, flags, rc)
        _emit(MQTT_EVENTS, {
            "event_type": "CONNACK_OK" if rc == 0 else "CONNACK_FAIL",
            "session_id": self._q0_session_id,
            "rc": int(rc),
            "flags": flags,
        })

    def _on_disconnect(self, client, userdata, rc):
        _FrozenPublisher._on_disconnect(self, client, userdata, rc)
        _emit(MQTT_EVENTS, {
            "event_type": "DISCONNECT",
            "session_id": self._q0_session_id,
            "rc": int(rc),
        })

    def _q0_on_publish(self, client, userdata, mid):
        with self._q0_lock:
            meta = self._q0_mid_map.pop(int(mid), None)
            row = {
                "event_type": "PUBACK",
                "session_id": self._q0_session_id,
                "mqtt_packet_id": int(mid),
                "record_id": "UNRESOLVED",
                "publish_attempt": None,
            }
            if meta is not None:
                row.update(meta)
            _emit(MQTT_EVENTS, row)


_original_make_payload = frozen.make_payload


def _instrumented_make_payload(run_id, boot_id, sequence):
    result = _original_make_payload(run_id, boot_id, sequence)
    _emit(SOURCE_EVENTS, {
        "event_type": "SOURCE_GENERATED",
        "run_id": run_id,
        "boot_id": boot_id,
        "sequence": int(sequence),
        "record_id": result[0],
    })
    return result


_original_set_outage = frozen.set_outage
_original_assert_blocked = frozen.assert_blocked


def _instrumented_assert_blocked(log):
    _original_assert_blocked(log)
    _emit(TRANSPORT_EVENTS, {"event_type": "OUTAGE_CONFIRMED"})


def _instrumented_set_outage(ip, enabled, log):
    _original_set_outage(ip, enabled, log)
    _emit(TRANSPORT_EVENTS, {
        "event_type": "OUTAGE_APPLY" if enabled else "RESTORE_APPLY",
        "broker_ipv4": ip,
    })
    if not enabled:
        deadline = time.time() + 15.0
        attempt = 0
        while True:
            attempt += 1
            started = time.time()
            try:
                s = socket.create_connection((frozen.BROKER, frozen.PORT), 2.0)
                s.close()
                _emit(TRANSPORT_EVENTS, {
                    "event_type": "PROBE_SUCCESS",
                    "probe_attempt": attempt,
                    "elapsed_s": time.time() - started,
                    "probe": "tcp_connect_broker_8883",
                })
                break
            except Exception as exc:
                _emit(TRANSPORT_EVENTS, {
                    "event_type": "PROBE_FAIL",
                    "probe_attempt": attempt,
                    "elapsed_s": time.time() - started,
                    "probe": "tcp_connect_broker_8883",
                    "error": str(exc),
                })
                if time.time() >= deadline:
                    raise RuntimeError("post-restoration user-plane probe timeout")
                time.sleep(0.25)


# Patch only observation hooks. Frozen main()/queue/outage/replay flow is reused.
frozen.Publisher = InstrumentedPublisher
frozen.make_payload = _instrumented_make_payload
frozen.assert_blocked = _instrumented_assert_blocked
frozen.set_outage = _instrumented_set_outage


if __name__ == "__main__":
    frozen.main()
