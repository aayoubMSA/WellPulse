from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import importlib.metadata
import json
import ssl
import threading


@dataclass(frozen=True)
class MqttTlsConfig:
    host: str
    port: int = 8883
    topic: str = "wellpulse/records"
    username: str | None = None
    password: str | None = None
    qos: int = 1
    keepalive_s: int = 60
    ca_file: str | None = None


@dataclass(frozen=True)
class PahoQoS1Config:
    """Frozen low-level MQTT session used by both POWDER B1 and W1.

    B1 uses this volatile session directly. W1 adds application-level durable
    queueing/reconciliation above the same transport. The Paho client itself is
    deliberately not given any application-level disk persistence.
    """

    host: str
    port: int = 8883
    topic: str = "wellpulse/records"
    username: str | None = None
    password: str | None = None
    ca_file: str | None = None
    tls: bool = True
    qos: int = 1
    keepalive_s: int = 60
    clean_session: bool = False
    reconnect_min_delay_s: int = 1
    reconnect_max_delay_s: int = 8
    max_queued_messages: int = 4096
    max_inflight_messages: int = 20

    def public_dict(self) -> dict:
        d = asdict(self)
        d["password"] = "SET" if self.password else None
        d["paho_mqtt_version"] = importlib.metadata.version("paho-mqtt")
        d["mqtt_protocol"] = "MQTTv311"
        d["application_level_persistence"] = False
        return d


class PahoQoS1Session:
    """Asynchronous volatile MQTT QoS1 session with auditable callbacks.

    This object intentionally relies on Paho's in-memory outgoing/session state.
    It provides no disk spool. A process restart therefore destroys any local
    pending state that has not reached the broker. This is the low-level session
    to be matched between B1 and W1 in WP-PWD01.
    """

    def __init__(self, config: PahoQoS1Config, client_id: str, event_log: str | Path | None = None):
        try:
            import paho.mqtt.client as mqtt
        except ImportError as exc:
            raise RuntimeError("MQTT transport requires paho-mqtt==2.1.0") from exc

        version = importlib.metadata.version("paho-mqtt")
        if version != "2.1.0":
            raise RuntimeError(f"WP-PWD01 requires paho-mqtt==2.1.0; found {version}")
        if config.qos != 1:
            raise ValueError("WP-PWD01 matched session is frozen at MQTT QoS 1")
        if config.clean_session is not False:
            raise ValueError("WP-PWD01 B1/W1 matched session requires clean_session=False")
        if config.max_queued_messages <= 0:
            raise ValueError("WP-PWD01 requires an explicit bounded outgoing queue")

        self.config = config
        self.client_id = client_id
        self._mqtt = mqtt
        self._event_log = Path(event_log) if event_log else None
        self._event_lock = threading.Lock()
        self._state_lock = threading.Lock()
        self._connected = False
        self._outstanding_mids: set[int] = set()
        self._published_calls = 0
        self._acked_calls = 0

        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
            clean_session=False,
            protocol=mqtt.MQTTv311,
            transport="tcp",
        )
        self.client.max_queued_messages_set(config.max_queued_messages)
        self.client.max_inflight_messages_set(config.max_inflight_messages)
        self.client.reconnect_delay_set(
            min_delay=config.reconnect_min_delay_s,
            max_delay=config.reconnect_max_delay_s,
        )
        if config.username:
            self.client.username_pw_set(config.username, config.password)
        if config.tls:
            self.client.tls_set_context(ssl.create_default_context(cafile=config.ca_file))

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _event(self, event: str, **fields) -> None:
        if self._event_log is None:
            return
        payload = {"utc": self._utc_now(), "event": event, **fields}
        self._event_log.parent.mkdir(parents=True, exist_ok=True)
        with self._event_lock:
            with self._event_log.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
                fh.flush()

    def _on_connect(self, client, userdata, flags, reason_code, properties) -> None:
        with self._state_lock:
            self._connected = not bool(getattr(reason_code, "is_failure", False))
        self._event(
            "mqtt_connect",
            reason_code=str(reason_code),
            session_present=bool(getattr(flags, "session_present", False)),
        )

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties) -> None:
        with self._state_lock:
            self._connected = False
        self._event("mqtt_disconnect", reason_code=str(reason_code))

    def _on_publish(self, client, userdata, mid, reason_code, properties) -> None:
        with self._state_lock:
            self._outstanding_mids.discard(int(mid))
            self._acked_calls += 1
        self._event("mqtt_puback", mid=int(mid), reason_code=str(reason_code))

    def connect(self) -> None:
        self._event("mqtt_connect_start", host=self.config.host, port=self.config.port)
        self.client.connect(self.config.host, self.config.port, self.config.keepalive_s)
        self.client.loop_start()

    def publish_async(self, payload_json: str):
        """Submit a QoS1 message without blocking telemetry generation.

        Paho may keep accepted QoS>0 messages in its bounded in-memory outgoing
        queue while disconnected. Queue exhaustion is a real B1 failure and is
        recorded rather than hidden by application-level retry logic.
        """
        info = self.client.publish(self.config.topic, payload_json, qos=1, retain=False)
        rc = int(info.rc)
        mid = int(info.mid)
        with self._state_lock:
            self._published_calls += 1
            if rc == int(self._mqtt.MQTT_ERR_SUCCESS):
                self._outstanding_mids.add(mid)
            connected = self._connected
        self._event("mqtt_publish_call", mid=mid, rc=rc, connected=connected)
        if rc == int(self._mqtt.MQTT_ERR_QUEUE_SIZE):
            raise RuntimeError("Paho volatile outgoing queue is full")
        return info

    def snapshot(self) -> dict:
        with self._state_lock:
            return {
                "connected": self._connected,
                "published_calls": self._published_calls,
                "puback_callbacks": self._acked_calls,
                "outstanding_mid_count": len(self._outstanding_mids),
            }

    def close_at_horizon(self) -> None:
        """Stop the volatile session at the frozen observation horizon.

        No post-horizon application drain is performed. The receiver ledger at
        H defines the primary endpoint.
        """
        self._event("mqtt_horizon_close", **self.snapshot())
        self.client.disconnect()
        self.client.loop_stop()


class PahoMqttTlsPublisher:
    """Legacy synchronous publisher retained for existing FIT/local adapters."""

    def __init__(self, config: MqttTlsConfig, client_id: str):
        try:
            import paho.mqtt.client as mqtt
        except ImportError as exc:
            raise RuntimeError("MQTT transport requires the optional 'paho-mqtt' package") from exc
        self.config = config
        self._mqtt = mqtt
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=mqtt.MQTTv311,
        )
        if config.username:
            self.client.username_pw_set(config.username, config.password)
        self.client.tls_set_context(ssl.create_default_context(cafile=config.ca_file))

    def connect(self):
        self.client.connect(self.config.host, self.config.port, self.config.keepalive_s)
        self.client.loop_start()

    def publish(self, payload_json: str):
        info = self.client.publish(self.config.topic, payload_json, qos=self.config.qos)
        info.wait_for_publish()
        if info.rc != self._mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"MQTT publish failed with rc={info.rc}")

    def close(self):
        self.client.disconnect()
        self.client.loop_stop()
