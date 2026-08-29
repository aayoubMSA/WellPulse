# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P20B-R5 venue lock + WP2-P20C PASS**.  
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
- P17V independent validation: **PASS / 9 OF 9 CLAIMS VALIDATED**
- P18/P18B: **HISTORICAL / SUPERSEDED**
- P18R scientific figure engineering: **PASS**
- P18R deterministic F1 hotfix: **PASS / SCIENTIFIC-TOPOLOGY AUTHORITY**
- P18RB: **CONDITIONAL PASS / SCIENCE PASS**
- P18RC main-figure production normalization: **PASS / CURRENT PRODUCTION MAIN-DISPLAY AUTHORITY**
- P19 reviewer supplement + sanitized artifact: **PASS / CURRENT REVIEWER-ARTIFACT AUTHORITY**
- post-P19 consortium WP architecture review: **PASS**
- P20A literature & novelty closure: **PASS / CURRENT NOVELTY AUTHORITY**
- P20B original Elsevier-heavy ranking: **HISTORICAL / SUPERSEDED**
- P20B-R1 publisher-neutral requalification: **PASS**
- P20B-R2 national publishing-agreement reweighting: **PASS**
- P20B-R3 industrial discoverability / translation axis: **PASS**
- P20B-R4 consortium venue-axis completeness: **PASS / 8-AXIS VECTOR FROZEN**
- P20B-R5 final multi-axis venue scoring: **PASS / IEEE IOT-J SELECTED**
- P20C authorship / credits / rights / IP-translation lock: **PASS**
- current scientific blockers: **0**
- new experiment required: **NO**
- new empirical claim required: **NO**
- live POWDER dependency: **NONE**
- submission authorization: **NO**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No later evidence may be relabelled as scored P7B success.

## Mandatory read order

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_POST_P19_CONSORTIUM_WP_ARCHITECTURE_REVIEW_2026-08-29.md`
3. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
4. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
5. `analysis/WP2_P12_CROSS_EVIDENCE_INTEGRATION_2026-08-29.md`
6. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
7. `manuscript/WP2_P16_ADVERSARIAL_PUBLICATION_QA_2026-08-29.md`
8. `docs/WP2_P17_EXPERIMENT_DOSSIER_V2_2_RESEARCH_PACK_2026-08-29.md`
9. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`
10. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
11. `manuscript/WP2_P18R_F1_HOTFIX_QA_2026-08-29.md`
12. `docs/WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION_CLOSURE_2026-08-29.md`
13. `docs/WP2_P19_REVIEWER_SUPPLEMENT_SANITIZED_ARTIFACT_CLOSURE_2026-08-29.md`
14. `analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md`
15. `docs/WP2_P20A_LITERATURE_NOVELTY_CLOSURE_2026-08-29.md`
16. `analysis/WP2_P20B_R1_PUBLISHER_NEUTRAL_VENUE_REQUALIFICATION_2026-08-29.md`
17. `analysis/WP2_P20B_R2_NATIONAL_PUBLISHING_AGREEMENT_REWEIGHTING_2026-08-29.md`
18. `analysis/WP2_P20B_R3_INDUSTRIAL_DISCOVERABILITY_TRANSLATION_AXIS_2026-08-29.md`
19. `analysis/WP2_P20B_R4_CONSORTIUM_VENUE_AXIS_COMPLETENESS_REVIEW_2026-08-29.md`
20. `analysis/WP2_P20B_R5_FINAL_MULTIAXIS_VENUE_SCORING_2026-08-29.md`
21. `docs/WP2_P20B_R5_FINAL_VENUE_SELECTION_CLOSURE_2026-08-29.md`
22. `analysis/WP2_P20C_AUTHORSHIP_CREDITS_RIGHTS_IP_LOCK_2026-08-29.md`
23. `docs/WP2_P20C_AUTHORSHIP_CREDITS_RIGHTS_IP_CLOSURE_2026-08-29.md`
24. Google Sheet `Research & Grants — Lessons Learned Ledger`; **LL-047 is the master venue-selection doctrine**. Older venue lessons are subordinate detail/evidence.
25. P9 forensic authorities only when exact POWDER trace/caveat semantics are required.

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
- E8 = broker/service failure while LTE remains healthy;
- E9 = no-fault control;
- E10 preserves exact/censored/upper-bound semantics;
- E10-A = no scalar recovery latency;
- E10-D = upper bound only;
- receiver-side unique-ID reconciliation governs reported delivery.

FIT and POWDER are complementary and non-substitutable. No pooled FIT+POWDER statistic/inference is permitted.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Manuscript baseline

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`

Title: **WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

P17V: claims `9/9` validated; numerical contradictions `0`; unsupported new claims `0`; scientific blockers `0`; new experiment required `NO`.

Never generalize the FIT result into generic MQTT superiority.

## P18RC / P19 durable authorities

P18RC archive: `WellPulse_P18RC_Main_Figure_Production_Normalization_2026-08-29.zip`  
Drive ID `1rdFq7ktppFBUp54UoeS5AP3kukDiU9sW`  
SHA-256 `97f0fd1e4c41bb67f6da70056935b60a1627695e082ea8d38eff657bce1d02a8`  
Drive read-back PASS.

Current figure PDF SHA-256:
- F1 `7d7feb075731475747282cf0dd0081ec6afb1bc45c17bd16c754063ac83237cb`;
- F2 `73b96a2b8c1fa2a4c15b3bd15b0065f77a2863dcacb84d8c3f2d7d0b57cef508`;
- F3 `faccbef11762df7c293728992e59ac9b17e4b455e4d2023dcddeb50f41e5e9b8`;
- F4 `87d2c703e4308477b3d89c5d0a9594a7380f2e0c8350d5d74721f779785a1b38`.

P19 archive: `WellPulse_P19_Reviewer_Supplement_Sanitized_Artifact_2026-08-29.zip`  
Drive ID `1t5S_L-S0hfmyMPLdXh8Fd-jGBOH8SCkl`  
SHA-256 `5a9ed4fa197ea5c3aa43447fabf16d7928aeabe58722e16af63afe25bc7cfdc7`  
Drive read-back PASS.

P19 manifest `54/54` PASS; isolated `python -I artifact_selfcheck.py` PASS. Two `__pycache__/*.pyc` files must be excluded from the final external package during P20D/P20E.

## P20A novelty authority

P20A current-search result:

- material anchors: **11/11 verified**;
- closest new comparator: Mohammed et al. 2026, DOI `10.48084/etasr.16945`;
- action: **WORDING NARROWING ONLY**;
- no novelty claim for generic persistence, disk-backed buffering, retransmission, store-and-forward, offline-first continuity, application/database acknowledgment, subscriber confirmation, generic robustness testing or historical decoupling of data reliability from network availability;
- E-MQTT constrains receiver-confirmation historical priority;
- Radwan et al. 2026 must be accounted for;
- Gaspar et al. DOI `10.1109/MIOT.2026.3681190` remains bibliographic-only for detailed attribution unless full text is directly recovered.

P20D must add Mohammed et al. 2026, account for E-MQTT and Radwan et al. 2026, and preserve all P20A wording constraints.

## Venue-selection authority — P20B-R5

LL-047 freezes eight independent venue axes:

1. scientific/editorial fit — 25%;
2. academic/institutional recognition — 10%;
3. industrial pull — 15%;
4. audience reach/access — 10%;
5. economics/route certainty — 10%;
6. speed/process predictability — 10%;
7. rights/IP/control — 10%;
8. evidence/reproducibility preservation — 10%.

Final R5 ranking:

1. **IEEE Internet of Things Journal — 90.00/100 — SELECTED**;
2. Internet of Things (Elsevier) — 89.00/100 — backup;
3. Scientific Reports — 87.25/100 — agreement-advantaged route;
4. ACM Transactions on Internet of Things — 83.25/100;
5. Computer Networks — 82.75/100;
6. IEEE TNSM — 81.75/100;
7. Telecommunication Systems — 76.75/100.

Selected route:

`VENUE=IEEE_INTERNET_OF_THINGS_JOURNAL`

`ROUTE=TRADITIONAL_NON_OA`

Current IEEE IoT-J material reports direct IoT architecture/networking/testbed scope, Q1/SCIE field status in current metric cross-checks, and average `6.9 weeks` to first decision. Current guide states mandatory `$175/page` beyond the first 8 published pages. No overlength payment is authorized.

Lossless-format rule: **never damage evidence/claims/figure legibility merely to hit 8 pages**. If final IEEE typesetting exceeds 8 pages, either obtain explicit author approval for overlength charges or revert to the ranked backup.

## P20C current authorship / rights / IP authority

Locked publication identity:

- sole author: **Ahmed Elsayed Ayoub**;
- corresponding author: **Ahmed Elsayed Ayoub**;
- affiliation: **Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City, Egypt**;
- research funding: **no external funding**;
- competing interests: **none currently identified**.

Frozen CRediT roles:

- Conceptualization;
- Methodology;
- Software;
- Validation;
- Formal analysis;
- Investigation;
- Data curation;
- Visualization;
- Writing — original draft;
- Writing — review & editing;
- Project administration.

Required P20D additions:

1. FIT IoT-LAB explicit acknowledgment; reference [8] remains required.
2. POWDER naming/citation and concise acknowledgment; reference [10] remains required.
3. IEEE-compliant generative-AI disclosure because AI assistance extended beyond grammar-only correction.
4. CRediT statement.
5. Funding and COI statements.

Rights/IP state:

- P18RC figures are project-generated; no third-party reproduced figure permission identified;
- P19 privacy/security sanitization remains mandatory;
- repository `aayoubMSA/WellPulse` is already **public**, so prior public disclosure exists;
- patentability: **not assessed / no claim**;
- formal institutional/student ownership for new protective/licensing action: **unresolved**;
- root repository currently has **no LICENSE file**;
- prior MIT intent for original WellPulse code is recorded but **not activated** until authority to license is verified;
- finite commercialization verdict: **`NO_IP_ACTION -> PUBLISH`**; future partner/licensing exploration remains possible for rights actually controlled.

IEEE copyright-form acceptance and any payment remain downstream author-controlled actions.

## Refactored remaining publication lane

1. **P20A — Literature & Novelty Closure — 15% — PASS**
2. **P20B / R1–R5 — Venue Qualification & Final Selection — 15% — PASS**
3. **P20C — Authorship / Credits / Rights / IP Lock — 15% — PASS**
4. **P20D — Final IEEE Manuscript & Source Package Integration — 25% — NEXT / NOT STARTED**
5. **P20E — Independent Submission-Readiness Validation — 20% — LOCKED**
6. **P21 — Author Submission Authorization Packet — 5% — LOCKED**
7. **P22 — Submission Execution & Receipt — 5% — LOCKED**

Remaining-lane earned progress: **45/100**.

## Exact next gate — WP2-P20D

P20D is the only next executable gate.

P20D must:

- re-read current IEEE IoT-J author instructions;
- create an IEEE-shaped final manuscript/source package without changing frozen science;
- integrate P20A literature additions/narrowing;
- insert P20C author/CRediT/funding/COI/testbed/AI statements;
- integrate P18RC figures and appropriate supplementary placement;
- retain P19 reviewer artifact while excluding `__pycache__/*.pyc`;
- run a **lossless IEEE page-count simulation**;
- report exact 8-page/overlength outcome;
- generate reproducible source/PDF and manifests/hashes;
- stop before submission, copyright acceptance or payment.

P20E remains locked until P20D passes.

## Immutable prohibitions

Do not claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB; deterministic RF-only recovery; exact broker latency from E10-D; population reliability from message counts or three FIT runs; pooled FIT+POWDER inference; historical firstness for persistence/store-and-forward/end-to-end confirmation; or unsupported field/rural/Siwa/pump/hydraulic/groundwater/agronomic/industrial-process validation.

## Stop state

`WP2_P20B_R5=PASS_FINAL_MULTIAXIS_VENUE_SELECTION`

`VENUE_SELECTED=IEEE_INTERNET_OF_THINGS_JOURNAL`

`ROUTE=TRADITIONAL_NON_OA`

`WP2_P20C=PASS_AUTHORSHIP_CREDITS_RIGHTS_IP_LOCK`

`P20D_UNLOCKED=YES`

`P20E_LOCKED=YES`

`CURRENT_SCIENTIFIC_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

`OVERLENGTH_PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_ACCEPTANCE_AUTHORIZED=NO`

`CURRENT_PHASE=WP2_P20D_GATE_NOT_STARTED`

`SUBMISSION_AUTHORIZED=NO`
