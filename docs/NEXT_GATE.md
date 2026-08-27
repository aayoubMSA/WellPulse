# Next Gate — WP2 Pre-Integration Compatibility + HCI/Raw-Evidence Review

**Current frontier:** GOLDEN A3 CLOSED / REBOOK NOT YET AUTHORIZED  
**Scientific completion:** 20%  
**Scored authorization:** `false`

## Current state

- Experiment `WP-GOLDEN-A3` / UUID `357f3275-403d-491a-906f-99677bdf454f` is no longer resolvable by the POWDER Portal API as of `2026-08-27T11:55:56Z` (`404 No such experiment`).
- Attempt 6 reached G6 PASS but became `DIAGNOSTIC_NONCANONICAL` at G7 because a supposedly read-only attenuator status probe invoked `tmcc attenuator <id>` and POWDER reported mutation semantics (`changing attenuation`).
- Attempt 7 passed request/static and Google Drive pre-mutation gates, then stopped before science because A3 no longer existed.
- No scored run occurred.
- G8/G9/G10 did not PASS in A3.

## Frozen scientific state

- H1 remains `VALID_W1_RECOVERY_FAILURE`; no reclassification.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled.
- Recovery-semantics amendment v1 and protocol v0.6 remain frozen.
- Primary cohort cutoff remains `t_rf_restore`.
- Application horizon remains fixed at 300 s from `t_service_ready`.
- `H = UNFROZEN`.
- `scored_runs_authorized=false`.

## Mandatory next gates

Before requesting or instantiating another POWDER experiment, complete both:

1. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
2. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`

for the GitHub Actions ↔ POWDER Golden integration.

Minimum evidence required:

1. Official/authoritative semantics for Portal API experiment lifecycle/status/expiry operations.
2. Exact POWDER profile revision, NUC hardware bindings, and startup/cleanup behavior.
3. Authoritative semantics for `tmcc attenuator`, including whether a truly read-only query exists.
4. Exact runtime/version fingerprints on GitHub and POWDER sides.
5. Auth/secret/redaction contract; no TLS session-secret material in logs/evidence.
6. Workflow concurrency, retry, trigger, and state-ownership contract.
7. Reservation budget proving sufficient time for setup + Golden G0–G10 + raw-data freeze/hash + dual evidence escrow + read-back verification + safe shutdown margin.
8. Persistence contract for `/proj/WellPulse` plus verified off-POWDER Drive escrow.
9. Explicit list of safe observability calls allowed during G3–G10; all unqualified probes prohibited.
10. Simple PI-facing live HCI fed only by orchestrator/process-emitted events; no HCI control path into POWDER during the protected scientific window.
11. Complete raw-data inventory independent of HCI counters/summaries.
12. Benchmark decision on whether in-run `/proj` checkpoint copying is non-perturbing; no unqualified background sync.
13. Boundary smoke tests and fail-close/rollback behavior.
14. End-to-end raw freeze/hash/persistent-copy/off-platform-copy/read-back verification before teardown.

Required gate outputs:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Until then:

`REBOOK_GOLDEN=false`

## Required HCI behavior for the next run

The PI-facing cockpit should show, simply:

- experiment/run identity and NON-SCORED status;
- reservation remaining safe budget;
- G0-G10 progress and current phase;
- latest PASS/FAIL event and timestamp;
- safe workload-emitted counters such as generated/published/PUBACK/received when available;
- `t_rf_restore` and `t_service_ready` when emitted;
- raw-evidence state;
- `/proj` copy state;
- off-POWDER copy/read-back state;
- fail-close and teardown authorization state.

The HCI consumes a one-way event/status stream. It must not independently SSH/API/CLI/poll/probe/reconfigure the live experiment during G3-G10.

`HCI_CONTROL_ACTIONS_ENABLED=false`

## Raw-data requirement

A successful HCI display is not evidence completion.

Before teardown require:

`RAW_EVIDENCE_COMPLETE=PASS`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

## After both gates PASS

1. Request/instantiate the smallest new non-scored Golden reservation with a measured safe time budget.
2. Confirm exact expected hardware/profile/runtime before workload launch.
3. Run one clean G0–G10 rehearsal with the passive HCI and no independent unqualified probes during the scientific window.
4. Preserve and verify complete raw evidence before teardown.
5. Only after Golden PASS may H requalification be considered.
6. Scored campaign remains prohibited until separately authorized by the frozen scientific gates.
