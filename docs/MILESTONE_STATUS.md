# WellPulse — Milestone Status

Last updated: 2026-08-27 after K1–K8 pre-integration compatibility closure.

## Scientific work packages

| WP | Scope | Weight | Credited progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 8/8 | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 12/12 | PASS / FROZEN |
| WP2 | RF Calibration & Measurement Validation | 15% | gate-open | **ACTIVE — compatibility PASS; HCI/raw gate + Golden + H remain** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0/30 | BLOCKED ON WP2 |
| WP4 | OTA External Replication | 15% | 0/15 | BLOCKED |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0/20 scientific closure | PREPARED, NOT EXECUTED |

Under gate-based credit, scientific weighted completion remains **20%** until WP2 closes.

## Frozen RF/scientific state

- FIT IoT-LAB scientific layer: FINAL PASS.
- POWDER G0–G5: PASS.
- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuation IDs `1 33 2 34` move together.
- RF calibration is frozen; do not reopen the sweep.
- primary cohort cutoff remains `t_rf_restore`.
- application horizon remains 300 s from `t_service_ready`.

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
- post-restoration: 0/3 ping;
- H remains unfrozen.

The dominant H1 non-recovery was localized below the WellPulse application layer in LTE core/session/IP continuity. Clean ordered recovery `stop UE -> EPC -> eNB -> fresh UE` passed; the full LTE/TLS/MQTT v3.1.1/QoS1 application path then passed 3/3 fresh sessions with payload hash equality.

## H1 evidence boundary

The original H1 node-local raw bundles were not recovered after teardown. Known expected raw archive SHA-256 anchors remain:

- nuc1: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`;
- nuc2: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`.

GitHub salvage preserved derived/provenance evidence only. PowerShell/local salvage is `CLOSED_NO_RECOVERY`. Do not claim record-level H1 raw recovery.

## K-series / compatibility state

The bounded compatibility campaign is now closed:

- `K1=PASS`
- `K2=PASS`
- `K3=PASS`
- `K4=PASS`
- `K5=PASS`
- `K6=PASS`
- `K7=PASS`
- `K8=PASS`

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

Decisive live compatibility run: `33085406598`  
Experiment: `fc7c2187-2376-4a92-8de1-4665a06ea943`  
Classification: `INFRASTRUCTURE_ONLY_NON_SCORED`

It verified READY/expiry binding, exact profile/hardware/image, controller SSH, runtime/profile fingerprint, K4 detached launch, K6 cross-node `/proj/WellPulse`, controller artifact round-trip, hashes, and teardown authorization.

K3 offline revalidation run `33087174307`: success.  
K7 semantic guard run `33087181821`: success.  
Integrated K2–K7 static acceptance run `33087199247`: success.

Canonical record:

`docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`

## Current WP2 frontier

The K-series is no longer the blocker.

Still open:

1. `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS` — passive HCI + complete independent raw evidence/escrow contract;
2. one clean non-scored G0–G10 Golden rehearsal;
3. verified complete raw evidence before teardown;
4. requalify/freeze H only after Golden PASS;
5. close WP2 scientifically and issue explicit scored authorization.

Current controls:

- `REBOOK_GOLDEN=false` until HCI/raw gate passes;
- `H=UNFROZEN`;
- `scored_runs_authorized=false`;
- no B1/W1/B2 scored run is authorized.

## Remaining scientific path

```text
WP0 PASS + WP1 PASS
        ↓
WP2 compatibility K1–K8 PASS
        ↓
LIVE_HCI_AND_RAW_EVIDENCE_GATE
        ↓
one clean non-scored Golden G0–G10
        ↓
requalify / freeze H
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
