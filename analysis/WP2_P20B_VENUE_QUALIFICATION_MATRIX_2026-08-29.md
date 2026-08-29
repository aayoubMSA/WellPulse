# WP2-P20B — Venue Qualification Matrix

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **COMPLETE / CURRENT-OFFICIAL-GUIDANCE + RECENT-PUBLICATION TEST / AUTHOR-COMMITMENT NOT IMPLIED**

## 1. Purpose

Qualify the strongest current publication venues for the frozen WellPulse manuscript without reopening experiments, changing P13 claims, altering P17/P17V conclusions, modifying P18RC figures, or changing P19 reviewer-artifact semantics.

P20B is a venue decision-support gate only. It may recommend a target and backups. It does not lock the author to a journal, accept copyright/license terms, incur an APC/payment commitment, or submit externally.

## 2. Authorities and decision doctrine

Scientific authorities:

- `HANDOVER_CURRENT.md`;
- `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`;
- `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`;
- `analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md`;
- `docs/WP2_P20A_LITERATURE_NOVELTY_CLOSURE_2026-08-29.md`.

Experience authority:

- Google Sheet `Research & Grants — Lessons Learned Ledger`, especially:
  - LL-036 Venue Utility Rule;
  - LL-037 Publication State Evidence Rule;
  - LL-038 Rejection Classification Rule;
  - LL-039 Active Route Rule;
  - LL-040 Venue Transformation Rule;
  - LL-041 Author Venue-Commit Rule.

Current venue facts were checked on 2026-08-29 against official/current Elsevier journal/shop/ScienceDirect information and actual recent journal publications. A venue is not considered qualified merely because keywords appear in its aims-and-scope page.

## 3. Frozen paper identity relevant to venue fit

Current manuscript:

**WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

The paper is:

- an empirical IoT/systems resilience paper;
- a bounded embedded durability comparison against a **non-durable B0 baseline** on FIT IoT-LAB;
- a separate controlled RF/LTE/MQTT path characterization on POWDER;
- an evidence/methodology contribution around explicit failure domains, endpoint-specific recovery semantics, receiver-side reconciliation, and non-pooled complementary evidence;
- supported by a reviewer supplement and sanitized reproducibility artifact.

The paper is **not**:

- an AI / expert-system paper;
- a generic MQTT-superiority paper;
- a new protocol-design paper;
- a population reliability-estimation paper;
- a field/agronomic validation paper.

## 4. Decision dimensions

Consortium utility score is a decision aid, not an acceptance probability.

| Dimension | Weight | Interpretation |
|---|---:|---|
| Scientific + article-type fit | 25 | Does the actual manuscript belong naturally in the venue? |
| Recent-publication/editorial fit | 20 | Does the journal publish current papers with comparable empirical questions/methods? |
| Editorial plausibility / desk-risk | 20 | Can the contribution be understood without inventing a different paper? |
| Supplement/artifact compatibility | 10 | Can figures, supplement and reproducibility material survive intact? |
| Transformation burden | 10 | How much venue-specific restructuring is likely before submission? |
| Cost exposure | 5 | Is a non-mandatory-APC route available, subject to final author choice? |
| Timeliness / operational suitability | 10 | Does current venue guidance support a timely publication route? |

Total = 100.

## 5. Ranked venue matrix

| Rank | Venue | Utility | Decision | Core reasoning |
|---|---|---:|---|---|
| **1** | **Internet of Things (Elsevier)** | **95/100** | **PRIMARY — GO** | Direct IoT scope; official scope explicitly includes reliability and accepts Full Research plus Open Software/Data; journal states high priority on timely publication; actual recent MQTT robustness work demonstrates direct editorial/readership fit; current WellPulse package can be reused with minimal scientific restructuring. |
| **2** | **Computer Networks (Elsevier)** | **86/100** | **BACKUP #1 — GO** | Strong networking/reliability scope; current MQTT and intermittent-IoT empirical publications; explicit Dataset and Open-Source Software article culture; excellent technical legitimacy. Risk: WellPulse is more failure-domain/evidence-methodology oriented than a protocol/network-algorithm contribution, increasing positioning burden. |
| **3** | **Journal of Systems Architecture (Elsevier)** | **76/100** | **BACKUP #2 — CONDITIONAL GO** | Strong embedded-software/system-architecture fit, including system software and communications software stack. W1 record-state semantics fit well. Risk: POWDER physical-path characterization is less central to JSA's architectural emphasis and would require a more architecture-forward narrative. |
| **4** | **Journal of Network and Computer Applications (Elsevier)** | **70/100** | **HOLD / LOWER PRIORITY** | Scope includes sensor networks, DTN and IoT, but current publication fit is less direct and more algorithm/application oriented. No advantage over the first three sufficient to justify first submission. |
| — | **Expert Systems with Applications** | **38/100** | **KILL FOR CURRENT PAPER** | Current WellPulse is not an expert/intelligent-system contribution. Selecting ESWA would force artificial AI/intelligent-system framing rather than fit the frozen science. |
| — | **Engineering Applications of Artificial Intelligence** | **22/100** | **KILL FOR CURRENT PAPER** | Current official scope expects a novel AI aspect used in a real-world engineering application; WellPulse has no novel AI contribution. This is a hard article-type mismatch. |

## 6. Primary qualification — Internet of Things

### Scope/article type — PASS

Current official Elsevier description identifies the journal as a comprehensive IoT/Cyber-Physical Human Systems venue and explicitly lists:

- Full Research papers;
- Open Software and Data;
- case studies / best practices;
- research on unique IoT challenges including **reliability**.

This maps directly to the current manuscript without changing its scientific identity.

### Recent-publication test — STRONG PASS

A directly relevant published example is:

B. A. Jesus, F. Lins, N. Laranjeiro, **“An approach to assess robustness of MQTT-based IoT systems,”** *Internet of Things*, 31, 101590 (2025), DOI `10.1016/j.iot.2025.101590`.

The paper evaluates MQTT-system robustness using fault injection on real case studies and includes a Zenodo data-availability record. It is not scientifically identical to WellPulse, but it proves that MQTT robustness/fault-oriented empirical work and associated reproducibility material are native to the journal's editorial/readership space.

### Artifact/supplement fit — STRONG PASS

The journal officially lists Open Software and Data among supported publication material, and the recent MQTT robustness article exposes a Zenodo data availability record. P19 therefore aligns naturally with journal culture; no privacy expansion of raw evidence is required.

### Cost — PASS WITH AUTHOR CHOICE LATER

The journal is offered through Elsevier's subscription ecosystem and supports open access. P20B therefore does **not** identify a mandatory OA fee as a prerequisite for the normal subscription route. Optional OA charges, institutional agreements/discounts, taxes and final publishing choices must be re-verified before any rights/payment lock. P20B authorizes **no payment and no OA commitment**.

### Main residual editorial risks

1. B0 is a deliberately non-durable comparator and must remain explicitly bounded.
2. Novelty must remain the P20A compound evaluation contribution; persistence/store-and-forward itself is prior art.
3. FIT and POWDER must remain visibly non-pooled and non-substitutable.
4. POWDER is controlled reference characterization, not architecture-effect estimation.

All four are already controlled by the current manuscript/figure/artifact architecture. No new experiment is needed for venue fit.

## 7. Backup #1 — Computer Networks

### Strengths

Official scope includes network reliability, performance measurement, modeling/analysis and system management. The journal also explicitly supports Dataset Articles and Open-Source Software Articles.

Recent empirical MQTT/network evidence includes:

- C. Innamorati et al., **“The pulse of MQTT in the wild: A large-scale traffic analysis,”** *Computer Networks*, 274, 111845 (2026), DOI `10.1016/j.comnet.2025.111845`;
- additional current work on intermittent IoT connectivity and MQTT/DDS/DTN systems in 2026.

### Why not primary

A Computer Networks submission would likely need the paper to foreground networking/path behavior more strongly. That creates greater risk that reviewers ask for stronger protocol/network comparison or treat the FIT durable-storage result as peripheral. The paper fits, but less natively than it fits *Internet of Things*.

`P20B_CN=GO_BACKUP_1`

## 8. Backup #2 — Journal of Systems Architecture

Official scope covers embedded systems/software, system software, application-specific architecture and communications where focused on analysis/software stack. This strongly supports W1's SQLite/WAL/state-machine implementation and gateway-process restart evidence.

However, the current manuscript intentionally gives substantial scientific weight to controlled RF/path characterization. A JSA version would need architecture-forward restructuring. That is permissible only later as venue-specific transformation and must not change evidence/claims.

`P20B_JSA=CONDITIONAL_GO_BACKUP_2`

## 9. Lower-priority / killed routes

### Journal of Network and Computer Applications — HOLD

Broad IoT/network-applications scope is legitimate, but no material fit/speed/burden advantage over IoT/CN/JSA was found.

### Expert Systems with Applications — KILL

The paper does not study an expert/intelligent system. Retargeting it there would be venue-driven scientific distortion.

### Engineering Applications of Artificial Intelligence — KILL

The paper contains no novel AI method/application contribution satisfying the current official scope. No artificial AI framing is allowed.

## 10. Formatting / length / artifact constraints

No hard full-research word/page ceiling was identified in the accessible current official guidance examined during P20B that would presently force scientific compression of the four-main-figure / three-main-table structure plus supplement.

This does **not** freeze submission formatting. P20D must re-read the selected journal's exact current Guide for Authors immediately before source transformation and must treat any venue-specific changed artifact as version-bound under LL-040.

## 11. Indexing / legitimacy gate

The top-ranked venues are established Elsevier journals with current ScienceDirect journal records and publisher-reported citation metrics. No legitimacy/indexing concern was identified that would disqualify the recommended primary or backups. Exact institutional promotion/scoring requirements, if any, remain an author/institutional check and are not inferred from impact metrics alone.

## 12. Selection verdict

**Primary recommendation:** `INTERNET_OF_THINGS_ELSEVIER`

**Backup #1:** `COMPUTER_NETWORKS_ELSEVIER`

**Backup #2:** `JOURNAL_OF_SYSTEMS_ARCHITECTURE_ELSEVIER_CONDITIONAL`

**Hold:** `JOURNAL_OF_NETWORK_AND_COMPUTER_APPLICATIONS`

**Kill for current manuscript:** `EXPERT_SYSTEMS_WITH_APPLICATIONS`, `ENGINEERING_APPLICATIONS_OF_ARTIFICIAL_INTELLIGENCE`.

The primary recommendation is deliberately a **recommendation, not a submission commitment**. Author venue lock remains downstream.

## 13. Acceptance gate

- current official scope/article-type checks: **PASS**;
- actual recent-publication fit test: **PASS**;
- primary + at least one backup: **PASS**;
- supplement/artifact compatibility: **PASS**;
- cost model assessed without payment commitment: **PASS**;
- destructive-formatting blocker found: **NO**;
- scientific reopening required: **NO**;
- new experiment required: **NO**;
- author committed to venue: **NO**;
- submission authorized: **NO**.

`WP2_P20B_MATRIX=COMPLETE`

`P20B_PRIMARY_RECOMMENDATION=INTERNET_OF_THINGS_ELSEVIER`

`P20B_BACKUP_1=COMPUTER_NETWORKS_ELSEVIER`

`P20B_BACKUP_2=JOURNAL_OF_SYSTEMS_ARCHITECTURE_CONDITIONAL`

`P20B_SCIENTIFIC_REOPEN=NO`

`P20B_NEW_EXPERIMENT_REQUIRED=NO`

`SUBMISSION_AUTHORIZED=NO`
