# Project Validation Status

## Current state — 2026-08-26 after consortium P0/P1 freeze and B2 qualification, Africa/Cairo

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Consortium review: **PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS**.
- P0 amendment: **IMPLEMENTED / LOCAL PASS; physical safeguards still open where applicable**.
- P1 amendment: **FROZEN PRE-SCORE**.
- B2 durable-client local semantics: **PASS 3/3 / QUALIFIED AS COMPACT SENSITIVITY COMPARATOR**.
- WP2: **IN PROGRESS — physical H is the active scientific frontier**.
- WP3/WP4: **BLOCKED**.
- WP5: **not scientifically closed**.
- Scientific weighted completion: **20%**.
- `scored_runs_authorized = false`.

## Frozen scientific interpretation

- S0: healthy-path integrity equivalence + overhead sanity.
- S1: network-only integrity primary; recovery/overhead secondary.
- S2: network-only integrity primary while volatile client state survives; recovery/overhead secondary.
- S3: primary process-state durability/integrity stress.
- Primary inferential endpoint remains unique primary-cohort completeness at common H.
- Precision stopping remains completeness-only.
- No separately powered confirmatory recovery-advantage claim.
- Use cross-testbed consistency/triangulation, not broad transportability.
- Claim remains bounded to 1 Hz low-rate telemetry.

## Frozen RF state

- Q0 = **0 dB**.
- Q1 = **40 dB**.
- Q2 = **52 dB**.
- Q3 = **55 dB**.
- attenuation IDs = `1 33 2 34`, always together.
- no additional RF sweep authorized.

Every scientific/non-scored/scored run requires Q0 end-to-end LTE user-plane PASS; attach/IP alone is insufficient.

## H active gate

Target successful non-scored W1 trial:

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Outcome classes:

- `TECHNICALLY_INVALID` — replaceable only for predefined technical invalidity.
- `VALID_W1_RECOVERY_FAILURE` — adverse valid evidence; not replaceable; blocks H freeze.
- `VALID_W1_RECOVERY_SUCCESS` — exactly three required.

Common horizon:

`H = max(120 s, ceil_to_30s(2 × p95))`

With n=3 successful trials, p95 is the maximum observed drain. H is frozen once before scoring and used identically for all arms/scenarios. If H > 300 s, stop and investigate; never cap.

## B2 comparator state

Local non-scored semantics evidence:

`evidence/local/wp2-b2-semantics-latest.md`

Exact qualified B2:

- Eclipse Paho Java 1.2.5;
- MQTT v3.1.1;
- QoS1;
- `cleanSession=false`;
- file-backed persistence;
- persistent disconnected buffer size 4096;
- delete-oldest disabled.

Result: three independent trials each preserved and recovered **5/5 unique records with 0 missing and 0 duplicates** across broker outage + abrupt client-process restart.

If later authorized after remote non-scored qualification:

- exactly 3 B2 runs in S2;
- exactly 3 B2 runs in S3;
- no B2 in S0/S1;
- no adaptive replication;
- non-primary sensitivity interpretation only.

## Latest guarded preflight

`evidence/local/wp2-h-preflight-latest.md`

Tested SHA `2fde85607eb37e14c5afe0554394e6966f0cae9e`:

- **34/34 tests PASS**;
- Python compile PASS;
- broker shell syntax PASS;
- RF/P0/P1/B2 guards PASS;
- POWDER interaction NONE;
- scored interaction NONE.

## Early-window booking state

The existing reservation remains:

**2026-08-26 19:00–22:00 Africa/Cairo — nuc1+nuc2**.

Earlier authenticated attempts did not obtain a usable window:

- exact nuc1+nuc2 search returned no earlier slot today;
- generic NUC5300 pair could not fit for 1/2/3 hours;
- direct immediate controlled-RF creation returned Portal internal error and created no experiment.

No booking probe executed scientific workload or RF manipulation; the fallback reservation was not modified.

## Open pre-score gates

1. physical H calibration and H freeze;
2. physical MQTT session isolation;
3. remote B1/W1 Paho/runtime reproduction;
4. experimental LTE route verification;
5. physical record identity/checksum verification;
6. evidence/clock alignment;
7. deterministic non-scored analysis reconstruction;
8. B1/W1 implementation matching audit;
9. non-scored S3 restart-domain verification;
10. non-scored B2 remote runtime/path/restart verification;
11. immutable pre-score reproducibility snapshot;
12. repair or explicitly bypass known-bad Actions SSH key path before trusted scored automation.

## Exact next action

At the 19:00–22:00 reservation:

1. create a fresh `PowderProfiles/srslte-controlled-rf` experiment;
2. capture fresh bindings and exact profile identity;
3. establish EPC/eNB + UE;
4. pass Q0 user-plane readiness;
5. prove route to `172.16.0.1` via `tun_srsue`;
6. verify remote Paho/runtime and fresh MQTT session isolation;
7. execute H attempts until exactly three `VALID_W1_RECOVERY_SUCCESS` trials exist;
8. stop if a `VALID_W1_RECOVERY_FAILURE` occurs;
9. run deterministic finalizer and freeze H only if H <= 300 s;
10. use the same bundle to close other WP2 gates where justified.

No WP3, no scored B1/W1/B2, and no RF reopening until all pre-score gates close.
