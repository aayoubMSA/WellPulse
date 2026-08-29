# WellPulse — Current Handover

Last updated: 2026-08-29 after **WP2-P17V — SUPERIOR INDEPENDENT CONSORTIUM VALIDATION**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from conversation memory.

## Executive scientific state

- WP0: **PASS / historical paper story superseded where necessary by P10 evidence-bounded contract**
- WP1: **PASS / frozen historical confirmatory design**
- WP2-P8 manual RF campaign: **COMPLETE / GOLDEN / MANUAL REFERENCE**
- WP2-P9 forensic reconciliation: **PASS / COMPLETE**
- WP2-P10 scientific analysis contract: **PASS / FROZEN**
- WP2-P11 full raw-data scientific analysis: **PASS / COMPLETE**
- WP2-P12 cross-evidence integration: **PASS / COMPLETE**
- WP2-P13 claim–evidence matrix: **PASS / FROZEN**
- WP2-P14 publication tables/figures: **PASS / FROZEN / historical main-display set**
- WP2-P15 manuscript construction: **PASS / historical internal full draft**
- WP2-P16 adversarial publication QA: **PASS / scientific QA complete**
- WP2-P17 dossier research pack + first consortium revision: **PASS / consortium-revised internal draft + QA**
- WP2-P17V superior independent validation: **PASS / VALIDATED WITH PRE-SUBMISSION CONDITIONS**
- new experiment required for current bounded manuscript: **NO**
- new empirical claims required: **NO**
- scientific blockers in P17V: **0**
- submission authorization: **NO**
- live POWDER dependency: **NONE**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8+ result may be promoted or relabelled as scored P7B.

## Mandatory read order for continuation

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
3. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
4. `analysis/WP2_P12_CROSS_EVIDENCE_INTEGRATION_2026-08-29.md`
5. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
6. `manuscript/WP2_P16_ADVERSARIAL_PUBLICATION_QA_2026-08-29.md`
7. `manuscript/WP2_P16_MANDATORY_EDITORIAL_PATCHES_2026-08-29.md`
8. `docs/WP2_P17_EXPERIMENT_DOSSIER_V2_2_RESEARCH_PACK_2026-08-29.md`
9. `analysis/WP2_P17_EVIDENCE_EXPLOITATION_MATRIX_2026-08-29.md`
10. `manuscript/WP2_P17_CONSORTIUM_MANUSCRIPT_REVIEW_2026-08-29.md`
11. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`
12. `manuscript/WP2_P17_CONSORTIUM_REVISION_QA_2026-08-29.md`
13. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
14. `manuscript/WP2_P17V_SUPERIOR_INDEPENDENT_CONSORTIUM_VALIDATION_2026-08-29.md`
15. P9 forensic authorities when exact POWDER trace/caveat semantics are required.
16. P14 display files only when auditing the historical display set; P18 is expected to redesign the main display set under a new QA gate.

## Frozen evidence roles

### FIT = architecture-level record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

- FIT IoT-LAB Grenoble A8-100;
- `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`;
- 10,000 records/cell;
- B0 = non-durable publish-only baseline;
- W1 = durable queue + receiver reconciliation;
- C0 healthy; C1 broker outage; C2 broker outage + gateway-process exec restart.

Principal results:

- C0: B0 100%, W1 100% in 3/3;
- C1: B0 80%, W1 100% in 3/3, `+20 pp` each run;
- C2: B0 80%, W1 100% in 3/3, `+20 pp` each run;
- each B0 C1/C2 run misses exactly 2,000/10,000 records, matching the imposed outage-period record block;
- every W1 final run contains all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`.

These are repeated outcomes under the exact treatment, not population reliability probabilities.

Canonical W1 implementation semantics:

- `record_id = run_id:boot_id:sequence` with zero-padded sequence;
- deterministic canonical JSON serialization;
- SHA-256 checksum;
- SQLite queue with WAL and `synchronous=FULL`;
- `PENDING` / `SENT` state;
- exact duplicate re-enqueue is idempotent;
- conflicting identity reuse raises an integrity error.

### POWDER = communication-path degradation/recovery characterization

Campaign: `WP2-P8`; profile `srslte-controlled-rf`.

Internal control classification:

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

Publication-facing role: **separately executed controlled reference characterization; not architecture-effect estimation**.

Principal evidence:

- E1R4 48–50 dB: ICMP clean, MQTT 20/20;
- E1R4 51 dB: ICMP 30% loss, MQTT 20/20;
- E1R4 52 dB: ICMP 60% loss, MQTT 13/20;
- E3 52 dB: ICMP loss `80/65/70%`, MQTT completeness `60/25/55%`;
- E8: broker interruption disrupts MQTT while LTE ping remains healthy;
- E9: no-fault control MQTT 60/60 with clean bidirectional ping;
- E10-A: no recovery observed inside preserved RF-only window; censored, no scalar latency;
- E10-B: action-begin→first MQTT publish `6.063318 s`; first ping `6.609430 s`; publish→CORE receipt `0.060172 s`;
- E10-C-B: RF restore→first ping `29.247733 s`; first publish `29.248129 s`;
- E10-D: `<=10.908749 s` upper bound only.

Receiver-side reconciliation is authoritative. Concrete examples: E1R4 seq 96 and E3 seq 150 are sender-present/receiver-absent without matching sender failure flags; E8 has 80 sender-log lines but only 60 unique IDs due to duplicated recovery sends.

Interpretation remains experiment-specific. No universal 52 dB threshold is claimed.

## Frozen integration doctrine

FIT and POWDER are complementary, not substitutable:

- **FIT = record-state survival / architecture comparison**.
- **POWDER = communication-path degradation / recovery characterization**.

The synthesis is **failure-domain-aware triangulation**. No pooled FIT+POWDER reliability statistic is allowed.

## Frozen claim envelope

P13 remains the scientific claim authority:

- primary empirical: `IC-01`, `IC-04`, `IC-06`;
- supporting empirical: `IC-02`, `IC-03`, `IC-05`, `IC-07`;
- methodological synthesis: `IC-08`, `IC-09`.

P17/P17V add no new empirical claims and do not expand P13.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## P17 durable research pack

Drive parent: `P12_WellPulse`  
Folder ID: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`

- dossier PDF `WellPulse_Experimental_Technical_Dossier_v2.2.pdf`
  - Drive ID `12ec22A89ybsNoBpYcglx9Im6pW8Vk55-`
  - SHA-256 `a9274514cbf21de58291c2640f560f6082711e0a8696890419e918e595b40f3e`
- reproducible dossier package Drive ID `1ts__z8kN0fORwDksQZoj4eeaG--UyCAw`
- experiment figure suite Drive ID `1y8rStzWdGEivWjuFCP0h5Y6Amv6267sY`
- figure-centered QA report Drive ID `1ukEvwr3_uOoZcCn3TknwOcZL6HRaLo1a`

Dossier role: **audit-grade experiment atlas / manuscript-supplement input**. Raw archives, P9 and P11 remain higher measurement authorities.

## P17 manuscript baseline

Canonical revised internal draft:

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`

Preferred working title:

**WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

P17 uses three empirical RQs and treats cross-testbed triangulation as synthesis rather than as a fourth pooled experiment.

`WP2_P17_QA=PASS_CONSORTIUM_REVISION_EVIDENCE_BOUNDED`

`P17_QA_UNSUPPORTED_CLAIMS=0`

`P17_QA_NUMERICAL_CONTRADICTIONS=0`

## P17V superior independent validation

A second, independent role-based consortium of 12 reviewers validated P17 against P11/P12/P13/P16, canonical code, forensic authorities and an independent current baseline/literature check.

Roles:

1. senior systems/meta-review editor;
2. MQTT protocol/persistence specialist;
3. embedded storage/crash-consistency reviewer;
4. wireless/RF experimentalist;
5. cellular/LTE systems reviewer;
6. experimental design/statistics reviewer;
7. causal/measurement-methodology reviewer;
8. reproducibility/forensic evidence auditor;
9. research-software reviewer;
10. literature/novelty meta-reviewer;
11. scientific-visualization reviewer;
12. adversarial associate-editor simulation.

Independent verdict:

**VALIDATED WITH PRE-SUBMISSION CONDITIONS.**

- claims validated: `9/9`;
- numerical contradictions: `0`;
- unsupported new claims: `0`;
- scientific blockers: `0`;
- new experiment required: `NO`.

Principal residual scientific limitation: B0 is non-durable and is not the strongest durable MQTT comparator. Independent official Paho documentation confirms that durable/persistent MQTT client state is established prior art. The current bounded paper remains defensible because it does not claim generic MQTT superiority.

P17V also independently reconfirmed the novelty boundary: persistence, retransmission, offline-first reconciliation, store-and-forward and testbed repeatability are prior art. The defensible contribution is the compound evaluation: failure-domain-aware framing + bounded embedded durability evidence + controlled physical-path characterization + endpoint-specific recovery semantics + receiver-side evidence preservation.

Gaspar et al. 2026 DOI `10.1109/MIOT.2026.3681190` is independently confirmed bibliographically. Detailed full-text comparison remains a pre-submission gate if accessible.

`P17V_VERDICT=VALIDATED_WITH_PRE_SUBMISSION_CONDITIONS`

## Authorship, affiliation, credits, rights

Canonical current author identity for internal project documents:

**Dr. Ahmed Elsayed Ayoub**  
Assistant Professor of Computer Engineering  
Department of Computer Systems Engineering  
Faculty of Engineering, MSA University  
Giza, Egypt

Do not invent coauthors, contributor roles, funding, copyright ownership, or licensing terms.

Before submission explicitly verify:

- final author list/order;
- CRediT/contributor roles;
- MSA affiliation wording;
- funding declarations;
- collaborator acknowledgments;
- FIT IoT-LAB citation/acknowledgment;
- POWDER citation/acknowledgment;
- copyright/licensing requirements of the selected venue and applicable institutional/testbed policies.

## Remaining gates before submission authorization

### P18 — Main-display redesign + claim/display QA

- architecture + evidence-role schematic;
- failure-domain taxonomy display/table;
- final main-versus-supplement display split;
- independent display QA against P13/P17/P17V.

### P19 — Reviewer-facing supplementary atlas + sanitized artifact

- derive concise reviewer supplement from dossier v2.2;
- include E0–E11, validity, anomalies, FIT ledger and endpoint semantics;
- package analysis code, derived non-sensitive data, manifests and figures;
- privacy/security sanitization before release.

### P20 — Final literature/credits/venue/submission preparation

Only after P18/P19 PASS:

- submission-date literature check and Gaspar full-text comparison if accessible;
- target-journal and author-instruction verification;
- final authorship/credits/funding/rights audit;
- clean submission-facing manuscript with internal control/status notes removed;
- proof and claim-reference-display-artifact consistency QA;
- explicit user authorization before external submission.

No new POWDER or FIT experiment is authorized or currently required.

## Immutable prohibitions

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- generic “WellPulse beats MQTT”;
- universal 52 dB threshold;
- deterministic RF-only recovery;
- exact broker latency from E10-D;
- population reliability from message counts or three FIT replicates;
- field/rural/Siwa/pump/hydraulic/groundwater/agronomic/industrial-process validation;
- unresolved RF-path/runtime USRP identity;
- pooled FIT+POWDER inferential statistics;
- historical uniqueness of the two-property model unless separately established by literature evidence.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence and registered research packs.**
2. **GitHub = canonical scientific/control record.**
3. **Home PC = independent third copy where applicable.**

Raw evidence remains immutable.

## Stop state

`WP2_P8_STATUS=COMPLETE_GOLDEN_EVIDENCE_PRESERVED`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`WP2_P9=PASS_GOLDEN_EVIDENCE_RECONCILED`

`WP2_P10=PASS_SCIENTIFIC_ANALYSIS_CONTRACT_FROZEN`

`WP2_P11=PASS_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS`

`WP2_P12=PASS_CROSS_EVIDENCE_INTEGRATION`

`WP2_P13=PASS_CLAIM_EVIDENCE_MATRIX_FROZEN`

`WP2_P14=PASS_PUBLICATION_TABLES_AND_FIGURES_FROZEN`

`WP2_P15=PASS_MANUSCRIPT_CONSTRUCTED_EVIDENCE_BOUNDED`

`WP2_P16=PASS_ADVERSARIAL_PUBLICATION_QA`

`P17_DOSSIER_RESEARCH_PACK=REGISTERED`

`WP2_P17_QA=PASS_CONSORTIUM_REVISION_EVIDENCE_BOUNDED`

`WP2_P17V=PASS_SUPERIOR_INDEPENDENT_VALIDATION`

`P17V_VERDICT=VALIDATED_WITH_PRE_SUBMISSION_CONDITIONS`

`LIVE_POWDER_DEPENDENCY=NONE`

`SUBMISSION_AUTHORIZED=NO`

`NEXT_PHASE=WP2_P18_MAIN_DISPLAY_REDESIGN_AND_QA`
