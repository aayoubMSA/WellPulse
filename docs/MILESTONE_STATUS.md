# WellPulse — Milestone Status

Last updated: 2026-08-27 after **WP2-P5 HCI/raw-evidence closure PASS**.

## Scientific work packages

| WP | Scope | Weight | Credited progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 8/8 | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 12/12 | PASS / FROZEN |
| WP2 | RF Calibration & Measurement Validation | 15% | gate-open | **ACTIVE — compatibility PASS; AUDIT-R1 PASS; HCI/raw PASS; Golden remains** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0/30 | BLOCKED ON WP2 |
| WP4 | OTA External Replication | 15% | 0/15 | BLOCKED |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0/20 scientific closure | PREPARED, NOT EXECUTED |

Under gate-based scientific credit, weighted completion remains **20%** until WP2 closes.

## Revised WP2 management/readiness decomposition

This internal tracking does not create partial scientific credit.

| Patch | Scope | Internal share | Status |
|---|---|---:|---|
| WP2-P1 | RF Foundation | 20% | PASS / FROZEN |
| WP2-P2 | Recovery Semantics | 15% | PASS / FROZEN |
| WP2-P3 | Platform Compatibility | 20% | PASS / CLOSED |
| WP2-P4 | Pre-Golden Reconciliation / AUDIT-R1 | 15% | PASS / CLOSED |
| WP2-P5 | HCI & Raw-Evidence Closure | 10% | **PASS / CLOSED** |
| WP2-P6 | One clean non-scored Golden | 15% | BLOCKED / NOT STARTED |
| WP2-P7 | Formal WP2 scientific closure + scored authorization decision | 5% | BLOCKED / NOT STARTED |

`WP2_MANAGEMENT_READINESS_PROGRESS=80/100`

Scientific weighted completion remains **20%**.

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

The original H1 node-local raw bundles were **not recovered after teardown**. GitHub/local salvage is derived/provenance only. H1 remains valid adverse non-scored evidence and must not be rerun/replaced/relabelled to select a horizon.

## K-series / compatibility state

K1–K8 are **PASS / CLOSED**.

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

Decisive live compatibility run: `33085406598`  
Experiment: `fc7c2187-2376-4a92-8de1-4665a06ea943`  
Classification: `INFRASTRUCTURE_ONLY_NON_SCORED`

Canonical record: `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`.

## AUDIT-R1 state

`AUDIT_R1=PASS`

Analysis semantics, H-selection supersession, controller/GitHub evidence authority, workflow governance and stale-status supersession remain reconciled and frozen.

## WP2-P5 HCI/raw-evidence closure

Canonical record:

`docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Frozen implementation consequences:

- `HCI_CONTROL_ACTIONS_ENABLED=false`;
- HCI is passive and consumes orchestrator-owned state only;
- observer failure is non-authoritative and non-fatal;
- `orchestration/hci_events.jsonl` is conditional/non-scientific observer evidence;
- mandatory scientific evidence remains independent of the HCI;
- no background/in-run `/proj` checkpoint is enabled during protected G3-G7 science;
- G9 persistent escrow occurs after G8 reconstruction;
- persistent/node side cannot authorize teardown;
- only independent controller artifact round-trip verification may emit `TEARDOWN_AUTHORIZED=YES`.

No POWDER contact, reservation, SSH, Golden or scored work occurred in WP2-P5.

## Current WP2 frontier

P5 is closed. The project is **STOPPED before P6**.

Only after a separate explicit user continuation:

1. perform protocol v0.6.1 advisory resource-availability preflight (`resinfo.php`, record `PASS|DEFER|UNKNOWN`) immediately before booking;
2. never change frozen hardware/profile merely to chase capacity;
3. book and execute one clean non-scored G0-G10 Golden rehearsal;
4. verify complete raw evidence and controller round-trip before teardown;
5. then decide WP2-P7 formal scientific closure and explicit scored authorization.

There is **no future H-calibration/freeze step**. `H_app=300 s from t_service_ready` is already prospectively frozen.

Current controls:

- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`;
- `REBOOK_GOLDEN=false`;
- `HCI_CONTROL_ACTIONS_ENABLED=false`;
- `H_app=300 s from t_service_ready`;
- `outcome_derived_H_calibration=PROHIBITED`;
- `scored_runs_authorized=false`;
- no B1/W1/B2 scored run is authorized.

## Remaining scientific path

```text
WP0 PASS + WP1 PASS
        ↓
WP2 compatibility K1–K8 PASS
        ↓
AUDIT-R1 PASS
        ↓
WP2-P5 HCI/raw-evidence PASS
        ↓
STOP / separate explicit user resume
        ↓
advisory resinfo preflight
        ↓
one clean non-scored Golden G0–G10
        ↓
WP2-P7 scientific closure + scored authorization decision
        ↓
WP3 conducted-RF B1/W1 + fixed B2 sensitivity
        ↓
WP4 compact OTA external replication
        ↓
WP5 analysis + reproducibility artifact + figures + manuscript closure
```

Scientific weighted completion remains **20%** until WP2 closes.
