# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P20B-R1 PASS — publisher-neutral venue requalification**.  
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
- P20B original venue qualification: **HISTORICAL / SUPERSEDED FOR RANKING — PUBLISHER-COVERAGE BIAS**
- P20B-R1 publisher-neutral venue requalification: **PASS / CURRENT VENUE AUTHORITY / AUTHOR COMMITMENT NOT MADE**
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
22. `handover/AGENT_MANDATE_WP2_P20A_2026-08-29.md`
23. `analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md`
24. `docs/WP2_P20A_LITERATURE_NOVELTY_CLOSURE_2026-08-29.md`
25. `analysis/WP2_P20B_R1_PUBLISHER_NEUTRAL_VENUE_REQUALIFICATION_2026-08-29.md`
26. `docs/WP2_P20B_R1_PUBLISHER_NEUTRAL_REQUALIFICATION_CLOSURE_2026-08-29.md`
27. Google Sheet `Research & Grants — Lessons Learned Ledger` before venue/submission-facing decisions; publication rules LL-036 through LL-043 are canonical reusable-experience authority.
28. Original P20B matrix/closure only as historical/superseded comparison.
29. P9 forensic authorities only when exact POWDER trace/caveat semantics are required.
30. P18/P18B only for historical comparison.

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

Independent consortium recheck after closure:
- archive hash exact match: PASS;
- manifest `54/54`: PASS;
- isolated `python -I artifact_selfcheck.py`: PASS;
- scientific reopening required: NO.

Non-blocking packaging hygiene exception: two `__pycache__/*.pyc` files are present in the current P19 archive. No obvious credential/privacy/scientific leak was identified, but compiled-cache files must be excluded from the final externally distributed package during P20D/P20E.

## P20A current novelty-boundary authority

Closure: `docs/WP2_P20A_LITERATURE_NOVELTY_CLOSURE_2026-08-29.md`.  
Comparator matrix: `analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md`.

P20A current-search result:

- material P17 literature/testbed/technical anchors: **11/11 verified**;
- closest newly identified conceptual comparator: Mohammed et al. 2026, DOI `10.48084/etasr.16945`;
- material action: **WORDING NARROWING ONLY**;
- no novelty claim is permitted for generic persistence, disk-backed buffering, retransmission, store-and-forward, offline-first continuity, application/database acknowledgment, end-to-end subscriber confirmation, testbed repeatability, or historical priority for decoupling data reliability from network availability;
- E-MQTT (2023) constrains receiver-confirmation priority wording;
- Radwan et al. (Scientific Reports, 17 Aug 2026, DOI `10.1038/s41598-026-66865-8`) is current load/congestion MQTT reliability prior work with no collision to the frozen claim envelope;
- Gaspar et al. DOI `10.1109/MIOT.2026.3681190` is bibliographically verified; a current author page advertises a PDF, but the full text was not recovered through the available retrieval channel, so detailed method/result attribution remains prohibited;
- final defensible contribution is the **compound failure-domain-aware evaluation structure and bounded evidence package**, not historical uniqueness of persistence/store-and-forward/reconciliation ingredients.

P20D later must add Mohammed et al. 2026, account for E-MQTT and Radwan et al. 2026, and preserve the P20A wording constraints.

## P20B-R1 current venue authority

Current decision matrix: `analysis/WP2_P20B_R1_PUBLISHER_NEUTRAL_VENUE_REQUALIFICATION_2026-08-29.md`.  
Current closure: `docs/WP2_P20B_R1_PUBLISHER_NEUTRAL_REQUALIFICATION_CLOSURE_2026-08-29.md`.

The original P20B matrix/closure are **historical/superseded for ranking** because the candidate universe was too Elsevier-concentrated.

Current publisher-neutral recommendation:

1. **IEEE Internet of Things Journal** — **PRIMARY / GO**;
2. **Internet of Things (Elsevier)** — **BACKUP #1 / GO**;
3. **ACM Transactions on Internet of Things** — **BACKUP #2 / GO subject to institutional/APC cost gate**;
4. **IEEE Transactions on Network and Service Management** — **BACKUP #3 / CONDITIONAL GO**;
5. **Computer Networks** — **GO / LOWER PRIORITY**;
6. **IEEE Open Journal of the Communications Society** — **TECHNICAL GO / ECONOMIC HOLD**;
7. **Journal of Systems Architecture** — **CONDITIONAL GO**;
8. **Journal of Network and Systems Management** — **HOLD**.

ESWA and EAAI remain killed for the current frozen manuscript.

Why IEEE IoT-J leads now:

- direct fit to IoT architecture, embedded software, communication/networking protocols, IoT services and testbeds/trials/experiments;
- current recent publications include MQTT-centered and resilience/testbed work;
- official journal material reports average first decision around 6.9 weeks and submission-to-ePublication around 14.5 weeks;
- traditional publication is possible without an OA APC;
- author preference for IEEE is compatible with, not overriding, the scientific fit.

Main IEEE IoT-J constraint: mandatory overlength charge currently applies beyond 8 published pages. If the author later selects IoT-J, P20D must conduct a lossless IEEE two-column/page-count simulation before any submission commitment. If fitting near the threshold would materially damage evidence, caveats, figure legibility or novelty discipline, the fallback is Elsevier Internet of Things rather than destructive compression.

ACM TIOT is a very strong scientific match for end-to-end architecture, dependability/robustness, testbeds and strong experimental evidence, but 2026 ACM Open institutional/APC status must be verified before commitment.

IEEE TNSM is viable for reliability/fault/performance evaluation but is narrower around network/service management. IEEE OJ-COMS is technically strong but its fully OA 2026 APC creates an economic hold absent confirmed coverage.

P20B-R1 makes **no author venue commitment** and authorizes no portal action, copyright/license acceptance, APC/payment, or submission.

`P20B_R1_PRIMARY_RECOMMENDATION=IEEE_INTERNET_OF_THINGS_JOURNAL`

`P20B_R1_BACKUP_1=ELSEVIER_INTERNET_OF_THINGS`

`P20B_R1_BACKUP_2=ACM_TRANSACTIONS_ON_INTERNET_OF_THINGS_COST_GATE`

`P20B_R1_BACKUP_3=IEEE_TNSM_CONDITIONAL`

`P20B_R1_AUTHOR_COMMITMENT=NO`

## Refactored remaining publication lane

Authority: `docs/WP2_POST_P19_CONSORTIUM_WP_ARCHITECTURE_REVIEW_2026-08-29.md`.

P20 remains an **umbrella only**. Monolithic P20 execution is rejected. Execute one bounded gate at a time:

1. **P20A — Literature & Novelty Closure — 15% — PASS**
2. **P20B / P20B-R1 — Venue Qualification & Publisher-Neutral Requalification — 15% — PASS**
3. **P20C — Authorship / Credits / Rights Lock — 15% — NOT STARTED**
4. **P20D — Final Manuscript & Source Package Integration — 25% — LOCKED**
5. **P20E — Independent Submission-Readiness Validation — 20% — LOCKED**
6. **P21 — Author Submission Authorization Packet — 5% — LOCKED**
7. **P22 — Submission Execution & Receipt — 5% — LOCKED**

Remaining-lane earned progress from the post-P19 refactor baseline: **30/100**.

P20D–P22 remain dependency-locked. P20C is the only next executable gate and requires current authorization.

## Exact next gate — DO NOT EXECUTE WITHOUT CURRENT AUTHORIZATION

### WP2-P20C — AUTHORSHIP / CREDITS / RIGHTS LOCK

P20C must verify, from canonical project records and user-controlled evidence where needed:

- exact author list and order;
- corresponding-author identity;
- CRediT contributions;
- affiliation wording;
- funding statements;
- conflict-of-interest declaration basis;
- FIT IoT-LAB / POWDER / institutional / collaborator acknowledgments;
- rights/permissions status of figures, data, software and externally sourced material;
- which license/public-release statements are actually supportable.

P20C must not invent a coauthor, contribution, funder, permission, license, waiver, institutional approval or conflict statement. It must separate verified fact from `UNKNOWN / AUTHOR INPUT REQUIRED`.

P20C does not perform final venue formatting/source integration, portal submission, license acceptance, OA purchase or payment.

## Immutable prohibitions

Do not claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB threshold; deterministic RF-only recovery; exact broker latency from E10-D; population reliability from message counts or three FIT runs; pooled FIT+POWDER inference; historical firstness for persistence/store-and-forward/end-to-end confirmation; or unsupported field/rural/Siwa/pump/hydraulic/groundwater/agronomic/industrial-process validation.

## Stop state

`WP2_P18RC=PASS_MAIN_FIGURE_PRODUCTION_NORMALIZATION`

`WP2_P19=PASS_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`

`POST_P19_WP_ARCHITECTURE_REVIEW=PASS`

`WP2_P20A=PASS_LITERATURE_AND_NOVELTY_CLOSURE`

`P20A_MATERIAL_ANCHORS_VERIFIED=11_OF_11`

`P20A_CLOSEST_NEW_COMPARATOR=MOHAMMED_ET_AL_2026_ETASR_16945`

`P20A_NOVELTY_ACTION=WORDING_NARROWING_ONLY`

`P20A_SCIENTIFIC_BLOCKERS=0`

`WP2_P20B_ORIGINAL=HISTORICAL_SUPERSEDED_FOR_RANKING`

`WP2_P20B_R1=PASS_PUBLISHER_NEUTRAL_REQUALIFICATION`

`P20B_R1_PRIMARY_RECOMMENDATION=IEEE_INTERNET_OF_THINGS_JOURNAL`

`P20B_R1_BACKUP_1=ELSEVIER_INTERNET_OF_THINGS`

`P20B_R1_BACKUP_2=ACM_TRANSACTIONS_ON_INTERNET_OF_THINGS_COST_GATE`

`P20B_R1_BACKUP_3=IEEE_TNSM_CONDITIONAL`

`P20B_R1_AUTHOR_COMMITMENT=NO`

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
