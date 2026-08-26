# WellPulse — Milestone Status

Last updated: 2026-08-26 after WP2-H implementation preflight, Africa/Cairo

## Scientific work packages

| WP | Scope | Weight | Progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 100% | PASS — serious related-work/comparator benchmark attached |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 100% design work | PRE-SCORE COMPARATOR REVIEW OPEN |
| WP2 | RF Calibration & Measurement Validation | 15% | ACTIVE | **RF-STATE PASS; H DESIGN/IMPLEMENTATION PREFLIGHT PASS; PHYSICAL H + remaining pre-score gates OPEN** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0% | BLOCKED BY WP2 + comparator freeze + explicit scored authorization |
| WP4 | OTA External Replication | 15% | 0% | BLOCKED BY WP3 |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0% scientific closure | PREPARED, NOT EXECUTED |

Under gate-based credit, scientific weighted completion remains **20%** until WP2 closes. Design or implementation effort inside an unclosed WP2 does not earn partial scientific credit.

```text
WP0  ████████████████████  8/8
WP1  ████████████████████ 12/12 design work; comparator sufficiency under review
WP2  ───────── ACTIVE ───  RF states PASS; H implementation ready; physical H not yet measured
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

G0–G5 are non-scored enabling/calibration work. They do not add scientific percentage independently.

## WP2 sub-gates

| WP2 sub-gate | State | Canonical evidence / next requirement |
|---|---|---|
| Controlled RF profile + numeric Q0–Q3 | **PASS / FROZEN** | `RF_CALIBRATION_FREEZE_v1.md` + G5 ledger |
| Q0 explicit user-plane readiness safeguard | **PASS / FROZEN** | Decision D-016; attach/IP alone is insufficient |
| H calibration semantics | **PASS / FROZEN FOR EXECUTION** | `H_CALIBRATION_PLAN_v1.md`; Decision D-017 |
| H pilot implementation preflight | **PASS** | `evidence/local/wp2-h-preflight-latest.md`: 28/28 tests + compile + shell syntax + guards |
| Physical W1 backlog-drain calibration | **OPEN / ACTIVE FRONTIER** | exactly three valid non-scored W1 trials required |
| Remote Paho/runtime reproduction | **OPEN** | verify on physical pilot runtime |
| MQTT experimental-radio path | **OPEN** | route must traverse `tun_srsue` to `172.16.0.1` |
| Record identity/checksum preservation | **OPEN** | verify end-to-end in pilot bundle |
| B1/W1 implementation matching | **OPEN** | pre-score audit required |
| Evidence capture + clock alignment | **OPEN** | verify mandatory endpoint timestamps |
| Deterministic analysis reconstruction | **OPEN** | reconstruct non-scored pilot bundle without manual edits |
| B2 durable-client decision | **OPEN** | compact S2/S3 sensitivity amendment if B2 qualifies |
| Scored authorization | **BLOCKED** | remains `false` until all pre-score gates pass |

## Frozen RF state

- Q0 = **0 dB** — strong/stable reference.
- Q1 = **40 dB** — degraded but continuously connected.
- Q2 = **52 dB** — near-threshold/intermittent; clean isolated 20 s test = **6 replies / 12 misses**.
- Q3 = **55 dB** — effective application-data outage from first isolated valid test.
- Attenuation IDs: `1 33 2 34`, always changed together.
- Clean +41/+42/+49 boundary checks remained continuously connected.
- **No further attenuation sweep is authorized.**

## Invalid-evidence safeguard

The contaminated-period 48/50/52/54, 42/44/46/47 and first +41 observations remain preserved as invalid troubleshooting provenance caused by a stale LTE user-plane bearer. They are excluded from RF-state classification and must never be promoted into the scientific corpus.

Every scientific/non-scored calibration or scored run must begin with explicit Q0 end-to-end LTE user-plane PASS.

## H active gate

Exactly three valid non-scored `W1_OFFLINE_FIRST` trials are frozen:

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

At 1 record/s with TLS and the frozen Paho transport. Backlog drain completes only when the pre-restoration cohort is complete at the sink with matching identity/checksum **and** W1 durable pending cohort count is zero.

`H = max(120 s, ceil_to_30s(2 × empirical-nearest-rank p95 drain time))`.

With exactly three valid trials, p95 is the maximum observed valid drain time. If `H > 300 s`, stop and investigate; never cap it.

The implementation is locally verified but the three physical drain-time observations do not yet exist.

## Current operational state

- Historical G5 experiment `575d246e-8d01-4827-9a84-f4368d272cea`: **ABSENT / CLEANUP PASS**.
- No fresh WP2-H POWDER experiment is currently live.
- Automated `POWDER_SSH_PRIVATE_KEY` path is known bad because the stored Actions value has public-key form, not private-key form. This must be repaired or explicitly bypassed with the canonical local acceptance key before trusted automated remote execution; no private key/passphrase may enter Git/evidence/chat.
- Approved fallback `nuc1+nuc2` reservation: **2026-08-26 19:00–22:00 Africa/Cairo**.

## Comparator gate

B1 remains the matched same-Paho-Python comparator but is not the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` remains open. If B2 qualifies, prefer a compact S2/S3 sensitivity comparison rather than expanding the full primary matrix.

`scored_runs_authorized = false`.

## Exact next action

During the next fresh `srslte-controlled-rf` experiment:

1. verify profile revision and live node bindings;
2. establish the profile-authoritative LTE lifecycle;
3. pass Q0 user-plane readiness and confirm MQTT route through `tun_srsue`;
4. run exactly three valid **non-scored W1 H-calibration trials**;
5. reconstruct the bundle deterministically and freeze H only if `H <= 300 s`.

Do not run B1/W1 scored cells, do not start WP3, and do not reopen RF calibration.

## Critical path

```text
G5 numeric RF calibration PASS
        ↓
H plan + implementation preflight PASS
        ↓
3 valid physical W1 H calibration trials → freeze H
        ↓
remaining WP2 runtime/path/identity/clock/analysis gates
        ↓
close B2 durable-client comparator gate
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

Current accepted evidence establishes frozen controlled-RF attenuation states and a locally verified H-pilot implementation. It does **not** establish the physical H value, B1/W1 scientific effects, pump/hydraulic/agronomic performance, Siwa field performance, or generic rural-field generalization.