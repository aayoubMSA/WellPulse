# WellPulse IEEE Revival — R7f-R2 Contribution + Evidence-Framing Repair Freeze

**Date:** 2026-09-22
**Status:** PASS
**Parent authority:** R7f-R1 + R7f hostile review
**Scope:** abstract + Introduction framing + A2 + Related Work retained-gap sentence + Discussion/Conclusion framing only

## 1. New source identity

`manuscript/revival_2026-09-22/WellPulse_Revival_R7fR2_EvidenceFraming_20260922.tex`

R7f-R1 remains preserved unchanged.

## 2. A2 repair

A2 is now:
**Measured W1 replay consequence.**

The manuscript now states explicitly that the experiment quantifies:
- the magnitude of the continuity cost;
- the repeatability of the continuity cost;
- a consequence implied by the tested serialized W1 replay order;
- not a generic MQTT phenomenon;
- not an architecture ranking;
- not a receiver-completion latency.

This directly closes the hostile-review attack that the repeated W1 blackout could be read as a general systems discovery even though the code path serially drains backlog before generating sequence 5001.

## 3. Abstract repair

The abstract no longer ends with the vague sentence that the results 'support recovery-observable measurement.'

It now states directly that:
- the measurements quantify the magnitude and repeatability of the serialized-replay continuity cost;
- the measurement discipline prevents sender-side acknowledgement closure from being mislabeled as receiver completion;
- replay-associated continuity evidence remains separate from the unresolved M2→M3 question.

All frozen abstract values remain unchanged:
- historical 68.785–70.264 s; mean 69.217 s;
- prospective 74.798–76.308 s; mean 75.438 s;
- 0/3 positive M2→M3;
- unresolved prospective endpoint result.

## 4. Discussion repair

The Discussion now makes the causal boundary explicit:
- W1 serially drains historical backlog before seq5001 generation;
- the experiment measures the resulting continuity cost;
- that behavior is structurally consistent with the code path;
- the evidence does not support generic MQTT durability/freshness causality.

Future-work boundary added:
- alternative replay scheduler comparison;
- backlog-size scaling;
- replay-concurrency ablation;
- broker-throughput sensitivity.

These are explicitly reserved for future work rather than presented as missing evidence for the bounded W1 claim.

## 5. Conclusion repair

The Conclusion now says that the experiments quantify the magnitude and repeatability of a continuity cost implied by the tested serialized code path.

It does not generalize that cost to MQTT as a protocol.

## 6. Scope/science lock

Machine QA verified:
- Methods + Results are byte-identical to R7f-R1;
- declarations and full 14-reference bibliography are byte-identical to R7f-R1;
- all frozen historical/prospective numeric anchors remain present;
- R7f-R1 A1/A3/A4 boundary repairs remain intact;
- no prohibited receiver-completion or novelty claim was reintroduced.

## 7. Machine QA

Temporary QA PR: `#46`.

GitHub Actions run:
`35706141251` — SUCCESS.

Passed:
- exact R7f-R2 authority checkout;
- Methods/Results byte lock;
- declarations/bibliography lock;
- measured-W1 framing;
- abstract evidence framing;
- future-work boundary;
- all frozen numeric anchors;
- R7f-R1 claim-boundary preservation;
- claim firewall;
- IEEEtran compile;
- undefined citations = 0;
- undefined references = 0;
- LaTeX errors = 0;
- overfull boxes = 0.

Temporary PR #46 closed unmerged.

## 8. Gate

`R7f_R2_CONTRIBUTION_FRAMING=PASS`

`R7f_R2_EVIDENCE_FRAMING=PASS`

`R7f_R2_METHODS_RESULTS_LOCK=PASS`

`NEXT=R7f-R3_REPRODUCIBILITY_SURFACE_REPAIR`

`R7g_ENTRY=LOCKED`

R7g remains locked until R7f-R3 and R7f-R4 pass.