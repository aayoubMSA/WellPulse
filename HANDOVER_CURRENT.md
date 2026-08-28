# WellPulse — Current Handover

Last updated: 2026-08-28 after **WP2-P7B-H2.2 controller/session ownership repair PASS**.

## Authority

This is the current canonical operational handover for `aayoubMSA/WellPulse`, branch `main`.

It supersedes the operational next-step state in earlier handovers, including `docs/WP2_P7B_MANUAL_ABORT_HANDOVER_2026-08-28.md`, while retaining those records as historical provenance.

Do not reconstruct current state from chat memory.

## Executive scientific state

- WP0: **PASS**.
- WP1: **PASS / FROZEN**.
- WP2: **ACTIVE / PRE-SCORE BLOCKED**.
- WP3: **BLOCKED ON WP2**.
- WP4: **BLOCKED**.
- WP5: **PREPARED / NOT EXECUTED**.
- P6 Golden baseline: **VALID / FROZEN**.
- P7/P7B offline hardening/runtime/EFCC work: retained and valid unless explicitly superseded.
- P7B physical qualification: **NOT PASSED**.
- Scored execution: **NOT AUTHORIZED**.

Latest attempted B1 state is frozen exactly as:

`P7B_B1_ATTEMPT=ABORTED_AFTER_SCIENTIFIC_IMPAIRMENT`

`B1_SCIENTIFIC_VERDICT=NULL`

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`AUTOMATIC_RETRY=PROHIBITED`

`MANUAL_RETRY=PROHIBITED_UNDER_CURRENT_FROZEN_CONTRACT`

`SCORED=NO`

`TEARDOWN=NOT_AUTHORIZED_BY_H1`

No partial scientific PASS/FAIL credit may be inferred from the aborted B1 attempt.

## Last observed reservation

Historical live target used for the aborted attempt:

- UUID: `f6de95cb-a13a-421e-bd0e-766dfc1d3fb3`
- name: `wp7brq2609012`
- profile: `srslte-controlled-rf`
- frozen profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- CORE: `nuc1`
- UE: `nuc2`
- run ID: `wp2-p7b-manual-20260828T024433Z`

Do not assume that this reservation remains live. No new reservation is authorized by this handover.

## WP2-P7B-H1 — PASS

Canonical closure:

`docs/WP2_P7B_H1_ABORT_EVIDENCE_FREEZE_ROOT_CAUSE_CLOSURE_2026-08-28.md`

Machine-readable root-cause record:

`evidence/powder/wp2-p7b-h1-abort-root-cause.json`

Terminal verdict:

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

### H1 evidence survival

One preservation-only execution was performed after explicit user authorization. It did not alter RF, restart services, retry B1, execute W1/B2, create a reservation, teardown, or perform scored work.

- operational branch: `wp2-p7b-h1-freeze-20260828`
- preservation workflow commit: `118a8c025ef0be5a643f710ff9c620abdcb5698b`
- Actions run: `33138161593`
- job: `98742778306`
- GitHub artifact ID: `9672862285`
- artifact bytes: `1,972,916`
- artifact SHA-256: `a7e3b06d27f46729fcf0ce57aab217a1cf2c1e9edb71211db58d0a7f9063d09d`
- independent downloaded artifact SHA-256: exact match
- controller manifest/hash verification: PASS
- UE internal source-hash verification: PASS
- CORE internal source-hash verification: PASS
- canonical durable Drive file ID: `1mE3GX6lm5k6DeUXaYqOmz7N74rKgYBJ3`
- canonical Drive filename: `wp2-p7b-h1-abort-freeze-33138161593.zip`

Two accidental Drive duplicate uploads were renamed with explicit `NONCANONICAL_DUPLICATE` prefixes and must not be used as evidence. They are not deleted by this handover.

The frozen tree also revealed a prior local abort bundle that had been executed after the earlier handover wording was written:

- prior bundle SHA-256: `a2f9e4a8677bc5b3488da6bf0aad76ad9c67eea2a755009d7cad745228b2b836`

The contradiction with the earlier statement that the abort-freeze sprint had not yet executed is retained as provenance. H1 independently closes evidence survival through off-POWDER pull and read-back.

## Exact aborted-run execution frontier

Authoritative frozen evidence establishes:

1. B1 Q0/readiness passed.
2. Q3 started at approximately `2026-08-28T02:45:46.961547Z`.
3. The intended B1 gateway process was destroyed at the frozen restart point.
4. The replacement gateway started at approximately `2026-08-28T02:46:51.402954Z`.
5. The generator remained alive and continued generating records.
6. At Q3 end, Q0 restore was commanded and `t_rf_restore` was written at approximately `02:47:47Z`.
7. `wp2_golden_service_restore.sh` began at `2026-08-28T02:47:47.138928511Z`.
8. Its evidence stops inside the first phase: `Stopping UE and clearing profile session/tunnel`.
9. `T_UE_STOPPED` was never written.
10. No CORE cleanup/start phase was reached.
11. The parent runner disappeared while detached generator/gateway children survived.
12. Later RCA observed `srsue` absent and `tun_srsue` missing, while CORE `srsepc`/`srsenb` were still running.

Therefore `restart_proof.json=MISSING` must not be interpreted as `gateway restart did not occur`. The gateway restart occurred; the final proof file had simply not yet reached its later write point.

## Classified first technical root cause

`FIRST_TECHNICAL_ROOT_CAUSE=CONTROLLER_SESSION_COLLISION_SERVICE_RESTORE_KILLED_OPERATOR_TMUX_UE`

`ROOT_CAUSE_CLASS=CONTROLLER_SESSION_INFRASTRUCTURE`

`ROOT_CAUSE_CONFIDENCE=HIGH`

Proof chain:

- `scripts/wp2_golden_service_restore.sh` begins its UE cleanup with `tmux kill-session -t ue` on the UE host.
- frozen `q0_radio_capture.txt` proves tmux session `ue` on `nuc2 / UE` contained the human/operator controller shell that launched the manual P7B runner;
- the alternative `srs-ue` session was absent in that capture;
- the restore log ends at this exact first UE-cleanup boundary;
- the controller/runner disappears while detached child processes continue;
- UE service/tunnel are removed but CORE is untouched because the restore helper never reaches CORE cleanup.

The exact Unix signal is not recorded, so no specific signal is claimed.

RLF/RRC reconnects and `SECURITY_MODE_REJECT`/NAS-integrity messages remain retained observations. They are not promoted to the first cause of the controller disappearance and do not convert B1 into a scientific failure.

## H1 amendment source — retained as draft provenance

Offline draft:

`experiments/WP-PWD01/P7B_CONTROLLER_SESSION_DISJOINTNESS_AMENDMENT_DRAFT_2026-08-28.md`

The draft remains provenance for the H1-derived A1–A7 proposal. H2.1 translated it into a separate machine-readable prospective delta; the draft itself grants no authority.

## WP2-P7B-H2.1 — PASS

Terminal verdict:

`H2_1_CONTRACT_DELTA=PASS`

Canonical closure:

`docs/WP2_P7B_H2_1_EXECUTABLE_CONTRACT_DELTA_CLOSURE_2026-08-28.md`

Prospective executable delta:

`experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json`

H2.1 deliberately did **not** edit the frozen base contract `p7b-executable-contract-v2.json`. Instead it pins that base and machine-encodes A1–A7 as operational safety/observability changes only.

H2.1 QA:

- delta commit: `46ec4dd758847fe2a16325739107b68ca05c811e`
- test commit: `5d6fa9d74bf5f4b1059434fc46344d264694c52e`
- Local Unit Tests run: `33139803749`
- job: `98747874891`
- result: **135/135 PASS**
- POWDER contact: **NONE**
- scientific mutation: **NONE**

## WP2-P7B-H2.2 — PASS

Terminal verdict:

`H2_2_SESSION_OWNERSHIP=PASS`

Canonical closure:

`docs/WP2_P7B_H2_2_CONTROLLER_SESSION_OWNERSHIP_REPAIR_CLOSURE_2026-08-28.md`

H2.2 implements only A1–A3 prospectively and offline.

New implementation surfaces:

- `src/wellpulse/p7b_session_ownership.py`
- `scripts/wp2_p7b_service_restore_h2.sh`
- `scripts/wp2_p7b_c_node_h2.py`
- `tests/test_wp2_p7b_h2_session_ownership.py`

Key safety change:

`DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO`

The prospective H2 restore contains no `tmux kill-session`. It discovers exact `srsue`/`srsenb`/`srsepc` PIDs, proves the controller PID is not among them, terminates only those service PIDs, and fails closed if stale service tmux state remains rather than destroying that session blindly.

The historical `scripts/wp2_golden_service_restore.sh` remains unchanged as provenance and is not the prospective H2-safe restore.

H2.2 QA:

- implementation commit: `989162cdc82fb0233cceee89e8e39e6780c2e728`
- QA trigger commit: `1eeb8771d0cc36f10f6684b55e499d0f3f071d38`
- Local Unit Tests run: `33140208485`
- job: `98749151195`
- result: **147/147 PASS**
- H2.2-specific tests: **12/12 PASS**
- POWDER contact: **NONE**
- live service mutation: **NONE**
- scientific mutation: **NONE**

The machine-readable H2 delta now records `status=OFFLINE_H2_2_SESSION_OWNERSHIP_PASS_NOT_LIVE_AUTHORITY`. All live/reservation/RF/retry/W1-B2/teardown/scored/WP3 authority remains false.

`H2_PROGRESS=40%`

## Frozen scientific controls

No H1, H2.1, or H2.2 action changed these controls:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuator IDs `[1,33,2,34]`, coupled.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct clocks.
- `H_app=300 s` from `t_service_ready`.
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`.
- preserve `T_service`, `T_app`, `T_total`.
- no outcome/W1/Golden/scored-derived re-estimation of H.
- pre-Q0 = `60 s`.
- Q3 duration = `120 s`.
- gateway/client restart offset = `60 s` into Q3.
- exact cell order = `B1 -> W1 -> B2`.
- generator remains outside gateway restart domain.
- no automatic scientific retry.
- negative/null/unfavourable evidence remains valid evidence.

## Manual-operation doctrine

For any future human-operated command block, label it explicitly as either:

- `nuc1 / CORE`, or
- `nuc2 / UE`.

Do not add diagnostic sleep/wait delays to manual scripts. Frozen scientific timing inside an authorized runner is separate and remains mandatory.

Evidence survival must remain simpler than the application path: shell/coreutils primitives, explicit per-node ownership, persistent escrow, originating-node pull, immutable artifact, and independent hash/read-back before teardown.

## Exact next bounded patch

`WP2-P7B-H2.3 — INCREMENTAL RESTART/RESTORATION FRONTIER EVIDENCE`

H2 is **OFFLINE / IN PROGRESS — 40%**.

H2.3 may only implement the already-frozen prospective A4–A6 controls offline:

1. write `restart_transition.json` immediately after replacement gateway start is proven;
2. write durable restoration-frontier markers before/after destructive restoration phases;
3. add supplementary parent-controller trap/flush handling that correctness does not depend on;
4. add offline tests of incremental evidence survival.

H2.3 must not contact POWDER, create a reservation, mutate RF, restart live services, retry B1, execute W1/B2, teardown, score, or alter scientific controls.

Remaining H2 patches after H2.3:

- H2.4 — static/adversarial QA;
- H2.5 — contract/runtime regression gate;
- H2.6 — future non-scored requalification authority decision.

Even a terminal H2 PASS does not itself contact POWDER. Any future live action requires a separate explicit user authority and must first establish the then-current reservation/access situation without assuming the historical reservation survives.

## Prohibited until a later explicit authority decision

- no POWDER contact;
- no reservation creation;
- no RF mutation;
- no service restart;
- no B1 retry;
- no W1/B2;
- no Golden rerun;
- no H recalibration;
- no scored B1/W1/B2;
- no teardown;
- no WP3;
- no scientific-control drift.

## Mandatory next-agent read order

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P7B_H1_ABORT_EVIDENCE_FREEZE_ROOT_CAUSE_CLOSURE_2026-08-28.md`
3. `evidence/powder/wp2-p7b-h1-abort-root-cause.json`
4. `experiments/WP-PWD01/P7B_CONTROLLER_SESSION_DISJOINTNESS_AMENDMENT_DRAFT_2026-08-28.md`
5. `experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json`
6. `docs/WP2_P7B_H2_1_EXECUTABLE_CONTRACT_DELTA_CLOSURE_2026-08-28.md`
7. `docs/WP2_P7B_H2_2_CONTROLLER_SESSION_OWNERSHIP_REPAIR_CLOSURE_2026-08-28.md`
8. `src/wellpulse/p7b_session_ownership.py`
9. `scripts/wp2_p7b_service_restore_h2.sh`
10. `scripts/wp2_p7b_c_node_h2.py`
11. `docs/WP2_P7B_MANUAL_ABORT_HANDOVER_2026-08-28.md`
12. `experiments/WP-PWD01/p7b-executable-contract-v2.json`
13. `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`
14. `scripts/wp2_p7b_c_node_r2.py`
15. `scripts/wp2_p7b_c_node_r1.py`
16. `scripts/wp2_p7b_c_node.py`
17. `scripts/wp2_golden_service_restore.sh`
18. `scripts/wp2_p7b_target_node_preflight.sh`
19. current `Research & Grants — Lessons Learned Ledger` in Drive

## Stop state

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

`H2_1_CONTRACT_DELTA=PASS`

`H2_2_SESSION_OWNERSHIP=PASS`

`H2_PROGRESS=40%`

`NEXT_PATCH=WP2-P7B-H2.3_INCREMENTAL_RESTART_RESTORATION_FRONTIER_EVIDENCE`

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`RETRY=NO_UNDER_CURRENT_CONTRACT`

`TEARDOWN=NO`

`LIVE_POWDER_AUTHORIZATION=NO`

**STOP — H2.2 CLOSED. H2.3 NOT STARTED.**
