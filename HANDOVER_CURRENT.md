# WellPulse — Current Handover

Last updated: 2026-08-26 after independent pre-WP3 consortium review, approved P0 amendments, run-matrix reconciliation, and guarded local preflight, Africa/Cairo

## Standing rule

No material project state may exist only in chat. Decisions, results, blockers, evidence boundaries, milestone percentages, and the exact next action must be recoverable from GitHub and/or Drive.

## Executive state

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- WP0: **8/8 PASS**.
- WP1: **12/12 design complete**; comparator sufficiency and consortium P1 refinements remain open before scoring.
- WP2: **IN PROGRESS**.
- WP3: **0/30 — BLOCKED**.
- WP4: **0/15 — BLOCKED**.
- WP5: **0/20 scientific closure**.
- Scientific weighted completion: **20%**.
- `scored_runs_authorized = false`.

No consortium review, local test, calibration observation, or implementation preflight is a scored B1/W1 result.

## Independent consortium review

Canonical review:

`docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`

Verdict:

`PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS`

Approved P0 authority:

`experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`

The consortium did **not** recommend reopening RF calibration, replacing POWDER, expanding into 5G/O-RAN/mobility, adding a broad traffic-rate sweep, or rebuilding the work packages.

The sharpened scientific interpretation is that B1 may retain a bounded volatile QoS1 backlog across network-only disconnection while the client process remains alive. Therefore S1/S2 may legitimately show similar eventual completeness for B1 and W1. S3 is the clearest durability stress test because the gateway-process restart destroys volatile client state.

Consortium P1 analysis/claim recommendations remain open and must be resolved before scored authorization.

## Approved P0 amendments

### P0-1 — calibration outcome classification

**IMPLEMENTED + LOCALLY VERIFIED.**

H-calibration attempts are now classified as:

- `TECHNICALLY_INVALID` — predefined infrastructure/protocol failure; preserved; replacement allowed.
- `VALID_W1_RECOVERY_FAILURE` — technically valid adverse W1 recovery outcome; preserved; not replaceable as invalid; blocks H freeze.
- `VALID_W1_RECOVERY_SUCCESS` — successful technically valid outcome.

H requires exactly three successful outcomes. Extra successful trials are prohibited.

Authorities:

- `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`
- `scripts/finalize_wp_pwd01_h_calibration.py`

### P0-2 — MQTT run/session isolation

**IMPLEMENTED LOCALLY; PHYSICAL VERIFICATION OPEN.**

- deterministic run-unique publisher client ID;
- deterministic run-unique receiver client ID;
- deterministic run-unique topic namespace;
- fresh first connection must report `session_present=false`;
- client/topic/session evidence is preserved;
- independent runs must not reuse identities;
- the S3 intra-run gateway restart intentionally reuses the same run-specific gateway client identity.

Authorities:

- `src/wellpulse/transport.py`
- `scripts/wp_pwd01_h_sender.py`
- `scripts/wp_pwd01_h_receiver.py`

### P0-3 — S3 restart domain

**RULE FROZEN; NON-SCORED VERIFICATION OPEN.**

Before WP3:

- telemetry generation remains outside the gateway restart domain;
- generation continues at 1 record/s;
- only the gateway/client process restarts;
- W1 durable state survives the restart;
- B1 recreates volatile Paho state using the same run-specific client identity within that S3 run;
- source sequence remains continuous;
- restart start/end/downtime are recorded;
- no node reboot/power cycle substitutes for the gateway-process restart.

### P0-4 — B1 instrumentation

**IMPLEMENTED + LOCALLY VERIFIED; PHYSICAL EVIDENCE OPEN.**

B1 now records total publish calls, accepted publish calls including accepted disconnected QoS1 submissions, PUBACK callbacks, accepted-but-unacknowledged IDs/count, connection count, and latest session-present state.

`outstanding_mid_count` is a compatibility name for accepted-but-unacknowledged state only. It must not be described as exact Paho internal queue occupancy.

Scientific B1 completeness/loss is reconstructed from generated/received record identity and checksum evidence.

### P0-5 — record identity collision handling

**IMPLEMENTED + LOCALLY VERIFIED.**

`DurableQueue.enqueue()` now:

- treats an exact same record/payload/checksum as idempotent;
- raises an integrity error when the same `record_id` is reused with different content/checksum.

## Latest guarded local preflight

Canonical evidence:

`evidence/local/wp2-h-preflight-latest.md`

Latest tested SHA:

`e20da2fb186eeab047080cbd851f46c3c96c81f0`

Result:

- **34/34 tests PASS**;
- Python pilot scripts compile PASS;
- broker shell syntax PASS;
- frozen-state and P0 guards PASS;
- POWDER interaction NONE;
- scored-run interaction NONE.

This proves local implementation readiness only. It does not prove physical H, POWDER MQTT session/path behavior, or any B1/W1 scientific effect.

## Frozen RF state

Authority:

`experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`

- Q0 = **0 dB** — strong/stable.
- Q1 = **40 dB** — degraded but continuously connected.
- Q2 = **52 dB** — near-threshold/intermittent; clean isolated 20 s test produced 6 replies / 12 misses.
- Q3 = **55 dB** — effective application-data outage.
- attenuation IDs = `1 33 2 34`, always changed together.

**No further attenuation sweep is authorized.**

Before every scientific/non-scored calibration or scored run, Q0 must pass explicit end-to-end LTE user-plane readiness. Attach/IP alone is insufficient.

## H calibration — active physical frontier

Authority:

`experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`

Target successful non-scored W1 trial:

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Frozen rules:

- W1 only;
- 1 record/s;
- TLS enabled;
- Q0 = 0 dB;
- Q3 = 55 dB;
- no Q1/Q2 sweep;
- no B1/S3/scored comparison in H calibration;
- run-isolated MQTT clients/topic;
- fresh first session required;
- `cohort_cutoff_utc` is the exact final Q3 -> Q0 restoration timestamp;
- drain completes only after sink cohort completeness with matching identity/checksum and zero W1 durable pending cohort records;
- with three successful trials, empirical nearest-rank p95 equals the maximum observed successful drain time;
- `H = max(120 s, ceil_to_30s(2 × p95))`;
- if H > 300 s, STOP AND INVESTIGATE; never cap.

A `VALID_W1_RECOVERY_FAILURE` blocks H freeze and cannot be replaced as technical invalidity.

## Current operational blockers

1. No fresh live WP2-H POWDER experiment exists now.
2. Automated `POWDER_SSH_PRIVATE_KEY` path remains known bad because the stored Actions value was diagnosed as public-key-form rather than private-key-form.

Repair or explicitly bypass the SSH automation path using the canonical local acceptance key. Never place a private key or passphrase in Git, evidence, or chat.

Fallback reservation remains:

**2026-08-26 19:00–22:00 Africa/Cairo**

for `nuc1+nuc2`.

Use it for unfinished WP2 validation, not RF hunting.

## Remaining pre-score gates

1. execute the amended physical H calibration and freeze H;
2. physically verify MQTT run/session isolation;
3. reproduce frozen Paho/runtime configuration remotely;
4. verify MQTT traverses the experimental LTE path via `tun_srsue`;
5. verify end-to-end record identity/checksum on pilot evidence;
6. verify clock/evidence alignment;
7. reconstruct a non-scored pilot deterministically without manual spreadsheet edits;
8. audit B1/W1 matching using corrected B1 instrumentation;
9. verify S3 restart-domain separation non-scored;
10. close B2 durable-client comparator decision;
11. resolve consortium P1 analysis/claim amendments;
12. repair or explicitly bypass the SSH automation path before trusted scored automation.

Use the same valid H pilot bundle to close as many of gates 2–8 as the evidence legitimately supports. Do not add experiments merely to increase experiment count.

## Exact next action

At the next fresh `srslte-controlled-rf` experiment, and only within WP2:

1. capture experiment/profile identity and fresh live bindings;
2. establish EPC/eNB + UE lifecycle;
3. pass Q0 end-to-end user-plane readiness;
4. verify route to `172.16.0.1` uses `tun_srsue`;
5. launch H sender/receiver with one unique run ID per attempted trial and verify fresh MQTT session isolation;
6. continue until exactly three `VALID_W1_RECOVERY_SUCCESS` trials exist, replacing only predefined `TECHNICALLY_INVALID` attempts;
7. if any `VALID_W1_RECOVERY_FAILURE` occurs, stop H freeze and investigate;
8. run `finalize_wp_pwd01_h_calibration.py` across all attempted trial directories;
9. freeze H only if the frozen rule passes and H <= 300 s;
10. use the same physical bundle to close other WP2 validation gates where justified.

Do **not** start WP3. Do **not** execute B1/W1/B2 scored cells. Do **not** reopen RF calibration. Do **not** change `scored_runs_authorized` until all pre-score gates pass.

## Canonical read order

1. `HANDOVER_CURRENT.md`
2. `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`
3. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
4. `docs/MILESTONE_STATUS.md`
5. `docs/STATUS.md`
6. `docs/DECISIONS.md`
7. `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`
8. `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`
9. `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`
10. `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`
11. `evidence/local/wp2-h-preflight-latest.md`
12. `experiments/WP-PWD01/protocol.md`
13. `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`
14. `experiments/WP-PWD01/analysis-plan.md`
15. `experiments/WP-PWD01/evidence-schema.md`
16. `experiments/WP-PWD01/randomization-plan.csv`
17. `experiments/WP-PWD01/run-matrix.yaml`
18. `powder/MANUAL_GOLDEN_PATH.md`

Never infer future node roles from prior runs. Never persist secrets, private keys, passphrases, RPC tokens, credential blocks, or raw credential-bearing manifests.
