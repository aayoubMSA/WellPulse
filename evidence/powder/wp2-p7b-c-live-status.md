# WP2-P7B-C Live Qualification — authoritative retained status

- Checked UTC: 2026-08-27T20:32:08Z
- Authorized source SHA: `a582b95ceef5705c7c1204df2c9dd637717dcef1`
- Authorized GitHub run: `33113016138`
- Experiment UUID: `26b6f315-459d-4a56-9167-69228e339f24`
- Experiment name: `wp7b3016138`
- Node run ID: `wp2-p7b-c-33113016138-20260827T203140Z`
- Evidence class: **NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION**
- P7B-C gate: **BLOCKED**
- First failure: **`RECEIVER_CONNECT_TIMEOUT`**
- Completed cells: `NONE`
- Scientific measurement started: **NO**
- W1 started: **NO**
- B2 started: **NO**
- Controller RC: `70`
- Scored authorization: **BLOCKED**
- `scored_runs_authorized=false`

## Retained live observations

- Portal reservation reached `ready`.
- Core and UE SSH gates passed.
- Frozen profile revision matched.
- B1 Q0 route: `172.16.0.1 dev tun_srsue src 172.16.0.2`.
- Five Q0 probes passed with 0% packet loss.
- TLS/MQTT readiness publish returned `rc=0`.
- Broker evidence later recovered in P7B-D proves receiver client `wp-hcrx-885b10cacb1c` connected, received CONNACK, subscribed to the exact B1 topic, and remained alive through repeated MQTT keepalive exchanges.
- The controller watcher did not observe the expected receiver event ledger and stopped fail-closed before generation/measurement.

Root-cause classification retained by P7B-E: **orchestration/evidence-path quoting defect; not demonstrated LTE/MQTT transport failure**.

## Retirement-trigger provenance

Repository cleanup deletion of `.wp2-p7b-c-live-trigger` caused GitHub run `33115086371` because path-filtered workflows also react to file deletion. That run failed at **Premutation authority and syntax gate**; `Install controller prerequisites` and `Execute one authorized P7B-C reservation` were both skipped. It created **no reservation and no POWDER contact**. Its temporary `UNAVAILABLE/not-run` status was non-authoritative and has been superseded by this restored retained record.

P7B-D final strict status is recorded separately in `evidence/powder/wp2-p7b-d-live-status.md`.
