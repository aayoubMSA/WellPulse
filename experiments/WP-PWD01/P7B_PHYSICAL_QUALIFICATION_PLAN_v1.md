# WP2-P7B Physical Qualification Plan — v1

**Status:** P7B-A OFFLINE CONTRACT FREEZE — PASS candidate  
**Date:** 2026-08-27  
**Evidence class:** NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION  
**Scored authorization:** BLOCKED  
**Live authority created by this document:** NONE

## Purpose and claim ceiling

P7B exists only to qualify the physical execution mechanics that remain open after P7. It is not a scientific B1/W1/B2 comparison, creates no scored observation, and may not be used to tune Q0-Q3, H_app, workload, comparator choice, replication, or any endpoint. Every application outcome is retained as non-scored qualification evidence but has no confirmatory evidentiary role.

Exactly one future reservation may be requested only after a separate explicit P7B-C authorization. A failed cell or failed evidence gate stops the qualification; it does not authorize a replacement reservation, an automatic retry, or a relaxed rule.

## Minimum-information design

One reservation contains exactly three sequential S3 diagnostic cells:

| Order | Cell | What it must qualify |
|---:|---|---|
| 1 | P7B-B1-S3 | Real-path accepted/unacknowledged accounting, volatile-state destruction/recreation, B1 runtime manifest |
| 2 | P7B-W1-S3 | Exact low-level match to B1, separated generator/gateway restart domain, SQLite survival/replay |
| 3 | P7B-B2-S3 | Eclipse Paho Java 1.2.5 TLS/LTE path, file persistence and disconnected-buffer survival across process restart |

S3 is the smallest cell that exercises the physical LTE/MQTT path and the required process-restart boundary together. Separate S2 cells would add reservation burden without closing an additional current blocker. This is a qualification design choice only; it does not change the frozen scored S2/S3 matrix.

## Frozen topology and restart boundary

For every cell:

- the telemetry generator is a distinct process outside the gateway/client restart domain;
- the generator writes the immutable generated-record ledger and continues at 1 Hz;
- the gateway/client is the only process intentionally terminated and restarted;
- no node reboot, power cycle, UE process restart, EPC/eNB restart, or broker restart is part of the gateway restart event;
- the generator PID/start marker remains unchanged across the restart;
- the old and new gateway PIDs differ;
- the same deterministic intra-run publisher client identity and topic are reused after restart;
- the receiver identity and topic remain run-isolated;
- restart request, old-process exit, new-process start, and first post-restart gateway-ready times are recorded in UTC and monotonic time.

For B1, the generated-record ledger is evidence only and must never become a replay source. Records reach the volatile Paho gateway through a non-durable handoff. For W1, generation durably enqueues to the WellPulse SQLite queue before the gateway replay process sees the record. For B2, the Java client reopens the same cell-local Paho file-persistence directory and disconnected buffer.

## Frozen cell schedule

Each cell uses:

1. fail-closed washout/readiness gate at Q0;
2. 60 s Q0 pre-impairment interval;
3. Q3 = 55 dB for 120 s on attenuation IDs 1, 33, 2, 34 together;
4. gateway/client process restart 60 s into Q3;
5. final Q3-to-Q0 restoration defining t_rf_restore;
6. the frozen clean LTE restoration and architecture-blind service-ready gate;
7. H_app = 300 s from t_service_ready;
8. Q0 cleanup and the next cell's independent washout/readiness gate.

The primary-cohort cutoff remains t_rf_restore. The clocks t_rf_restore, t_service_ready, and t_app_complete remain distinct. T_service, T_app, and T_total are retained. These clocks are captured to prove execution compatibility, not to estimate an effect.

## Runtime locks

B1 and W1 must emit machine-readable manifests proving equality of the low-level transport fields:

- Python and OS/runtime fingerprint;
- paho-mqtt 2.1.0;
- MQTTv311, QoS 1, TLS enabled;
- clean_session=false;
- keepalive 60 s;
- reconnect delay 1 s / 8 s;
- outgoing queue limit 4096;
- inflight limit 20;
- broker endpoint and CA fingerprint;
- deterministic run-unique topic and client identities.

The only intended arm difference is application-level persistence/reconciliation: disabled for B1; WellPulse SQLite WAL + synchronous FULL durable queue enabled for W1.

B2 is a separate sensitivity comparator and is not claimed to be runtime-matched to the Python arms. It is frozen at Eclipse Paho Java 1.2.5, JAR SHA-256 `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`, MQTTv311, QoS 1, TLS enabled, cleanSession=false, keepalive 60 s, automaticReconnect=false, connection timeout 5 s, MqttDefaultFilePersistence, disconnected buffer enabled/size 4096/persist=true/delete-oldest=false.

## Fail-closed washout/readiness before every cell

All checks must pass before generation begins:

1. all four attenuators read back Q0 = 0 dB;
2. experimental route to the broker resolves through tun_srsue;
3. five LTE user-plane probes show 0% loss;
4. an architecture-blind TLS/MQTT probe succeeds on the experimental endpoint;
5. deterministic cell-unique publisher, receiver, and topic identities are recorded;
6. first connection reports session_present=false;
7. architecture state/persistence directory is absent or proven empty before creation;
8. no unresolved prior client, subscriber, broker-session, or gateway process remains;
9. pinned runtime/config and CA/broker fingerprints match the contract;
10. UTC and monotonic clock capture is healthy;
11. Q0 radio metrics are captured; if RSRP/SNR are exposed, Q0 must remain within the frozen representative envelope (RSRP -75 to -45 dBm and DL SNR 25 to 60 dB);
12. evidence directories are writable and the persistent/off-platform evidence plan is armed.

Any failure yields CELL_NOT_STARTED_READINESS_FAIL and stops P7B. Attach/IP state alone is insufficient.

## Cell acceptance gates

### B1

- real-path event reconstruction records every publish call, return code, MID and PUBACK;
- immediately before restart, at least one QoS1 call is accepted but unacknowledged;
- the accepted-but-unacknowledged MID set reconstructed from events equals the reported snapshot count;
- no exact internal Paho queue-occupancy claim is made;
- the restarted gateway has a new PID and fresh volatile counters, while reusing the same intra-run client identity/topic;
- B1 has no application-level or client-file persistence.

### W1

- the B1/W1 low-level manifest comparison is exact for every frozen matched field;
- the generator remains alive and emits at least one continuous-sequence record while the gateway is down;
- the SQLite path survives the gateway restart, with WAL and synchronous=FULL recorded;
- at least one record pending before restart remains reconstructible from the durable queue after restart;
- the gateway resumes against the same cell-local queue without regenerating source records.

### B2

- the exact Java/JAR/config lock is reproduced remotely;
- route and broker traffic use tun_srsue and TLS on the same experimental endpoint/payload schema/evidence path;
- at least one disconnected-buffer record and its persistence file exist before abrupt gateway-process destruction;
- the new Java process reopens the same persistence directory with the same client identity;
- the persisted pre-restart record set is present after restart and the buffer drains by the fixed horizon.

Delivery/completeness is retained for diagnostics. It is not compared across cells and cannot be used to alter the protocol.

## Evidence and survival gates

Required reservation-level evidence:

- authoritative Portal manifest, experiment UUID/name/profile revision and bindings;
- source commit and clean execution-tree record;
- per-cell washout/readiness verdicts;
- runtime/config/CA/broker fingerprints and exact B1/W1 comparison;
- attenuation timeline, clock evidence, route proof and radio metrics;
- generator, gateway and receiver process-event ledgers;
- generated and all received-attempt ledgers;
- B1 MQTT event reconstruction and pre-restart snapshot;
- W1 SQLite database/WAL evidence and queue timeline;
- B2 JAR hash, persistence inventory and buffer timeline;
- deterministic per-cell reconstruction and gate verdict;
- complete raw SHA-256 inventory.

The teardown chain is unchanged:

`node raw -> /proj escrow -> controller pull -> GitHub artifact -> independent download/read-back -> outer TAR SHA-256 + internal SOURCE_SHA256SUMS`.

Only EVIDENCE_ESCROW_GATE=PASS may produce TEARDOWN_AUTHORIZED=YES.

## Overall verdict and stop rules

P7B PASS requires all three cell gates, all three readiness gates, exact B1/W1 matching, complete restart-domain proof, complete raw evidence, independent off-POWDER verification, and confirmed teardown.

On any failure:

- preserve the complete pre-score qualification evidence;
- restore Q0 if safely possible;
- do not start a later cell;
- do not create another reservation;
- do not authorize scored work;
- return to an explicit decision gate.

After P7B PASS, stop. The immutable pre-score snapshot and scored-authorization decision are a separate offline patch. P7B itself never sets scored_runs_authorized=true.

## Patch boundaries

- **P7B-A (this patch):** contract/design freeze and offline contract QA only.
- **P7B-B:** offline implementation plus premutation compatibility/readiness QA; requires explicit continuation.
- **P7B-C:** one live non-scored reservation and exactly the three cells; requires separate explicit live authorization.
- **P7B-D:** evidence survival, independent read-back and teardown.
- **P7B-E:** canonical closure and STOP; immutable authorization snapshot remains subsequent.

P7B-A contacts no POWDER system, creates no reservation, performs no SSH, mutates no testbed, and executes no scientific or scored run.
