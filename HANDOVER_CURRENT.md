# WellPulse — Current Handover

Last updated: 2026-08-26 after independent pre-WP3 consortium review, P0/P1 freeze, B2 local qualification, guarded preflight, 14:00–16:00 POWDER operational window, and automation credential-readiness verification, Africa/Cairo

## Executive state

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- WP0: **8/8 PASS**.
- WP1: **12/12 design complete; P0/P1 pre-score amendments frozen; B2 local semantics PASS**.
- WP2: **IN PROGRESS — physical H is the active scientific frontier**.
- WP3: **0/30 — BLOCKED**.
- WP4: **0/15 — BLOCKED**.
- WP5: **0/20 scientific closure**.
- Scientific weighted completion: **20%**.
- `scored_runs_authorized = false`.

No local QA, B2 semantics test, booking probe, or H calibration is a scored B1/W1/B2 scientific result.

## Canonical pre-score review and amendments

Read together:

1. `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`
2. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
3. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
4. `experiments/WP-PWD01/run-matrix.yaml`

Consortium verdict:

`PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS`

The project was not redesigned. RF calibration, POWDER selection, the low-rate 1 Hz workload, and the WP structure remain intact.

## Scientific interpretation now frozen

The study asks **when durable application-level record semantics add value beyond correctly configured MQTT**, rather than assuming W1 wins every network outage.

- `S0_HEALTHY`: healthy-path integrity equivalence and overhead sanity.
- `S1_INTERMITTENT`: network-only integrity is primary; recovery/overhead are secondary engineering characterization.
- `S2_HARD_OUTAGE`: network-only integrity is primary while volatile client-process state survives; recovery/overhead are secondary.
- `S3_OUTAGE_RESTART`: primary durability/integrity stress when gateway/client volatile state is destroyed.

Primary inferential endpoint remains unique primary-cohort completeness at common H. Precision stopping remains completeness-only. A separately powered confirmatory recovery-advantage claim is prohibited.

Use `cross-testbed consistency` / `cross-testbed triangulation`, not broad transportability. Confirmatory claim is bounded to the frozen 1 Hz low-rate telemetry regime.

## P0 safeguards

### Calibration outcome classification

- `TECHNICALLY_INVALID`: predefined infrastructure/protocol failure; preserved; replacement allowed.
- `VALID_W1_RECOVERY_FAILURE`: technically valid adverse W1 outcome; preserved; not replaceable as invalid; blocks H freeze.
- `VALID_W1_RECOVERY_SUCCESS`: successful technically valid trial.

Exactly three successful trials are required for H; extra successful trials are prohibited.

### MQTT run/session isolation

Locally implemented; physical verification remains open.

- deterministic run-unique publisher client ID;
- deterministic run-unique receiver client ID;
- deterministic run-unique topic;
- first fresh-run connection requires `session_present=false`;
- independent runs may not reuse identities;
- S3 intentionally reuses the same run-specific gateway identity only across the intra-run process restart.

### S3 restart domain

Rule frozen; non-scored remote verification remains open.

- telemetry generator remains outside the gateway restart domain and continues at 1 Hz;
- only gateway/client process restarts;
- W1 durable state survives;
- B1/B2 reuse their same run-specific identity after the intentional restart;
- source identity/sequence remains continuous;
- no node reboot/power cycle substitutes for gateway-process restart.

### B1 instrumentation and record integrity

B1 accepted/unacknowledged instrumentation is locally verified; it is not exact internal Paho queue occupancy. Scientific completeness/loss is reconstructed from generated/received identity and checksum evidence.

`DurableQueue` fails closed when the same `record_id` appears with different content/checksum; exact duplicate content remains idempotent.

## B2 durable standard-client comparator — QUALIFIED LOCALLY

Canonical evidence:

`evidence/local/wp2-b2-semantics-latest.md`

Configuration:

- Eclipse Paho Java `1.2.5`;
- MQTT v3.1.1;
- QoS1;
- `cleanSession=false`;
- `MqttDefaultFilePersistence`;
- persistent disconnected buffer enabled;
- size 4096;
- delete-oldest disabled.

Local semantics result: **PASS 3/3**.

Every trial generated five records while broker connectivity was absent, abruptly destroyed the client process, and recovered all five after restart: **5/5 unique, 0 missing, 0 duplicates**.

B2 is therefore frozen as a **secondary sensitivity comparator**, not the primary causal arm.

If later authorized after a non-scored POWDER runtime/path/restart gate:

- exactly 3 B2 runs in S2;
- exactly 3 B2 runs in S3;
- no B2 in S0/S1;
- no adaptive B2 replication;
- B2-vs-W1 remains non-primary sensitivity analysis.

Authority: `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md` and `experiments/WP-PWD01/b2-sensitivity-plan.csv`.

## Frozen RF state

Authority: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.

- Q0 = **0 dB** — strong/stable.
- Q1 = **40 dB** — degraded but continuously connected.
- Q2 = **52 dB** — near-threshold/intermittent; clean isolated test produced 6 replies / 12 misses.
- Q3 = **55 dB** — effective application-data outage.
- attenuation IDs = `1 33 2 34`, always changed together.

**No further attenuation sweep is authorized.**

Every scientific/non-scored/scored run begins only after explicit Q0 end-to-end LTE user-plane PASS. Attach/IP alone is insufficient.

## H calibration — ACTIVE PHYSICAL FRONTIER

Target successful non-scored W1 trial:

`30 s readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Frozen H rule:

`H = max(120 s, ceil_to_30s(2 × p95))`

With exactly three successful calibration trials, nearest-rank p95 is the maximum of the three observed drain times. H is one common operational observation horizon used unchanged for B1/W1/B2 and all scenarios. It is frozen before scored data and may not be re-estimated from outcomes.

If H > 300 s: **STOP AND INVESTIGATE; never cap**.

## Latest guarded local preflight

Canonical evidence:

`evidence/local/wp2-h-preflight-latest.md`

Tested SHA:

`2fde85607eb37e14c5afe0554394e6966f0cae9e`

Result:

- **34/34 tests PASS**;
- Python compile PASS;
- broker shell syntax PASS;
- frozen RF + P0 + P1 + B2 guards PASS;
- POWDER interaction NONE;
- scored interaction NONE.

## 14:00–16:00 POWDER operational window — CLOSED / SCIENTIFICALLY CLEAN

Mandatory pre-read:

`powder/PRE_EXPERIMENT_GATE_2026-08-26.md`

Observed operational outcome:

- `WP-HCAL-A` reached READY with correct `nuc1+nuc2` physical bindings, but its originally injected SSH identity did not authorize the current automation key.
- The current automation private key/passphrase path was then validated in GitHub Actions, and the corresponding public key was registered with POWDER.
- Immediate same-reservation terminate/recreate (`WP-HCAL-A` -> `WP-HCAL-B`) did not recover to READY.
- After deliberate cooldown, the resource-release gate passed and `WP-HCAL-C` creation succeeded, but it oscillated between `provisioning` and `pending` for about 23 minutes and never reached READY.
- After reservation expiry, Portal API showed zero visible/active H-cal experiments and `FINAL_RELEASE_GATE=PASS`.
- No LTE user-plane, MQTT H trial, RF scientific action, or scored run occurred. The window is operationally failed but scientifically clean.

Operational rule D-020 is now mandatory: do not use `terminate -> immediate recreate` on the same reserved nodes. Use positive resource-release verification plus a convergence interval, and prefer a single early instantiation per clean reservation.

The fallback reservation remains:

**2026-08-26 19:00–22:00 Africa/Cairo — `nuc1+nuc2`**.

## Current open pre-score gates

1. physical H calibration and freeze H;
2. physical MQTT run/session isolation;
3. remote Paho/runtime reproduction;
4. prove MQTT uses `tun_srsue` / experimental LTE path;
5. physical end-to-end identity/checksum verification;
6. evidence/clock alignment;
7. deterministic reconstruction of a non-scored pilot bundle;
8. B1/W1 implementation matching audit using corrected B1 semantics;
9. non-scored S3 restart-domain verification;
10. non-scored remote B2 runtime/path/restart verification;
11. immutable pre-score reproducibility snapshot after H and implementation gates close;
12. prove the newly registered current automation SSH identity on both nodes of a READY fresh experiment before relying on remote execution.

Credential readiness is now verified without exposing secret values: `POWDER_API_TOKEN`, `POWDER_SSH_PRIVATE_KEY`, and `POWDER_SSH_KEY_PASSPHRASE` are available through GitHub Actions Secrets; the private key structure/passphrase unlock and `ssh-agent` load have passed; and the corresponding public key has been registered with POWDER. This does **not** count as SSH acceptance until a fresh READY experiment proves login on both allocated nodes. Never place private-key/passphrase/token material in Git, evidence, or chat.

## Exact next action

At the 2026-08-26 19:00–22:00 reservation, and **only within WP2**:

**Mandatory first step:** read `powder/PRE_EXPERIMENT_GATE_2026-08-26.md` and D-020 before touching POWDER. Instantiate once early; do not churn the allocator with terminate/recreate loops.

1. create one fresh `PowderProfiles/srslte-controlled-rf` experiment;
2. capture exact profile revision and fresh live bindings;
3. establish EPC/eNB + UE lifecycle;
4. pass Q0 end-to-end user-plane readiness;
5. prove route to `172.16.0.1` uses `tun_srsue`;
6. verify remote Paho 2.1.0/runtime and fresh MQTT session isolation;
7. execute H attempts until exactly three `VALID_W1_RECOVERY_SUCCESS` trials exist, replacing only predefined `TECHNICALLY_INVALID` attempts;
8. if any `VALID_W1_RECOVERY_FAILURE` occurs, stop H freeze and investigate;
9. run `finalize_wp_pwd01_h_calibration.py` across all attempted trial directories;
10. freeze H only if the rule passes and H <= 300 s;
11. use the same evidence bundle to close runtime/path/identity/clock/analysis gates where justified.

If meaningful reservation time remains after H is scientifically closed, only non-scored S3/B2 implementation qualification may follow. No scored B1/W1/B2 run is authorized.

## Canonical read order

1. `HANDOVER_CURRENT.md`
2. `powder/PRE_EXPERIMENT_GATE_2026-08-26.md`
3. `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`
4. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
5. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
6. `docs/MILESTONE_STATUS.md`
7. `docs/STATUS.md`
8. `docs/DECISIONS.md`
9. `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`
10. `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`
11. `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md`
12. `evidence/local/wp2-b2-semantics-latest.md`
13. `evidence/local/wp2-h-preflight-latest.md`
14. `experiments/WP-PWD01/protocol.md`
15. `experiments/WP-PWD01/analysis-plan.md`
16. `experiments/WP-PWD01/evidence-schema.md`
17. `experiments/WP-PWD01/randomization-plan.csv`
18. `experiments/WP-PWD01/b2-sensitivity-plan.csv`
19. `experiments/WP-PWD01/run-matrix.yaml`
20. `powder/MANUAL_GOLDEN_PATH.md`

Never infer future node roles from prior runs. Never persist secrets, private keys, passphrases, RPC tokens, credential blocks, or raw credential-bearing manifests.
