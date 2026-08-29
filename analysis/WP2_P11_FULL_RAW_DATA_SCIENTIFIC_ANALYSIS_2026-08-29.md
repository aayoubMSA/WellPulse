# WP2-P11 — Full Raw-Data Scientific Analysis

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **PASS / COMPLETE**

## 1. Scope

This is the scientific-analysis stage defined by the frozen P10 contract. It analyzes the final FIT architecture-comparison evidence and the P9-accepted POWDER golden evidence. It does not draft manuscript prose, select a journal, generate final publication figures, authorize live experiments, execute B2, or alter scored P7B status.

FIT and POWDER remain separate evidence classes and are not statistically pooled.

## 2. Evidence re-verification

### FIT raw archives

Authenticated Drive copies were read and their outer SHA256 values recomputed:

| Replicate | Drive ID | SHA256 | Gate |
|---|---|---|---|
| R1 | `14SMrvpmFgX7J2eHIkBuUkEcCwI19c5Nl` | `1c18a5e93597607765fbd05ebb7d81554d31735b8644eccf613e2d5162423d55` | PASS |
| R2 | `1Bi8zr7lO6UKn5BSoMrjQhoTcXIL5UtIX` | `cf25bdcd4684b6be2d6e5b328776a5704f85a520068c5fe6ace4121c909a0fe7` | PASS |
| R3 | `1Y1bBgs0iclyXeKsDr4tTI-ZcQEqr3EaO` | `ef92f4c3cce6e3824669b7771a35ae8c2374275ef4e1b4937c69c79ef47ac3c8` | PASS |

For each archive, 103 non-self manifest entries matched `SHA256SUMS.txt`. The manifest also contains a self-entry with the SHA256 of an empty file; this is a deterministic self-reference artifact caused by hashing `SHA256SUMS.txt` while generating that same file. The outer ZIP hashes match the durable Drive anchors, all scientific source files used below verify, and the self-entry is not a metric source. It is preserved as `P11-A01 / FIT_SHA256_MANIFEST_SELF_REFERENCE` rather than treated as corruption.

### POWDER raw authorities

The three P9 authorities were re-hashed again during P11 and exactly match their canonical hashes:

- master P8: `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878`;
- E10/E11: `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6`;
- private golden preservation: `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8`.

P9 validity classes, anomalies and endpoint semantics remain binding.

## 3. RQ1 analysis — embedded durability and integrity on FIT

P11 independently reconstructed all 18 final cells directly from each cell's `generated.jsonl` and independent `*_received.jsonl`. Record IDs were reconciled as sets; duplicates and unexpected IDs were counted independently. Reconnect/backlog timing was read from the verified cell-local `edge_metrics.json`.

Canonical machine-readable output:

`analysis/WP2_P11_FIT_RECONSTRUCTED_RUNS_2026-08-29.csv`

### Run-level completeness

| Condition | B0 R1/R2/R3 | W1 R1/R2/R3 | W1-B0 difference |
|---|---|---|---|
| C0 healthy | 100%, 100%, 100% | 100%, 100%, 100% | `0 pp` in 3/3 |
| C1 broker outage | 80%, 80%, 80% | 100%, 100%, 100% | `+20 pp` in 3/3 |
| C2 outage + gateway-process exec restart | 80%, 80%, 80% | 100%, 100%, 100% | `+20 pp` in 3/3 |

For every B0 C1 and C2 run, exactly 2,000 of 10,000 generated record IDs were permanently absent at the receiver. For every W1 C0/C1/C2 run, all 10,000 generated IDs were present exactly once at final reconciliation. No unexpected receiver IDs were found in any of the 18 cells.

Because the run-level completeness differences are exactly identical across all three replicates within each condition, conventional small-sample confidence intervals around those empirical differences would falsely suggest more distributional information than the experiment contains. P11 therefore reports these as repeated deterministic outcomes under the exact frozen treatment, not as a population reliability percentage.

### Reconnect behavior

C1 reconnect times:

- B0 mean `1.325412 s`, SD `0.032117 s`, range `1.306527–1.362495 s`;
- W1 mean `1.317088 s`, SD `0.012321 s`, range `1.309382–1.331298 s`.

C2 reconnect times:

- B0 mean `1.362121 s`, SD `0.028096 s`, range `1.329756–1.380250 s`;
- W1 mean `1.344870 s`, SD `0.027923 s`, range `1.327973–1.377100 s`.

The observed reconnect differences are small relative to the 20-point completeness separation and are treated as engineering characterization, not a powered recovery-time superiority result.

### W1 backlog drain

- C1 mean `67.731246 s`, SD `0.275086 s`, range `67.549132–68.047688 s`;
- C2 mean `67.870252 s`, SD `0.851885 s`, range `67.320791–68.851579 s`.

This is the observed cost of eventual durable recovery in this FIT workload: W1 preserved all records but required a measurable post-outage backlog-drain interval.

### RQ1 scientific result

Within the exact FIT final experiment, the durable W1 path preserved the entire 10,000-record set under both controlled outage and outage-plus-gateway-process-restart, while the non-durable B0 path permanently missed the 2,000 records generated during the imposed outage interval. Healthy operation was complete for both architectures. This result is limited to B0 versus W1 under the frozen FIT impairment semantics and does not establish superiority over a standard durable MQTT client.

## 4. RQ2 analysis — POWDER physical RF degradation and transition behavior

P11 reconstructed per-level MQTT unique-sequence completeness directly from `UE/sent.log` and `CORE/received.log` for E1R4, E2 and E3, and parsed the matching raw ping summaries.

Canonical machine-readable output:

`analysis/WP2_P11_POWDER_DERIVED_METRICS_2026-08-29.csv`

### Ascending fine boundary — E1R4

| Attenuation | ICMP loss | Avg RTT | MQTT completeness |
|---:|---:|---:|---:|
| 48 dB | 0% | 32.274 ms | 20/20 = 100% |
| 49 dB | 0% | 36.963 ms | 20/20 = 100% |
| 50 dB | 0% | 34.452 ms | 20/20 = 100% |
| 51 dB | 30% | 51.171 ms | 20/20 = 100% |
| 52 dB | 60% | 66.578 ms | 13/20 = 65% |

The transition is cross-layer rather than simultaneous: ICMP degradation is already material at 51 dB while all 20 MQTT records still arrive. At 52 dB both ICMP and application delivery degrade substantially. E1R4 sequence 96 remains a receiver-missing record without a matching sender `MQTT_FAIL`; receiver evidence governs the 13/20 result.

### Descending recovery — E2

At 52 dB, ICMP loss was 65% and MQTT completeness 11/20 = 55%. At 51 dB, ICMP improved to 10% loss while MQTT recovered to 20/20; at 50 dB and below, the sampled ICMP windows were clean and MQTT remained complete.

The evidence supports a transition/recovery region around 50–52 dB for this tested POWDER setup. It does not justify a universal RF threshold or a single deterministic failure point.

### Near-threshold repeatability — E3

ICMP loss by cycle:

| Attenuation | Cycle 1 | Cycle 2 | Cycle 3 | Mean |
|---:|---:|---:|---:|---:|
| 49 dB | 0% | 0% | 0% | 0% |
| 50 dB | 5% | 0% | 5% | 3.33% |
| 51 dB | 10% | 5% | 50% | 21.67% |
| 52 dB | 80% | 65% | 70% | 71.67% |

MQTT completeness by cycle:

| Attenuation | Cycle 1 | Cycle 2 | Cycle 3 |
|---:|---:|---:|---:|
| 49 dB | 100% | 100% | 100% |
| 50 dB | 100% | 100% | 100% |
| 51 dB | 100% | 95% | 100% |
| 52 dB | 60% | 25% | 55% |

Thus, 52 dB consistently produced severe impairment but its magnitude varied materially across cycles. At 51 dB the path was unstable at the ICMP layer, while MQTT remained almost entirely complete. E3 sequence 150 remains a receiver-side loss not represented by a sender failure event and is retained in cycle-2 52 dB completeness.

### RQ2 scientific result

The raw evidence supports an experiment-specific degradation region rather than a sharp universal threshold: the path is consistently healthy in the sampled 48–49 dB region, begins to show variable degradation around 50–51 dB, and is severely impaired at 52 dB. MQTT is more tolerant than ICMP in the transition region, but also becomes incomplete under severe attenuation.

## 5. RQ3 analysis — failure-domain and recovery-mechanism separation

P11 retains the P9 endpoint semantics and does not create new timing definitions.

### RF-only / restart-assisted behavior

- E4 demonstrates a valid RF-only impairment/recovery reference with baseline, impairment and recovery evidence.
- E5 demonstrates UE-restart-assisted recovery but the forward UE recovery-ping artifact was not frozen; only the preserved reverse recovery/MQTT evidence is used.
- E6 demonstrates CORE-restart recovery with both-node evidence.
- E7 demonstrates combined RF + CORE restart + RF restore + UE restart recovery; the preserved 481.046 ms reverse-baseline RTT maximum remains in the record and is not removed.
- E10-A is a valid censored RF-only timing observation: no ping or MQTT recovery was observed in the preserved window, so no scalar recovery latency exists.
- E10-B: RF restore + UE restart action-begin to first MQTT publish = `6.063318 s`; action-begin to first ping = `6.609430 s`; publish to CORE receipt = `0.060172 s`.
- E10-C-B: RF restore to first ping = `29.247733 s`; RF restore to first publish = `29.248129 s`; attempt A remains a setup artifact.
- E10-D: broker-start action-begin to first manually initiated successful publish is `<=10.908749 s`; this is an upper bound, not exact broker recovery latency.

### Broker-only and no-fault controls

E8 isolates an application-layer failure while the LTE path remains healthy. During broker interruption, both UE and reverse CORE pings remained 20/20, while MQTT records 21–40 were absent. The duplicate recovery send 41–60 is preserved: the sender log has 80 lines but only 60 unique IDs; unique receiver reconciliation yields 40/60 unique total delivery.

E9 no-fault control yields 60/60 MQTT unique delivery and clean bidirectional ping.

### RQ3 scientific result

The evidence distinguishes failure domains that would be hidden by a single generic “outage” label. RF restoration alone is not deterministic across all observations, restart-assisted cases recover under their tested sequences, and broker-only failure can disrupt MQTT while the LTE path remains healthy. The timing values are mechanism- and endpoint-specific and must not be collapsed into one generic recovery-latency metric.

## 6. RQ4 analysis — cross-layer triangulation

The two evidence classes answer different questions:

- FIT directly tests record durability/integrity of W1 versus a non-durable B0 baseline under controlled application/connectivity failure on real embedded hardware.
- POWDER tests how a real LTE/MQTT path degrades and recovers under controlled physical RF and service/process interventions.

They are complementary but not interchangeable. FIT demonstrates that durable record semantics can prevent permanent loss under its frozen outage/restart treatment. POWDER demonstrates that the underlying communication path has a variable physical-RF transition region and that recovery behavior depends on the failure/recovery mechanism.

The defensible integration is therefore failure-domain-aware triangulation, not a pooled estimate of “WellPulse reliability.”

## 7. Sensitivity / anomaly impact

The principal P11 conclusions survive the preserved anomalies without data cleaning:

- E1R4 seq 96: receiver-side accounting already includes it as missing; no conclusion depends on sender failure flags.
- E3 seq 150: same control; receiver-side cycle completeness remains authoritative.
- E8 duplicate sends: using unique IDs prevents inflation; the diagnostic duplicate remains visible.
- E5 missing forward recovery ping: no forward metric is reconstructed.
- E10-A/E10-D: censoring and upper-bound semantics prevent false exact latency claims.
- E11 one-sided collector: no independent CORE/MQTT result is inferred.
- FIT `SHA256SUMS.txt` self-reference: does not affect any scientific source file or outer-archive identity; explicitly documented as P11-A01.

## 8. What P11 does not establish

P11 does not establish:

- a scored P7B PASS;
- POWDER B1-vs-W1 superiority;
- superiority over a durable MQTT persistence comparator;
- population-level reliability probabilities from three FIT replicates;
- universal attenuation thresholds;
- deterministic RF-only recovery;
- field, rural, Siwa, pump, hydraulic, groundwater or agronomic validation.

## 9. Reproducibility artifacts

- `analysis/wp2_p11_analyze.py`
- `analysis/WP2_P11_FIT_RECONSTRUCTED_RUNS_2026-08-29.csv`
- `analysis/WP2_P11_POWDER_DERIVED_METRICS_2026-08-29.csv`
- this report
- P9 forensic trace map and QA outputs for POWDER raw provenance
- FIT R1/R2/R3 Drive archives and their outer SHA256 anchors

## 10. P11 acceptance gate

- all FIT final cells reconstructed from raw generated/received identity sets: PASS;
- FIT archive outer hashes match durable Drive anchors: PASS;
- all POWDER analyses use P9-valid evidence/classes: PASS;
- selected POWDER per-level metrics independently reconstructed from raw logs: PASS;
- FIT and POWDER statistically separated: PASS;
- anomalies/censoring propagated: PASS;
- unsupported architecture comparison introduced: NO;
- manuscript prose/final figures/new experiment created: NO.

`P11_UNSUPPORTED_SURVIVING_VALUES=0`

`P11_UNRESOLVED_EVIDENCE_DISCREPANCIES=0`

`WP2_P11=PASS_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS`

`P11_NEXT=WP2_P12_CROSS_EVIDENCE_INTEGRATION`
