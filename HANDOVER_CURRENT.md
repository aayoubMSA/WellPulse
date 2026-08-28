# WellPulse — Current Handover

Last updated: 2026-08-28 after **P7B-RQ2 one-shot live session blocked at M2 target-runtime preflight**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct state from chat memory.

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

Historical B1 remains exactly:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

No partial PASS/FAIL credit.

## H1/H2

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

`FIRST_TECHNICAL_ROOT_CAUSE=CONTROLLER_SESSION_COLLISION_SERVICE_RESTORE_KILLED_OPERATOR_TMUX_UE`

`ROOT_CAUSE_CLASS=CONTROLLER_SESSION_INFRASTRUCTURE`

`ROOT_CAUSE_CONFIDENCE=HIGH`

`WP2_P7B_H2=PASS`

`WP2_P7B_H2_DETAIL=PASS_REQUALIFICATION_REPAIR_CLOSED`

## P7B-RQ2 live attempt — consumed at M2

User explicitly authorized one non-scored P7B-RQ2 session.

Reservation identity:

`EXPERIMENT_ID=41d64b85-e743-4d06-a81d-687c28c58e52`

`EXPERIMENT_NAME=WP-05-C`

User confirmed reservation `ready` before dispatch.

GitHub Actions run:

`RUN_ID=33144807486`

Results:

`M0=PASS`

`M1=PASS`

`M2=BLOCKED:PINNED_PYTHON_MISSING`

M2 job:

`98763460078`

Exact first named blocker:

`WP2_P7B_TARGET_NODE_PREFLIGHT=BLOCKED:PINNED_PYTHON_MISSING`

Classification:

`PRE_SCIENCE_TARGET_RUNTIME_INFRASTRUCTURE_BLOCK`

This is **not** a scientific failure.

The controller completed M1 read-only Portal reservation/manifest validation, then M2 contacted and staged source to:

- `nuc1 / CORE`
- `nuc2 / UE`

The Paho Java JAR hash gate passed. Target-native preflight then stopped on the missing pinned Python runtime before M3.

## Downstream state

`M3=SKIPPED`

`B1_RQ2=NOT_STARTED`

`B1_EVIDENCE=SKIPPED`

`W1=NOT_STARTED`

`W1_EVIDENCE=SKIPPED`

`B2=NOT_STARTED`

`B2_EVIDENCE=SKIPPED`

`RECONSTRUCT=SKIPPED`

`FINAL_EVIDENCE_JOB=SKIPPED`

`SCIENTIFIC_MEASUREMENT_STARTED=NO`

`RF_MUTATION=NO`

`SERVICE_MUTATION=NO`

`ACTIONS_ARTIFACTS=0`

`SCORED=NO`

`TEARDOWN=NO`

## Authority after failure

`RQ2_ONE_SHOT_CONSUMED=YES`

`RERUN_AUTHORIZED=NO`

`AUTOMATIC_RETRY=NO`

`SECOND_RESERVATION_AUTHORIZED=NO`

`RESERVATION_EXTENSION_AUTHORIZED=NO`

`TEARDOWN_AUTHORIZED=NO`

Do not rerun workflow run `33144807486` and do not start another P7B live workflow under the consumed RQ2 authority.

## Canonical failure closure

`docs/WP2_P7B_RQ2_M2_PREFLIGHT_BLOCKED_PINNED_PYTHON_2026-08-28.md`

Activation state:

`experiments/WP-PWD01/p7b-rq2-live-authorization-2026-08-28.json`

Frozen target scientific source remains:

`SCIENTIFIC_SOURCE_SHA=2d7eb744f14ad4d5889909dac3cc29236c667190`

Frozen science remains unchanged:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`
- attenuators `[1,33,2,34]`
- pre-Q0 `60 s`
- Q3 `120 s`
- restart `60 s` into Q3
- cell order `B1 -> W1 -> B2`
- primary cohort cutoff `t_rf_restore`
- `H_app=300 s` from `t_service_ready`
- generator outside gateway restart domain
- no automatic scientific retry

## Mandatory next-agent read order

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P7B_RQ2_M2_PREFLIGHT_BLOCKED_PINNED_PYTHON_2026-08-28.md`
3. `experiments/WP-PWD01/p7b-rq2-live-authorization-2026-08-28.json`
4. `.github/workflows/wp2-p7b-rq2-session.yml`
5. `scripts/wp2_p7b_rq2_controller.sh`
6. `scripts/wp2_p7b_target_node_preflight.sh`
7. `scripts/wp2_p7b_rq2_module_adapter.py`
8. `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`
9. `experiments/WP-PWD01/p7b-executable-contract-v2.json`
10. `experiments/WP-PWD01/p7b-h2-requalification-authority-v1.json`
11. H2.1–H2.6 closures
12. current `Research & Grants — Lessons Learned Ledger`

## Stop state

`NEXT_STATE=OFFLINE_RQ2_PINNED_PYTHON_RECOVERY_DECISION`

`LIVE_EXECUTION=STOPPED`

`DO_NOT_RERUN=YES`

**STOP — RQ2 CONSUMED AT M2 BEFORE SCIENCE. OFFLINE PINNED-RUNTIME RECOVERY DECISION REQUIRED.**
