# Project Validation Status

## Current state — 2026-08-26 after G5 RF-state freeze, Africa/Cairo

- Canonical GitHub repository and Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS**; Grenoble A8; 18/18 final cells reconciled.
- POWDER G0–G4: **PASS**.
- POWDER G5 RF control + numeric calibration: **PASS**.
- WP2 RF Calibration & Measurement Validation: **IN PROGRESS**; numeric Q0–Q3 calibration is frozen, but H and remaining pre-score measurement/evidence gates remain open.
- Scientific weighted completion remains **20%** under gate-based credit until WP2 closes.
- `scored_runs_authorized = false`.

## G5 accepted calibration

Canonical freeze: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.
Canonical ledger: `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`.
Clean handover snapshot: `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`.

Frozen programmed attenuation values:

- Q0 = **0 dB** — strong/stable reference.
- Q1 = **40 dB** — degraded but continuously connected.
- Q2 = **52 dB** — near-threshold/intermittent; clean 20 s window = **6 replies / 12 misses**.
- Q3 = **55 dB** — effective application-data outage from the first isolated valid outage test.

Clean post-reset boundary checks show +41, +42 and +49 remain continuously connected, while +52 is intermittent. No additional RF sweep is authorized.

## G5 live-run metadata

- experiment `WP-G5-RF-CAL`;
- UUID `575d246e-8d01-4827-9a84-f4368d272cea`;
- profile `srslte-controlled-rf`, revision `a6da96560b6526dc6816761282722c996418fd8c`;
- binding `enb1 -> nuc1`, `rue1 -> nuc2`;
- UE `172.16.0.2`, EPC SGi `172.16.0.1` after clean bearer restoration;
- attenuation IDs `1 33 2 34`, always changed together;
- final commanded state at handover: all four IDs restored to 0 dB;
- last explicit Q0 health check: **3/3 replies, 0% loss**.

If this experiment is still active, sanitize/preserve any desired ephemeral logs, terminate it cleanly and verify zero usage before moving on.

## Technical invalidity rule learned in G5

Repeated severe RLF/re-attach testing can leave the LTE user-plane bearer stale even while the UE appears attached and has an IP. The contaminated 48/50/52/54, 42/44/46/47 and first +41 classifications are retained for provenance but excluded from canonical RF-state evidence.

Every future scored run/block must pass explicit Q0 user-plane readiness before scientific execution. Attach/IP alone is insufficient.

## Scientific programme state

- WP0 Novelty & Venue Lock: **8/8 complete**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design work complete**, comparator sufficiency remains **OPEN FOR PRE-SCORE REVIEW**.
- WP2 RF Calibration & Measurement Validation: **ACTIVE**; RF numeric sub-gate PASS, overall gate not closed.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — BLOCKED BY WP2 + comparator freeze + scored authorization**.
- WP4 OTA External Replication: **0/15 — BLOCKED BY WP3**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**.

## Comparator gate

B1 remains the same-implementation Paho-Python matched comparator but must not be described as the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` remains under review. Exact B2 semantics and any compact S2/S3 sensitivity amendment remain unfrozen.

No scored run may begin until this comparator gate and the remaining WP2 gates are explicitly closed.

## Immediate next stage

1. Finish safe G5 teardown if still live; no further RF hunting.
2. Stay in WP2 and calibrate/freeze common recovery horizon `H` using the smallest valid non-scored W1 recovery pilot.
3. Close remote runtime, B1/W1 matching, identity/checksum, clock/evidence, and analysis-pilot gates.
4. Close B2 comparator amendment and only then consider explicit scored authorization.

An approved `nuc1+nuc2` fallback reservation remains available for **2026-08-26 19:00–22:00 Africa/Cairo**; reserve it for unfinished WP2 validation, not repeat calibration.

## Evidence boundary

Accepted G5 evidence proves controlled physical-RF attenuation states and qualified user-plane behavior on POWDER LTE. It does not prove WellPulse-vs-MQTT scientific effects, pump mechanics, hydraulics, groundwater, agronomy, Siwa field performance or generic rural-field generalization.