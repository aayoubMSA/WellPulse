# WP2-P13 — Claim–Evidence Matrix

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **PASS / COMPLETE**

## 1. Purpose

Freeze the manuscript-eligible claim envelope before final figures and manuscript construction. Every surviving claim must identify its evidence class, exact supporting observations, trace path, strength, caveats, permitted wording and prohibited overstatement.

P13 does not draft manuscript prose, select a journal, create final publication figures, authorize experiments, execute B2, or alter any raw evidence.

## 2. Claim-strength scale

- **A — Direct replicated empirical evidence:** claim follows directly from repeated run-level observations under a frozen treatment with receiver-side reconciliation.
- **B — Direct empirical characterization:** claim follows directly from accepted experiment-specific measurements but is not a powered architecture treatment effect.
- **C — Structured methodological synthesis:** claim integrates independently supported evidence classes without pooling them statistically.
- **REJECT:** traceability, validity, or claim boundary is insufficient for manuscript use.

Strength labels describe the support available for the exact bounded wording; they are not generic quality scores.

## 3. Canonical claim–evidence matrix

| ID | Frozen bounded claim | Evidence authority | Direct support | Strength | Required caveat | Manuscript status |
|---|---|---|---|---|---|---|
| IC-01 | Under the exact FIT final C1/C2 treatments, W1 preserved all 10,000 generated records in every replicate, whereas B0 permanently missed the 2,000 outage-period records. | FIT `FINAL_WP_RT01_FIT_A8`; P11 FIT reconstructed CSV | C1: B0 80%, W1 100% in R1–R3. C2: B0 80%, W1 100% in R1–R3. Zero unexpected IDs; W1 zero final duplicates. | **A** | B0 is non-durable publish-only; three replicates do not establish a population reliability probability; no strongest-durable-MQTT superiority. | **PASS** |
| IC-02 | Under healthy FIT C0, both B0 and W1 achieved complete final delivery in all three replicates. | FIT final raw archives; P11 reconstructed CSV | B0 = 100% and W1 = 100% in C0 R1–R3. | **A** | Exact workload/platform only; no universal healthy-path reliability claim. | **PASS** |
| IC-03 | W1's complete FIT recovery required a measurable post-outage backlog-drain interval under the tested workload. | FIT verified `edge_metrics.json`; P11 analysis | C1 backlog drain mean 67.731246 s; C2 mean 67.870252 s, with all three run-level values preserved. | **A** | Backlog drain is not reconnect time and must not be numerically equated with POWDER recovery clocks. | **PASS** |
| IC-04 | In the tested POWDER profile, physical degradation occurred over a transition region rather than at one deterministic threshold, with severe but variable impairment at 52 dB. | POWDER E1R4/E2/E3; P9 trace map; P11 derived metrics | E1R4 52 dB: ICMP 60% loss, MQTT 65%; E2 52 dB: ICMP 65%, MQTT 55%; E3 52 dB MQTT 60/25/55%, ICMP 80/65/70%. | **B** | Experiment-specific attenuation/profile only; no universal 52 dB failure threshold; unresolved attenuator-ID→physical-path mapping is not inferred. | **PASS** |
| IC-05 | In the POWDER transition region, lower-layer ICMP degradation could become visible before MQTT completeness declined. | POWDER E1R4/E3; P11 derived metrics | E1R4 at 51 dB: ICMP loss 30% while MQTT 20/20; E3 at 51 dB: ICMP 10/5/50% while MQTT 100/95/100%. | **B** | This is cross-layer path behavior, not evidence of W1 durability or MQTT universal robustness. | **PASS** |
| IC-06 | Recovery behavior depended on the failure/recovery mechanism, and RF-only restoration was not deterministic across all preserved POWDER observations. | POWDER E4–E11; P9 validity/anomaly register; P11 analysis | E10-A: censored no recovery in preserved window; E10-B: restart-assisted recovery with first MQTT publish 6.063318 s from action-begin; E10-C-B: first publish 29.248129 s from RF restore; E10-D upper bound only. | **B** | Timing endpoints are mechanism-specific and cannot be collapsed into one recovery latency; E10-A must remain visible. | **PASS** |
| IC-07 | A broker-only interruption could disrupt MQTT while the LTE path remained healthy in the tested POWDER control. | POWDER E8 private frozen archive; P9 trace map; P11 analysis | During broker interruption, UE and reverse CORE pings remained 20/20 while MQTT records 21–40 were absent; unique delivery 40/60 after preserving duplicate recovery sends. | **B** | E8 is a control/path-isolation result, not an architecture comparison; duplicate sends are preserved and unique IDs govern completeness. | **PASS** |
| IC-08 | FIT and POWDER jointly support a failure-domain-aware validation methodology in which durable record survival and communication-path recovery are treated as distinct properties. | P12 cross-evidence integration, grounded in P11 FIT + POWDER results | FIT directly measures record survival under application/connectivity failure; POWDER separately characterizes RF/path degradation and mechanism-specific recovery. | **C** | Qualitative/structured triangulation only; no pooled reliability percentage, p-value, CI, or cross-platform treatment effect. | **PASS** |
| IC-09 | Both evidence layers demonstrate the value of receiver-side, evidence-first reconciliation for defensible resilience reporting. | FIT generated/received identity reconstruction; POWDER P9 forensic trace map and receiver-side unique sequence reconciliation | FIT conclusions were reconstructed from generated/received ID sets; POWDER completeness uses UE sent vs CORE received unique IDs, including sender/receiver disagreements and duplicate-send handling. | **C** | This is a reproducibility/methodological contribution, not proof that this reconciliation method is uniquely necessary in all IoT studies. | **PASS** |

## 4. Exact evidence traces

### FIT claims IC-01–IC-03

Primary raw authorities:

- R1 Drive ID `14SMrvpmFgX7J2eHIkBuUkEcCwI19c5Nl`, SHA256 `1c18a5e93597607765fbd05ebb7d81554d31735b8644eccf613e2d5162423d55`;
- R2 Drive ID `1Bi8zr7lO6UKn5BSoMrjQhoTcXIL5UtIX`, SHA256 `cf25bdcd4684b6be2d6e5b328776a5704f85a520068c5fe6ace4121c909a0fe7`;
- R3 Drive ID `1Y1bBgs0iclyXeKsDr4tTI-ZcQEqr3EaO`, SHA256 `ef92f4c3cce6e3824669b7771a35ae8c2374275ef4e1b4937c69c79ef47ac3c8`.

Trace:

`claim → P11 FIT reconstructed table → cell generated.jsonl + receiver jsonl / edge_metrics.json → FIT frozen ZIP → SHA256 → Drive ID`

P11 independently reconstructed all 18 cells and found no unexpected receiver IDs.

### POWDER claims IC-04–IC-07

Canonical forensic trace authority:

`evidence/powder/WP2_P9_FORENSIC_TRACE_MAP_2026-08-29.md`

Master P8 authority:

- SHA256 `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878`;
- Drive ID `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR`.

Private E7/E8/E9 preservation authority:

- SHA256 `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8`;
- Drive ID `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K`.

E10/E11 authority:

- SHA256 `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6`;
- Drive ID `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0`.

Trace:

`claim → P11 POWDER derived table / P9 reconstructed metric → run + raw source → frozen authority → SHA256 → Drive ID`

## 5. Claim-specific permitted wording

### IC-01 — permitted

Use language bounded to the exact FIT experiment, for example:

> In the final FIT IoT-LAB experiment, W1 retained 10,000/10,000 records in each outage and outage-plus-gateway-restart replicate, while B0 retained 8,000/10,000.

Do not replace this with “WellPulse is 100% reliable” or “WellPulse outperforms MQTT generally.”

### IC-02 — permitted

State healthy-path equivalence under FIT C0. Do not claim equivalence outside the tested load/hardware.

### IC-03 — permitted

Describe W1 backlog drain as an engineering recovery cost under FIT. Keep reconnect time and backlog-drain time separate.

### IC-04 — permitted

Use “transition region”, “experiment-specific”, and “severe but variable at 52 dB”. Do not use “failure threshold = 52 dB”.

### IC-05 — permitted

State that MQTT remained complete in some windows where ICMP was already degraded. Do not infer that MQTT is always more resilient than ICMP or that W1 caused the tolerance.

### IC-06 — permitted

State exact actions and endpoints. E10-B may support `action-begin → first MQTT publish = 6.063318 s`; E10-C-B may support `RF restore → first publish = 29.248129 s`. E10-A must be reported as non-recovery within the observation window. E10-D remains an upper bound only.

### IC-07 — permitted

State that broker interruption isolated application-layer MQTT failure while the tested LTE ping path remained healthy. Do not generalize to all broker failures or all LTE states.

### IC-08 — permitted

Frame as a validation methodology/result synthesis: record survival and communication-path recovery are distinct resilience properties and were tested in separate evidence layers.

### IC-09 — permitted

Frame receiver-side reconciliation and immutable provenance as a reproducibility practice demonstrated by this project, not as a universal theorem.

## 6. Global prohibited claims

The following remain rejected regardless of wording changes:

1. `WellPulse achieved 100% reliability across FIT and POWDER.`
2. `WellPulse outperformed MQTT on POWDER.`
3. `The scored P7B experiment passed.`
4. `52 dB is the WellPulse/POWDER universal failure threshold.`
5. `UE restart recovers WellPulse in 6 s.` without the exact E10-B action and endpoint.
6. `CORE recovery latency is 29.25 s.` without exact E10-C-B semantics.
7. `Broker recovery latency is 10.9 s.` from E10-D.
8. `RF restoration reliably recovers the system.`
9. `WellPulse is superior to a strongest-available durable MQTT client.`
10. Any rural, field, Siwa, pump, hydraulic, groundwater, agronomic or crop-performance claim.
11. Any pooled FIT+POWDER inferential statistic or global reliability percentage.
12. Any inference of unresolved runtime USRP identity or attenuator-ID→physical-path mapping.

## 7. Claim hierarchy for manuscript construction

### Primary empirical claims

- **P1:** IC-01 — FIT durability/integrity effect under C1/C2.
- **P2:** IC-04 — POWDER transition-region characterization.
- **P3:** IC-06 — failure-domain/recovery-mechanism dependence.

### Supporting empirical claims

- IC-02 healthy FIT control.
- IC-03 durable recovery cost.
- IC-05 cross-layer transition tolerance.
- IC-07 broker-only failure-domain isolation.

### Methodological synthesis claims

- IC-08 failure-domain-aware two-property resilience framework.
- IC-09 receiver-side evidence-first reconciliation/reproducibility.

This hierarchy prevents methodological synthesis from being presented as if it were an additional independent empirical effect.

## 8. Claim-to-RQ mapping

| RQ | Primary claims | Supporting claims |
|---|---|---|
| RQ1 Embedded durability/integrity | IC-01 | IC-02, IC-03 |
| RQ2 Physical RF degradation/transition | IC-04 | IC-05 |
| RQ3 Failure-domain/recovery separation | IC-06 | IC-07, exact FIT C2 restart semantics |
| RQ4 Cross-layer triangulation | IC-08 | IC-09 and bounded results from IC-01/04/06 |

## 9. P14 figure/table authorization envelope

P14 may visualize only claims/measurements that passed P13.

Authorized quantitative sources:

- FIT run-level completeness by architecture/condition;
- FIT permanent-missing counts;
- FIT reconnect and W1 backlog-drain run values;
- POWDER ICMP loss/RTT and MQTT completeness by attenuation/cycle/direction;
- mechanism-specific POWDER recovery timing with censor/upper-bound notation;
- evidence/validation-layer schematic for IC-08/IC-09.

P14 must not create a combined FIT+POWDER reliability score or a visual implying POWDER B1-vs-W1 comparison.

## 10. P13 acceptance gate

- candidate claims assessed: `9/9`;
- claims PASS with bounded wording: `9/9`;
- direct replicated empirical claims (A): `3`;
- direct characterization claims (B): `4`;
- methodological synthesis claims (C): `2`;
- rejected candidate claims: `0`;
- unsupported manuscript-eligible values: `0`;
- pooled FIT+POWDER inferential claims: `0`;
- prohibited scored-P7B promotion: `0`.

`P13_CLAIMS_REVIEWED=9`

`P13_CLAIMS_PASSED=9`

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

`WP2_P13=PASS_CLAIM_EVIDENCE_MATRIX_FROZEN`

`P13_NEXT=WP2_P14_PUBLICATION_TABLES_AND_FIGURES`
