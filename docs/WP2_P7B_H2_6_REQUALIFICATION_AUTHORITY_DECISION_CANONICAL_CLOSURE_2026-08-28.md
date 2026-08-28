# WP2-P7B-H2.6 — Requalification Authority Decision + Canonical Closure — 2026-08-28

## Terminal verdict

`WP2_P7B_H2=PASS`

`WP2_P7B_H2_DETAIL=PASS_REQUALIFICATION_REPAIR_CLOSED`

`H2_PROGRESS=100%`

`POWDER_CONTACT=NO`

`NETWORK_CONTACT=NO`

`LIVE_POWDER_AUTHORIZATION=NO`

`NEW_RESERVATION_AUTHORIZATION=NO`

`RF_AUTHORIZATION=NO`

`B1_REQUALIFICATION_AUTHORIZATION=NO`

`W1_B2_AUTHORIZATION=NO`

`SCORED_AUTHORIZATION=NO`

`TEARDOWN_AUTHORIZATION=NO`

`WP3_EXECUTION_AUTHORIZATION=NO`

H2.6 consumed H1 and H2.1–H2.5 evidence and closes the controller/session recovery program. The repair is sufficient for a future **non-scored physical requalification request**, but this closure itself grants no live execution authority.

## Authority decision

Canonical prospective authority overlay:

`experiments/WP-PWD01/p7b-h2-requalification-authority-v1.json`

Exact Git blob:

`76522aa16d9af09d2f3d779a256236f752850245`

Authority ID:

`P7B-RQ2`

The overlay deliberately does not edit or replace the frozen scientific/runtime contracts. It binds them together with the validated H2 safety/observability layer.

If a separate future user authorization is issued for `P7B-RQ2`, the prospective node entrypoint is:

`scripts/wp2_p7b_c_node_h2.py`

Exact blob:

`d66bc791455127ef87497cea3e912ee6f46e685b`

This wrapper inherits the frozen r2 implementation and installs A1–A6 before inherited execution. It is not live-authorized by this closure.

## Historical attempt semantics

The prior B1 attempt remains permanently:

`B1=NULL_ABORTED_AFTER_Q3`

The historical attempt is consumed and is not reinterpreted as PASS or FAIL.

Any later user-authorized `P7B-RQ2` execution would be a **new bounded non-scored requalification session**, not continuation of the aborted run and not an automatic retry.

The overlay permits at most one new reservation and one live session **only if separately authorized later**. GitHub may not create the reservation. The user remains the manual reservation boundary.

## Required future boundary

Before any future live action, all of the following remain mandatory:

1. a separate explicit user instruction authorizing `P7B-RQ2` live execution;
2. then-current reservation/access validation;
3. user creation or selection of the POWDER reservation and provision of `experiment_id` + `experiment_name`;
4. M0 exact authority/source/contract SHA freeze;
5. M1 read-only reservation/EFCC delta validation;
6. M2 controller-session disjointness + target preflight;
7. M3 known-good Q0 baseline before treatment;
8. paired evidence survival/readback after every scientific cell;
9. no automatic retry, second reservation, extension, or teardown.

A future live workflow `.github/workflows/wp2-p7b-rq2-session.yml` must remain absent until that separate user live authorization exists.

## Frozen scientific state

H2 closure does not alter:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuators `[1,33,2,34]` coupled;
- pre-Q0 `60 s`;
- Q3 `120 s`;
- restart `60 s` into Q3;
- cell order `B1 -> W1 -> B2`;
- cohort cutoff `t_rf_restore`;
- `H_app=300 s` anchored at `t_service_ready`;
- distinct `t_rf_restore`, `t_service_ready`, `t_app_complete`;
- generator outside gateway restart domain;
- negative/null/unfavourable evidence retention;
- no automatic scientific retry.

Frozen contract blobs remain:

- executable contract v2 `233aabeaf3081470bc3ebc1ee04168f8932fc415`;
- target-runtime contract v2 `9531893989effb142e694294b95c0c7146353742`;
- modular pipeline v1 `2c85af21f502c092c2da0ecb1bf615c8f705069b`;
- historical Golden restore `cdf865eaaaf1c08bc8f7a8896d7f705739e60b9c`.

## Final QA

Final canonical QA after normalizing the H2 terminal gate:

- commit `8735013bedc6d576424b0aa88670cd6ea68caa45`
- workflow `Local Unit Tests`
- run `33142326835`
- job `98755668809`
- Python `3.12.14`
- Paho MQTT `2.1.0`
- **174/174 tests PASS**
- **6/6 H2.6-specific tests PASS**

The immediately preceding H2.6 QA run `33142248360` also passed 174/174; the second run exists only to normalize the terminal gate from an expanded label to the canonical exact `WP2_P7B_H2=PASS` required by the H2 promotion contract.

Machine-readable H2.6 result:

`evidence/powder/wp2-p7b-h2-6-authority-decision.json`

## H2 completion

- H2.1 Contract Delta — PASS
- H2.2 Controller/Session Ownership Repair — PASS
- H2.3 Incremental Failure Evidence — PASS
- H2.4 Static + Adversarial QA — PASS
- H2.5 Contract/Runtime Regression Gate — PASS
- H2.6 Requalification Authority Decision + Canonical Closure — PASS

`H2_PROGRESS=100%`

## Stop state

`NEXT_STATE=STOP_H2_COMPLETE_AWAIT_SEPARATE_EXPLICIT_USER_LIVE_AUTHORIZATION_P7B_RQ2`

No live workflow was created. No reservation was created or selected. No POWDER target was contacted. No RF/service mutation or experiment retry occurred.

**STOP — H2 COMPLETE. P7B-RQ2 LIVE EXECUTION NOT AUTHORIZED.**
