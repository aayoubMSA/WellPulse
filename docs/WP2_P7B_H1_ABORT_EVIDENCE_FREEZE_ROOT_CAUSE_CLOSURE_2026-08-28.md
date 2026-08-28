# WP2-P7B-H1 — Aborted-Q3 Evidence Freeze + Offline Root-Cause Closure — 2026-08-28

## Verdict

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

`P7B_B1_ATTEMPT=ABORTED_AFTER_SCIENTIFIC_IMPAIRMENT`

`B1_SCIENTIFIC_VERDICT=NULL`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`AUTOMATIC_RETRY=PROHIBITED`

`MANUAL_RETRY=PROHIBITED_UNDER_CURRENT_FROZEN_CONTRACT`

`SCORED_AUTHORIZATION=BLOCKED`

`TEARDOWN_AUTHORIZED_BY_H1=NO`

## Scope

H1 was restricted to preservation of the already-aborted B1 attempt, off-testbed evidence survival, independent read-back, and offline first-cause classification. H1 did not create a reservation, change RF, restart any service, rerun B1, execute W1/B2, perform scored work, or teardown the reservation.

Latest scientific attempt:

- reservation UUID: `f6de95cb-a13a-421e-bd0e-766dfc1d3fb3`
- reservation name: `wp7brq2609012`
- run ID: `wp2-p7b-manual-20260828T024433Z`
- CORE: `nuc1`
- UE: `nuc2`
- evidence class: `NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION`

Current reservation liveness is not implied by this closure and must not be assumed later.

## H1 evidence-survival execution

A preservation-only one-shot operational branch and workflow were used:

- operational branch: `wp2-p7b-h1-freeze-20260828`
- workflow: `.github/workflows/wp2-p7b-h1-abort-freeze.yml`
- operational commit: `118a8c025ef0be5a643f710ff9c620abdcb5698b`
- GitHub Actions run: `33138161593`
- job: `98742778306`
- workflow conclusion: `SUCCESS`

The workflow contained no reservation creation, RF mutation, service restart, B1/W1/B2 execution, teardown, or scored action. Each remote operation was explicitly labelled `nuc1 / CORE` or `nuc2 / UE`.

Preservation chain completed:

`node raw -> /proj H1 escrow -> per-node hash/package -> controller pull from originating node -> controller hash/read-back -> GitHub artifact -> independent artifact download/read-back`

### Immutable off-POWDER evidence

- GitHub artifact ID: `9672862285`
- artifact name: `wp2-p7b-h1-abort-freeze-33138161593`
- artifact bytes: `1,972,916`
- artifact SHA-256: `a7e3b06d27f46729fcf0ce57aab217a1cf2c1e9edb71211db58d0a7f9063d09d`
- independent downloaded artifact SHA-256: exact match
- `CONTROLLER_SHA256SUMS`: PASS
- UE package SHA/read-back: PASS
- CORE package SHA/read-back: PASS
- UE internal `SOURCE_SHA256SUMS`: PASS
- CORE internal `SOURCE_SHA256SUMS`: PASS

Durable Drive copy:

- canonical Drive file ID: `1mE3GX6lm5k6DeUXaYqOmz7N74rKgYBJ3`
- canonical filename: `wp2-p7b-h1-abort-freeze-33138161593.zip`

Two accidental Drive duplicate uploads were immediately renamed with `NONCANONICAL_DUPLICATE` prefixes and are not canonical evidence. They are not referenced for any claim.

## Previously existing abort freeze retained

The H1-frozen `/proj` tree revealed that a prior local abort-freeze operation had in fact been executed after the earlier handover text was written. It produced:

- `WP2_P7B_ABORT_FREEZE=PASS`
- prior aborted bundle: `/proj/WellPulse/evidence/wp2-p7b-manual-20260828T024433Z-ABORTED-B1-EVIDENCE.tar.gz`
- prior bundle SHA-256: `a2f9e4a8677bc5b3488da6bf0aad76ad9c67eea2a755009d7cad745228b2b836`

The earlier statement that this sprint had not yet executed is retained as historical provenance rather than silently rewritten. H1 supersedes that uncertainty for evidence survival because H1 completed independent off-POWDER pull and read-back.

## Scientific boundary remains unchanged

Frozen evidence proves:

- B1 independent Q0/readiness gate: PASS
- `Q3_STARTED=YES`
- Q3 attenuator set evidence exists
- scientific impairment therefore started
- B1 completed cells: none
- W1/B2 never started
- `restart_proof.json` is missing
- `t_service_ready` and `t_app_complete` are missing

The missing final `restart_proof.json` does not mean that the gateway restart did not occur. The frozen runner writes that final proof only near the end of the cell after RF restoration, service recovery, the fixed application horizon, and final checks.

## Offline execution-frontier reconstruction

The raw evidence reconstructs the frontier as follows:

1. B1 cell began at approximately `2026-08-28T02:44:44Z`.
2. Q3 began at approximately `2026-08-28T02:45:46.961547Z`.
3. The old B1 gateway stop was requested at approximately `02:46:46.970797Z`.
4. The old gateway exited at approximately `02:46:46.986343Z`.
5. A new gateway process started at approximately `02:46:51.402954Z`.
6. The telemetry generator remained alive and continued generating records.
7. At the Q3 end, the runner issued Q0 restore and wrote `t_rf_restore` at approximately `02:47:47Z`.
8. `wp2_golden_service_restore.sh` began at `2026-08-28T02:47:47.138928511Z`.
9. The restore log reaches only its first operation: `Stopping UE and clearing profile session/tunnel`.
10. `T_UE_STOPPED` was never written; no later restore milestone exists.
11. After the runner disappeared, detached generator/gateway children continued, `srsue` was absent and `tun_srsue` missing, while CORE `srsepc`/`srsenb` remained running.

This frontier rules out the interpretation that the controller disappeared before the intended gateway restart. The restart occurred; the controller disappeared at the beginning of LTE service restoration.

## First technical root cause

`FIRST_TECHNICAL_ROOT_CAUSE=CONTROLLER_SESSION_COLLISION_SERVICE_RESTORE_KILLED_OPERATOR_TMUX_UE`

`ROOT_CAUSE_CLASS=CONTROLLER_SESSION_INFRASTRUCTURE`

`ROOT_CAUSE_CONFIDENCE=HIGH`

### Evidence chain

`scripts/wp2_golden_service_restore.sh` begins UE restoration by remotely executing, on the UE host, a command whose first destructive action includes:

`tmux kill-session -t ue`

The frozen B1 `q0_radio_capture.txt` proves that tmux session `ue` on `nuc2 / UE` was not merely a service console. Its pane contained the human/operator controller shell used to launch the manual P7B runner, including the manual sprint/runner commands. The alternative `srs-ue` tmux capture was absent.

Therefore the restoration helper targeted the tmux session that hosted the active manual controller. The exact abrupt frontier is consistent with destruction of that controller session: the restore log stops inside the first UE cleanup step, the parent runner disappears, detached generator/gateway processes survive, the UE service/tunnel are removed by the partial cleanup, and CORE remains untouched because the restore helper never reaches its CORE-stop stage.

The exact Unix signal delivered to the runner was not recorded, so this closure does not overclaim a specific signal. The causal controller/session collision is nevertheless directly supported by the session identity and execution frontier.

## What is not classified as the first cause

Repeated RLF/RRC reconnect behaviour and `SECURITY_MODE_REJECT`/NAS-integrity observations are preserved as technical observations. They are not promoted to the first cause of the abrupt runner disappearance because the controller/session collision explains the disappearance at a later, directly evidenced orchestration boundary.

They also do not convert B1 into a scientific failure.

## Future contract consequence

Because the first cause is controller/session/infrastructure, H1 permits an offline future-qualification amendment draft. That draft is:

`experiments/WP-PWD01/P7B_CONTROLLER_SESSION_DISJOINTNESS_AMENDMENT_DRAFT_2026-08-28.md`

It is not live authority and does not authorize a B1 retry, a new reservation, RF mutation, teardown, or scored execution.

## H1 acceptance gates

- `H1_P1=PASS_EVIDENCE_ACCESSIBLE`
- `H1_P2=PASS_DUAL_NODE_RAW_EVIDENCE_FROZEN`
- `H1_P3=PASS_HASH_PACKAGE_CONTROLLER_PULL`
- `H1_P4=PASS_INDEPENDENT_ARTIFACT_READBACK`
- `H1_P5=PASS_FIRST_TECHNICAL_ROOT_CAUSE_CLASSIFIED`
- `H1_P6=PASS_OFFLINE_AMENDMENT_AND_CANONICAL_CLOSURE`

## Frozen stop state

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`AUTOMATIC_RETRY=NO`

`MANUAL_RETRY=NO_UNDER_CURRENT_CONTRACT`

`TEARDOWN=NOT_AUTHORIZED_BY_H1`

No further POWDER action follows from this closure.
