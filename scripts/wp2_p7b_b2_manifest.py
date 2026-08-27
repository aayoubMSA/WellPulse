#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform


EXPECTED_JAR_SHA256 = "59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Freeze exact WP2-P7B B2 runtime manifest")
    ap.add_argument("--jar", required=True)
    ap.add_argument("--ca-file", required=True)
    ap.add_argument("--host", required=True)
    ap.add_argument("--port", type=int, default=8883)
    ap.add_argument("--broker-fingerprint", required=True)
    ap.add_argument("--client-id", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--persistence-dir", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    jar = Path(args.jar)
    jar_sha = sha256_file(jar)
    if jar_sha != EXPECTED_JAR_SHA256:
        raise RuntimeError(f"Paho Java JAR hash mismatch: {jar_sha}")
    manifest = {
        "evidence_class": "NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION",
        "scored": False,
        "architecture": "B2_MQTT_DURABLE_CLIENT",
        "runtime": {
            "java_runtime": platform.java_ver(),
            "paho_java_version": "1.2.5",
            "paho_jar_sha256": jar_sha,
        },
        "transport": {
            "host": args.host,
            "port": args.port,
            "protocol": "MQTTv311",
            "qos": 1,
            "tls": True,
            "clean_session": False,
            "keepalive_s": 60,
            "automatic_reconnect": False,
            "connection_timeout_s": 5,
            "ca_sha256": sha256_file(Path(args.ca_file)),
            "broker_fingerprint": args.broker_fingerprint,
            "client_id": args.client_id,
            "topic": args.topic,
        },
        "application": {
            "persistence_enabled": True,
            "store": "MqttDefaultFilePersistence",
            "persistence_dir": args.persistence_dir,
            "disconnected_buffer": {
                "enabled": True,
                "size": 4096,
                "persist": True,
                "delete_oldest": False,
            },
        },
    }
    Path(args.output).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("P7B_B2_RUNTIME_MANIFEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
