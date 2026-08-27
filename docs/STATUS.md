# Project Validation Status

> **AUDIT-R1 SUPERSESSION NOTICE — 2026-08-27**  
> This file is a **historical post-H1 / pre-recovery-amendment snapshot only**. It is not current operational authority.  
> Current authority: `HANDOVER_CURRENT.md`, `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`, `docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`, and `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`.  
> In particular: `H=UNFROZEN` and the RS-1..RS-7 next-action sequence below are superseded; current `H_app=300 s` is prospectively frozen from `t_service_ready`; **do not run H calibration**. The original H1 node-local raw bundles were **not recovered after teardown**; surviving H1 material is derived/provenance only. `REBOOK_GOLDEN=false`.

## Historical snapshot — 2026-08-26 post-H1 closeout

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Consortium pre-WP3 review: **PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS**.
- B2 durable-client local semantics: **PASS 3/3 / compact S2+S3 sensitivity comparator**.
- WP2: **ACTIVE — POST-H1 / PRE-AMENDMENT / PRE-SCORE**.
- H1 Trial #1: **`VALID_W1_RECOVERY_FAILURE`**.
- H: **UNFROZEN**. *(Historical; superseded by the notice above.)*
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

The coordinated sequence was not yet an approved in-scenario action at the time of this historical snapshot; later Recovery Semantics Amendment v1 governs current restoration semantics.

## Evidence/reproducibility — historical correction

The historical snapshot previously stated that original H1 raw archives were preserved. **AUDIT-R1 corrects that statement:** the original H1 node-local raw bundles were not recovered after teardown. Surviving H1 GitHub/local salvage is derived/provenance only and must not be represented as original raw evidence.

Historical node-local manifest anchors recorded before teardown:

- nuc1: 22 files, SHA-256 `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`.
- nuc2: 34 files, SHA-256 `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`.

These anchors are provenance; they do not make the unavailable raw bundles recoverable.

## Historical scientific frontier

Authority at the time: `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`.

The historical sequence was:

`RS-1 offline evidence reconstruction -> RS-2 LTE mechanism review -> RS-3 recovery-clock/H estimand review -> RS-4 adversarial review -> RS-5 prospective amendment -> RS-6 Golden E2E rehearsal design -> RS-7 GO/KILL`

That sequence was subsequently completed/superseded. **Do not execute it from this file.**

## Current pointer

Use `HANDOVER_CURRENT.md` and `docs/NEXT_GATE.md`. AUDIT-R1 is offline-only; after it closes, the separately authorized next patch is HCI/raw-evidence closure. No Golden reservation or scored work is authorized by this document.
