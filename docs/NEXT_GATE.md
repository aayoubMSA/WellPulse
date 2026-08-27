# Next Gate — WP2 Pre-Integration Compatibility Review

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

## Mandatory next gate

Before requesting or instantiating another POWDER experiment, complete:

`docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`

for the GitHub Actions ↔ POWDER integration.

Minimum evidence required:

1. Official/authoritative semantics for Portal API experiment lifecycle/status/expiry operations.
2. Exact POWDER profile revision, NUC hardware bindings, and startup/cleanup behavior.
3. Authoritative semantics for `tmcc attenuator`, including whether a truly read-only query exists.
4. Exact runtime/version fingerprints on GitHub and POWDER sides.
5. Auth/secret/redaction contract; no TLS session-secret material in logs/evidence.
6. Workflow concurrency, retry, trigger, and state-ownership contract.
7. Reservation budget proving sufficient time for setup + Golden G0–G10 + evidence escrow + safe shutdown margin.
8. Persistence contract for `/proj/WellPulse` plus verified off-POWDER Drive escrow.
9. Explicit list of safe observability calls allowed during G3–G10; all unqualified probes prohibited.
10. Boundary smoke tests and fail-close/rollback behavior.

Required gate output:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

Until then:

`REBOOK_GOLDEN=false`

## After compatibility PASS

1. Request/instantiate the smallest new non-scored Golden reservation.
2. Confirm exact expected hardware/profile/runtime before workload launch.
3. Run one clean G0–G10 rehearsal with no independent unqualified probes during the scientific window.
4. Require `EVIDENCE_ESCROW_GATE=PASS` before teardown.
5. Only after Golden PASS may H requalification be considered.
6. Scored campaign remains prohibited until separately authorized by the frozen scientific gates.
