# Project Validation Status

## Current state — 2026-08-26 16:25 Africa/Cairo

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Consortium review: **PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS**.
- P0 amendment: **IMPLEMENTED / LOCAL PASS; physical safeguards still open where applicable**.
- P1 amendment: **FROZEN PRE-SCORE**.
- B2 durable-client local semantics: **PASS 3/3 / QUALIFIED AS COMPACT SENSITIVITY COMPARATOR**.
- WP2: **IN PROGRESS — physical W1 H calibration is the active scientific frontier**.
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

`30 s readiness -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Outcome classes:

- `TECHNICALLY_INVALID` — replaceable only for predefined technical invalidity.
- `VALID_W1_RECOVERY_FAILURE` — adverse valid evidence; not replaceable; blocks H freeze.
- `VALID_W1_RECOVERY_SUCCESS` — exactly three required.

Common horizon:

`H = max(120 s, ceil_to_30s(2 × p95))`

With n=3 successful trials, p95 is the maximum observed drain. H is frozen once before scoring and used identically for all arms/scenarios. If H > 300 s, stop and investigate; never cap.

## Current automation/credential state

The secure GitHub Actions path is now **credential-ready**:

- official Portal API authentication works;
- SSH private-key structure is valid;
- passphrase unlock works;
- identity loads into `ssh-agent`;
- corresponding public key is registered with POWDER for future experiments.

This supersedes the earlier stale statement that `POWDER_SSH_PRIVATE_KEY` was unusable.

Fresh-node SSH acceptance remains **OPEN** because the last READY experiment was created before registration of the current public key. Do not ask the user to re-enter secret material without actual evidence of credential invalidity.

## 14:00–16:00 POWDER window

Status: **CLOSED / SCIENTIFICALLY CLEAN**.

- `WP-HCAL-A` reached READY and physical `nuc1+nuc2` mapping was verified.
- SSH failed with the current automation identity because that identity was not injected into the already-running experiment.
- current public key was registered with POWDER.
- immediate terminate/recreate (`A -> B`) did not recover to READY.
- after cooldown, the resource-release gate passed.
- `WP-HCAL-C` creation succeeded but remained mostly `pending` with intermittent `provisioning`; it never reached READY.
- after reservation expiry, final read-only Portal API check found zero active H-cal experiments and release gate PASS.
- no H, LTE user-plane, MQTT, or scored scientific run occurred.

Mandatory pre-read:

`powder/PRE_EXPERIMENT_GATE_2026-08-26.md`

Mandatory allocator rule D-020:

`terminate -> verify release -> convergence interval -> recreate only if still necessary`

Never use immediate same-resource recreate as the default recovery path.

## Open pre-score gates

1. fresh experiment READY under current registered automation key;
2. SSH acceptance on both live nodes;
3. physical H calibration and H freeze;
4. physical MQTT session isolation;
5. remote B1/W1 Paho/runtime reproduction;
6. experimental LTE route verification via `tun_srsue`;
7. physical record identity/checksum verification;
8. evidence/clock alignment;
9. deterministic non-scored analysis reconstruction;
10. B1/W1 implementation matching audit;
11. non-scored S3 restart-domain verification;
12. non-scored B2 remote runtime/path/restart verification;
13. immutable pre-score reproducibility snapshot;
14. explicit scored authorization.

## Current reservation

**2026-08-26 19:00–22:00 Africa/Cairo — `nuc1+nuc2`**.

## Exact next action

Before touching POWDER, read:

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_POWDER_NEXT.md`
3. `powder/PRE_EXPERIMENT_GATE_2026-08-26.md`
4. D-020 in `docs/DECISIONS.md`

Then:

1. verify the reservation is live and still owns `nuc1+nuc2`;
2. instantiate exactly one fresh `PowderProfiles/srslte-controlled-rf` experiment early;
3. wait for READY without teardown/recreate churn;
4. verify exact profile revision, manifest, live node bindings and SSH endpoints;
5. prove current automation-key SSH on both nodes;
6. establish EPC/eNB + UE;
7. pass Q0 end-to-end LTE user-plane readiness;
8. prove route to `172.16.0.1` via `tun_srsue`;
9. verify remote Paho/runtime and fresh MQTT session isolation;
10. only then execute H attempts until exactly three `VALID_W1_RECOVERY_SUCCESS` trials exist;
11. stop for any valid W1 recovery failure or H > 300 implication;
12. freeze H only through deterministic finalization.

No WP3, no scored B1/W1/B2, and no RF reopening until all pre-score gates close.