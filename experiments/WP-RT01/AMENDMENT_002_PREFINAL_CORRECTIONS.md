# WP-RT01-v1.0 — Pre-final FIT Execution Amendment 002

Date frozen: 2026-08-23
Status: FROZEN BEFORE FINAL DATA COLLECTION
Supersedes only the affected operational details of Amendment 001; the scientific contract remains unchanged.

No final WP-RT01 matrix run had been collected when this amendment was frozen. The triggering evidence was the invalid pre-final real-A8 dry run in GitHub Actions run `32625757492` / FIT experiment `448257` on `saclay/a8-101`, which is classified `REAL_A8_DRY_RUN_NOT_FINAL_EXPERIMENT` and must not be interpreted as performance evidence.

## B1 — Cross-version checksum verification

The A8 runs Python 3.5.1 while the reconciliation analyzer runs on current Python. The failed dry run showed that parsing and re-serializing the A8 JSON before checksum verification can change the textual representation of some floating-point timestamps while preserving their numeric value (for example, an A8 wire value ending in `...4499` can re-serialize as `...45`). This caused false checksum failures.

Correction:
- the A8 wire payload remains unchanged;
- the checksum remains SHA-256 over the canonical compact sorted-key JSON body before the `checksum_sha256` field is inserted;
- verification reconstructs those original canonical bytes directly from the received/generated wire JSON text by removing the checksum field without parsing and re-serializing the remaining values;
- parsed JSON is still used for semantic fields and reconciliation after the checksum has been verified against the original bytes.

This is an evidence-verification correction only; it does not alter generated records, outage timing, MQTT treatment, or endpoints.

## B2 — QoS1 drain on the FIT A8 Mosquitto client

The failed dry run established the following simultaneous facts:
- the A8 edge runner executed 160 nominally successful 50-record QoS1 publish batches, totaling 8,000 intended B0 deliveries outside the outage;
- `mosquitto_pub` returned success for those batches;
- the frontend subscriber captured only 498 records, typically only the first few messages from each 50-record batch;
- the subscriber produced no error log.

The A8 image uses the old Mosquitto 1.5.x client. Its stdin-line (`-l`) implementation can reach EOF and disconnect while QoS1 messages remain outstanding. The previous runner used `communicate(payload)`, which closes stdin immediately after supplying the batch and therefore exposed this behavior.

Correction:
- retain the FIT-provided `/usr/bin/mosquitto_pub` and TLS/authentication path;
- wrap stdin-line publishing so the real client stdin remains open after all batch lines are supplied;
- run with debug callbacks and require one observed `PUBACK` for every QoS1 message in the batch before stdin is closed;
- fail the batch on early client exit, missing acknowledgements, or timeout;
- never mark W1 queue records SENT until the corresponding batch has passed the full-PUBACK gate;
- after edge completion, allow the frontend subscriber to reach the expected delivery count (8,000 for B0/C2; 10,000 for W1/C2) or a bounded timeout before capture is stopped. Reconciliation remains authoritative.

This correction makes the already-required QoS1 acknowledgement semantics explicit; it does not change QoS, payloads, outage treatment, or the B0/W1 distinction.

## B3 — SQLite rollback journal on FIT shared NFS

Amendment 001 stated `journal_mode=WAL`. Capability evidence established that the A8 durable work path used for preserved run evidence is mounted via NFS. SQLite's official WAL documentation states that WAL does not work over a network filesystem because it relies on shared-memory coordination.

Therefore the FIT adapter uses:
- `PRAGMA journal_mode=DELETE`;
- `PRAGMA synchronous=FULL`;
- a single WellPulse writer process per run;
- per-record durable enqueue before publish eligibility;
- persisted queue state across the C2 gateway-process restart.

This paragraph supersedes only the `journal_mode=WAL` phrase in Amendment 001 A3. The durability hypothesis and success criteria are unchanged. The bounded real-A8 W1/C2 dry run must demonstrate 10,000 local committed records, zero pending records after recovery, 10,000 unique received records, zero permanent missing, and zero final duplicates before any final matrix run is accepted.

## B4 — Dry-run invalidation and replacement rule

GitHub Actions run `32625757492` / FIT experiment `448257` is invalidated as an implementation/evidence-pipeline diagnostic. Its observed 498 received records and checksum errors must not be used in scientific analysis, figures, tables, or claims.

A replacement bounded B0/C2 + W1/C2 10,000-record real-A8 dry run is required after B1–B3 are version-controlled. Only if all dry-run gates pass may the 18-run final matrix begin.
