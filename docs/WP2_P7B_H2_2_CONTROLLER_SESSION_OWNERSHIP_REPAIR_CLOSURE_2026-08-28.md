# WP2-P7B-H2.2 — Controller/Session Ownership Repair Closure — 2026-08-28

## Terminal verdict

`H2_2_SESSION_OWNERSHIP=PASS`

`POWDER_CONTACT=NO`

`LIVE_SERVICE_MUTATION=NO`

`RF_MUTATION=NO`

`RETRY=NO`

`SCORED=NO`

`TEARDOWN=NO`

H2.2 implements only the prospective A1–A3 operational controls frozen by H2.1. It does not authorize or execute any live POWDER action.

## Root cause addressed

H1 classified the first technical cause as:

`CONTROLLER_SESSION_COLLISION_SERVICE_RESTORE_KILLED_OPERATOR_TMUX_UE`

The historical restore helper used `tmux kill-session -t ue`, while the manual controller itself occupied tmux session `ue` on `nuc2 / UE`.

H2.2 removes this failure mechanism from the prospective path rather than wrapping the same unsafe primitive with another weak check.

## Implementation

### Controller/session guard

New library:

`src/wellpulse/p7b_session_ownership.py`

It fail-closes when:

- the controller session is unknown;
- the controller is in `ue`, `srs-ue`, `enb`, `srs-enb`, or `srs-epc`;
- the controller process identity collides with `srsue`, `srsenb`, or `srsepc`;
- an unapproved process name is selected for service cleanup;
- the controller PID appears in a selected service PID set.

Required prospective markers include:

- `CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS`
- `CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION=PASS`
- `SERVICE_PID_OWNERSHIP_PROOF=PASS`

### Prospective H2 entrypoint

New wrapper:

`scripts/wp2_p7b_c_node_h2.py`

It captures controller PID/process/session before entering the inherited P7B execution path, fails closed if the controller is inside a service cleanup namespace, and installs the H2-safe restore implementation before delegating to the R2 executable-contract/runtime stack.

This wrapper grants no live authority. It explicitly emits:

- `LIVE_AUTHORIZATION=SEPARATE_REQUIRED`
- `SCORED_AUTHORIZATION=BLOCKED`

### Ownership-safe restore

New prospective restore:

`scripts/wp2_p7b_service_restore_h2.sh`

Key repair:

`DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO`

The script contains no `tmux kill-session` operation.

Instead it:

1. requires explicit controller PID/session/host-role identity;
2. rejects controller placement in any service lifecycle tmux namespace;
3. discovers exact `srsue`, `srsenb`, and `srsepc` PIDs;
4. proves the controller PID is not in the selected destructive PID set;
5. terminates only those exact service PIDs;
6. fails closed if a stale service tmux namespace remains after process cleanup rather than destroying that session blindly;
7. continues with the existing profile-authoritative CORE then UE startup order only after the safe cleanup gates pass.

The historical `scripts/wp2_golden_service_restore.sh` is deliberately unchanged and retained as provenance for the H1 failure and Golden history. It is not the prospective H2-safe restore.

## Scientific contract preservation

H2.2 embeds no RF levels, attenuator IDs, cell sequence, H horizon, or primary endpoint values in its new implementation files. The frozen scientific contract remains in the existing executable contract and H2 delta.

No change was made to:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuators `[1,33,2,34]`;
- pre-Q0 `60 s`;
- Q3 `120 s`;
- restart offset `60 s`;
- cell order `B1 -> W1 -> B2`;
- `t_rf_restore`, `t_service_ready`, `t_app_complete` semantics;
- `H_app=300 s` from `t_service_ready`;
- primary cohort cutoff `t_rf_restore`;
- automatic retry prohibition;
- non-scored status.

## QA evidence

Implementation commit:

`989162cdc82fb0233cceee89e8e39e6780c2e728`

Offline QA trigger commit:

`1eeb8771d0cc36f10f6684b55e499d0f3f071d38`

GitHub Actions:

- workflow: `Local Unit Tests`
- run: `33140208485`
- job: `98749151195`
- result: **PASS**
- total tests: **147/147 PASS**
- H2.2-specific tests: **12/12 PASS**
- Python: `3.12.14` on the CI validation host
- Paho MQTT: `2.1.0`
- POWDER contact: **NONE**

The H2.2 tests prove at least:

1. a controller in tmux `ue` is rejected;
2. an attached-SSH/non-tmux or external controller identity is accepted when otherwise valid;
3. a controller process may not masquerade as a service process;
4. controller PID collision with a service cleanup set blocks;
5. unapproved process targets block;
6. the safe restore is Bash syntax-valid;
7. the prospective restore contains no `tmux kill-session`;
8. cleanup is exact PID scoped;
9. the H2 wrapper binds the safe restore before inherited execution;
10. the historical Golden restore remains preserved as provenance;
11. no frozen RF/cell controls are duplicated into the new repair files.

## Contract promotion

The canonical prospective delta was advanced to:

`status=OFFLINE_H2_2_SESSION_OWNERSHIP_PASS_NOT_LIVE_AUTHORITY`

with H2.2 implementation binding recorded in:

`experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json`

All authority flags remain false.

## Next patch

`WP2-P7B-H2.3 — INCREMENTAL RESTART/RESTORATION FRONTIER EVIDENCE`

H2.3 may implement A4–A6 offline only. It must not contact POWDER or authorize retry.

**STOP — H2.2 CLOSED. H2.3 NOT STARTED.**
