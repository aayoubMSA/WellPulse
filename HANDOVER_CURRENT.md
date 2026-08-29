# WellPulse — Current Handover

Last updated: 2026-08-29 after **P20D-R3/R3-R2 reference expansion + P20E-R3 red-hat PASS**.  
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
- P20A original 17-group literature closure: **PASS / HISTORICAL INPUT AUTHORITY**
- P20B-R1 through R5: **PASS / HISTORICAL VENUE RANKING**
- P20B-R6 desk-triage reweighting: **PASS / INTERNET OF THINGS (ELSEVIER) SELECTED**
- P20C authorship/credits/rights/IP lock: **PASS**
- IEEE P20D/R1 + P20E + P21: **HISTORICAL / SUPERSEDED FOR CURRENT ROUTE**
- Elsevier P20D-R2 + P20E-R2 + P21-R2: **HISTORICAL / SUPERSEDED BY R3-R2 BYTES**
- **P20D-R3/R3-R2 reference/survey expansion: PASS / CURRENT PRODUCTION AUTHORITY**
- **P20E-R3 red-hat adversarial review: PASS / CURRENT SUBMISSION-READINESS AUTHORITY**
- P21-R3 author authorization packet: **LOCKED / NOT STARTED**
- P22 submission execution & receipt: **LOCKED**
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

## Active manuscript-presentation requirement

The author explicitly requires that the paper **properly show the effort performed in the literature survey**.

Operational meaning:

- keep the literature/novelty audit visible in the main manuscript;
- do not collapse it into a few related-work sentences merely to shorten the paper;
- preserve the seven search axes, synthesis table, explicit audit outcome and full Supplement S1;
- describe it as a **targeted, claim-bounding submission-date novelty audit**, not a PRISMA systematic review/meta-analysis/exhaustive bibliographic census;
- do not trim survey visibility unless a verified venue rule or later editorial request creates a concrete requirement.

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
6. `analysis/WP2_P20A_COMPARATOR_NOVELTY_MATRIX_2026-08-29.md` — historical 17-group baseline
7. `analysis/WP2_P20B_R6_DESK_TRIAGE_PRIORITY_VENUE_SWITCH_2026-08-29.md`
8. `docs/WP2_P20B_R6_DESK_TRIAGE_PRIORITY_VENUE_SWITCH_CLOSURE_2026-08-29.md`
9. `analysis/WP2_P20C_AUTHORSHIP_CREDITS_RIGHTS_IP_LOCK_2026-08-29.md`
10. `analysis/WP2_P20D_R3_REFERENCE_SURVEY_EXPANSION_2026-08-29.md`
11. `analysis/WP2_P20E_R3_RED_HAT_ADVERSARIAL_SUBMISSION_REVIEW_2026-08-29.md`
12. `docs/WP2_P20E_R3_RED_HAT_ADVERSARIAL_SUBMISSION_REVIEW_CLOSURE_2026-08-29.md`
13. Research & Grants Lessons Learned Ledger: **LL-047 venue doctrine + LL-048 publication identity**.
14. P9 forensic authorities only when exact POWDER trace/caveat semantics are needed.

Old IEEE and Elsevier R2 P21 packets are historical only. **Do not use them to unlock P22.**

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

Run/replicate is the scientific unit. The 10,000 messages within each run are not 10,000 independent samples. C2 is gateway-process `exec` restart, not node/hardware reboot. B0 is non-durable and not the strongest durable MQTT comparator.

### POWDER — communication-path characterization

WP2-P8 profile `srslte-controlled-rf` is a separately executed physical-RF/LTE/MQTT controlled characterization, not architecture-effect estimation.

- E1/E2/E3 transition region is experiment-specific; 52 dB is not universal;
- E8 isolates broker/service failure while LTE remains healthy;
- E9 is no-fault control;
- E10-A remains censored with no scalar recovery latency;
- E10-B exact: 6.063318 s first MQTT, 6.609430 s first ping, 0.060172 s publish-to-CORE receipt;
- E10-C-B exact: 29.247733 s first ping, 29.248129 s first MQTT;
- E10-D is upper bound only, `<=10.908749 s`;
- receiver-side unique-ID reconciliation governs delivery;
- FIT and POWDER are complementary/non-substitutable and are not statistically pooled.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Immutable claim prohibitions

Never claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB; deterministic RF-only recovery; exact E10-D broker recovery latency; population reliability from message counts/three FIT runs; pooled FIT+POWDER inference; historical firstness for persistence/store-and-forward/end-to-end acknowledgment/offline recovery/testbed usage; or unsupported field/rural/pump/hydraulic/groundwater/agronomic/industrial-process validation.

## Current literature / survey authority — R3

The current manuscript uses a targeted submission-date novelty audit across seven axes:

1. MQTT persistence, sessions, QoS state and retransmission;
2. MQTT/IoT robustness, stress testing and fault injection;
3. offline-first, edge/cloud continuity and store-and-forward;
4. downstream acknowledgment / receiver confirmation and durable application persistence;
5. failure-domain-aware resilience/recovery evaluation;
6. real wireless/IoT testbeds, repeatability and reproducibility;
7. receiver-side identity reconciliation/provenance where materially related.

Current R3 audit composition:

- source/axis groups: **32**;
- peer-reviewed scholarly articles: **25**;
- normative MQTT standard: **1**;
- official technical/platform sources: **6**;
- wording-narrowing groups: **17**;
- contextual/no-impact groups: **15**;
- scientific blockers: **0**.

The 32-group R3 expansion supersedes the 17-group count **for the current manuscript only**; older P20A remains historical evidence of the earlier closure state.

The paper does not claim that the audit is systematic/exhaustive. It uses the audit to define the allowed claim envelope.

## Current venue / route authority

Selected first route:

**Internet of Things (Elsevier)**

Initial route:

**Subscription / non-OA**

Reason: fast editorial triage/desk-decision speed became a material author objective; Elsevier IoT remained scientifically strong and allows the survey/evidence architecture to remain visible without IEEE eight-page pressure.

Backup 1: **IEEE Internet of Things Journal**.

No APC, paid OA route, copyright/license acceptance or payment is authorized.

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
- Elsevier generative-AI declaration: present;
- repository public disclosure already exists; no patentability claim;
- commercialization verdict: `NO_IP_ACTION -> PUBLISH`;
- repository software licence remains unactivated pending authority-to-license verification.

## Current production authority — P20D-R3/R3-R2

Archive:
`WellPulse_P20D_R3R2_Elsevier_IoT_Submission_Package_2026-08-29.zip`

Drive ID:
`1Th-aO9_2wOnhD6EWyh5b6qml4fPmGDSb`

Archive size:
`2,157,349 bytes`

Archive SHA-256:
`6ca12912711f9f7b9f255bb161399244fac4572c7d902db0ad2270741b38496d`

Drive raw read-back: **exact hash match / PASS**.

Main PDF:
`WellPulse_Elsevier_IoT_P20D_R3R2_SubmissionDraft.pdf`

- pages: **19**;
- references: **32**;
- SHA-256: `d68c7b19a0785a4c8527156e93213ee4ac0582cccaccd95c28f815da6641c768`;
- publication name: **Ahmed Ayoub**;
- fonts: embedded;
- private IPv4 addresses: none detected;
- unresolved citation markers: 0.

Supplement S1:
- `Supplement_S1_Literature_Novelty_Audit.pdf`
- `Supplement_S1_Literature_Novelty_Audit.csv`
- rows: **32** / narrowing 17 / no-impact 15 / blockers 0.

Supplement S2:
`Supplement_S2_Reproducibility_Artifact.zip`

SHA-256:
`99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`

Isolated `python -I artifact_selfcheck.py`: **PASS**.

## Current red-hat authority — P20E-R3

Status: **PASS / NO SCIENTIFIC OR PRODUCTION BLOCKER**.

Finite defects found and fixed before freeze:

1. stale 17-group statement after expansion → corrected to 32;
2. pseudo-systematic-review risk → explicit source composition + claim-bounding/non-exhaustive qualification;
3. internal Gaspar retrieval-process wording → neutral scholarly scope treatment;
4. S2 label/file-role mismatch → normalized submission-facing filename.

Strongest surviving disclosed limitations:

- B0 is non-durable; no strongest-durable-MQTT superiority;
- FIT has three independent run-level replicates/cell; inference remains bounded/descriptive;
- audit is targeted/claim-bounding, not exhaustive/systematic;
- Gaspar detailed method/result comparison is not asserted;
- 19-page survey-visible manuscript is intentional under the active author objective.

Validation state:

- references: 32/32 cited;
- unresolved citation keys: 0;
- forbidden claim regression: 0;
- publication identity: PASS;
- S2 self-check: PASS;
- privacy/security scan: PASS;
- scientific blockers: 0;
- production blockers: 0.

## Publication lane

1. P20A — 15% — **PASS / historical literature baseline retained**
2. P20B / R1-R6 — 15% — **PASS / ELSEVIER ROUTE CURRENT**
3. P20C — 15% — **PASS**
4. P20D / R3-R2 — 25% — **PASS / CURRENT PRODUCTION AUTHORITY**
5. P20E / R3 — 20% — **PASS / RED-HAT CLEARED**
6. **P21-R3 — Author Submission Authorization Packet — 5% — LOCKED / NOT STARTED**
7. P22 — Submission Execution & Receipt — 5% — LOCKED

Earned progress: **90/100**.

## Exact next gate

The user has explicitly said **not yet** to submission progression. Therefore stop here.

If the author later asks to resume submission preparation, execute **P21-R3 only** against the exact R3-R2 bytes above. P21-R3 must recheck current portal requirements/concurrent-submission state and prepare an internal authorization packet. It must not infer authorization from `continue`, `go on`, venue preference, or prior P21 packets.

P22 remains locked until a new explicit author authorization based on the current R3-R2 package.

## Stop state

`WP2_P20D_R3=PASS_REFERENCE_SURVEY_EXPANSION`

`WP2_P20E_R3=PASS_RED_HAT_ADVERSARIAL_SUBMISSION_REVIEW`

`PUBLICATION_LANE_PROGRESS=90_OF_100`

`P21_R2=SUPERSEDED`

`P21_R3=LOCKED_NOT_STARTED`

`P22_LOCKED=YES`

`PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`

`CURRENT_PHASE=STOP_AFTER_RED_HAT_PASS`

`SUBMISSION_AUTHORIZED=NO`
