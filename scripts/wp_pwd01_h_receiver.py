#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import signal
import ssl
import threading

from wellpulse.transport import make_run_client_id, make_run_topic


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description="WP-PWD01 non-scored H-calibration MQTT receiver")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--host", default="172.16.0.1")
    parser.add_argument("--port", type=int, default=8883)
    parser.add_argument("--topic", default=None, help="Optional override; default is deterministic run-isolated topic")
    parser.add_argument("--ca-file", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    if importlib.metadata.version("paho-mqtt") != "2.1.0":
        raise RuntimeError("WP-PWD01 requires paho-mqtt==2.1.0")

    import paho.mqtt.client as mqtt

    mqtt_topic = args.topic or make_run_topic(args.run_id, "HCAL")
    client_id = make_run_client_id(args.run_id, "HCRX")

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    received_path = out / "telemetry_received.csv"
    events_path = out / "receiver_events.jsonl"
    stop = threading.Event()
    io_lock = threading.Lock()
    isolation_failure: list[str] = []
    connect_count = 0

    new_file = not received_path.exists() or received_path.stat().st_size == 0
    csv_fh = received_path.open("a", encoding="utf-8", newline="")
    writer = csv.DictWriter(
        csv_fh,
        fieldnames=["record_id", "received_ts_utc", "payload_sha256", "payload_json", "mqtt_qos", "mqtt_retain"],
    )
    if new_file:
        writer.writeheader()
        csv_fh.flush()

    def event(name: str, **fields) -> None:
        payload = {"utc": utc_now(), "event": name, **fields}
        with io_lock:
            with events_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
                fh.flush()

    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id,
        clean_session=False,
        protocol=mqtt.MQTTv311,
        transport="tcp",
    )
    client.tls_set_context(ssl.create_default_context(cafile=args.ca_file))

    def on_connect(client, userdata, flags, reason_code, properties):
        nonlocal connect_count
        connect_count += 1
        session_present = bool(getattr(flags, "session_present", False))
        event(
            "receiver_connect",
            reason_code=str(reason_code),
            session_present=session_present,
            connection_count=connect_count,
            client_id=client_id,
            topic=mqtt_topic,
        )
        if bool(getattr(reason_code, "is_failure", False)):
            return
        if connect_count == 1 and session_present:
            isolation_failure.append(
                "fresh H-calibration receiver unexpectedly resumed an existing MQTT session"
            )
            event("receiver_isolation_failure", reason=isolation_failure[-1])
            stop.set()
            return
        result, mid = client.subscribe(mqtt_topic, qos=1)
        event("receiver_subscribe", rc=int(result), mid=int(mid), topic=mqtt_topic, qos=1)

    def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
        event("receiver_disconnect", reason_code=str(reason_code))

    def on_message(client, userdata, msg):
        received_ts = utc_now()
        raw = bytes(msg.payload)
        payload_text = raw.decode("utf-8", errors="replace")
        digest = hashlib.sha256(raw).hexdigest()
        record_id = "__UNPARSEABLE__"
        try:
            parsed = json.loads(payload_text)
            record_id = str(parsed.get("record_id", "__MISSING_RECORD_ID__"))
        except Exception as exc:
            event("receiver_payload_parse_error", error=type(exc).__name__)
        with io_lock:
            writer.writerow(
                {
                    "record_id": record_id,
                    "received_ts_utc": received_ts,
                    "payload_sha256": digest,
                    "payload_json": payload_text,
                    "mqtt_qos": int(msg.qos),
                    "mqtt_retain": bool(msg.retain),
                }
            )
            csv_fh.flush()
        event("receiver_message", record_id=record_id, payload_sha256=digest, qos=int(msg.qos))

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    def request_stop(signum, frame):
        event("receiver_stop_signal", signal=int(signum))
        stop.set()

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)

    event(
        "receiver_start",
        run_id=args.run_id,
        host=args.host,
        port=args.port,
        topic=mqtt_topic,
        client_id=client_id,
        initial_session_present_required=False,
        paho_mqtt_version=importlib.metadata.version("paho-mqtt"),
        tls=True,
    )
    client.connect(args.host, args.port, keepalive=60)
    client.loop_start()
    try:
        while not stop.wait(0.25):
            pass
    finally:
        try:
            client.disconnect()
        finally:
            client.loop_stop()
            event("receiver_stop", isolation_failure=isolation_failure[-1] if isolation_failure else None)
            csv_fh.close()
    return 20 if isolation_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
