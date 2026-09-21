# WellPulse IEEE Revival — R7b Revival Source Skeleton Freeze

**Date:** 2026-09-22
**Status:** PASS CANDIDATE / SOURCE-SKELETON ONLY
**Governing authority:** R6 + R7a
**Full manuscript prose rewrite:** NOT YET PERFORMED

## 1. New source identity

R7b creates a new manuscript source identity:

`manuscript/revival_2026-09-22/WellPulse_Revival_R7b_Skeleton_20260922.tex`

This is not the rejected TNSM controlled release and does not reuse its identity or hashes.

The recovered Sep-07 LaTeX source is used only as structural/provenance input. Any conflict with R6 is resolved in favor of R6.

## 2. Title candidates

### T1 — PROVISIONAL LEAD
**Beyond Reconnection: Measuring Recovery Observables and Replay-Induced Continuity Gaps in MQTT Telemetry**

Strengths:
- retains continuity with the submitted paper;
- does not claim receiver-completion lag;
- foregrounds the surviving M0–M5 measurement object and repeated W1 M4 result.

### T2
**Measuring Recovery in MQTT Telemetry: Distinct Observables and a Reproducible Completeness–Continuity Trade-off**

Constraint:
“reproducible” refers only to repeated behavior in the tested W1 implementation, not general deployment prevalence.

### T3
**Recovery Is More Than Reconnection: Experimental Observables and Serialized-Replay Continuity Gaps in MQTT Telemetry**

### T4
**Experimental Recovery Observables for MQTT Telemetry: Completeness, Continuity, and Bounded Receiver Evidence**

R7b selects T1 provisionally. Final title remains open until R7f hostile review.

## 3. Abstract candidate — frozen for R7c/R7d refinement

Word count: **167 words**.

> Telemetry recovery is often summarized by a single reconnect or catch-up time, although network restoration, MQTT session restoration, broker-side QoS-1 acknowledgement closure, receiver-side historical completion, live-data continuity, and stale-record carryover are different observables. This study defines an experimental measurement protocol that separates these states and applies it to MQTT telemetry on FIT IoT-LAB and POWDER. In the tested W1 implementation, serialized backlog replay preserved eventual 10,000/10,000 receiver completeness but repeatedly suspended new record generation. Six historical FIT runs showed sequence-5000-to-5001 gaps of 68.785–70.264 s (mean 69.217 s); three prospective scored runs showed 74.798–76.308 s (mean 75.438 s). The prospective runs directly instrumented sender PUBACK closure and receiver completion, but 0/3 produced either a causal witness or a clock-resolved positive M2-to-M3 separation, so that interval remains unresolved. A POWDER trace independently exhibited stale carryover: newer records arrived before an older record after restoration. The results support recovery-observable measurement and identify an implementation-specific completeness–continuity trade-off without claiming a new persistence architecture, a universal MQTT effect, or pooled cross-testbed inference.

## 4. Frozen research questions

**RQ1.** Which experimentally observable endpoints are required to distinguish network-path restoration, MQTT-session restoration, broker-side QoS-1 acknowledgement closure, receiver-side historical completion, live-data continuity, and receiver-side stale carryover?

**RQ2.** Under the tested serialized W1 backlog-replay implementation, what live-generation discontinuity is observed in the historical and prospective FIT IoT-LAB campaigns?

**RQ3.** When M2 and M3 are directly instrumented prospectively, does the qualified evidence resolve a positive M2-to-M3 separation under the frozen causal-witness and clock-uncertainty rules?

**RQ4.** What complementary, bounded evidence does POWDER provide about failure-domain-specific recovery and receiver-side stale carryover without pooling the two testbeds?

## 5. Frozen contribution blocks

**A1 — Recovery-observable measurement protocol.**
Separate M0–M5 so reconnect, session restoration, PUBACK closure, receiver completion, live-data continuity, and ordering are not treated as interchangeable evidence.

**A2 — Repeated W1 completeness–continuity result.**
Historical and prospective FIT campaigns separately show repeated tens-of-seconds suspension of new record generation under serialized backlog replay while eventual receiver completeness is preserved.

**A3 — Cross-environment triangulation without pooling.**
FIT contributes implementation-specific replay evidence; POWDER contributes bounded physical failure-domain/stale-carryover evidence.

**A4 — Explicit negative/bounded result.**
The prospective Stage-A campaign produced 0/3 positive M2-to-M3 results and 3/3 UNRESOLVED outcomes. This result is retained explicitly.

## 6. New manuscript architecture

1. Introduction
2. Related Work and Claim Boundary
3. Recovery Observables and Experimental Protocol
   - M0–M5 taxonomy
   - historical FIT
   - prospective FIT Stage A
   - POWDER
   - non-pooling rule
4. Results
   - historical FIT completeness + replay-associated generation gap
   - prospective Stage-A M2/M3 adjudication
   - POWDER bounded evidence
   - synthesis
5. Discussion
6. Threats to Validity
7. Reproducibility and Data Availability
8. Conclusion

## 7. Evidence anchors encoded directly in the skeleton

### M0–M5 observable table
Included in source.

### Prospective Stage-A result table
Included in source:
- R1 gap = 75.208 s; D23 = [-5.038, +4.801] s; UNRESOLVED.
- R2 gap = 76.308 s; D23 = [-4.857, +4.932] s; UNRESOLVED.
- R3 gap = 74.798 s; D23 = [-4.858, +4.815] s; UNRESOLVED.
- all H PUBACK = 2000/2000;
- all H receiver = 2000/2000;
- no causal witness.

These values are frozen evidence anchors for R7c; they are not inferential statistics.

## 8. Claim firewall encoded in source comments

Prohibited:
- 68 s end-to-end recovery;
- 68 s receiver completion;
- repeated empirical M2>M3 claim;
- repeated service-recovery misclassification;
- architecture novelty;
- generic “durability harms freshness”;
- “first” / “to our knowledge” architecture claims;
- historical+prospective pooling;
- FIT+POWDER pooling;
- POWDER stale-carryover prevalence.

## 9. R7b acceptance criteria

- new source identity: PASS;
- rejected release untouched: PASS;
- provisional title compatible with R6: PASS;
- abstract contains no killed C6 claim: PASS;
- 0/3 prospective result explicit: PASS;
- M0–M5 encoded: PASS;
- R1/R2/R3 table encoded: PASS;
- four RQs bounded to evidence: PASS;
- four contribution blocks match R6: PASS;
- full prose rewrite deferred: PASS;
- venue decision deferred to R8: PASS.

## 10. Gate

`R7b_REVIVAL_SOURCE_SKELETON=PASS`

`R7b_FULL_PROSE_REWRITE=NOT_STARTED`

`R7c_ENTRY=UNLOCKED`

Next:
R7c reconstructs Methods + Results only, using this source identity and the preserved evidence. It must not yet perform the Introduction/Related Work/Discussion/Conclusion prose sweep.