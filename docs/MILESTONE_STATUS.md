# WellPulse — Milestone Status

Last updated: 2026-08-27 after **WP2-P7B-B offline implementation + premutation QA PASS / stopped before P7B-C**.

## Scientific work packages

| WP | Scope | Weight | Credited progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 8/8 | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 12/12 | PASS / FROZEN |
| WP2 | RF Calibration & Measurement Validation | 15% | gate-open | **ACTIVE — P7B-B offline implementation PASS; physical qualification still open** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0/30 | BLOCKED ON WP2 |
| WP4 | OTA External Replication | 15% | 0/15 | BLOCKED |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0/20 scientific closure | PREPARED, NOT EXECUTED |

Under gate-based scientific credit, weighted completion remains **20%** until WP2 closes.

## WP2 management/readiness decomposition

This internal tracking does not create partial scientific credit.

| Patch | Scope | Internal share | Status |
|---|---|---:|---|
| WP2-P1 | RF Foundation | 20% | PASS / FROZEN |
| WP2-P2 | Recovery Semantics | 15% | PASS / FROZEN |
| WP2-P3 | Platform Compatibility | 20% | PASS / CLOSED |
| WP2-P4 | Pre-Golden Reconciliation / AUDIT-R1 | 15% | PASS / CLOSED |
| WP2-P5 | HCI & Raw-Evidence Closure | 10% | PASS / CLOSED |
| WP2-P6 | One clean non-scored Golden | 15% | **PASS_RECOVERED_SINGLE_RUN / CLOSED** |
| WP2-P7 | Reusable-path hardening + scored authorization decision | 5% | **HARDENING PASS / SCORED AUTHORIZATION BLOCKED** |

P7B tracking adds no scientific or WP2-management credit: **A+B PASS (40/100 P7B); C-E blocked**.

`WP2_MANAGEMENT_READINESS_PROGRESS=95/100`

The remaining 5/100 is the mandatory pre-score physical qualification plus immutable authorization snapshot. Scientific weighted completion remains **20%**.

## Frozen RF/scientific state

- FIT IoT-LAB scientific layer: FINAL PASS.
- POWDER G0-G5: PASS.
- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuation IDs `1 33 2 34` move together.
- RF calibration is frozen; do not reopen the sweep.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct clocks.
- `T_service`, `T_app`, `T_total` are preserved.
- prospective application observation horizon = **`H_app=300 s` from `t_service_ready`**.
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`.
- outcome-derived/W1-derived/Golden-derived/scored-derived horizon re-estimation is prohibited.

## H1 experiment of record

Experiment: `WP-HCAL-E`  
UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`  
Run: `wp2h1-a1-20260826-001`  
Classification: **`VALID_W1_RECOVERY_FAILURE`**  
Scored: **NO**

The original H1 node-local raw bundles were not recovered after teardown. H1 remains valid adverse non-scored evidence and must not be rerun/replaced/relabelled to select a horizon.

## K-series / compatibility state

K1-K8 are **PASS / CLOSED**.

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

Decisive live compatibility run: `33085406598`  
Experiment: `fc7c2187-2376-4a92-8de1-4665a06ea943`  
Classification: `INFRASTRUCTURE_ONLY_NON_SCORED`

## AUDIT-R1 and P5

- `AUDIT_R1=PASS`.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.
- no background `/proj` checkpoint during protected G3-G7 science.
- persistent escrow occurs after reconstruction.
- only independent controller artifact round-trip/hash verification may authorize teardown.

## WP2-P6 Golden

Canonical record: `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`.

- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`.
- one reservation only; no scientific rerun.
- scientific run `wp2-p6r-33099648133-20260827T174149Z`.
- primary cohort `181`; valid by 300 s `181/181`; `completeness_300=1.0`.
- raw evidence complete, `/proj` escrow PASS, controller artifact round-trip PASS, teardown confirmed.

## WP2-P7 hardening and decision

Canonical record: `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`.

- reusable-path hardening PASS;
- bounded offline closure run `33103997677` PASS;
- **36/36 tests PASS**;
- no POWDER contact, mutation, science or scored run occurred in P7;
- scored authorization remained blocked on mandatory pre-score physical qualification.

`SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`

`scored_runs_authorized=false`

## WP2-P7B-A contract freeze

Canonical record: `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`.

- `WP2_P7B_A=PASS_OFFLINE_CONTRACT_FREEZE`;
- one future reservation / exactly three sequential non-scored S3 diagnostic cells: B1, W1, B2;
- 41/41 offline tests PASS in run `33106623492`, job `98638079325`;
- no POWDER contact, reservation, SSH, mutation, science or scored run.

## WP2-P7B-B offline implementation + premutation QA

Canonical record: `docs/WP2_P7B_B_OFFLINE_IMPLEMENTATION_CLOSURE_2026-08-27.md`.

- `WP2_P7B_B=PASS_OFFLINE_IMPLEMENTATION_PREMUTATION_QA`;
- P7B internal progress: **40/100**;
- separated generator/gateway processes implemented;
- B1 accepted/unacknowledged reconstruction implemented and fail-closed tested;
- W1 durable queue/replay and restart-survival proof implemented;
- exact B1/W1 low-level manifest comparison implemented;
- complete per-cell readiness/washout validation implemented;
- deterministic three-cell evidence reconstruction and stop/interlocks implemented;
- remote-capable Eclipse Paho Java 1.2.5 B2 adapter implemented;
- Local Unit Tests run `33108767123`, job `98645668213`: **56/56 PASS**;
- initial B2 API-compatibility run `33108767171` FAILED and is retained as QA provenance;
- one-line compatibility fix `6892ad26810d598965dfbe85ecb38f53b1097a5c`;
- accepted B2 semantics run `33108848011`, job `98645950042`: exact 1.2.5 build PASS plus three independent 5/5 recovery trials, zero missing and zero duplicates;
- `POWDER_CONTACT=NO`; `POWDER_MUTATION=NO`; `SCIENTIFIC_RUN=NO`; `SCORED_RUN=NO`.

WP2 management/readiness remains 95/100 and scientific weighted completion remains 20% because no physical pre-score gate has yet closed.

## Remaining pre-score blockers

The offline implementation blockers are closed. The following **physical** gates remain open:

1. B1 accepted/unacknowledged instrumentation on the real remote path;
2. B1/W1 matched runtime/config proof on POWDER;
3. S3 process-restart-domain separation non-scored proof;
4. B2 Java durable-client remote runtime/path/restart qualification;
5. full inter-cell washout/readiness enforcement for B1/W1/B2;
6. evidence survival + independent off-POWDER read-back + teardown;
7. immutable pre-score snapshot only after the physical gates PASS.

The shortest defensible closure remains the frozen one-reservation P7B-C qualification followed by P7B-D/E.

## Current frontier

`WP2-P7B-C — ONE LIVE NON-SCORED PHYSICAL QUALIFICATION RESERVATION`

Status: **BLOCKED / NOT AUTHORIZED pending separate explicit live authorization**.

No current authority exists to contact POWDER, create a reservation, SSH, mutate the testbed or run a physical P7B cell. There is no future H-calibration step.

## Remaining scientific path

```text
WP0 PASS + WP1 PASS
        ↓
WP2 K1-K8 + AUDIT-R1 + P5 PASS
        ↓
P6 non-scored Golden PASS
        ↓
P7 hardening PASS / scored authorization BLOCKED
        ↓
P7B-A contract PASS
        ↓
P7B-B offline implementation/QA PASS
        ↓
STOP / separate explicit P7B-C live authorization
        ↓
P7B-C one non-scored physical qualification reservation
        ↓
P7B-D evidence survival/read-back/teardown
        ↓
P7B-E canonical closure + STOP
        ↓
immutable pre-score snapshot + scored-authorization decision
        ↓
WP3 conducted-RF B1/W1 + fixed B2 sensitivity
        ↓
WP4 compact OTA external replication
        ↓
WP5 analysis + reproducibility artifact + figures + manuscript closure
```

Scientific weighted completion remains **20%** until WP2 closes.
