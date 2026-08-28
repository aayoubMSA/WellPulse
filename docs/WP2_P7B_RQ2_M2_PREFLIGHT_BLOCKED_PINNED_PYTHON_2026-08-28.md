# WP2-P7B-RQ2 — M2 Preflight Blocked — 2026-08-28

## Terminal state

`P7B_RQ2_M2=BLOCKED:PINNED_PYTHON_MISSING`

`RUN_ID=33144807486`

`M0=PASS`

`M1=PASS`

`M2=BLOCKED`

`FIRST_NAMED_BLOCKER=PINNED_PYTHON_MISSING`

`M3=SKIPPED`

`B1_RQ2=NOT_STARTED`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCIENTIFIC_MEASUREMENT_STARTED=NO`

`RF_MUTATION=NO`

`SERVICE_MUTATION=NO`

`RERUN=NO`

`SCORED=NO`

`TEARDOWN=NO`

## Evidence

GitHub Actions run `33144807486`, M2 job `98763460078`.

The exact target-native preflight terminal was:

`WP2_P7B_TARGET_NODE_PREFLIGHT=BLOCKED:PINNED_PYTHON_MISSING`

The controller had already completed read-only reservation/manifest validation in M1 and had contacted `nuc1 / CORE` and `nuc2 / UE` in M2 for exact-source staging and preflight. The Paho Java JAR hash gate passed before the target preflight. M2 then failed on the missing pinned Python runtime before M3.

All downstream jobs M3, B1, B1 evidence, W1, W1 evidence, B2, B2 evidence, reconstruction, and final summary were skipped. No Actions artifacts were produced because the failure occurred before any scientific cell/evidence job.

## Classification

`PRE_SCIENCE_TARGET_RUNTIME_INFRASTRUCTURE_BLOCK`

This is not a scientific failure and does not change the historical B1 verdict. The RQ2 one-shot workflow authority is consumed and must not be rerun.

## Frozen next state

`NEXT_STATE=OFFLINE_RQ2_PINNED_PYTHON_RECOVERY_DECISION`

The current reservation is not authorized for further automated mutation under this consumed session. Diagnose and repair the pinned-runtime provisioning path offline first. Any future live attempt requires a new explicit authority decision under the project contract.

**STOP — M2 BLOCKED BEFORE SCIENCE; NO RERUN.**
