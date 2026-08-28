# WellPulse — Current Handover

Last updated: 2026-08-28 after **P7B-RQ2 R0 IDENTITY BOUND / READY WAIT**.

## Authority

Canonical repository: `aayoubMSA/WellPulse`  
Canonical branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from chat memory.

## Executive scientific state

- WP0: **PASS**
- WP1: **PASS / FROZEN**
- WP2: **ACTIVE / PRE-SCORE BLOCKED**
- WP3: **BLOCKED ON WP2**
- WP4: **BLOCKED**
- WP5: **PREPARED / NOT EXECUTED**
- P6 Golden baseline: **VALID / FROZEN**
- P7B physical qualification: **NOT PASSED**
- scored execution: **NOT AUTHORIZED**

Historical B1 remains:

`P7B_B1_ATTEMPT=ABORTED_AFTER_SCIENTIFIC_IMPAIRMENT`

`B1_SCIENTIFIC_VERDICT=NULL`

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

No partial B1 PASS/FAIL credit may be inferred.

## H1/H2 — closed

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

`FIRST_TECHNICAL_ROOT_CAUSE=CONTROLLER_SESSION_COLLISION_SERVICE_RESTORE_KILLED_OPERATOR_TMUX_UE`

`ROOT_CAUSE_CLASS=CONTROLLER_SESSION_INFRASTRUCTURE`

`ROOT_CAUSE_CONFIDENCE=HIGH`

`WP2_P7B_H2=PASS`

`WP2_P7B_H2_DETAIL=PASS_REQUALIFICATION_REPAIR_CLOSED`

`H2_PROGRESS=100%`

H2 canonical authority overlay:

`experiments/WP-PWD01/p7b-h2-requalification-authority-v1.json`

Authority ID:

`P7B-RQ2`

## P7B-RQ2 — explicit live authorization received

The user explicitly authorized execution on 2026-08-28.

`LIVE_POWDER_AUTHORIZATION=YES_P7B_RQ2`

This authorization is bounded to **one future non-scored P7B-RQ2 physical requalification session** and does not authorize:

- automatic reservation creation;
- automatic reservation selection;
- automatic retry;
- a second reservation;
- reservation extension;
- automatic teardown;
- scored execution;
- WP3.

## Current stage — R0 IDENTITY BOUND / READY WAIT

`P7B_RQ2_R0_IDENTITY=PASS_BOUND`

`CURRENT_STAGE=R0_IDENTITY_BOUND_AWAITING_READY_CONFIRMATION`

`EXPERIMENT_ID=41d64b85-e743-4d06-a81d-687c28c58e52`

`EXPERIMENT_NAME=WP-05-C`

`LAST_OBSERVED_RESERVATION_STATUS=booting`

`RESERVATION_READY_CONFIRMED=NO`

`NEXT_REQUIRED_INPUT=FRESH_READY_CONFIRMATION`

The reservation identity is now bound. The latest user screenshot showed state `booting`, with `nuc1` and `nuc2` still `changing` / `pending`, so readiness is not inferred from the supplied status URL alone.

Current action state:

`WORKFLOW_DISPATCH=NO`

`POWDER_CONTACT=NO`

`PORTAL_CONTACT=NO`

`SSH=NO`

`RF_MUTATION=NO`

`SERVICE_MUTATION=NO`

`B1_RQ2=NOT_STARTED`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`TEARDOWN=NO`

No Portal or target contact is permitted before fresh readiness confirmation because the first real `workflow_dispatch` consumes the single session authority.

## Canonical R0 binding note

`docs/WP2_P7B_RQ2_R0_IDENTITY_BOUND_READY_WAIT_2026-08-28.md`

Canonical live-activation closure:

`docs/WP2_P7B_RQ2_LIVE_ACTIVATION_R0_WAIT_2026-08-28.md`

Activation record:

`experiments/WP-PWD01/p7b-rq2-live-authorization-2026-08-28.json`

Activation blob after R0 binding:

`797283777625732d7f8f574c64f0f143d5504dc3`

## Frozen target scientific source

`SCIENTIFIC_SOURCE_SHA=2d7eb744f14ad4d5889909dac3cc29236c667190`

The live target must receive this exact source commit. Later control-plane documentation/test changes do not change the scientific source.

Frozen scientific/runtime artifacts remain:

- executable contract v2: `233aabeaf3081470bc3ebc1ee04168f8932fc415`
- target-runtime contract v2: `9531893989effb142e694294b95c0c7146353742`
- modular pipeline v1: `2c85af21f502c092c2da0ecb1bf615c8f705069b`
- H2 entrypoint: `d66bc791455127ef87497cea3e912ee6f46e685b`
- frozen r2 entrypoint: `fa506e661f90fe9c21418fd2f86c8ca0a9230175`
- H2 ownership library: `7810d1ed603fc305bd419c91a2b14bcca2e95e24`
- H2 safe restore: `72f465f274c86d7ec514f358023074aa26f96551`
- historical Golden restore: `cdf865eaaaf1c08bc8f7a8896d7f705739e60b9c`

## Modular P7B-RQ2 execution surface

Target-side module adapter:

`scripts/wp2_p7b_rq2_module_adapter.py`

Blob:

`ccb3b86493bb16611bdf8e7947d0241e8c85d83a`

GitHub control helper:

`scripts/wp2_p7b_rq2_controller.sh`

Blob:

`b990a0cfa52bd23b1771857cbf938ac5aac7f0bd`

Authorized workflow:

`.github/workflows/wp2-p7b-rq2-session.yml`

Blob:

`6df75614b9b68050c1645e1b603cb946e7b4f5cd`

Trigger:

`workflow_dispatch` only.

Required inputs:

- `experiment_id=41d64b85-e743-4d06-a81d-687c28c58e52`
- `experiment_name=WP-05-C`
- `authority_id=P7B-RQ2`

One-shot semantics:

- `GITHUB_RUN_ATTEMPT=1`;
- M0 read-only GitHub API check requires the current run to be the first/only `workflow_dispatch` run for this workflow;
- experiment-scoped concurrency;
- `cancel-in-progress=false`.

The obsolete idea `GITHUB_RUN_NUMBER=1` was removed because pre-live schema-validation history had already consumed run numbers before any live dispatch.

## Live DAG / simple HCI

If and only if reservation readiness is freshly confirmed, the authorized DAG is:

1. M0 — authority/source/contract freeze;
2. M1 — existing reservation + manifest read-only validation;
3. M2 — exact source stage + target-native runtime/EFCC preflight;
4. M3 — H2-safe Q0 known-good baseline;
5. M4 — B1;
6. M5 — B1 evidence escrow/readback;
7. M6 — W1;
8. M7 — W1 evidence escrow/readback;
9. M8 — B2;
10. M9 — B2 evidence escrow/readback;
11. M10 — non-scored reconstruction;
12. M99 — final evidence readback and STOP before manual teardown.

No later scientific cell may run unless the preceding cell and evidence job permit it.

## Evidence survival

Required chain:

`node_raw -> /proj escrow -> controller pull -> Actions artifact -> readback`

Each post-cell evidence job writes project escrow before controller pull. If one side has no evidence tree after an early failure, the absence is preserved as:

`CLASSIFICATION=PARTIAL_FAILURE_EVIDENCE`

instead of discarding the available evidence.

M2 additionally syntax-compiles `scripts/wp2_p7b_rq2_module_adapter.py` under the pinned target Python before RF mutation can occur.

## Pre-live QA history

### Preserved schema-validation failure

Run `33143081065`:

- workflow schema validation failure;
- **0 jobs started**;
- no Portal/POWDER/SSH contact;
- no live execution;
- classification `PRELIVE_WORKFLOW_SCHEMA_VALIDATION_FAILURE_NO_JOBS_NO_POWDER_CONTACT`.

The YAML alias/schema surface was removed.

### Preserved stale-test failure

Run `33143425295`:

- 193 tests executed;
- 2 failures;
- both classified as stale test-harness assumptions after legitimate post-H2 activation;
- no implementation/scientific/live failure.

### Final activation QA — PASS

Commit:

`48361df6dbba0277cc6969e05971a593784fa580`

Run:

`33143509011`

Job:

`98759435090`

Result:

**193/193 tests PASS**

Validation host:

- Ubuntu 24.04.4
- Python 3.12.14
- Paho MQTT 2.1.0

The final suite covers H2 regression/adversarial gates, authority boundaries, modular adapter, live workflow structure, first-dispatch semantics, target syntax gating, project escrow, partial-failure preservation, and prohibition of automatic reservation/retry/teardown.

Post-QA:

`ACTIONS_IN_PROGRESS=0`

`ACTIONS_QUEUED=0`

`P7B_RQ2_WORKFLOW_DISPATCH_COUNT=0`

No workflow-schema validation run was generated by the final workflow-control-plane commit, confirming the earlier invalid YAML surface is gone.

## Frozen scientific controls

No activation or R0-binding patch changed:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`
- attenuators `[1,33,2,34]`, coupled
- pre-Q0 = `60 s`
- Q3 = `120 s`
- gateway restart = `60 s` into Q3
- cell order = `B1 -> W1 -> B2`
- primary cohort cutoff = `t_rf_restore`
- `H_app=300 s` from `t_service_ready`
- distinct clocks: `t_rf_restore`, `t_service_ready`, `t_app_complete`
- generator outside gateway restart domain
- no automatic scientific retry
- negative/null/unfavourable evidence remains valid

## Manual/automatic boundary after R0 identity binding

Once fresh reservation readiness is confirmed:

1. preserve the bound `experiment_id` and `experiment_name`;
2. preserve the first-dispatch one-shot lock;
3. begin M0;
4. M1 may contact the Portal **read-only** to verify exact reservation/name/project/status/expiry/manifest/nuc1/nuc2/image/hardware;
5. M2 may then SSH/stage only if M1 passes;
6. RF/service mutation remains prohibited until M2 passes and M3 begins under the same authority.

GitHub must never create the reservation.

## Mandatory next-agent read order

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P7B_RQ2_R0_IDENTITY_BOUND_READY_WAIT_2026-08-28.md`
3. `docs/WP2_P7B_RQ2_LIVE_ACTIVATION_R0_WAIT_2026-08-28.md`
4. `experiments/WP-PWD01/p7b-rq2-live-authorization-2026-08-28.json`
5. `.github/workflows/wp2-p7b-rq2-session.yml`
6. `scripts/wp2_p7b_rq2_controller.sh`
7. `scripts/wp2_p7b_rq2_module_adapter.py`
8. `experiments/WP-PWD01/p7b-h2-requalification-authority-v1.json`
9. `docs/WP2_P7B_H2_6_REQUALIFICATION_AUTHORITY_DECISION_CANONICAL_CLOSURE_2026-08-28.md`
10. H2.1–H2.5 closures and H2.4/H2.5 machine-readable evidence
11. `scripts/wp2_p7b_c_node_h2.py`
12. `scripts/wp2_p7b_target_node_preflight.sh`
13. `experiments/WP-PWD01/p7b-executable-contract-v2.json`
14. `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`
15. `experiments/WP-PWD01/p7b-modular-pipeline-contract-v1.json`
16. current `Research & Grants — Lessons Learned Ledger`

## Stop state

`WP2_P7B_H2=PASS`

`P7B_RQ2_LIVE_AUTHORIZATION=YES`

`P7B_RQ2_CONTROL_PLANE=PASS_READY`

`P7B_RQ2_R0_IDENTITY=PASS_BOUND`

`EXPERIMENT_ID=41d64b85-e743-4d06-a81d-687c28c58e52`

`EXPERIMENT_NAME=WP-05-C`

`RESERVATION_READY_CONFIRMED=NO`

`WORKFLOW_DISPATCH=NO`

`POWDER_CONTACT=NO`

`B1_RQ2=NOT_STARTED`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`TEARDOWN=NO`

`NEXT_STATE=P7B_RQ2_R0_READY_WAIT`

`NEXT_REQUIRED_INPUT=FRESH_READY_CONFIRMATION`

**STOP — R0 IDENTITY BOUND; RESERVATION READY NOT YET CONFIRMED; DO NOT DISPATCH.**
