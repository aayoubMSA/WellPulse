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
