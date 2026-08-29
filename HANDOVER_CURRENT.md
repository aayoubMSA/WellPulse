# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P20D PASS — final IEEE manuscript/source package integration**.  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This is the canonical operational retrieval point. GitHub is the scientific/control record; Google Drive is the durable authority for frozen/raw binary evidence and archived production packages. Repository/Drive evidence overrides chat memory.

## Executive state

- P8 manual POWDER campaign: **COMPLETE / GOLDEN / MANUAL REFERENCE**
- P9 forensic reconciliation: **PASS**
- P10 scientific analysis contract: **PASS / FROZEN**
- P11 full raw-data scientific analysis: **PASS**
- P12 cross-evidence integration: **PASS**
- P13 claim–evidence matrix: **PASS / FROZEN CLAIM AUTHORITY**
- P16 adversarial publication QA: **PASS**
- P17 consortium manuscript + dossier: **PASS**
- P17V independent validation: **PASS / 9 OF 9 CLAIMS VALIDATED**
- P18R deterministic F1 hotfix: **PASS / SCIENTIFIC-TOPOLOGY AUTHORITY**
- P18RC main-figure production normalization: **PASS / CURRENT FIGURE AUTHORITY**
- P19 reviewer supplement + sanitized artifact: **PASS / CURRENT REVIEWER-ARTIFACT AUTHORITY**
- post-P19 WP architecture review: **PASS**
- P20A literature & novelty closure: **PASS / CURRENT NOVELTY AUTHORITY**
- P20B original Elsevier-heavy ranking: **HISTORICAL / SUPERSEDED**
- P20B-R1 through R4: **PASS**
- P20B-R5 final venue selection: **PASS / IEEE INTERNET OF THINGS JOURNAL SELECTED**
- P20C authorship / credits / rights / IP lock: **PASS**
- P20D final IEEE manuscript & source package integration: **PASS**
- current scientific blockers: **0**
- new experiment required: **NO**
- new empirical claim required: **NO**
- submission authorization: **NO**

Publication-lane progress: **70/100**.

## Global publication identity — HARD RULE

Research & Grants experience-ledger authority: **LL-048**.

The scholarly publication name is exactly:

**Ahmed Ayoub**

Do not use expanded variants in manuscripts, portal metadata, CRediT, citations, publication correspondence, repository release metadata, ORCID/Scopus/Google-Scholar-facing records, or submission artifacts unless the author explicitly overrides this rule for a specific legal/administrative form.

## Historical scored state — unchanged

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
8. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md` — historical scientific baseline only
9. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
10. `manuscript/WP2_P18R_F1_HOTFIX_QA_2026-08-29.md`
11. `docs/WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION_CLOSURE_2026-08-29.md`
12. `docs/WP2_P19_REVIEWER_SUPPLEMENT_SANITIZED_ARTIFACT_CLOSURE_2026-08-29.md`
13. `analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md`
14. `docs/WP2_P20A_LITERATURE_NOVELTY_CLOSURE_2026-08-29.md`
15. `analysis/WP2_P20B_R4_CONSORTIUM_VENUE_AXIS_COMPLETENESS_REVIEW_2026-08-29.md`
16. `analysis/WP2_P20B_R5_FINAL_MULTIAXIS_VENUE_SCORING_2026-08-29.md`
17. `docs/WP2_P20B_R5_FINAL_VENUE_SELECTION_CLOSURE_2026-08-29.md`
18. `analysis/WP2_P20C_AUTHORSHIP_CREDITS_RIGHTS_IP_LOCK_2026-08-29.md`
19. `docs/WP2_P20C_AUTHORSHIP_CREDITS_RIGHTS_IP_CLOSURE_2026-08-29.md`
20. `analysis/WP2_P20D_FINAL_IEEE_MANUSCRIPT_SOURCE_PACKAGE_INTEGRATION_2026-08-29.md`
21. `docs/WP2_P20D_FINAL_IEEE_MANUSCRIPT_SOURCE_PACKAGE_CLOSURE_2026-08-29.md`
22. Research & Grants Lessons Learned Ledger: **LL-047 master venue doctrine + LL-048 canonical publication identity**.
23. P9 forensic authorities only when exact POWDER trace/caveat semantics are required.

## Frozen scientific doctrine

### FIT — record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

`B0/W1 × C0/C1/C2 × 3 runs = 18 cells`, exactly 10,000 records/run.

- C0 B0/W1 = 100% all runs;
- C1 B0 = 80%, W1 = 100% all runs;
- C2 B0 = 80%, W1 = 100% all runs;
- B0 C1/C2 permanently miss exactly 2,000 records/run;
- W1 final reconciliation contains all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`.

These are repeated run-level outcomes under exact treatments, not population reliability probabilities. C2 is gateway-process `exec` restart, not node reboot. B0 is non-durable and is not the strongest durable MQTT comparator.

### POWDER — communication-path characterization

WP2-P8 profile `srslte-controlled-rf` is a separately executed physical-RF/LTE/MQTT controlled reference characterization; it is **not architecture-effect estimation**.

- E1/E2/E3 transition region is experiment-specific; 52 dB is not universal;
- E8 isolates broker/service failure while LTE remains healthy;
- E9 is no-fault control;
- E10-A has no scalar recovery latency and remains censored;
- E10-D is an upper bound only;
- receiver-side unique-ID reconciliation governs delivery.

FIT and POWDER are complementary/non-substitutable and are not statistically pooled.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Immutable claim prohibitions

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- generic `WellPulse beats MQTT`;
- universal 52 dB threshold;
- deterministic RF-only recovery;
- exact broker recovery latency from E10-D;
- population reliability from message counts or three FIT runs;
- pooled FIT+POWDER inference;
- historical firstness for persistence, store-and-forward, subscriber/end-to-end acknowledgment, or generic offline recovery;
- unsupported field/rural/pump/hydraulic/groundwater/agronomic/industrial-process validation.

## P20A novelty authority

P20D has integrated the required current comparators:

- Mohammed et al. 2026, DOI `10.48084/etasr.16945`;
- Im and Lim 2023 E-MQTT, DOI `10.3390/app132212419`;
- Radwan et al. 2026, DOI `10.1038/s41598-026-66865-8`.

Gaspar et al. DOI `10.1109/MIOT.2026.3681190` remains bibliographic/scope-only unless full text is directly recovered.

Defensible contribution: failure-domain-aware evaluation separating application record-state survival from communication-path recovery, combining receiver-reconciled embedded durability evidence with separately executed controlled path characterization while preserving endpoint semantics and avoiding pooled reliability inference.

## Venue authority

Selected target: **IEEE Internet of Things Journal**.

Route: **Traditional / non-OA**.

Current IoT-J rule reverified at P20D: mandatory USD 175/page charges apply beyond the first eight published pages; submission signifies acceptance of that requirement.

P20D IEEEtran author build = **6 pages**, creating two pages of author-build headroom. Production pagination can still change. No overlength payment is authorized.

Backup ranking remains:

1. IEEE IoT-J — selected;
2. Internet of Things (Elsevier);
3. Scientific Reports — agreement-advantaged route;
4. ACM Transactions on Internet of Things;
5. Computer Networks;
6. IEEE TNSM;
7. Telecommunication Systems.

## P20C publication identity / rights authority

- sole author: **Ahmed Ayoub**;
- corresponding author: **Ahmed Ayoub**;
- affiliation: **Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City, Egypt**;
- research funding: **no external funding**;
- competing interests: **none currently identified**;
- FIT IoT-LAB and POWDER acknowledgments required;
- CRediT statement required;
- IEEE generative-AI disclosure required;
- repository is already public; prior public disclosure exists;
- no patentability claim;
- current commercialization verdict: `NO_IP_ACTION -> PUBLISH`;
- repository software licence not activated pending authority-to-license verification;
- IEEE copyright acceptance remains downstream and author-controlled.

## P18RC / P19 authorities

P18RC archive:
`WellPulse_P18RC_Main_Figure_Production_Normalization_2026-08-29.zip`
Drive ID `1rdFq7ktppFBUp54UoeS5AP3kukDiU9sW`
SHA-256 `97f0fd1e4c41bb67f6da70056935b60a1627695e082ea8d38eff657bce1d02a8`

Authoritative F1-F4 PDF SHA-256:
- F1 `7d7feb075731475747282cf0dd0081ec6afb1bc45c17bd16c754063ac83237cb`
- F2 `73b96a2b8c1fa2a4c15b3bd15b0065f77a2863dcacb84d8c3f2d7d0b57cef508`
- F3 `faccbef11762df7c293728992e59ac9b17e4b455e4d2023dcddeb50f41e5e9b8`
- F4 `87d2c703e4308477b3d89c5d0a9594a7380f2e0c8350d5d74721f779785a1b38`

P19 archive:
Drive ID `1t5S_L-S0hfmyMPLdXh8Fd-jGBOH8SCkl`
SHA-256 `5a9ed4fa197ea5c3aa43447fabf16d7928aeabe58722e16af63afe25bc7cfdc7`

P20D creates publication-safe derivatives without changing frozen authorities. F1-F4 metadata normalization to `Ahmed Ayoub` produced **0.0% rendered-pixel change** for every figure. P19 externalized supplement removes `__pycache__/*.pyc`; isolated self-check PASS.

## P20D durable authority

Archive:
`WellPulse_P20D_IEEE_Submission_Package_2026-08-29.zip`

Drive ID:
`19K3gB9TY4znMZmGHw_DQHZnM9ee_eMSx`

Archive size:
`3,597,127 bytes`

Archive SHA-256:
`3377b6c13c53f47594d75c50419bceaee87e81e4450f000dcf01054b78706f0b`

Drive raw read-back SHA-256: **exact match / PASS**.

Submission-draft PDF SHA-256:
`a3737379e4688ef64b4b95ba3350ad29ae5e90563a5a45f384f92b50e2d729ca`

TeX SHA-256:
`249b73d004728cb39cd5e34621985b3b8c5794185824951ecdb549a7db52fd01`

Submission-safe P19 supplement ZIP SHA-256:
`a8dc2e789fed93c5f18ebc17cbf7ae2f66514dfdc157770d5fd5abded3d7fac5`

## Publication lane

1. P20A — 15% — **PASS**
2. P20B / R1-R5 — 15% — **PASS**
3. P20C — 15% — **PASS**
4. P20D — 25% — **PASS**
5. **P20E — Independent Submission-Readiness Validation — 20% — NEXT / NOT STARTED**
6. P21 — Author Submission Authorization Packet — 5% — LOCKED
7. P22 — Submission Execution & Receipt — 5% — LOCKED

Earned progress: **70/100**.

## Exact next gate — WP2-P20E

P20E must be an independent red-team validation of the exact P20D bytes/layout, not another authoring pass.

It must verify at minimum:

- exact PDF/source identity and hashes;
- all numerical claims against frozen authorities;
- P20A novelty boundaries and added references;
- LL-048 publication-name consistency everywhere submission-facing;
- author/affiliation/CRediT/funding/COI/testbed/AI statements;
- IEEE page-count and page-charge risk;
- figure legibility, grayscale/accessibility, captions and alt-text mapping;
- supplement manifest/self-check/privacy/security state;
- absence of legacy internal-control prose from submission-facing files;
- references and DOI integrity;
- no hidden scientific claim drift from P17V/P13;
- no payment/license/submission action.

P20E may PASS, PASS WITH FINITE FIXES, or FAIL. It must not submit externally.

## Stop state

`WP2_P20D=PASS_FINAL_IEEE_MANUSCRIPT_SOURCE_PACKAGE_INTEGRATION`

`PUBLICATION_LANE_PROGRESS=70_OF_100`

`P20E_UNLOCKED=YES`

`P21_LOCKED=YES`

`OVERLENGTH_PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_ACCEPTANCE_AUTHORIZED=NO`

`CURRENT_PHASE=WP2_P20E_GATE_NOT_STARTED`

`SUBMISSION_AUTHORIZED=NO`
