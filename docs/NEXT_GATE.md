# Next Gate — WP2 Golden E2E Rehearsal

**Current frontier:** RS-7 COMPLETE / GOLDEN RESERVATION READY  
**Scientific completion:** 20%  
**Scored authorization:** `false`

## Frozen state

- H1 remains `VALID_W1_RECOVERY_FAILURE`; no reclassification.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled.
- Recovery-semantics amendment v1 and protocol v0.6 remain frozen.
- Primary cohort cutoff remains `t_rf_restore`.
- Application horizon remains fixed at 300 s from `t_service_ready`.
- No scored B1/W1/B2 run is authorized.
- H1 raw record-level bundles remain unavailable from user-accessible persistent storage; support recovery remains separate.

## Completed consortium gates

- RS-2 LTE recovery mechanism review — PASS.
- RS-3 estimand/H/fairness review — PASS.
- RS-4 adversarial review — PASS with horizon correction.
- RS-5 prospective amendment — PASS/frozen.
- RS-6 Golden E2E design — PASS/frozen.
- RS-7 implementation/reservation readiness — PASS, `RESERVE=true`.

## Exact next action

Reserve one POWDER slot:

- preferred duration: **120 minutes**;
- minimum: **90 minutes**;
- profile family: `PowderProfiles/srslte-controlled-rf`;
- physical roles: `nuc1` core/eNB/broker/receiver and `nuc2` UE/sender/controller;
- attenuator IDs: `1 33 2 34`;
- purpose: exactly one **non-scored S2-style Golden E2E rehearsal**.

No scored campaign is allowed in this slot.

## Golden execution authority

Canonical runbook: `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`.

Canonical orchestrator: `scripts/wp2_golden_orchestrator.sh`.

Required terminal progression is G0 through G10. Application outcome direction does not determine Golden PASS.

## Mandatory evidence rule

G9 is fail-closed:

1. freeze raw evidence;
2. SHA-256 manifest;
3. verified copy to `/proj/WellPulse/evidence-escrow/<experiment>/<run-id>/`;
4. verified copy to Google Drive remote `gdrive:` rooted at `POWDER_EVIDENCE_ESCROW`;
5. Drive read-back SHA-256 verification;
6. if Drive save/verification fails, retry the save action;
7. after retry exhaustion: `STOP_DO_NOT_TERMINATE=1`;
8. teardown only after `EVIDENCE_ESCROW_GATE=PASS` and `TEARDOWN_AUTHORIZED=YES`.

The Google Drive destination is already authenticated/listable from POWDER. Credentials remain outside Git and scientific artifacts.

## Reservation verdict

`RS7_CURRENT_VERDICT=RESERVE`

`RESERVE=true`

`RS7_ACCEPTED_PROGRESS=100/100`

`scored_runs_authorized=false`
