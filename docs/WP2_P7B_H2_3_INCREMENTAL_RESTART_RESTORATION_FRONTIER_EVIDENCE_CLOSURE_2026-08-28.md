# WP2-P7B-H2.3 — Incremental Restart/Restoration Frontier Evidence Closure — 2026-08-28

## Terminal verdict

`H2_3_FRONTIER_EVIDENCE=PASS`

`POWDER_CONTACT=NO`

`LIVE_SERVICE_MUTATION=NO`

`RF_MUTATION=NO`

`RETRY=NO`

`W1_B2=NO`

`SCORED=NO`

`TEARDOWN=NO`

H2.3 implements only A4–A6 from the H2 prospective operational-safety delta. It creates no live workflow, reservation, RF action, service action, retry authority, scored authority, or teardown authority.

## A4 — incremental restart-transition evidence

Prospective entrypoint:

`scripts/wp2_p7b_c_node_h2.py`

The H2 wrapper instruments the inherited P7B execution path instead of copying or rewriting the frozen scientific `run_cell` logic.

It captures generator/gateway state around the already-defined gateway destruction/replacement sequence and durably writes:

`cells/{cell}/restart_transition.json`

immediately after the replacement gateway has passed its existing startup/ready gate, before Q3 completion or LTE restoration.

Required fields include:

- `generator_pid_before`
- `generator_pid_after`
- `old_gateway_pid`
- `old_gateway_exit_observed`
- `new_gateway_pid`
- `new_gateway_start_observed`
- `client_identity`
- `topic_identity`
- UTC and monotonic timestamps for request, old exit, new start, and new ready
- `source_generation_continuity_status`

The write is atomic and durability-oriented: temporary file, file fsync, replace, and best-effort parent-directory fsync.

`restart_transition.json` is incremental evidence only. The existing later `restart_proof.json` remains mandatory and is not replaced.

## A5 — incremental restoration frontier

Prospective safe restore:

`scripts/wp2_p7b_service_restore_h2.sh`

Per-cell frontier:

`cells/{cell}/restoration_frontier.jsonl`

Each marker is written before/after the corresponding destructive or recovery phase and flushed before advancing. The canonical order is:

1. `RESTORE_REQUESTED`
2. `UE_CLEANUP_BEGIN`
3. `UE_CLEANUP_END`
4. `CORE_CLEANUP_BEGIN`
5. `CORE_CLEANUP_END`
6. `CORE_START_BEGIN`
7. `CORE_START_END`
8. `CORE_STABLE_READY`
9. `UE_START_BEGIN`
10. `UE_START_END`
11. `UE_PROCESS_READY`
12. `SERVICE_READY_PROBE_BEGIN`
13. `SERVICE_READY_PROBE_END`

Each row records `phase`, `utc`, `monotonic`, and `status`.

The service-ready probe is executed with explicit result handling so that `SERVICE_READY_PROBE_END` is durably written as PASS or FAIL before a failed probe raises. Thus the last completed frontier remains available even when restoration fails later.

No artificial scientific delay was added for observability.

## A6 — supplementary controller-exit evidence

The H2 wrapper installs supplementary EXIT, TERM, and HUP hooks that attempt to append:

`orchestration/controller_survival_frontier.jsonl`

The records are explicitly marked `supplementary_only=true`.

Correctness does not depend on these hooks. Abrupt loss remains diagnosable from the independently and incrementally persisted A4/A5 evidence even if a trap cannot run.

SIGKILL is not claimed to be catchable.

## Scientific preservation

H2.3 does not duplicate or alter frozen scientific controls. In particular it changes none of:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`
- attenuator IDs `[1,33,2,34]`
- pre-Q0 `60 s`
- Q3 `120 s`
- restart offset `60 s`
- cell order `B1 -> W1 -> B2`
- `H_app=300 s` from `t_service_ready`
- primary cohort cutoff `t_rf_restore`
- clock semantics
- no-automatic-retry rule
- non-scored status

The historical controller and Golden restore remain provenance; H2.3 is a prospective wrapper/instrumentation layer.

## QA evidence and preserved failed attempts

Implementation commit:

`550db6af5a1c3a919448fe659d72ccc80c8d16b0`

### QA attempt 1 — preserved / classified

- run `33140578317`
- job `98750306271`
- total tests: 159
- H2.3-specific tests: **12/12 PASS**
- overall result: FAIL due only to two stale H2.1 assertions that still required the old H2.1 status and H2.2 next-patch string after H2.2 had legitimately promoted the contract.
- classification: `TEST_HARNESS_STATE_PROGRESSION_ASSERTION_STALE`
- scientific failure: NO
- H2.3 implementation failure: NO

### QA attempt 2 — preserved / classified

- run `33140641978`
- job `98750503612`
- H2.3-specific tests remained PASS
- overall result: FAIL due only to one stale assertion requiring `DO_NOT_EDIT_BASE_AS_PART_OF_H2_1` after the policy had been strengthened to `DO_NOT_EDIT_BASE_DURING_H2`.
- classification: `TEST_HARNESS_STRENGTHENED_POLICY_ASSERTION_STALE`
- scientific failure: NO
- H2.3 implementation failure: NO

The stale assertions were repaired to test monotonic project-state progression and equal-or-stronger base immutability. No authority or scientific gate was weakened.

### Final QA — PASS

- final QA commit: `7e9a8c946ae2eee0781002f15c011c0207ae3ad2`
- run `33140704668`
- job `98750703203`
- **159/159 tests PASS**
- H2.3-specific tests: **12/12 PASS**
- Python validation host: `3.12.14`
- Paho MQTT: `2.1.0`
- POWDER contact: NONE
- live service mutation: NONE

The final gate proves A4 required fields/write timing, final-proof preservation, exact A5 marker order and durable flush semantics, service-probe failure frontier preservation, A6 supplementary-only hooks, no new live/retry authority, no frozen-science duplication, and regression compatibility with the existing suite.

## Contract promotion

`experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json`

is now:

`status=OFFLINE_H2_3_FRONTIER_EVIDENCE_PASS_NOT_LIVE_AUTHORITY`

All live authority flags remain false.

## Next patch

`WP2-P7B-H2.4 — STATIC + ADVERSARIAL QA`

H2.4 may test A1–A7 adversarially offline. It must not contact POWDER or create live authority.

**STOP — H2.3 CLOSED. H2.4 NOT STARTED.**
