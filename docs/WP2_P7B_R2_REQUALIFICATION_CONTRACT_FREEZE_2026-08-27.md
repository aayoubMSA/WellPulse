# WP2-P7B-R2 — Requalification Authority + Contract Freeze Closure

**Date:** 2026-08-27  
**Verdict:** `WP2_P7B_R2=PASS_ONE_REPLACEMENT_CONTRACT_FREEZE`  
**Decision:** `REQUALIFICATION_DECISION=GO_ONE_REPLACEMENT_NON_SCORED`  
**Replacement authority ID:** `P7B-RQ1`  
**Live authorization:** `P7B_RQ1_LIVE_AUTHORIZED=false`  
**Evidence class:** OFFLINE / NON-SCORED / PRE-SCORE AUTHORITY FREEZE  
**POWDER contact / reservation / SSH / mutation:** NO / NO / NO / NO  
**Scientific run / scored run:** NO / NO  
**Scored authorization:** BLOCKED

## Scope and decision boundary

R2 decides only whether one replacement non-scored physical qualification reservation is prospectively defensible after the first P7B-C reservation stopped before scientific measurement because of a specific orchestration/evidence-path defect that R1 repaired and regression-protected.

R2 does not create a reservation, contact POWDER, activate a workflow, SSH to a node, execute a physical cell, authorize scored work, change the scientific protocol, or relabel the first blocked attempt.

The original P7B contract remains immutable historical authority. It still records `reservation_limit=1`, no automatic retry and no automatic replacement. That original reservation was consumed. R2 therefore uses a separate prospective amendment rather than editing the original contract retroactively.

## Retained first-attempt provenance

The following results remain unchanged:

- experiment UUID `26b6f315-459d-4a56-9167-69228e339f24`;
- experiment name `wp7b3016138`;
- GitHub run `33113016138`;
- `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`;
- completed cells: NONE;
- scientific measurement started: NO;
- W1/B2: NOT STARTED;
- `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`;
- teardown complete after preservation/read-back of the captured declared roots;
- missing receiver event ledger was not reconstructed or backfilled.

The physical pre-block evidence remains informative operational provenance: reservation READY, manifest/profile/SSH gates PASS, B1 Q0 route through `tun_srsue`, five probes at 0% loss, TLS/MQTT readiness PASS, and broker evidence that the receiver connected/subscribed/remained alive.

## Why one replacement is justified

R2 issues GO for exactly one prospective replacement because all of the following are true:

1. the first attempt stopped before generation/scientific measurement;
2. the blocking contradiction was operational, not an unfavorable scientific outcome;
3. broker evidence showed the receiver itself was connected and alive;
4. R1 identified the writer/watcher path mismatch concretely;
5. R1 replaced unresolved remote paths with an absolute-path contract;
6. R1 added receiver process fail-fast and bounded root-cause diagnostics;
7. R1 added absolute-path/hash preservation helpers;
8. R1 passed 65/65 offline tests without scientific drift;
9. R2 adds prospective one-replacement authority rather than treating the old automatic-retry prohibition as optional.

This justification cannot be reused to authorize a second replacement. Any failure of `P7B-RQ1` is terminal for this requalification authority unless a new explicit amendment is separately justified and approved.

## Machine-readable R2 contract

Created:

`experiments/WP-PWD01/p7b-requalification-r2-contract.json`

Creation commit:

`fec4040f01517f1ba92acc3552ef57060297a74c`

Current contract Git blob SHA:

`2a5b7b4ca025811da665dd0159403abc12d4f4a8`

Frozen decision fields include:

- `decision=GO_ONE_REPLACEMENT_NON_SCORED_QUALIFICATION`;
- `authority_id=P7B-RQ1`;
- `maximum_new_reservations=1`;
- `second_replacement_authorized=false`;
- `automatic_retry=false`;
- `automatic_new_reservation=false`;
- `requires_separate_explicit_live_authorization=true`;
- `current_live_authorized=false`;
- `scored_runs_authorized=false`.

## Execution lock

R2 freezes the repaired R1 execution surface:

- tested implementation commit: `695b31cba6c0256b3637223abdfef4f4b11bf6ca`;
- only permitted node entrypoint: `scripts/wp2_p7b_c_node_r1.py`;
- node-entrypoint Git blob SHA: `6d28468c93742046d952668b9df1cad8e6ea78c0`;
- absolute-path contract: `scripts/wp2_p7b_path_contract.py`;
- path-contract Git blob SHA: `2e77e7e355e25c6e3f747956e2f2b0ac5ad46161`;
- preservation helper: `scripts/wp2_p7b_preservation_helpers.sh`;
- preservation-helper Git blob SHA: `9063ec2e97e9cbf7a9f76d6ea10920236d8370ef`;
- historical `scripts/wp2_p7b_c_node.py` is prohibited as a future authority-bearing entrypoint.

The retired historical controller still points to the old node runner and is therefore explicitly **not R2-compliant** and must not be reactivated.

## Future-controller static acceptance gate

Created:

`scripts/wp2_p7b_r2_validate_controller.py`

Implementation commit:

`c4bd71bd6cf8e32d4184cfaaa1976b12e8f3a271`

Current Git blob SHA:

`92961f476ddab32f1df33756d3857ef27df92323`

Before any future live workflow may be created, its authority-bearing controller must pass this static gate. The gate requires at minimum:

- exactly one `portal-cli experiment create`;
- authority marker `P7B-RQ1`;
- exact repaired entrypoint `scripts/wp2_p7b_c_node_r1.py`;
- no invocation of the historical node entrypoint;
- resolved-path preservation helper present;
- `AUTOMATIC_RETRY=NO`;
- `SECOND_REPLACEMENT=NO`;
- no scored authorization marker;
- `EVIDENCE_ESCROW_GATE=PASS`;
- `CONTROLLER_OFFPOWDER_GATE=PASS`;
- `TEARDOWN_AUTHORIZED=YES` before the single terminate operation.

This validator has no POWDER authority and performs only static file inspection.

## Evidence-survival improvement frozen for the replacement

The next live requalification, if separately authorized, must not repeat the C-then-manual-D operational gap. The replacement contract freezes one bounded live chain in which physical qualification evidence is preserved and independently read back before teardown.

Required chain:

`node raw -> /proj persistent escrow -> controller pull -> GitHub artifact -> independent controller read-back -> outer/internal SHA-256 -> teardown`

Additional rules:

- only resolved absolute paths are valid;
- literal `$HOME` or `~` preservation paths fail closed;
- complete raw evidence is required;
- `TEARDOWN_AUTHORIZED=YES` only after both `EVIDENCE_ESCROW_GATE=PASS` and `CONTROLLER_OFFPOWDER_GATE=PASS`;
- if evidence survival/read-back fails, leave the experiment live and STOP;
- no automatic replacement reservation follows any failure.

This is an operational safety improvement only and changes no scientific treatment, endpoint or timing semantics.

## Frozen scientific controls

R2 preserves the original P7B physical design exactly:

- profile `PowderProfiles/srslte-controlled-rf` revision `a6da96560b6526dc6816761282722c996418fd8c`;
- attenuation IDs `1 33 2 34` coupled;
- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- 60 s Q0 pre-impairment interval;
- Q3 = 120 s;
- gateway/client restart 60 s into Q3;
- cell order `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`;
- generator remains outside gateway restart domain;
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct;
- primary cohort cutoff remains `t_rf_restore`;
- `H_app=300 s` from `t_service_ready`;
- preserve `T_service`, `T_app`, `T_total`;
- no RF/H recalibration or outcome-driven protocol change.

`scientific_change_from_original_p7b=false`.

## R2 regression QA

Created:

`tests/test_wp2_p7b_r2_contract.py`

Regression commit:

`b77609bfb9256a0eb189c0e5dd29a2f1f68c3bc2`

Accepted Local Unit Tests:

- run `33117108893`;
- job `98674462071`;
- tested SHA `b77609bfb9256a0eb189c0e5dd29a2f1f68c3bc2`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **73/73 tests PASS**;
- result: SUCCESS.

R2-specific regressions prove:

1. R2 remains offline/non-scored and permits one replacement only;
2. the original reservation limit remains consumed rather than silently reset;
3. original blocked evidence remains immutable;
4. profile/RF/timing/cell order equal the original frozen contract;
5. R1 entrypoint/path/preservation artifacts are frozen and present;
6. evidence gates precede teardown in the future-controller contract;
7. the retired historical controller fails the R2 static acceptance gate;
8. a synthetic compliant future controller passes the gate;
9. no P7B live workflow or RQ1 trigger exists after R2.

All earlier P7B/R1 regressions also remained PASS in the same 73-test run.

## R2 verdict

`WP2_P7B_R2=PASS_ONE_REPLACEMENT_CONTRACT_FREEZE`

`REQUALIFICATION_DECISION=GO_ONE_REPLACEMENT_NON_SCORED`

`P7B_RQ1_AUTHORITY_CONTRACT=FROZEN`

`P7B_RQ1_LIVE_AUTHORIZED=false`

`SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`

`scored_runs_authorized=false`

Successful P7B physical-qualification credit remains **40/100** from A+B only. R1/R2 are repair/authority patches and create no physical or scientific credit. WP2 management/readiness remains **95/100** and scientific weighted completion remains **20%**.

## Exact next bounded patch

`WP2-P7B-R3 — ONE REPLACEMENT NON-SCORED PHYSICAL REQUALIFICATION + EVIDENCE SURVIVAL`

Current status:

`P7B_RQ1_LIVE_AUTHORIZED=false`

R3 requires **separate explicit live authorization**. Generic offline continuation or the R2 GO decision does not authorize R3.

If explicitly authorized later, R3 may create at most the one `P7B-RQ1` reservation, execute only the frozen B1 -> W1 -> B2 sequence with fail-closed readiness, preserve/read-back all evidence, and terminate only after the escrow/off-POWDER gates pass. Any cell/evidence failure stops later scientific actions and does not authorize another reservation.

## Stop boundary

Until separate explicit R3 live authorization exists:

- no POWDER contact/reservation/SSH;
- no P7B-RQ1 reservation;
- no physical B1/W1/B2 requalification;
- no Golden/H/RF recalibration;
- no scored work;
- no OTA replication;
- no WP3;
- no `scored_runs_authorized=true`;
- no immutable pre-score snapshot claiming physical readiness.

**STOP — R2 PASS. P7B-RQ1 contract is frozen but live execution is NOT authorized.**
