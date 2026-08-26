# RS-7 WP7.1 — Existing Implementation Recovery

Date: 2026-08-26
Owner: Pre-Reservation Consortium
Status: PASS
Weight: 15%

## Objective

Recover the actual implementation already used in H1 and identify exactly what can be reused versus what must be replaced for the Golden E2E rehearsal.

## Recovered canonical implementation

The repository tree confirms the H1 implementation was not lost. The following execution artifacts exist on `main`:

- `scripts/wp_pwd01_h_sender.py` — blob `6b680c5b671aa836b9a0f8c090ac44ee03957cd1`
- `scripts/wp_pwd01_h_receiver.py` — blob `cbdad9e7188ae956caa36d3c7e33754b07017642`
- `scripts/finalize_wp_pwd01_h_calibration.py` — blob `9a065649c92166f9bd7da52c3471551faf9c9b8f`
- `scripts/wp2_rs1a_sender_reconstruct.py` — blob `94634dc47596fc5cec5a049671ee6e2feaf4a61f`
- `powder/wp2_h_epc_broker.sh` — blob `0f11b8a0edf0d64bf9a13062f1220c03e0330e97`
- `src/wellpulse/powder_analysis.py` and supporting transport/store modules
- `tests/test_wp2_h_pilot_scripts.py` plus core unit tests.

The exact sender/receiver blobs match the deployment hashes recorded during the physical H1 session.

## Recovered behavior

### Sender

`wp_pwd01_h_sender.py` already implements:

- fixed attenuator IDs `1 33 2 34`;
- Q0=0 dB and Q3=55 dB;
- 30 s warm-up, 60 s pre-impairment Q0, 120 s Q3;
- route check through `tun_srsue`;
- mandatory 5-packet Q0 user-plane gate;
- `paho-mqtt==2.1.0` check;
- run-unique MQTT client/topic;
- W1 SQLite durable queue;
- `telemetry_generated.csv`;
- `attenuation_timeline.csv`;
- `queue_timeline.csv`;
- `mqtt_events.jsonl`;
- `sender_summary.json`;
- `calibration_manifest.json`;
- `w1_queue.sqlite`;
- exact Q3/Q0 command timestamps and cohort cutoff.

### Receiver

`wp_pwd01_h_receiver.py` already implements:

- `paho-mqtt==2.1.0`;
- run-unique receiver client/topic;
- TLS;
- QoS1 subscription;
- first-session isolation gate;
- `telemetry_received.csv`;
- `receiver_events.jsonl`;
- record IDs, received UTC timestamps, payload SHA-256, QoS/retain evidence.

### Existing finalizer

`finalize_wp_pwd01_h_calibration.py` is scientifically superseded for the Golden rehearsal because it implements the old W1-only H-calibration semantics, including successful-trial counting and old drain-time/H logic. It must remain preserved for H1 provenance but must not drive the new Golden verdict.

### LTE/profile startup

Canonical physical evidence confirms the profile-authoritative startup command on both physical nodes was:

`/local/repository/bin/start.sh`

On the core/eNB node it starts EPC/eNB through the profile tmux/runtime; on the UE node it starts the UE side. H1 recovery characterization establishes that a clean-order recovery must stop UE first, then bring core/RAN to stable state, then start a fresh UE.

## Reuse / replace decision

| Artifact | Decision | Reason |
|---|---|---|
| H1 receiver | REUSE WITH MINOR WRAPPER | raw receiver evidence remains appropriate |
| H1 sender generator/queue code | REUSE CORE LOGIC | workload/identity/durable-state code is proven |
| H1 sender RF/drain controller | REPLACE FOR GOLDEN | embeds old 150 s drain/H semantics and no standardized G5/G6 service boundary |
| old H finalizer | PRESERVE, DO NOT USE | superseded by fixed 300 s/service-ready semantics |
| broker/TLS setup | REUSE WITH PINNED MODERN MOSQUITTO REQUIREMENT | old system Mosquitto 1.4.15 was incompatible; physical session qualified Mosquitto 2.0.20 |
| profile `start.sh` | REUSE AS AUTHORITATIVE START PATH | directly evidenced on hardware |
| RS1 reconstruction script | REUSE IDEAS ONLY | H1-specific raw reconstruction, not Golden output schema |

## Material implementation facts recovered

1. The prior code exists and exact hashes are known; no reconstruction from memory is necessary.
2. The new Golden package must not modify the historical H1 scripts in place. New filenames are required so H1 remains reproducible as executed.
3. Golden must externalize RF/restoration orchestration from the old sender so G5/G6 can be architecture-blind and auditable.
4. Golden reconstruction must use `t_service_ready + 300 s`, not the old queue-drain/H rules.
5. Broker setup must explicitly require/qualify a modern TLS-compatible Mosquitto runtime rather than silently using system 1.4.15.
6. Raw evidence names already available from H1 are sufficient to anchor the new inventory; Golden adds restoration/service/escrow evidence rather than replacing those ledgers.

## WP7.1 acceptance gate

PASS. No unknown critical H1 dependency remains at source-code level. The remaining work is prospective implementation, not historical recovery.

`RS7_WP7_1=PASS`

Next: WP7.2 — build the Golden orchestration package without altering the frozen H1 implementation.
