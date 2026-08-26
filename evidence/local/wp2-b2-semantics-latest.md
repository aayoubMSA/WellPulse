# WP2 B2 Durable MQTT Client Semantics — latest

- Checked UTC: 2026-08-26T09:59:45Z
- Tested GitHub SHA: 3b052dc316a6bcacc9742b990fc54116dd909458
- Evidence class: **LOCAL NON-SCORED PRE-SCORE COMPARATOR QUALIFICATION**
- POWDER interaction: **NONE**
- Scored run interaction: **NONE**
- Eclipse Paho Java: **1.2.5**
- MQTT: **v3.1.1 / QoS1 / cleanSession=false**
- File persistence: **MqttDefaultFilePersistence**
- Persistent disconnected buffer: **enabled, size 4096, delete-oldest=false**
- Paho JAR SHA-256: `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`
- Gate: **PASS**

## Trial results

| Trial | Offline buffered | Persisted .msg files | Received | Unique | Duplicates | Missing | Result |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 5 | 5 | 5 | 5 | 0 | 0 | PASS |
| 2 | 5 | 5 | 5 | 5 | 0 | 0 | PASS |
| 3 | 5 | 5 | 5 | 5 | 0 | 0 | PASS |

## Interpretation

The candidate standard Paho Java client demonstrably preserved all five QoS1 records generated during broker unavailability across abrupt client-process destruction and delivered them after process and broker recovery in all three independent semantics trials. B2 is therefore semantically qualified for a compact pre-frozen sensitivity comparison; this is not a scientific B2-vs-W1 result.
