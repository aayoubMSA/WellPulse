# WellPulse — Current Handover

Last updated: 2026-08-29 after completion of **WP2-P11 — FULL RAW-DATA SCIENTIFIC ANALYSIS**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from conversation memory.

## Executive scientific state

- WP0: **PASS / EARLIER PAPER STORY PARTIALLY SUPERSEDED BY P10 EVIDENCE-BOUND CONTRACT**
- WP1: **PASS / FROZEN HISTORICAL CONFIRMATORY DESIGN**
- WP2: **ACTIVE — OFFLINE SCIENTIFIC INTEGRATION**
- WP2-P8 manual RF campaign: **COMPLETE / GOLDEN / NON-SCORED MANUAL REFERENCE**
- WP2-P9 forensic reconciliation: **PASS / COMPLETE / INDEPENDENT RE-AUDIT PASS**
- WP2-P10 scientific analysis contract: **PASS / FROZEN**
- WP2-P11 full raw-data scientific analysis: **PASS / COMPLETE**
- WP2-P12 cross-evidence integration: **NOT STARTED**
- P7B scored physical qualification: **NOT PASSED**
- scored execution: **NOT AUTHORIZED**
- live POWDER dependency for current phase: **NONE**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8/P9/P10/P11 result may be promoted, reinterpreted or relabelled as scored P7B.

## Canonical evidence classes

### FIT final architecture comparison

Source: `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`

- class: `FINAL_WP_RT01_FIT_A8`
- platform: FIT IoT-LAB Grenoble, A8-100
- matrix: `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`
- exactly 10,000 records/cell
- B0 = non-durable publish-only baseline
- W1 = WellPulse durable queue + reconciliation
- C0 = healthy
- C1 = deterministic broker outage
- C2 = broker outage + gateway-process exec restart

This remains the only current final evidence class supporting a direct architecture-level `B0 vs W1` comparison.

FIT Drive raw archives and SHA256:

| Rep | Drive ID | SHA256 |
|---|---|---|
| R1 | `14SMrvpmFgX7J2eHIkBuUkEcCwI19c5Nl` | `1c18a5e93597607765fbd05ebb7d81554d31735b8644eccf613e2d5162423d55` |
| R2 | `1Bi8zr7lO6UKn5BSoMrjQhoTcXIL5UtIX` | `cf25bdcd4684b6be2d6e5b328776a5704f85a520068c5fe6ace4121c909a0fe7` |
| R3 | `1Y1bBgs0iclyXeKsDr4tTI-ZcQEqr3EaO` | `ef92f4c3cce6e3824669b7771a35ae8c2374275ef4e1b4937c69c79ef47ac3c8` |

### POWDER golden physical-RF evidence

- campaign: `WP2-P8`
- reservation: `WP-07-C`
- profile: `srslte-controlled-rf`
- topology: `enb1 -> nuc1 / CORE`; `rue1 -> nuc2 / UE`
- classification: `P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

P8/P9 support controlled physical-RF/LTE/MQTT characterization, transition behavior, hysteresis, repeatability, recovery-mechanism comparison, controls and timing. They do **not** provide a scored `B1 vs W1` POWDER architecture comparison.

POWDER Drive authorities remain:

| Authority | SHA256 | Drive ID |
|---|---|---|
| Master P8 evidence | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` |
| E10/E11 collector | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` |
| Private golden preservation | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` |

## P9 forensic authority

P9 remains authoritative for POWDER run validity, anomalies, endpoint semantics and traceability.

Required trace chain:

`reported value → reconstructed table → raw-file root → frozen archive → SHA256 → Drive evidence`

`UNSUPPORTED_SURVIVING_VALUES=0`

`UNRESOLVED_ARCHIVE_HASH_DISCREPANCIES=0`

Important immutable caveats remain:

- E5 forward recovery ping observed live but not frozen;
- E8 duplicate recovery send; unique IDs govern completeness;
- E10-A censored no-recovery observation;
- E10-C attempt A setup artifact, B valid with caveat;
- E10-D upper-bound timing only;
- E1R4 seq 96 and E3 seq 150 receiver-missing despite no sender failure event;
- E11 R1-R3 collector is UE-side only;
- E7 481.046 ms RTT maximum preserved;
- runtime UHD identity not independently exposed;
- attenuator-ID→physical-path mapping unresolved;
- 89 screenshots preserved but unclassified;
- documented post-manifest collector/self-log append exceptions remain non-metric provenance anomalies.

## P10 frozen scientific contract

Canonical file:

`docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`

Frozen RQs:

1. **RQ1 — Embedded durability/integrity:** FIT W1 vs B0 under C0/C1/C2.
2. **RQ2 — Physical RF degradation/transition:** POWDER E1-E3.
3. **RQ3 — Failure-domain/recovery separation:** POWDER E4-E11.
4. **RQ4 — Cross-layer triangulation:** FIT + POWDER without pooled inference.

Frozen contribution package:

- C1 real-embedded durability evidence;
- C2 controlled physical-RF/LTE/MQTT characterization;
- C3 failure-domain separation;
- C4 evidence-first reproducibility.

## P11 closure — full raw-data scientific analysis

Canonical outputs:

1. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
2. `analysis/WP2_P11_FIT_RECONSTRUCTED_RUNS_2026-08-29.csv`
3. `analysis/WP2_P11_POWDER_DERIVED_METRICS_2026-08-29.csv`
4. `analysis/wp2_p11_analyze.py`

### RQ1 — FIT principal results

All 18 cells were independently reconstructed from `generated.jsonl` and receiver evidence.

- C0: B0 = 100% in 3/3; W1 = 100% in 3/3; difference `0 pp`.
- C1: B0 = 80% in 3/3; W1 = 100% in 3/3; difference `+20 pp` in every replicate.
- C2: B0 = 80% in 3/3; W1 = 100% in 3/3; difference `+20 pp` in every replicate.
- Every B0 C1/C2 run permanently missed exactly 2,000/10,000 generated records.
- Every W1 final run contained all 10,000 generated IDs exactly once.
- No unexpected receiver IDs were found.

Reconnect characterization:

- C1 B0 mean `1.325412 s`; W1 mean `1.317088 s`.
- C2 B0 mean `1.362121 s`; W1 mean `1.344870 s`.

W1 backlog drain:

- C1 mean `67.731246 s`;
- C2 mean `67.870252 s`.

The completeness effects have zero empirical run-level variance in this 3-replicate design, so P11 does not manufacture population CIs or reliability percentages from them.

### RQ2 — POWDER transition results

E1R4 ascending:

- 48 dB: ICMP 0% loss; MQTT 20/20.
- 49 dB: ICMP 0%; MQTT 20/20.
- 50 dB: ICMP 0%; MQTT 20/20.
- 51 dB: ICMP 30%; MQTT 20/20.
- 52 dB: ICMP 60%; MQTT 13/20 = 65%.

E2 descending:

- 52 dB: ICMP 65%; MQTT 11/20 = 55%.
- 51 dB: ICMP 10%; MQTT 20/20.
- 50 dB and below in sampled windows: ICMP clean; MQTT complete.

E3 repeatability:

- 49 dB ICMP loss: `0/0/0%`; MQTT `100/100/100%`.
- 50 dB ICMP loss: `5/0/5%`; MQTT `100/100/100%`.
- 51 dB ICMP loss: `10/5/50%`; MQTT `100/95/100%`.
- 52 dB ICMP loss: `80/65/70%`; MQTT `60/25/55%`.

Interpretation is an experiment-specific transition region around 50–52 dB, not a universal hard threshold. MQTT remained more tolerant than ICMP in the transition region but became incomplete under severe attenuation.

### RQ3 — recovery/failure-domain results

- RF-only recovery is not deterministic: E10-A has no observed recovery inside its preserved window.
- E10-B RF restore + UE restart: first MQTT publish `6.063318 s`; first ping `6.609430 s`; publish→CORE receipt `0.060172 s`.
- E10-C-B RF restore: first ping `29.247733 s`; first publish `29.248129 s`.
- E10-D broker result remains `<=10.908749 s` upper bound only.
- E8 demonstrates MQTT disruption while LTE pings remain healthy.
- E9 no-fault control: MQTT 60/60 and clean bidirectional ping.

### RQ4 — integration rule

FIT and POWDER provide complementary evidence layers:

- FIT = architecture durability/integrity comparison under controlled application/connectivity failure;
- POWDER = physical-RF degradation/recovery characterization and failure-domain separation.

They must not be pooled into one “WellPulse reliability” estimate.

### New P11 provenance anomaly

`P11-A01 / FIT_SHA256_MANIFEST_SELF_REFERENCE`: each FIT `SHA256SUMS.txt` contains a self-entry equal to the empty-file SHA256 because the manifest hashes itself during generation. All 103 non-self entries verify, all outer ZIP hashes match Drive, and the self-entry is not a metric source. This is documented, not cleaned away.

P11 gates:

`P11_UNSUPPORTED_SURVIVING_VALUES=0`

`P11_UNRESOLVED_EVIDENCE_DISCREPANCIES=0`

`WP2_P11=PASS_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS`

## Claim prohibitions carried forward

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- superiority to the strongest available durable MQTT client;
- universal RF thresholds;
- exact E10-D broker latency;
- deterministic RF-only recovery;
- population reliability from message counts or three FIT replicates;
- rural/field/Siwa/pump/hydraulic/agronomic validation;
- unresolved RF-path or runtime USRP identity.

B2 remains a comparator limitation/qualification issue, not current comparative evidence. No B2 or new live experiment is required for the current offline paper-analysis lane.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence.**
2. **GitHub = canonical scientific/control record** for manifests, hashes, contracts, analysis scripts, derived tables, anomaly registers, results and handovers.
3. **Home PC = independent third copy where applicable.**

Raw archives remain immutable.

## Stop state

`WP2_P8_STATUS=COMPLETE_GOLDEN_EVIDENCE_PRESERVED`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`WP2_P9=PASS_GOLDEN_EVIDENCE_RECONCILED`

`WP2_P10=PASS_SCIENTIFIC_ANALYSIS_CONTRACT_FROZEN`

`WP2_P11=PASS_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS`

`PRIMARY_ARCHITECTURE_COMPARISON=FIT_B0_VS_W1`

`POWDER_ROLE=CONTROLLED_PHYSICAL_RF_AND_RECOVERY_CHARACTERIZATION`

`LIVE_POWDER_DEPENDENCY=NONE_FOR_CURRENT_PHASE`

`NEXT_PHASE=WP2_P12_CROSS_EVIDENCE_INTEGRATION`
