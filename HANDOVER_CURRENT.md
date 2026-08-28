# WellPulse — Current Handover

Last updated: 2026-08-28 after **WP2-P7B-H2.3 incremental restart/restoration frontier evidence PASS**.

## Authority

This is the current canonical operational handover for `aayoubMSA/WellPulse`, branch `main`.

Do not reconstruct current state from chat memory. Historical detail remains authoritative in the referenced closure/evidence artifacts below.

## Executive scientific state

- WP0: **PASS**.
- WP1: **PASS / FROZEN**.
- WP2: **ACTIVE / PRE-SCORE BLOCKED**.
- WP3: **BLOCKED ON WP2**.
- WP4: **BLOCKED**.
- WP5: **PREPARED / NOT EXECUTED**.
- P6 Golden baseline: **VALID / FROZEN**.
- P7/P7B offline hardening/runtime/EFCC work: retained unless explicitly superseded.
- P7B physical qualification: **NOT PASSED**.
- Scored execution: **NOT AUTHORIZED**.

Latest attempted scientific state remains exactly:

`P7B_B1_ATTEMPT=ABORTED_AFTER_SCIENTIFIC_IMPAIRMENT`

`B1_SCIENTIFIC_VERDICT=NULL`

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`AUTOMATIC_RETRY=PROHIBITED`

`SCORED=NO`

No partial B1 PASS/FAIL may be inferred from the aborted attempt.

## Historical live target — do not assume still live

- reservation UUID: `f6de95cb-a13a-421e-bd0e-766dfc1d3fb3`
- name: `wp7brq2609012`
- profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- CORE: `nuc1`
- UE: `nuc2`
- aborted run ID: `wp2-p7b-manual-20260828T024433Z`

No current authority exists to query, reuse, replace, or mutate this target.

## WP2-P7B-H1 — PASS

Terminal verdict:

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

Canonical records:

- `docs/WP2_P7B_H1_ABORT_EVIDENCE_FREEZE_ROOT_CAUSE_CLOSURE_2026-08-28.md`
- `evidence/powder/wp2-p7b-h1-abort-root-cause.json`

First technical root cause:

`FIRST_TECHNICAL_ROOT_CAUSE=CONTROLLER_SESSION_COLLISION_SERVICE_RESTORE_KILLED_OPERATOR_TMUX_UE`

`ROOT_CAUSE_CLASS=CONTROLLER_SESSION_INFRASTRUCTURE`

`ROOT_CAUSE_CONFIDENCE=HIGH`

Frozen evidence proves the manual controller was running inside tmux `ue` on the UE while the historical restore path began by destroying that same session. The gateway restart itself occurred; missing later `restart_proof.json` was a consequence of the controller disappearing before that later proof write point. RLF/RRC/NAS observations remain secondary observations and do not convert B1 into a scientific failure.

## H2 prospective amendment state

Machine-readable H2 contract delta:

`experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json`

Current status:

`OFFLINE_H2_3_FRONTIER_EVIDENCE_PASS_NOT_LIVE_AUTHORITY`

The frozen base `experiments/WP-PWD01/p7b-executable-contract-v2.json` remains immutable throughout H2.

### H2.1 — PASS

`H2_1_CONTRACT_DELTA=PASS`

Closure:

`docs/WP2_P7B_H2_1_EXECUTABLE_CONTRACT_DELTA_CLOSURE_2026-08-28.md`

A1–A7 were translated into a prospective machine-readable operational safety/observability delta without scientific-control or authority drift.

QA: run `33139803749`, job `98747874891`, **135/135 PASS**.

### H2.2 — PASS

`H2_2_SESSION_OWNERSHIP=PASS`

Closure:

`docs/WP2_P7B_H2_2_CONTROLLER_SESSION_OWNERSHIP_REPAIR_CLOSURE_2026-08-28.md`

Prospective implementation:

- `src/wellpulse/p7b_session_ownership.py`
- `scripts/wp2_p7b_service_restore_h2.sh`
- `scripts/wp2_p7b_c_node_h2.py`

Key safety rule:

`DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO`

The prospective restore uses exact service PID ownership and cannot blindly destroy service tmux sessions. The historical `scripts/wp2_golden_service_restore.sh` remains unchanged as provenance.

QA: run `33140208485`, job `98749151195`, **147/147 PASS**, including **12/12 H2.2-specific**.

### H2.3 — PASS

`H2_3_FRONTIER_EVIDENCE=PASS`

Closure:

`docs/WP2_P7B_H2_3_INCREMENTAL_RESTART_RESTORATION_FRONTIER_EVIDENCE_CLOSURE_2026-08-28.md`

Implementation commit:

`550db6af5a1c3a919448fe659d72ccc80c8d16b0`

A4–A6 are now implemented prospectively and offline.

#### A4 restart-transition evidence

The H2 wrapper instruments the inherited P7B path without copying the scientific `run_cell` logic and durably writes:

`cells/{cell}/restart_transition.json`

immediately after the replacement gateway passes its existing startup/ready gate and before Q3 completion/LTE restoration.

The record includes generator before/after PID, old/new gateway PID and observed transition state, client/topic identity, UTC + monotonic timestamps, and source-generation continuity. It does **not** replace the later mandatory `restart_proof.json`.

#### A5 restoration frontier

The ownership-safe restore durably appends:

`cells/{cell}/restoration_frontier.jsonl`

with ordered markers:

`RESTORE_REQUESTED -> UE_CLEANUP_BEGIN -> UE_CLEANUP_END -> CORE_CLEANUP_BEGIN -> CORE_CLEANUP_END -> CORE_START_BEGIN -> CORE_START_END -> CORE_STABLE_READY -> UE_START_BEGIN -> UE_START_END -> UE_PROCESS_READY -> SERVICE_READY_PROBE_BEGIN -> SERVICE_READY_PROBE_END`

Each row contains `phase`, `utc`, `monotonic`, and `status`. The service-ready END marker is written as PASS/FAIL before a probe failure is raised.

#### A6 supplementary parent evidence

EXIT/TERM/HUP hooks may append:

`orchestration/controller_survival_frontier.jsonl`

with `supplementary_only=true`. Correctness does not depend on trap execution; incremental A4/A5 evidence is the authoritative failure frontier.

#### H2.3 QA history

The first two offline QA attempts are preserved, not hidden:

- run `33140578317`: H2.3 tests passed; overall FAIL came from two stale H2.1 state-progression assertions.
- run `33140641978`: H2.3 tests passed; overall FAIL came from one stale assertion that rejected the strengthened `DO_NOT_EDIT_BASE_DURING_H2` policy.

The test harness was corrected to accept monotonic project progression and equal-or-stronger immutability. No scientific or authority gate was weakened.

Final QA:

- commit `7e9a8c946ae2eee0781002f15c011c0207ae3ad2`
- run `33140704668`
- job `98750703203`
- **159/159 PASS**
- **12/12 H2.3-specific PASS**
- POWDER contact: NONE
- live service mutation: NONE
- scientific mutation: NONE

`H2_PROGRESS=55%`

## Frozen scientific controls

No H1/H2.1/H2.2/H2.3 action changed:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`
- attenuator IDs `[1,33,2,34]`, coupled
- pre-Q0 = `60 s`
- Q3 = `120 s`
- restart offset = `60 s` into Q3
- exact cell order = `B1 -> W1 -> B2`
- primary cohort cutoff = `t_rf_restore`
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct
- `H_app=300 s` from `t_service_ready`
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`
- preserve `T_service`, `T_app`, `T_total`
- generator remains outside gateway restart domain
- no outcome-derived H re-estimation
- no automatic scientific retry
- negative/null/unfavourable evidence remains valid evidence

## Runtime / integration doctrine still binding

- target project Python: `$HOME/.wp2-golden-venv/bin/python` 3.11.13
- target system Python 3.6.9 must not run project code
- paho-mqtt 2.1.0
- B2 Eclipse Paho Java 1.2.5 JAR SHA-256 `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`
- no remote jq dependency
- preservation path should use bash/coreutils primitives
- Actions process/agent state is step-local
- `tmcc attenuator` physical dB readback is unavailable; Q0 uses set ACK + independent path evidence
- EFCC must be rerun after material runtime/profile/hardware/API changes
- evidence survival must remain simpler than the experiment path
- teardown requires complete raw evidence, escrow, independent readback, and explicit authority

For manual command blocks, explicitly identify `nuc1 / CORE` or `nuc2 / UE`. Do not add diagnostic sleeps to human-operated scripts.

## Exact next bounded patch

`WP2-P7B-H2.4 — STATIC + ADVERSARIAL QA`

H2 is **OFFLINE / IN PROGRESS — 55%**.

H2.4 may only execute offline A7 adversarial/static QA, including at minimum:

1. controller inside tmux `ue` rejected before RF;
2. allowed controller survives simulated service cleanup;
3. service ownership selection cannot match controller PID/session;
4. restart-transition evidence survives synthetic failure after replacement gateway start;
5. each restore-phase synthetic failure preserves the last durable frontier;
6. frozen scientific controls remain unchanged;
7. automatic retry remains absent;
8. no live POWDER/workflow/reservation surface is introduced.

H2.4 must not contact POWDER, create a reservation, SSH to the testbed, mutate RF, restart live services, retry B1, execute W1/B2, teardown, score, or alter scientific controls.

Remaining after H2.4:

- H2.5 — contract/runtime regression gate — 15%
- H2.6 — future non-scored requalification authority decision + canonical closure — 10%

Even terminal H2 PASS does not itself grant live authority.

## Live authority matrix — all NO

`LIVE_POWDER_AUTHORIZATION=NO`

`NEW_RESERVATION_AUTHORIZATION=NO`

`RF_AUTHORIZATION=NO`

`B1_RETRY_AUTHORIZATION=NO`

`W1_B2_AUTHORIZATION=NO`

`SCORED_AUTHORIZATION=NO`

`TEARDOWN_AUTHORIZATION=NO`

`WP3_EXECUTION_AUTHORIZATION=NO`

## Mandatory next-agent read order

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P7B_H1_ABORT_EVIDENCE_FREEZE_ROOT_CAUSE_CLOSURE_2026-08-28.md`
3. `evidence/powder/wp2-p7b-h1-abort-root-cause.json`
4. `experiments/WP-PWD01/P7B_CONTROLLER_SESSION_DISJOINTNESS_AMENDMENT_DRAFT_2026-08-28.md`
5. `experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json`
6. `docs/WP2_P7B_H2_1_EXECUTABLE_CONTRACT_DELTA_CLOSURE_2026-08-28.md`
7. `docs/WP2_P7B_H2_2_CONTROLLER_SESSION_OWNERSHIP_REPAIR_CLOSURE_2026-08-28.md`
8. `docs/WP2_P7B_H2_3_INCREMENTAL_RESTART_RESTORATION_FRONTIER_EVIDENCE_CLOSURE_2026-08-28.md`
9. `src/wellpulse/p7b_session_ownership.py`
10. `scripts/wp2_p7b_c_node_h2.py`
11. `scripts/wp2_p7b_service_restore_h2.sh`
12. `tests/test_wp2_p7b_h2_contract_delta.py`
13. `tests/test_wp2_p7b_h2_session_ownership.py`
14. `tests/test_wp2_p7b_h2_frontier_evidence.py`
15. `experiments/WP-PWD01/p7b-executable-contract-v2.json`
16. `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`
17. `scripts/wp2_p7b_c_node_r2.py`
18. `scripts/wp2_p7b_c_node.py`
19. `scripts/wp2_golden_service_restore.sh`
20. current `Research & Grants — Lessons Learned Ledger` in Drive

## Stop state

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

`H2_1_CONTRACT_DELTA=PASS`

`H2_2_SESSION_OWNERSHIP=PASS`

`H2_3_FRONTIER_EVIDENCE=PASS`

`H2_PROGRESS=55%`

`NEXT_PATCH=WP2-P7B-H2.4_STATIC_ADVERSARIAL_QA`

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`RETRY=NO`

`TEARDOWN=NO`

`LIVE_POWDER_AUTHORIZATION=NO`

**STOP — H2.3 CLOSED. H2.4 NOT STARTED.**
