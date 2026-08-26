# WP-PWD01 — Golden E2E Rehearsal v1

Date frozen: 2026-08-26
Stage: RS-6 / PRE-RESERVATION / PRE-SCORE
Authority: `RECOVERY_SEMANTICS_AMENDMENT_v1.md`
Status: FROZEN DESIGN FOR ONE NON-SCORED GOLDEN REHEARSAL
Scored runs authorized: false

## 1. Purpose

Validate the complete experimental machinery before any scored campaign: physical RF treatment, deterministic LTE substrate restoration, architecture-blind service boundary, fixed application observation, raw-data reconstruction, and fail-closed evidence escrow.

`GOLDEN_E2E=PASS` is a methods/readiness result. It is not evidence that WellPulse outperforms a comparator.

## 2. Rehearsal selection

Use one non-scored S2-style rehearsal. S2 exercises the long Q3 RF outage and standardized service-restoration boundary without adding the S3 gateway-process-restart factor.

The architecture used for the Golden rehearsal must not influence any restoration/readiness rule. No scored inference is permitted from its application outcome.

## 3. Frozen sequence

`fresh state -> Q0 readiness -> workload -> Q3 120 s -> Q0 -> clean-order LTE restore -> service-ready probe -> 300 s observation -> reconstruction -> evidence escrow -> verdict`

All shell-visible orchestration must expose a progress bar and current gate.

## 4. Gates

### G0 — Environment identity

Capture before treatment:

- POWDER experiment UUID/profile revision;
- node bindings and host identities;
- WellPulse Git commit and hashes of execution scripts;
- LTE executable/configuration hashes;
- Python/Paho/application runtime versions;
- UTC synchronization evidence.

Failure => `GOLDEN_E2E=FAIL_ENVIRONMENT_IDENTITY`.

### G1 — Pre-run clean state

Require:

- run-unique run ID, MQTT client ID and topic;
- no stale run-specific application state;
- expected broker and TLS material;
- clean LTE startup state;
- architecture treatment fixed before outcome observation.

Failure => `GOLDEN_E2E=FAIL_PRESTATE`.

### G2 — Q0 physical + application readiness

Before workload/treatment, prove:

- `tun_srsue` exists with expected addressing;
- route to experimental broker endpoint traverses `tun_srsue`;
- 5/5 bounded ICMP succeeds;
- TLS connection succeeds;
- MQTT QoS1 subscribe/publish/PUBACK/receive round-trip succeeds with payload SHA-256 equality.

Failure => `GOLDEN_E2E=FAIL_PRERUN_READINESS`.

### G3 — Frozen workload and RF schedule

Run the frozen 1 Hz workload and apply the frozen S2 RF schedule. The long outage state is Q3 = 55 dB on attenuator IDs `1 33 2 34` for 120 s. Preserve command start/end timestamps and programmed attenuation.

Any deviation => `GOLDEN_E2E=FAIL_TREATMENT_FIDELITY`.

### G4 — Physical restoration clock

`t_rf_restore` is the UTC command-end timestamp at which all four attenuators complete Q3 -> Q0. Freeze the primary cohort as all valid records generated at or before `t_rf_restore`.

### G5 — Deterministic substrate restoration

Immediately after `t_rf_restore`, execute the architecture-blind clean-order sequence:

1. stop UE LTE process;
2. reset/start EPC and wait for deterministic core readiness;
3. start eNB and wait for deterministic RAN readiness;
4. start a fresh UE only after EPC/eNB readiness;
5. invoke G6.

Do not inspect queue depth, record delivery, comparator identity, completeness, or application outcome to alter this sequence.

### G6 — Service-ready gate

Freeze the infrastructure qualification bound at **120 s from the start of G5**.

Within that bound the probe must establish, in order:

1. `tun_srsue` exists with expected run addressing;
2. broker route traverses `tun_srsue`;
3. **5/5 ICMP** to the experimental endpoint succeeds under the frozen probe timeout;
4. TLS handshake to broker `172.16.0.1:8883` succeeds.

`t_service_ready` is the UTC timestamp when the final required service-ready condition passes.

The probe must not subscribe to application result topics, inspect queue/database state, inspect delivered records, or use architecture identity.

Failure by 120 s => classify immediately as `TECHNICALLY_INVALID_SERVICE_RESTORE`; preserve the attempt; do not inspect application outcomes for classification.

### G7 — Fixed application observation

If G6 passes, observe for exactly:

`H_app = 300 s from t_service_ready`

No early termination because the queue appears empty or the cohort appears complete. Preserve continuous raw application evidence through the horizon.

### G8 — Offline reconstruction gate

From preserved raw evidence, reconstruct at minimum:

- `t_rf_restore`;
- `t_service_ready`;
- primary-cohort denominator;
- unique valid received primary-cohort numerator by `t_service_ready + 300 s`;
- `completeness_300`;
- duplicate/missing/corrupt record counts;
- checksum/identity integrity;
- `t_app_complete` if achieved;
- `T_service`;
- `T_app` if defined;
- `T_total` if defined;
- queue/durable-state trajectory where the architecture exposes such state.

Reconstruction must be executable from escrowed artifacts without relying on terminal scrollback or remembered values.

Failure => `GOLDEN_E2E=FAIL_RECONSTRUCTION`.

### G9 — Fail-closed Evidence Escrow Gate

Before teardown, require:

1. freeze source raw bundle;
2. SHA-256 every admitted artifact and the bundle;
3. copy to `/proj/WellPulse`;
4. independently verify copied hashes;
5. create an off-POWDER copy;
6. independently verify off-POWDER hashes;
7. verify the mandatory raw-file inventory;
8. write provenance including run ID, experiment identity, source paths, destination paths, hashes, and UTC timestamps;
9. emit `EVIDENCE_ESCROW_GATE=PASS`.

If any step fails: `STOP / DO_NOT_TERMINATE`. Reservation expiry is not permission to bypass the gate.

Hashes, console summaries, and derived tables alone do not satisfy this gate.

### G10 — Golden verdict

`GOLDEN_E2E=PASS` only if G0-G9 pass and the run is reconstructable from escrowed evidence.

Application completeness need not be favorable for Golden PASS. An unfavorable but correctly measured application result is valid rehearsal evidence.

## 5. Mandatory raw evidence inventory

At minimum preserve both endpoint evidence required to reproduce the result, including where generated by the frozen runners:

- sender summary/manifest;
- attenuation timeline;
- generated-record ledger;
- sender queue/state timeline;
- sender MQTT event ledger;
- durable queue/database state where applicable;
- receiver summary/manifest;
- received-record ledger;
- receiver MQTT event ledger;
- LTE/core/eNB/UE logs required to reconstruct G5/G6;
- service-ready probe output;
- runtime/reproducibility fingerprints;
- orchestration console log;
- reconstruction output;
- SHA-256 manifests and escrow provenance.

RS-7 must convert this semantic inventory into exact filenames before reservation.

## 6. Automation/interlock requirements

The Golden orchestration must be command-driven and require no discretionary human decision after launch except emergency abort. It must:

- show a shell progress bar and current gate;
- timestamp every state transition in UTC;
- fail closed on unexpected return codes;
- restore RF to Q0 on abort where technically possible;
- never classify application failure as infrastructure invalidity after `t_service_ready`;
- never perform teardown until G9 passes;
- emit one final machine-readable classification.

## 7. RS-6 acceptance gate

RS-6 PASS requires this design to freeze:

- exact sequence and gate semantics;
- 120 s service-restoration qualification bound;
- 5/5 ICMP + TLS service-ready definition;
- fixed 300 s application horizon;
- reconstruction requirements;
- mandatory dual-location verified escrow;
- deterministic Golden classifications.

RS-6 does not authorize a reservation by itself. RS-7 must perform implementation/readiness QA, freeze exact scripts/filenames, estimate reservation duration/resources, and issue a final `RESERVE / DO_NOT_RESERVE` decision.
