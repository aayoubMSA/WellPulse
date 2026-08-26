# WellPulse — Milestone Status

Last updated: 2026-08-26 16:25 Africa/Cairo after consortium P0/P1 freeze, B2 qualification, frozen RF calibration, and the 14:00–16:00 POWDER operational window.

## Scientific work packages

| WP | Scope | Weight | Progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 100% | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 100% design work | **P0/P1 FROZEN; B2 LOCAL SEMANTICS PASS; physical/remote pre-score gates remain in WP2** |
| WP2 | RF Calibration & Measurement Validation | 15% | ACTIVE | **RF PASS/FROZEN; physical W1 H calibration is active frontier** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0% | BLOCKED BY WP2 + pre-score snapshot + explicit scored authorization |
| WP4 | OTA External Replication | 15% | 0% | BLOCKED BY WP3 |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0% scientific closure | PREPARED, NOT EXECUTED |

Under gate-based credit, scientific weighted completion remains **20%** until WP2 closes.

```text
WP0  ████████████████████  8/8
WP1  ████████████████████ 12/12 design
WP2  ───────── ACTIVE ───  RF PASS; physical H open
WP3  ░░░░░░░░░░░░░░░░░░░  0/30
WP4  ░░░░░░░░░░░░░░░░░░░  0/15
WP5  ░░░░░░░░░░░░░░░░░░░  0/20

OVERALL  ████░░░░░░░░░░░░░░░░  20%
```

## POWDER infrastructure/calibration gates

```text
G0 Account + WellPulse project      ████████████████████ PASS
G1 Manual compute provisioning      ████████████████████ PASS
G2 Explicit-key SSH + teardown      ████████████████████ PASS
G3 Simulated stack/data path        ████████████████████ PASS
G4 Controlled physical-RF lifecycle ████████████████████ PASS
G5 RF control + numeric calibration ████████████████████ PASS / FROZEN
```

## WP2 sub-gates

| WP2 sub-gate | State |
|---|---|
| Controlled RF Q0–Q3 | **PASS / FROZEN** |
| Q0 explicit user-plane readiness rule | **PASS / FROZEN; enforce every run** |
| H adverse-outcome classification | **PASS LOCAL / FROZEN** |
| H semantics/common-H anti-bias rule | **PASS / FROZEN** |
| Guarded local preflight | **PASS — 34/34 + RF/P0/P1/B2 guards** |
| Physical W1 H calibration | **OPEN / ACTIVE FRONTIER** |
| MQTT run/session isolation | **PASS LOCAL / PHYSICAL OPEN** |
| Remote B1/W1 runtime reproduction | **OPEN** |
| Experimental LTE MQTT path | **OPEN** |
| Record-ID collision fail-closed | **PASS LOCAL** |
| End-to-end identity/checksum | **OPEN PHYSICAL** |
| B1 accepted/unacked instrumentation | **PASS LOCAL / PHYSICAL OPEN** |
| B1/W1 implementation matching | **OPEN** |
| S3 restart-domain separation | **OPEN — NON-SCORED REMOTE VERIFICATION** |
| Evidence + clock alignment | **OPEN** |
| Deterministic pilot reconstruction | **OPEN** |
| B2 local semantics | **PASS 3/3** |
| B2 comparator decision | **PASS / COMPACT S2+S3 ONLY** |
| B2 remote runtime/path/restart gate | **OPEN — NON-SCORED** |
| Consortium P1 analysis/claim freeze | **PASS / FROZEN** |
| Inter-run washout/readiness rule | **PASS / FROZEN; physical enforcement OPEN** |
| Current automation credential material | **PASS — secure GitHub Actions path provisioned** |
| Current automation SSH login on a fresh READY experiment | **OPEN** |
| Immutable pre-score snapshot | **OPEN — after H/implementation gates** |
| Scored authorization | **BLOCKED / FALSE** |

## Frozen RF state

- Q0 = **0 dB**.
- Q1 = **40 dB**.
- Q2 = **52 dB**.
- Q3 = **55 dB**.
- attenuation IDs `1 33 2 34` move together.
- no further attenuation hunting authorized.

## H active gate

Successful non-scored W1 trial:

`30 s readiness -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

`H = max(120 s, ceil_to_30s(2 × p95))`

With three successful trials, p95 is the maximum observed drain. H is one common pre-score observation window for all arms/scenarios.

- `TECHNICALLY_INVALID` → preserve; predefined replacement allowed.
- `VALID_W1_RECOVERY_FAILURE` → adverse valid evidence; stop/investigate; no invalid replacement.
- `VALID_W1_RECOVERY_SUCCESS` → exactly three required.

If H > 300 s: stop and investigate; never cap.

## B2 state

Local semantics: **PASS 3/3** with `5/5 unique, 0 missing, 0 duplicates` in every trial after broker outage + abrupt client-process destruction.

B2 remains a non-primary sensitivity comparator. If later scored authorization is granted: exactly 3 S2 + 3 S3 B2 runs, no S0/S1, no adaptive replication.

## 14:00–16:00 POWDER operational window

Status: **CLOSED / OPERATIONALLY FAILED / SCIENTIFICALLY CLEAN**.

- `WP-HCAL-A` reached READY with correct physical `nuc1+nuc2` mapping.
- Its already-instantiated nodes did not authorize the newly selected automation SSH identity.
- The current public key was then registered with POWDER.
- Immediate A→B terminate/recreate failed to recover to READY.
- After deliberate cooldown, positive resource-release verification passed.
- `WP-HCAL-C` was created but remained mostly `pending`, with intermittent `provisioning`, and never reached READY.
- Final post-expiry Portal check: zero active H-cal experiments; release gate PASS.
- No H trial, LTE user-plane trial, MQTT trial, scientific RF action, or scored run occurred.

Mandatory operational rule: read `powder/PRE_EXPERIMENT_GATE_2026-08-26.md` and D-020 before the next experiment. Never use `terminate -> immediate recreate` on the same reserved nodes.

## Credential/automation state

The secure GitHub Actions path is now provisioned and runtime-validated:

- Portal API token authentication: PASS.
- SSH private-key structure: PASS.
- passphrase unlock: PASS.
- `ssh-agent` load: PASS.
- matching public key registered with POWDER for future instantiations.

Do not ask the user to re-enter secret material unless an actual credential failure is independently demonstrated. Secret values must never be committed or logged.

Fresh-node SSH acceptance is still open because the 14:00 READY experiment predated registration of the current public key.

## Current operational reservation

**2026-08-26 19:00–22:00 Africa/Cairo — `nuc1+nuc2`**.

Preferred execution policy: one early fresh instantiation, wait patiently for READY, verify live manifest + SSH both nodes, then proceed to Q0/path/runtime/session gates. No allocator churn.

## Critical path

```text
RF calibration PASS
        ↓
3 successful physical W1 H trials → freeze H
        ↓
close physical runtime/path/identity/clock/analysis gates
        ↓
non-scored S3 + B2 remote implementation qualification
        ↓
immutable pre-score snapshot
        ↓
explicit scored authorization
        ↓
WP3 B1/W1 confirmatory campaign + fixed 6-run B2 sensitivity
        ↓
WP4 compact OTA replication
        ↓
WP5 analysis + artifact + manuscript closure
```

## Exact next action

At the 19:00 reservation, first read `HANDOVER_CURRENT.md`, `docs/AGENT_HANDOVER_POWDER_NEXT.md`, and `powder/PRE_EXPERIMENT_GATE_2026-08-26.md`. Instantiate one fresh controlled-RF experiment only once; after READY, prove live bindings and SSH on both nodes, then Q0 user-plane, `tun_srsue` routing, runtime match, and fresh MQTT isolation before any H trial.

No scored runs. No WP3. No RF reopening.