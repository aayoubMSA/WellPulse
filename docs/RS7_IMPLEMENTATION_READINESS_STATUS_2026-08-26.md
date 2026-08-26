# WellPulse WP2 — RS-7 Implementation & Reservation Readiness Status

Date: 2026-08-27
Owner: Pre-Reservation Consortium
Stage: RESERVATION READY / PRE-SCORE

## Executive verdict

**RESERVE — Golden rehearsal authorized; scored runs remain unauthorized.**

The Golden E2E implementation package exists, passed offline static/functional QA, and the real Google Drive remote is authenticated and listable from the POWDER execution environment. The user explicitly approved proceeding without a separate disposable write/read/delete preflight. Risk is controlled prospectively by making G9 itself fail-closed and retrying Drive escrow until verified; teardown is prohibited unless the persistent `/proj` copy and Google Drive read-back SHA-256 verification both pass.

## Work-package status

### WP7.1 — Existing implementation recovery — PASS — 15/100
Recovered and reconciled the actual H1 implementation and execution dependencies.

### WP7.2 — Golden orchestration package — PASS — 30/100
Implemented frozen G0-G10 orchestration, deterministic LTE restoration, architecture-blind service readiness, fixed 300 s observation, visible progress, and explicit failure classes.

### WP7.3 — Evidence, reconstruction, and fail-closed teardown — PASS — 30/100

Implemented and QA'd:

- exact evidence inventory;
- raw-record reconstruction;
- source SHA-256 manifest;
- verified persistent `/proj/WellPulse/evidence-escrow/...` copy;
- rclone Google Drive adapter;
- exact remote read-back SHA-256 verification;
- teardown guard;
- corruption/failure tests;
- automatic Drive retry loop.

Operational external destination:

- Google Drive folder: `P12_WellPulse / 00_Validation_Workspace / 02_RAW_EVIDENCE / POWDER_EVIDENCE_ESCROW`
- folder ID: `18i-tHVI7YYCqeZMHDB-bXvUsXZ1D68km`
- rclone remote: `gdrive:` rooted at that folder.

Live connection gate already passed: configured remote exists and `rclone lsf gdrive:` succeeds from POWDER.

The separate disposable write/read/delete probe was intentionally waived in favor of validating the actual evidence transfer at G9. This does not weaken teardown safety because G9 now performs the real copy and full read-back SHA-256 verification. If saving or verification fails, the transfer is retried automatically. After the configured retry budget is exhausted the result is `STOP_DO_NOT_TERMINATE=1`; the experiment must remain available and G9 may be rerun. No teardown authorization is emitted until verified Drive evidence exists.

### WP7.4 — Reservation readiness QA — PASS — 25/100

Resource requirement:

- profile family: `PowderProfiles/srslte-controlled-rf`
- physical roles: `nuc1` core/eNB/broker/receiver, `nuc2` UE/sender/controller
- attenuator IDs: `1 33 2 34`
- no GPU or extra radio resources.

Time budget:

- provisioning/preflight: 20-25 min
- Golden scientific sequence: <=10 min
- collection/reconstruction: ~10 min
- `/proj` + Drive escrow/read-back verification: 10-15 min
- contingency/retry: ~20 min
- safe closeout margin: ~15 min

**Reservation duration: 120 minutes preferred; 90 minutes minimum.**

## Live G9 rule

Required sequence:

1. freeze admitted raw evidence;
2. create source SHA-256 manifest;
3. copy to `/proj/WellPulse/evidence-escrow/<experiment>/<run-id>/`;
4. verify persistent copy against source hashes;
5. copy verified persistent bundle to `gdrive:<experiment>/<run-id>/`;
6. read back every admitted Drive object and recompute SHA-256;
7. if any copy/read/verification step fails, retry the Drive save action;
8. if retries exhaust, hard STOP and do not terminate the POWDER experiment;
9. only after the rclone teardown guard passes may `TEARDOWN_AUTHORIZED=YES` be emitted.

This directly implements the no-repeat control created after H1.

## Final consortium decision

`RS7_CURRENT_VERDICT=RESERVE`

`RESERVE=true`

`RS7_ACCEPTED_PROGRESS=100/100`

`scored_runs_authorized=false`

Next action: reserve one 120-minute POWDER slot and execute exactly one non-scored Golden E2E rehearsal. Do not run B1/W1/B2 scored experiments in that reservation.
