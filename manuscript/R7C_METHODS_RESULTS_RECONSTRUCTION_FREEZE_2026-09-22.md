# WellPulse IEEE Revival — R7c Methods + Results Reconstruction Freeze

**Date:** 2026-09-22
**Status:** PASS
**Governing authority:** R6 + R7a + R7b
**Scope:** Methods/Protocol + Results only

## 1. New R7c source identity

`manuscript/revival_2026-09-22/WellPulse_Revival_R7c_Methods_Results_20260922.tex`

R7b remains preserved unchanged. R7c is a new source file.

## 2. Scope lock

Machine comparison against R7b verified:
- Introduction and Related Work prefix: byte-identical;
- Discussion, Threats to Validity, Reproducibility, Conclusion, and bibliography suffix: byte-identical.

Therefore R7c modified only:
- Recovery Observables and Experimental Protocol;
- Results.

## 3. Methods reconstruction

### M0–M5 taxonomy
Full manuscript prose now distinguishes:
- M0 network-path restoration;
- M1 MQTT-session restoration;
- M2 sender-to-broker QoS-1 PUBACK closure;
- M3 receiver-side historical-state completion;
- M4 live-data continuity / replay-associated generation gap;
- M5 receiver ordering / stale carryover.

PUBACK closure is explicitly stated not to establish subscriber receipt.

### Historical FIT
Methods now state:
- B0 = intentionally non-durable publish-only control;
- W1 = application-side persistent queue with serialized replay;
- C0 healthy;
- C1 broker-path interruption without process restart;
- C2 interruption plus one gateway-process restart;
- 10,000 uniquely identified records per run;
- run, not message, is the scientific unit.

Historical W1 reconnect values retained as publisher/session observations:
- C1: 1.309382, 1.331298, 1.310584 s;
- C2: 1.377100, 1.329536, 1.327973 s.

Critical correction:
the historical field formerly called backlog drain is explicitly described as sender-side QoS-1 acknowledgement closure/program progress, not M3 receiver completion.

Historical M4 anchors:
- 68.992, 69.466, 68.944, 68.785, 70.264, 68.852 s;
- mean 69.217 s;
- range 68.785–70.264 s;
- exact historical M3 latency was not instrumented.

### Prospective FIT Stage A
Methods now encode:
- W1/C1;
- 10,000 records;
- H = seq 3001–5000 = 2,000 records;
- direct M2 PUBACK coverage;
- direct M3 receiver reconciliation;
- same-receiver seq5001 causal witness rule;
- conservative pre/post cross-host clock interval;
- UNRESOLVED when the conservative interval crosses zero;
- frozen 3-run decision rule;
- no silent replacement of invalid runs.

### POWDER
Methods now preserve:
- E1R4 ascending 48–52 dB;
- E2 descending transition;
- E3 repeated 49–52 dB cycles;
- no universal attenuation threshold;
- E10 exact/censored/upper-bound semantics;
- E8 broker interruption/path-isolation role;
- E3 cycle-3 M5 stale-carryover existence observation.

### Non-pooling
Historical FIT, prospective FIT, and POWDER are explicitly separate evidence classes. No pooled effect estimate, reliability percentage, confidence interval, or pooled hypothesis test is constructed.

## 4. Results reconstruction

### Historical FIT completeness
- C0 B0 = 10,000/10,000 in all three runs;
- C0 W1 = 10,000/10,000 in all three runs;
- C1/C2 B0 = 8,000/10,000 in every run;
- C1/C2 W1 = 10,000/10,000 in every run.

B0 is explicitly bounded as a non-durable mechanism-isolation control, not a strongest-durable-MQTT comparator.

### Historical W1 continuity result
Six replay-associated seq5000→5001 gaps are reported separately with mean 69.217 s and range 68.785–70.264 s.

Allowed interpretation:
implementation-specific completeness–continuity trade-off.

Explicitly prohibited interpretation:
receiver completion latency or generic durability-harms-freshness conclusion.

### Prospective scored FIT
R1:
- generation gap 75.208 s;
- H PUBACK 2000/2000;
- H receiver 2000/2000;
- no causal witness;
- D23 interval [-5.038,+4.801] s;
- UNRESOLVED.

R2:
- generation gap 76.308 s;
- H PUBACK 2000/2000;
- H receiver 2000/2000;
- no causal witness;
- D23 interval [-4.857,+4.932] s;
- UNRESOLVED.

R3:
- generation gap 74.798 s;
- H PUBACK 2000/2000;
- H receiver 2000/2000;
- no causal witness;
- D23 interval [-4.858,+4.815] s;
- UNRESOLVED.

Prospective M4 mean = 75.438 s; range = 74.798–76.308 s.

Stage result:
- 3/3 valid;
- 0/3 positive;
- 3/3 UNRESOLVED;
- NOT_CONFIRMED_STOP;
- Stage B not authorized.

The active prose explicitly states that 0/3 does not establish M2=M3 and does not support a repeated material M2-before-M3 claim.

### POWDER results
Encoded bounded observations include:
- E1R4 51 dB: ICMP loss 30%, MQTT 20/20;
- E1R4 52 dB: ICMP loss 60%, MQTT 13/20;
- E2 52 dB: ICMP loss 65%, MQTT 11/20;
- E2 51 dB: ICMP loss 10%, MQTT 20/20;
- E3 52 dB cycles: MQTT 60% / 25% / 55%; ICMP loss 80% / 65% / 70%;
- E10-A censored;
- E10-B exact 6.063318 s first MQTT publish and 6.609430 s first ping; publish→CORE 0.060172 s;
- E10-C-B exact 29.247733 s first ping and 29.248129 s first publish;
- E10-D upper bound ≤10.908749 s;
- E8 healthy tested LTE ping path during MQTT broker interruption;
- E3 cycle-3 seq251–255 before older seq231 as one bounded stale-carryover event.

No threshold, prevalence, or pooled-recovery claim is made.

## 5. Cross-evidence synthesis

R7c now states:
- historical FIT = repeated W1 replay-associated M4 blackout + eventual completeness;
- prospective FIT = repeated M4 blackout + direct but unresolved M2/M3 test;
- POWDER = bounded cross-layer/failure-domain/M5 evidence;
- synthesis = measurement discipline, not a pooled statistical effect.

## 6. Machine QA

Temporary QA PR: `#42`.

QA attempts 35662724025 and 35662810787 failed only because the temporary scanner treated an explicitly negated sentence ('does not support ... M2 materially precedes M3') as a prohibited positive claim. The manuscript source was not changed.

Final QA run:
`35662897612` — SUCCESS.

Passed:
- exact R7c authority checkout;
- R7b locked-prefix byte identity;
- R7b locked-suffix byte identity;
- historical/prospective FIT non-pooling gate;
- all historical FIT numeric anchors;
- all prospective R1/R2/R3 numeric anchors;
- M0–M5 table integrity;
- explicit 0/3 negative result;
- POWDER transition and recovery timing anchors;
- stale-carryover bounded wording;
- prohibited positive-claim scan;
- exact IEEEtran LaTeX compile;
- no undefined control sequence;
- no LaTeX error.

Temporary PR #42 closed unmerged.

## 7. Gate

`R7c_METHODS_RESULTS_RECONSTRUCTION=PASS`

`R7c_SCOPE_LOCK=PASS`

`R7C_MACHINE_QA=PASS`

`R7d_ENTRY=UNLOCKED`

Next:
R7d reconstructs Introduction + Related Work + Discussion + Threats + Reproducibility + Conclusion around the frozen R6/R7c evidence. Methods and Results become locked except for later editorial-only fixes.