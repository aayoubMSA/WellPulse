# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P18R — SCIENTIFIC FIGURE ENGINEERING LIFECYCLE**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from conversation memory.

## Executive scientific state

- WP0: **PASS / historical paper story superseded where necessary by P10 evidence-bounded contract**
- WP1: **PASS / frozen historical confirmatory design**
- WP2-P8 manual RF campaign: **COMPLETE / GOLDEN / MANUAL REFERENCE**
- WP2-P9 forensic reconciliation: **PASS / COMPLETE**
- WP2-P10 scientific analysis contract: **PASS / FROZEN**
- WP2-P11 full raw-data scientific analysis: **PASS / COMPLETE**
- WP2-P12 cross-evidence integration: **PASS / COMPLETE**
- WP2-P13 claim–evidence matrix: **PASS / FROZEN**
- WP2-P14 historical publication display set: **PASS / HISTORICAL ONLY**
- WP2-P15 manuscript construction: **PASS / historical internal full draft**
- WP2-P16 adversarial publication QA: **PASS / scientific QA complete**
- WP2-P17 dossier research pack + first consortium revision: **PASS / consortium-revised internal draft + QA**
- WP2-P17V superior independent validation: **PASS / VALIDATED WITH PRE-SUBMISSION CONDITIONS**
- WP2-P18 first main-display redesign: **SUPERSEDED BY P18R**
- WP2-P18B high-standard benchmark: **HISTORICAL BENCHMARK OF PRE-P18R DISPLAY/PACKAGE STATE**
- WP2-P18R scientific figure engineering lifecycle: **PASS / CURRENT MAIN-DISPLAY AUTHORITY**
- new experiment required for current bounded manuscript: **NO**
- new empirical claims required: **NO**
- current scientific blockers: **0**
- submission authorization: **NO**
- live POWDER dependency: **NONE**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8+ result may be promoted or relabelled as scored P7B.

## Mandatory read order for continuation

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
3. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
4. `analysis/WP2_P12_CROSS_EVIDENCE_INTEGRATION_2026-08-29.md`
5. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
6. `manuscript/WP2_P16_ADVERSARIAL_PUBLICATION_QA_2026-08-29.md`
7. `manuscript/WP2_P16_MANDATORY_EDITORIAL_PATCHES_2026-08-29.md`
8. `docs/WP2_P17_EXPERIMENT_DOSSIER_V2_2_RESEARCH_PACK_2026-08-29.md`
9. `analysis/WP2_P17_EVIDENCE_EXPLOITATION_MATRIX_2026-08-29.md`
10. `manuscript/WP2_P17_CONSORTIUM_MANUSCRIPT_REVIEW_2026-08-29.md`
11. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`
12. `manuscript/WP2_P17_CONSORTIUM_REVISION_QA_2026-08-29.md`
13. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
14. `manuscript/WP2_P17V_SUPERIOR_INDEPENDENT_CONSORTIUM_VALIDATION_2026-08-29.md`
15. `analysis/WP2_P18R_FIGURE_REQUIREMENTS_SPEC_2026-08-29.md`
16. `manuscript/WP2_P18R_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE_2026-08-29.md`
17. `analysis/WP2_P18R_GENERATOR_RELEASE_RECEIPT_2026-08-29.md`
18. P9 forensic authorities when exact POWDER trace/caveat semantics are required.
19. P18/P18B only for historical comparison; P18R is the current main-display authority.

## Frozen evidence roles

### FIT = architecture-level record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

- FIT IoT-LAB Grenoble A8-100;
- `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`;
- exactly 10,000 records/cell;
- B0 = non-durable publish-only baseline;
- W1 = durable queue + receiver reconciliation;
- C0 healthy; C1 broker outage; C2 broker outage + gateway-process `exec` restart.

Principal results:

- C0: B0 100%, W1 100% in 3/3;
- C1: B0 80%, W1 100% in 3/3, `+20 pp` each run;
- C2: B0 80%, W1 100% in 3/3, `+20 pp` each run;
- every B0 C1/C2 run misses exactly 2,000/10,000 records, matching the imposed outage-period record block;
- every W1 final run contains all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`.

These are repeated outcomes under the exact treatment, not population reliability probabilities.

Canonical W1 implementation semantics:

- stable `record_id = run_id:boot_id:sequence` identity;
- deterministic canonical JSON;
- SHA-256 checksum;
- SQLite WAL + `synchronous=FULL`;
- `PENDING` / `SENT` state;
- exact duplicate re-enqueue is idempotent;
- conflicting identity reuse raises an integrity error.

### POWDER = communication-path degradation/recovery characterization

Campaign: `WP2-P8`; profile `srslte-controlled-rf`.

Internal control classification remains:

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

Publication-facing role: **separately executed controlled reference characterization; not architecture-effect estimation**.

Principal evidence:

- E1R4 48–50 dB: ICMP clean, MQTT 20/20;
- E1R4 51 dB: ICMP 30% loss, MQTT 20/20;
- E1R4 52 dB: ICMP 60% loss, MQTT 13/20;
- E2 52 dB: ICMP 65% loss, MQTT 11/20;
- E3 52 dB: ICMP loss `80/65/70%`, MQTT completeness `60/25/55%`;
- E8: broker interruption disrupts MQTT while LTE ping remains healthy;
- E9: no-fault control MQTT 60/60 with clean bidirectional ping;
- E10-A: no recovery observed inside preserved RF-only window; censored, no scalar latency;
- E10-B: action-begin→first MQTT publish `6.063318 s`; first ping `6.609430 s`; publish→CORE receipt `0.060172 s`;
- E10-C-B: RF restore→first ping `29.247733 s`; first publish `29.248129 s`;
- E10-D: `<=10.908749 s` upper bound only.

Receiver-side reconciliation remains authoritative. Important concrete examples include E1R4 sequence 96 and E3 sequence 150 being sender-present/receiver-absent without matching sender failure flags, and E8 containing 80 sender-log lines but only 60 unique IDs because recovery IDs were duplicated.

Interpretation remains experiment-specific. No universal 52 dB threshold exists.

## Frozen integration doctrine

FIT and POWDER are complementary, not substitutable:

- **FIT = record-state survival / architecture comparison**.
- **POWDER = communication-path degradation / recovery characterization**.

The synthesis is **failure-domain-aware triangulation**. No pooled FIT+POWDER reliability statistic is allowed.

## Frozen claim envelope

P13 remains the scientific claim authority:

- primary empirical: `IC-01`, `IC-04`, `IC-06`;
- supporting empirical: `IC-02`, `IC-03`, `IC-05`, `IC-07`;
- methodological synthesis: `IC-08`, `IC-09`.

P17/P17V/P18R add no new empirical claims and do not expand P13.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Current manuscript baseline

Canonical consortium-revised internal draft:

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`

Preferred working title:

**WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

P17 uses three empirical RQs and treats cross-testbed triangulation as synthesis rather than a fourth pooled experiment.

Independent P17V verdict:

**VALIDATED WITH PRE-SUBMISSION CONDITIONS.**

- claims validated: `9/9`;
- numerical contradictions: `0`;
- unsupported new claims: `0`;
- scientific blockers: `0`;
- new experiment required: `NO`.

Principal scientific limitation remains transparent: B0 is non-durable and is not the strongest durable MQTT comparator. The current paper is defensible only because it makes the bounded B0 comparison rather than generic MQTT superiority.

## P17 durable research pack

Drive parent: `P12_WellPulse`  
Folder ID: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`

- dossier PDF `WellPulse_Experimental_Technical_Dossier_v2.2.pdf`
  - Drive ID `12ec22A89ybsNoBpYcglx9Im6pW8Vk55-`
  - SHA-256 `a9274514cbf21de58291c2640f560f6082711e0a8696890419e918e595b40f3e`
- reproducible dossier package Drive ID `1ts__z8kN0fORwDksQZoj4eeaG--UyCAw`
- experiment figure suite Drive ID `1y8rStzWdGEivWjuFCP0h5Y6Amv6267sY`
- figure-centered QA report Drive ID `1ukEvwr3_uOoZcCn3TknwOcZL6HRaLo1a`

Dossier role: **audit-grade experiment atlas / manuscript-supplement input**. Raw archives, P9 and P11 remain higher measurement authorities.

## P18R — current main-display authority

P18R supersedes the first P18 main-display implementation. P14/P18 remain historical comparison points only.

### Why P18R exists

The first P18 figures were numerically correct but scientifically too thin. AI-generated redesigns were explicitly rejected and are not canonical. A second consortium design round required a code-first scientific-figure engineering lifecycle.

Core doctrine:

> **Richness must come from scientific structure, not decoration.**

### Current main figures

1. **Figure 1 — System and evidence architecture**
   - W1 code-grounded record-state machine;
   - stable identity/checksum;
   - SQLite WAL/PENDING state;
   - publish/retry/receiver reconciliation;
   - FIT design/treatments/endpoints;
   - POWDER transition/recovery/control roles;
   - IC-01…IC-09 mapping and explicit non-pooling guard.

2. **Figure 2 — FIT record survival and recovery cost**
   - Panel A: all run-level B0/W1 final completeness observations for C0/C1/C2;
   - Panel B: reconnect times;
   - Panel C: W1 backlog-drain times;
   - final integrity, reconnect and durable catch-up remain distinct constructs.

3. **Figure 3 — POWDER transition and repeatability**
   - Panel A: E1R4/E2 ICMP response;
   - Panel B: E1R4/E2 MQTT completeness;
   - Panel C: E3 ICMP-loss cycle variability;
   - Panel D: E3 MQTT-completeness repeatability;
   - no fitted or universal threshold.

4. **Figure 4 — Failure-domain and recovery semantics**
   - Panel A: RF/UE/CORE/broker/no-fault intervention-domain matrix for E4–E10;
   - Panel B: E10 endpoint table preserving exact/censored/upper-bound semantics.

### Current main/supplement boundary

Main article: P18R Figures 1–4.

Supplement:

- detailed E0/E4–E11 experiment atlas;
- individual timeline plots;
- FIT full run ledger;
- run-validity/anomaly registers;
- detailed provenance/hash tables.

Sanitized artifact:

- canonical derived CSVs supporting public values;
- reproducible generator source;
- figure specification;
- manifests and QA receipts;
- releasable evidence after P19 privacy/security review.

### P18R toolchain and V&V

Implementation:

- Matplotlib/Pandas/Numpy for quantitative figures;
- deterministic vector/structured rendering for figure-table material;
- no AI image dependency;
- no manually edited raster source in canonical production path.

The first code implementation was rejected internally despite successful execution because of production-scale/text-layout defects. The layout engine was revised, rebuilt and independently rendered for final visual inspection.

Frozen checks include:

- FIT 18-cell design and all key run-level outcomes;
- 2,000-record B0 outage loss;
- E1R4/E2 key boundary values;
- E3 52 dB `60/25/55%` MQTT and `80/65/70%` ICMP loss;
- E10 censored/upper-bound semantics.

Final release:

`WellPulse_P18R_Scientific_Figure_Engineering_Release_2026-08-29.zip`

Drive ID:

`1alitbv9479Mq9URhXIBHkQql7zuuA51o`

ZIP SHA-256:

`5586091bc518cc541c3c9b75e9a0c965913877cd6bf83d1644fa6f05264e1083`

Generator source SHA-256:

`5a313546fd88b6e06d7d3c473bb6742e214723287bdd37a9b84cf26faadf87f6`

Final figure PDF SHA-256:

- F1 `179b3201b63a5910473885e2005d2ba2bfd55c9fe888f0d1ed42980d21a09ea1`;
- F2 `a38e321ec4a6b51ede1fff89601432852ac0c9e0e56d32ac880724a3b9ad0eff`;
- F3 `bc23a25a53beb13396b056b22bdd93af62ec7c7f91b3d81199028dd4496887ee`;
- F4 `a2be6684ddd339f6b60c1406cb9673a2d14a2c6c038cdb8a0ec748b6b93f5d0c`.

`P18R_CONSORTIUM_DECISION=CONSENSUS_CODE_GENERATED_COMPOSITE_FIGURES`

`P18R_AI_GENERATED_ASSETS=REJECTED_NOT_CANONICAL`

`P18R_DATA_INVARIANTS=PASS`

`P18R_RENDER_FIRST_VISUAL_QA=PASS`

`P18R_FIGURE_ENGINE_VV=PASS`

`WP2_P18R=PASS_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE`

## Benchmark status after P18R

P18B's earlier display score applies to the **pre-P18R** figure implementation and is now historical for figure-quality comparison. A fresh high-standard benchmark should be run against the P18R release before freezing the final submission-facing visual package.

Recommended next bounded gate:

### P18RB — post-P18R high-standard benchmark

Benchmark the new code-generated figures and source package against:

- current target-publisher artwork rules once venue is selected;
- general IEEE/Elsevier/Nature-quality figure-production criteria where venue-neutral;
- accessibility and grayscale robustness;
- typography at final print width;
- code/data/figure reproducibility;
- claim-to-display completeness;
- artifact-evaluation-style reproducibility expectations.

P18RB must not alter science silently. Any scientific encoding change reopens P18R V&V.

## Authorship, affiliation, credits, rights

Canonical current author identity for internal project documents:

**Dr. Ahmed Elsayed Ayoub**  
Assistant Professor of Computer Engineering  
Department of Computer Systems Engineering  
Faculty of Engineering, MSA University  
Giza, Egypt

Do not invent coauthors, CRediT roles, funding, copyright ownership, or licensing terms.

Before submission explicitly verify:

- final author list/order;
- CRediT/contributor roles;
- MSA affiliation wording;
- funding declarations;
- collaborator acknowledgments;
- FIT IoT-LAB acknowledgment/citation;
- POWDER acknowledgment/citation;
- copyright/licensing requirements of the selected venue and applicable institutional/testbed policies.

## Remaining gates before submission authorization

### P18RB — fresh benchmark of P18R

- compare P18R against highest applicable scientific-artwork/reproducibility standards;
- issue gap register;
- permit only evidence-neutral production refinements without reopening science;
- reopen P18R V&V for any scientific encoding change.

### P19 — reviewer-facing supplementary atlas + sanitized artifact

- derive concise reviewer supplement from dossier v2.2;
- include E0–E11, validity, anomalies, FIT ledger and endpoint semantics;
- package analysis code, derived non-sensitive data, manifests and figures;
- privacy/security sanitization before release;
- target an artifact capable of meeting an ACM-style Functional bar and approaching Reusable.

### P20 — final literature / venue / credits / rights / source package

Only after P18RB/P19 PASS:

- submission-date literature check and Gaspar full-text comparison if accessible;
- target-journal selection and current author instructions;
- clean venue LaTeX/source manuscript;
- venue-specific artwork typography/naming/placement normalization;
- final data/code availability statements;
- final authorship/order + CRediT roles;
- funding/COI/collaborator acknowledgments;
- FIT IoT-LAB and POWDER acknowledgment/citation verification;
- copyright/license/permissions audit;
- source↔PDF↔figures↔supplement↔artifact proof QA;
- explicit user authorization before external submission.

## Immutable prohibitions

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- generic “WellPulse beats MQTT”;
- universal 52 dB threshold;
- deterministic RF-only recovery;
- exact broker latency from E10-D;
- population reliability from message counts or three FIT replicates;
- field/rural/Siwa/pump/hydraulic/groundwater/agronomic/industrial-process validation;
- unresolved RF-path/runtime USRP identity;
- pooled FIT+POWDER inferential statistics;
- historical uniqueness of the two-property framework unless separately established by literature evidence.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence and registered research packs.**
2. **GitHub = canonical scientific/control record.**
3. **Home PC = independent third copy where applicable.**

Raw evidence remains immutable.

## Stop state

`WP2_P8_STATUS=COMPLETE_GOLDEN_EVIDENCE_PRESERVED`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`WP2_P9=PASS_GOLDEN_EVIDENCE_RECONCILED`

`WP2_P10=PASS_SCIENTIFIC_ANALYSIS_CONTRACT_FROZEN`

`WP2_P11=PASS_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS`

`WP2_P12=PASS_CROSS_EVIDENCE_INTEGRATION`

`WP2_P13=PASS_CLAIM_EVIDENCE_MATRIX_FROZEN`

`WP2_P14=PASS_HISTORICAL_DISPLAY_SET`

`WP2_P15=PASS_MANUSCRIPT_CONSTRUCTED_EVIDENCE_BOUNDED`

`WP2_P16=PASS_ADVERSARIAL_PUBLICATION_QA`

`P17_DOSSIER_RESEARCH_PACK=REGISTERED`

`WP2_P17_QA=PASS_CONSORTIUM_REVISION_EVIDENCE_BOUNDED`

`WP2_P17V=PASS_SUPERIOR_INDEPENDENT_VALIDATION`

`P17V_VERDICT=VALIDATED_WITH_PRE_SUBMISSION_CONDITIONS`

`WP2_P18=SUPERSEDED_BY_P18R`

`WP2_P18B=HISTORICAL_PRE_P18R_BENCHMARK`

`WP2_P18R=PASS_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE`

`P18R_AI_GENERATED_ASSETS=REJECTED_NOT_CANONICAL`

`LIVE_POWDER_DEPENDENCY=NONE`

`SUBMISSION_AUTHORIZED=NO`

`NEXT_PHASE=WP2_P18RB_POST_P18R_HIGH_STANDARD_BENCHMARK`
