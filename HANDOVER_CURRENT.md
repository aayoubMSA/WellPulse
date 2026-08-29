# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P20E-R4 PASS / R4-R1 finite production repair**.  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This is the canonical operational retrieval point. GitHub is the scientific/control record; Google Drive is the durable binary-evidence authority for previously archived packages. Repository/Drive evidence overrides chat memory.

## Executive state

- P8 POWDER campaign: **COMPLETE / GOLDEN**
- P9 forensic reconciliation: **PASS**
- P10 scientific analysis contract: **PASS / FROZEN**
- P11 full raw-data analysis: **PASS**
- P12 cross-evidence integration: **PASS**
- P13 claim–evidence matrix: **PASS / FROZEN CLAIM AUTHORITY**
- P16 adversarial publication QA: **PASS**
- P17/P17V manuscript + independent claim validation: **PASS / HISTORICAL SCIENTIFIC BASELINE**
- P18R/P18RC figures: **PASS / SCIENTIFIC + PRODUCTION FIGURE AUTHORITY**
- P19 reviewer/reproducibility artifact: **PASS**
- P20A literature baseline: **PASS / HISTORICAL INPUT**
- P20B-R6 venue switch: **PASS / INTERNET OF THINGS (ELSEVIER) SELECTED**
- P20C authorship/credits/rights/IP: **PASS**
- R3-R2 manuscript + P20E-R3 red-hat: **HISTORICAL / SUPERSEDED**
- P20D-R4 consortium from-scratch rewrite: **PASS**
- **R4-R1 finite production repair: PASS / CURRENT MANUSCRIPT AUTHORITY**
- **P20E-R4 fresh independent red-hat: PASS / CURRENT SUBMISSION-READINESS AUTHORITY**
- **P21-R4 author submission authorization packet: NEXT / NOT STARTED**
- P22 submission execution: **LOCKED**
- scientific blockers: **0**
- production blockers: **0**
- new experiment required: **NO**
- new empirical claim required: **NO**
- submission authorized: **NO**

Publication-lane earned progress: **90/100**.

## Global publication identity — HARD RULE

Research & Grants experience-ledger authority: **LL-048**.

Publication-facing name is exactly:

**Ahmed Ayoub**

Do not use expanded variants in manuscripts, portal metadata, CRediT, citations, correspondence, repository release metadata, ORCID/Scopus/Google-Scholar-facing records, or submission artifacts unless explicitly overridden for a specific legal/administrative form.

## Active survey-visibility requirement

The author explicitly requires that the manuscript properly show the effort performed in the literature survey.

R4-R1 satisfies this by making the audit part of the main scientific argument rather than a short Related Work appendix.

Current audit state:

- source/axis groups: **32**;
- peer-reviewed scholarly articles: **25**;
- normative MQTT standard: **1**;
- official technical/platform sources: **6**;
- wording-narrowing outcomes: **17**;
- contextual/no-impact outcomes: **15**;
- scientific blockers: **0**.

The manuscript describes this as a **targeted, claim-bounding submission-date novelty audit**, not a PRISMA systematic review, meta-analysis, or exhaustive bibliographic census.

Supplement S1 preserves the complete 32-group collision matrix.

`SURVEY_VISIBILITY_REQUIREMENT=ACTIVE`

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
3. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
4. `docs/WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION_CLOSURE_2026-08-29.md`
5. `docs/WP2_P19_REVIEWER_SUPPLEMENT_SANITIZED_ARTIFACT_CLOSURE_2026-08-29.md`
6. `analysis/WP2_P20B_R6_DESK_TRIAGE_PRIORITY_VENUE_SWITCH_2026-08-29.md`
7. `analysis/WP2_P20C_AUTHORSHIP_CREDITS_RIGHTS_IP_LOCK_2026-08-29.md`
8. `analysis/WP2_P20D_R4_CONSORTIUM_FROM_SCRATCH_REWRITE_REVIEW_2026-08-29.md`
9. `docs/WP2_P20D_R4_CONSORTIUM_FROM_SCRATCH_REWRITE_CLOSURE_2026-08-29.md`
10. `analysis/WP2_P20E_R4_RED_HAT_REVIEW_2026-08-29.md`
11. `docs/WP2_P20E_R4_RED_HAT_REVIEW_CLOSURE_2026-08-29.md`
12. Research & Grants Lessons Learned Ledger: **LL-047 venue doctrine + LL-048 publication identity**.
13. P9 forensic authorities only when exact POWDER trace/caveat semantics are required.

Old P21 packets and old R3/R3-R2 submission bytes are historical only. Do not use them to unlock P22.

## Historical scored state — immutable

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No later evidence may be relabelled as scored P7B success.

## Frozen scientific doctrine

### FIT — record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

`B0/W1 × C0/C1/C2 × 3 runs = 18 cells`, exactly 10,000 records/run.

- C0 B0/W1 = 100% all runs;
- C1 B0 = 80%, W1 = 100% all runs;
- C2 B0 = 80%, W1 = 100% all runs;
- B0 C1/C2 permanently miss exactly 2,000 records/run;
- W1 final reconciliation contains all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`;
- FIT reconnect means remain descriptive engineering observations, not powered latency comparisons.

Run/replicate is the scientific unit. The 10,000 messages inside each run are not 10,000 independent samples. C2 is a gateway-process `exec` restart, not node/hardware reboot. B0 is non-durable and is not the strongest durable MQTT comparator.

### POWDER — communication-path characterization

WP2-P8 profile `srslte-controlled-rf` is separately executed physical-RF/LTE/MQTT characterization, not architecture-effect estimation.

- E1/E2/E3 transition region is experiment-specific; 52 dB is not universal;
- E8 isolates broker/service failure while LTE remains healthy;
- E9 is no-fault control;
- E10-A remains censored with no scalar recovery latency;
- E10-B exact: 6.063318 s first MQTT, 6.609430 s first ping, 0.060172 s publish-to-CORE receipt;
- E10-C-B exact: 29.247733 s first ping, 29.248129 s first MQTT;
- E10-D remains upper bound only, `<=10.908749 s`;
- receiver-side unique-ID reconciliation governs delivery;
- FIT and POWDER are complementary/non-substitutable and are not statistically pooled.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Immutable claim prohibitions

Never claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB; deterministic RF-only recovery; exact broker recovery latency from E10-D; population reliability from message counts/three FIT runs; pooled FIT+POWDER inference; historical firstness for persistence/store-and-forward/end-to-end acknowledgment/offline recovery/real-testbed use; or unsupported field/rural/pump/hydraulic/groundwater/agronomic/crop/industrial-process validation.

## Current venue / route authority

Selected first route:

**Internet of Things (Elsevier)**

Article type: **Full Research paper**.

Initial route: **Subscription / non-OA**.

Reason: fast desk/editorial triage became a material objective while scientific fit remained strong. Current journal scope includes IoT reliability, software engineering, testbeds and quality assurance.

Backup 1: **IEEE Internet of Things Journal**.

No APC, paid-OA route, copyright/licence acceptance or payment is authorized.

## Current manuscript authority — R4-R1

Title:
**WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

Author:
**Ahmed Ayoub**

Current production state:

- manuscript PDF: `WellPulse_Consortium_Rewrite_R4R1_SubmissionDraft.pdf`;
- pages: **21**;
- references: **32 / 32 cited**;
- abstract: **250 words**;
- keywords: **7**;
- PDF SHA-256: `6ebd6a07a7ed512cb2a53fb75f778536a2fad86b5d0de690e1ddbcd3d685c6ac`;
- TeX SHA-256: `ac85fac31af5d203ffbb04d7f191ee283e02e55fe4529ac6b8f4558359d85dcb`;
- fonts: embedded;
- preflight warnings: **0**;
- publication name: **Ahmed Ayoub**.

Finite repair from R4:

1. abstract 269 -> 250 words;
2. keywords 8 -> 7;
3. Highlights rewritten without project/testbed acronyms or jargon;
4. editable `highlights.docx` added;
5. generative-AI declaration heading normalized to current Elsevier wording.

No experiment, numerical result, figure, reference set, statistical unit, claim class or inferential role changed.

## Current R4-R1 package

Archive:
`WellPulse_CONSORTIUM_REWRITE_R4R1_Package_2026-08-29.zip`

- size: **2,228,500 bytes**;
- SHA-256: `290b89fff927f2e4bfeeade3031844be2c3f94333584496ff04718ce58cc6b67`;
- manifest rows: 16;
- manifest mismatches: 0;
- ZIP integrity: PASS.

This R4-R1 finite-repair archive was generated and validated locally during P20E-R4. A new Drive upload was not performed at this gate because the available Drive upload action requires a connector file reference rather than a raw local path. Do not falsely treat the earlier R4 Drive archive as R4-R1 byte authority. Archive R4-R1 to Drive in a later gate when a compliant file-reference path is available.

Previous R4 Drive archive remains historical base evidence:
- Drive ID `19HUAsnBDr3lWdJPTqaDe1EF1XTcbZYtp`;
- SHA-256 `52d89acf6020bdc2979aac4b086a1581751f8c072269a65c2e586241759b5c21`.

Supplement S1:
- rows: 32;
- SHA-256 `e9bcda5b7ec5b3993b51eb69a4da6a52d15bfa2da9e14774d65db88cb65721d8`.

Supplement S2:
- SHA-256 `99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`;
- isolated artifact self-check: PASS;
- no `__pycache__` / `.pyc`.

Editable Highlights:
- SHA-256 `3248fe4ad6be9fe23503517b10783c38a3be4c3a9536f207f326b6667ff5a640`.

## Current red-hat authority — P20E-R4

Status: **PASS AFTER FINITE PRODUCTION REPAIR / NO SCIENTIFIC OR PRODUCTION BLOCKER**.

Independent evidence:

- all frozen FIT values independently recomputed and matched;
- POWDER exact/censored/upper-bound semantics matched;
- B0 non-durable boundary remains explicit;
- 32/32 references cited, unresolved keys = 0;
- literature audit remains targeted/claim-bounding;
- no forbidden-claim regression;
- no FIT+POWDER pooling;
- four main figures byte-identical to R4 inputs;
- S1 visual QA PASS;
- S2 isolated self-check PASS;
- privacy/publication-name scans PASS;
- independent deterministic rebuild = **21 pages / 0 changed pages / 0.0% changed pixels**.

Residual reviewer risks, not blockers:

1. matched durable MQTT comparator may be requested;
2. additional FIT replicates may be requested;
3. targeted literature audit is not exhaustive/systematic;
4. Gaspar detailed method/result comparison is not asserted;
5. survey-visible 21-page preprint remains intentionally detailed.

## Publication identity / disclosures

- sole/corresponding author: **Ahmed Ayoub**;
- affiliation: **Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt**;
- institutional email: `aelsayedo@msa.edu.eg`;
- canonical ORCID: `0009-0004-7895-3191`;
- research funding: no external research funding;
- competing interests: none currently identified;
- FIT IoT-LAB + POWDER acknowledgment/citations: present;
- CRediT: present;
- data availability: present;
- Elsevier generative-AI declaration: present;
- repository public disclosure exists; no patentability claim;
- commercialization verdict: `NO_IP_ACTION -> PUBLISH`.

## Publication lane

1. P20A — 15% — **PASS / historical literature baseline**
2. P20B / R1-R6 — 15% — **PASS / ELSEVIER ROUTE CURRENT**
3. P20C — 15% — **PASS**
4. P20D-R4/R4-R1 — 25% — **PASS / CURRENT MANUSCRIPT AUTHORITY**
5. P20E-R4 — 20% — **PASS / RED-HAT CLEARED**
6. **P21-R4 — Author Submission Authorization Packet — 5% — NEXT / NOT STARTED**
7. P22 — Submission Execution & Receipt — 5% — LOCKED

Earned progress: **90/100**.

## Exact next gate — P21-R4

P21-R4 may prepare an internal author-authorization packet against the exact R4-R1 bytes. It must recheck current Editorial Manager requirements, concurrent-submission state, author/ORCID/contact metadata, file-role mapping, and Subscription/non-OA route.

P21-R4 must not submit externally and must not infer author authorization from `continue`, `go on`, `next`, journal preference, or any historical P21 packet.

P22 remains locked until a new explicit author authorization based on R4-R1.

## Stop state

`WP2_P20D_R4=PASS_FROM_SCRATCH_CONSORTIUM_REWRITE`

`R4R1_CURRENT_MANUSCRIPT_AUTHORITY=YES`

`WP2_P20E_R4=PASS_AFTER_FINITE_PRODUCTION_REPAIR`

`PUBLICATION_LANE_PROGRESS=90_OF_100`

`P21_R4=NEXT_NOT_STARTED`

`P22_LOCKED=YES`

`PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`

`CURRENT_PHASE=STOP_AFTER_P20E_R4_PASS`

`SUBMISSION_AUTHORIZED=NO`
