# WP2-P9 Cross-Node Reconciliation Report — 2026-08-29

## Rule

CORE/nuc1 and UE/nuc2 evidence were reconciled wherever both endpoints exist. Receiver-side unique sequences are authoritative for end-to-end delivery. Disagreements are preserved rather than repaired.

| Experiment/run | CORE ↔ UE reconciliation | Result |
|---|---|---|
| E0 clean | 10/10 forward and 10/10 reverse ICMP; UE tunnel 172.16.0.2 | CONSISTENT CONTROL |
| E1 initial | UE forward pings fail already at 0 dB; sender events show MQTT failure and CORE receives none | CONSISTENT FAILURE; run NULL because prerequisite violated before treatment |
| E1R2 | 65 unique MQTT sent / 65 received; ICMP 0–30 dB clean | CONSISTENT |
| E1R3 | 100 / 100 MQTT; 50 dB ping 8/10 with stop point recorded | CONSISTENT |
| E1R4 | 100 main-sweep unique sent / 93 received; receiver missing 82,84,90,91,92,96,97 | DISAGREEMENT: seq 96 is receiver-missing but no corresponding sender `MQTT_FAIL` event; receiver result retained |
| E2 | 160 sent / 151 received; all 9 missing IDs occur at 52 dB and are present in sender failure events | CONSISTENT |
| E3 | 255 sent / 222 received | DISAGREEMENT: seq 150 is receiver-missing without a corresponding sender `MQTT_FAIL` event; receiver result retained |
| E4 | baseline/impairment/recovery phases reconcile; 21–40 absent at receiver | CONSISTENT |
| E5 manual | MQTT baseline/recovery reconcile; 21–40 absent during impairment; CORE reverse recovery ping succeeds | VALID WITH CAVEAT: forward UE recovery ping observed live but not frozen; IP transition 172.16.0.3→172.16.0.4 evidenced across node observations |
| E6 | CORE restart timestamps, UE RF restore and both-direction recovery evidence align; MQTT 40/60 | CONSISTENT |
| E7 | CORE restart, UE RF restore+restart and recovery evidence align; MQTT 40/60 | CONSISTENT; reverse baseline includes a preserved 481.046 ms RTT outlier |
| E8 | LTE stays healthy while broker is down; MQTT receiver misses 21–40 | CONSISTENT WITH CAVEAT: recovery send 41–60 was attempted twice; 80 sent-log lines but only 60 unique sequence IDs |
| E9 | 60/60 MQTT and clean bidirectional ping, no treatment | CONSISTENT CONTROL |
| E10-A | UE timing probes show no ping or MQTT recovery through full recorded attempts | CENSORED; no cross-node recovery success exists to reconcile |
| E10-B | action begin, publish success and CORE receipt align; publish→receive = 0.060172 s | CONSISTENT |
| E10-C-A | no complete two-node evidence; setup artifacts only | SETUP_ARTIFACT |
| E10-C-B | action/ping/publish timing valid; later CORE end-to-end verification exists | VALID WITH CAVEAT: later CORE verification line is duplicated; primary timing remains publish-side |
| E10-D | broker action and first manually started publish are ordered correctly | UPPER-BOUND ONLY; no exact broker recovery latency |
| E11 R1-R3 | nuc2 impairment/recovery and IP transitions are internally consistent | VALID WITH CAVEAT: collector contains no independent nuc1 archive, so no cross-node MQTT/completeness claim is derived |

## Cross-node disagreements that survive reconciliation

1. **E1R4 sequence 96** — sender log contains the sequence; CORE receiver does not; sender `events.log` has no matching `MQTT_FAIL`. End-to-end completeness therefore follows receiver reconciliation: 93/100.
2. **E3 sequence 150** — sender log contains the sequence; CORE receiver does not; sender failure-event record does not list it. End-to-end completeness follows receiver reconciliation: 222/255.
3. **E10-C-B end-to-end verification record** — the later CORE verification line occurs twice. It is retained as duplicate evidence and is not used to manufacture an additional observation.
4. **E11 R1-R3** — absence of a nuc1/CORE collector archive limits the replication evidence to UE-side ICMP/recovery/IP transitions.

No disagreement required changing raw evidence or inferring an unresolved RF path.

`P9_D_CROSS_NODE_RECONCILIATION=PASS`
