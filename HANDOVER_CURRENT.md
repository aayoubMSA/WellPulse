# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P18RC PASS**.  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the canonical operational retrieval point. GitHub is the scientific/control/source record; Google Drive is the durable authority for frozen/raw binary evidence and registered research packs. Repository/Drive evidence overrides chat memory.

## Executive state

- WP2-P8 manual POWDER campaign: **COMPLETE / GOLDEN / MANUAL REFERENCE**
- WP2-P9 forensic reconciliation: **PASS / COMPLETE**
- WP2-P10 scientific analysis contract: **PASS / FROZEN**
- WP2-P11 full raw-data scientific analysis: **PASS / COMPLETE**
- WP2-P12 cross-evidence integration: **PASS / COMPLETE**
- WP2-P13 claim–evidence matrix: **PASS / FROZEN CLAIM AUTHORITY**
- WP2-P14: **PASS / HISTORICAL DISPLAY SET**
- WP2-P15: **PASS / HISTORICAL INTERNAL FULL DRAFT**
- WP2-P16: **PASS / ADVERSARIAL PUBLICATION QA**
- WP2-P17: **PASS / CONSORTIUM-REVISED INTERNAL MANUSCRIPT + DOSSIER RESEARCH PACK**
- WP2-P17V: **PASS / VALIDATED WITH PRE-SUBMISSION CONDITIONS**
- WP2-P18 first redesign: **SUPERSEDED BY P18R**
- WP2-P18B: **HISTORICAL PRE-P18R BENCHMARK**
- WP2-P18R scientific figure engineering: **PASS**
- P18R deterministic F1 hotfix: **PASS / SCIENTIFIC-TOPOLOGY AUTHORITY**
- WP2-P18RB benchmark: **CONDITIONAL PASS / SCIENCE PASS / PRODUCTION NORMALIZATION REQUIRED**
- WP2-P18RC main-figure production normalization: **PASS / CURRENT PRODUCTION MAIN-DISPLAY AUTHORITY**
- current scientific blockers: **0**
- new experiment required: **NO**
- new empirical claim required: **NO**
- live POWDER dependency: **NONE**
- submission authorization: **NO**

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
10. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`
11. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
12. `manuscript/WP2_P17V_SUPERIOR_INDEPENDENT_CONSORTIUM_VALIDATION_2026-08-29.md`
13. `analysis/WP2_P18R_FIGURE_REQUIREMENTS_SPEC_2026-08-29.md`
14. `manuscript/WP2_P18R_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE_2026-08-29.md`
15. `manuscript/WP2_P18R_F1_HOTFIX_QA_2026-08-29.md`
16. `analysis/WP2_P18R_GENERATOR_RELEASE_RECEIPT_2026-08-29.md`
17. `docs/WP2_P18R_F1_DRIVE_ARCHIVAL_CLOSURE_2026-08-29.md`
18. `analysis/WP2_P18RB_POST_P18R_HIGH_STANDARD_BENCHMARK_2026-08-29.md`
19. `docs/WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION_CLOSURE_2026-08-29.md`
20. P9 forensic authorities when exact POWDER trace/caveat semantics are required.
21. P18/P18B only for historical comparison.

## Frozen evidence roles

### FIT — architecture-level record-state survival
Authority: `FINAL_WP_RT01_FIT_A8`.

Design: `B0/W1 × C0/C1/C2 × 3 runs = 18 cells`, exactly 10,000 records/run.

Frozen outcome:
- C0: B0/W1 = 100% all runs;
- C1: B0 = 80%, W1 = 100% all runs;
- C2: B0 = 80%, W1 = 100% all runs;
- B0 C1/C2 permanently miss exactly 2,000 records/run;
- W1 final reconciliation has all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`.

These are repeated run-level outcomes under the exact treatments, not population reliability probabilities. C2 is gateway-process `exec` restart, not node reboot.

### POWDER — communication-path degradation/recovery characterization
Campaign: `WP2-P8`, profile `srslte-controlled-rf`.

Publication role: **separately executed physical-RF/LTE/MQTT controlled reference characterization; not architecture-effect estimation**.

Frozen interpretation:
- E1/E2/E3 characterize an experiment-specific transition region;
- 52 dB is not a universal threshold;
- E8 separates broker/service failure from healthy LTE connectivity;
- E9 is the no-fault control;
- E10 preserves exact/censored/upper-bound timing semantics;
- E10-A has no scalar recovery latency;
- E10-D is upper-bound only;
- receiver-side unique-ID reconciliation governs reported delivery where sender/receiver records disagree.

## Frozen integration doctrine

FIT and POWDER are complementary and non-substitutable:
- FIT = record-state survival / bounded architecture comparison;
- POWDER = communication-path degradation and recovery characterization.

No pooled FIT+POWDER reliability statistic or inferential effect is allowed. P13 remains the claim authority. P17/P17V/P18R/P18RB/P18RC add no new empirical claims and do not expand the P13 envelope.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Current manuscript baseline

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`

Working title: **WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

P17V: **VALIDATED WITH PRE-SUBMISSION CONDITIONS**; claims `9/9`; numerical contradictions `0`; unsupported new claims `0`; scientific blockers `0`; new experiment required `NO`.

B0 remains explicitly non-durable and is not the strongest durable MQTT comparator. Never generalize the FIT result into generic MQTT superiority.

## Durable Drive authorities

### P17 dossier/research pack
Parent folder ID: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`

- dossier PDF `WellPulse_Experimental_Technical_Dossier_v2.2.pdf` — Drive ID `12ec22A89ybsNoBpYcglx9Im6pW8Vk55-`, SHA-256 `a9274514cbf21de58291c2640f560f6082711e0a8696890419e918e595b40f3e`;
- reproducible dossier package — Drive ID `1ts__z8kN0fORwDksQZoj4eeaG--UyCAw`;
- experiment figure suite — Drive ID `1y8rStzWdGEivWjuFCP0h5Y6Amv6267sY`;
- figure-centered QA report — Drive ID `1ukEvwr3_uOoZcCn3TknwOcZL6HRaLo1a`.

Raw FIT and POWDER frozen archives remain higher measurement authorities than the dossier.

### Historical P18R full figure release
`WellPulse_P18R_Scientific_Figure_Engineering_Release_2026-08-29.zip` — Drive ID `1alitbv9479Mq9URhXIBHkQql7zuuA51o`, SHA-256 `5586091bc518cc541c3c9b75e9a0c965913877cd6bf83d1644fa6f05264e1083`.

### P18R deterministic F1 hotfix
Canonical pre-normalization generator: `analysis/wp2_p18r_generate_f1_hotfix.py`; Git blob `bf344808414b78d9b0c688140e9de9a755d9a1e7`; SHA-256 `3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`.

Pre-normalization F1 PDF SHA-256: `4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`.

Archive `WellPulse_P18R_F1_Hotfix_Final_2026-08-29.zip` — Drive ID `12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M`, ZIP SHA-256 `e9d5a54b24506b879a748b5a06b39699e6f6ec1ed31093491c27b2be7d7e6e1d`; Drive read-back PASS.

### P18RC current production-normalized main set
Canonical closure: `docs/WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION_CLOSURE_2026-08-29.md`.

Archive: `WellPulse_P18RC_Main_Figure_Production_Normalization_2026-08-29.zip`  
Drive ID: `1rdFq7ktppFBUp54UoeS5AP3kukDiU9sW`  
ZIP SHA-256: `97f0fd1e4c41bb67f6da70056935b60a1627695e082ea8d38eff657bce1d02a8`  
Drive read-back hash: **PASS / exact match**.

Current normalized PDF SHA-256:
- F1 `7d7feb075731475747282cf0dd0081ec6afb1bc45c17bd16c754063ac83237cb`;
- F2 `73b96a2b8c1fa2a4c15b3bd15b0065f77a2863dcacb84d8c3f2d7d0b57cef508`;
- F3 `faccbef11762df7c293728992e59ac9b17e4b455e4d2023dcddeb50f41e5e9b8`;
- F4 `87d2c703e4308477b3d89c5d0a9594a7380f2e0c8350d5d74721f779785a1b38`.

P18RC QA: F2 accidental/default color semantics removed; typography normalized to embedded Arial-compatible sans; nonessential quantitative grids removed; ordinary Matplotlib strokes <=1 pt; explicit F1–F4 alt text frozen; grayscale/non-color-only interpretation PASS; file metadata normalized; zero known clipping/overlap/crossing; two independent builds yielded identical hashes for all 12 PDF/SVG/PNG assets.

P18RC is production-only. F1 scientific/topological authority remains the deterministic hotfix semantics; P18RC changes typography/metadata/encoding discipline only.

## Exact next gate

### WP2-P19 — REVIEWER-FACING SUPPLEMENT + SANITIZED ARTIFACT

P19 should package:
- reviewer-facing E0–E11 atlas;
- FIT full run ledger;
- run-validity and anomaly evidence;
- endpoint semantics;
- analysis code and derived non-sensitive data;
- P18RC normalized figures/captions/alt text;
- claim/result → script → output map;
- manifests, hashes and dependency/runtime documentation;
- explicit public/private evidence boundary and privacy/security review;
- blank-environment/reviewer exercisability where feasible.

P19 must not expose credential-bearing/private preservation material. P20 remains responsible for final literature/venue/source-package/credits/rights normalization and explicit submission authorization.

## Authorship / credits / rights guard

Do not invent coauthors, CRediT roles, funding, copyright ownership, or licensing terms. Before external submission/release, verify final author list/order, CRediT roles, affiliation wording, funding/COI, collaborator acknowledgments, FIT IoT-LAB and POWDER acknowledgment/citation, and venue/institution/testbed copyright-license requirements.

## Immutable prohibitions

Do not claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB threshold; deterministic RF-only recovery; exact broker latency from E10-D; population reliability from message counts or three FIT runs; pooled FIT+POWDER inference; or unsupported field/rural/Siwa/pump/hydraulic/groundwater/agronomic/industrial-process validation.

## Stop state

`WP2_P18R=PASS_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE`

`P18R_F1_HOTFIX=PASS_DETERMINISTIC_F1_ACCEPTED`

`WP2_P18RB=CONDITIONAL_PASS_SCIENCE_PASS_PRODUCTION_NORMALIZATION_REQUIRED`

`WP2_P18RC=PASS_MAIN_FIGURE_PRODUCTION_NORMALIZATION`

`P18RC_DRIVE_ARCHIVE=PASS`

`P18RC_DRIVE_READBACK_HASH=PASS`

`P18RC_DETERMINISTIC_12_OF_12=PASS`

`CURRENT_SCIENTIFIC_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

`LIVE_POWDER_DEPENDENCY=NONE`

`SUBMISSION_AUTHORIZED=NO`

`CURRENT_PHASE=WP2_P19_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`
