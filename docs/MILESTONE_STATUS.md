# WellPulse — Milestone Status

Last updated: 2026-08-27 after **WP2-P7B-A offline contract freeze PASS / stopped before P7B-B**.

## Scientific work packages

| WP | Scope | Weight | Credited progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 8/8 | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 12/12 | PASS / FROZEN |
| WP2 | RF Calibration & Measurement Validation | 15% | gate-open | **ACTIVE — P7B-A contract PASS; implementation and physical qualification open** |
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

P7B tracking (no added scientific or management credit): **A PASS (20/100 P7B); B-E blocked**.

`WP2_MANAGEMENT_READINESS_PROGRESS=95/100`

The remaining 5/100 is the mandatory pre-score physical qualification + immutable authorization snapshot. Scientific weighted completion remains **20%**.

## Frozen RF/scientific state

- FIT IoT-LAB scientific layer: FINAL PASS.
- POWDER G0–G5: PASS.
- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuation IDs `1 33 2 34` move together.
- RF calibration is frozen; do not reopen the sweep.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct clocks.
- `T_service`, `T_app`, `T_total` are preserved.
- prospective application observation horizon = **`H_app=300 s` from `t_service_ready`**.
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`.
- outcome-derived/W1-derived horizon re-estimation is prohibited.

## H1 experiment of record

Experiment: `WP-HCAL-E`  
UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`  
Run: `wp2h1-a1-20260826-001`  
Classification: **`VALID_W1_RECOVERY_FAILURE`**  
Scored: **NO**

The original H1 node-local raw bundles were not recovered after teardown. H1 remains valid adverse non-scored evidence and must not be rerun/replaced/relabelled to select a horizon.

## K-series / compatibility state

K1–K8 are **PASS / CLOSED**.

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

P6 exposed two reusable-path defects after the scientific measurement: internal management alias resolution and `scp .../receiver/.` collection. P7 hardened both without rerunning the science.

## WP2-P7 hardening and decision

Canonical record: `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`.

- management aliases now require manifest-derived endpoints and pre-G0 SSH proof;
- receiver evidence uses the live-qualified tar-stream transfer;
- planned post-cohort generated traffic is separated from truly unexpected identities;
- clock-authority and transport regressions are executable under the actual unit-test gate;
- bounded offline closure run `33103997677` PASS;
- **36/36 tests PASS**;
- full offline escrow/interlock and corruption fail-closed QA PASS;
- no POWDER contact, mutation, science or scored run occurred in P7.

Decision:

`SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`

`scored_runs_authorized=false`

## WP2-P7B-A contract freeze

Canonical record: `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`.

- `WP2_P7B_A=PASS_OFFLINE_CONTRACT_FREEZE`.
- P7B internal progress: **20/100**.
- one future reservation / exactly three S3 diagnostic cells: B1, W1, B2.
- 41/41 offline tests PASS in run `33106623492`, job `98638079325`.
- no POWDER contact, reservation, SSH, mutation, science or scored run.
- next: P7B-B offline implementation/premutation QA, blocked pending explicit continuation.
- WP2 management/readiness remains 95/100; scientific weighted completion remains 20%.

## Remaining pre-score blockers

1. B1 accepted/unacknowledged instrumentation on the real remote path.
2. B1/W1 matched runtime/config proof on POWDER.
3. S3 process-restart-domain separation non-scored proof.
4. B2 Java durable-client remote runtime/path/restart qualification.
5. Full inter-run washout/readiness enforcement for B1/W1/B2.
6. Immutable pre-score snapshot only after 1-5 PASS.

The shortest defensible closure is one bounded non-scored qualification reservation designed to close items 1-5 together.

## Current frontier

`WP2-P7B-B — OFFLINE IMPLEMENTATION + PREMUTATION COMPATIBILITY/READINESS QA`

Status: **BLOCKED / NOT STARTED pending explicit continuation**. P7B-A is PASS; P7B-C live execution remains separately blocked.

No current workflow has authority to create a POWDER reservation or run scored science. There is no future H-calibration step.

## Remaining scientific path

```text
WP0 PASS + WP1 PASS
        ↓
WP2 K1–K8 + AUDIT-R1 + P5 PASS
        ↓
P6 non-scored Golden PASS
        ↓
P7 hardening PASS / scored authorization BLOCKED
        ↓
STOP / explicit resume
        ↓
P7B-A contract PASS -> P7B-B offline implementation -> separate authorization -> P7B-C one non-scored physical qualification reservation
        ↓
if PASS: immutable pre-score snapshot + scored-authorization decision
        ↓
WP3 conducted-RF B1/W1 + fixed B2 sensitivity
        ↓
WP4 compact OTA external replication
        ↓
WP5 analysis + reproducibility artifact + figures + manuscript closure
```

Scientific weighted completion remains **20%** until WP2 closes.
