# WellPulse — Current Handover

Last updated: 2026-08-29 after **P20B-R6 venue switch + P20D-R2 survey-visible Elsevier build + P20E-R2 PASS + P21-R2 packet ready**.  
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
- P17 manuscript + dossier: **PASS**
- P17V independent claim validation: **PASS / 9 OF 9**
- P18R deterministic F1 hotfix: **PASS / SCIENTIFIC-TOPOLOGY AUTHORITY**
- P18RC production main figures: **PASS / FIGURE AUTHORITY**
- P19 reviewer/reproducibility artifact: **PASS**
- P20A literature & novelty closure: **PASS / 17-GROUP AUDIT AUTHORITY**
- P20B-R1 through R5: **PASS / HISTORICAL VENUE RANKING**
- **P20B-R6 desk-triage reweighting: PASS / INTERNET OF THINGS (ELSEVIER) SELECTED**
- P20C authorship/credits/rights/IP lock: **PASS**
- IEEE P20D/R1 + P20E + P21: **HISTORICAL / SUPERSEDED FOR CURRENT ROUTE**
- **P20D-R2 Elsevier survey-visible integration: PASS / CURRENT PRODUCTION AUTHORITY**
- **P20E-R2 independent Elsevier validation: PASS**
- **P21-R2 Elsevier authorization packet: PASS / AUTHOR DECISION PENDING**
- P22 submission execution & receipt: **LOCKED**
- scientific blockers: **0**
- production blockers: **0**
- new experiment required: **NO**
- submission authorized: **NO**

Publication-lane earned progress: **95/100**.

## Global publication identity — HARD RULE

Research & Grants experience-ledger authority: **LL-048**.

Publication-facing name is exactly:

**Ahmed Ayoub**

Do not use expanded variants in manuscripts, portal metadata, CRediT, citations, correspondence, repository release metadata, ORCID/Scopus/Google-Scholar-facing records, or submission artifacts unless explicitly overridden for a specific legal/administrative form.

## Active manuscript-presentation requirement

The author explicitly requires that the paper **properly show the effort performed in the literature survey**.

Operational meaning:

- the survey/novelty audit must remain visible in the main manuscript;
- do not collapse it back into a few related-work sentences merely to shorten the paper;
- preserve the seven search/comparator axes, main-text synthesis table and explicit audit outcome;
- preserve the full source-by-source audit as supplementary material;
- describe it accurately as a **targeted submission-date novelty audit**, not a PRISMA/systematic review/meta-analysis unless future work actually satisfies such a protocol.

`SURVEY_VISIBILITY_REQUIREMENT=ACTIVE`

## Historical scored state — immutable

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No later evidence may be relabelled as scored P7B success.

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
3. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
4. `docs/WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION_CLOSURE_2026-08-29.md`
5. `docs/WP2_P19_REVIEWER_SUPPLEMENT_SANITIZED_ARTIFACT_CLOSURE_2026-08-29.md`
6. `analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md`
7. `analysis/WP2_P20B_R6_DESK_TRIAGE_PRIORITY_VENUE_SWITCH_2026-08-29.md`
8. `docs/WP2_P20B_R6_DESK_TRIAGE_PRIORITY_VENUE_SWITCH_CLOSURE_2026-08-29.md`
9. `analysis/WP2_P20C_AUTHORSHIP_CREDITS_RIGHTS_IP_LOCK_2026-08-29.md`
10. `analysis/WP2_P20D_R2_ELSEVIER_IOT_SURVEY_VISIBLE_INTEGRATION_2026-08-29.md`
11. `docs/WP2_P20D_R2_ELSEVIER_IOT_SURVEY_VISIBLE_INTEGRATION_CLOSURE_2026-08-29.md`
12. `analysis/WP2_P20E_R2_INDEPENDENT_ELSEVIER_SUBMISSION_READINESS_VALIDATION_2026-08-29.md`
13. `docs/WP2_P20E_R2_INDEPENDENT_ELSEVIER_SUBMISSION_READINESS_VALIDATION_CLOSURE_2026-08-29.md`
14. `docs/WP2_P21_R2_ELSEVIER_AUTHOR_SUBMISSION_AUTHORIZATION_PACKET_2026-08-29.md`
15. Research & Grants Lessons Learned Ledger: **LL-047 venue doctrine + LL-048 publication identity**.

Old IEEE P20D/P20E/P21 artifacts remain historical audit/back-up material only. Do not use the old IEEE P21 packet for P22.

## Frozen scientific doctrine

### FIT — record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

`B0/W1 × C0/C1/C2 × 3 runs = 18 cells`, exactly 10,000 records/run.

- C0 B0/W1 = 100% all runs;
- C1 B0 = 80%, W1 = 100%;
- C2 B0 = 80%, W1 = 100%;
- B0 C1/C2 permanently miss exactly 2,000 records/run;
- W1 final reconciliation contains all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`.

These are run-level repeated outcomes under exact treatments, not population reliability probabilities. C2 is gateway-process `exec` restart, not node reboot. B0 is non-durable and is not the strongest durable MQTT comparator.

### POWDER — communication-path characterization

WP2-P8 profile `srslte-controlled-rf` is a separately executed physical-RF/LTE/MQTT controlled reference characterization, not architecture-effect estimation.

- E1/E2/E3 transition region is experiment-specific; 52 dB is not universal;
- E8 isolates broker/service failure while LTE remains healthy;
- E9 is no-fault control;
- E10-A remains censored with no scalar recovery latency;
- E10-D is an upper bound only;
- receiver-side unique-ID reconciliation governs delivery;
- FIT and POWDER are complementary/non-substitutable and are not statistically pooled.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Immutable claim prohibitions

Never claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB; deterministic RF-only recovery; exact E10-D broker recovery latency; population reliability from message counts/three FIT runs; pooled FIT+POWDER inference; historical firstness for persistence/store-and-forward/end-to-end acknowledgment; or unsupported field/rural/pump/hydraulic/groundwater/agronomic/industrial-process validation.

## P20A literature / survey authority

The submission-date novelty audit uses seven axes:

1. MQTT persistence, sessions, QoS state and retransmission;
2. MQTT/IoT robustness, stress testing and fault injection;
3. offline-first, edge/cloud continuity and store-and-forward;
4. downstream acknowledgment / receiver confirmation and durable application persistence;
5. failure-domain-aware resilience/recovery evaluation;
6. real wireless/IoT testbeds, repeatability and reproducibility;
7. receiver-side identity reconciliation/provenance where materially related.

Audit result:

- retained source/axis groups: **17**;
- wording-narrowing groups: **11**;
- no-impact/context groups: **6**;
- scientific blockers: **0**.

Material/current comparators include Mohammed et al. 2026 DOI `10.48084/etasr.16945`, Im & Lim E-MQTT DOI `10.3390/app132212419`, Radwan et al. 2026 DOI `10.1038/s41598-026-66865-8`, and the FIT/POWDER platform/testbed literature. Gaspar et al. DOI `10.1109/MIOT.2026.3681190` remains bibliographic/scope-only unless full text is directly recovered.

Defensible contribution: failure-domain-aware evaluation separating application record-state survival from communication-path recovery, combining receiver-reconciled embedded durability evidence with separately executed controlled path characterization while preserving mechanism-specific endpoint semantics and avoiding pooled reliability inference.

## Current venue / route authority — P20B-R6

Selected first route:

**Internet of Things (Elsevier)**

Initial route:

**Subscription / non-OA**

Reason for switch from IEEE IoT-J:

- the author elevated **editorial triage / desk-decision speed** as a material objective distinct from average peer-review first-decision time;
- Elsevier IoT was already nearly tied with IEEE in the 8-axis ranking;
- current official scope directly covers IoT reliability, software engineering, testbeds and quality assurance, Full Research papers, Survey Papers, Open Software and Data, and practitioner-facing engineering;
- the journal explicitly states high priority on timely publication;
- the Elsevier format allows the survey effort and evidence architecture to remain visible without an IEEE eight-page overlength pressure.

Backup 1: **IEEE Internet of Things Journal**.

No APC or paid OA route is authorized.

## Publication identity / disclosures

- sole/corresponding author: **Ahmed Ayoub**;
- affiliation: **Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt**;
- institutional email: `aelsayedo@msa.edu.eg`;
- canonical ORCID: `0009-0004-7895-3191`;
- research funding: **no external research funding**;
- competing interests: **none currently identified**;
- FIT IoT-LAB and POWDER acknowledgment/citation: present;
- CRediT: present;
- Data availability: present;
- Elsevier generative-AI declaration: present immediately before References;
- repository public disclosure already exists; no patentability claim;
- commercialization verdict: `NO_IP_ACTION -> PUBLISH`;
- repository software licence remains unactivated pending authority-to-license verification.

## Current production authority — P20D-R2

Archive:
`WellPulse_P20D_R2_Elsevier_IoT_Submission_Package_2026-08-29.zip`

Drive ID:
`163sZVVq2qRQn8EPnZDniRLxgoOCY2lK7`

Size:
`2,132,191 bytes`

Archive SHA-256:
`43d9cba4c14fcfc17d0c8d11e18ff3ee82ab3a3a8ee7b57e60db46634e025f89`

Drive raw read-back: **exact hash match / PASS**.

Main PDF:
`WellPulse_Elsevier_IoT_P20D_R2_SubmissionDraft.pdf`

- 16 pages;
- approximately 4,682 words;
- SHA-256 `46953e6f8c579faf040d8f7cbf342e200ec603b205832abbd73d3c3434b8f2a0`.

Survey S1 PDF SHA-256:
`a098f1f366ff1d152b7e27524f454393620b93f31df563417749a28f86804017`

P19 reproducibility supplement SHA-256:
`99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`

Five Highlights are present and all are <=85 characters.

## P20E-R2 independent validation authority

PASS:

- independent rebuild: **16 pages**;
- packaged-versus-rebuild render diff: **0 changed pages / 0.0% changed pixels**;
- all fonts embedded;
- survey CSV: **17 rows / 11 wording-narrowing / 6 no-impact / 0 blockers**;
- survey aggregate counts match main paper/P20A;
- manuscript correctly identifies the survey as targeted novelty audit, not systematic review;
- P19 isolated `python -I artifact_selfcheck.py`: **PASS**;
- cache files: **0**;
- publication identity/declarations: PASS;
- key FIT/POWDER numerical spot checks: PASS;
- novelty boundaries: PASS;
- forbidden claim families: absent;
- scientific blockers: **0**;
- production blockers: **0**.

## Current P21-R2 authorization authority

`docs/WP2_P21_R2_ELSEVIER_AUTHOR_SUBMISSION_AUTHORIZATION_PACKET_2026-08-29.md`

Concurrent-submission evidence check:

- exact title Gmail search: **0 results**;
- broader WellPulse/Elsevier/Editorial Manager search: no relevant manuscript-submission record;
- canonical repo contains no submission receipt.

This supports `CONCURRENT_SUBMISSION_EVIDENCE_FOUND=NO`, but the author must explicitly confirm no concurrent submission because absence of email cannot prove every external portal action.

Portal file map:

- main: `WellPulse_Elsevier_IoT_P20D_R2_SubmissionDraft.pdf`;
- Highlights: `highlights.txt` (convert to Word only if the live portal requires it, without wording change);
- survey supplement: `Supplement_S1_Literature_Novelty_Audit.pdf` + `.csv`;
- reproducibility supplement: `WellPulse_P19_REPRODUCIBILITY_SUPPLEMENT.zip`;
- TeX/F1-F4/alt text retained for portal/production requests;
- outer ZIP is archival authority, not a single portal upload.

## Publication lane

1. P20A — 15% — **PASS**
2. P20B / R1-R6 — 15% — **PASS / ELSEVIER ROUTE CURRENT**
3. P20C — 15% — **PASS**
4. P20D / R2 — 25% — **PASS**
5. P20E / R2 — 20% — **PASS**
6. P21 / R2 — 5% — **PASS / PACKET READY / AUTHOR DECISION PENDING**
7. **P22 — Submission Execution & Receipt — 5% — LOCKED**

Earned progress: **95/100**.

## Exact next gate — author decision, then P22 only if YES

To unlock P22, the author must explicitly confirm that the WellPulse manuscript is not currently under consideration elsewhere and choose:

`AUTHORIZE_ELSEVIER_SUBMISSION=YES`

or

`AUTHORIZE_ELSEVIER_SUBMISSION=NO`

A generic `continue`, `go on`, or venue preference must not be interpreted as external submission authorization.

If and only if YES, P22 may open the current Elsevier submission portal, verify live portal metadata/file roles, upload the validated artifacts, and submit only if no new paid/open-access/licence/material condition appears. Any unexpected financial or rights commitment remains a separate author-controlled gate.

## Stop state

`WP2_P20B_R6=PASS_DESK_TRIAGE_PRIORITY_SWITCH`

`VENUE_SELECTED=ELSEVIER_INTERNET_OF_THINGS`

`WP2_P20D_R2=PASS_ELSEVIER_IOT_SURVEY_VISIBLE_INTEGRATION`

`WP2_P20E_R2=PASS_INDEPENDENT_ELSEVIER_SUBMISSION_READINESS_VALIDATION`

`WP2_P21_R2=PASS_PACKET_READY_AUTHOR_DECISION_PENDING`

`PUBLICATION_LANE_PROGRESS=95_OF_100`

`P22_LOCKED=YES`

`PAYMENT_AUTHORIZED=NO`

`CURRENT_PHASE=AUTHOR_ELSEVIER_SUBMISSION_AUTHORIZATION_DECISION`

`SUBMISSION_AUTHORIZED=NO`
