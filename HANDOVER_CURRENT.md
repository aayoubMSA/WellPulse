# WellPulse — Current Handover

Last updated: 2026-08-28 after **WP2-P7B-H1 aborted-Q3 evidence freeze + offline first-cause classification PASS**.

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

## Draft future amendment — not authority

Offline draft:

`experiments/WP-PWD01/P7B_CONTROLLER_SESSION_DISJOINTNESS_AMENDMENT_DRAFT_2026-08-28.md`

Status:

`DRAFT_OFFLINE_ONLY`

`LIVE_AUTHORIZATION=NO`

`RETRY_AUTHORIZATION=NO`

`NEW_RESERVATION_AUTHORIZATION=NO`

`RF_AUTHORIZATION=NO`

`TEARDOWN_AUTHORIZATION=NO`

`SCORED_AUTHORIZATION=NO`

The draft proposes controller/service-session disjointness, ownership proof before tmux destruction, controller execution outside the restoration failure domain, incremental restart-transition evidence, restoration frontier markers, and adversarial offline QA.

It changes no scientific control.

## Frozen scientific controls

No H1 action changed these controls:

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

`WP2-P7B-H2 — CONTROLLER/RESTORE-DOMAIN CONTRACT AMENDMENT QA + FUTURE REQUALIFICATION AUTHORITY DECISION`

H2 is **OFFLINE / NOT STARTED**.

H2 may only:

1. translate the H1 draft into a finite executable contract delta;
2. repair controller/session ownership boundaries offline;
3. add incremental restart/restoration frontier evidence offline;
4. add static/adversarial tests that prove the controller cannot be killed by service cleanup;
5. run offline contract-delta/runtime regression QA;
6. decide whether a future non-scored requalification can be scientifically authorized under a newly frozen contract.

Even an H2 PASS does not itself contact POWDER. Any future live action must still require separate explicit user authority and must first establish the then-current reservation/access situation without assuming this historical reservation survives.

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
5. `docs/WP2_P7B_MANUAL_ABORT_HANDOVER_2026-08-28.md`
6. `experiments/WP-PWD01/p7b-executable-contract-v2.json`
7. `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`
8. `scripts/wp2_p7b_c_node_r2.py`
9. `scripts/wp2_p7b_c_node_r1.py`
10. `scripts/wp2_p7b_c_node.py`
11. `scripts/wp2_golden_service_restore.sh`
12. `scripts/wp2_p7b_target_node_preflight.sh`
13. current `Research & Grants — Lessons Learned Ledger` in Drive

## Stop state

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`RETRY=NO_UNDER_CURRENT_CONTRACT`

`TEARDOWN=NO`

**STOP — H1 CLOSED. H2 OFFLINE NOT STARTED.**
