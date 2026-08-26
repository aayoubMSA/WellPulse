# Project Validation Status

## Current state — 2026-08-26 post-H1 closeout

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Consortium pre-WP3 review: **PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS**.
- B2 durable-client local semantics: **PASS 3/3 / compact S2+S3 sensitivity comparator**.
- WP2: **ACTIVE — POST-H1 / PRE-AMENDMENT / PRE-SCORE**.
- H1 Trial #1: **`VALID_W1_RECOVERY_FAILURE`**.
- H: **UNFROZEN**.
- WP3/WP4: **BLOCKED**.
- WP5: **not scientifically closed**.
- Scientific weighted completion: **20%**.
- `scored_runs_authorized = false`.
- Repository: **private**.

## H1 physical evidence

Experiment: `WP-HCAL-E` (`9153e16a-1eb1-45f5-88bf-303636a9d1ec`), profile revision `a6da96560b6526dc6816761282722c996418fd8c`, mapping `enb1 -> nuc1`, `rue1 -> nuc2`.

Run `wp2h1-a1-20260826-001` satisfied entry/runtime/RF gates and then failed to restore a usable LTE user plane within the frozen post-Q0 bound.

Key values:

- Q3 full-state: `120.000117905 s`.
- Q0/RF restore cutoff: `2026-08-26T18:16:00.428045+00:00`.
- generated records: 361.
- pre-restoration cohort: 211.
- final pending: 270.
- inflight: 20.
- published calls: 111.
- PUBACK callbacks: 91.
- pre-Q3 Q0 health: 5/5 ping PASS.
- post-restoration health: 0/3 ping.
- queue pending zero: not reached.

This is adverse valid evidence and is not replaceable as technical invalidity.

## Failure diagnosis

Radio recovery occurred sufficiently for later strong uplink decoding, while EPC/MME/SPGW showed stale/context/IP churn and repeated attach/session cleanup failures. The observed non-recovery is therefore dominated by the LTE substrate/testbed state machine rather than a demonstrated application/MQTT durability failure.

## Recovery characterization

- UE-only restart: FAIL.
- core/RAN reset with UE still running: FAIL to restore user plane.
- coordinated `stop UE -> EPC -> eNB -> fresh UE`: PASS.
- after that recovery, exact TLS/MQTTv3.1.1/QoS1/round-trip/SHA-256 application path: **PASS 3/3 fresh sessions**.

The coordinated sequence is not yet an approved in-scenario action.

## Evidence/reproducibility

Original H1 raw archives, recovery-characterization archives, runtime/config fingerprints, and final node-local evidence manifests are preserved.

Final node-local manifest anchors:

- nuc1: 22 files, SHA-256 `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`.
- nuc2: 34 files, SHA-256 `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`.

The raw files, not the hashes alone, contain the record-level data required for scientific tables and figures.

## Current scientific frontier

Authority: `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`.

No H rerun is allowed yet.

Current path:

`RS-1 offline evidence reconstruction -> RS-2 LTE mechanism review -> RS-3 recovery-clock/H estimand review -> RS-4 adversarial review -> RS-5 prospective amendment -> RS-6 Golden E2E rehearsal design -> RS-7 GO/KILL`

Canonical RS-1 sender tool:

`scripts/wp2_rs1a_sender_reconstruct.py`

Candidate clocks under review:

- `t_rf_restore`;
- `t_service_ready`;
- `t_app_complete`.

No protocol amendment is frozen yet.

## Exact next action

1. Work offline from the preserved H1 node archives.
2. Execute RS-1A through RS-1E and preserve/hashes derived outputs.
3. Complete RS-2, RS-3 and RS-4 before writing a prospective amendment.
4. Freeze a Golden E2E non-scored rehearsal only after the amendment is defensible.
5. Reopen H only after `GO_REOPEN_H`.

No scored B1/W1/B2, no WP3, and no RF recalibration before the gate closes.
