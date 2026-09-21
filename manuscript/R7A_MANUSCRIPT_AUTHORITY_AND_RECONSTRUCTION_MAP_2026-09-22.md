# WellPulse IEEE Revival — R7a Manuscript Authority Recovery and Reconstruction Map

**Date:** 2026-09-22  
**Branch:** `revival-r6-adjudication`  
**Scope:** authority recovery + section-level reconstruction map only  
**Manuscript editing:** NOT PERFORMED in R7a

## 1. Governing scientific authority

The manuscript may be reconstructed only from the following authority stack, in this order:

1. **R6 integrated scientific adjudication**  
   `experiments/WP-RT01/R6_INTEGRATED_SCIENTIFIC_ADJUDICATION.md`  
   Commit: `23c649c97eb870697b76f400a045a86896c2a33f`

2. **R5 scored Stage-A evidence and preservation record**  
   `experiments/WP-RT01/R5_STAGE_A_STATUS.md`  
   `experiments/WP-RT01/R5_RAW_EVIDENCE_PRESERVATION.md`  
   Scored artifact SHA-256:  
   `5b52005e48d8987091c447186eb39261824f32df15653c3d2773a031b062d4a2`

3. **Q0 instrumentation qualification**  
   `experiments/WP-RT01/Q0_REVIVAL_STATUS.md`

4. **Historical FIT and POWDER evidence already accepted by R6**  
   These remain provenance-bounded evidence and may not override R6 claim ceilings.

Any older manuscript, handover, positioning memo, or supplement is subordinate when it conflicts with R6.

## 2. Exact rejected TNSM decision authority

### Submission identity

- Journal: IEEE Transactions on Network and Service Management
- Manuscript ID: `TNSM-2026-12181`
- Submitted title:
  **Beyond Reconnection: Receiver-Verified Service Recovery in MQTT Telemetry Across Failure Domains**
- Decision date: 20 Sep 2026
- Decision: denied publication
- Associate Editor: Dr. Dimitrios Michael Manias
- Editor-in-Chief: Dr. Abdallah Shami

### Associate Editor defects that R7 must close

The decision letter states, in substance:

1. technical and presentation standards not met;
2. no novelty;
3. manuscript not mature enough;
4. contributions unclear;
5. structure harms readability;
6. Introduction fails to establish background/motivation and is difficult to follow;
7. one related-work sentence names TNSM awkwardly;
8. Related Work fails to establish state of the art or a research gap;
9. novelty unclear — “What is being proposed?”;
10. results unconvincing and do not support a novel contribution;
11. paper-organization paragraph missing;
12. singular-author manuscript uses “we”;
13. in-text citations do not follow IEEE convention;
14. references are not IEEE-formatted.

R7 reconstruction must visibly close each item; no item may be treated as merely cosmetic.

## 3. Rejected-release identity and byte authority

The final pre-portal TNSM doctrine record preserves the controlled-release identities:

- final controlled manuscript source SHA-256:  
  `80abe30f23a2ba5018ea370f250d642ef94fb9289a4872689536901401a1c5f3`
- final controlled manuscript PDF SHA-256:  
  `f9a9cbb8b93197045c2b03dc1a9cb829eeb02dcf4bcdfd38ef1cb3ec0d0ef918`
- cover-letter PDF SHA-256:  
  `f868eec7625affcff9fe66f65e711b39ba37b4ce1f26586c81a4752994ec8f42`
- reviewer supplement SHA-256:  
  `3b6ede7ba4b73dd19767eff531eab05058e9220c95c873fb540cfad28677d5d9`
- final controlled submission package SHA-256:  
  `7945ccbd58b85aa128bf8163436f0a289d53a80fc8b743e5cc7e0cdae3e32802`

The exact final TNSM source/PDF bytes are **not currently recovered as files in Drive or the active repository tree**. Their hashes and construction/QA records are preserved.

Therefore R7 must not pretend to perform an in-place edit of exact rejected bytes. It must construct a **new revival source** under a new identity.

## 4. Recoverable submitted-source scaffold

The immediately preceding Internet of Things submission is available byte-for-byte and provides the full manuscript scaffold from which the TNSM conversion was made.

### Drive authority

Folder:
`WellPulse_IOT_SUB01_20260907`

Submission package:
`WellPulse_IOT_SUB01_Submission_Package_20260907.zip`

SHA-256:
`a4980193897dd75c0df05f511e2d0cb0c00dd1ba5fc68bbda725ec0dabc85ced`

LaTeX source ZIP:
`02_WellPulse_IOT_SUB01_LaTeX_Source_20260907.zip`

SHA-256:
`ca55eee9b3e47879e89f351d4648234c75af745f08778ec4011246ffa5465a2f`

Compiled manuscript:
`01_WellPulse_IOT_SUB01_Manuscript_20260907.pdf`

SHA-256:
`87b1044ad2af7c07a1463eb4c85eb9109cdab09fe1ed67fcf3feb15c0594b368`

The source contains:
- `WellPulse_Manuscript.tex`
- four scientific figure PDFs.

This scaffold is textual/layout provenance only. Its old scientific interpretation is not authoritative where R6 supersedes it.

## 5. R7 reconstruction doctrine

The rejected paper was centered on **receiver-verified service-recovery closure** and a claimed post-reconnect incomplete-state interval. R6 no longer permits that as the central empirical contribution.

The revival paper must instead be reconstructed around the following frozen object:

> Telemetry recovery should be measured as distinct observables rather than collapsed into a single recovery time. In the tested W1 implementation, serialized backlog replay preserved eventual delivery but repeatedly suspended new record generation for tens of seconds. A separate POWDER trace showed that stale receiver-side carryover can survive restoration. The prospective campaign did not establish a repeated positive separation between broker-side PUBACK closure and receiver-side historical completion.

### Frozen surviving contributions

**A1 — Recovery-observable measurement protocol**  
Separate M0–M5 so reconnect, session restoration, broker-side PUBACK closure, receiver completeness, live-generation continuity, and stale carryover/order are not conflated.

**A2 — Repeated W1 completeness–continuity result**  
Serialized historical replay repeatedly produced a large live-generation discontinuity while eventual receiver completeness was preserved.

**A3 — Cross-environment triangulation without pooling**  
FIT supplies implementation-specific replay behavior; POWDER supplies bounded physical stale-carryover/failure-domain evidence.

**A4 — Explicit negative/bounded result**  
The prospective Stage-A campaign did not confirm repeated positive M2→M3 separation; this negative result is reported, not hidden.

## 6. Section-level surgical reconstruction map

### 6.1 Title

**Current rejected title:**  
“Beyond Reconnection: Receiver-Verified Service Recovery in MQTT Telemetry Across Failure Domains”

**Disposition:** REPLACE.

Reason:
- “Receiver-Verified Service Recovery” over-centers C6, which R6 demoted to NOT CONFIRMED.
- the title should reflect measurement semantics and/or completeness–continuity behavior without implying demonstrated receiver-side lag after M2.

R7b must generate title candidates only after the body claim architecture is fixed.

### 6.2 Abstract

**Disposition:** FULL REWRITE.

Delete/supersede:
- “complete queue drainage required about 68 s” when presented as receiver completion;
- any claim that this exposes a prolonged receiver-incomplete state after reconnect;
- any wording that implies C6 repeated material misclassification was demonstrated.

Retain/restate:
- FIT B0/W1 completeness only as bounded context, not novelty;
- repeated W1 live-generation blackout;
- prospective R5 values: 75.208, 76.308, 74.798 s;
- 0/3 positive, 3/3 UNRESOLVED for M2→M3;
- POWDER as bounded complementary evidence;
- explicit measurement-study contribution.

### 6.3 Introduction

**Disposition:** REBUILD.

Required opening problem:
- “recovery” is overloaded across multiple observables;
- a single recovery time hides different system states.

Remove as central gap:
- evidence required to “close” a recovery incident based on repeated M2→M3 divergence;
- any novelty claim based simply on separating network/service/data layers.

Required RQ structure:
1. What distinct recovery observables should be measured?
2. What implementation-specific completeness–continuity behavior appears under serialized W1 backlog replay?
3. What can and cannot be concluded about M2→M3 from prospective instrumentation?
4. What bounded physical observations does POWDER add?

Required contribution paragraph:
A1–A4 exactly; architecture novelty prohibited.

Required final paragraph:
explicit paper organization, closing the AE defect.

### 6.4 Related Work

**Disposition:** MAJOR REWRITE / NARROW.

The old TNSM positioning on “receiver-verified recovery closure” is no longer the protected novelty wedge.

Required four blocks:
1. MQTT persistence / session / store-and-forward mechanisms — concede prior art.
2. MQTT robustness, broker performance, fault injection, and stress testing — concede prior art.
3. layered recovery / network-service-data continuity — concede prior art.
4. retained measurement gap — operationally separating observable endpoints while quantifying an implementation-specific completeness–continuity trade-off and reporting an explicit negative receiver-completion result.

Must include the direct prior-art threats already identified:
- disruption-tolerant / offline-first synchronization;
- subscriber confirmation;
- layered continuity / recovery;
- broker robustness and performance.

Must not end with “the first” or “novel framework.”

The AE-flagged sentence naming TNSM as a venue must be removed.

### 6.5 Evaluation Framework / Methods

**Disposition:** STRUCTURAL REWRITE.

Preserve:
- identity-based receiver reconciliation;
- failure-domain semantics;
- exact/censored/upper-bound timing classes;
- FIT and POWDER non-pooling;
- B0 as a non-durable mechanism-isolation control.

Replace:
- old scalar `T_drain = t_complete - t_reconnect` as a claimed receiver-completion metric where `t_complete` was not actually instrumented for the historical FIT runs.

Add:
- M0 network-path restoration;
- M1 MQTT-session restoration;
- M2 sender→broker QoS-1 PUBACK closure;
- M3 receiver-verified historical-state completion;
- M4 live-generation continuity/freshness;
- M5 receiver ordering/stale carryover.

Add prospective protocol:
- H = seq3001–5000;
- M2 direct PUBACK coverage;
- M3 receiver reconciliation;
- same-receiver seq5001 causal witness rule;
- pre/post conservative clock bounds;
- UNRESOLVED classification when the interval crosses zero;
- Stage-A 3-run stop rule.

Historical and prospective FIT must be explicitly labeled as different campaigns.

### 6.6 FIT Results

**Disposition:** CRITICAL REWRITE.

#### Historical FIT

Retain:
- 10,000/10,000 eventual W1 completeness;
- B0 8,000/10,000 bounded negative-control result;
- reconnect about 1.3 s only with its exact endpoint definition.

Correct:
the historical approximately 68–70 s values are not receiver completion.

Authoritative interpretation:
- they are sender-side backlog/PUBACK-closure and implementation-order evidence;
- six historical seq5000→seq5001 gaps:
  68.992, 69.466, 68.944, 68.785, 70.264, 68.852 s;
- mean = 69.217 s;
- range = 68.785–70.264 s.

#### Prospective scored FIT

Add as a new principal result:
- R1 generation gap = 75.208044774 s;
- R2 = 76.307649507 s;
- R3 = 74.797521961 s;
- mean = 75.438 s;
- all 3 runs valid;
- H PUBACK = 2000/2000;
- H receiver completion = 2000/2000;
- 0/3 causal witnesses;
- 0/3 clock-resolved positives;
- 3/3 UNRESOLVED;
- final Stage-A decision = NOT_CONFIRMED_STOP.

Do not pool historical and prospective FIT means.

### 6.7 POWDER Results

**Disposition:** MOSTLY PRESERVE, ADD ONE R6-RELEVANT RESULT.

Preserve:
- failure-domain separation;
- exact/censored/upper-bound timing semantics;
- profile-specific attenuation results;
- no universal RF threshold;
- no pooled FIT+POWDER inference.

Add explicitly:
- E3 cycle 3 stale carryover / ordering existence result:
  seq251–255 arrived at the receiver before older seq231;
- existence claim only;
- no prevalence/frequency inference.

### 6.8 Comparative Synthesis

**Disposition:** REWRITE.

Remove:
“Together they demonstrate” a repeated receiver-recovery misclassification if that conclusion depends on C6.

Replacement synthesis:
- FIT demonstrates repeatable W1 generation blackout under serialized replay and eventual completeness;
- POWDER demonstrates bounded domain/endpoint heterogeneity and one stale-carryover observation;
- prospective R5 leaves M2→M3 materially positive separation unresolved;
- common lesson is measurement discipline, not a pooled effect.

### 6.9 Discussion / Engineering Interpretation

**Disposition:** MAJOR REWRITE.

Delete:
- “path returned in about 1.3 s while complete backlog drainage required about 68 s” if “backlog drainage” means receiver historical completion;
- “receiver state remained incomplete for roughly a minute” from historical data.

Replace with:
- W1 serialized replay repeatedly blocks new record generation for roughly 69 s historically and 75–76 s prospectively;
- this is an implementation-specific completeness–continuity trade-off;
- eventual completeness does not imply continuity/freshness;
- M2 and M3 are semantically different but their positive separation was not resolved in the prospective campaign;
- negative result explicitly retained.

### 6.10 Threats to Validity

**Disposition:** EXPAND.

Must include:
- historical endpoint instrumentation error;
- no exact historical M3 latency;
- prospective cross-host clock uncertainty of approximately ±5 s around D23;
- no causal witness in R5 Stage A;
- 0/3 positive does not prove M2=M3;
- W1 behavior implementation/workload-specific;
- no durable-mechanism superiority;
- B0 asymmetry;
- three run-level replicates only;
- no historical/prospective pooling;
- single bounded POWDER stale-carryover observation;
- testbed results are not field/agronomic validation.

### 6.11 Reproducibility / Data Availability

**Disposition:** UPDATE.

Add durable R5 raw preservation authority:
- artifact SHA-256:
  `5b52005e48d8987091c447186eb39261824f32df15653c3d2773a031b062d4a2`
- three Drive-preserved copies;
- owner-only private integrity copy is long-term authority;
- public/supplemental release must remain sanitized.

Keep credentials/private-session material excluded.

### 6.12 Conclusion

**Disposition:** FULL REWRITE.

Must not conclude:
- approximately 68 s receiver catch-up;
- repeated material endpoint misclassification;
- architecture novelty.

Must conclude:
1. recovery comprises distinct observables;
2. W1 serialized replay repeatedly created a tens-of-seconds live-generation blackout while preserving eventual completeness;
3. POWDER supplied bounded stale-carryover / failure-domain evidence;
4. prospective M2→M3 positive separation was not confirmed and remains unresolved under the measurement uncertainty;
5. the contribution is experimental measurement discipline plus bounded implementation evidence.

## 7. Figure and table reconstruction map

### Existing Figure 1 — system/evidence architecture
Status in prior TNSM main paper: removed from main, retained in supplement.

R7 disposition:
- do not restore the old architecture figure as a novelty figure;
- if a first figure is needed, replace it with an **observable timeline / M0–M5 measurement figure**.

### Existing Figure 2 — FIT record survival / reconnect / catch-up
Disposition: REDESIGN REQUIRED.

Reason:
its catch-up interpretation is contaminated by the old 68 s receiver-completion claim.

Replacement content should separate:
- historical reconnect endpoint;
- historical sender-side PUBACK/backlog/generation blackout evidence;
- prospective 3-run generation-gap evidence;
- M2→M3 interval classified UNRESOLVED.

### Existing Figure 3 — POWDER transition behavior
Disposition: PRESERVE WITH CLAIM-CHECKED CAPTION.

No universal threshold language.

### Existing Figure 4 — POWDER failure-domain / timing semantics
Disposition: PRESERVE WITH CLAIM-CHECKED CAPTION.

May add textual cross-reference to stale carryover, but do not retrofit unverified quantitative content into the figure unless reconstructed from preserved raw evidence.

### New table recommended
One compact **Recovery Observable Table**:
M0–M5, event definition, clock authority, what it establishes, what it does not establish.

### New result table required
One **Prospective Stage-A Table**:
R1/R2/R3, generation gap, H PUBACK coverage, H receiver completion, causal witness, D23 interval, primary class.

No statistical significance table.

## 8. Editorial repair map from AE comments

| AE defect | R7 repair |
|---|---|
| Introduction weak / poorly motivated | rebuild around overloaded recovery observables and concrete W1 trade-off |
| Related Work lacks SOTA/gap | four-block SOTA synthesis ending in bounded measurement gap |
| novelty unclear | explicit A1–A4 contribution paragraph; architecture novelty killed |
| “What is being proposed?” | propose a measurement protocol/taxonomy, not a new persistence mechanism |
| results unconvincing | lead with 6 historical + 3 prospective generation-blackout observations and explicit negative R5 result |
| structure hurts readability | separate Related Work, Methods, Results, Discussion, Reproducibility |
| missing paper organization | add end-of-Introduction roadmap |
| “we” with one author | use “this study,” “the experiment,” or first-person singular only where appropriate |
| IEEE citation style wrong | enforce bracketed IEEE citations |
| references formatted wrong | rebuild bibliography in IEEE style |
| awkward TNSM self-reference | remove venue-name sentence entirely |

## 9. Claim firewall for R7b+

The following phrases/conclusions are prohibited unless R6 is formally reopened with new evidence:

- “approximately 68 s end-to-end recovery”;
- “approximately 68 s receiver completion”;
- “complete receiver backlog drainage required about 68 s”;
- “receiver remained incomplete for about 68 s after reconnect”;
- “endpoint misclassification was repeatedly demonstrated”;
- “M2 materially precedes M3” as an empirical conclusion;
- “novel recovery architecture”;
- “new live lane/backlog lane architecture”;
- “durability harms freshness” generically;
- “first” / “to our knowledge” architecture novelty;
- pooled historical+prospective FIT effect estimate;
- pooled FIT+POWDER effect estimate;
- POWDER stale-carryover prevalence.

## 10. R7 execution decomposition

R7 is decomposed into independent gates:

### R7a — Authority recovery + reconstruction map
Current sub-WP.

### R7b — New revival source skeleton
Create a new LaTeX source identity, section architecture, title candidates, abstract candidate, and contribution/RQ blocks. No full prose sweep yet.

### R7c — Methods + Results reconstruction
Replace invalid timing semantics, add M0–M5 and prospective Stage-A evidence, update displays.

### R7d — Introduction + Related Work + Discussion + Conclusion reconstruction
Close AE novelty/maturity/readability defects against R6.

### R7e — Editorial / IEEE compliance
Single-author voice, IEEE citations/references, structure, terminology, page/figure consistency.

### R7f — Hostile scientific review
Attempt to reject the reconstructed paper using:
- novelty;
- evidence sufficiency;
- comparator;
- endpoint semantics;
- negative-result interpretation;
- testbed heterogeneity;
- sample-size;
- over-generalization.

### R7g — Compile / visual / evidence QA
Byte-level source/PDF package; claim-to-evidence scan; figures/tables; reproducibility links.

No venue decision occurs inside R7. Venue requalification remains R8.

## 11. R7a hostile QA

### QA-1 — Exact rejected decision recovered?
PASS.
The TNSM decision email and every AE criticism relevant to reconstruction were recovered.

### QA-2 — Exact rejected byte identity handled honestly?
PASS.
The final controlled-release hashes are preserved, but exact final TNSM bytes are not falsely claimed as recovered.

### QA-3 — Usable source scaffold recovered?
PASS.
The Sep-07 full LaTeX source and compiled PDF were recovered byte-for-byte with SHA-256 hashes.

### QA-4 — R6 claim changes propagated into every manuscript section?
PASS.
Title, Abstract, Introduction, Related Work, Methods, FIT Results, POWDER, Synthesis, Discussion, Threats, Reproducibility, Conclusion, figures, and tables are explicitly mapped.

### QA-5 — Old 68 s receiver-completion interpretation eliminated?
PASS.
It is identified as prohibited in every relevant section.

### QA-6 — Prospective 0/3 result retained rather than hidden?
PASS.
It is a required principal result and contribution A4.

### QA-7 — Architecture novelty remains killed?
PASS.

### QA-8 — Manuscript edited during R7a?
NO.
No manuscript source/PDF was modified.

## 12. Gate

`R7a_AUTHORITY_RECOVERY=PASS`

`R7a_RECONSTRUCTION_MAP=PASS`

`MANUSCRIPT_EDITED=NO`

`R7b_ENTRY=UNLOCKED`

R7b must create a **new revival source identity**. It must not overwrite or relabel the rejected TNSM controlled release.
