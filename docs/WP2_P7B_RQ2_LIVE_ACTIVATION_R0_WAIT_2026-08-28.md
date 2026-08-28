# WP2-P7B-RQ2 — Live Activation / Manual R0 Wait — 2026-08-28

## Terminal state

`P7B_RQ2_LIVE_ACTIVATION=PASS_CONTROL_PLANE_READY_R0_IDENTITY_REQUIRED`

`LIVE_POWDER_AUTHORIZATION=YES_P7B_RQ2`

`R0_RESERVATION_IDENTITY=BLOCKED_MISSING_EXPERIMENT_ID_AND_EXPERIMENT_NAME`

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

## Authorization interpretation

The user explicitly authorized execution of `P7B-RQ2` on 2026-08-28. That authorization opens exactly one future non-scored P7B-RQ2 requalification session, but it does not move or replace the manual R0 reservation boundary.

The user must still create or select an existing POWDER reservation and provide exactly:

- `experiment_id`
- `experiment_name`

GitHub automation is prohibited from creating or selecting a reservation.

Until both values are supplied, the workflow remains intentionally **not dispatch-ready** and no POWDER/Portal/SSH/RF/service action is permitted.

## Frozen science source

The target-side scientific source for the authorized session is frozen at:

`SCIENTIFIC_SOURCE_SHA=2d7eb744f14ad4d5889909dac3cc29236c667190`

This source contains the H2 repair and the modular target adapter. Control-plane fixes made after this SHA do not rewrite the frozen scientific implementation.

## Modular target adapter

Path:

`scripts/wp2_p7b_rq2_module_adapter.py`

Blob:

`ccb3b86493bb16611bdf8e7947d0241e8c85d83a`

The adapter exposes exactly:

- `prepare` — M3 Q0 known-good baseline preparation;
- `B1` — M4;
- `W1` — M6;
- `B2` — M8;
- `reconstruct` — M10.

It reuses the actual H2 -> r2 -> r1 execution layers rather than copying scientific logic. Each cell checks persisted prior-cell state and calls the frozen `run_cell` once.

## GitHub control plane

Workflow:

`.github/workflows/wp2-p7b-rq2-session.yml`

Workflow blob:

`6df75614b9b68050c1645e1b603cb946e7b4f5cd`

Controller helper:

`scripts/wp2_p7b_rq2_controller.sh`

Controller blob:

`b990a0cfa52bd23b1771857cbf938ac5aac7f0bd`

Activation record:

`experiments/WP-PWD01/p7b-rq2-live-authorization-2026-08-28.json`

Activation blob:

`899318cc8bd625af621f2f023fd8b8b3f2381221`

The workflow is `workflow_dispatch` only and requires:

- `experiment_id`
- `experiment_name`
- `authority_id=P7B-RQ2`

One-shot semantics are enforced by:

1. `GITHUB_RUN_ATTEMPT=1`;
2. a GitHub Actions read-only query requiring the current run to be the **first and only** `workflow_dispatch` run for this workflow;
3. experiment-scoped concurrency with `cancel-in-progress: false`.

This replaced an earlier proposed `GITHUB_RUN_NUMBER=1` guard after pre-live analysis showed schema-validation history had already consumed workflow run numbers. No live dispatch had occurred.

## Live DAG / HCI

The registered execution surface is:

1. M0 — authority/source/contract freeze;
2. M1 — existing reservation identity + manifest, read-only;
3. M2 — exact source stage + target-native runtime/EFCC preflight;
4. M3 — H2-safe Q0 known-good baseline;
5. M4 — B1;
6. M5 — B1 escrow + off-POWDER readback;
7. M6 — W1;
8. M7 — W1 escrow + off-POWDER readback;
9. M8 — B2;
10. M9 — B2 escrow + off-POWDER readback;
11. M10 — non-scored reconstruction;
12. M99 — final escrow/readback and STOP before teardown.

There is no automatic retry, second reservation, reservation extension, teardown, scored execution, or WP3 authority.

## Evidence survival

Each scientific cell uses the evidence chain:

`node_raw -> /proj escrow -> controller pull -> Actions artifact -> readback`

The controller uses `wp2_p7b_preservation_helpers_v2.sh` for project escrow. If one side has no evidence tree after an early failure, the absence is preserved explicitly as:

`CLASSIFICATION=PARTIAL_FAILURE_EVIDENCE`

rather than causing the preservation job to lose all available evidence.

M2 also syntax-compiles the new modular adapter under the pinned target Python before any RF mutation.

## Preserved pre-live QA failures

### Workflow schema validation

Run:

`33143081065`

Jobs started: **0**.

Classification:

`PRELIVE_WORKFLOW_SCHEMA_VALIDATION_FAILURE_NO_JOBS_NO_POWDER_CONTACT`

The YAML alias/schema surface was removed before R0. This was not a scientific failure and not a live execution attempt.

### Stale assertion regression

Run:

`33143425295`

Result: 193 tests executed with two assertion failures. Both were test-harness assumptions:

1. a historical R2 test allowed only the earlier R3 workflow name;
2. a live-surface test interpreted `killall` inside a prohibition-regex string as an executable command.

No implementation/live/scientific failure was found. The tests were changed to be phase-aware and to inspect executable command surfaces.

## Final pre-live QA

Commit:

`48361df6dbba0277cc6969e05971a593784fa580`

GitHub Actions:

- workflow: `Local Unit Tests`
- run: `33143509011`
- job: `98759435090`
- Python validation host: `3.12.14`
- Paho MQTT: `2.1.0`
- **193/193 tests PASS**

The complete suite includes H2 adversarial/regression gates, authority-boundary tests, modular-adapter tests, and the RQ2 live-surface tests.

Post-QA Actions state:

- in progress: `0`
- queued: `0`
- `P7B-RQ2` workflow-dispatch runs: `0`

Therefore no reservation access, Portal read, SSH, RF mutation, service mutation, or scientific execution has occurred under P7B-RQ2.

## Historical scientific state remains unchanged

`B1_HISTORICAL=NULL_ABORTED_AFTER_Q3_CONSUMED`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

No H2/live-activation work changes:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuators `[1,33,2,34]`;
- pre-Q0 `60 s`;
- Q3 `120 s`;
- restart `60 s` into Q3;
- cell order `B1 -> W1 -> B2`;
- cohort cutoff `t_rf_restore`;
- `H_app=300 s` from `t_service_ready`;
- generator outside gateway restart domain;
- no automatic scientific retry;
- negative/null/unfavourable evidence remains valid.

## Exact next state

`NEXT_STATE=P7B_RQ2_MANUAL_R0_WAIT`

`NEXT_REQUIRED_INPUTS=experiment_id,experiment_name`

Once both are supplied, the next permitted action is to bind them into the activation record and then perform M0 followed by **M1 read-only reservation/manifest validation**. No RF or service mutation is permitted before M2 and M3 pass.

**STOP — LIVE AUTHORIZATION RECORDED; CONTROL PLANE READY; MANUAL R0 RESERVATION IDENTITY REQUIRED.**
