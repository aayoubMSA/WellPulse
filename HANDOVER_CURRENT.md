# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P18 — MAIN-DISPLAY REDESIGN + CLAIM/DISPLAY QA** and **WP2-P18B — HIGH-STANDARD PUBLICATION/ARTIFACT BENCHMARK**.

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
- WP2-P14 historical publication display set: **PASS / SUPERSEDED FOR MAIN-DISPLAY USE BY P18**
- WP2-P15 manuscript construction: **PASS / historical internal full draft**
- WP2-P16 adversarial publication QA: **PASS / scientific QA complete**
- WP2-P17 dossier research pack + consortium revision: **PASS / consortium-revised internal draft + QA**
- WP2-P17V superior independent validation: **PASS / VALIDATED WITH PRE-SUBMISSION CONDITIONS**
- WP2-P18 main-display redesign: **PASS / NEW MAIN DISPLAY SET FROZEN**
- WP2-P18B high-standard benchmark: **COMPLETE / DISPLAY 95.6% CHECKLIST COVERAGE / WHOLE PACKAGE 84% READINESS-EQUIVALENT**
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
15. `manuscript/WP2_P18_MAIN_DISPLAY_REDESIGN_AND_QA_2026-08-29.md`
16. `manuscript/WP2_P18_FINAL_DISPLAY_PACK_INTEGRITY_RECEIPT_2026-08-29.md`
17. `manuscript/WP2_P18_FIGURE_CAPTIONS_ALT_TEXT_2026-08-29.md`
18. `analysis/WP2_P18_FAILURE_DOMAIN_TAXONOMY_2026-08-29.csv`
19. `analysis/WP2_P18_MAIN_SUPPLEMENT_DISPLAY_SPLIT_2026-08-29.csv`
20. `analysis/WP2_P18B_HIGH_STANDARD_PUBLICATION_ARTIFACT_BENCHMARK_2026-08-29.md`
21. P9 forensic authorities when exact POWDER trace/caveat semantics are required.
22. P14 files only for historical comparison; P18 is authoritative for the current main display set.

## Frozen evidence roles

### FIT = architecture-level record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

- FIT IoT-LAB Grenoble A8-100;
- `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`;
- 10,000 records/cell;
- B0 = non-durable publish-only baseline;
- W1 = durable queue + receiver reconciliation;
- C0 healthy; C1 broker outage; C2 broker outage + gateway-process exec restart.

Principal results:
- C0: B0 100%, W1 100% in 3/3;
- C1: B0 80%, W1 100% in 3/3, `+20 pp` each run;
- C2: B0 80%, W1 100% in 3/3, `+20 pp` each run;
- every B0 C1/C2 run misses exactly 2,000/10,000 records, matching the imposed outage-period record block;
- every W1 final run contains all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`.

These are repeated outcomes under the exact treatment, not population reliability probabilities.

Canonical W1 implementation semantics:
- stable `run_id:boot_id:sequence` identity;
- deterministic canonical JSON;
- SHA-256 checksum;
- SQLite WAL + `synchronous=FULL`;
- `PENDING` / `SENT` states;
- identical re-enqueue is idempotent;
- conflicting identity reuse raises an integrity error.

### POWDER = communication-path degradation/recovery characterization

Campaign: `WP2-P8`; profile `srslte-controlled-rf`.

Internal control classification:

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

Publication-facing role: **separately executed controlled reference characterization; not architecture-effect estimation**.

Principal evidence:
- E1R4 48–50 dB: ICMP clean, MQTT 20/20;
- E1R4 51 dB: ICMP 30% loss, MQTT 20/20;
- E1R4 52 dB: ICMP 60% loss, MQTT 13/20;
- E3 52 dB: ICMP loss `80/65/70%`, MQTT completeness `60/25/55%`;
- E8: broker interruption disrupts MQTT while LTE ping remains healthy;
- E9: no-fault control MQTT 60/60 with clean bidirectional ping;
- E10-A: no recovery inside preserved RF-only timing window; censored, no scalar latency;
- E10-B: action-begin→first MQTT publish `6.063318 s`; first ping `6.609430 s`; publish→CORE receipt `0.060172 s`;
- E10-C-B: RF restore→first ping `29.247733 s`; first publish `29.248129 s`;
- E10-D: `<=10.908749 s` upper bound only.

Receiver-side reconciliation remains authoritative. E1R4 seq 96 and E3 seq 150 are sender-present/receiver-absent without matching sender failure flags; E8 has 80 sender-log lines but only 60 unique IDs due to duplicate recovery sends.

Interpretation remains experiment-specific. No universal 52 dB threshold is claimed.

## Frozen integration doctrine

FIT and POWDER are complementary, not substitutable:
- **FIT = record-state survival / architecture comparison**;
- **POWDER = communication-path degradation / recovery characterization**.

The synthesis is **failure-domain-aware triangulation**. No pooled FIT+POWDER reliability statistic is allowed.

## Frozen claim envelope

P13 remains the scientific claim authority:
- primary empirical: `IC-01`, `IC-04`, `IC-06`;
- supporting empirical: `IC-02`, `IC-03`, `IC-05`, `IC-07`;
- methodological synthesis: `IC-08`, `IC-09`.

P17/P17V/P18 add no new empirical claim and do not expand P13.

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

## P18 current main-display authority

P18 replaces P14 for the publication-facing **main display selection**. P14 remains historical evidence of earlier display work.

### Main figures

1. `Fig_P18_01_architecture_evidence_roles` — W1 record lifecycle + FIT/POWDER non-overlapping roles.
2. `Fig_P18_02_FIT_completeness` — B0/W1 run-level final completeness on a full `0–100%` scale.
3. `Fig_P18_03_POWDER_transition_direction` — E1R4/E2 cross-layer response on a full percentage scale.
4. `Fig_P18_04_POWDER_E3_repeatability` — E3 cycles on a full `0–100%` completeness scale.

### Main tables

1. failure-domain / experiment / manipulated-component / endpoint / admissible-interpretation taxonomy;
2. compact FIT run-level summary;
3. mechanism-specific recovery-semantics table preserving exact/censored/upper-bound status.

### Supplement split

Move from main to supplement:
- standalone FIT backlog-drain plot while retaining numerical values in main text/table;
- E0/E4–E11 detailed atlas figures;
- run-validity and anomaly registers;
- detailed provenance/hash tables.

Move to sanitized artifact:
- derived CSVs;
- reconstruction/display scripts;
- non-sensitive manifests;
- releasable evidence only after privacy/security review.

### P18 production and integrity

- Figure 1 = exactly `7.16 in` wide;
- Figures 2–4 = exactly `3.5 in` wide;
- PDF/SVG vector masters;
- PNG fallback = 600 dpi;
- PDF fonts embedded/subset;
- captions and alt text frozen in `manuscript/WP2_P18_FIGURE_CAPTIONS_ALT_TEXT_2026-08-29.md`;
- quantitative percentage plots use full percentage axes to avoid visual exaggeration.

Durable final P18 display pack:
- Drive ID `1tAj83-6rbDEdho9yKdREXU00w6h1pteh`;
- final ZIP SHA-256 `3f5879dbac7493819930157d46980de99efdee37044b6b1ffdb19f04fec395f1`.

`WP2_P18=PASS_MAIN_DISPLAY_REDESIGN_CLAIM_DISPLAY_QA`

`P18_UNSUPPORTED_DISPLAY_CLAIMS=0`

`P18_CROSS_PLATFORM_QUANTITATIVE_POOLING=NONE`

## P18B high-standard benchmark

Cross-publisher benchmark anchors include current IEEE graphics guidance, Elsevier artwork guidance, Nature Portfolio data/code-availability expectations, and ACM-style artifact-evaluation criteria.

Benchmark result:

- P18 main-display checklist coverage: **95.6%**;
- whole publication-package readiness-equivalent: **84%**;
- scientific blockers: `0`.

These percentages are operational checklist-coverage indicators, not acceptance probabilities.

Remaining gold-standard gaps are deliberately assigned to P19/P20:

### P19 — reviewer-facing supplement + sanitized artifact

Target an artifact capable of meeting an ACM-style **Functional** bar and approaching **Reusable**:
- concise reviewer supplement derived from dossier v2.2;
- E0–E11 + FIT ledger + validity/anomaly + timing semantics;
- sanitized derived data supporting public values;
- README/inventory;
- software/hardware environment and dependency lock;
- expected runtimes/resources;
- claim/result → script → output map;
- one-command reproduction path where feasible;
- blank-environment execution receipt;
- explicit private/raw exclusions;
- license only after verified rights decision;
- DOI-capable archive only after release authorization.

### P20 — final literature / venue / credits / rights / source package

Only after P19 PASS:
- submission-date literature search and Gaspar full-text comparison if accessible;
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

## Authorship, affiliation, credits, rights

Canonical current author identity for internal project documents:

**Dr. Ahmed Elsayed Ayoub**  
Assistant Professor of Computer Engineering  
Department of Computer Systems Engineering  
Faculty of Engineering, MSA University  
Giza, Egypt

Do not invent coauthors, CRediT roles, funding, copyright ownership, or licensing terms.

Before submission explicitly verify all authorship, funding, collaborator, institutional/testbed credit, copyright and licensing requirements.

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

`WP2_P18=PASS_MAIN_DISPLAY_REDESIGN_CLAIM_DISPLAY_QA`

`P18B_DISPLAY_BENCHMARK=PASS_95_6_PERCENT_CHECKLIST_COVERAGE`

`P18B_FULL_PACKAGE_READINESS=84_PERCENT_CHECKLIST_COVERAGE`

`LIVE_POWDER_DEPENDENCY=NONE`

`SUBMISSION_AUTHORIZED=NO`

`NEXT_PHASE=WP2_P19_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`
