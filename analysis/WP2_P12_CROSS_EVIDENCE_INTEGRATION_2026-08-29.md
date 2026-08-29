# WP2-P12 — Cross-Evidence Integration

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **PASS / COMPLETE**

## 1. Purpose

Integrate the two completed WellPulse evidence classes into one scientifically coherent interpretation without pooling incompatible data, inventing a missing POWDER architecture comparison, or expanding claims beyond the P10/P11 evidence envelope.

This WP does not draft manuscript prose, select a venue, generate final figures, authorize experiments, execute B2, or modify any raw evidence.

## 2. Evidence classes remain distinct

### FIT — architecture-comparison evidence

Authority: `FINAL_WP_RT01_FIT_A8`.

Role:
- direct `B0 vs W1` comparison;
- real embedded A8 hardware;
- C0 healthy, C1 broker outage, C2 broker outage + gateway-process exec restart;
- 3 replicates per architecture-condition cell;
- 10,000 records per cell;
- final receiver reconciliation.

Primary supported scientific dimension: **record durability/integrity under controlled application/connectivity failure**.

### POWDER — physical-RF/recovery evidence

Authority: `WP2-P8` + `WP2-P9`, classification `P8_CLASS=MANUAL_NON_SCORED_REFERENCE`.

Role:
- controlled physical attenuation;
- LTE/ICMP and MQTT behavior near the impairment transition;
- hysteresis and repeatability;
- RF-only, UE-restart, CORE-restart, combined-recovery, broker-only and no-fault controls;
- mechanism-specific recovery timing;
- two-node forensic reconciliation.

Primary supported scientific dimension: **physical communication-path degradation and failure-domain-specific recovery**.

## 3. Integration principle

The two evidence classes are **complementary, not substitutable**.

FIT answers:

> Does application-level durable record handling prevent permanent telemetry loss under the frozen outage/restart conditions compared with a non-durable baseline?

POWDER answers:

> How does the underlying LTE/MQTT communication path degrade and recover under controlled RF and service/process interventions?

Therefore the scientifically valid project-level interpretation is:

> WellPulse has demonstrated a durable-record advantage over a non-durable baseline under controlled embedded outage/restart conditions, while an independent controlled-RF campaign shows that the communication substrate itself exhibits a variable transition region and recovery behavior that depends on the failure and recovery mechanism.

This is **failure-domain-aware triangulation**. It is not a single combined reliability estimate.

## 4. Cross-evidence integration matrix

| Scientific dimension | FIT authority | POWDER authority | Integrated interpretation |
|---|---|---|---|
| Healthy operation | B0/W1 both 100% in C0 | E9 60/60 MQTT + clean bidirectional ping | Both evidence classes provide healthy-reference behavior, but under different workloads/platforms; no pooled baseline is computed. |
| Permanent record loss under outage | B0 loses exactly 2,000/10,000 in C1/C2; W1 retains 10,000/10,000 | E4–E8 show outage-phase MQTT incompleteness in the manual RF/service cases | Application-layer loss can arise from different failure domains; only FIT supports the B0-vs-W1 durability effect. |
| Durable recovery cost | W1 backlog drain ~67.7–67.9 s after outage/restart | P8/P9 provides mechanism-specific recovery timing, e.g. E10-B ~6 s and E10-C-B ~29.25 s for different recovery definitions | Recovery time is mechanism- and endpoint-specific. FIT backlog drain must not be numerically compared with POWDER attach/publish timing as if they measured the same construct. |
| Physical degradation transition | Not tested physically | E1–E3: healthy 48–49 dB region, variable degradation 50–51 dB, severe impairment at 52 dB in this setup | Physical RF degradation is independently characterized on POWDER; it cannot be attributed to WellPulse architecture performance. |
| Cross-layer tolerance | FIT does not expose RF transition | At 51 dB E1R4, ICMP loss 30% while MQTT remained 20/20 | Application-layer delivery can remain intact after lower-layer degradation becomes visible, but this is a POWDER path observation, not evidence of W1 durability. |
| Restart domain | C2 = gateway-process exec restart | E5/E10-B UE restart; E6/E10-C CORE-related restart; E7 combined restart | Restart semantics materially change the failure domain; terms must remain exact and never collapse into generic “system restart.” |
| Broker-only failure | C1 uses broker outage as the application/connectivity treatment | E8 isolates broker failure while LTE remains healthy | Together they support the methodological need to separate application/service failure from physical radio failure. They are not statistically combined. |
| Reproducibility/provenance | final artifacts, hashes, generated/received identity reconciliation | frozen archives, SHA256, anomaly register, trace map | Both layers support an evidence-first reproducibility contribution, though their artifact structures differ. |

## 5. Integrated interpretation by research question

### RQ1 — Embedded durability/integrity

Evidence source: FIT only.

Result retained:
- C0: B0 and W1 both 100% completeness in 3/3 replicates;
- C1: W1-B0 = +20 percentage points in 3/3;
- C2: W1-B0 = +20 percentage points in 3/3;
- B0 permanently misses exactly 2,000/10,000 records in every C1/C2 run;
- W1 preserves 10,000/10,000 in every C1/C2 run with zero final duplicate records;
- W1 recovery carries a measured backlog-drain cost of ~67.7–67.9 s under this workload.

POWDER does not strengthen this effect estimate numerically because it did not execute the same architecture comparison.

### RQ2 — Physical RF degradation/transition

Evidence source: POWDER only.

Result retained:
- 48–49 dB sampled region is consistently healthy;
- 50–51 dB is a variable degradation/transition region;
- 52 dB is severely impaired in the tested profile;
- ICMP can degrade before MQTT completeness falls;
- direction/hysteresis and cycle variability matter;
- there is no universal scalar threshold claim.

FIT does not validate this RF behavior.

### RQ3 — Failure-domain/recovery separation

Evidence source: primarily POWDER, with FIT supplying a distinct gateway-process-restart example.

Integrated result:
- broker outage, RF impairment, UE restart, CORE restart, gateway-process restart and combined recovery are materially different treatments;
- recovery metrics from one treatment are not interchangeable with those from another;
- RF restoration alone is not deterministic across all preserved POWDER observations;
- restart-assisted recovery can restore service under the tested sequences;
- broker-only failure can interrupt MQTT while LTE remains healthy;
- durable application-level recovery on FIT addresses record preservation, not radio reattachment.

### RQ4 — Cross-layer triangulation

The strongest project-level synthesis is a layered causal boundary:

1. **FIT layer:** demonstrates the consequence of having or not having durable record semantics when application/connectivity failure removes immediate delivery opportunity.
2. **POWDER layer:** demonstrates that the network substrate can move through healthy, degraded and severely impaired states, and that restoration/restart mechanisms produce different recovery trajectories.
3. **Combined interpretation:** a resilient telemetry system must be evaluated both for **record-state survival** and for **communication-path recovery**; success in one layer does not guarantee success in the other.

This is the central cross-evidence result of P12.

## 6. What can be integrated quantitatively

Only within each evidence class.

Allowed:
- FIT B0-vs-W1 differences within C0/C1/C2;
- FIT reconnect/backlog summaries within the FIT design;
- POWDER attenuation-level ICMP/MQTT summaries;
- POWDER within-run/within-experiment recovery timing using P9 endpoint semantics.

Not allowed:
- pooled FIT+POWDER completeness;
- pooled “reliability percentage”;
- comparing FIT backlog drain directly against POWDER recovery latency as a treatment effect;
- using POWDER MQTT completeness as W1 performance;
- using FIT C1/C2 as evidence for physical RF behavior.

## 7. Cross-evidence consistency and tension

### Consistent findings

1. **Failure-domain identity matters.** Both platforms show that different failure mechanisms produce different observable outcomes.
2. **Application success is not equivalent to lower-layer health.** POWDER demonstrates MQTT can remain complete when ICMP is already degraded.
3. **Recovery is multi-stage.** FIT separates reconnect from backlog drain; POWDER separates RF restore, service readiness, ping, publish and receiver-side receipt.
4. **Receiver-side reconciliation is essential.** Both evidence systems depend on end-to-end receiver evidence rather than sender success alone.
5. **Healthy controls are necessary.** FIT C0 and POWDER E9 establish platform-specific no-fault reference behavior.

### Tensions that must remain visible

1. FIT's non-durable B0 is intentionally weaker than a durable standard MQTT client; no strongest-client superiority claim is available.
2. POWDER did not execute the scored B1-vs-W1 comparison anticipated by the earlier WP0 design.
3. POWDER RF-only recovery is not deterministic across all observations; E10-A is a valid censored non-recovery case.
4. FIT completeness effects are repeated deterministic outcomes under the exact treatment, not population reliability probabilities.
5. Platform workloads, impairment mechanisms, hardware and evidence schemas differ substantially.

These tensions narrow the paper but strengthen its defensibility.

## 8. Candidate project-level conclusions allowed into P13 claim mapping

The following are **candidate claims for evidence mapping**, not manuscript prose:

- `IC-01`: Under the exact FIT final outage conditions, W1 preserved all 10,000 generated records in every C1/C2 replicate, whereas B0 permanently missed the 2,000 outage-period records.
- `IC-02`: Under healthy FIT C0, both B0 and W1 achieved complete final delivery in all replicates.
- `IC-03`: W1's complete FIT recovery required a measurable backlog-drain interval after connectivity returned.
- `IC-04`: In the tested POWDER profile, physical degradation was a region rather than a single deterministic threshold, with severe but variable impairment at 52 dB.
- `IC-05`: In the POWDER transition region, ICMP degradation could precede MQTT incompleteness.
- `IC-06`: Recovery behavior depended on the failure/recovery mechanism; RF-only restoration was not deterministic across all preserved observations.
- `IC-07`: Broker-only interruption could break MQTT while the LTE path remained healthy.
- `IC-08`: FIT and POWDER jointly support a failure-domain-aware validation methodology in which durable record survival and communication-path recovery are treated as distinct properties.
- `IC-09`: Both evidence layers support receiver-side, evidence-first reconciliation as a necessary basis for defensible resilience reporting.

Every candidate claim above must pass P13 claim-to-evidence mapping before manuscript use.

## 9. Explicitly prohibited integrated claims

P12 prohibits:
- “WellPulse achieved 100% reliability across FIT and POWDER”;
- “WellPulse outperformed MQTT on POWDER”;
- “52 dB is the WellPulse failure threshold”;
- “UE restart recovers WellPulse in 6 s” without preserving the exact E10-B action/endpoint semantics;
- “CORE recovery latency is 29.25 s” without preserving the exact E10-C-B semantics;
- “broker recovery latency is 10.9 s” from E10-D;
- “RF-only restoration reliably recovers the system”;
- any field/rural/Siwa/pump/hydraulic/agronomic inference;
- any pooled p-value, confidence interval, or reliability estimate spanning FIT and POWDER.

## 10. P12 acceptance gate

- FIT and POWDER roles explicitly separated: PASS;
- no pooled inference introduced: PASS;
- architecture-comparison authority restricted to FIT: PASS;
- physical-RF authority restricted to POWDER: PASS;
- recovery endpoints preserved by failure domain: PASS;
- negative/censored/anomalous evidence retained: PASS;
- candidate integrated claims bounded for P13: PASS;
- no manuscript prose/final figures/new experiments created: PASS.

`P12_UNSUPPORTED_INTEGRATED_CLAIMS=0`

`P12_STATISTICAL_POOLING=NONE`

`WP2_P12=PASS_CROSS_EVIDENCE_INTEGRATION`

`P12_NEXT=WP2_P13_CLAIM_EVIDENCE_MATRIX`
