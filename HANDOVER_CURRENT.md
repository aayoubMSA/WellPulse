# WellPulse — Current Handover

Last updated: 2026-08-29 after completion of **WP2-P10 — SCIENTIFIC ANALYSIS CONTRACT**.

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
- WP2-P11 full raw-data scientific analysis: **NOT STARTED**
- P7B scored physical qualification: **NOT PASSED**
- scored execution: **NOT AUTHORIZED**
- live POWDER dependency for current phase: **NONE**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8/P9/P10 result may be promoted, reinterpreted or relabelled as scored P7B.

## Canonical evidence authorities

### FIT final architecture-comparison evidence

Source: `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`

- Evidence class: `FINAL_WP_RT01_FIT_A8`
- Grenoble A8-100
- `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`
- exactly 10,000 records/cell
- 18/18 final reconciliation PASS
- B0 = non-durable publish-only baseline
- W1 = WellPulse durable queue + reconciliation
- C0 = healthy
- C1 = deterministic broker outage
- C2 = broker outage + gateway-process exec restart

This is the current final evidence class supporting a direct architecture-level `B0 vs W1` comparison.

### POWDER golden physical-RF evidence

- Campaign: `WP2-P8`
- reservation: `WP-07-C`
- profile: `srslte-controlled-rf`
- `enb1 -> nuc1 / CORE`
- `rue1 -> nuc2 / UE`
- classification: `P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

P8 supports controlled physical-RF/LTE/MQTT characterization, threshold behavior, hysteresis, near-threshold variability, recovery-mechanism comparison, controls and timing. It does **not** provide a scored `B1 vs W1` POWDER architecture comparison.

## WP2-P9 forensic closure

P9 remains authoritative for all POWDER numeric reconstruction.

Three authenticated Drive authorities were downloaded read-only and outer SHA256 values matched the canonical anchors:

| Authority | SHA256 | Drive ID |
|---|---|---|
| Master P8 evidence | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` |
| E10/E11 collector | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` |
| Private golden preservation | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` |

Census: **598 immutable members** across the three authorities.

Principal receiver-side MQTT reconstructions include E1R2 `65/65`, E1R3 `100/100`, E1R4 `93/100`, E2 `151/160`, E3 `222/255`, E4/E5/E6/E7/E8 `40/60` unique, E9 `60/60`. E8 retains 80 sender lines but 60 unique IDs.

Required trace chain is closed:

`reported value → reconstructed table → raw-file root → frozen archive → SHA256 → Drive evidence`

`UNSUPPORTED_SURVIVING_VALUES=0`

`UNRESOLVED_ARCHIVE_HASH_DISCREPANCIES=0`

Canonical P9 outputs:

1. `evidence/powder/WP2_P9_CANONICAL_EVIDENCE_CENSUS_2026-08-29.md`
2. `evidence/powder/WP2_P9_CENSUS_E10_E11_SHA256_2026-08-29.csv`
3. `evidence/powder/WP2_P9_RUN_VALIDITY_REGISTER_2026-08-29.md`
4. `evidence/powder/WP2_P9_RECONSTRUCTED_METRIC_TABLES_2026-08-29.md`
5. `evidence/powder/WP2_P9_CROSS_NODE_RECONCILIATION_2026-08-29.md`
6. `evidence/powder/WP2_P9_ANOMALY_REGISTER_2026-08-29.md`
7. `evidence/powder/WP2_P9_FORENSIC_TRACE_MAP_2026-08-29.md`
8. `evidence/powder/WP2_P9_FORENSIC_QA_REPORT_2026-08-29.md`
9. `analysis/powder/wp2_p9_reconstruct.py`

## Immutable P9 caveats carried forward

- E5 forward recovery-ping observed live but not frozen.
- E8 duplicate recovery-send attempt; unique IDs govern completeness.
- E10-A no recovery within preserved observation window; no exact latency.
- E10-C attempt A = setup artifact; B = valid with timing caveat.
- E10-D timing = upper bound, not exact broker recovery latency.
- departure `CAPTURE_STATUS.txt` post-manifest append on both nodes = documented exception, not corruption.
- master `meta/collection.log` and E10/E11 `meta/collector.log` each contain one deterministic collector self-log append after their own manifest hash; outer ZIP hashes match and neither log is a metric source (`A-018`).
- runtime UHD device not independently exposed; no runtime USRP serial/firmware claim.
- attenuator-ID→physical-path mapping unresolved; never infer it.
- E1R4 seq 96 and E3 seq 150 remain sender/event-vs-receiver disagreements; receiver governs completeness.
- E10-C-B later CORE verification line duplicated; do not double-count.
- E11 R1-R3 collector is UE-side only; no independent CORE metric may be inferred.
- E7 reverse baseline 481.046 ms RTT maximum preserved as observed.
- 89 screenshots preserved and hashed but unclassified by run; do not invent attribution.
- final profile/RSpec capture remains PRIVATE because it contains credential-bearing/encrypted portal material.

## WP2-P10 closure — scientific analysis contract

Canonical contract:

`docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`

P10 resolves a material mismatch between the earlier planned paper and the evidence actually obtained.

The earlier WP0 story anticipated a scored POWDER `B1_MQTT_QOS1 vs W1_OFFLINE_FIRST` comparison and possible B2 durable-client sensitivity. That scored comparison was not completed and must not be implied.

The frozen post-P10 paper thesis is instead **failure-domain-aware resilience using complementary real-hardware evidence**:

1. FIT supplies the direct architecture comparison (`B0 vs W1`) under healthy, broker-outage and broker-outage+gateway-restart conditions.
2. POWDER P8/P9 supplies controlled physical-RF/LTE/MQTT degradation, threshold, hysteresis, variability, recovery and control evidence.
3. FIT and POWDER are complementary validation layers and must never be pooled statistically as one population.

### Frozen research questions

- **RQ1 — Embedded durability/integrity:** W1 vs B0 under FIT C0/C1/C2.
- **RQ2 — Physical RF degradation/transition:** ICMP/MQTT behavior, threshold region, hysteresis and variability from POWDER E1-E3.
- **RQ3 — Failure-domain/recovery separation:** RF-only, UE restart, CORE restart, combined recovery, broker-only control and timing from E4-E11.
- **RQ4 — Cross-layer triangulation:** structured complementary interpretation across FIT and POWDER without pooled inference.

### Frozen contribution package

- C1: real-embedded durability evidence against a non-durable baseline.
- C2: controlled two-node physical-RF/LTE/MQTT characterization.
- C3: failure-domain separation across RF, radio/UE, CORE, broker and combined recovery cases.
- C4: evidence-first reproducibility with immutable hashes, receiver reconciliation and claim-to-raw-evidence traceability.

### P10 claim prohibitions

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- superiority to the strongest available durable MQTT client;
- universal RF thresholds;
- exact E10-D broker latency;
- deterministic RF-only recovery;
- rural/field/Siwa/pump/hydraulic/agronomic validation;
- unresolved RF-path or runtime USRP identity;
- statistical independence from message count.

B2 remains a comparator limitation/qualification issue, not current comparative evidence. B2 execution is not required for P11 and is not authorized by P10.

## P11 entry gate

P11 may now begin. It must:

- analyze FIT at the run/replicate level;
- analyze POWDER using only P9-accepted evidence and endpoint semantics;
- preserve all anomalies/censoring;
- keep FIT and POWDER statistically separate;
- reproduce analyses from canonical evidence/code;
- introduce no unsupported architecture comparison.

P11 does not authorize manuscript prose, final publication figures, journal selection, new experiments, POWDER access, B2 execution or scored P7B retry.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence.**
2. **GitHub = canonical scientific/control record** for manifests, hashes, contracts, analysis scripts, derived tables, anomaly registers, results and handovers.
3. **Home PC = independent third copy where applicable.**

Raw archives remain immutable. Do not commit credential-bearing or large raw bundles into ordinary Git history.

## Stop state

`WP2_P8_STATUS=COMPLETE_GOLDEN_EVIDENCE_PRESERVED`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`WP2_P9=PASS_GOLDEN_EVIDENCE_RECONCILED`

`WP2_P10=PASS_SCIENTIFIC_ANALYSIS_CONTRACT_FROZEN`

`PRIMARY_ARCHITECTURE_COMPARISON=FIT_B0_VS_W1`

`POWDER_ROLE=CONTROLLED_PHYSICAL_RF_AND_RECOVERY_CHARACTERIZATION`

`LIVE_POWDER_DEPENDENCY=NONE_FOR_CURRENT_PHASE`

`NEXT_PHASE=WP2_P11_FULL_RAW_DATA_ANALYSIS`
