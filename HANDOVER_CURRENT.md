# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P20B-R2 PASS — national publishing-agreement reweighting**.  
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
- post-P19 consortium WP architecture review: **PASS / FUTURE LANE REFACTORED**
- P20A literature & novelty closure: **PASS / CURRENT NOVELTY-BOUNDARY AUTHORITY**
- P20B original venue qualification: **HISTORICAL / SUPERSEDED FOR RANKING**
- P20B-R1 publisher-neutral venue requalification: **PASS / CURRENT SCOPE-AND-EDITORIAL VENUE AUTHORITY**
- P20B-R2 national publishing-agreement reweighting: **PASS / CURRENT ECONOMIC-AND-ROUTE AUTHORITY**
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
2. `docs/WP2_POST_P19_CONSORTIUM_WP_ARCHITECTURE_REVIEW_2026-08-29.md`
3. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
4. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
5. `analysis/WP2_P12_CROSS_EVIDENCE_INTEGRATION_2026-08-29.md`
6. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
7. `manuscript/WP2_P16_ADVERSARIAL_PUBLICATION_QA_2026-08-29.md`
8. `manuscript/WP2_P16_MANDATORY_EDITORIAL_PATCHES_2026-08-29.md`
9. `docs/WP2_P17_EXPERIMENT_DOSSIER_V2_2_RESEARCH_PACK_2026-08-29.md`
10. `analysis/WP2_P17_EVIDENCE_EXPLOITATION_MATRIX_2026-08-29.md`
11. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`
12. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
13. `manuscript/WP2_P17V_SUPERIOR_INDEPENDENT_CONSORTIUM_VALIDATION_2026-08-29.md`
14. `analysis/WP2_P18R_FIGURE_REQUIREMENTS_SPEC_2026-08-29.md`
15. `manuscript/WP2_P18R_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE_2026-08-29.md`
16. `manuscript/WP2_P18R_F1_HOTFIX_QA_2026-08-29.md`
17. `analysis/WP2_P18R_GENERATOR_RELEASE_RECEIPT_2026-08-29.md`
18. `docs/WP2_P18R_F1_DRIVE_ARCHIVAL_CLOSURE_2026-08-29.md`
19. `analysis/WP2_P18RB_POST_P18R_HIGH_STANDARD_BENCHMARK_2026-08-29.md`
20. `docs/WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION_CLOSURE_2026-08-29.md`
21. `docs/WP2_P19_REVIEWER_SUPPLEMENT_SANITIZED_ARTIFACT_CLOSURE_2026-08-29.md`
22. `analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md`
23. `docs/WP2_P20A_LITERATURE_NOVELTY_CLOSURE_2026-08-29.md`
24. `analysis/WP2_P20B_R1_PUBLISHER_NEUTRAL_VENUE_REQUALIFICATION_2026-08-29.md`
25. `docs/WP2_P20B_R1_PUBLISHER_NEUTRAL_REQUALIFICATION_CLOSURE_2026-08-29.md`
26. `analysis/WP2_P20B_R2_NATIONAL_PUBLISHING_AGREEMENT_REWEIGHTING_2026-08-29.md`
27. `docs/WP2_P20B_R2_NATIONAL_PUBLISHING_AGREEMENT_REWEIGHTING_CLOSURE_2026-08-29.md`
28. Google Sheet `Research & Grants — Lessons Learned Ledger`; publication rules LL-036 through **LL-044** are canonical reusable-experience authority.
29. Original P20B matrix/closure only as historical/superseded comparison.
30. P9 forensic authorities only when exact POWDER trace/caveat semantics are required.
31. P18/P18B only for historical comparison.

## Frozen scientific doctrine

### FIT — architecture-level record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

`B0/W1 × C0/C1/C2 × 3 runs = 18 cells`, exactly 10,000 records/run.

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

### P18RC current production main figures

Archive: `WellPulse_P18RC_Main_Figure_Production_Normalization_2026-08-29.zip`  
Drive ID `1rdFq7ktppFBUp54UoeS5AP3kukDiU9sW`  
SHA-256 `97f0fd1e4c41bb67f6da70056935b60a1627695e082ea8d38eff657bce1d02a8`  
Drive read-back: PASS.

Current PDF SHA-256:
- F1 `7d7feb075731475747282cf0dd0081ec6afb1bc45c17bd16c754063ac83237cb`;
- F2 `73b96a2b8c1fa2a4c15b3bd15b0065f77a2863dcacb84d8c3f2d7d0b57cef508`;
- F3 `faccbef11762df7c293728992e59ac9b17e4b455e4d2023dcddeb50f41e5e9b8`;
- F4 `87d2c703e4308477b3d89c5d0a9594a7380f2e0c8350d5d74721f779785a1b38`.

F1 scientific/topological semantics remain the deterministic hotfix authority.

### P19 reviewer supplement + sanitized artifact

Archive: `WellPulse_P19_Reviewer_Supplement_Sanitized_Artifact_2026-08-29.zip`  
Drive ID `1t5S_L-S0hfmyMPLdXh8Fd-jGBOH8SCkl`  
SHA-256 `5a9ed4fa197ea5c3aa43447fabf16d7928aeabe58722e16af63afe25bc7cfdc7`  
Drive read-back: PASS.

P19 includes reviewer-facing FIT + E0–E11 atlas, sanitized validity/anomaly register, derived non-sensitive CSVs, P13 claim map, P18RC figures/alt text, analysis/rebuild code, claim→script→output map, standard-library self-check, dependency record, privacy/security review and manifests.

Independent recheck: manifest `54/54` PASS; isolated `python -I artifact_selfcheck.py` PASS; scientific reopening required NO.

Non-blocking packaging exception: two `__pycache__/*.pyc` files must be excluded from the final external package during P20D/P20E.

## P20A — current novelty authority

- material P17 literature/testbed/technical anchors: **11/11 verified**;
- closest new comparator: Mohammed et al. 2026, DOI `10.48084/etasr.16945`;
- action: **WORDING NARROWING ONLY**;
- E-MQTT (2023) constrains receiver-confirmation priority wording;
- Radwan et al. 2026 Scientific Reports DOI `10.1038/s41598-026-66865-8` has no collision with the frozen claim envelope;
- Gaspar et al. DOI `10.1109/MIOT.2026.3681190` remains bibliographic-only for detailed attribution unless full text is directly recovered;
- final defensible contribution is the compound failure-domain-aware evaluation structure and bounded evidence package, not persistence/store-and-forward/end-to-end-confirmation historical novelty.

P20D later must add Mohammed et al. 2026, account for E-MQTT and Radwan et al. 2026, and preserve all P20A wording constraints.

## P20B-R1 — publisher-neutral scope/editorial authority

R1 corrected the original Elsevier-concentrated search. Serious current publisher families were screened, including IEEE, ACM, Elsevier and Springer Nature.

Scope/editorial ranking before national-agreement economics:

1. **IEEE Internet of Things Journal** — primary specialist GO;
2. **Internet of Things (Elsevier)** — strong specialist GO;
3. **ACM Transactions on Internet of Things** — strong scientific GO, cost/institutional gate;
4. **IEEE Transactions on Network and Service Management** — conditional GO;
5. **Computer Networks** — lower-priority GO;
6. **IEEE Open Journal of the Communications Society** — technical GO / economic hold;
7. **Journal of Systems Architecture** — conditional;
8. **Journal of Network and Systems Management** — hold because management emphasis is required.

ESWA and EAAI remain killed for the current frozen manuscript.

IEEE IoT-J is a direct match for IoT architecture, embedded software, networking, and testbeds/trials. If selected later, P20D must run a lossless IEEE-format/page-count simulation before commitment because overlength charges may apply and destructive compression is prohibited.

## P20B-R2 — national publishing-agreement authority

R2 adds current national/institutional OA economics without changing science.

### Verified Springer Nature / STDF / EKB coverage

- current agreement runs through **2029-12-31**;
- **October University for Modern Sciences and Arts** is explicitly listed as participating;
- eligible corresponding authors may receive OA publication-fee coverage subject to STDF/EKB eligibility verification and approval;
- corresponding-author and primary-affiliation conditions apply;
- the majority-of-research / article-type / journal-family rules must be satisfied;
- **Scientific Reports** is explicitly included in current agreement guidance;
- recent MSA Springer Nature papers demonstrate that STDF/EKB OA publication funding is operational in practice.

Important distinction: **publication-fee coverage is not research funding**. Do not state that STDF/EKB funded the WellPulse research unless independent evidence supports that. At most, if later approved, record publication/OA funding in the publisher-required metadata.

### Current multi-objective route strategy

Do not collapse the choice into one scalar ranking without stating the author's objective.

**Specialist / IEEE route:**  
`IEEE Internet of Things Journal` — strongest specialist scholarly home and current primary when domain fit/IEEE visibility dominate.

**Agreement-advantaged speed / zero-expected-APC route:**  
`Scientific Reports` — co-primary strategic route when acceptance plausibility, broad legitimacy, speed, package reuse, and verified Springer Nature national OA coverage dominate. Article-level funding remains conditional on STDF/EKB approval.

**Specialist fallback:**  
`Internet of Things (Elsevier)` — direct fit; subscription route avoids mandatory OA; no broad national MSA APC-free Elsevier publishing agreement has been verified.

**Springer specialist fallback:**  
`Telecommunication Systems` — agreement-advantaged specialist alternative; still lower direct IoT-resilience readership fit than IEEE IoT-J / Elsevier Internet of Things.

Additional publisher-agreement state:

- Taylor & Francis: EKB OA-agreement existence verified; exact MSA/article/journal-level coverage remains unresolved and must be checked before use;
- Elsevier: EKB access/research-tool partnership verified; broad national APC-free publishing for MSA not verified;
- IEEE: no national MSA/SCU/EKB APC waiver verified; database access/subscription must never be treated as a publishing waiver.

`P20B_R2_CO_PRIMARY_SPECIALIST=IEEE_INTERNET_OF_THINGS_JOURNAL`

`P20B_R2_CO_PRIMARY_ZERO_APC_SPEED=SCIENTIFIC_REPORTS`

`P20B_R2_SPECIALIST_BACKUP=ELSEVIER_INTERNET_OF_THINGS`

`P20B_R2_SPRINGER_SPECIALIST_BACKUP=TELECOMMUNICATION_SYSTEMS`

`P20B_R2_AUTHOR_COMMITMENT=NO`

`P20B_R2_PAYMENT_AUTHORIZED=NO`

## Refactored remaining publication lane

Authority: `docs/WP2_POST_P19_CONSORTIUM_WP_ARCHITECTURE_REVIEW_2026-08-29.md`.

1. **P20A — Literature & Novelty Closure — 15% — PASS**
2. **P20B / R1 / R2 — Venue Qualification, Publisher-Neutral Requalification & Agreement Reweighting — 15% — PASS**
3. **P20C — Authorship / Credits / Rights Lock — 15% — NOT STARTED**
4. **P20D — Final Manuscript & Source Package Integration — 25% — LOCKED**
5. **P20E — Independent Submission-Readiness Validation — 20% — LOCKED**
6. **P21 — Author Submission Authorization Packet — 5% — LOCKED**
7. **P22 — Submission Execution & Receipt — 5% — LOCKED**

Remaining-lane earned progress: **30/100**.

P20D–P22 remain dependency-locked. P20C is the only next executable gate and requires current authorization.

## Exact next gate — DO NOT EXECUTE WITHOUT CURRENT AUTHORIZATION

### WP2-P20C — AUTHORSHIP / CREDITS / RIGHTS LOCK

P20C must verify from canonical project records and user-controlled evidence where needed:

- exact author list and order;
- corresponding-author identity;
- whether the corresponding-author / MSA affiliation arrangement preserves Springer Nature STDF/EKB eligibility if that route remains live;
- CRediT contributions;
- exact affiliation wording;
- research-funding statement separately from possible publication/OA funding;
- conflict-of-interest declaration basis;
- FIT IoT-LAB / POWDER / institutional / collaborator acknowledgments;
- rights/permissions status of figures, data, software and externally sourced material;
- supportable license/public-release statements.

P20C must not invent a coauthor, contribution, funder, permission, license, waiver, institutional approval or conflict statement. It must separate verified fact from `UNKNOWN / AUTHOR INPUT REQUIRED`.

P20C does not perform final venue formatting/source integration, portal submission, license acceptance, OA purchase or payment.

## Immutable prohibitions

Do not claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB threshold; deterministic RF-only recovery; exact broker latency from E10-D; population reliability from message counts or three FIT runs; pooled FIT+POWDER inference; historical firstness for persistence/store-and-forward/end-to-end confirmation; or unsupported field/rural/Siwa/pump/hydraulic/groundwater/agronomic/industrial-process validation.

## Stop state

`WP2_P18RC=PASS_MAIN_FIGURE_PRODUCTION_NORMALIZATION`

`WP2_P19=PASS_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`

`POST_P19_WP_ARCHITECTURE_REVIEW=PASS`

`WP2_P20A=PASS_LITERATURE_AND_NOVELTY_CLOSURE`

`P20A_SCIENTIFIC_BLOCKERS=0`

`WP2_P20B_ORIGINAL=HISTORICAL_SUPERSEDED_FOR_RANKING`

`WP2_P20B_R1=PASS_PUBLISHER_NEUTRAL_REQUALIFICATION`

`WP2_P20B_R2=PASS_NATIONAL_PUBLISHING_AGREEMENT_REWEIGHTING`

`MSA_SPRINGER_NATURE_OA_AGREEMENT=VERIFIED_ACTIVE_TO_2029_12_31`

`P20B_R2_CO_PRIMARY_SPECIALIST=IEEE_INTERNET_OF_THINGS_JOURNAL`

`P20B_R2_CO_PRIMARY_ZERO_APC_SPEED=SCIENTIFIC_REPORTS`

`P20B_R2_SPECIALIST_BACKUP=ELSEVIER_INTERNET_OF_THINGS`

`P20B_R2_SPRINGER_SPECIALIST_BACKUP=TELECOMMUNICATION_SYSTEMS`

`P20B_AUTHOR_COMMITMENT=NO`

`P20C_LOCK_RELEASED=YES`

`P18RC_REOPEN=NO`

`P19_REOPEN_SCIENCE=NO`

`P19_PACKAGING_EXCEPTION=NON_BLOCKING_PYCACHE_REMOVE_BEFORE_EXTERNAL_PACKAGE`

`CURRENT_SCIENTIFIC_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

`NEW_EMPIRICAL_CLAIM_REQUIRED=NO`

`LIVE_POWDER_DEPENDENCY=NONE`

`P20_MONOLITHIC_EXECUTION=REJECTED`

`CURRENT_PHASE=WP2_P20C_GATE_NOT_STARTED`

`SUBMISSION_AUTHORIZED=NO`
