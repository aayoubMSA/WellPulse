# WellPulse: Failure-Domain-Aware Validation of Durable IIoT Telemetry Across Embedded and Controlled-RF Testbeds

**Manuscript stage:** P15 evidence-bounded full draft  
**Date:** 2026-08-29  
**Status:** INTERNAL SCIENTIFIC DRAFT — NOT SUBMISSION AUTHORIZATION

## Abstract

Intermittent connectivity in industrial Internet of Things (IIoT) systems creates two related but distinct problems: preserving application records while delivery is unavailable, and restoring the communication path after the underlying failure is removed. Treating these as one generic notion of “reliability” can obscure where failures occur and which mechanisms actually recover them. This paper presents WellPulse, a lightweight durable telemetry path, and evaluates these two resilience properties using complementary real-hardware experiments. First, on FIT IoT-LAB A8 hardware, a durable WellPulse path (W1) is compared with a non-durable publish-only baseline (B0) under healthy operation, controlled broker outage, and broker outage plus gateway-process restart. Across three replicates per condition and 10,000 generated records per cell, both architectures delivered 100% under the healthy condition. Under both failure conditions, B0 retained 8,000/10,000 records while W1 retained 10,000/10,000 in every replicate, with no final duplicate records; complete W1 recovery required a post-outage backlog-drain interval of approximately 67.7–67.9 s under the tested workload. Second, a separate manual non-scored POWDER campaign characterizes the LTE/MQTT path under controlled physical attenuation and recovery interventions. The path exhibited an experiment-specific transition region rather than a single deterministic threshold: in one ascending sweep, ICMP loss reached 30% at 51 dB while MQTT remained 20/20, whereas at 52 dB ICMP loss reached 60% and MQTT completeness fell to 13/20. Three near-transition cycles at 52 dB produced MQTT completeness of 60%, 25%, and 55%, showing substantial variability. Recovery also depended on mechanism: RF-only restoration did not recover within one preserved observation window, whereas restart-assisted sequences produced distinct endpoint-specific timings. These evidence classes are not statistically pooled. Together they support a failure-domain-aware validation approach in which durable record survival and communication-path recovery are measured as distinct resilience properties, with receiver-side reconciliation and immutable provenance used to bound every reported result.

**Keywords:** Industrial Internet of Things; MQTT; offline-first telemetry; store-and-forward; resilience; fault recovery; wireless testbeds; FIT IoT-LAB; POWDER; reproducibility

---

## 1. Introduction

Industrial and remote-monitoring IoT systems are often expected to continue producing useful telemetry even when connectivity is intermittent, infrastructure components restart, or the radio path degrades. MQTT is widely used for such systems because of its lightweight publish/subscribe model and quality-of-service mechanisms. However, transport recovery and application-record durability are not equivalent. A client may reconnect successfully while records created during a disruption have already been lost, and a durable queue may preserve records even though the network path itself remains unavailable.

This distinction matters because recent work has already established many of the individual ingredients commonly associated with “resilient IoT.” MQTT robustness assessment, retransmission after network disconnection, edge/cloud continuity, offline-first execution, reconciliation, disruption-tolerant MQTT variants, and store-and-forward in 5G/NTN settings are active and established research areas [1–7]. Consequently, neither buffering nor store-and-forward alone is a defensible novelty claim. A recent systematic review of IoT application-layer protocol testing also identifies continuing challenges around non-determinism, reproducible testbed configurations, and real-world validation [1].

The problem addressed here is therefore narrower: **how should a durable telemetry architecture be validated when application-record survival and physical communication-path recovery fail in different domains?** We study this question through two intentionally separate evidence classes.

The first evidence class uses real embedded hardware on FIT IoT-LAB to compare a durable WellPulse path (W1) against a non-durable publish-only baseline (B0). The experiment isolates application/connectivity failure and gateway-process restart while preserving receiver-side record identity reconciliation. The second evidence class uses the POWDER wireless testbed to characterize an LTE/MQTT path under controlled physical attenuation, near-transition repetition, and several recovery interventions. POWDER is used here as a controlled wireless scientific instrument rather than as an architecture-comparison arm [8]. Importantly, the POWDER campaign is classified as a **manual, non-scored reference experiment**; it is not a completed scored B1-versus-W1 comparison.

The paper makes four bounded contributions:

1. **Real-embedded durability evidence.** A receiver-reconciled comparison of W1 and B0 under healthy, broker-outage, and broker-outage-plus-gateway-restart conditions on FIT IoT-LAB hardware.
2. **Controlled physical-RF characterization.** A two-node POWDER characterization of LTE/ICMP and MQTT behavior across an attenuation transition region, including direction dependence and near-transition variability.
3. **Failure-domain separation.** Experimental distinction among broker failure, physical RF impairment, UE restart, CORE-related restart, gateway-process restart, combined recovery, and no-fault controls, with recovery clocks kept mechanism-specific.
4. **Evidence-first reproducibility.** Receiver-side identity reconciliation, immutable evidence archives, SHA-256 anchors, preserved anomalies, and an explicit claim-to-raw-evidence trace.

The central methodological proposition is not that these two testbeds estimate one global reliability number. Rather, they expose different resilience properties: **record-state survival** and **communication-path recovery**. The analysis therefore keeps FIT and POWDER statistically separate and integrates them only through structured triangulation.

### 1.1 Research questions

- **RQ1 — Embedded durability and integrity:** Under controlled broker outage and gateway-process restart on real embedded hardware, how does W1 differ from B0 in final unique-record completeness, permanent loss, duplicates, and recovery/backlog behavior?
- **RQ2 — Physical RF degradation and transition behavior:** How does the end-to-end LTE/MQTT path behave as controlled attenuation approaches and crosses the observed impairment region, including ICMP loss, MQTT completeness, direction effects, and near-transition variability?
- **RQ3 — Failure-domain and recovery-mechanism separation:** How do RF-only restoration, UE restart, CORE-related recovery, combined recovery, and broker-only interruption differ in observed recovery behavior and timing?
- **RQ4 — Cross-layer triangulation:** What complementary conclusions can be drawn from the embedded durability and controlled-RF evidence while preserving differences in platform, workload, impairment mechanism, and evidence class?

---

## 2. Related Work and Novelty Boundary

### 2.1 MQTT robustness and retransmission

MQTT reliability and robustness have been studied from several directions. Jesus et al. proposed a dedicated robustness-assessment approach based on message-level fault injection and demonstrated failures in real MQTT-based case studies [2]. Their work establishes robustness testing itself as an important problem, but its fault model is different from the connectivity, process-state, and physical-RF failures studied here.

Domingues et al. addressed the recovery of data accumulated during MQTT disconnections using a local retransmission mechanism and performed a large practical study of payload sizing, retransmission time, and throughput [4]. This work is particularly important to the novelty boundary of WellPulse: local buffering followed by MQTT retransmission is established prior art. The present study therefore does not claim novelty for storing records and forwarding them after reconnection. Instead, it focuses on record-level receiver reconciliation, failure-domain decomposition, and complementary real-hardware evidence.

A 2026 article by Gaspar et al., titled *The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications*, further confirms that practical MQTT reliability stress testing remains an active topic [5]. The current public sources available during this manuscript construction confirmed the bibliographic record but did not expose sufficient methods/results for a detailed methodological comparison; no unobserved details from that article are inferred here.

### 2.2 Offline-first, edge continuity, and store-and-forward

Colarusso et al. studied business continuity during transient Edge–Cloud disconnection using edge mirroring and a distributed consistency mechanism [3]. Herrera et al. presented an offline-first edge runtime combining CRDT-based reconciliation, opportunistic connectivity, and MQTT-SN [6]. These works establish that offline-first operation and state reconciliation are not new in themselves.

At the network/core level, Monzon Baeza et al. experimentally validated store-and-forward functionality in a distributed 5G core for intermittently connected LEO non-terrestrial IoT sensing [7]. This again makes a generic “5G plus store-and-forward” novelty claim inappropriate. The present paper instead keeps application durability and radio-path recovery as separate evidence dimensions.

### 2.3 Testbeds and reproducibility

Controlled experimentation is necessary because resilience results can depend strongly on the failure mechanism and platform state. POWDER was designed to provide end-to-end, software-defined wireless experimentation with control and visibility across layers, including controllable attenuation environments [8]. FIT IoT-LAB similarly enables repeatable experiments on real embedded hardware. These platforms are used here for different scientific purposes rather than pooled as exchangeable samples.

The novelty claim is therefore compound and empirical: an embedded architecture comparison with explicit process-state durability, a separate controlled physical-RF characterization, failure-domain-specific recovery semantics, and evidence-preserving receiver reconciliation. This is narrower than earlier project concepts that anticipated a scored POWDER architecture comparison; that scored comparison was not completed and is not implied in this paper.

---

## 3. WellPulse Architecture and Evaluation Model

### 3.1 Architecture under test

WellPulse W1 is a lightweight durable telemetry path designed around application-level record identity and local persistence. Conceptually, a generated telemetry record is assigned a stable identity and durable local state before final cloud reconciliation. Records that cannot be delivered immediately remain recoverable after connectivity returns, and receiver-side identity reconciliation determines whether each generated record ultimately arrived.

The architecture is deliberately evaluated at the record level rather than equating a successful publish call with successful end-to-end delivery. This distinction is important because sender-side status can diverge from receiver evidence, as observed in the POWDER campaign.

### 3.2 Baseline boundary

The FIT comparison uses **B0**, a non-durable publish-only baseline. B0 provides a useful causal contrast for the specific question of application-level durable record survival but is not the strongest durable MQTT configuration available. Therefore, this manuscript does not claim superiority over MQTT generally or over a standard client configured with durable persistence.

An earlier project plan anticipated a matched QoS1/reconnect comparator and a possible durable-client sensitivity arm for a scored POWDER campaign. That confirmatory comparison was not completed. The manuscript is explicitly bounded to the final evidence that exists: FIT B0-versus-W1 for architecture effects and POWDER for physical path characterization.

### 3.3 Two-property resilience model

We distinguish two properties:

1. **Record-state survival:** whether generated application records survive the failure and are ultimately reconciled at the receiver.
2. **Communication-path recovery:** whether and when the underlying end-to-end path regains the capability to carry traffic after RF, service, or process intervention.

These properties interact operationally but are not interchangeable measurements. For example, transport reconnection can precede complete backlog drainage, and lower-layer path degradation can occur while application delivery remains complete.

---

## 4. Methods

## 4.1 Evidence policy and statistical unit

The analysis follows an evidence-first policy. Raw binary archives are retained as immutable authorities, derived metrics are reconstructed from approved raw files, and receiver-side identity sets govern final delivery accounting. Failed attempts, duplicate sends, censored observations, and missing artifacts are retained rather than cleaned away.

For FIT, the experimental **replicate/run** is the scientific unit. The 10,000 messages within a run are repeated observations used for deterministic record reconciliation and are not treated as 10,000 independent statistical replicates. For POWDER, the manual campaign provides controlled characterization rather than a powered architecture treatment comparison. FIT and POWDER are never pooled statistically.

## 4.2 FIT IoT-LAB experiment

### 4.2.1 Platform and matrix

The final embedded experiment was executed on FIT IoT-LAB at Grenoble using A8-100 hardware. The matrix was:

`B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`

Each cell generated exactly 10,000 records.

- **B0:** non-durable publish-only baseline.
- **W1:** WellPulse durable queue plus receiver reconciliation.
- **C0:** normal connectivity, no restart.
- **C1:** deterministic broker outage, no gateway-process restart.
- **C2:** deterministic broker outage plus a WellPulse gateway-process `exec` restart after record 4000.

For C1 and C2, broker connectivity was rejected during records 3001–5000. C2 is a gateway-process restart, not a node/hardware reboot.

### 4.2.2 FIT endpoints

For every cell, generated record IDs were compared with independently captured receiver IDs. We report:

- final unique-record completeness;
- permanent missing count;
- duplicate count after final reconciliation;
- unexpected receiver IDs;
- reconnect time where valid;
- W1 backlog-drain time after recovery.

Because all three replicate-level completeness differences within each failure condition were identical, we report raw replicate effects rather than manufacture confidence intervals that would imply unsupported population precision.

## 4.3 POWDER controlled-RF experiment

### 4.3.1 Platform and evidence class

The POWDER campaign used a two-node LTE setup under profile `srslte-controlled-rf`:

- `nuc1 / CORE`: EPC/eNB-side functions, MQTT broker/receiver, and CORE-side monitoring;
- `nuc2 / UE`: UE-side LTE/MQTT publisher and impairment/recovery actions.

The campaign classification is:

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

It is not a scored B1-versus-W1 experiment and is used only for physical-RF/LTE/MQTT characterization and mechanism-specific recovery observations.

### 4.3.2 RF transition experiments

Three experiment groups support the transition analysis:

- **E1R4:** ascending fine sweep across 48–52 dB attenuation;
- **E2:** descending recovery sweep from severe impairment;
- **E3:** three repeated near-transition cycles across 49–52 dB.

At each sampled attenuation level, ICMP outcome and MQTT unique-sequence delivery were reconstructed. MQTT completeness is based on unique sent sequence IDs at the UE versus unique received sequence IDs at the CORE.

### 4.3.3 Failure-domain and recovery experiments

Additional runs separated recovery mechanisms:

- RF-only impairment/recovery reference;
- UE-restart-assisted recovery;
- CORE-related restart/recovery;
- combined RF and process recovery;
- broker-only interruption control;
- no-fault control;
- timing-focused runs E10-A through E10-D;
- UE-side replication runs E11 with their one-sided evidence limitation.

Timing endpoints are not collapsed. In particular:

- E10-A is a censored RF-only observation with no recovery inside the preserved window;
- E10-B reports action-begin to first MQTT publish and first ping after RF restore plus UE restart;
- E10-C-B reports RF-restore to first ping/publish in its valid recovery sequence;
- E10-D reports only an upper bound from broker action to a manually initiated successful publish.

## 4.4 Evidence reconstruction and anomaly handling

FIT results were reconstructed from each cell's generated and receiver JSONL data plus verified metrics files. The three frozen FIT archives matched their durable SHA-256 anchors. A self-reference artifact in each `SHA256SUMS.txt` was retained and documented; all 103 non-self entries per archive verified and the artifact is not a scientific metric source.

POWDER analysis uses the P9 forensic validity register and trace map. Every surviving value follows the chain:

`reported value → reconstructed table → raw source → frozen archive → SHA-256 → durable evidence authority`

Examples of preserved anomalies include receiver-missing MQTT sequences that lacked matching sender failure flags, duplicate recovery sends in E8, a missing forward recovery-ping artifact in E5, E10-A censoring, E10-D upper-bound semantics, and an E11 collector that is UE-side only. None is silently corrected.

---

## 5. Results

## 5.1 RQ1 — Embedded durability and integrity on FIT

Figure 1 and Table 1 summarize final unique-record completeness. Under C0, both B0 and W1 delivered all 10,000 generated records in all three replicates. Thus, the durable path introduced no observed completeness penalty under the tested healthy condition.

Under C1 broker outage, every B0 replicate retained 8,000/10,000 generated records (80%), while every W1 replicate retained 10,000/10,000 (100%). The absolute W1–B0 difference was therefore +20 percentage points in each of the three replicates. The same separation occurred under C2, where the outage was combined with a gateway-process `exec` restart: B0 retained 8,000/10,000 and W1 retained 10,000/10,000 in every replicate. No unexpected receiver IDs were found, and W1 produced zero final duplicate records after reconciliation.

**[Insert Figure 1 here]**

**Figure 1.** Final unique-record completeness for the FIT IoT-LAB architecture experiment. Each condition contains three replicate-level B0 and W1 observations; small horizontal offsets reveal coincident replicate values without altering measured y values. Both architectures achieved 100% under C0. Under C1 and C2, B0 retained 80% while W1 retained 100% in all three replicates. Results are bounded to the tested FIT workload and B0 non-durable baseline.

These results demonstrate a record-survival advantage for W1 over the specific non-durable B0 treatment. They do not establish a population reliability probability and do not establish superiority over a durable MQTT client.

### 5.1.1 Reconnect and backlog-drain behavior

Reconnect times were similar between B0 and W1. For C1, mean reconnect time was 1.325412 s for B0 and 1.317088 s for W1. For C2, means were 1.362121 s and 1.344870 s, respectively. These differences are treated as engineering characterization rather than a powered latency comparison.

Complete W1 recovery required a measurable backlog-drain interval. The C1 mean was 67.731246 s (range 67.549132–68.047688 s), and the C2 mean was 67.870252 s (range 67.320791–68.851579 s). Figure 2 shows all three run-level values.

**[Insert Figure 2 here]**

**Figure 2.** W1 post-outage backlog-drain time in the FIT IoT-LAB experiment. Symbols show individual replicates and the horizontal segment shows the arithmetic mean. Backlog drain is reported separately from transport reconnect time because they are distinct recovery constructs.

Thus, durability prevented permanent loss in these treatments but did not make recovery instantaneous. The backlog-drain period is an observable cost of eventual record recovery under the tested workload.

## 5.2 RQ2 — Physical RF degradation and transition behavior on POWDER

Figure 3 shows the ascending E1R4 and descending E2 sweeps using ICMP response success (`100 − loss`) and MQTT unique-record completeness on a shared percentage scale.

During E1R4, 48–50 dB produced 0% ICMP loss and 20/20 MQTT delivery. At 51 dB, ICMP loss increased to 30%, but MQTT remained 20/20. At 52 dB, ICMP loss increased to 60% and MQTT completeness fell to 13/20 (65%). The transition was therefore cross-layer rather than simultaneous: lower-layer degradation became visible before application completeness declined.

During E2, the descending sweep began at 52 dB with 65% ICMP loss and 11/20 MQTT delivery (55%). At 51 dB, ICMP loss improved to 10% and MQTT recovered to 20/20. Sampled windows at 50 dB and below were clean for ICMP and complete for MQTT.

**[Insert Figure 3 here]**

**Figure 3.** Cross-layer response during ascending (E1R4) and descending (E2) POWDER attenuation sweeps. ICMP is shown as response success (100 minus packet-loss percentage) so that it shares a common 0–100% scale with MQTT unique-record completeness. At 51 dB in E1R4, ICMP response had fallen to 70% while MQTT remained complete; at 52 dB both layers degraded. The attenuation values are experiment-specific and do not define a universal failure threshold.

### 5.2.1 Near-transition repeatability

E3 repeated the 49–52 dB region three times. MQTT remained 100% at 49 and 50 dB in all cycles. At 51 dB, MQTT completeness was 100%, 95%, and 100%, while ICMP loss was 10%, 5%, and 50%. At 52 dB, the cycles diverged sharply: MQTT completeness was 60%, 25%, and 55%, while ICMP loss was 80%, 65%, and 70%.

**[Insert Figure 4 here]**

**Figure 4.** Near-transition MQTT repeatability in POWDER E3. All three cycles remain complete through 50 dB, remain 95–100% at 51 dB, and diverge at 52 dB (60%, 25%, and 55%), demonstrating severe but variable impairment rather than a single deterministic transition.

The evidence therefore supports an **experiment-specific transition region** around 50–52 dB rather than a universal hard threshold. The magnitude of severe impairment at 52 dB is materially variable across repetitions.

## 5.3 RQ3 — Failure-domain and recovery-mechanism separation

The recovery campaign showed that a single generic “recovery latency” would be scientifically misleading.

In E10-A, RF-only restoration did not produce observed ping or MQTT recovery inside the preserved observation window. This is retained as a censored non-recovery result rather than converted into an inferred latency.

In E10-B, after RF restoration plus a UE-restart action, action-begin to first MQTT publish was 6.063318 s and action-begin to first ping was 6.609430 s. Once the first MQTT publish occurred, the corresponding CORE receipt followed 0.060172 s later.

In the valid E10-C-B sequence, RF restore to first ping was 29.247733 s and RF restore to first MQTT publish was 29.248129 s. A preceding attempt was classified as a setup artifact and is not pooled with the valid timing.

E10-D provides only an upper bound: broker-start action-begin to the first manually initiated successful publish was ≤10.908749 s. It is not an exact broker recovery latency because the probe was manually initiated after recovery could already have occurred.

Table 3 preserves these endpoint definitions and censoring semantics.

The broker-only control E8 further separates application/service failure from radio-path failure. During broker interruption, both UE and reverse CORE ping tests remained 20/20 while MQTT records 21–40 were absent. Duplicate recovery sends were retained in the sender log and unique sequence IDs governed the final 40/60 delivery count. By contrast, the no-fault E9 control delivered 60/60 MQTT records with clean bidirectional ping.

Together these results show that broker interruption, physical RF impairment, UE restart, CORE-related recovery, and gateway-process restart occupy different failure domains and cannot be represented by one generic outage model.

## 5.4 RQ4 — Cross-layer triangulation

The two evidence classes support a layered interpretation rather than a pooled reliability estimate.

The FIT experiment answers an application-state question: when immediate delivery is unavailable, does the architecture preserve generated record state until final receiver reconciliation? Under the tested C1/C2 conditions, W1 did and B0 did not.

The POWDER experiment answers a communication-path question: how does the LTE/MQTT path move from healthy to degraded to severely impaired states, and how does recovery depend on the intervention? The results show an attenuation transition region, cross-layer differences between ICMP and MQTT, and mechanism-specific recovery trajectories.

The integrated result is therefore that resilient telemetry should be evaluated along at least two axes: **survival of application records** and **recovery of the communication path**. A system can succeed on one axis while remaining impaired on the other. FIT backlog drainage after reconnection is one example; POWDER's 51 dB windows with degraded ICMP but complete MQTT are another.

---

## 6. Discussion

## 6.1 Durable record semantics matter at the application boundary

The FIT result is deliberately simple but important. The failure interval generated exactly 2,000 records. B0 permanently missed those 2,000 records in every C1 and C2 replicate, while W1 recovered all of them. Because healthy C0 behavior was complete for both architectures, the observed separation is specifically associated with the failure treatment rather than a general delivery difference in the tested setup.

The strongest interpretation is not that W1 “beats MQTT.” B0 is a non-durable baseline, and prior work has demonstrated database-backed retransmission and durable/offline-first mechanisms [3,4,6,7]. Rather, the FIT result establishes that application-level durable state materially changes record survival across the exact outage/restart treatment. The untested comparison against a strong durable MQTT client remains a limitation.

## 6.2 Reliability has a time cost

W1 achieved complete final delivery at the cost of approximately 68 s of backlog drainage after connectivity returned. This matters for operational interpretation. A system can be lossless in the eventual sense while still exhibiting a substantial interval during which historical records are being reconciled. Systems with hard real-time deadlines would need a different endpoint than eventual final completeness.

This observation aligns with prior retransmission research showing that recovery design involves trade-offs in retransmission time, payload sizing, and throughput [4]. Our contribution here is not a retransmission optimization claim; it is to preserve the distinction between reconnection and complete record recovery in the evaluation.

## 6.3 Physical degradation is a region, not a universal scalar boundary

The POWDER results show why one-shot “failure threshold” measurements are risky. At 51 dB, E1R4 exhibited 30% ICMP loss while all MQTT records arrived. Across E3 cycles at the same nominal 51 dB, ICMP loss varied from 5% to 50% while MQTT remained 95–100%. At 52 dB, both layers were consistently impaired, but MQTT completeness still varied from 25% to 60% across three cycles.

The correct interpretation is therefore local to the tested profile: approximately 50–52 dB formed a transition region in these experiments. No universal link-budget or device-independent threshold is inferred, and the unresolved mapping between individual attenuator identifiers and physical paths is not reconstructed after the fact.

## 6.4 Lower-layer health and application delivery are not interchangeable

The POWDER controls reinforce a broader measurement lesson. In E1R4, application delivery remained complete after ICMP degradation appeared. Conversely, in E8, the LTE ping path remained healthy while MQTT delivery failed because the broker was unavailable. Consequently, neither ICMP success nor transport/session status alone is a sufficient proxy for final application record delivery.

This motivates receiver-side reconciliation. Sender logs contained cases in which a sequence appeared to have been sent without a matching sender failure event but was absent at the receiver. Counting only sender success would therefore have overstated application completeness. Unique receiver IDs provide the more defensible endpoint for this study.

## 6.5 Failure-domain-aware validation

A practical implication is that resilience evaluations should state the failure domain explicitly. “Restart” can mean gateway-process restart, UE restart, CORE restart, broker restart, or full node reboot; these are not equivalent treatments. Likewise, “network outage” can represent application-service unavailability, software path blocking, controlled physical RF attenuation, or loss of volatile process state.

The present evidence suggests a validation structure in which application durability and communication recovery are characterized independently before higher-level claims are integrated. This prevents a successful durable queue from being credited for radio recovery, or a successful radio reconnect from being treated as proof that all records survived.

## 6.6 Reproducibility and negative evidence

The project deliberately retained adverse evidence: the censored E10-A non-recovery observation, duplicate E8 sends, a missing E5 artifact, setup artifacts, sender/receiver disagreements, an RTT outlier, and manifest-generation anomalies that did not affect scientific source files. This is important because removing such evidence would produce a cleaner but less defensible narrative.

The P9–P14 workflow reconstructs numerical results from immutable evidence and then freezes claim wording and display scope before manuscript construction. Although this governance process is not itself a universal experimental standard, it demonstrates how claim-to-raw-evidence traceability can reduce post hoc overinterpretation in systems experiments.

---

## 7. Threats to Validity and Limitations

### 7.1 Comparator limitation

The FIT B0 baseline is intentionally non-durable. The study therefore demonstrates the effect of application-level durability relative to that baseline, not superiority over the strongest MQTT persistence configuration. A durable MQTT client or equivalent persistence mechanism could reduce or eliminate the observed difference. The paper makes no claim to the contrary.

### 7.2 Replication and inference

FIT uses three replicates per architecture-condition cell. The identical 0 or +20 percentage-point completeness differences across replicates are repeated outcomes under the exact treatment, not population reliability probabilities. The message count within each run does not increase the independent sample size.

The POWDER campaign is a manual non-scored characterization campaign, not a powered architecture comparison. Its threshold/recovery findings are descriptive and experiment-specific.

### 7.3 Platform and workload scope

FIT and POWDER differ in hardware, workload, failure mechanism, evidence structure, and scientific role. They are not pooled. The results do not establish rural, field, agricultural, pump, hydraulic, groundwater, or crop performance. Agriculture may motivate the broader WellPulse use case, but the present paper validates the telemetry/resilience layer only.

### 7.4 POWDER instrumentation limits

The study does not infer unresolved runtime USRP serial/firmware identity or individual attenuator-ID-to-physical-path mapping. E11 provides UE-side evidence only and is not used to infer independent CORE metrics. E5 lacks a frozen forward recovery-ping artifact. E10-D remains an upper bound, not exact broker recovery latency.

### 7.5 Related-work completeness

The related-work refresh was performed through 29 August 2026 using publisher, author, institutional, and canonical project sources. The bibliographic existence of Gaspar et al. [5] was confirmed, but accessible sources did not expose sufficient methods/results for a detailed comparison during P15. The manuscript therefore makes no specific methodological claim about that paper beyond its documented scope/title. A final pre-submission literature check remains required.

---

## 8. Reproducibility and Evidence Availability

The project separates durable raw evidence from the scientific/control record.

- **Raw binary evidence:** preserved in authenticated durable archives with SHA-256 anchors.
- **Scientific/control record:** analysis scripts, derived tables, validity classes, anomaly registers, claim mappings, figure-generation code, and current handover are versioned in the canonical repository.
- **FIT reconstruction:** all 18 final cells can be reconstructed from generated/receiver identity sets and verified metrics files.
- **POWDER reconstruction:** surviving numerical claims trace through the forensic map to run-specific raw files, frozen archives, SHA-256 hashes, and durable storage identifiers.

The final public artifact policy will require a separate privacy/security review because some preservation bundles contain private or credential-bearing platform material and cannot be released as-is.

---

## 9. Conclusion

This study evaluated WellPulse resilience without collapsing fundamentally different failure domains into one reliability score. On real embedded FIT IoT-LAB hardware, application-level durable record handling changed the outcome of controlled outage and outage-plus-gateway-restart treatments: W1 preserved 10,000/10,000 records in every replicate while the non-durable B0 baseline retained 8,000/10,000. Complete durable recovery incurred an observable backlog-drain interval of about 68 s under the tested workload.

A separate controlled-RF POWDER campaign showed that communication-path degradation followed an experiment-specific transition region rather than a deterministic universal threshold. ICMP degradation could precede MQTT incompleteness, severe 52 dB impairment varied substantially across repeated cycles, and recovery behavior depended on the intervention. One RF-only timing run did not recover inside its preserved observation window, while restart-assisted sequences produced different endpoint-specific timings.

The combined evidence supports a failure-domain-aware view of IIoT resilience: **record-state survival and communication-path recovery are distinct properties that should be measured separately and reconciled at the receiver before broader claims are made**. This framing also clarifies the study's boundaries: it does not establish scored POWDER architecture superiority, superiority over durable MQTT persistence, a universal RF threshold, or field/agronomic performance.

---

## References

[1] M. Asgari Araghi and F. Khendek, “A systematic literature review on IoT application layer protocol testing and future research directions,” *Discover Internet of Things*, vol. 6, art. 61, 2026. doi: 10.1007/s43926-026-00322-w.

[2] B. A. Jesus, F. Lins, and N. Laranjeiro, “An approach to assess robustness of MQTT-based IoT systems,” *Internet of Things*, vol. 31, 101590, 2025. doi: 10.1016/j.iot.2025.101590.

[3] C. Colarusso, I. Falco, and E. Zimeo, “Business continuity of Cloud-based IoT applications through a seamless continuum,” *Internet of Things*, vol. 33, 101723, 2025. doi: 10.1016/j.iot.2025.101723.

[4] M. Domingues, J. N. Faria, and D. Portugal, “Dimensioning payload size for fast retransmission of MQTT packets in the wake of network disconnections,” *EURASIP Journal on Wireless Communications and Networking*, vol. 2024, art. 2, 2024. doi: 10.1186/s13638-023-02327-3.

[5] L. M. Gaspar, J. N. C. Faria, M. Domingues, F. Famá, L. Martins, and D. Portugal, “The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications,” *IEEE Internet of Things Magazine*, 2026. doi: 10.1109/MIOT.2026.3681190.

[6] N. I. Herrera, E. R. Gómez-Torres, E. E. González, R. M. Toasa, and P. Baldeón, “CAMS F Edge DTN: Context-Aware Offline-First Synchronization and Local Reasoning Using CRDTs and MQTT-SN,” *Future Internet*, vol. 18, no. 4, art. 180, 2026. doi: 10.3390/fi18040180.

[7] V. Monzon Baeza, F. X. Romero Soto, R. Parada, and C. Monzo, “Experimental Validation of a Distributed 5G Core with Store-and-Forward for IoT Sensing over LEO Non-Terrestrial Networks,” *Sensors*, vol. 26, no. 15, art. 4919, 2026. doi: 10.3390/s26154919.

[8] J. Breen et al., “Powder: Platform for Open Wireless Data-driven Experimental Research,” *Computer Networks*, vol. 197, 108281, 2021. doi: 10.1016/j.comnet.2021.108281.

---

## Internal manuscript-control note

This draft is governed by the frozen P13 claim envelope and P14 displays. It must not be edited later to introduce any of the following without reopening scientific QA: scored P7B success; POWDER B1-vs-W1 superiority; strongest-durable-MQTT superiority; universal 52 dB threshold; deterministic RF-only recovery; exact E10-D broker latency; population reliability from message counts/three FIT replicates; field/Siwa/pump/hydraulic/agronomic validation; unresolved RF-path/runtime-radio identity; or pooled FIT+POWDER inferential statistics.
