from dataclasses import dataclass
import ssl

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

class PahoMqttTlsPublisher:
    def __init__(self, config: MqttTlsConfig, client_id: str):
        try:
            import paho.mqtt.client as mqtt
        except ImportError as exc:
            raise RuntimeError("MQTT transport requires the optional 'paho-mqtt' package") from exc
        self.config = config
        self._mqtt = mqtt
        self.client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
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
        self.client.loop_stop()
        self.client.disconnect()
