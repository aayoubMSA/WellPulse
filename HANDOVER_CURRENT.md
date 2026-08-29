# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P19 PASS**.  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the canonical operational retrieval point. GitHub is the scientific/control/source record; Google Drive is the durable authority for frozen/raw binary evidence and registered research packs. Repository/Drive evidence overrides chat memory.

## Executive state

- P8 manual POWDER campaign: **COMPLETE / GOLDEN / MANUAL REFERENCE**
- P9 forensic reconciliation: **PASS**
- P10 scientific analysis contract: **PASS / FROZEN**
- P11 full raw-data scientific analysis: **PASS**
- P12 cross-evidence integration: **PASS**
- P13 claim–evidence matrix: **PASS / FROZEN CLAIM AUTHORITY**
- P14/P15: **PASS / HISTORICAL DISPLAY + DRAFT**
- P16 adversarial publication QA: **PASS**
- P17 consortium manuscript + dossier: **PASS**
- P17V independent validation: **PASS / VALIDATED WITH PRE-SUBMISSION CONDITIONS**
- P18/P18B: **HISTORICAL / SUPERSEDED**
- P18R scientific figure engineering: **PASS**
- P18R deterministic F1 hotfix: **PASS / SCIENTIFIC-TOPOLOGY AUTHORITY**
- P18RB benchmark: **CONDITIONAL PASS / SCIENCE PASS / PRODUCTION NORMALIZATION REQUIRED**
- P18RC main-figure production normalization: **PASS / CURRENT PRODUCTION MAIN-DISPLAY AUTHORITY**
- P19 reviewer supplement + sanitized artifact: **PASS / CURRENT REVIEWER-ARTIFACT AUTHORITY**
- current scientific blockers: **0**
- new experiment required: **NO**
- new empirical claim required: **NO**
- live POWDER dependency: **NONE**
- submission authorization: **NO**

Historical scored state is unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8+ result may be promoted or relabelled as scored P7B.

## Mandatory read order

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
20. `docs/WP2_P19_REVIEWER_SUPPLEMENT_SANITIZED_ARTIFACT_CLOSURE_2026-08-29.md`
21. P9 forensic authorities when exact POWDER trace/caveat semantics are required.
22. P18/P18B only for historical comparison.

## Frozen scientific doctrine

### FIT — architecture-level record-state survival
Authority: `FINAL_WP_RT01_FIT_A8`.

`B0/W1 × C0/C1/C2 × 3 runs = 18 cells`, 10,000 records/run.

- C0 B0/W1 = 100% all runs;
- C1 B0 = 80%, W1 = 100% all runs;
- C2 B0 = 80%, W1 = 100% all runs;
- B0 C1/C2 permanently miss exactly 2,000 records/run;
- W1 final reconciliation contains all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`.

These are run-level repeated outcomes under exact treatments, not population reliability probabilities. C2 is gateway-process `exec` restart, not node reboot. B0 is non-durable and is not the strongest durable MQTT comparator.

### POWDER — communication-path degradation/recovery characterization
Campaign `WP2-P8`, profile `srslte-controlled-rf`.

Role: separately executed physical-RF/LTE/MQTT controlled reference characterization; **not architecture-effect estimation**.

- E1/E2/E3 = experiment-specific transition region; 52 dB is not universal;
- E8 isolates broker/service failure while LTE remains healthy;
- E9 = no-fault control;
- E10 preserves exact/censored/upper-bound semantics;
- E10-A = no scalar recovery latency;
- E10-D = upper bound only;
- receiver-side unique-ID reconciliation governs reported delivery.

FIT and POWDER are complementary and non-substitutable. No pooled FIT+POWDER reliability statistic, CI, p-value, or inferential effect is allowed.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Manuscript baseline

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`

Title: **WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

P17V: claims `9/9` validated; numerical contradictions `0`; unsupported new claims `0`; scientific blockers `0`; new experiment required `NO`.

Never generalize the FIT result into generic MQTT superiority.

## Durable Drive authorities

Parent research folder: `P12_WellPulse` / `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`.

### P17 dossier
- PDF Drive ID `12ec22A89ybsNoBpYcglx9Im6pW8Vk55-`, SHA-256 `a9274514cbf21de58291c2640f560f6082711e0a8696890419e918e595b40f3e`;
- reproducible package `1ts__z8kN0fORwDksQZoj4eeaG--UyCAw`;
- experiment figure suite `1y8rStzWdGEivWjuFCP0h5Y6Amv6267sY`;
- figure QA report `1ukEvwr3_uOoZcCn3TknwOcZL6HRaLo1a`.

Raw FIT/POWDER frozen archives remain higher measurement authorities.

### Historical P18R release
`WellPulse_P18R_Scientific_Figure_Engineering_Release_2026-08-29.zip` — Drive `1alitbv9479Mq9URhXIBHkQql7zuuA51o`, SHA-256 `5586091bc518cc541c3c9b75e9a0c965913877cd6bf83d1644fa6f05264e1083`.

### Deterministic F1 hotfix
Pre-normalization generator `analysis/wp2_p18r_generate_f1_hotfix.py`, blob `bf344808414b78d9b0c688140e9de9a755d9a1e7`, SHA-256 `3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`; pre-normalization PDF SHA-256 `4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`. Archive Drive `12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M`, read-back PASS.

### P18RC current production main figures
Closure: `docs/WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION_CLOSURE_2026-08-29.md`.

Archive: `WellPulse_P18RC_Main_Figure_Production_Normalization_2026-08-29.zip`  
Drive ID `1rdFq7ktppFBUp54UoeS5AP3kukDiU9sW`  
SHA-256 `97f0fd1e4c41bb67f6da70056935b60a1627695e082ea8d38eff657bce1d02a8`  
Drive read-back: PASS.

Current PDF SHA-256:
- F1 `7d7feb075731475747282cf0dd0081ec6afb1bc45c17bd16c754063ac83237cb`;
- F2 `73b96a2b8c1fa2a4c15b3bd15b0065f77a2863dcacb84d8c3f2d7d0b57cef508`;
- F3 `faccbef11762df7c293728992e59ac9b17e4b455e4d2023dcddeb50f41e5e9b8`;
- F4 `87d2c703e4308477b3d89c5d0a9594a7380f2e0c8350d5d74721f779785a1b38`.

P18RC: F2 semantic cleanup PASS; embedded Arial-compatible sans PASS; grids/ordinary strokes normalized; F1–F4 alt text frozen; grayscale PASS; metadata normalized; zero known clipping/overlap/crossing; two-build 12/12 hash equality PASS. F1 scientific/topological semantics remain the deterministic hotfix authority.

### P19 reviewer supplement + sanitized artifact
Closure: `docs/WP2_P19_REVIEWER_SUPPLEMENT_SANITIZED_ARTIFACT_CLOSURE_2026-08-29.md`.

Archive: `WellPulse_P19_Reviewer_Supplement_Sanitized_Artifact_2026-08-29.zip`  
Drive ID `1t5S_L-S0hfmyMPLdXh8Fd-jGBOH8SCkl`  
SHA-256 `5a9ed4fa197ea5c3aa43447fabf16d7928aeabe58722e16af63afe25bc7cfdc7`  
Drive read-back: PASS.

P19 includes reviewer-facing FIT + E0–E11 atlas, sanitized validity/anomaly register, derived non-sensitive CSVs, P13 claim map, P18RC figures/alt text, analysis/rebuild code, claim→script→output map, standard-library self-check, dependency record, privacy/security review and manifests.

Privacy boundary: private raw archives, credential-bearing material, unclassified screenshots, secrets/tokens and testbed-credential files are excluded. E11 exact RFC1918 session addresses were replaced with `session address changed`; the transition fact and one-sided-collector caveat remain. Standard-library self-check PASS; F2–F4 sanitized-data rebuild PASS.

## Exact next gate — DO NOT EXECUTE WITHOUT CURRENT AUTHORIZATION

### WP2-P20 — FINAL LITERATURE / VENUE / SOURCE PACKAGE / CREDITS / RIGHTS NORMALIZATION

P20 must handle:
- final submission-date literature verification, including Gaspar et al. full-text comparison if accessible;
- target-journal selection/verification and venue-specific formatting;
- final manuscript source package;
- final author list/order and CRediT roles;
- affiliation wording;
- funding/COI;
- collaborator acknowledgments;
- FIT IoT-LAB and POWDER acknowledgment/citation wording;
- copyright/license/permissions and artifact-release terms;
- final proof QA;
- explicit submission authorization gate.

Submission remains **NOT AUTHORIZED**.

## Immutable prohibitions

Do not claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB threshold; deterministic RF-only recovery; exact broker latency from E10-D; population reliability from message counts or three FIT runs; pooled FIT+POWDER inference; or unsupported field/rural/Siwa/pump/hydraulic/groundwater/agronomic/industrial-process validation.

## Stop state

`WP2_P18RC=PASS_MAIN_FIGURE_PRODUCTION_NORMALIZATION`

`WP2_P19=PASS_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`

`P19_PRIVACY_SECURITY_REVIEW=PASS`

`P19_STDLIB_SELFCHECK=PASS`

`P19_QUANTITATIVE_REBUILD=PASS`

`P19_DRIVE_ARCHIVE=PASS`

`P19_DRIVE_READBACK_HASH=PASS`

`CURRENT_SCIENTIFIC_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

`LIVE_POWDER_DEPENDENCY=NONE`

`SUBMISSION_AUTHORIZED=NO`

`CURRENT_PHASE=WP2_P20_GATE_NOT_STARTED`
