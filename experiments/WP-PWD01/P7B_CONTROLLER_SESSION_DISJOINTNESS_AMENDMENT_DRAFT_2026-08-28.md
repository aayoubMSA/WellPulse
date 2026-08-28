# P7B Controller/Service-Session Disjointness Amendment — DRAFT — 2026-08-28

## Authority status

`STATUS=DRAFT_OFFLINE_ONLY`

`LIVE_AUTHORIZATION=NO`

`RETRY_AUTHORIZATION=NO`

`NEW_RESERVATION_AUTHORIZATION=NO`

`RF_AUTHORIZATION=NO`

`TEARDOWN_AUTHORIZATION=NO`

`SCORED_AUTHORIZATION=NO`

This draft exists only because H1 classified the aborted-Q3 first technical cause as controller/session/infrastructure. It does not amend the frozen scientific controls unless and until a later bounded offline QA/authority decision explicitly promotes a tested version.

## Root-cause input

H1 closure:

`docs/WP2_P7B_H1_ABORT_EVIDENCE_FREEZE_ROOT_CAUSE_CLOSURE_2026-08-28.md`

Classified cause:

`CONTROLLER_SESSION_COLLISION_SERVICE_RESTORE_KILLED_OPERATOR_TMUX_UE`

The manual controller was hosted inside tmux session `ue` on `nuc2 / UE`. The frozen service-restore helper used `tmux kill-session -t ue` as its first UE cleanup action. The runner disappeared at that exact restore frontier.

## Scientific controls explicitly unchanged

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`
- attenuator IDs = `[1,33,2,34]`, coupled
- pre-Q0 = `60 s`
- Q3 duration = `120 s`
- gateway/client restart offset = `60 s` into Q3
- exact cell order = `B1 -> W1 -> B2`
- generator remains outside gateway restart domain
- primary cohort cutoff = `t_rf_restore`
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct
- `H_app=300 s` from `t_service_ready`
- primary endpoint remains `completeness_300`
- preserve `T_service`, `T_app`, `T_total`
- no outcome/W1/Golden/scored-derived re-estimation of H
- no automatic scientific retry
- negative/null evidence remains evidence

## Proposed operational amendment controls

### A1 — Controller/session disjointness pre-RF gate

Before any RF mutation, record the controller process/session identity on every target host it occupies.

A live controller must fail closed if it resides inside any tmux/session namespace that the service-management path may kill, reset, or reuse, including at minimum `ue`, `srs-ue`, `enb`, `srs-enb`, and `srs-epc` where applicable.

Required prospective marker:

`CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS`

### A2 — Ownership proof before tmux-session destruction

Generic `tmux kill-session -t <name>` is prohibited in restoration/cleanup unless the implementation first proves that the named session is owned exclusively by the intended service and does not host the controller/operator.

Preferred design is exact service-process ownership and PID-scoped termination rather than a generic session-name kill.

### A3 — Controller outside the restoration failure domain

The qualification controller must execute outside the service namespace it restores. A CI/controller host or a dedicated control session not touched by service cleanup is preferred.

Self-SSH is not itself prohibited, but no self-SSH cleanup command may destroy the shell/session/process issuing or supervising that command.

### A4 — Incremental restart-transition evidence

The runner should write an intermediate proof immediately after the replacement gateway process has started and passed its restart-start gate, before waiting for Q3 completion or LTE restoration.

Prospective file:

`restart_transition.json`

Minimum fields:

- generator PID before/after transition
- old gateway PID and observed exit
- new gateway PID and observed start
- client/topic identity
- restart-request UTC/monotonic timestamps
- old-exit UTC/monotonic timestamps
- new-start/new-ready UTC/monotonic timestamps
- source-generation continuity status available at that frontier

The existing final `restart_proof.json` remains the later full-horizon proof and is not replaced.

### A5 — Incremental restoration frontier evidence

Before and after each potentially destructive restoration substep, write a durable phase marker. At minimum distinguish:

1. restore requested
2. UE cleanup begin/end
3. CORE cleanup begin/end
4. CORE start begin/end
5. CORE stable-ready
6. UE start begin/end
7. UE process-ready
8. service-ready probe begin/end

This is observability only and must not add artificial diagnostic delay to the scientific schedule.

### A6 — Parent-controller survival handling

The prospective controller should record/trap termination conditions where technically reliable (`EXIT`, `TERM`, `HUP`) and flush the latest phase/frontier marker before exit. This mechanism is supplementary evidence only; correctness must not depend on a trap always running after abrupt infrastructure loss.

### A7 — Static/adversarial QA before any future live authority

Any promoted amendment must include offline regression tests that prove at least:

- a controller intentionally placed in tmux `ue` is rejected before RF;
- service cleanup does not kill a controller in its allowed control namespace;
- service-owned tmux/PID selection cannot match the controller PID/session;
- `restart_transition.json` survives a synthetic failure immediately after gateway restart;
- a synthetic failure during each restoration phase preserves the last completed frontier;
- no test changes frozen RF/timing/scientific controls;
- no automatic retry is introduced.

## Promotion gate

This draft must remain non-authoritative until a future bounded offline patch performs implementation design, static/adversarial QA, contract-delta audit, and an explicit authority decision.

A future PASS of those offline gates still would not itself authorize POWDER contact or a scientific retry; separate explicit live authority would remain mandatory.
