# WellPulse IEEE Revival — R7f-R1 SOTA + Claim-Boundary Repair Freeze

**Date:** 2026-09-22
**Status:** PASS
**Parent authority:** R7e + R7f hostile review
**Scope:** Introduction contribution wording + Related Work + bibliography only

## 1. New source identity

`manuscript/revival_2026-09-22/WellPulse_Revival_R7fR1_SOTA_ClaimBoundary_20260922.tex`

R7e remains preserved unchanged.

## 2. Contribution-boundary repair

A1 changed from a potentially novelty-sounding taxonomy/protocol claim to:
**Operational recovery-measurement discipline.**

The manuscript now states explicitly:
- M0–M5 labels are not claimed as novel by themselves;
- the contribution is assigning evidence authority and a claim ceiling to each endpoint;
- concrete validation comes from reclassifying the historical sender-side backlog endpoint and prospectively adjudicating M2/M3.

A3 changed from:
`Cross-environment triangulation without pooling`

to:
`Complementary cross-environment evidence without pooling`.

The text now states that FIT and POWDER answer different measurement questions and are not replications of one common effect.

A4 changed from:
`Explicit negative/bounded result`

to:
`Prospective endpoint adjudication`.

The 0/3 result is framed as constraining the claim ceiling rather than as a standalone positive systems contribution.

## 3. SOTA expansion

Six focused peer-reviewed references were added and independently verified as matched and unretracted:

1. Mohammed et al. 2026 — resilient MQTT monitoring architecture
   DOI: 10.22266/ijies2026.0531.19
   Relevance: disk-backed persistence + application/database-level acknowledgement beyond broker QoS.

2. Mohammed et al. 2026 — scalable edge MQTT architecture
   DOI: 10.48084/etasr.16945
   Relevance: edge persistence + application/database-level confirmation; directly narrows end-to-end ACK novelty.

3. Chen et al. 2020 — broker-crash rerouting/topic-session continuity
   DOI: 10.1155/2020/8884924
   Relevance: broker substitution/failover is explicit prior art.

4. Sochor et al. 2021 — automated MQTT broker compatibility evaluation
   DOI: 10.1002/smr.2410
   Relevance: empirical implementation/version heterogeneity; blocks generic extrapolation across brokers.

5. Nawaz et al. 2019 — formal MQTT QoS semantics
   DOI: 10.1002/ett.3742
   Relevance: reinforces that QoS acknowledgement semantics must be interpreted at the protocol interaction being acknowledged.

6. Kamoun et al. 2024 — distributed-broker MQTT architecture
   DOI: 10.1002/ett.4945
   Relevance: distributed broker availability/performance is prior art.

These additions increase the focused bibliography from 8 to 14 references.

## 4. Explicit concessions added

The manuscript now explicitly concedes that the following are prior art:
- application-level acknowledgement;
- disk-backed persistence;
- end-to-end durability confirmation;
- broker failover/substitution;
- distributed-broker availability;
- broker implementation/version heterogeneity;
- live-versus-history scheduling trade-offs;
- layered recovery separation.

The retained gap is now stated as:
an operational measurement discipline with explicit evidence authority and claim ceilings, demonstrated through the historical endpoint correction, prospective unresolved M2/M3 adjudication, implementation-specific W1 continuity evidence, and complementary non-pooled POWDER evidence.

## 5. Science lock

Machine QA verified:
- title byte-identical to R7e;
- abstract byte-identical to R7e;
- Recovery Observables/Methods through declarations byte-identical to R7e;
- no Methods/Results/Discussion/Threats/Reproducibility/Conclusion data or scientific wording changed.

## 6. Reference integrity

All six newly added DOI-bearing references were citation-audited:
- matched: 6/6;
- mismatched: 0;
- ambiguous: 0;
- not found: 0;
- retracted: 0.

Full source citation integrity:
- 14 unique bibliography keys;
- every citation key resolves;
- no duplicate bibliography key;
- no undefined citation/reference at compile.

## 7. Machine QA

Temporary QA PR: `#45`.

GitHub Actions run:
`35704999197` — SUCCESS.

Passed:
- exact R7f-R1 authority checkout;
- title/abstract lock;
- Methods-through-declarations science lock;
- six new SOTA references;
- two direct 2026 application-ACK/durability papers;
- A1/A3/A4 boundary repair;
- explicit prior-art concessions;
- 14-reference citation integrity;
- claim firewall;
- IEEEtran compile;
- undefined citations = 0;
- undefined references = 0;
- LaTeX errors = 0;
- overfull boxes = 0.

Temporary PR #45 closed unmerged.

## 8. Gate

`R7f_R1_SOTA_REPAIR=PASS`

`R7f_R1_CLAIM_BOUNDARY_REPAIR=PASS`

`R7f_R1_SCIENCE_LOCK=PASS`

`NEXT=R7f-R2_CONTRIBUTION_AND_EVIDENCE_FRAMING_REPAIR`

`R7g_ENTRY=LOCKED`

R7g remains locked until the remaining hostile-review repairs R7f-R2 through R7f-R4 pass.