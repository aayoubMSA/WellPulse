# Project Validation Status

## Current state — 2026-08-26 after independent pre-WP3 consortium review and approved P0 amendments, Africa/Cairo

- Canonical GitHub repository and Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS**; Grenoble A8; 18/18 final cells reconciled.
- POWDER G0–G4: **PASS**.
- POWDER G5 RF control + numeric calibration: **PASS / FROZEN**.
- Old G5 experiment UUID `575d246e-8d01-4827-9a84-f4368d272cea`: **ABSENT / CLEANUP PASS**.
- Independent consortium review: **PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS**.
- Approved P0 amendment: `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`.
- WP2 RF Calibration & Measurement Validation: **IN PROGRESS**.
- WP2-H recovery-horizon design: **FROZEN AS P0-AMENDED**.
- WP2-H implementation + P0 code amendments: **IMPLEMENTED + LOCALLY VERIFIED**.
- Latest completed local preflight evidence: `evidence/local/wp2-h-preflight-latest.md` — **34/34 tests PASS**, Python compile PASS, broker shell syntax PASS, frozen-state guards PASS; POWDER interaction NONE; scored-run interaction NONE.
- Physical W1 H calibration: **NOT YET EXECUTED**.
- Scientific weighted completion remains **20%** until WP2 closes.
- `scored_runs_authorized = false`.

## Frozen RF calibration

Canonical freeze: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.

- Q0 = **0 dB** — strong/stable reference.
- Q1 = **40 dB** — degraded but continuously connected.
- Q2 = **52 dB** — near-threshold/intermittent; clean isolated 20 s window = **6 replies / 12 misses**.
- Q3 = **55 dB** — effective application-data outage.
- Attenuation IDs: `1 33 2 34`, always changed together.
- **No further attenuation sweep is authorized.**

## Mandatory Q0 readiness rule

Before every future scientific/non-scored calibration or scored run, Q0 must pass explicit end-to-end LTE user-plane readiness through the experimental path. Attach/IP alone is insufficient.

## Approved P0 controls

### H outcome classification

A calibration attempt is now classified as one of:

- `TECHNICALLY_INVALID` — predefined infrastructure/protocol failure; preserved and replaceable;
- `VALID_W1_RECOVERY_FAILURE` — technically valid adverse W1 outcome; preserved, not replaceable as invalid, blocks H freeze;
- `VALID_W1_RECOVERY_SUCCESS` — successful technically valid outcome.

H requires exactly three successful outcomes. Extra successful trials are not authorized.

### MQTT run/session isolation

H sender/receiver now use deterministic run-unique client identities and a run-unique topic namespace. Fresh first connections must show `session_present=false`; otherwise the attempt is technically invalid.

Physical verification of this rule on POWDER is still OPEN.

### S3 restart domain

The rule is frozen but non-scored physical/implementation verification remains OPEN:

- telemetry generator stays outside the gateway restart domain and continues at 1 Hz;
- only the gateway/client process restarts;
- W1 durable state survives;
- B1 recreates the volatile client with the same run-specific client identity inside the same S3 run;
- source record sequence remains continuous;
- restart timestamps/downtime are recorded;
- no node reboot/power cycle substitutes for the gateway-process restart.

### B1 instrumentation

B1 now records accepted QoS1 publishes, including accepted disconnected submissions, PUBACK callbacks, and accepted-but-unacknowledged state. This must not be described as exact Paho internal queue occupancy.

### Record identity integrity

`DurableQueue.enqueue()` now fails closed if an existing `record_id` is reused with different content/checksum. Exact duplicate content remains idempotent.

## WP2-H active gate

The active physical scientific gate remains non-scored W1 recovery-horizon calibration.

Target successful trial schedule:

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Frozen H rule:

`H = max(120 s, ceil_to_30s(2 × p95))`

With exactly three successful trials, empirical nearest-rank p95 is the maximum of the three observed successful drain times. If H exceeds 300 s, **STOP AND INVESTIGATE; do not cap**.

## Remaining execution blockers

1. No fresh live POWDER experiment exists now; a new `srslte-controlled-rf` experiment must be instantiated during an available reservation and its live bindings verified.
2. Automated `POWDER_SSH_PRIVATE_KEY` path remains known bad because the stored Actions value has public-key form rather than private-key form. Repair or explicitly bypass using the canonical local acceptance key. No private key/passphrase may enter Git/evidence/chat.

Fallback reservation remains available for `nuc1+nuc2` on **2026-08-26 19:00–22:00 Africa/Cairo**.

## Scientific programme state

- WP0 Novelty & Venue Lock: **8/8 PASS**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design complete**; comparator sufficiency and consortium P1 refinements remain OPEN PRE-SCORE.
- WP2 RF Calibration & Measurement Validation: **ACTIVE**.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — BLOCKED**.
- WP4 OTA External Replication: **0/15 — BLOCKED**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**.

## Remaining pre-score work

1. execute the amended physical H calibration and freeze H;
2. physically verify MQTT run/session isolation on the H path;
3. reproduce frozen Paho/runtime configuration remotely;
4. verify MQTT traverses `tun_srsue` / experimental radio path;
5. verify identity/checksum evidence physically;
6. verify clock/evidence alignment;
7. reconstruct a non-scored pilot deterministically without manual spreadsheet edits;
8. audit B1/W1 implementation matching with corrected B1 instrumentation;
9. verify the S3 restart domain non-scored;
10. close the B2 durable-client comparator decision;
11. resolve consortium P1 analysis/claim amendments;
12. repair or explicitly bypass the known-bad SSH automation path before trusted scored automation.

## Exact next action

At the next fresh `srslte-controlled-rf` experiment:

1. capture live bindings and verify profile/runtime identity;
2. establish LTE and pass explicit Q0 user-plane readiness;
3. verify route through `tun_srsue`;
4. verify fresh MQTT session isolation;
5. execute the amended W1 H calibration until exactly three `VALID_W1_RECOVERY_SUCCESS` trials exist, replacing only predefined `TECHNICALLY_INVALID` attempts;
6. if any `VALID_W1_RECOVERY_FAILURE` occurs, stop and investigate rather than replacing it;
7. reconstruct all attempted trials deterministically and freeze H only if the frozen rule passes.

Do not open WP3, do not run B1/W1/B2 scored pairs, and do not change `scored_runs_authorized` until every remaining pre-score gate closes.

## Evidence boundary

Accepted evidence proves controlled physical-RF attenuation states and locally verified P0/H-pilot implementation. It does **not** yet prove physical H, WellPulse-vs-MQTT scientific effects, pump mechanics, hydraulics, groundwater, agronomy, Siwa field performance, or generic rural-field generalization.
