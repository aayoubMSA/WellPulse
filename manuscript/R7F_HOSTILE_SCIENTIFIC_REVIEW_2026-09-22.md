# WellPulse IEEE Revival — R7f Hostile Scientific Review

**Date:** 2026-09-22  
**Review target:** `manuscript/revival_2026-09-22/WellPulse_Revival_R7e_Editorial_20260922.tex`  
**R7e source blob:** `ee8d455328e420aa11103c554c32509f215dc208`  
**R7e successful-build TEX SHA-256:** `b966a951d94a1c8d2d72cbd55c6680df355853a53f3577b2ed1c8f1fef369442`  
**Review mode:** hostile / rejection-seeking  
**Manuscript edits in R7f:** NONE

## 1. Executive disposition

The revived manuscript is scientifically coherent and no longer contains the fatal endpoint error that drove the original rejection. The surviving W1 result is correctly bounded, the prospective 0/3 result is retained honestly, and POWDER is not statistically pooled with FIT.

However, a skeptical expert reviewer can still reject the paper on **novelty depth, SOTA completeness, protocol-validation depth, and reproducibility presentation**.

Disposition:

`R7f_HOSTILE_REVIEW_EXECUTED=PASS`

`R7f_MANUSCRIPT_DISPOSITION=MAJOR_REPAIR_REQUIRED`

`R7g_ENTRY=LOCKED_PENDING_R7f_REPAIR`

No new experiment is required by the hostile review. The required repairs are manuscript/evidence-presentation repairs unless R8 later targets a venue that demands stronger comparative experimentation.

## 2. Reviewer-lens verdicts

### Lens A — MQTT / protocol semantics
**Verdict: SCIENCE SOUND, POSITIONING INCOMPLETE.**

Strengths:
- M2 is correctly restricted to publisher-to-broker QoS-1 acknowledgement closure.
- M3 is correctly receiver-reconciled historical completion.
- The manuscript does not infer subscriber completion from PUBACK.
- The 0/3 prospective result is not converted into a positive M2→M3 claim.

Attack:
The Related Work currently treats E-MQTT as the principal end-to-end-confirmation comparator, but two peer-reviewed 2026 papers now directly address MQTT broker-QoS versus application/database-level confirmation and recovery:
1. A. Mohammed et al., “A Resilient MQTT-based Architecture for Real-time Solar Photovoltaic Monitoring,” *International Journal of Intelligent Engineering and Systems*, 19(5), 2026. DOI: 10.22266/ijies2026.0531.19.
2. A. Mohammed et al., “A Scalable MQTT-Based Edge IoT Architecture for Real-Time Distributed Solar PV Panel Monitoring,” *Engineering, Technology & Applied Science Research*, 16(3), 36014–36024, 2026. DOI: 10.48084/etasr.16945.

Both explicitly couple disk-backed persistence with application/database-level acknowledgement beyond broker QoS. Their existence narrows any remaining “broker acknowledgement versus end-to-end durability” gap further.

Required repair:
- add both papers;
- explicitly concede their end-to-end durability/application-ACK contribution;
- state that WellPulse differs by **measurement semantics and endpoint adjudication**, not by application-level acknowledgement architecture.

Severity: **MAJOR / mandatory before resubmission.**

## 3. Lens B — novelty and contribution depth
**Verdict: CORE SURVIVES, BUT A1 IS VULNERABLE.**

A1 currently calls M0–M5 a “reproducible measurement protocol.” A hostile reviewer can respond:
- network restoration, session restoration, acknowledgement, receiver completion, continuity, and ordering are individually familiar observables;
- simply naming them M0–M5 is not, by itself, a scientific contribution;
- the paper must show why this operationalization changes experimental conclusions or prevents a concrete class of measurement errors.

The paper partly does this through the corrected historical 68 s interpretation and the prospective 0/3 adjudication, but that logic is distributed across sections rather than made explicit as the validation of A1.

Required repair:
- reframe A1 from taxonomy novelty to **operational recovery-measurement discipline**;
- add one compact campaign-by-observable coverage matrix showing which of M0–M5 is directly observed in historical FIT, prospective FIT, and POWDER;
- state explicitly that not every campaign observes every endpoint;
- show the historical endpoint reclassification as the protocol’s concrete validation case;
- avoid implying that the M0–M5 labels themselves are novel.

Severity: **MAJOR / repairable without new experiment.**

## 4. Lens C — W1 completeness–continuity result
**Verdict: VALID BUT VENUE-LIMITING.**

The repeated generation blackout is real under the frozen W1 code path:
- 6/6 historical observations around 69 s;
- 3/3 prospective observations around 75–76 s;
- eventual receiver completeness preserved.

Hostile attack:
The mechanism is structurally expected because W1 serially drains the historical queue before generating sequence 5001. A reviewer can argue that the experiments mainly quantify an implementation behavior already implied by the code, rather than discover a general systems phenomenon.

Missing comparative depth:
- no interleaved live/backlog scheduler comparator;
- no backlog-size scaling curve;
- no replay-concurrency ablation;
- no broker-throughput sensitivity analysis.

This does **not** invalidate A2 because the paper correctly limits it to the tested W1 implementation. It does constrain the suitable venue and prevents broad novelty claims.

Required repair:
- explicitly call A2 a **measured implementation consequence** rather than an emergent generic trade-off;
- state that the experiment quantifies the magnitude and repeatability of a code-path-implied continuity cost;
- preserve alternative-scheduler/backlog-scaling experiments as future work, not as missing evidence for the bounded claim.

Severity: **MAJOR for top-tier networking novelty; MINOR for a bounded experimental/measurement venue.**

## 5. Lens D — prospective negative result
**Verdict: STRONG SCIENTIFIC HYGIENE; LIMITED POSITIVE CONTRIBUTION.**

Strength:
The prospective campaign is one of the strongest parts of the revival because it refuses to convert clock-uncertain evidence into a positive result.

Attack:
A4 is currently framed as a “contribution,” but 0/3 UNRESOLVED primarily serves as **claim adjudication / falsification discipline**, not a standalone positive systems contribution.

Required repair:
- retain the result prominently;
- consider renaming A4 from “Explicit negative/bounded result” to **Prospective endpoint adjudication**;
- make clear that its scientific value is constraining the claim ceiling.

Severity: **MODERATE.**

## 6. Lens E — cross-environment evidence
**Verdict: EVIDENCE VALID; WORD ‘TRIANGULATION’ OVERSTATES UNITY.**

FIT and POWDER probe different phenomena:
- FIT: serialized W1 replay and endpoint instrumentation;
- POWDER: physical transition/failure-domain behavior and one stale-carryover observation.

They are complementary, but they do not independently estimate the same latent effect. “Cross-environment triangulation” may therefore imply stronger convergent validation than the design supplies.

Required repair:
- rename A3 to **Complementary cross-environment evidence without pooling**;
- use “complementary” rather than “triangulation” throughout;
- preserve the current non-pooling rule.

Severity: **MAJOR wording/claim-boundary repair.**

## 7. Lens F — statistics and replication
**Verdict: ACCEPTABLE FOR DESCRIPTIVE ENGINEERING; NOT FOR POPULATION INFERENCE.**

Strengths:
- run, not message, is the unit;
- no message-level pseudo-replication;
- no p-value theater;
- no confidence intervals constructed from tiny n;
- historical and prospective campaigns are not pooled.

Attacks:
1. Historical six-gap mean combines C1 and C2 observations even though C1 and C2 are different treatments.
2. n=3 per cell and n=3 prospective runs support repeatability in the tested setup only.
3. Means can look more inferential than intended with such small deterministic run sets.

Required repair:
- report C1 and C2 historical gap summaries separately in addition to the six-run campaign range;
- retain all individual run values;
- keep language descriptive;
- optionally emphasize median/range or per-run values over an aggregate mean.

Existing condition means from frozen evidence:
- historical W1 C1 mean ≈ 69.134 s;
- historical W1 C2 mean ≈ 69.300 s.

Severity: **MODERATE.**

## 8. Lens G — reproducibility
**Verdict: CURRENT MANUSCRIPT PRESENTATION IS NOT YET STRONG ENOUGH TO SUPPORT THE WORD “REPRODUCIBLE.”**

The repository/evidence system is strong internally, but the paper itself omits several execution details that a reader would need:
- broker/client versions;
- Paho version;
- Mosquitto version;
- W1 persistence implementation details (SQLite queue);
- exact C1/C2 outage mechanism;
- outage timing/window;
- FIT node/site/execution identity;
- prospective clock-bound procedure details;
- treatment command semantics;
- sanitized execution scripts / public artifact pointer.

Static inspection of the R7e manuscript found:
- figures: 0;
- tables: 3;
- bibliography items: 8;
- “Mosquitto”: absent;
- “paho”: absent;
- “SQLite”: absent;
- “iptables”: absent;
- FIT experiment 449953: absent;
- no supplement reference.

The Reproducibility section cites internal preservation machinery and says the public repository/DOI pointer is deferred. That is honest, but at submission time it weakens the claim that the protocol is reproducible.

Required repair:
- either create and cite a sanitized supplementary reproduction package before submission, or downgrade “reproducible” to “operational” / “repeatable within the preserved experimental package”;
- add a compact implementation/configuration table;
- expose enough method detail that a reviewer need not trust an inaccessible internal evidence ledger.

Severity: **MAJOR / mandatory before submission.**

## 9. Lens H — visual scientific communication
**Verdict: UNDERDEVELOPED FOR A JOURNAL PAPER.**

R7e contains zero figures. For a paper whose central contribution is separating recovery stages, this is a missed opportunity and a likely readability criticism.

Required repair:
At minimum add one scientific figure, without changing evidence:
- recovery-observable timeline/schematic M0→M5 showing that ordering is semantic, not asserting measured temporal separation;
or
- W1 execution timeline showing outage, serialized backlog replay, and the seq5000→5001 generation blackout;
or preferably both if page budget permits.

Any figure must be generated entirely from frozen semantics/data and must not visually imply M2>M3 where the prospective evidence is unresolved.

Severity: **MODERATE-to-MAJOR.**

## 10. Lens I — Related Work completeness
**Verdict: FAIL IN CURRENT FORM.**

Eight references are too sparse for a journal article that survives primarily by precise novelty positioning. Seven DOI-bearing references were independently verified as matched and unretracted; the OASIS MQTT standard is a non-DOI standards reference and was not resolvable by the DOI-oriented verifier.

The problem is not reference authenticity. It is **coverage**.

Required additions should include:
- the two 2026 Mohammed et al. MQTT durability/application-ACK papers above;
- at least several more directly relevant works on MQTT persistence/recovery, broker failover, telemetry buffering/replay, and empirical IoT messaging failure/recovery behavior;
- only works that materially sharpen the boundary; avoid padding.

Target:
a focused Related Work set large enough to establish SOTA credibly, not a fixed arbitrary reference count.

Severity: **MAJOR / mandatory.**

## 11. Lens J — title/abstract
**Verdict: GOOD, WITH ONE SMALL RISK.**

Title is bounded and no longer makes the rejected receiver-completion claim.

Abstract accurately reports:
- separate recovery observables;
- 10,000/10,000 eventual completeness;
- historical/prospective generation gaps;
- 0/3 unresolved M2→M3;
- one POWDER stale-carryover trace;
- non-universal claim ceiling.

Minor attack:
“The results support recovery-observable measurement” is vague and can read as self-validation.

Required repair:
replace with a sharper statement that the protocol **prevents sender-side acknowledgement closure from being mislabeled as receiver completion and exposes replay-associated continuity separately**, while preserving the 0/3 unresolved outcome.

Severity: **MINOR.**

## 12. Fatal-issue search

### F1. Contradiction with R6?
PASS — none found.

### F2. Resurrected 68 s receiver-completion claim?
PASS — none found.

### F3. Hidden positive M2→M3 inference?
PASS — none found.

### F4. Generic MQTT durability/freshness causality?
PASS — blocked.

### F5. Pooled FIT/POWDER inference?
PASS — blocked.

### F6. Pseudo-replication?
PASS — explicitly blocked.

### F7. POWDER prevalence overclaim?
PASS — blocked.

### F8. Fabricated/retracted current references?
PASS for all DOI-bearing references audited; none retracted. OASIS standard not evaluated by DOI resolver.

### F9. Missing direct 2026 prior art?
FAIL — two directly overlapping MQTT durability/application-ACK papers are absent.

### F10. Submission-ready reproducibility?
FAIL — internal preservation is strong, but public/supplementary reproduction surface is not yet submission-ready.

## 13. Required repair package before R7g

### R7f-R1 — SOTA repair
- add and distinguish the two Mohammed et al. 2026 MQTT-ACK papers;
- expand focused recovery/persistence empirical literature;
- keep architecture novelty killed.

### R7f-R2 — Contribution-boundary repair
- A1: operational measurement discipline, not taxonomy novelty;
- A3: “complementary cross-environment evidence,” not “triangulation”;
- A4: prospective endpoint adjudication / negative claim-boundary result.

### R7f-R3 — Reproducibility surface
- compact implementation/configuration table;
- sanitized supplement/public reproduction package or downgrade “reproducible” wording;
- preserve private raw authority separately.

### R7f-R4 — Evidence presentation
- explicit M0–M5 × campaign observability matrix;
- split historical C1/C2 descriptive summaries;
- add at least one evidence-faithful recovery timeline/measurement figure.

No new scored experiment is required for R7f-R1 through R7f-R4.

## 14. Venue-risk note for R8

Even after the above repairs, the manuscript’s strongest empirical result remains an implementation-specific consequence of serialized replay rather than a new recovery mechanism. A highly selective networking/systems journal may still consider the novelty depth insufficient without a scheduler comparison, scaling study, or broader mechanism evaluation.

That is a **venue-fit risk**, not a scientific invalidity. R8 must account for it when requalifying journals.

## 15. Gate

`R7f_HOSTILE_REVIEW_EXECUTED=PASS`

`R7f_FATAL_SCIENTIFIC_DEFECT=NONE_FOUND`

`R7f_MAJOR_REPAIR_REQUIRED=YES`

`R7g_ENTRY=LOCKED`

`NEXT=R7f-R1_SOTA_AND_CLAIM_BOUNDARY_REPAIR`

Stop state:
- R7e manuscript unchanged;
- no scientific data modified;
- no new experiment authorized;
- R7g remains locked until targeted repair package passes.
