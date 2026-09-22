# WellPulse IEEE Revival — R7d Full Prose Reconstruction Freeze

**Date:** 2026-09-22
**Status:** PASS
**Scope:** Introduction + Related Work + Discussion + Threats + Reproducibility + Conclusion
**Methods + Results authority:** R7c, byte-locked

## 1. New R7d source

`manuscript/revival_2026-09-22/WellPulse_Revival_R7d_Full_Prose_20260922.tex`

R7c remains preserved unchanged.

## 2. Introduction repair

The Introduction now:
- begins from the overloaded meaning of telemetry recovery;
- distinguishes path, session, broker acknowledgement, receiver completion, live continuity, and stale carryover;
- states explicitly that the study proposes an experimental recovery-observable protocol, not a new MQTT persistence/failover architecture;
- assigns FIT and POWDER non-overlapping evidence roles;
- preserves four bounded RQs;
- preserves four R6-compliant contributions;
- adds an explicit paper-organization paragraph.

This closes the AE complaints that the motivation/background were unclear, the contribution was unclear, 'what is being proposed?' was unanswered, and the organization paragraph was missing.

## 3. Related Work boundary

Current prior-art checks were explicitly incorporated:
- MQTT v5 broker/QoS semantics;
- E-MQTT subscriber-level end-to-end confirmation;
- Jesus et al. 2025 MQTT robustness/fault injection;
- Gaspar et al. 2026 MQTT reliability stress testing;
- Neagu et al. 2026 network/application/data-layer HA recovery;
- Kang et al. 2026 current-state freshness versus historical reconstruction scheduling.

Resulting concessions:
- subscriber confirmation is prior art;
- MQTT fault injection is prior art;
- reliability stress testing is prior art;
- layered recovery separation is prior art;
- current-versus-historical scheduling trade-offs are prior art;
- architecture firstness is not claimed.

Retained gap:
experimental recovery measurement as M0–M5 with explicit evidence authority, implementation-specific W1 completeness–continuity evidence, bounded POWDER evidence, and an explicit negative/unresolved M2→M3 outcome.

Verified DOI anchors encoded:
- 10.3390/app132212419;
- 10.1016/j.iot.2025.101590;
- 10.1109/MIOT.2026.3681190;
- 10.3390/fi18030137;
- 10.1109/TON.2026.3673496.

## 4. Discussion reconstruction

Discussion now centers on:
- completeness versus current-data continuity;
- implementation-specific serialized replay behavior;
- the scientific meaning of the 0/3 prospective result;
- explicit refusal to infer M2=M3;
- endpoint/domain/timing semantics for POWDER;
- one Recovery Declaration Matrix mapping observations to permitted incident interpretations;
- service-monitoring implications without requiring a new MQTT wire protocol.

## 5. Threats to Validity

Threats now explicitly include:
- historical endpoint instrumentation error;
- absent exact historical M3 latency;
- prospective cross-host clock uncertainty;
- no causal witness in R1–R3;
- 0/3 positive does not prove endpoint equality;
- W1 implementation/workload specificity;
- B0 non-durable comparator asymmetry;
- three run-level replicates;
- message IDs are reconciliation records, not pseudo-replicates;
- no historical/prospective pooling;
- no FIT/POWDER pooling;
- POWDER profile specificity;
- single stale-carryover observation;
- exact/censored/upper-bound timing distinction;
- no field/production/agronomic reliability claim.

## 6. Reproducibility and Data Availability

The manuscript now records the preserved R5 raw archive identity:
`5b52005e48d8987091c447186eb39261824f32df15653c3d2773a031b062d4a2`

Archive size:
`6,881,643 bytes`

Archive entries:
`127`

It states that three durable copies were re-downloaded and hash-verified, while private Drive IDs and credentials are not exposed in the manuscript. Final public repository/DOI pointer is deferred rather than invented.

## 7. Conclusion reconstruction

The Conclusion now states only:
- telemetry recovery comprises distinct observables;
- serialized W1 replay preserved eventual completeness while suspending new generation for roughly 69 s historically and 75–76 s prospectively;
- those campaigns remain separate;
- M2→M3 positive separation was not confirmed and remains unresolved;
- POWDER contributes bounded cross-layer/failure-domain/stale-carryover evidence;
- contribution is an evidence discipline, not a new persistence architecture or global reliability claim.

## 8. AE defect closure

- weak Introduction/background: CLOSED;
- unclear contribution: CLOSED;
- unclear proposal: CLOSED;
- weak SOTA gap: CLOSED by explicit prior-art concession + retained bounded gap;
- unconvincing result framing: CLOSED by data-first W1 result + explicit negative prospective result;
- poor structure/readability: substantially CLOSED at scientific-prose level;
- missing organization paragraph: CLOSED;
- single-author 'we': CLOSED;
- awkward TNSM self-reference: absent;
- citation/reference IEEE formatting: provisionally improved; final editorial audit remains R7e.

## 9. Machine QA

Temporary QA PR: `#43`.

Initial run `35699521505` failed only because the temporary QA expected the singular phrase 'does not support' while the manuscript correctly used 'the data do not support'. The manuscript source was unchanged.

Final QA run:
`35699577111` — SUCCESS.

Passed:
- exact R7d authority checkout;
- R7c Methods + Results byte identity;
- AE closure markers;
- exactly four RQs;
- exactly four contributions;
- single-author voice: no prose 'we' or 'our';
- prohibited-claim scan;
- explicit negative M2/M3 language;
- explicit generic-durability negation;
- six related-work citation anchors;
- five verified DOI anchors;
- private Drive IDs absent;
- required section architecture;
- IEEEtran latexmk compile;
- no undefined control sequence;
- no LaTeX error.

Temporary PR #43 closed unmerged.

## 10. Gate

`R7d_FULL_PROSE_RECONSTRUCTION=PASS`

`R7d_METHODS_RESULTS_LOCK=PASS`

`R7D_MACHINE_QA=PASS`

`R7e_ENTRY=UNLOCKED`

Next:
R7e performs IEEE editorial/compliance engineering only: author metadata, single-author style sweep, citation/reference formatting, terminology consistency, page/float/caption hygiene, and source-package cleanliness. Scientific claims remain locked.