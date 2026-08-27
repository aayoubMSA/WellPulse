# WP2-P7B-E — Canonical Blocked Closure

Date: 2026-08-27

## Scope

This patch performs canonical closure only after the authorized live P7B-C reservation and the subsequent P7B-D evidence-survival/teardown attempt. It does not authorize or perform a new POWDER reservation, live rerun, scored execution, RF recalibration, H recalibration, Golden rerun, WP3 execution, or protocol relaxation.

## P7B-C retained result

Authorized live reservation:

- experiment UUID: `26b6f315-459d-4a56-9167-69228e339f24`
- experiment name: `wp7b3016138`
- GitHub run: `33113016138`
- node run ID: `wp2-p7b-c-33113016138-20260827T203140Z`
- evidence class: NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION

Retained verdict:

`WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`

Observed facts:

- the reservation reached Portal `ready`;
- core and UE SSH gates passed;
- frozen profile revision matched;
- B1 Q0 route used `tun_srsue` to `172.16.0.1`;
- five Q0 probes passed with 0% packet loss;
- TLS/MQTT readiness publish passed (`rc=0`);
- broker log proves the receiver client `wp-hcrx-885b10cacb1c` connected, received CONNACK, subscribed to the exact B1 topic, and remained alive through repeated PINGREQ/PINGRESP traffic;
- the controller nevertheless timed out waiting for the expected receiver event ledger;
- completed P7B-C cells: NONE;
- scientific measurement started: NO;
- W1 and B2 did not start;
- scored run: NO.

Root-cause classification is therefore orchestration/evidence-path visibility, not demonstrated LTE or MQTT transport failure. The live command construction passes the receiver `--output-dir` through a single-quoted expression containing `$HOME`, while the console redirect and readiness watcher use the expanded expected path. This creates a path mismatch risk and explains the observed broker-alive / event-ledger-unseen contradiction.

## P7B-D retained result

First preservation attempt:

- GitHub run `33114265831`;
- fail-closed before persistent copy because of a preservation-script path quoting defect;
- no artifact;
- no teardown in this attempt.

Same-reservation preservation retry:

- GitHub run `33114517583`, job `98665610066`: SUCCESS;
- no new reservation;
- no scientific rerun;
- no scored run;
- `/proj` persistence for the declared UE/core roots: PASS;
- controller pull and internal SHA-256 verification: PASS;
- GitHub artifact upload: PASS;
- artifact ID: `9663926250`;
- artifact ZIP digest: `0bd31f534712d2f1fe3793008e7b00c1e6df85f58277686b3de5ffb5fd6455bb`;
- deterministic inner TAR SHA-256: `f49263f77d673cf5961dd6efb3b0ce2a3d7dde5969d48f20e0c383f105693877`;
- deterministic inner TAR bytes: `296960`;
- independent artifact download: PASS;
- independent inner TAR hash verification: PASS;
- independent internal `SOURCE_SHA256SUMS` verification for captured declared roots: PASS;
- teardown authorized only after off-POWDER read-back;
- teardown confirmed when the exact UUID transitioned through `terminating` then became not found.

Strict evidence gap:

- expected core root contained receiver `console.txt` but not the expected `receiver_events.jsonl`;
- the exact missing event ledger was not recovered before teardown;
- therefore complete-raw-evidence survival cannot be claimed.

Strict retained verdict:

`WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`

## P7B-E closure verdict

`WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`

This means the closure record itself is complete and the failed/partial evidence is preserved without relabelling. It does **not** mean P7B physical qualification passed.

Successful P7B qualification credit remains **40/100** from P7B-A and P7B-B only. P7B-C did not pass, P7B-D did not pass strict completeness, and P7B-E administrative closure creates no physical-qualification credit.

WP2 management/readiness remains **95/100**. Scientific weighted completion remains **20%**. Scored authorization remains blocked.

## Frozen controls preserved

No scientific control changed:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuation IDs `1 33 2 34` remain coupled;
- `H_app=300 s` remains frozen;
- no outcome-derived horizon re-estimation;
- no RF recalibration;
- no Golden rerun;
- no H calibration;
- H1 remains valid adverse non-scored evidence;
- K1-K8 remain closed absent material interface change;
- negative/null/unfavorable evidence remains evidence and is not overwritten.

## Next bounded patch — offline only

`WP2-P7B-R1 — RECEIVER-PATH REPAIR + OBSERVABILITY REGRESSION QA`

Purpose:

1. fix the `$HOME`/remote-path quoting defect in the P7B-C receiver launch path;
2. fix the same class of quoting defect in evidence-preservation helpers;
3. make receiver startup fail-fast on process exit and expose the receiver console/event path immediately;
4. echo bounded raw diagnostics into GitHub Actions on failure: receiver process state, receiver console/events, broker tail, route, Q0 probes, TLS probe, runtime/version locks;
5. add regression tests that prove the watcher and receiver write to the identical absolute path and reject literal `$HOME` paths;
6. run offline reconstruction/contract tests only;
7. issue a separate GO/BLOCKED decision for whether a future physical requalification reservation is scientifically and operationally justified.

R1 does not itself authorize POWDER contact or a replacement reservation.

## Stop boundary

Until R1 closes and a later separate explicit live authorization is granted:

- no POWDER reservation or SSH;
- no physical P7B retry;
- no automatic replacement reservation;
- no scored work;
- no immutable pre-score snapshot claiming readiness;
- no WP3 execution.

**STOP — P7B CLOSED BLOCKED; NEXT PATCH IS OFFLINE R1 ONLY.**
