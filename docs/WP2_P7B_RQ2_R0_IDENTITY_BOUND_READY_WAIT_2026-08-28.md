# WP2-P7B-RQ2 — Manual R0 Identity Bound / Ready Wait — 2026-08-28

## Terminal state

`P7B_RQ2_R0_IDENTITY=PASS_BOUND`

`EXPERIMENT_ID=41d64b85-e743-4d06-a81d-687c28c58e52`

`EXPERIMENT_NAME=WP-05-C`

`RESERVATION_READY_CONFIRMED=NO`

`LAST_OBSERVED_RESERVATION_STATUS=booting`

`WORKFLOW_DISPATCH=NO`

`POWDER_CONTACT=NO`

`PORTAL_CONTACT=NO`

`SSH=NO`

`RF_MUTATION=NO`

`SERVICE_MUTATION=NO`

`B1_RQ2=NOT_STARTED`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`TEARDOWN=NO`

## R0 identity source

The user supplied the POWDER experiment status URL:

`https://www.powderwireless.net/status.php?uuid=41d64b85-e743-4d06-a81d-687c28c58e52`

Therefore the exact reservation identity is bound as:

- experiment ID: `41d64b85-e743-4d06-a81d-687c28c58e52`
- experiment name: `WP-05-C`

The immediately preceding user screenshot showed the reservation in state `booting`, with `nuc1` and `nuc2` still `changing` / `pending`. The identity is therefore accepted, but readiness is **not** inferred from the URL alone.

## Visible reservation facts from the user screenshot

- project: `WellPulse`
- profile: `srslte-controlled-rf`
- displayed profile RefSpec prefix: `a6da9656`
- `enb1 -> nuc1`
- `rue1 -> nuc2`
- hardware displayed: `nuc5300`
- image displayed: `PowderProfiles/U18LL-SRSLTE:1`
- state displayed: `booting`
- node status displayed: `changing`
- startup displayed: `pending`

These are observational screenshot facts only. M1 remains responsible for authoritative read-only reservation/manifest verification once the one-shot workflow is dispatched.

## Fail-closed readiness rule

The P7B-RQ2 workflow is one-shot: the first real `workflow_dispatch` consumes the single session authority. Therefore it must **not** be dispatched while the reservation is known or suspected to be `booting/changing`.

Before dispatch, the user must provide a fresh visual confirmation that the reservation is `ready` and both nodes have completed startup, or another authoritative current-state confirmation must be available.

After readiness is confirmed, dispatch inputs are frozen as:

- `experiment_id=41d64b85-e743-4d06-a81d-687c28c58e52`
- `experiment_name=WP-05-C`
- `authority_id=P7B-RQ2`

Then M0 begins. M1 may perform Portal read-only validation. M2 may SSH/stage only after M1 passes. RF/service mutation remains blocked until M2 passes and M3 begins under the same authority.

## Current gate

`NEXT_STATE=P7B_RQ2_R0_READY_WAIT`

`NEXT_REQUIRED_INPUT=FRESH_READY_CONFIRMATION`

**STOP — R0 IDENTITY BOUND; RESERVATION READY NOT YET CONFIRMED; DO NOT DISPATCH.**
