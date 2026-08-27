# WellPulse — Milestone Status

Last updated: 2026-08-27 after **AUDIT-R1 pre-Golden reconciliation**.

## Scientific work packages

| WP | Scope | Weight | Credited progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 8/8 | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 12/12 | PASS / FROZEN |
| WP2 | RF Calibration & Measurement Validation | 15% | gate-open | **ACTIVE — compatibility PASS; AUDIT-R1 reconciled; HCI/raw gate + Golden remain** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0/30 | BLOCKED ON WP2 |
| WP4 | OTA External Replication | 15% | 0/15 | BLOCKED |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0/20 scientific closure | PREPARED, NOT EXECUTED |

Under gate-based credit, scientific weighted completion remains **20%** until WP2 closes. AUDIT-R1 is governance/analysis-contract reconciliation and earns no additional scientific WP credit.

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

Key preserved derived observations:

- Q3 full-state duration: `120.000117905 s`;
- RF restoration cutoff: `2026-08-26T18:16:00.428045+00:00`;
- 361 generated records; 211 in primary cohort;
- final pending: 270; app inflight: 20;
- publish calls: 111; PUBACK callbacks: 91;
- Q0 pre-readiness: 5/5 ping PASS;
- post-restoration: 0/3 ping.

The old H-selection scheme associated with H1 is superseded. H1 remains valid adverse non-scored evidence and must not be rerun/replaced/relabelled to select a horizon.

The dominant H1 non-recovery was localized below the WellPulse application layer in LTE core/session/IP continuity. Clean ordered recovery `stop UE -> EPC -> eNB -> fresh UE` passed; the full LTE/TLS/MQTT v3.1.1/QoS1 application path then passed 3/3 fresh sessions with payload hash equality.

## H1 evidence boundary

The original H1 node-local raw bundles were **not recovered after teardown**. GitHub/local salvage is derived/provenance only. Do not claim record-level H1 raw recovery.

Historical expected archive SHA-256 anchors remain provenance:

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`;
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`.

## K-series / compatibility state

K1–K8 are **PASS / CLOSED**.

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

Decisive live compatibility run: `33085406598`  
Experiment: `fc7c2187-2376-4a92-8de1-4665a06ea943`  
Classification: `INFRASTRUCTURE_ONLY_NON_SCORED`

It verified READY/expiry binding, exact profile/hardware/image, controller SSH, runtime/profile fingerprint, detached launch, cross-node `/proj/WellPulse`, controller artifact round-trip, hashes, and teardown authorization.

Canonical record: `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`.

AUDIT-R1 removed stale runnable K-era workflow/trigger surfaces from the active GitHub Actions tree; this does not reopen or alter K evidence.

## AUDIT-R1 reconciliation state

Reconciled offline:

- analysis plan/schema/run matrix/general analysis/tests -> `t_rf_restore` cohort + `t_service_ready+300 s` endpoint;
- old W1-derived H selection -> superseded/fail-closed;
- Golden evidence inventory -> `/proj -> controller -> GitHub artifact -> independent read-back/hash` authority;
- workflow/trigger surface -> 6 active offline/static workflows, 4 root sentinels, zero active K/H-calibration workflow;
- stale STATUS/RS7/H-calibration/decision instructions -> controlled by canonical supersession map;
- protocol v0.6.1 advisory resource preflight preserved for later use only.

## Current WP2 frontier

Still open, in order:

1. `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS` — bounded passive HCI + exact independent raw-evidence closure;
2. explicit user authorization to continue;
3. advisory POWDER resource-availability preflight (`resinfo.php`, record `PASS|DEFER|UNKNOWN`) immediately before booking; it never changes frozen hardware/profile automatically;
4. one clean non-scored G0–G10 Golden rehearsal;
5. verified complete raw evidence and controller round-trip before teardown;
6. close WP2 scientifically and issue explicit scored authorization.

There is **no future H-calibration/freeze step**. `H_app=300 s from t_service_ready` is already prospectively frozen.

Current controls:

- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`;
- `REBOOK_GOLDEN=false`;
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
AUDIT-R1 offline reconciliation PASS
        ↓
LIVE_HCI_AND_RAW_EVIDENCE_GATE
        ↓
explicit user resume + advisory resinfo preflight
        ↓
one clean non-scored Golden G0–G10
        ↓
WP2 scientific closure + scored authorization
        ↓
WP3 conducted-RF B1/W1 + fixed B2 sensitivity
        ↓
WP4 compact OTA external replication
        ↓
WP5 analysis + reproducibility artifact + figures + manuscript closure
```

Scientific weighted completion remains **20%** until WP2 closes.
