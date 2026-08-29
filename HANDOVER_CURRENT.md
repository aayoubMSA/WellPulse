# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P20D-R1 production-compliance repair + WP2-P20E independent submission-readiness PASS**.  
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
- P20D initial IEEE integration package: **PASS / HISTORICAL PRODUCTION PACKAGE**
- P20D-R1 bounded IEEE production-compliance repair: **PASS / CURRENT SUBMISSION-PACKAGE AUTHORITY**
- P20E independent submission-readiness validation: **PASS**
- current scientific blockers: **0**
- current production blockers: **0**
- new experiment required: **NO**
- new empirical claim required: **NO**
- submission authorization: **NO**

Publication-lane progress: **90/100**.

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
20. `analysis/WP2_P20D_FINAL_IEEE_MANUSCRIPT_SOURCE_PACKAGE_INTEGRATION_2026-08-29.md` — historical initial production package
21. `docs/WP2_P20D_FINAL_IEEE_MANUSCRIPT_SOURCE_PACKAGE_CLOSURE_2026-08-29.md`
22. `analysis/WP2_P20D_R1_IEEE_PRODUCTION_COMPLIANCE_REPAIR_2026-08-29.md`
23. `docs/WP2_P20D_R1_IEEE_PRODUCTION_COMPLIANCE_REPAIR_CLOSURE_2026-08-29.md`
24. `analysis/WP2_P20E_INDEPENDENT_SUBMISSION_READINESS_VALIDATION_2026-08-29.md`
25. `docs/WP2_P20E_INDEPENDENT_SUBMISSION_READINESS_VALIDATION_CLOSURE_2026-08-29.md`
26. Research & Grants Lessons Learned Ledger: **LL-047 master venue doctrine + LL-048 canonical publication identity**.
27. P9 forensic authorities only when exact POWDER trace/caveat semantics are required.

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

Current manuscript integrates:

- Mohammed et al. 2026, DOI `10.48084/etasr.16945`;
- Im and Lim 2023 E-MQTT, DOI `10.3390/app132212419`;
- Radwan et al. 2026, DOI `10.1038/s41598-026-66865-8`.

Gaspar et al. DOI `10.1109/MIOT.2026.3681190` remains bibliographic/scope-only unless full text is directly recovered.

Defensible contribution: failure-domain-aware evaluation separating application record-state survival from communication-path recovery, combining receiver-reconciled embedded durability evidence with separately executed controlled path characterization while preserving endpoint semantics and avoiding pooled reliability inference.

## Venue authority

Selected target: **IEEE Internet of Things Journal**.

Route: **Traditional / non-OA**.

Current IoT-J rules reverified during P20D/P20E:

- manuscript in IEEE double-column journal style;
- abstract 150–250 words, one paragraph;
- ORCID required for all authors at submission/proof stages;
- mandatory USD 175/page charge beyond the first eight published pages; submission signifies acceptance of the requirement;
- Traditional route has no OA APC;
- IEEE copyright form remains a downstream action;
- substantive AI use must be disclosed in the Acknowledgment;
- supplementary collections are separate upload items and require adequate README information.

Validated R1 IEEEtran author build = **6 pages** and abstract = **221 words**. Production pagination can still change. No overlength payment is authorized.

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
- affiliation: **Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt**;
- research funding: **no external funding**;
- competing interests: **none currently identified**;
- FIT IoT-LAB and POWDER acknowledgments required and present;
- CRediT statement present;
- IEEE generative-AI disclosure present;
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

P20D/P20D-R1 create publication-safe derivatives without changing frozen authorities. F1-F4 metadata normalization to `Ahmed Ayoub` produced **0.0% rendered-pixel change**. Submission-safe P19 supplement excludes `__pycache__/*.pyc`; isolated self-check PASS.

## Current production authority — P20D-R1

Archive:
`WellPulse_P20D_R1_IEEE_Submission_Package_2026-08-29.zip`

Drive ID:
`1j61flpHqrVlR_c-Hu1ueUjl5p2RQwhGG`

Archive size:
`3,601,271 bytes`

Archive SHA-256:
`73b46d0b19cfd74689bdc10efb27c71a5460ca1c9ab6843503155a87696eb73c`

Drive raw read-back SHA-256: **exact match / PASS**.

Submission-draft PDF SHA-256:
`95917105f9d03fce155b9cc2a579d2e0e6f567a30557f87f82382db193597fa1`

TeX SHA-256:
`0e0c64ba0552f2e71e8a00e4cc29a35da908b7f0996a5a94db34e36d2ef644ef`

Submission-safe P19 supplement ZIP SHA-256:
`99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`

The earlier P20D archive at Drive ID `19K3gB9TY4znMZmGHw_DQHZnM9ee_eMSx` remains historical production evidence but is superseded for submission-readiness by P20D-R1.

## P20E independent validation authority

P20E independently extracted and rebuilt the exact P20D-R1 archive.

PASS evidence:

- outer archive/Drive read-back hash exact;
- root manifest 66/66 and SHA list 67/67 valid;
- nested P19 manifest 53/53 valid;
- PDF = 6 pages, US Letter, unencrypted text PDF;
- fonts embedded;
- independent TeX rebuild = 6 pages;
- rebuild visual diff = **0 changed pages / 0.0% pixels**;
- abstract = 221 words;
- publication name consistency = `Ahmed Ayoub`, expanded variants 0;
- P19 isolated scientific self-check PASS;
- cache files 0;
- no detected private IPv4 or exposed credential value in reviewer-facing corpus;
- key FIT and POWDER values independently recomputed and match frozen authorities;
- P20A comparator/novelty boundaries preserved;
- forbidden claim families absent;
- AI disclosure / CRediT / funding / COI / FIT / POWDER statements present;
- supplementary README compliant with current IEEE collection-description expectations.

`SCIENTIFIC_BLOCKERS=0`

`PRODUCTION_BLOCKERS=0`

## Publication lane

1. P20A — 15% — **PASS**
2. P20B / R1-R5 — 15% — **PASS**
3. P20C — 15% — **PASS**
4. P20D / R1 — 25% — **PASS**
5. P20E — 20% — **PASS**
6. **P21 — Author Submission Authorization Packet — 5% — NEXT / UNLOCKED**
7. P22 — Submission Execution & Receipt — 5% — LOCKED

Earned progress: **90/100**.

## Exact next gate — WP2-P21

P21 is the only next executable gate. It prepares an author-facing authorization packet; it does **not** submit.

P21 must surface and verify:

1. exact target = IEEE Internet of Things Journal;
2. exact route = Traditional / non-OA;
3. exact manuscript/PDF/supplement archive hashes from P20D-R1;
4. exact publication identity = Ahmed Ayoub;
5. exact ORCID linked to Ahmed Ayoub in the submission account;
6. confirmation that this manuscript is not under active consideration elsewhere;
7. explicit author awareness that IoT-J states submission signifies acceptance of mandatory overlength charges if final published length exceeds eight pages, despite the current 6-page author build;
8. main-manuscript vs supplement vs optional separate-graphics portal upload mapping;
9. copyright form remains downstream, not pre-authorized;
10. final explicit author decision: `AUTHORIZE_SUBMISSION=YES/NO`.

P21 may prepare all metadata and portal mapping, but must stop before any external submission/copyright/payment action. P22 remains locked until the user explicitly authorizes submission after seeing P21.

## Stop state

`WP2_P20D_R1=PASS_BOUNDED_IEEE_PRODUCTION_COMPLIANCE_REPAIR`

`WP2_P20E=PASS_INDEPENDENT_SUBMISSION_READINESS_VALIDATION`

`PUBLICATION_LANE_PROGRESS=90_OF_100`

`P21_UNLOCKED=YES`

`P22_LOCKED=YES`

`OVERLENGTH_PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_ACCEPTANCE_AUTHORIZED=NO`

`CURRENT_PHASE=WP2_P21_GATE_NOT_STARTED`

`SUBMISSION_AUTHORIZED=NO`
