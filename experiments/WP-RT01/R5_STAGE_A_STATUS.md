# WellPulse IEEE Revival — R5 Stage-A Harness Status

## Scope
This record freezes R5a only: build and QA of the scored Stage-A harness. No scored FIT run has been executed.

Branch:
`revival-r5-stage-a`

Pre-status branch checkpoint:
`2b2145ad62b8d04e7d8da54311f77f63a9bcddfb`

## R4 Amendment A2 — same-receiver causal witness
The frozen W1 implementation completes PUBACK coverage of the historical backlog H before generating sequence 5001.

Therefore, when source monotonic evidence verifies:

`M2 < generation(seq5001)`

and the receiver observes seq5001 before at least one member of H, the following causal chain holds:

`M2 < generation(seq5001) < receive(seq5001) < receive(late H) <= M3`

This proves receiver incompleteness after M2 without cross-host timestamp subtraction.

Rules:
- causal evidence may classify a run POSITIVE even when the M2→M3 duration is not clock-resolved;
- no duration claim is permitted from causal-only evidence;
- if no causal witness exists, the frozen pre/post clock-interval method remains the fallback;
- the 4.183 s Q0 bound remains an uncertainty bound, not a scientific effect threshold.

## Frozen Stage-A design
Treatment:
- W1
- C1 connectivity-only outage
- no process restart
- 10,000 generated records
- H = sequences 3001–5000, exactly 2,000 records
- live causal witness = sequence 5001

Stage A:
- exactly three planned scored T1 replicates: R1, R2, R3
- all valid scientific outcomes are retained
- INVALID is the only fail-fast condition
- no automatic replacement of an INVALID attempt
- no automatic Stage B

Decision:
- >=2/3 POSITIVE -> CONFIRM_REPEAT_OCCURRENCE_STOP
- 0/3 POSITIVE -> NOT_CONFIRMED_STOP
- exactly 1/3 POSITIVE -> STAGE_B_REQUIRED_TWO_ADDITIONAL_VALID_RUNS
- any INVALID -> STAGE_A_INCOMPLETE_INVALID_RUN; no C6 adjudication

Claim ceiling:
No prevalence, probability, reliability-rate, or population-frequency inference.

## Implementation
Per-run adjudicator:
`scripts/analyze_r5_stage_a_run.py`

Stage aggregate adjudicator:
`scripts/adjudicate_r5_stage_a.py`

Secret-free scored loop:
`scripts/run_fit_r5_stage_a_loop.sh`

Adversarial tests:
`tests/test_r5_stage_a.py`

The scored loop hard-locks the qualified implementation blobs:
- instrumented W1 wrapper: `9a0585ecacc9bdb87ec469d9ea1ad9ce998ccc9e`
- frozen W1 runner: `3683737f9756c8b96c4c2e41f4372fc388fadb7d`
- receiver stamp stream: `51a31081990c4d92e99462f7c6cd88736260036e`

The loop contains no FIT password handling. FIT reservation/auth/bootstrap is intentionally separated from scored execution.

## Censor integrity
Receiver start/stop timestamps are explicitly recorded. A run with missing H records cannot be called censored-positive unless receiver capture is proven to extend through the conservative M1+300 s receiver-clock censor boundary. Otherwise the run is INVALID for protocol incompleteness.

## Machine QA
Temporary QA-only PR:
`#35 R5 Stage-A static QA dispatcher`

GitHub Actions run:
`35596493707`

Result:
`SUCCESS`

Passed gates:
- Python compile
- unit tests
- Bash syntax
- exactly R1/R2/R3 boundedness
- no automatic R4/R5 Stage-B execution
- no FIT_PASSWORD in scored loop
- qualified-code blob immutability

PR #35 was closed unmerged after QA. No FIT credentials, reservation, or scored experiment were used by the QA workflow.

## Gate
`R5a_HARNESS_QA=PASS`
`R5_STAGE_A_EXECUTION=LOCKED_PENDING_EXPLICIT_EXECUTION_STEP`

Next:
R5b — prepare the one manual GitHub Actions bootstrap/dispatcher that stages the already-qualified FIT environment and invokes the frozen Stage-A loop. Do not execute until explicitly authorized.


## R5c scored launch attempt #1 — execution-plumbing failure before R1 science
GitHub Actions run: `35642069178`
FIT experiment: `449952`
Authorization gate: PASS
Bootstrap/staging: PASS
R1 pre-clock qualification: PASS, cross-host bound `4.152086496353149 s`

Failure point:
The scored loop failed while capturing the receiver start epoch. The remote shell mangled the nested quoting of:
`python3 -c 'import time; print("%.9f"%time.time())'`
into invalid Python:
`import time; print(%.9f%time.time())`

Scientific disposition:
- failure occurred before receiver subscription startup and before the R1 source runner;
- no scored R1, R2, or R3 outcome was produced;
- no Stage-A scientific verdict exists;
- this is classified as execution plumbing only, not a scientific or instrumentation result.

Evidence preserved:
- artifact id: `10657948536`
- artifact size: 273,512 bytes
- artifact digest: `sha256:22018c38076d373a1260d37a51353329be813f8dc9b5a86999a0beaa7dab7783`
- 67 files uploaded

Correction:
Receiver start/stop epoch capture now uses the quote-stable remote command:
`python3 -c 'import time; print(time.time())'`

Fix commit:
`4ca152fec27ffea5550e4cd8ea60cfca7b43693a`

Current gate:
`R5_STAGE_A_SCORED_RUNS_EXECUTED=0`
`R5c_RETRY=LOCKED_PENDING_PATCH_QA_AND_DISPATCHER_REPIN`


## R5c timestamp-plumbing patch QA — PASS
Temporary QA PR: `#38`
Final successful QA run: `35642747498`

Passed gates:
- Python compile;
- all 11 R5 Stage-A unit tests;
- Bash syntax;
- exactly R1/R2/R3 boundedness;
- no automatic R4/R5 Stage-B invocation;
- receiver timestamp quote-smoke: PASS;
- qualified instrumented/frozen/receiver blobs unchanged.

The failed QA predecessor `35642674319` was a temporary-QA grep quoting error after the actual timestamp smoke had already passed; it has no effect on the scored harness.

Gate transition:
`R5c_PATCH_QA=PASS`
`R5c_RETRY=LOCKED_PENDING_DISPATCHER_REPIN_AND_MERGE`


## R5 Stage-A scored execution — COMPLETE / NOT CONFIRMED STOP
GitHub Actions run: `35653569079`
Workflow conclusion: `success`
FIT experiment: `449953`
Node: Grenoble A8-102
Frozen authority executed: `c9fd8968f1408d9a2e3a57dd825df05c2f1d9147`

All three planned scored runs completed and were objectively valid:
- R1: `R5-SA-R1-EXP449953` — primary_class=`UNRESOLVED`; positive_for_stage_rule=false; H=2000/2000 receiver-complete; H PUBACK coverage=2000/2000; no causal witness; generation gap 5000→5001 = 75.208044774 s; D23 interval = [-5.037870646, +4.800559282] s.
- R2: `R5-SA-R2-EXP449953` — primary_class=`UNRESOLVED`; positive_for_stage_rule=false; H=2000/2000 receiver-complete; H PUBACK coverage=2000/2000; no causal witness; generation gap 5000→5001 = 76.307649507 s; D23 interval = [-4.857098222, +4.932285786] s.
- R3: `R5-SA-R3-EXP449953` — primary_class=`UNRESOLVED`; positive_for_stage_rule=false; H=2000/2000 receiver-complete; H PUBACK coverage=2000/2000; no causal witness; generation gap 5000→5001 = 74.797521961 s; D23 interval = [-4.858398557, +4.814558148] s.

Additional integrity observations common across scored runs:
- generated_unique=10000;
- receiver_unique=10000;
- unresolved_pubacks_all=0;
- payload_mismatch_count=0;
- stale_arrival_event_count=0;
- invalid_reasons=[];
- historical_records_after_causal_witness=0;
- receiver_causal_positive=false;
- clock_resolved_positive=false.

Stage-A machine adjudication:
- all_runs_valid=true;
- positive_run_count=0;
- primary_class_counts={UNRESOLVED:3};
- decision=`NOT_CONFIRMED_STOP`;
- stage_complete=true;
- next_action: STOP. The central repeated-occurrence claim is not confirmed under Stage A. Retain bounded individual phenomena without upgrading C6.

No Stage-B run was executed and none is authorized by the frozen decision rule for a 0/3 Stage-A outcome.

Evidence artifact:
- artifact id: `10666003184`;
- size: 6,881,643 bytes;
- retention: 90 days;
- digest: `sha256:5b52005e48d8987091c447186eb39261824f32df15653c3d2773a031b062d4a2`.

Scientific interpretation:
The prospective campaign did not resolve a positive M2→M3 separation under the qualified clock uncertainty and produced no same-receiver causal witness in any of the three valid runs. Therefore C6 cannot be upgraded to a repeated-occurrence central claim. The historical FIT finding remains an implementation-specific ≈75 s live-generation blackout associated with serialized backlog replay, while receiver-side historical completion relative to M2 remains unresolved within approximately ±5 s in this campaign.

Gate:
`R5_STAGE_A=COMPLETE`
`R5_DECISION=NOT_CONFIRMED_STOP`
`R5_STAGE_B=NOT_REQUIRED_AND_NOT_AUTHORIZED`
`NEXT=R6_INTEGRATED_SCIENTIFIC_ADJUDICATION`
