# WellPulse — Milestone Status

Last updated: 2026-08-26 after independent pre-WP3 consortium review and P0 guarded preflight, Africa/Cairo

## Scientific work packages

| WP | Scope | Weight | Progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 100% | PASS — serious related-work/comparator benchmark attached |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 100% design work | PRE-SCORE COMPARATOR + CONSORTIUM P1 REVIEW OPEN |
| WP2 | RF Calibration & Measurement Validation | 15% | ACTIVE | **RF PASS; P0 AMENDMENTS LOCAL PASS; PHYSICAL H + remaining pre-score gates OPEN** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0% | BLOCKED BY WP2 + comparator freeze + explicit scored authorization |
| WP4 | OTA External Replication | 15% | 0% | BLOCKED BY WP3 |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0% scientific closure | PREPARED, NOT EXECUTED |

Under gate-based credit, scientific weighted completion remains **20%** until WP2 closes. Design, review, or implementation effort inside an unclosed WP2 does not earn partial scientific credit.

```text
WP0  ████████████████████  8/8
WP1  ████████████████████ 12/12 design; comparator/P1 review open
WP2  ───────── ACTIVE ───  RF PASS; P0 local PASS; physical H open
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

G0–G5 are non-scored enabling/calibration work and do not add scientific percentage independently.

## Independent consortium gate

Canonical review: `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`

Verdict: `PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS`

Approved P0 authority: `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`

The consortium did not reopen RF calibration or expand the WP structure. Its P0 amendments are implemented locally; P1 analysis/claim refinements remain open before scored authorization.

## WP2 sub-gates

| WP2 sub-gate | State | Canonical evidence / next requirement |
|---|---|---|
| Controlled RF profile + numeric Q0–Q3 | **PASS / FROZEN** | `RF_CALIBRATION_FREEZE_v1.md` + G5 ledger |
| Q0 explicit user-plane readiness safeguard | **PASS / FROZEN** | attach/IP alone is insufficient |
| H adverse-outcome classification | **PASS LOCAL / FROZEN** | technical invalidity separated from valid adverse W1 outcome |
| H calibration semantics | **PASS / FROZEN AS AMENDED** | `H_CALIBRATION_PLAN_v1.md` |
| P0 implementation preflight | **PASS** | `evidence/local/wp2-h-preflight-latest.md`: 34/34 tests + compile + shell syntax + P0 guards |
| Physical W1 backlog-drain calibration | **OPEN / ACTIVE FRONTIER** | exactly 3 successful technically valid W1 trials required; adverse W1 failure blocks H freeze |
| MQTT run/session isolation | **PASS LOCAL / PHYSICAL OPEN** | unique clients/topic; first fresh session must show `session_present=false` |
| Remote Paho/runtime reproduction | **OPEN** | verify on physical pilot runtime |
| MQTT experimental-radio path | **OPEN** | route must traverse `tun_srsue` to `172.16.0.1` |
| Record identity collision handling | **PASS LOCAL** | conflicting duplicate ID fails closed |
| Record identity/checksum preservation | **OPEN PHYSICAL** | verify end-to-end in pilot bundle |
| B1 accepted/unacked instrumentation | **PASS LOCAL / PHYSICAL OPEN** | do not claim exact Paho internal queue occupancy |
| B1/W1 implementation matching | **OPEN** | pre-score audit required |
| S3 restart-domain separation | **OPEN** | non-scored verification required before WP3 |
| Evidence capture + clock alignment | **OPEN** | verify mandatory endpoint timestamps |
| Deterministic analysis reconstruction | **OPEN** | reconstruct non-scored pilot bundle without manual edits |
| B2 durable-client decision | **OPEN** | compact S2/S3 sensitivity amendment if B2 qualifies |
| Consortium P1 analysis/claim amendments | **OPEN** | resolve before scored authorization |
| Scored authorization | **BLOCKED** | remains `false` until all pre-score gates pass |

## Frozen RF state

- Q0 = **0 dB** — strong/stable reference.
- Q1 = **40 dB** — degraded but continuously connected.
- Q2 = **52 dB** — near-threshold/intermittent; clean isolated 20 s test = **6 replies / 12 misses**.
- Q3 = **55 dB** — effective application-data outage.
- Attenuation IDs: `1 33 2 34`, always changed together.
- **No further attenuation sweep is authorized.**

## H active gate

Target successful non-scored W1 trial:

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Frozen outcome classes:

- `TECHNICALLY_INVALID` — preserve; replacement allowed only for predefined technical failure.
- `VALID_W1_RECOVERY_FAILURE` — preserve; do not replace as invalid; stop H freeze and investigate.
- `VALID_W1_RECOVERY_SUCCESS` — exactly three required for H calculation.

`H = max(120 s, ceil_to_30s(2 × empirical-nearest-rank p95 drain time))`

With exactly three successful trials, p95 is the maximum of the three observed successful drain times. If `H > 300 s`, stop and investigate; never cap it.

## Latest local QA

`evidence/local/wp2-h-preflight-latest.md`

- Tested SHA: `e20da2fb186eeab047080cbd851f46c3c96c81f0`.
- **34/34 tests PASS**.
- Python compile PASS.
- Broker shell syntax PASS.
- Frozen-state and P0 guards PASS.
- POWDER interaction NONE.
- Scored interaction NONE.

## Current operational state

- Historical G5 experiment: **ABSENT / CLEANUP PASS**.
- No fresh WP2-H POWDER experiment is currently live.
- Automated `POWDER_SSH_PRIVATE_KEY` path remains known bad because the stored Actions value has public-key form, not private-key form. Repair or explicitly bypass with the canonical local acceptance key; never place private key/passphrase material in Git/evidence/chat.
- Approved fallback `nuc1+nuc2` reservation: **2026-08-26 19:00–22:00 Africa/Cairo**.

## Comparator and scientific-story gate

B1 remains the matched same-Paho-Python primary comparator but is not the strongest durable MQTT client generally. B2 remains open as a compact sensitivity comparator candidate.

The consortium sharpened the expected interpretation: S1/S2 may show near-complete delivery for both B1 and W1 because B1 can retain bounded volatile QoS1 state while the process remains alive. S3 is the clearest durability stress test because the gateway-process restart destroys volatile client state. This is an interpretation amendment, not a scored result.

`scored_runs_authorized = false`.

## Exact next action

During the next fresh `srslte-controlled-rf` experiment:

1. verify profile revision and live node bindings;
2. establish LTE and pass explicit Q0 user-plane readiness;
3. confirm MQTT route through `tun_srsue`;
4. verify fresh run-isolated MQTT session state;
5. execute the amended non-scored W1 H calibration until exactly three `VALID_W1_RECOVERY_SUCCESS` trials exist, replacing only predefined technical invalidity;
6. if a `VALID_W1_RECOVERY_FAILURE` occurs, stop and investigate instead of replacing it;
7. reconstruct all attempted trials deterministically and freeze H only if the frozen rule passes.

Do not run B1/W1 scored cells, do not start WP3, and do not reopen RF calibration.

## Critical path

```text
G5 numeric RF calibration PASS
        ↓
Consortium P0 amendments + guarded local preflight PASS
        ↓
3 successful physical W1 H calibration trials → freeze H
        ↓
remaining WP2 runtime/path/identity/clock/S3 gates
        ↓
close B2 + consortium P1 amendments
        ↓
explicit scored authorization
        ↓
WP3 conducted scored campaign
        ↓
WP4 compact OTA replication
        ↓
WP5 deterministic analysis + artifact + manuscript closure
```

## Evidence boundary

Current accepted evidence establishes frozen controlled-RF attenuation states and locally verified P0/H-pilot implementation. It does **not** establish physical H, B1/W1 scientific effects, pump/hydraulic/agronomic performance, Siwa field performance, or generic rural-field generalization.
