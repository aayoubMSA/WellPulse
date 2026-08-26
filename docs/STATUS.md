# Project Validation Status

## Current state — 2026-08-26 after WP2-H implementation preflight, Africa/Cairo

- Canonical GitHub repository and Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS**; Grenoble A8; 18/18 final cells reconciled.
- POWDER G0–G4: **PASS**.
- POWDER G5 RF control + numeric calibration: **PASS**.
- Old G5 experiment UUID `575d246e-8d01-4827-9a84-f4368d272cea`: **ABSENT / CLEANUP GATE PASS** as of 2026-08-26T00:14:52Z; no scientific action occurred during cleanup.
- WP2 RF Calibration & Measurement Validation: **IN PROGRESS**.
- WP2-H recovery-horizon calibration design: **FROZEN** in `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md` and Decision D-017.
- WP2-H pilot implementation: **IMPLEMENTED + LOCALLY VERIFIED**, but **not yet physically executed on POWDER**.
- Dedicated preflight evidence: `evidence/local/wp2-h-preflight-latest.md` — **28/28 tests PASS**, Python compile PASS, broker shell syntax PASS, frozen-state guards PASS on tested SHA `d8ab08df5f4cac7394e16c78097b8dc2ca192649`.
- Scientific weighted completion remains **20%** under gate-based credit until WP2 closes.
- `scored_runs_authorized = false`.

## Frozen RF calibration

Canonical freeze: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.  
Canonical ledger: `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`.  
Clean G5 handover: `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`.

Frozen programmed attenuation values:

- Q0 = **0 dB** — strong/stable reference.
- Q1 = **40 dB** — degraded but continuously connected.
- Q2 = **52 dB** — near-threshold/intermittent; clean 20 s window = **6 replies / 12 misses**.
- Q3 = **55 dB** — effective application-data outage from the first isolated valid outage test.

All attenuation IDs `1 33 2 34` must change together. Clean post-reset boundary checks show +41, +42 and +49 remain continuously connected, while +52 is intermittent. **No additional RF sweep is authorized.**

## Mandatory Q0 readiness rule

Repeated severe RLF/re-attach testing can leave the LTE user-plane bearer stale even while the UE appears attached and retains an IP. The contaminated 48/50/52/54, 42/44/46/47 and first +41 observations remain preserved as invalid troubleshooting evidence and are excluded from canonical RF-state classification.

Before every future scientific/non-scored calibration or scored run, Q0 must pass explicit end-to-end LTE user-plane readiness through the experimental path. Attach/IP alone is insufficient.

## WP2-H active gate

The only active scientific gate is the non-scored W1 recovery pilot required to freeze common horizon `H`.

Frozen calibration design:

- exactly **3 valid W1 hard-outage calibration trials**;
- workload = **1 record/s**;
- readiness/warm-up 30 s -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain;
- TLS enabled on the MQTT calibration path;
- p95 estimator = empirical nearest-rank; with n=3 this is the maximum valid observed drain time;
- backlog drain completes only after both sink cohort completeness and zero W1 durable pending cohort records;
- `H = max(120 s, ceil_to_30s(2 × p95))`;
- if calculated `H > 300 s`, **STOP AND INVESTIGATE; do not cap**.

Implemented components:

- `src/wellpulse/horizon.py` — deterministic H calculation;
- `src/wellpulse/powder_w1.py` — non-blocking durable W1 replay above frozen Paho QoS1;
- `scripts/wp_pwd01_h_sender.py` — Q0 readiness, 1 Hz generation, independent RF controller, Q3/Q0 timing, queue evidence;
- `scripts/wp_pwd01_h_receiver.py` — TLS MQTT sink attempt ledger with SHA-256;
- `scripts/finalize_wp_pwd01_h_calibration.py` — deterministic sink/queue drain reconstruction and H calculation;
- `powder/wp2_h_epc_broker.sh` — ephemeral TLS broker bootstrap with private keys excluded from evidence.

## Remaining execution blocker for H

There is currently no live POWDER experiment. A fresh `srslte-controlled-rf` experiment must be instantiated in an available reservation, and its live bindings must be verified rather than inherited from G4/G5.

The repository's automated SSH secret path is also **known bad**: the current `POWDER_SSH_PRIVATE_KEY` diagnostic shows a public-key value rather than a private key. Do not trust automated remote execution through that secret until it is repaired or explicitly bypassed with the canonical local acceptance key. No private key/passphrase may enter Git or evidence.

An approved `nuc1+nuc2` fallback reservation remains available for **2026-08-26 19:00–22:00 Africa/Cairo** and should be used for this unfinished WP2 validation, not RF hunting.

## Scientific programme state

- WP0 Novelty & Venue Lock: **8/8 PASS**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design complete**, comparator sufficiency remains **OPEN PRE-SCORE**.
- WP2 RF Calibration & Measurement Validation: **ACTIVE**; RF-state sub-gate PASS, H physical calibration OPEN, remaining pre-score gates OPEN.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — BLOCKED**.
- WP4 OTA External Replication: **0/15 — BLOCKED**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**.

## Comparator gate

B1 remains the matched same-Paho-Python comparator but must not be represented as the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` remains an open pre-score gate; if it qualifies, prefer a compact S2/S3 sensitivity comparison rather than expanding the full primary matrix.

## Exact next action

At the next fresh `srslte-controlled-rf` experiment:

1. capture live bindings and verify profile/runtime identity;
2. establish LTE and pass explicit Q0 user-plane readiness;
3. run the frozen **three-trial non-scored W1 H calibration** only;
4. reconstruct the bundle deterministically and freeze H if `H <= 300 s`;
5. preserve any invalid trial as invalid evidence and replace only for documented technical invalidity.

Do not open WP3, do not run B1/W1 scored pairs, and do not change `scored_runs_authorized` until every remaining pre-score gate closes.

## Evidence boundary

Accepted evidence proves controlled physical-RF attenuation states and locally verified H-pilot implementation. It does **not** yet prove the physical H value, WellPulse-vs-MQTT scientific effects, pump mechanics, hydraulics, groundwater, agronomy, Siwa field performance, or generic rural-field generalization.