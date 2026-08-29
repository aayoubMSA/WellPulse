# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P20D-R5 Role Model Paper rebuild + WP2-P20E-R5 Scientific/Editorial Red-Hat PASS**.  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This is the canonical operational retrieval point. GitHub is the scientific/control record; Google Drive is the durable binary-evidence authority. Repository/Drive evidence overrides chat memory.

## Executive state

- P8 POWDER campaign: **COMPLETE / GOLDEN**
- P9 forensic reconciliation: **PASS**
- P10 scientific analysis contract: **PASS / FROZEN**
- P11 full raw-data analysis: **PASS**
- P12 cross-evidence integration: **PASS**
- P13 claim–evidence matrix: **PASS / FROZEN CLAIM AUTHORITY**
- P16 adversarial publication QA: **PASS**
- P17/P17V manuscript + independent claim validation: **PASS / HISTORICAL SCIENTIFIC BASELINE**
- P18R/P18RC historical figure authorities: **PASS / SUPERSEDED FOR CURRENT MAIN DISPLAY BY R5 FIGURE REBUILD; SCIENTIFIC VALUES PRESERVED**
- P19 reviewer/reproducibility artifact: **PASS**
- P20A literature baseline: **PASS / HISTORICAL INPUT**
- P20B-R6 venue switch: **PASS / INTERNET OF THINGS (ELSEVIER) SELECTED**
- P20C authorship/credits/rights/IP: **PASS**
- R3/R4/R4-R1 manuscripts and red-hats: **HISTORICAL / SUPERSEDED BY R5 BYTES**
- **P20D-R5 Role Model Paper doctrine rebuild: PASS / CURRENT MANUSCRIPT AUTHORITY**
- **P20E-R5 Scientific + Editorial Red-Hat: PASS / CURRENT SUBMISSION-READINESS AUTHORITY**
- **P21-R5 author submission authorization packet: NEXT / NOT STARTED**
- P22 submission execution: **LOCKED**
- scientific blockers: **0**
- production blockers: **0**
- new experiment required for current bounded claims: **NO**
- new empirical claim required: **NO**
- submission authorized: **NO**

Publication-lane earned progress: **90/100**.

## Global publication identity — HARD RULE

Research & Grants Lessons Learned authority: **LL-048**.

Publication-facing name is exactly:

**Ahmed Ayoub**

Do not use expanded variants in manuscripts, portal metadata, CRediT, citations, correspondence, repository release metadata, ORCID/Scopus/Google-Scholar-facing records, or submission artifacts unless explicitly overridden for a specific legal/administrative form.

## Role Model Paper requirement — HARD PUBLICATION STANDARD

Research & Grants authority: **LL-049 / Research Operating Doctrine v2.2 §22A**.

Scope: scholarly research/publication work only.

Target:
**Teach → Prove → Translate → Persuade**.

Current R5 applies:
- one governing scientific question/intellectual spine;
- visible literature synthesis that defines the claim boundary;
- mandatory Field-Native Glossary Gate;
- mathematics only where it removes endpoint ambiguity;
- fair comparator boundaries;
- claim → evidence → analysis → validation → limitation trace;
- negative/adverse evidence kept visible;
- reviewer-question-driven figures and synthesis tables;
- practical engineering interpretation without upgrading evidence to field/industrial validation;
- separate Scientific and Editorial Red Hats.

Field-native glossary is paper/subfield-specific. Publication prose must prefer established MQTT/IoT/dependability vocabulary and block generic AI synonyms and internal WP/agent/control jargon where a field-native term exists.

## Active survey-visibility requirement

The paper must visibly show the literature effort and how it changes the research claim.

Current R5 state:
- direct novelty-control source/axis groups: **32**;
- peer-reviewed scholarly articles inside the direct audit: **25**;
- normative MQTT standard: **1**;
- official technical/platform sources: **6**;
- additional framing references: **2**;
- total manuscript bibliography: **34 / 34 cited**;
- wording-narrowing outcomes in S1: **17**;
- contextual/no-impact outcomes: **15**;
- scientific blockers from novelty audit: **0**.

The audit is explicitly a **targeted, submission-date claim-bounding synthesis**, not a PRISMA systematic review, meta-analysis, prevalence study, or exhaustive bibliographic census.

Supplement S1 preserves the full 32-group collision matrix.

`SURVEY_VISIBILITY_REQUIREMENT=ACTIVE`

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
3. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
4. `docs/WP2_P19_REVIEWER_SUPPLEMENT_SANITIZED_ARTIFACT_CLOSURE_2026-08-29.md`
5. `analysis/WP2_P20B_R6_DESK_TRIAGE_PRIORITY_VENUE_SWITCH_2026-08-29.md`
6. `analysis/WP2_P20C_AUTHORSHIP_CREDITS_RIGHTS_IP_LOCK_2026-08-29.md`
7. `analysis/WP2_P20D_R5_ROLE_MODEL_DOCTRINE_REBUILD_2026-08-29.md`
8. `docs/WP2_P20D_R5_ROLE_MODEL_DOCTRINE_REBUILD_CLOSURE_2026-08-29.md`
9. `analysis/WP2_P20E_R5_ROLE_MODEL_RED_HAT_2026-08-29.md`
10. `docs/WP2_P20E_R5_ROLE_MODEL_RED_HAT_CLOSURE_2026-08-29.md`
11. Research & Grants Lessons Learned Ledger: **LL-047 venue doctrine + LL-048 publication identity + LL-049 Role Model Paper doctrine**.
12. P9 forensic authorities only when exact POWDER trace/caveat semantics are required.

Old P21 packets and all R3/R4/R4-R1 submission bytes are historical only. **Do not use them to unlock P22.**

## Historical scored state — immutable

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No later evidence may be relabelled as scored P7B success.

## Frozen scientific doctrine

### FIT — data durability / end-to-end completeness

Authority: `FINAL_WP_RT01_FIT_A8`.

`B0/W1 × C0/C1/C2 × 3 runs = 18 cells`, exactly 10,000 records/run.

Internal labels remain traceability labels; R5 publication prose uses field-native descriptions.

- healthy C0: B0/W1 = 100% in all runs;
- broker-outage C1: B0 = 80%, W1 = 100% in all runs;
- outage + gateway-process-restart C2: B0 = 80%, W1 = 100% in all runs;
- B0 C1/C2 permanently miss exactly 2,000 records/run;
- W1 final reconciliation contains all 10,000 generated IDs exactly once;
- W1 final missing/duplicate/unexpected = 0;
- W1 queue-drain means: C1 `67.731246 s`; C2 `67.870252 s`;
- reconnect means remain descriptive engineering observations, not powered latency comparisons.

Run/replicate is the scientific unit. The 10,000 within-run records are reconciliation observations, not 10,000 independent samples. C2 is a gateway-process `exec` restart, not node/hardware reboot. B0 is non-durable and is not the strongest durable MQTT comparator.

### POWDER — communication-path / failure-domain characterization

WP2-P8 profile `srslte-controlled-rf` remains separately executed physical-RF/LTE/MQTT characterization, not architecture-effect estimation.

- E1/E2/E3 transition region is experiment-specific; 52 dB is not universal;
- E8 isolates broker/service failure while LTE remains healthy;
- E9 is no-fault control;
- E10-A remains censored with no scalar recovery latency;
- E10-B exact: 6.063318 s first MQTT, 6.609430 s first ping, 0.060172 s publish-to-receiver receipt;
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

Backup 1: **IEEE Internet of Things Journal**.

No APC, paid-OA route, copyright/licence acceptance or payment is authorized.

## Current manuscript authority — R5 Role Model Paper

Title:
**Beyond Reconnection: Failure-Domain-Aware Evaluation of Data Durability and Recovery in MQTT-Based IoT Telemetry**

Author:
**Ahmed Ayoub**

R5 deliberately removes the undergraduate/project-report signals identified in R4-R1:
- project brand removed from title lead;
- internal experiment codes removed from reader-facing narrative/figure legends where unnecessary;
- field-native glossary applied;
- literature synthesis drives the claim boundary;
- endpoint model mathematically formalized;
- methodology organized by evidence role rather than execution chronology;
- main figures rebuilt as scientific argument artifacts;
- Engineering Interpretation and Design Guidance section added;
- conclusion states a reusable engineering reliability contract rather than project status.

Current production state:
- manuscript PDF: `WellPulse_Role_Model_R5_RedHat_Cleared.pdf`;
- pages: **23**;
- abstract: **240 words**;
- keywords: **7**;
- references: **34 / 34 cited**;
- PDF SHA-256: `28f508b1c6abf91c555e9cfa72148a47efde6dda6e7c91fc8054d27f4d4af7e3`;
- TeX SHA-256: `46d95f42b2bbbf8d9d561ad866248058e63bb36d03c75149020d4a89ae628402`;
- publication name: **Ahmed Ayoub**;
- PDF openable / unencrypted / not scanned;
- fonts embedded;
- overfull hbox warnings: 0;
- final visual QA: PASS.

## Mathematical endpoint model — publication-facing

R5 defines:
- receiver-reconciled completeness `C_e2e = |G ∩ R| / |G|`;
- permanent missing set `M = G \ R`;
- duplicates `D = N_R - |R|`;
- endpoint-specific path recovery `T_path(e)=t_e-t_0`;
- queue-drain time `T_drain=t_complete-t_reconnect`;
- recovery observations that retain failure domain, action, endpoint, timing, and exact/censored/upper-bound semantics.

These definitions are measurement bookkeeping, not a claimed universal reliability theory.

## R5 figures — current display authority

R5 uses four deterministic publication-facing figures generated from frozen derived data or bounded conceptual definitions:
1. failure-domain-aware evaluation framework;
2. delivery completeness + path reconnection + queue-drain cost;
3. cross-layer transition behavior + repeatability;
4. failure-domain intervention matrix + recovery endpoint semantics.

R5 display authority supersedes R4 main-display layout for the current manuscript. It does **not** supersede frozen numerical/scientific evidence authorities.

## Current R5 package — durable binary authority

Archive:
`WellPulse_ROLE_MODEL_R5_RedHat_Cleared_Package_2026-08-29.zip`

Drive ID:
`13Yegfc_i6axvNSOj0AVzkgPqonqTVVPi`

Archive size:
`4,194,563 bytes`

Archive SHA-256:
`bd98d49b7bd975177dd093a3172a2404410dff633c50778292cd719eaa303c7a`

Drive raw read-back: **exact size/hash match / PASS**.

Package:
- 31 manifest rows + manifest/hash files;
- ZIP integrity PASS;
- TeX source;
- PDF/SVG/PNG figures;
- deterministic figure generator + frozen source data;
- `FIELD_NATIVE_GLOSSARY.md`;
- Role Model doctrine application record;
- Scientific and Editorial Red-Hat reports;
- Supplement S1 literature audit;
- Supplement S2 reproducibility artifact;
- editable highlights DOCX + text;
- build-validation receipt;
- SHA-256 manifest.

Supplement S1:
- rows: 32;
- CSV SHA-256 `c9c5e17367cddca13cc523a95a0dd92734734c0ca04e1580e416413bc7bf8462`.

Supplement S2:
- SHA-256 `99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`;
- isolated `python -I artifact_selfcheck.py`: **PASS**.

Highlights DOCX:
- SHA-256 `e1a16519d800f1e4e6b74d1df0da8ef9f9ace3dcb290a98b52a121659d9a6a0c`;
- render QA: PASS;
- 5 highlights, each <=72 characters.

## Current red-hat authority — P20E-R5

Status: **PASS / ROLE MODEL PAPER GATE PASSED / NO SCIENTIFIC OR PRODUCTION BLOCKER**.

Fresh version-bound checks:
- frozen FIT values independently recomputed and matched;
- POWDER exact/censored/upper-bound semantics matched;
- non-durable comparator boundary explicit;
- three-run inferential limit explicit;
- 34/34 references cited;
- targeted literature status explicit;
- no internal WP/run-code narrative regression;
- no forbidden claim regression;
- no FIT+POWDER pooling;
- mathematics endpoint-bound and non-ornamental;
- engineering guidance explicitly non-field-validation;
- all 23 PDF pages visually inspected;
- Supplement S2 self-check PASS;
- independent clean rebuild = **23 pages / 0 changed pages / 0.0% changed pixels**.

Role Model gate:
- Teach: PASS;
- Prove: PASS;
- Translate: PASS;
- Persuade: PASS;
- Field-Native Glossary: PASS;
- Scientific Red Hat: PASS;
- Editorial Red Hat: PASS.

Residual reviewer risks — disclosed, not blockers:
1. a matched durable MQTT comparator may be requested for stronger architecture-superiority claims;
2. three FIT run-level replicates limit inferential breadth;
3. literature audit is targeted, not exhaustive/systematic;
4. POWDER remains descriptive characterization, not architecture treatment-effect estimation.

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
- commercialization verdict remains `NO_IP_ACTION -> PUBLISH`.

## Publication lane

1. P20A — 15% — **PASS / historical literature baseline**
2. P20B / R1-R6 — 15% — **PASS / ELSEVIER ROUTE CURRENT**
3. P20C — 15% — **PASS**
4. **P20D-R5 — 25% — PASS / CURRENT ROLE MODEL MANUSCRIPT AUTHORITY**
5. **P20E-R5 — 20% — PASS / SCIENTIFIC + EDITORIAL RED-HAT CLEARED**
6. **P21-R5 — Author Submission Authorization Packet — 5% — NEXT / NOT STARTED**
7. P22 — Submission Execution & Receipt — 5% — LOCKED

Earned progress: **90/100**.

## Exact next gate — P21-R5

P21-R5 may prepare an internal author-authorization packet against the **exact R5 package above**. It must recheck current Editorial Manager requirements, concurrent-submission state, author/ORCID/contact metadata, file-role mapping, and Subscription/non-OA route.

P21-R5 must not submit externally and must not infer authorization from `continue`, `go on`, `next`, journal preference, manuscript approval, or historical P21 packets.

P22 remains locked until a new explicit author authorization based on the exact R5 bytes.

## Stop state

`WP2_P20D_R5=PASS_ROLE_MODEL_DOCTRINE_REBUILD`

`R5_CURRENT_MANUSCRIPT_AUTHORITY=YES`

`WP2_P20E_R5_SCIENTIFIC_RED_HAT=PASS`

`WP2_P20E_R5_EDITORIAL_RED_HAT=PASS`

`ROLE_MODEL_PAPER_GATE=PASS`

`PUBLICATION_LANE_PROGRESS=90_OF_100`

`P21_R4=SUPERSEDED_BY_R5_BYTES`

`P21_R5=NEXT_NOT_STARTED`

`P22_LOCKED=YES`

`PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`

`CURRENT_PHASE=STOP_AFTER_P20E_R5_PASS`

`SUBMISSION_AUTHORIZED=NO`
