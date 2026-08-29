# WellPulse — Current Handover

Last updated: 2026-08-29 after completion of **WP2-P16 — ADVERSARIAL PUBLICATION QA**.

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
- WP2-P14 publication tables/figures: **PASS / FROZEN / VISUAL QA PASS**
- WP2-P15 manuscript construction: **PASS / COMPLETE / INTERNAL FULL DRAFT**
- WP2-P16 adversarial publication QA: **PASS / SCIENTIFIC QA COMPLETE**
- new experiment required for current bounded manuscript: **NO**
- submission authorization: **NOT YET**
- live POWDER dependency: **NONE**

Historical scored state remains unchanged and is internal control truth:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8+ result may be promoted or relabelled as scored P7B.

## Mandatory read order for any continuation

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
3. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
4. `analysis/WP2_P12_CROSS_EVIDENCE_INTEGRATION_2026-08-29.md`
5. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
6. `analysis/WP2_P14_PUBLICATION_TABLES_FIGURES_2026-08-29.md`
7. `analysis/WP2_P14_FIGURE_CAPTIONS_AND_ALT_TEXT_2026-08-29.md`
8. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P15_2026-08-29.md`
9. `manuscript/WP2_P16_ADVERSARIAL_PUBLICATION_QA_2026-08-29.md`
10. `manuscript/WP2_P16_MANDATORY_EDITORIAL_PATCHES_2026-08-29.md`
11. P9 forensic authorities when exact POWDER trace/caveat semantics are required.

## Frozen evidence roles

### FIT = architecture-level record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

- `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`;
- 10,000 records/cell;
- B0 = non-durable publish-only baseline;
- W1 = durable queue + receiver reconciliation.

Principal results:

- C0: B0 100%, W1 100% in 3/3;
- C1: B0 80%, W1 100% in 3/3, `+20 pp` each replicate;
- C2: B0 80%, W1 100% in 3/3, `+20 pp` each replicate;
- B0 C1/C2 permanently misses exactly 2,000/10,000 records;
- W1 final reconciliation retains all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`, C2 `67.870252 s`.

These are repeated outcomes under the exact treatment, not population reliability probabilities.

Canonical W1 implementation semantics:

- `record_id = run_id:boot_id:sequence`;
- canonical serialization + SHA-256;
- SQLite WAL with `synchronous=FULL`;
- explicit `PENDING` / `SENT` states;
- exact duplicate re-enqueue is idempotent;
- conflicting identity reuse raises an integrity error.

### POWDER = communication-path degradation/recovery characterization

Campaign: `WP2-P8`; profile `srslte-controlled-rf`.

Internal evidence classification remains:

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

Publication-facing role: **separately executed reference characterization; not architecture-effect estimation**.

Principal evidence:

- E1R4 48–50 dB: ICMP clean, MQTT 20/20;
- E1R4 51 dB: ICMP 30% loss, MQTT 20/20;
- E1R4 52 dB: ICMP 60% loss, MQTT 13/20;
- E3 52 dB: ICMP loss `80/65/70%`, MQTT completeness `60/25/55%`;
- E10-A: no recovery observed inside preserved RF-only window;
- E10-B RF restore + UE restart: action-begin→first MQTT publish `6.063318 s`, first ping `6.609430 s`, publish→CORE receipt `0.060172 s`;
- E10-C-B: RF restore→first ping `29.247733 s`, first publish `29.248129 s`;
- E10-D: `<=10.908749 s` upper bound only;
- E8: broker interruption disrupts MQTT while LTE ping remains healthy;
- E9: no-fault control MQTT 60/60.

Interpretation remains an experiment-specific transition region, not a universal 52 dB threshold.

## Frozen integration doctrine

FIT and POWDER are complementary, not substitutable:

- **FIT = record-state survival / architecture comparison**.
- **POWDER = communication-path degradation / recovery characterization**.

The synthesis is **failure-domain-aware triangulation**. No pooled FIT+POWDER reliability statistic is allowed.

## P13 claim envelope

Nine manuscript-eligible bounded claims remain frozen.

Primary empirical claims:

- `IC-01` FIT W1 vs B0 durability/integrity effect;
- `IC-04` POWDER transition-region characterization;
- `IC-06` failure/recovery mechanism dependence.

Supporting claims: `IC-02`, `IC-03`, `IC-05`, `IC-07`.

Methodological synthesis: `IC-08`, `IC-09`.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## P14 frozen displays

- Figure 1 — FIT architecture-level completeness.
- Figure 2 — FIT W1 backlog-drain cost.
- Figure 3 — POWDER ascending/descending cross-layer transition.
- Figure 4 — POWDER E3 near-transition repeatability.
- Table 1 — FIT architecture summary.
- Table 2 — POWDER transition summary.
- Table 3 — POWDER recovery timing semantics.

`P14_VISUAL_QA=PASS`

## P15 manuscript

Canonical internal full draft:

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P15_2026-08-29.md`

P15 contains Abstract, Introduction/RQs, related work, architecture, Methods, RQ1–RQ4 Results, Discussion, threats/limitations, reproducibility, conclusion, references, and P14 display insertion points.

## P16 adversarial publication QA

Canonical QA report:

`manuscript/WP2_P16_ADVERSARIAL_PUBLICATION_QA_2026-08-29.md`

Mandatory editorial patches:

`manuscript/WP2_P16_MANDATORY_EDITORIAL_PATCHES_2026-08-29.md`

### P16 scientific verdict

**The existing evidence is sufficient for a defensible paper without a new experiment, provided the manuscript remains within the frozen claim envelope.**

Strongest residual limitation: FIT B0 is intentionally non-durable and is not the strongest durable MQTT comparator. Therefore the paper reports a bounded durability effect relative to B0 and must never claim general MQTT superiority.

P16 reviewer attacks covered:

- store-and-forward novelty;
- strawman/comparator risk;
- two-testbed cohesion;
- manual POWDER characterization;
- statistical pseudoreplication;
- universal-threshold risk;
- recovery-clock ambiguity;
- sender-vs-receiver accounting;
- architecture specification;
- internal workflow jargon;
- literature completeness;
- artifact privacy/release.

### Mandatory publication-facing patches before submission

Twelve patches are frozen. Key ones:

1. use title: **WellPulse: Failure-Domain-Aware Validation of Durable IIoT Telemetry with Embedded Durability and Controlled-RF Characterization**;
2. remove reader-facing `P7B/scored/non-scored` jargon while retaining internal control truth;
3. insert exact W1 implementation semantics from `records.py` and `store.py`;
4. keep B0 explicitly identified as non-durable whenever the +20 pp FIT effect is summarized;
5. explicitly state the non-overlapping FIT/POWDER inferential roles early in Methods;
6. remove WP identifiers/internal workflow names from submitted prose;
7. remove the internal manuscript-control note from submitted copy;
8. keep Gaspar et al. at bibliographic/scope level until full-text comparison is completed;
9. promise only a sanitized public artifact, not release of private credential-bearing preservation bundles.

These patches change neither results nor frozen claims.

### Literature verification in P16

Bibliographic anchors were re-verified on 2026-08-29. Gaspar et al. DOI `10.1109/MIOT.2026.3681190` is independently confirmed, but detailed full-text comparison remains a submission-date gate if accessible.

### P16 closure

`P16_SCIENTIFIC_BLOCKERS=0`

`P16_NEW_EXPERIMENT_REQUIRED=NO`

`P16_MANDATORY_EDITORIAL_PATCHES=YES`

`P16_PUBLIC_ARTIFACT_SANITIZATION_REQUIRED=YES`

`WP2_P16=PASS_ADVERSARIAL_PUBLICATION_QA`

## Remaining gates before submission authorization

These are publication-preparation gates, not evidence-generation gates:

1. apply all frozen P16 editorial patches to a clean submission-facing manuscript;
2. produce sanitized public/reviewer artifact package;
3. perform final submission-date literature check, especially Gaspar et al. if full text is accessible;
4. select/re-verify target journal, scope, indexing/quartile/APC and author instructions at submission time;
5. format/type-set manuscript and integrate the frozen P14 figures/tables;
6. final proof/claim-reference-artifact consistency check;
7. explicit user authorization before external submission.

No new POWDER or FIT experiment is authorized or currently required.

## Immutable prohibitions

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- universal 52 dB threshold;
- deterministic RF-only recovery;
- exact broker latency from E10-D;
- population reliability from message counts or three FIT replicates;
- rural/field/Siwa/pump/hydraulic/groundwater/agronomic validation;
- unresolved RF-path/runtime-radio identity;
- pooled FIT+POWDER inferential statistics.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence.**
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

`LIVE_POWDER_DEPENDENCY=NONE`

`SUBMISSION_AUTHORIZED=NO`

`NEXT_PHASE=SUBMISSION_PREPARATION_NOT_STARTED`
