# WellPulse — Current Handover

Last updated: 2026-08-29 after completion of **WP2-P13 — CLAIM–EVIDENCE MATRIX**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from conversation memory. Detailed evidence, analysis and caveats remain in the canonical files referenced below.

## Executive scientific state

- WP0: **PASS / EARLIER PAPER STORY PARTIALLY SUPERSEDED BY P10 EVIDENCE-BOUND CONTRACT**
- WP1: **PASS / FROZEN HISTORICAL CONFIRMATORY DESIGN**
- WP2: **ACTIVE — OFFLINE SCIENTIFIC INTEGRATION / PUBLICATION PREPARATION**
- WP2-P8 manual RF campaign: **COMPLETE / GOLDEN / NON-SCORED MANUAL REFERENCE**
- WP2-P9 forensic reconciliation: **PASS / COMPLETE / INDEPENDENT RE-AUDIT PASS**
- WP2-P10 scientific analysis contract: **PASS / FROZEN**
- WP2-P11 full raw-data scientific analysis: **PASS / COMPLETE**
- WP2-P12 cross-evidence integration: **PASS / COMPLETE**
- WP2-P13 claim–evidence matrix: **PASS / FROZEN**
- WP2-P14 publication tables and figures: **NOT STARTED**
- P7B scored physical qualification: **NOT PASSED**
- scored execution: **NOT AUTHORIZED**
- live POWDER dependency for current phase: **NONE**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8/P9/P10/P11/P12/P13 result may be promoted, reinterpreted or relabelled as scored P7B.

## Canonical evidence classes

### FIT — final architecture comparison

Authority: `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`

- evidence class `FINAL_WP_RT01_FIT_A8`;
- FIT IoT-LAB Grenoble, A8-100;
- `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`;
- exactly 10,000 records per cell;
- B0 = non-durable publish-only baseline;
- W1 = WellPulse durable queue + reconciliation;
- C0 healthy; C1 broker outage; C2 broker outage + gateway-process exec restart.

This is the only current final evidence class supporting a direct architecture-level `B0 vs W1` comparison.

FIT raw authorities:

| Rep | Drive ID | SHA256 |
|---|---|---|
| R1 | `14SMrvpmFgX7J2eHIkBuUkEcCwI19c5Nl` | `1c18a5e93597607765fbd05ebb7d81554d31735b8644eccf613e2d5162423d55` |
| R2 | `1Bi8zr7lO6UKn5BSoMrjQhoTcXIL5UtIX` | `cf25bdcd4684b6be2d6e5b328776a5704f85a520068c5fe6ace4121c909a0fe7` |
| R3 | `1Y1bBgs0iclyXeKsDr4tTI-ZcQEqr3EaO` | `ef92f4c3cce6e3824669b7771a35ae8c2374275ef4e1b4937c69c79ef47ac3c8` |

### POWDER — golden physical-RF/recovery evidence

- campaign `WP2-P8`;
- profile `srslte-controlled-rf`;
- `enb1 -> nuc1 / CORE`; `rue1 -> nuc2 / UE`;
- classification `P8_CLASS=MANUAL_NON_SCORED_REFERENCE`.

P8/P9 support controlled physical-RF/LTE/MQTT degradation, transition behavior, hysteresis, repeatability, recovery-mechanism comparison, controls and timing. They do **not** provide a scored B1-vs-W1 POWDER architecture comparison.

POWDER Drive authorities:

| Authority | SHA256 | Drive ID |
|---|---|---|
| Master P8 evidence | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` |
| E10/E11 collector | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` |
| Private golden preservation | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` |

## Mandatory read order for P14+

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
3. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
4. `analysis/WP2_P12_CROSS_EVIDENCE_INTEGRATION_2026-08-29.md`
5. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
6. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.csv`
7. P9 forensic authorities as needed, especially `evidence/powder/WP2_P9_FORENSIC_TRACE_MAP_2026-08-29.md` and `evidence/powder/WP2_P9_ANOMALY_REGISTER_2026-08-29.md`.

## P11 scientific results carried forward

### FIT

- C0: B0 = 100% and W1 = 100% in 3/3; difference `0 pp`.
- C1: B0 = 80%, W1 = 100% in 3/3; difference `+20 pp` in every replicate.
- C2: B0 = 80%, W1 = 100% in 3/3; difference `+20 pp` in every replicate.
- Every B0 C1/C2 run permanently missed exactly 2,000/10,000 generated records.
- Every W1 final run contained all 10,000 generated IDs exactly once.
- W1 backlog-drain mean: C1 `67.731246 s`; C2 `67.870252 s`.

These are repeated deterministic outcomes under the exact three-replicate FIT treatment, not population reliability probabilities.

### POWDER transition

E1R4 ascending:

- 48 dB: ICMP 0% loss; MQTT 20/20.
- 49 dB: ICMP 0%; MQTT 20/20.
- 50 dB: ICMP 0%; MQTT 20/20.
- 51 dB: ICMP 30%; MQTT 20/20.
- 52 dB: ICMP 60%; MQTT 13/20 = 65%.

E3 at 52 dB:

- ICMP loss `80/65/70%` across cycles;
- MQTT completeness `60/25/55%`.

Interpretation: experiment-specific transition region around 50–52 dB, not a universal threshold.

### POWDER recovery/failure domains

- E10-A: no recovery observed inside preserved RF-only observation window; censored result.
- E10-B RF restore + UE restart: action-begin→first MQTT publish `6.063318 s`; action-begin→first ping `6.609430 s`; publish→CORE receipt `0.060172 s`.
- E10-C-B: RF restore→first ping `29.247733 s`; RF restore→first publish `29.248129 s`.
- E10-D: broker-start action-begin→manual successful publish `<=10.908749 s`; upper bound only.
- E8: MQTT interruption while LTE ping remained healthy.
- E9: no-fault control MQTT 60/60 with clean bidirectional ping.

## P12 integration doctrine

FIT and POWDER are complementary, not substitutable:

- **FIT = record-state survival / architecture comparison**.
- **POWDER = communication-path degradation / recovery characterization**.

The project-level synthesis is **failure-domain-aware triangulation**. A resilient telemetry system must be evaluated for both **durable record survival** and **communication-path recovery**. No pooled FIT+POWDER reliability statistic is allowed.

## P13 closure — claim–evidence matrix

Canonical outputs:

1. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
2. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.csv`

Nine candidate claims were reviewed and all nine passed with bounded wording:

### Strength A — direct replicated empirical evidence

- `IC-01`: FIT C1/C2 W1 10,000/10,000 vs B0 8,000/10,000 in every replicate, bounded to the exact treatment.
- `IC-02`: FIT C0 healthy final delivery complete for both B0 and W1 in 3/3.
- `IC-03`: W1 complete FIT recovery carries a measurable backlog-drain interval (~67.7–67.9 s).

### Strength B — direct experiment-specific characterization

- `IC-04`: POWDER physical degradation is a transition region; 52 dB is severe but variable in the tested profile.
- `IC-05`: ICMP degradation can precede MQTT incompleteness in the transition region.
- `IC-06`: recovery depends on failure/recovery mechanism; RF-only restoration was not deterministic across all preserved observations.
- `IC-07`: broker-only interruption can disrupt MQTT while LTE ping remains healthy.

### Strength C — methodological synthesis

- `IC-08`: durable record survival and communication-path recovery are distinct resilience properties requiring separate validation layers.
- `IC-09`: receiver-side evidence-first reconciliation and immutable provenance support defensible resilience reporting in this project.

P13 hierarchy:

- primary empirical claims: `IC-01`, `IC-04`, `IC-06`;
- supporting empirical claims: `IC-02`, `IC-03`, `IC-05`, `IC-07`;
- methodological synthesis: `IC-08`, `IC-09`.

P13 gates:

`P13_CLAIMS_REVIEWED=9`

`P13_CLAIMS_PASSED=9`

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

`WP2_P13=PASS_CLAIM_EVIDENCE_MATRIX_FROZEN`

## Immutable caveats and prohibitions

Carry forward all P9/P11 anomalies. In particular:

- E5 forward recovery ping was not frozen;
- E8 duplicate recovery sends remain preserved and unique IDs govern completeness;
- E10-A is censored no-recovery evidence;
- E10-C attempt A is setup artifact; B is valid with caveat;
- E10-D is upper-bound timing only;
- E1R4 seq 96 and E3 seq 150 are receiver-missing despite no sender failure event;
- E11 R1–R3 is UE-side only;
- E7 481.046 ms RTT maximum remains preserved;
- unresolved runtime UHD identity and attenuator-ID→physical-path mapping must not be inferred;
- FIT `SHA256SUMS.txt` self-reference anomaly (`P11-A01`) is documented; all 103 non-self entries and outer ZIP hashes verify.

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- universal RF threshold;
- deterministic RF-only recovery;
- exact E10-D broker latency;
- population reliability from message counts or three FIT replicates;
- rural/field/Siwa/pump/hydraulic/groundwater/agronomic validation;
- unresolved RF-path or runtime USRP identity;
- pooled FIT+POWDER inferential statistics.

## P14 authorization envelope

P14 may create publication tables/figures only from P13-passed claims and approved quantitative sources:

- FIT run-level completeness, missing counts, reconnect values and W1 backlog-drain values;
- POWDER ICMP loss/RTT and MQTT completeness by attenuation/cycle/direction;
- mechanism-specific POWDER recovery timing with censor/upper-bound notation;
- evidence-layer / failure-domain schematic for the P13 methodological synthesis.

P14 must not create a combined FIT+POWDER reliability score or any visual implying a POWDER B1-vs-W1 comparison.

P14 does not authorize new experiments, manuscript prose, journal submission, or scored P7B retry.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence.**
2. **GitHub = canonical scientific/control record** for manifests, hashes, contracts, analysis scripts, derived tables, anomaly registers, claim matrices, results and handovers.
3. **Home PC = independent third copy where applicable.**

Raw archives remain immutable.

## Stop state

`WP2_P8_STATUS=COMPLETE_GOLDEN_EVIDENCE_PRESERVED`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`WP2_P9=PASS_GOLDEN_EVIDENCE_RECONCILED`

`WP2_P10=PASS_SCIENTIFIC_ANALYSIS_CONTRACT_FROZEN`

`WP2_P11=PASS_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS`

`WP2_P12=PASS_CROSS_EVIDENCE_INTEGRATION`

`WP2_P13=PASS_CLAIM_EVIDENCE_MATRIX_FROZEN`

`PRIMARY_ARCHITECTURE_COMPARISON=FIT_B0_VS_W1`

`POWDER_ROLE=CONTROLLED_PHYSICAL_RF_AND_RECOVERY_CHARACTERIZATION`

`LIVE_POWDER_DEPENDENCY=NONE_FOR_CURRENT_PHASE`

`NEXT_PHASE=WP2_P14_PUBLICATION_TABLES_AND_FIGURES`
