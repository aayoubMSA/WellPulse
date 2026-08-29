# WellPulse — Current Handover

Last updated: 2026-08-29 after completion of **WP2-P15 — MANUSCRIPT CONSTRUCTION**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from conversation memory. Detailed evidence, analysis, caveats and claim wording remain in the canonical files referenced below.

## Executive scientific state

- WP0: **PASS / EARLIER PAPER STORY PARTIALLY SUPERSEDED BY P10 EVIDENCE-BOUND CONTRACT**
- WP1: **PASS / FROZEN HISTORICAL CONFIRMATORY DESIGN**
- WP2: **ACTIVE — PUBLICATION QA**
- WP2-P8 manual RF campaign: **COMPLETE / GOLDEN / NON-SCORED MANUAL REFERENCE**
- WP2-P9 forensic reconciliation: **PASS / COMPLETE / INDEPENDENT RE-AUDIT PASS**
- WP2-P10 scientific analysis contract: **PASS / FROZEN**
- WP2-P11 full raw-data scientific analysis: **PASS / COMPLETE**
- WP2-P12 cross-evidence integration: **PASS / COMPLETE**
- WP2-P13 claim–evidence matrix: **PASS / FROZEN**
- WP2-P14 publication tables and figures: **PASS / FROZEN / VISUAL QA PASS**
- WP2-P15 manuscript construction: **PASS / COMPLETE / INTERNAL FULL DRAFT**
- WP2-P16 adversarial publication QA: **NOT STARTED**
- P7B scored physical qualification: **NOT PASSED**
- scored execution: **NOT AUTHORIZED**
- live POWDER dependency for current phase: **NONE**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8/P9/P10/P11/P12/P13/P14/P15 result may be promoted, reinterpreted or relabelled as scored P7B.

## Mandatory read order for P16+

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
3. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
4. `analysis/WP2_P12_CROSS_EVIDENCE_INTEGRATION_2026-08-29.md`
5. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
6. `analysis/WP2_P14_PUBLICATION_TABLES_FIGURES_2026-08-29.md`
7. `analysis/WP2_P14_FIGURE_CAPTIONS_AND_ALT_TEXT_2026-08-29.md`
8. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P15_2026-08-29.md`
9. `manuscript/WP2_P15_MANUSCRIPT_CONSTRUCTION_REPORT_2026-08-29.md`
10. P9 forensic authorities when exact POWDER trace/caveat semantics are needed.

## Canonical evidence roles

### FIT — architecture comparison

Authority: `FINAL_WP_RT01_FIT_A8`.

- FIT IoT-LAB Grenoble, A8-100;
- `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`;
- 10,000 records/cell;
- B0 = non-durable publish-only baseline;
- W1 = WellPulse durable queue + reconciliation;
- C0 healthy; C1 broker outage; C2 broker outage + gateway-process exec restart.

Principal results:

- C0: B0 100%, W1 100% in 3/3;
- C1: B0 80%, W1 100% in 3/3; `+20 pp` each replicate;
- C2: B0 80%, W1 100% in 3/3; `+20 pp` each replicate;
- every B0 C1/C2 run missed exactly 2,000/10,000 records;
- every W1 final run contained all 10,000 generated IDs exactly once;
- W1 backlog-drain mean: C1 `67.731246 s`; C2 `67.870252 s`.

These are repeated outcomes under the exact treatment, not population reliability probabilities.

### W1 implementation semantics rechecked in P15

Canonical source confirms:

- `record_id = run_id:boot_id:sequence`;
- canonical JSON record representation and SHA-256 checksum;
- SQLite durable queue with WAL and `synchronous=FULL`;
- explicit `PENDING` / `SENT` state;
- exact re-enqueue idempotence;
- conflicting record-ID reuse raises an integrity error.

These source-level semantics support the manuscript description of application-level durable identity/state. They do not create new experimental evidence.

### POWDER — physical RF/recovery characterization

Campaign: `WP2-P8`, profile `srslte-controlled-rf`, classification:

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

Role: physical-RF/LTE/MQTT transition, direction/repeatability, failure-domain separation, mechanism-specific recovery timing, broker/no-fault controls. It does **not** provide a scored B1-vs-W1 architecture comparison.

Principal transition evidence:

- E1R4 48–50 dB: ICMP clean, MQTT 20/20;
- E1R4 51 dB: ICMP 30% loss, MQTT 20/20;
- E1R4 52 dB: ICMP 60% loss, MQTT 13/20;
- E3 52 dB: ICMP loss `80/65/70%`, MQTT completeness `60/25/55%`.

Interpretation: experiment-specific transition region around 50–52 dB, not a universal threshold.

Recovery semantics:

- E10-A: censored no recovery inside preserved RF-only window;
- E10-B RF restore + UE restart: action-begin→first MQTT publish `6.063318 s`; first ping `6.609430 s`; publish→CORE receipt `0.060172 s`;
- E10-C-B: RF restore→first ping `29.247733 s`; first publish `29.248129 s`;
- E10-D: broker-start action-begin→manual successful publish `<=10.908749 s`, upper bound only;
- E8: broker interruption broke MQTT while LTE ping remained healthy;
- E9: no-fault control MQTT 60/60 with clean bidirectional ping.

## Frozen integration doctrine

FIT and POWDER are complementary, not substitutable:

- **FIT = record-state survival / architecture comparison**.
- **POWDER = communication-path degradation / recovery characterization**.

The project-level synthesis is **failure-domain-aware triangulation**. Durable record survival and communication-path recovery are distinct resilience properties. No pooled FIT+POWDER reliability statistic is allowed.

## Frozen claim envelope

Nine P13 claims remain manuscript-eligible with bounded wording.

Primary empirical claims:

- `IC-01` FIT W1 vs B0 durability/integrity effect under C1/C2;
- `IC-04` POWDER experiment-specific transition region;
- `IC-06` failure/recovery mechanism dependence and non-deterministic RF-only restoration.

Supporting empirical claims:

- `IC-02`, `IC-03`, `IC-05`, `IC-07`.

Methodological synthesis:

- `IC-08` two-property resilience validation;
- `IC-09` receiver-side evidence-first reconciliation/provenance.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## P14 frozen displays

- Figure 1 — FIT architecture-level final completeness.
- Figure 2 — FIT W1 backlog-drain cost.
- Figure 3 — POWDER ascending/descending cross-layer transition.
- Figure 4 — POWDER E3 near-transition repeatability.
- Table 1 — FIT architecture summary.
- Table 2 — POWDER transition summary.
- Table 3 — POWDER recovery timing semantics.

Rendering remains vector-first (SVG/PDF) with 600-dpi PNG fallback and final visual QA PASS.

`WP2_P14=PASS_PUBLICATION_TABLES_AND_FIGURES_FROZEN`

## P15 closure — manuscript construction

Canonical manuscript:

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P15_2026-08-29.md`

Construction/QA report:

`manuscript/WP2_P15_MANUSCRIPT_CONSTRUCTION_REPORT_2026-08-29.md`

Working title:

**WellPulse: Failure-Domain-Aware Validation of Durable IIoT Telemetry Across Embedded and Controlled-RF Testbeds**

The full internal draft contains:

- abstract and keywords;
- Introduction and four RQs;
- related-work/novelty boundary;
- architecture and two-property resilience model;
- FIT and POWDER Methods;
- RQ1–RQ4 Results with P14 display insertion points/captions;
- Discussion;
- threats to validity/limitations;
- reproducibility/evidence availability;
- conclusion;
- focused reference list.

### P15 literature refresh

The closest literature was refreshed through 2026-08-29. The refresh confirms that buffering, store-and-forward, MQTT retransmission/robustness testing, offline-first execution, edge/cloud reconciliation, 5G S&F, and testbed use are prior art and are not standalone WellPulse novelty claims.

The surviving contribution package remains:

1. application-level durable identity/state with receiver reconciliation;
2. explicit failure-domain decomposition;
3. real-embedded architecture evidence;
4. separate controlled physical-RF characterization;
5. claim-to-immutable-evidence reproducibility.

Gaspar et al. 2026 (`10.1109/MIOT.2026.3681190`) was bibliographically confirmed, but accessible sources during P15 did not expose enough methods/results for detailed comparison. The manuscript does not infer those missing details. A final pre-submission/full-text check remains mandatory if accessible in P16/submission QA.

### P15 status

`P15_MANUSCRIPT_FULL_DRAFT=YES`

`P15_PRIMARY_CLAIMS_WITHIN_P13=PASS`

`P15_LITERATURE_REFRESH=PASS_WITH_GASPAR_FULLTEXT_LIMITATION`

`P15_NEW_EXPERIMENT_REQUIRED=NO_AT_THIS_STAGE`

`WP2_P15=PASS_MANUSCRIPT_CONSTRUCTED_EVIDENCE_BOUNDED`

## Immutable caveats and prohibitions

Carry all P9/P11 caveats forward, including E5 missing forward recovery ping, E8 duplicate recovery sends, E10-A censoring, E10-C setup artifact A, E10-D upper-bound timing, E1R4/E3 sender-vs-receiver disagreements, E11 one-sided collector, E7 RTT outlier, unresolved runtime UHD identity/attenuator physical-path mapping, and FIT `SHA256SUMS.txt` self-reference anomaly with verified non-self entries and outer ZIP hashes.

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- universal 52 dB threshold;
- deterministic RF-only recovery;
- exact broker latency from E10-D;
- population reliability from message counts or three FIT replicates;
- rural/field/Siwa/pump/hydraulic/groundwater/agronomic validation;
- unresolved RF-path or runtime USRP identity;
- pooled FIT+POWDER inferential statistics.

## P16 mission

P16 must adversarially test the manuscript as a skeptical reviewer/editor would, including:

- baseline strength / strawman risk;
- cohesion of the two-testbed paper;
- novelty versus 2024–2026 literature;
- title/abstract risk of implying a POWDER W1 comparison;
- methods completeness and reproducibility;
- statistical language;
- manual/non-scored POWDER framing;
- claim/display consistency;
- artifact privacy/release risk;
- whether any critical deficiency requires analysis revision, manuscript revision, or a future experiment.

P16 may recommend a new experiment only if a manuscript-critical claim cannot survive without it. It must not execute one without separate explicit authorization.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence.**
2. **GitHub = canonical scientific/control record** for manifests, hashes, analysis code, derived tables, claims, figures, manuscript and handovers.
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

`PRIMARY_ARCHITECTURE_COMPARISON=FIT_B0_VS_W1`

`POWDER_ROLE=CONTROLLED_PHYSICAL_RF_AND_RECOVERY_CHARACTERIZATION`

`LIVE_POWDER_DEPENDENCY=NONE_FOR_CURRENT_PHASE`

`NEXT_PHASE=WP2_P16_ADVERSARIAL_PUBLICATION_QA`
