# WP-RT01-v1.0 — Pre-final FIT Execution Amendment 001

Date frozen: 2026-08-23
Status: FROZEN BEFORE FINAL DATA COLLECTION

This amendment does not change the primary claim, 10,000-record workload, B0/W1 architectures, C0/C1/C2 conditions, primary endpoints, success criterion, or replication target in `EXPERIMENT_CONTRACT.md`.

## A1 — Deterministic connectivity interruption

The FIT A8 capability smoke established `tc_present=NO`; therefore `tc/netem` cannot be used on the selected A8 image.

For C1 and C2, the final implementation will use a deterministic broker-specific network block on the A8 node:

- mechanism: Linux `iptables` OUTPUT rule
- target: the run-time-resolved IPv4 address of `mqtt4.iot-lab.info`
- port: TCP/8883 only
- action: `REJECT`
- active sequence interval: records 3001 through 5000 inclusive
- recovery: remove the exact rule after record 5000 before backlog drain

This preserves SSH and the FIT shared evidence path while making the MQTT transport unavailable. It must be described as deterministic broker/network blocking, not as `netem`, latency shaping, or a general Internet outage.

Capability evidence before final collection: `iptables_chain_create=PASS` on real FIT A8 hardware.

## A2 — MQTT trust anchor compatibility

On 2026-08-23, FIT's documented `/opt/iot-lab-ca.pem` was observed to contain an older GEANT/USERTrust chain while the deployed `mqtt4.iot-lab.info` endpoint presented a current Let's Encrypt Generation-Y chain. The documented bundle produced TLS verification error 20 on both the FIT Saclay frontend and the A8 node.

Final execution therefore uses **ISRG Root X1** obtained from the official Let's Encrypt certificate endpoint and accepted only after SHA-256 fingerprint verification:

`96BCEC06264976F37460779ACF28C5A7CFE8A3C0AAE11A8FFCEE05C0BDDF08C6`

This is an operational trust-store compatibility correction, not an experimental treatment. TLS peer verification remains enabled; insecure verification bypasses are prohibited.

Capability evidence before final collection:
- FIT frontend: TLS verify code 0 + authenticated MQTT round trip PASS.
- FIT A8: TLS 1.2 verify code 0 + authenticated MQTT round trip PASS.

## A3 — A8 runtime adapter

The canonical WellPulse Python package requires Python >=3.10, while the FIT A8 capability smoke established Python 3.5.1. Final FIT execution will therefore use a version-controlled, Python-3.5-compatible adapter that preserves the frozen semantics rather than changing the research logic.

Required semantic invariants:
- deterministic `run_id + boot_id + sequence` record identity;
- canonical JSON + SHA-256 checksum;
- B0 has no durable record queue and permanently loses records generated during the blocked interval;
- W1 uses SQLite with `journal_mode=WAL`, `synchronous=FULL`, per-record durable enqueue, and idempotent record identity;
- W1 drains pending records after transport recovery;
- C2 restarts the gateway execution image during the blocked interval after record 4000, then resumes from persisted controller state and queue state;
- final sink remains idempotent by `record_id` while raw broker deliveries are preserved for duplicate counting.

The adapter must pass a bounded 10,000-record real-A8 dry run before any final matrix cell is accepted as final evidence.

## A4 — Final run order

Final runs are paired by condition to reduce temporal drift while alternating architecture order by replicate:

- Replicate 1: B0-C0, W1-C0, B0-C1, W1-C1, B0-C2, W1-C2
- Replicate 2: W1-C0, B0-C0, W1-C1, B0-C1, W1-C2, B0-C2
- Replicate 3: B0-C0, W1-C0, B0-C1, W1-C1, B0-C2, W1-C2

Each final run remains an independent 10,000-record run with its own run ID, queue/sink state, raw logs, metadata, metrics, and SHA-256 manifest.

## Change-control boundary

This amendment is frozen before final WP-RT01 data collection. Any later implementation correction that can affect the primary endpoints must invalidate affected runs or be separately versioned before collecting replacement runs.
