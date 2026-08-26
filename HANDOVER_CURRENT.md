# WellPulse — Current Handover

Last updated: 2026-08-26 after independent pre-WP3 consortium review, approved P0 amendments, and P0 local preflight, Africa/Cairo

## Standing handover rule

No material project state may exist only in chat. Decisions, results, artifacts, blockers, evidence boundaries, milestone percentages and the exact next action must be recoverable from GitHub and/or Drive.

## Executive state

- FIT IoT-LAB scientific evidence layer: **FINAL PASS**.
- POWDER G0–G4: **PASS**.
- POWDER G5 RF impairment/control + numeric RF-state calibration: **PASS / FROZEN**.
- Old G5 experiment UUID `575d246e-8d01-4827-9a84-f4368d272cea`: **ABSENT / CLEANUP PASS**.
- WP0 Novelty & Venue Lock: **8/8 PASS**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design complete**; comparator sufficiency and consortium P1 analysis refinements remain open pre-score.
- WP2 RF Calibration & Measurement Validation: **IN PROGRESS**.
  - numeric RF-state calibration: **PASS / FROZEN**;
  - common recovery-horizon `H` design: **FROZEN AS P0-AMENDED**;
  - W1 H-calibration implementation: **IMPLEMENTED + LOCALLY VERIFIED**;
  - consortium P0 code amendments: **IMPLEMENTED + LOCAL PREFLIGHT PASS**;
  - physical W1 H-calibration observations: **NOT YET EXECUTED**;
  - physical MQTT isolation/runtime/path/evidence gates: **OPEN**;
  - S3 restart-domain verification: **OPEN PRE-SCORE**.
- WP3: **0/30 — BLOCKED** by WP2 + comparator freeze + explicit scored authorization.
- WP4: **0/15 — BLOCKED** by WP3.
- WP5: **0/20 scientific closure**.
- Gate-based scientific weighted completion remains **20%** until WP2 closes.
- `scored_runs_authorized = false`.

No G5 calibration observation, H calibration implementation test, consortium review, or local P0 test is a scored B1/W1 scientific result.

## Independent pre-WP3 consortium review

Canonical review:

`docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`

Verdict:

`PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS`

The project remains scientifically viable. The review did **not** recommend reopening RF calibration, replacing POWDER, expanding into O-RAN/5G/mobility, adding a broad traffic-rate grid, or rebuilding the WP structure.

The review sharpened the central scientific interpretation: with a live Paho Python process, B1 can retain a bounded volatile QoS1 backlog across network-only disconnection. Therefore S1/S2 may legitimately show near-complete eventual delivery for both B1 and W1. The clearest record-durability contrast is expected when volatile client state is destroyed in S3. Null or small S1/S2 completeness differences are therefore informative rather than protocol failures.

Approved P0 amendment authority:

`experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`

P1 recommendations from the consortium remain **not yet fully frozen into the scored protocol** and must be resolved before `scored_runs_authorized=true`.

## P0 amendments — current implementation state

### P0-1 — H technical invalidity vs adverse W1 outcome

**IMPLEMENTED / LOCALLY VERIFIED.**

H calibration now distinguishes:

- `TECHNICALLY_INVALID` — predefined infrastructure/protocol failure; preserved and replaceable;
- `VALID_W1_RECOVERY_FAILURE` — technically valid adverse W1 recovery outcome; preserved, not replaceable as invalid, blocks H freeze;
- `VALID_W1_RECOVERY_SUCCESS` — successful technically valid calibration outcome.

H requires exactly three successful outcomes. Extra successful trials are not authorized. A valid adverse W1 outcome cannot be erased by replacement.

Authorities:

- `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`;
- `scripts/finalize_wp_pwd01_h_calibration.py`.

### P0-2 — MQTT run/session isolation

**IMPLEMENTED LOCALLY; PHYSICAL VERIFICATION OPEN.**

Implemented helpers generate deterministic run-unique MQTT client identities and run-isolated topic namespaces. H sender and receiver use separate run-unique client identities and the same run-unique topic. A fresh H client must observe `session_present=false` on its first connection or the trial is technically invalid.

Authorities:

- `src/wellpulse/transport.py`;
- `scripts/wp_pwd01_h_sender.py`;
- `scripts/wp_pwd01_h_receiver.py`.

The same isolation principle is mandatory for future scored runs. The only intentional reuse of a gateway client identity is the intra-run gateway-process restart in S3.

### P0-3 — S3 restart-domain separation

**RULE FROZEN; NON-SCORED IMPLEMENTATION VERIFICATION OPEN.**

Before scored execution, prove that:

- telemetry generation remains outside the gateway restart domain and continues at 1 record/s;
- only the gateway/client process is restarted;
- W1 durable state survives that restart;
- B1 recreates volatile Paho state using the same run-specific client identity within the S3 run;
- source record sequence/identity remains continuous;
- restart timestamps/downtime are captured;
- no node reboot/power cycle substitutes for the gateway-process restart.

### P0-4 — B1 accepted-message instrumentation

**IMPLEMENTED / LOCALLY VERIFIED; PHYSICAL EVIDENCE OPEN.**

`PahoQoS1Session` now records total publish calls, accepted publish calls including disconnected QoS1 submissions, PUBACK callbacks, accepted-but-unacknowledged IDs/count, connection count and latest session-present state.

`outstanding_mid_count` is retained only as a compatibility name for accepted-but-unacknowledged state. It must **not** be described as exact internal Paho queue occupancy.

Scientific B1 completeness/loss is reconstructed from generated/received record identity and checksum evidence, not this internal counter alone.

### P0-5 — record identity collision handling

**IMPLEMENTED / LOCALLY VERIFIED.**

`DurableQueue.enqueue()` no longer silently ignores conflicting reuse of `record_id`.

- exact same canonical payload/checksum with the same ID is idempotent;
- same ID with different payload/checksum raises an integrity error.

Authority: `src/wellpulse/store.py`; test: `tests/test_store.py`.

## Latest local preflight

Canonical evidence:

`evidence/local/wp2-h-preflight-latest.md`

Latest P0 preflight tested GitHub SHA:

`e34d16fc813f0c0f6fc5824286df0b33bbc4f007`

Result:

- **34/34 tests PASS**;
- Python pilot scripts compile PASS;
- broker shell syntax PASS;
- frozen-state guards PASS;
- POWDER interaction NONE;
- scored-run interaction NONE.

This proves local implementation readiness only. It does not establish physical H, MQTT path/session behavior on POWDER, or any B1/W1 scientific effect.

## Canonical repositories and workspaces

- GitHub: `aayoubMSA/WellPulse`.
- Drive project root `P12_WellPulse`: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`.
- Drive validation workspace `00_Validation_Workspace`: `1SydHCA2jlkatxdGgUtJ1P8atgyi8_ta3`.
- Drive raw evidence `02_RAW_EVIDENCE`: `11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`.
- Drive handover folder `WellPulse Handover`: `1Du4j_YkMLvQjWJCxV5zqxxK6OGG2Q0hA`.
- Clean G5 snapshot: `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`.
- Consortium review: `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`.
- P0 amendment: `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`.
- WP2-H calibration plan: `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`.
- Latest preflight: `evidence/local/wp2-h-preflight-latest.md`.

## Frozen scientific design

Canonical base protocol remains `experiments/WP-PWD01/protocol.md` v0.4, subject to the explicit pre-score P0 amendment above and still-open P1/comparator decisions before scoring.

Primary comparison remains:

- `B1_MQTT_QOS1`: Paho Python MQTT v3.1.1, QoS1, TLS on scored path, automatic reconnect, `clean_session=False`, volatile client state, no application-level disk durability/reconciliation.
- `W1_OFFLINE_FIRST`: same low-level Paho session plus SQLite durable application queue, stable record identity/checksum, replay, idempotent receiver and reconciliation.

Frozen low-level parameters: `paho-mqtt==2.1.0`, keepalive 60 s, reconnect 1–8 s, outgoing queue 4096, inflight 20.

Comparator caveat remains open: B1 is the clean matched same-implementation comparator but not the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` must be qualified/frozen before scoring if retained. Preferred direction remains a compact S2/S3 sensitivity amendment rather than a full three-arm matrix.

## G5 accepted experiment state and teardown

Historical non-scored G5 experiment:

- `WP-G5-RF-CAL`;
- UUID `575d246e-8d01-4827-9a84-f4368d272cea`;
- profile `srslte-controlled-rf`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`;
- historical live binding `enb1 -> nuc1`, `rue1 -> nuc2`;
- UE `172.16.0.2`, EPC SGi `172.16.0.1` after clean bearer restoration;
- attenuation path IDs `1 33 2 34`, always changed together.

Historical bindings **must never be assumed for a new experiment**. Capture and verify live logical-to-physical bindings every time.

The old G5 experiment is absent and requires no further teardown.

Fallback reservation remains available for `nuc1+nuc2` on **2026-08-26 19:00–22:00 Africa/Cairo**. Use it for unfinished WP2 validation, not RF hunting.

## RF calibration — FROZEN

Numeric authority: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.

| State | Programmed attenuation | Meaning | Accepted observation |
|---|---:|---|---|
| Q0 | **0 dB** | strong/stable | ~-60 dBm RSRP, SNR ~40–45 dB, BLER 0; clean user-plane PASS |
| Q1 | **40 dB** | degraded but continuously connected | ~-100 dBm RSRP, SNR ~18–19 dB; continuous ping |
| Q2 | **52 dB** | near-threshold/intermittent | clean isolated 20 s window: **6 replies / 12 misses**; clean Q0 recovery |
| Q3 | **55 dB** | effective application-data outage | isolated valid outage with immediate recovery after Q0 reset |

Attenuation IDs: `1 33 2 34`, changed together.

**No more attenuation sweep is authorized or scientifically useful.**

## Critical RF invalidity safeguard

Repeated severe RLF/re-attach testing previously produced a stale user-plane bearer while the UE still appeared attached and had an IP. Contaminated exploratory observations remain provenance only and are excluded from canonical RF classification.

Before every future scientific/non-scored calibration or scored run, Q0 must pass an explicit end-to-end user-plane readiness check through the experimental radio path. Attached state or assigned IP alone is insufficient.

## WP2-H recovery-horizon design — FROZEN AS AMENDED

Authority: `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`.

Target successful calibration schedule:

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Frozen rules:

- W1 only;
- 1 record/s;
- TLS enabled;
- Q0 = 0 dB;
- Q3 = 55 dB;
- all four attenuators move together;
- no Q1/Q2 sweep;
- no B1/S3/scored comparison in this gate;
- deterministic run-isolated MQTT clients/topic;
- fresh first connection requires no prior session state;
- `cohort_cutoff_utc` is exact final Q3 -> Q0 restoration;
- drain completes only when the cohort is complete at sink with matching identity/checksum and W1 durable pending cohort reaches zero;
- with three successful trials, nearest-rank p95 equals the maximum observed successful drain time;
- `H = max(120 s, ceil_to_30s(2 × p95))`;
- if `H > 300 s`, STOP AND INVESTIGATE; never cap;
- valid adverse W1 recovery outcome blocks H freeze and is not replaceable as technical invalidity.

## Current execution blockers

1. **No fresh live WP2-H POWDER experiment exists now.** A new `srslte-controlled-rf` experiment must be instantiated during an available reservation and its live bindings verified.
2. **Automated SSH private-key path remains known bad.** `POWDER_SSH_PRIVATE_KEY` in Actions was diagnosed as public-key-form rather than private-key-form. Repair or explicitly bypass with the canonical local acceptance key. Never place private key/passphrase material in Git/evidence/chat.

These are execution-access blockers, not scientific evidence against the design.

## Remaining pre-score work

Do not authorize scored runs yet. Material open gates:

1. physically execute the amended three-successful-trial W1 H calibration and freeze `H`;
2. verify fresh MQTT publisher/receiver session isolation physically on the H path;
3. reproduce frozen Paho/runtime configuration remotely;
4. verify MQTT payload traverses `tun_srsue` / experimental cellular path rather than control network;
5. verify end-to-end identity/checksum and fail-closed collision semantics on pilot evidence;
6. verify evidence capture and clock alignment;
7. run deterministic analysis on a non-scored pilot bundle without manual spreadsheet edits;
8. audit B1/W1 implementation matching using the corrected B1 instrumentation semantics;
9. non-scored verify S3 restart-domain separation;
10. close B2 durable-client comparator decision/amendment;
11. resolve consortium P1 analysis/claim amendments before scored authorization;
12. repair or explicitly bypass the known-bad automated POWDER SSH path before trusted scored automation.

Use the same valid H pilot bundle to close gates 2–8 where evidence is sufficient; do not create extra experiments merely to increase experiment count.

## Exact next action

At the next fresh `srslte-controlled-rf` experiment, and **only within WP2**:

1. capture experiment/profile identity and verify live logical-to-physical bindings;
2. start the profile-authoritative EPC/eNB and UE lifecycle;
3. pass explicit Q0 LTE user-plane readiness;
4. verify route to `172.16.0.1` uses `tun_srsue`;
5. launch the H receiver/sender with one unique run ID per attempted trial and confirm fresh first-session isolation evidence;
6. execute the amended H calibration until exactly three `VALID_W1_RECOVERY_SUCCESS` trials exist, replacing only predefined `TECHNICALLY_INVALID` attempts;
7. if any `VALID_W1_RECOVERY_FAILURE` occurs, stop H freeze and investigate rather than replacing it;
8. run `finalize_wp_pwd01_h_calibration.py` across all attempted trial directories;
9. if the resulting H is `<= 300 s`, freeze it canonically; if H is `> 300 s`, stop and investigate without capping;
10. use the same physical bundle to close other WP2 runtime/path/identity/clock/analysis gates where justified.

Do **not** start WP3. Do **not** execute B1/W1/B2 scored cells. Do **not** reopen RF attenuation calibration. Do **not** change `scored_runs_authorized` until all remaining pre-score gates pass.

## Reproducibility read order

1. `HANDOVER_CURRENT.md`
2. `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`
3. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
4. `docs/handovers/2026-08-26_G5_RF_CALIBRATION_HANDOVER.md`
5. `docs/MILESTONE_STATUS.md`
6. `docs/STATUS.md`
7. `docs/DECISIONS.md`
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
