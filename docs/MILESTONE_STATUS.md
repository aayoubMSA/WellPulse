# WellPulse — Milestone Status

Last updated: 2026-08-26 after consortium P0/P1 freeze, B2 qualification, and guarded preflight, Africa/Cairo

## Scientific work packages

| WP | Scope | Weight | Progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 100% | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 100% design work | **P0/P1 FROZEN; B2 LOCAL SEMANTICS PASS; physical/remote pre-score gates remain in WP2** |
| WP2 | RF Calibration & Measurement Validation | 15% | ACTIVE | **RF PASS; P0/P1/B2 local gates PASS; PHYSICAL H is active frontier** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0% | BLOCKED BY WP2 + pre-score snapshot + explicit scored authorization |
| WP4 | OTA External Replication | 15% | 0% | BLOCKED BY WP3 |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0% scientific closure | PREPARED, NOT EXECUTED |

Under gate-based credit, scientific weighted completion remains **20%** until WP2 closes.

```text
WP0  ████████████████████  8/8
WP1  ████████████████████ 12/12 design; P0/P1/B2 local decisions frozen
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
G5 RF control + numeric calibration ████████████████████ PASS
```

## Consortium/comparator gates

- Independent consortium review: **PASS WITH PRE-SCORE AMENDMENTS**.
- P0 amendment: **FROZEN / IMPLEMENTED LOCALLY**.
- P1 amendment: **FROZEN PRE-SCORE**.
- B2 local durable-client semantics: **PASS 3/3**.
- B2 scientific scope: **exactly 3 S2 + 3 S3 sensitivity runs only**, subject to remote non-scored qualification and later scored authorization.
- Primary B1/W1 comparison remains matched Python/Paho; B2 remains non-primary due runtime/client differences.

## WP2 sub-gates

| WP2 sub-gate | State |
|---|---|
| Controlled RF Q0–Q3 | **PASS / FROZEN** |
| Q0 explicit user-plane readiness | **PASS / FROZEN** |
| H adverse-outcome classification | **PASS LOCAL / FROZEN** |
| H semantics and common-H anti-bias rule | **PASS / FROZEN** |
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

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

`H = max(120 s, ceil_to_30s(2 × p95))`

With three successful trials, p95 is the maximum observed drain. H is one common pre-score observation window for all arms/scenarios and may not be recomputed after outcomes appear.

- `TECHNICALLY_INVALID` → preserve; predefined replacement allowed.
- `VALID_W1_RECOVERY_FAILURE` → adverse valid evidence; stop/investigate; no invalid replacement.
- `VALID_W1_RECOVERY_SUCCESS` → exactly three required.

If H > 300 s: stop and investigate; never cap.

## B2 local result

Three independent Paho Java 1.2.5 trials each preserved five offline QoS1 messages through abrupt client-process destruction and recovered:

`5/5 unique, 0 missing, 0 duplicates`

in every trial.

This qualifies semantics only; it is not B2-vs-W1 science.

## Current operational state

Fallback reservation:

**2026-08-26 19:00–22:00 Africa/Cairo — nuc1+nuc2**.

Earlier-slot investigation is closed for today:

- exact nuc1+nuc2: no earlier slot today;
- generic NUC5300 pair: scheduler could not fit 1/2/3 h;
- direct immediate controlled-RF allocation: rejected; no experiment created;
- fallback reservation unchanged.

Automated `POWDER_SSH_PRIVATE_KEY` remains known bad. Use the proven manual local acceptance path unless the GitHub secret is safely repaired outside chat.

## Critical path

```text
RF calibration PASS
        ↓
Consortium P0/P1 + B2 local semantics PASS
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

At 19:00 Cairo, instantiate a fresh `srslte-controlled-rf` experiment and execute only WP2 H calibration after fresh bindings, Q0 user-plane PASS, `tun_srsue` route PASS, runtime match, and fresh MQTT session isolation. Use the same H evidence bundle to close as many physical WP2 gates as it legitimately supports.

No scored runs. No WP3. No RF reopening.
