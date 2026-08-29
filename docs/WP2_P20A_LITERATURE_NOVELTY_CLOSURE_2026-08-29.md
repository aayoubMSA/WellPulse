# WP2-P20A — Literature & Novelty Closure

Date: 2026-08-29  
Status: **PASS / SUBMISSION-DATE LITERATURE CLOSED / NOVELTY BOUNDARY NARROWED / NO SCIENTIFIC BLOCKER**

## 1. Scope

P20A executed only the venue-neutral final literature/novelty gate defined in `handover/AGENT_MANDATE_WP2_P20A_2026-08-29.md`.

It did not select a journal, perform venue formatting, change authorship/rights, rebuild the final source package, alter any experiment/result, add an empirical claim, reopen P13/P17/P17V/P18RC/P19, or authorize submission.

Companion authority:

`analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md`

## 2. Search completion

A current search dated **2026-08-29** covered:

- MQTT persistence/session/retransmission;
- MQTT/IoT robustness, stress testing and fault injection;
- offline-first / Edge–Cloud continuity / store-and-forward;
- end-to-end acknowledgment, receiver confirmation and durable application persistence;
- failure-domain-aware resilience/recovery evaluation;
- real wireless/IoT testbeds and repeatability/reproducibility;
- receiver-side reconciliation/provenance where materially relevant.

The search explicitly included literature published after the earlier P16/P17 review and identified material 2026 comparators that were not yet present in the P17 reference list.

## 3. Material P17 bibliography re-verification

All 11 material P17 related-work/testbed/technical anchors were rechecked against current authoritative publisher/project/institutional sources.

| P17 ref. | Anchor | Verification result |
|---|---|---|
| [1] | Asgari Araghi & Khendek 2026, DOI `10.1007/s43926-026-00322-w` | **VERIFIED** — Springer / Discover Internet of Things |
| [2] | Jesus, Lins & Laranjeiro 2025, DOI `10.1016/j.iot.2025.101590` | **VERIFIED** — Elsevier / Internet of Things |
| [3] | Domingues, Faria & Portugal 2024, DOI `10.1186/s13638-023-02327-3` | **VERIFIED** — Springer Nature / EURASIP JWCN |
| [4] | Gaspar et al. 2026, DOI `10.1109/MIOT.2026.3681190` | **BIBLIOGRAPHICALLY VERIFIED** — ISR Coimbra + CTTC + current author publication list; full-text status handled separately below |
| [5] | Colarusso, Falco & Zimeo 2025, DOI `10.1016/j.iot.2025.101723` | **VERIFIED** — Elsevier / Internet of Things |
| [6] | Herrera et al. 2026, DOI `10.3390/fi18040180` | **VERIFIED** — MDPI / Future Internet |
| [7] | Monzon Baeza et al. 2026, DOI `10.3390/s26154919` | **VERIFIED** — MDPI / Sensors + indexed full record |
| [8] | Adjih et al. 2015 FIT IoT-LAB, DOI `10.1109/WF-IOT.2015.7389098` | **VERIFIED** — FIT IoT-LAB official citation guidance + publication record |
| [9] | Papadopoulos et al. 2017, DOI `10.1016/j.comnet.2017.03.012` | **VERIFIED** — Elsevier / Computer Networks |
| [10] | Breen et al. 2021 POWDER, DOI `10.1016/j.comnet.2021.108281` | **VERIFIED** — Elsevier / Computer Networks + POWDER official citation guidance |
| [11] | Eclipse Paho Java persistence documentation | **VERIFIED** — current Eclipse Paho docs/source explicitly document file persistence and loss risk for memory-only state across shutdown/restart |

`P20A_MATERIAL_P17_ANCHORS_VERIFIED=11_OF_11`

## 4. Gaspar et al. 2026 full-text gate

Bibliographic identity is independently verified:

**L. M. Gaspar, J. N. C. Faria, M. Domingues, F. Famá, L. Martins, D. Portugal, “The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications,” IEEE Internet of Things Magazine, 2026, DOI `10.1109/MIOT.2026.3681190`.**

Current evidence also shows that David Portugal's publication page advertises a `[PDF | DOI]` entry for this article. During P20A, however, the actual linked PDF/full text could not be recovered through the available retrieval channel, and IEEE full text was not independently exposed through an accessible authoritative page.

Therefore:

- **no method/result/fault-model/quantitative attribution is made from Gaspar et al.;**
- the manuscript treatment must remain bibliographic/scope-level only;
- no overlap is inferred from the title alone;
- if the full text is later directly recovered before final submission, it may be compared without reopening experiments; any material collision must be evaluated against this P20A matrix before wording changes.

`P20A_GASPAR_BIBLIOGRAPHIC_RECORD=VERIFIED`

`P20A_GASPAR_AUTHOR_PDF_LINK=ADVERTISED`

`P20A_GASPAR_FULLTEXT=NOT_RECOVERED_IN_CURRENT_RETRIEVAL_CHANNEL`

`P20A_GASPAR_DETAILED_ATTRIBUTION=PROHIBITED`

## 5. New submission-date literature with material effect

### 5.1 Mohammed et al. 2026 — material comparator

**A. Mohammed, R. S. S. Singh, S. Aslam, Y. C. Wong, “A Scalable MQTT-Based Edge IoT Architecture for Real-Time Distributed Solar PV Panel Monitoring,” Engineering, Technology & Applied Science Research, 16(3), 36014–36024, 2026, DOI `10.48084/etasr.16945`.**

This is the closest newly identified conceptual comparator. Its published record describes disk-backed edge persistence, an application-level acknowledgment after fog/database insertion, tested recovery during network disruption, and explicit decoupling of sensing reliability from network availability.

**Impact: `WORDING NARROWING — MATERIAL`.**

It does **not** invalidate WellPulse's bounded evidence, but it eliminates any defensible priority claim for:

- durable application persistence during network interruption;
- application-level acknowledgment after durable downstream storage;
- generic complete-recovery concept;
- historical priority for decoupling data/sensing reliability from network availability.

This paper is a **mandatory related-work addition** in P20D.

### 5.2 Im & Lim 2023 E-MQTT — receiver-confirmation comparator

**Y. Im, M. Lim, “E-MQTT: End-to-End Synchronous and Asynchronous Communication Mechanisms in MQTT Protocol,” Applied Sciences 13(22), 12419, 2023, DOI `10.3390/app132212419`.**

E-MQTT establishes prior work on publisher awareness of subscriber-side receipt through an MQTT protocol extension. It is not the same mechanism as WellPulse's receiver-side record-identity reconciliation, but it means end-to-end receiver confirmation cannot be framed as historically new.

**Impact: `WORDING NARROWING`.**

This is a **mandatory/strongly preferred related-work addition** in P20D wherever receiver-side evidence is positioned as a contribution.

### 5.3 Radwan, Sheldon & Wang 2026 — very recent MQTT reliability work

**N. M. Radwan, F. T. Sheldon, Y. Wang, “A backpressure-driven flow control model for stabilizing MQTT communication in IoT systems,” Scientific Reports, published 17 August 2026, DOI `10.1038/s41598-026-66865-8`.**

The study addresses broker congestion, latency and message loss under varying traffic loads/network conditions using adaptive publishing/backpressure. Its core question is load/flow-control stability rather than durable record survival under explicit failure domains.

**Impact: `NO IMPACT` on the frozen WellPulse claim envelope**, but it should be added or explicitly considered in P20D so the submission reflects literature current to 29 August 2026.

## 6. Other current boundary evidence

Current official/technical sources further reinforce the existing conservative boundary:

- AWS IoT Core persistent sessions can retain subscriptions and qualifying queued messages for later delivery after reconnect, subject to service limits/expiry;
- Azure IoT Operations documents destination-aware acknowledgment and disk persistence for queued processing across outages/restarts;
- Eclipse Paho provides file-backed persistence for reliable in-flight MQTT message handling across network/client/device interruption;
- recent NIST work (2026, DOI `10.1109/OJIM.2026.3679169`) reinforces that controlled repeatable physical wireless-IoT testing is itself established methodology.

These are comparator/context sources, not WellPulse scientific evidence.

## 7. Final novelty boundary

### Not defensible as novelty

The submission must not claim novelty for persistence, buffering, disk-backed queues, retransmission, store-and-forward, offline-first continuity, generic reconciliation, application/database acknowledgments, end-to-end subscriber confirmation, generic MQTT robustness/fault testing, real-testbed repeatability, or the abstract idea that application/data reliability can differ from network availability.

### Defensible bounded contribution

The manuscript can defend the following **compound evaluation contribution**, without claiming historical firstness:

> WellPulse uses a failure-domain-aware evaluation framework that measures application record-state survival separately from communication-path recovery, combining receiver-reconciled real-embedded durability evidence with a separately executed controlled wireless/path characterization, preserving mechanism-specific exact/censored/upper-bound recovery semantics and integrating the evidence without a pooled reliability metric.

The FIT result remains a bounded comparison against the **non-durable B0 baseline**, not a protocol-level or strongest-durable-MQTT superiority result.

Receiver-side reconciliation remains a demonstrated evidence practice, not a historical-priority theorem.

## 8. Collision verdict

Companion matrix result:

- `SCIENTIFIC BLOCKER = 0`
- `WORDING NARROWING = 11 source/axis groups`
- `NO IMPACT = 6 source/axis groups`

The closest new comparator requires **editorial novelty narrowing only**. No new experiment, new empirical claim, new statistic, or reinterpretation of existing evidence is required.

## 9. P20D mandatory literature instructions

When the manuscript is integrated later under P20D:

1. add Mohammed et al. 2026 as a direct durable-edge/application-ack comparator;
2. add E-MQTT where end-to-end receiver confirmation is discussed;
3. add or explicitly account for Radwan et al. 2026 as current MQTT load-stability/reliability work;
4. keep Gaspar et al. at bibliographic/scope level unless full text is directly recovered;
5. retain explicit B0 non-durable boundary and durable-MQTT limitation;
6. state the two-property/failure-domain structure as **this study's evaluation framework**, not a certified first-ever framework;
7. do not change any P13 empirical claim, numerical value, statistical unit, failure-domain meaning, or FIT/POWDER inferential role.

## 10. Acceptance gate

- current literature search completed and dated: **PASS**;
- material P17 bibliographic anchors verified: **11/11 PASS**;
- Gaspar bibliographic record: **PASS**;
- Gaspar full-text: **explicit non-recovery status recorded; no unsupported attribution**;
- newly published material comparators assessed: **PASS**;
- comparator/novelty matrix: **PASS**;
- novelty remains inside P13/P17V envelope: **PASS**;
- scientific blocker: **0**;
- new experiment required: **NO**;
- new empirical claim required: **NO**;
- submission authorized: **NO**.

## 11. Closure

`WP2_P20A=PASS_LITERATURE_AND_NOVELTY_CLOSURE`

`P20A_SEARCH_DATE=2026-08-29`

`P20A_MATERIAL_ANCHORS_VERIFIED=11_OF_11`

`P20A_CLOSEST_NEW_COMPARATOR=MOHAMMED_ET_AL_2026_ETASR_16945`

`P20A_NOVELTY_ACTION=WORDING_NARROWING_ONLY`

`P20A_SCIENTIFIC_BLOCKERS=0`

`P20A_NEW_EXPERIMENT_REQUIRED=NO`

`P20A_NEW_EMPIRICAL_CLAIM_REQUIRED=NO`

`P20B_LOCK_RELEASED=YES`

`NEXT=WP2_P20B_VENUE_QUALIFICATION_AND_SELECTION_GATE`

`SUBMISSION_AUTHORIZED=NO`
