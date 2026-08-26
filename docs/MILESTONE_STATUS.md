# WellPulse — Milestone Status

Last updated: 2026-08-26 after the completed POWDER physical H1 session and post-session evidence closeout.

## Scientific work packages

| WP | Scope | Weight | Credited progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 8/8 | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 12/12 | PASS / FROZEN |
| WP2 | RF Calibration & Measurement Validation | 15% | gate-open | **ACTIVE — H1 valid recovery failure; Recovery-Semantics Amendment Consortium** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0/30 | BLOCKED |
| WP4 | OTA External Replication | 15% | 0/15 | BLOCKED |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0/20 scientific closure | PREPARED, NOT EXECUTED |

Under gate-based credit, scientific weighted completion remains **20%** until WP2 closes.

## Frozen RF/infrastructure state

- POWDER G0–G5: PASS.
- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuation IDs `1 33 2 34` move together.
- no RF sweep reopening.
- Q0 end-to-end user-plane PASS required before every physical run.

## Physical H1 result

Experiment: `WP-HCAL-E`, UUID `9153e16a-1eb1-45f5-88bf-303636a9d1ec`.

Run: `wp2h1-a1-20260826-001`.

Classification: **`VALID_W1_RECOVERY_FAILURE`**.

Key observations:

- Q3 full-state duration: `120.000117905 s`.
- RF restoration cutoff: `2026-08-26T18:16:00.428045+00:00`.
- 361 generated records; 211 in the pre-restoration cohort.
- final pending: 270; app inflight: 20.
- published calls: 111; PUBACK callbacks: 91.
- Q0 pre-readiness: 5/5 ping PASS.
- post-restoration health: 0/3 ping.
- queue never drained within the frozen bound.
- H remains unfrozen.

## Failure diagnosis and recovery characterization

The dominant post-outage non-recovery was LTE core/session-context/IP continuity pathology rather than demonstrated WellPulse/MQTT application failure.

Recovery tests:

- UE-only restart: FAIL.
- EPC/eNB reset while UE remained active: FAIL to restore usable user plane.
- coordinated `stop UE -> EPC -> eNB -> fresh UE`: PASS.

After clean-order LTE recovery, the exact TLS/MQTTv3.1.1/QoS1/payload-integrity path passed in **3/3** independent fresh sessions.

The clean-order sequence is a qualified testbed recovery primitive only, not yet an approved in-trial scientific action.

## Reproducibility/evidence state

Raw H1 artifacts, recovery logs, runtime fingerprints, and node-local chain-of-custody manifests are preserved.

Node-local final evidence manifests:

- nuc1: 22 files, SHA-256 `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`.
- nuc2: 34 files, SHA-256 `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`.

Repository is private.

## Current WP2 frontier

**Do not rerun H.**

Recovery-Semantics consortium sequence:

`RS-1 evidence reconstruction -> RS-2 LTE recovery review -> RS-3 estimand/H review -> RS-4 adversarial review -> RS-5 prospective amendment -> RS-6 Golden E2E rehearsal design -> RS-7 GO/KILL`

RS-1 is offline/read-only and uses the preserved artifacts. Canonical sender reconstruction tool:

`scripts/wp2_rs1a_sender_reconstruct.py`

## Critical path

```text
WP0/WP1 PASS
      ↓
WP2 H1 valid adverse evidence
      ↓
RS-1..RS-4 scientific reconstruction/review
      ↓
RS-5 prospective recovery-semantics amendment
      ↓
RS-6 non-scored Golden E2E rehearsal
      ↓
RS-7 GO_REOPEN_H gate
      ↓
3 valid H successes under amended/frozen protocol -> freeze H
      ↓
remaining physical implementation gates + immutable pre-score snapshot
      ↓
explicit scored authorization
      ↓
WP3 conducted-RF B1/W1 + fixed B2 sensitivity
      ↓
WP4 compact OTA replication
      ↓
WP5 analysis/artifact/manuscript closure
```

No scored run, WP3, or RF recalibration is authorized at the current state.
