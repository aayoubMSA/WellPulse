# WP2-P10 — Scientific Analysis Contract

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **FROZEN / PASS**

## 1. Purpose

Freeze the scientific questions, evidence classes, comparison structure, analysis boundaries, and claim prohibitions for the post-POWDER WellPulse paper-analysis lane before P11 raw-data analysis begins.

This contract does not draft manuscript prose, choose a journal, create final figures, reopen live experimentation, reinterpret P8 as scored P7B, or authorize any new experiment.

## 2. Canonical evidence classes

### EVIDENCE-A — FIT final embedded experiment

Source: `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`

- Evidence class: `FINAL_WP_RT01_FIT_A8`
- Platform: FIT IoT-LAB, Grenoble, A8-100
- Matrix: `B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`
- 10,000 records per cell
- 18/18 final reconciliation PASS
- B0 = publish-only / non-durable baseline
- W1 = WellPulse durable offline-first queue + reconciliation
- C0 = no fault
- C1 = deterministic broker outage
- C2 = deterministic broker outage + gateway-process exec restart

This is the **only current final evidence class that directly supports an architecture-level B0-vs-W1 comparison**.

### EVIDENCE-B — POWDER P8 golden manual reference

Sources:

- `docs/WP2_P8_GOLDEN_EXPERIMENT_HANDOVER_2026-08-29.md`
- `evidence/powder/WP2_P8_GOLDEN_EVIDENCE_INDEX_2026-08-29.md`
- `evidence/powder/WP2_P9_RECONSTRUCTED_METRIC_TABLES_2026-08-29.md`
- `evidence/powder/WP2_P9_CROSS_NODE_RECONCILIATION_2026-08-29.md`
- `evidence/powder/WP2_P9_ANOMALY_REGISTER_2026-08-29.md`
- `evidence/powder/WP2_P9_FORENSIC_QA_REPORT_2026-08-29.md`

Classification:

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

This evidence supports controlled physical-RF/LTE/MQTT characterization, threshold behavior, hysteresis, repeatability, recovery-mechanism comparison, broker-only control, no-fault control, timing endpoints, and cross-node forensic reconciliation.

It **does not** provide a scored B1-vs-W1 POWDER architecture comparison.

### EVIDENCE-C — Historical scored P7B

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`B1=NULL_ABORTED_AFTER_Q3`

Historical P7B is retained as failed/aborted evidence and must not enter positive effect estimation.

## 3. Material correction to the earlier WP0 paper plan

The earlier WP0 novelty lock anticipated a confirmatory POWDER `B1_MQTT_QOS1` versus `W1_OFFLINE_FIRST` comparison, with a possible compact durable-client B2 sensitivity arm.

That confirmatory scored comparison was **not completed**. Therefore the paper must not retain RQs or contribution wording that imply such a comparison exists.

The paper is not blocked; its scientific contract is narrowed to the evidence actually obtained.

## 4. Frozen paper-level scientific thesis

The paper will study **failure-domain-aware resilience of a durable IIoT telemetry architecture using complementary real-hardware evidence**:

1. controlled application/connectivity failure on real embedded hardware is used to test the record-integrity benefit of WellPulse against a non-durable baseline;
2. controlled physical RF impairment on POWDER is used to characterize how the end-to-end LTE/MQTT communication path degrades and recovers, including threshold variability and recovery mechanisms;
3. the two evidence classes are integrated as complementary validation layers, never pooled as one statistical population.

The paper must distinguish **architecture-comparison evidence** from **physical-RF characterization evidence** at all times.

## 5. Frozen research questions

### RQ1 — Embedded durability and integrity

Under controlled broker outage and gateway-process restart on real embedded hardware, how does WellPulse (`W1`) differ from a non-durable publish-only baseline (`B0`) in final unique-record completeness, permanent loss, duplicates, and recovery/backlog behavior?

Evidence authority: FIT final 18-cell matrix only.

### RQ2 — Physical RF degradation and transition behavior

How does the end-to-end LTE/MQTT path behave as controlled physical attenuation approaches and crosses the observed impairment region, including packet loss, MQTT completeness, hysteresis, and near-threshold run-to-run variability?

Evidence authority: POWDER P8/P9 E1–E3 plus appropriate controls.

### RQ3 — Failure-domain and recovery-mechanism separation

How do RF-only restoration, UE restart, CORE restart, combined recovery, and broker-only interruption differ in observed recovery behavior and timing, and what limitations or censored outcomes remain?

Evidence authority: POWDER E4–E11, with P9 validity/anomaly constraints.

### RQ4 — Cross-layer triangulation

What complementary conclusions can be drawn when embedded durability evidence and controlled physical-RF evidence are considered together, while preserving platform, baseline, impairment-mechanism, workload, and evidence-class differences?

This is qualitative/structured triangulation, not pooled inference.

## 6. Frozen contribution package

### C1 — Real-embedded durability evidence

A reconciled real-hardware experiment quantifying durable record semantics against a non-durable baseline under normal operation, controlled outage, and gateway-process restart.

### C2 — Controlled physical-RF characterization

A two-node POWDER characterization of LTE/MQTT degradation, transition variability, hysteresis, and recovery under controlled RF attenuation with immutable raw evidence and receiver-side reconciliation.

### C3 — Failure-domain separation

Experimental separation of RF impairment, radio/UE recovery, CORE restart, broker-only failure, combined recovery, and no-fault control rather than collapsing all failures into a single outage category.

### C4 — Evidence-first reproducibility

Run-level provenance, immutable archives, SHA256 anchors, receiver-side sequence reconciliation, explicit anomaly preservation, and claim-to-raw-evidence traceability.

## 7. Comparison structure

### FIT

Primary structured comparison:

- `B0 vs W1` within each `C0/C1/C2` condition;
- replicate is the experimental unit;
- report all three run-level replicates before aggregate summaries;
- do not treat the 10,000 individual messages as independent replicates.

### POWDER

Primary structured comparisons:

- attenuation level / direction within E1–E3;
- baseline → impairment → recovery within E4–E7;
- RF/system recovery cases versus broker-only E8 and no-fault E9 controls;
- timing cases E10 with exact endpoint semantics;
- E11 only within its validated UE-side replication boundary.

POWDER P8 is not an architecture treatment comparison.

## 8. P11 required analyses

P11 must compute or independently verify, from raw/forensically accepted evidence:

### FIT

- run-level completeness and permanent-missing counts;
- B0-vs-W1 absolute completeness difference per condition;
- duplicate counts;
- reconnect and W1 backlog-drain summaries where valid;
- across-replicate descriptive variation;
- effect sizes with uncertainty only at the run level;
- explicit deterministic/structural outcomes where zero empirical variance makes conventional small-sample inferential summaries uninformative.

### POWDER

- ICMP loss/RTT versus attenuation;
- MQTT completeness versus attenuation;
- threshold-region and direction/hysteresis summaries;
- near-threshold cycle variability;
- baseline/impairment/recovery phase differences;
- mechanism-specific recovery timing using the P9 endpoint semantics;
- censored/non-recovery treatment for E10-A;
- upper-bound treatment for E10-D;
- control comparisons against E8/E9;
- explicit anomaly-sensitive sensitivity checks where a preserved anomaly could affect interpretation.

## 9. Statistical rules

1. The **run/replicate**, not the message, is the experimental unit for inferential statements.
2. Message-level observations may characterize within-run loss, sequence behavior, and latency distributions but must not inflate sample size.
3. Report raw run-level values alongside aggregates.
4. Prefer absolute effects and engineering magnitude over p-value-driven conclusions.
5. Do not manufacture confidence intervals where the experimental design or zero-variance deterministic result makes them misleading.
6. FIT and POWDER are not pooled statistically.
7. Exploratory threshold/recovery analyses must be labeled as characterization where no predeclared confirmatory inferential design exists.
8. Negative, NULL, censored, duplicate, and anomalous observations remain part of the scientific record.

## 10. Mandatory claim boundaries

The paper may support, subject to P11–P16 analysis/QA:

- durability/integrity advantages of W1 over B0 under the exact FIT controlled failure semantics;
- controlled physical-RF/LTE/MQTT degradation and recovery observations on the tested POWDER profile;
- observed threshold region, hysteresis, variability, and recovery-mechanism differences as experiment-specific findings;
- complementary cross-layer validation/triangulation across FIT and POWDER.

The paper must **not** claim:

- scored P7B success;
- a POWDER B1-vs-W1 architecture advantage;
- superiority to a strongest-available durable MQTT client;
- exact broker recovery latency from E10-D;
- deterministic RF-only recovery when E10-A shows non-recovery within its observation window;
- universal RF thresholds beyond the tested POWDER setup;
- field/rural/Siwa reliability;
- pump, hydraulic, groundwater, agronomic, or crop validation;
- runtime USRP serial/firmware identity;
- unresolved attenuator-ID-to-physical-path mapping;
- statistical independence based on message count.

## 11. B2 durable-client status

`B2_SEMANTICS_GATE_v1.md` is a frozen local qualification protocol, not completed scored comparative evidence in the current canonical record.

Therefore B2 cannot be presented as an experimentally defeated comparator.

At manuscript stage it must be handled as a **limitation/comparator boundary** unless separate valid evidence is later authorized and obtained. No B2 experiment is required to begin P11 under this contract.

## 12. Literature/novelty control

The prior WP0 literature/comparator audit remains useful but its original paper story is superseded where it assumes a completed scored B1/W1 POWDER matrix.

Before final claim lock in P13/P15:

- update the literature search through the submission date;
- fully evaluate the previously flagged Gaspar et al. 2026 MQTT reliability paper if accessible;
- benchmark the final contribution against durable MQTT persistence, offline-first/store-and-forward systems, MQTT robustness studies, and reproducible wireless-testbed work;
- narrow or remove any contribution already established by prior art.

This literature update may change novelty wording, but it may not change measured results.

## 13. P11 acceptance gate

P11 may start only with this P10 contract frozen.

P11 passes only if:

- all reported numerical analyses trace to approved evidence classes;
- no P8/P9 value is promoted to scored P7B;
- FIT and POWDER remain statistically separate;
- all anomalies/censoring rules are propagated;
- no unsupported architecture comparison is introduced;
- analysis outputs are reproducible from canonical evidence and code.

## 14. Scope exclusions

P10/P11 do not authorize:

- manuscript prose;
- journal selection;
- final figures;
- new live experiments;
- POWDER access;
- B2 execution;
- scored P7B retry;
- field validation;
- claim expansion beyond the frozen evidence envelope.

## 15. Closure

`P10_SCIENTIFIC_QUESTION_CONTRACT=FROZEN`

`PRIMARY_ARCHITECTURE_COMPARISON=FIT_B0_VS_W1`

`POWDER_ROLE=CONTROLLED_PHYSICAL_RF_AND_RECOVERY_CHARACTERIZATION`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`P10_NEXT=WP2_P11_FULL_RAW_DATA_ANALYSIS`

`WP2_P10=PASS_SCIENTIFIC_ANALYSIS_CONTRACT_FROZEN`
