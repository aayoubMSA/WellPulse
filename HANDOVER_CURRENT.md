# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P20D-R4 consortium from-scratch manuscript rewrite PASS**.  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This is the canonical operational retrieval point. GitHub is the scientific/control record; Google Drive is the durable binary-evidence/production-package authority. Repository/Drive evidence overrides chat memory.

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
- R3-R2 manuscript + P20E-R3 red-hat: **HISTORICAL / SUPERSEDED BY R4 BYTES**
- **P20D-R4 consortium from-scratch rewrite: PASS / CURRENT MANUSCRIPT AUTHORITY**
- **P20E-R4 fresh independent red-hat: NEXT / NOT STARTED**
- P21 author authorization packet: **LOCKED**
- P22 submission execution: **LOCKED**
- scientific blockers: **0**
- new experiment required: **NO**
- new empirical claim required: **NO**
- submission authorized: **NO**

Publication-lane earned progress is intentionally reset to **70/100** because the rewritten R4 bytes have not yet passed their own independent P20E gate.

## Global publication identity — HARD RULE

Research & Grants experience-ledger authority: **LL-048**.

Publication-facing name is exactly:

**Ahmed Ayoub**

Do not use expanded variants in manuscripts, portal metadata, CRediT, citations, correspondence, repository release metadata, ORCID/Scopus/Google-Scholar-facing records, or submission artifacts unless explicitly overridden for a specific legal/administrative form.

## Active survey-visibility requirement

The author explicitly requires that the manuscript properly show the effort performed in the literature survey.

R4 satisfies this by making the audit part of the main scientific argument rather than a short Related Work appendix.

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
8. `analysis/WP2_P20E_R3_RED_HAT_ADVERSARIAL_SUBMISSION_REVIEW_2026-08-29.md` — historical red-hat input that motivated R4
9. `analysis/WP2_P20D_R4_CONSORTIUM_FROM_SCRATCH_REWRITE_REVIEW_2026-08-29.md`
10. `docs/WP2_P20D_R4_CONSORTIUM_FROM_SCRATCH_REWRITE_CLOSURE_2026-08-29.md`
11. Research & Grants Lessons Learned Ledger: **LL-047 venue doctrine + LL-048 publication identity**.
12. P9 forensic authorities only when exact POWDER trace/caveat semantics are required.

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
- E1R4: 51 dB = 30% ICMP loss with MQTT 20/20; 52 dB = 60% ICMP loss with MQTT 13/20;
- E2: 52 dB = 65% ICMP loss and MQTT 11/20; 51 dB = 10% ICMP loss and MQTT 20/20;
- E3 at 52 dB = MQTT 60%, 25%, 55%; ICMP loss 80%, 65%, 70%;
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

Never claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- generic `WellPulse beats MQTT`;
- universal 52 dB threshold;
- deterministic RF-only recovery;
- exact broker recovery latency from E10-D;
- population reliability from message counts or three FIT runs;
- pooled FIT+POWDER inference;
- historical firstness for persistence, store-and-forward, end-to-end acknowledgment, offline recovery, or real-testbed use;
- unsupported field/rural/pump/hydraulic/groundwater/agronomic/crop/industrial-process validation.

## Current venue / route authority

Selected first route:

**Internet of Things (Elsevier)**

Article type:

**Full Research paper**

Initial route:

**Subscription / non-OA**

Reason: fast desk/editorial triage became a material objective while scientific fit remained strong. Current Elsevier scope explicitly includes IoT reliability, software engineering, testbeds, and quality assurance and accepts Full Research papers.

Backup 1: **IEEE Internet of Things Journal**.

No APC, paid-OA route, copyright/licence acceptance, or payment is authorized.

## Current R4 manuscript authority

Title:
**WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

Author:
**Ahmed Ayoub**

R4 build:

- manuscript PDF: `WellPulse_Consortium_Rewrite_R4_SubmissionDraft.pdf`;
- pages: **21**;
- references: **32 / all cited**;
- PDF SHA-256: `dba6c0f960204d88c1e7c1789e1fe6eb6e7ec3cf157145f770b01ad2a79fa4ea`;
- TeX SHA-256: `cfba916c5f2a61875748143e2e0a6f3e10aec3b32f987ba67963002d74751512`;
- fonts embedded;
- render/preflight: PASS;
- five Elsevier Highlights, each <=85 characters.

Narrative architecture:

`prior-art audit -> claim boundary -> two-property evaluation model -> FIT record survival -> POWDER path recovery -> synthesis`

R4 is a from-scratch narrative rewrite. Only verified scientific values, figure assets, verified bibliography records, and frozen publication/disclosure metadata were retained from the previous production package.

## Durable R4 archive

Archive:
`WellPulse_CONSORTIUM_REWRITE_R4_Package_2026-08-29.zip`

Drive ID:
`19HUAsnBDr3lWdJPTqaDe1EF1XTcbZYtp`

Archive size:
`2,188,788 bytes`

SHA-256:
`52d89acf6020bdc2979aac4b086a1581751f8c072269a65c2e586241759b5c21`

Drive raw read-back: **exact size/hash match / PASS**.

Package includes:

- R4 PDF;
- LaTeX source;
- F1-F4 current submission-safe figures;
- Supplement S1 literature/novelty audit PDF + CSV;
- Supplement S2 sanitized reproducibility artifact;
- Highlights;
- consortium rewrite review;
- manifest and SHA-256 list.

## Publication identity / disclosures

- sole/corresponding author: **Ahmed Ayoub**;
- affiliation: **Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt**;
- institutional email: `aelsayedo@msa.edu.eg`;
- canonical ORCID: `0009-0004-7895-3191`;
- research funding: **no external research funding**;
- competing interests: **none currently identified**;
- FIT IoT-LAB and POWDER acknowledgment/citation: present;
- CRediT: present;
- data availability: present;
- Elsevier generative-AI declaration: present;
- repository public disclosure already exists; no patentability claim;
- commercialization verdict: `NO_IP_ACTION -> PUBLISH`;
- repository software licence remains unactivated pending authority-to-license verification.

## Consortium rewrite verdict

R4 addresses the R3 red-hat weaknesses by making the literature audit a control on interpretation rather than a separate survey appendage.

Residual reviewer risks are disclosed but are not scientific blockers:

1. a reviewer may request a matched durable MQTT comparator;
2. a reviewer may request more FIT replicates;
3. a reviewer may request systematic-review machinery because the audit is extensive.

The manuscript already limits its claims so that none of these is currently a validity contradiction.

## Publication lane

1. P20A — 15% — **PASS / historical literature baseline**
2. P20B / R1-R6 — 15% — **PASS / ELSEVIER ROUTE CURRENT**
3. P20C — 15% — **PASS**
4. **P20D-R4 — 25% — PASS / CURRENT MANUSCRIPT AUTHORITY**
5. **P20E-R4 — 20% — NEXT / FRESH INDEPENDENT RED-HAT REQUIRED**
6. P21 — 5% — LOCKED
7. P22 — 5% — LOCKED

Earned progress: **70/100**.

## Exact next gate — P20E-R4

P20E-R4 must independently red-team the exact R4 bytes and must not act as an authoring pass unless it returns a finite defect.

At minimum verify:

- all numerical claims against frozen FIT/POWDER authorities;
- all 32 references cited and no unsupported prior-art attribution;
- survey method correctly described as targeted/claim-bounding, not systematic;
- B0 non-durable limitation visible and comparator claims bounded;
- run-level statistical discipline;
- exact/censored/upper-bound recovery semantics;
- no FIT+POWDER pooling;
- figure legibility and unchanged scientific content;
- S1/S2 integrity, privacy/security, and self-check;
- publication name/disclosures/affiliation;
- Elsevier scope and current portal/author requirements;
- no hidden submission, licence, copyright, or payment action.

P20E-R4 may PASS, PASS WITH FINITE FIXES, or FAIL. It must not submit externally.

## Stop state

`WP2_P20D_R4=PASS_FROM_SCRATCH_CONSORTIUM_REWRITE`

`R4_CURRENT_MANUSCRIPT_AUTHORITY=YES`

`PUBLICATION_LANE_PROGRESS=70_OF_100`

`P20E_R3=HISTORICAL_INPUT_ONLY`

`P20E_R4=NEXT_NOT_STARTED`

`P21_LOCKED=YES`

`P22_LOCKED=YES`

`PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`

`CURRENT_PHASE=WP2_P20E_R4_GATE_NOT_STARTED`

`SUBMISSION_AUTHORIZED=NO`
