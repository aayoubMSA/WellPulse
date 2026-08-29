# WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry

**Manuscript stage:** P17 consortium-revised internal draft  
**Date:** 2026-08-29  
**Status:** INTERNAL SCIENTIFIC DRAFT — NOT SUBMISSION AUTHORIZATION

**Author:** Dr. Ahmed Elsayed Ayoub  
**Affiliation:** Assistant Professor of Computer Engineering, Department of Computer Systems Engineering, Faculty of Engineering, MSA University, Giza, Egypt

**Authorship/credit control:** the final author list, contributor roles, funding acknowledgments, and institutional/testbed credits must be re-verified before submission. This draft does not invent unverified coauthors or funding attributions.

---

## Abstract

Resilient Internet-of-Things (IoT) telemetry is often discussed as a single reliability problem, although two distinct properties are involved: preserving application records while immediate delivery is unavailable, and restoring the communication path after radio, service, or process failure. This study evaluates these properties separately using complementary real-hardware evidence. On FIT IoT-LAB A8 hardware, a durable WellPulse path (W1) was compared with a **non-durable publish-only baseline (B0)** under healthy operation, deterministic broker outage, and broker outage plus gateway-process restart. Each architecture-condition cell generated 10,000 records in three run-level replicates. Both paths achieved complete final delivery under the healthy condition. Under both failure conditions, B0 permanently missed the 2,000 records generated during the imposed outage interval (8,000/10,000 final records), whereas W1 reconciled 10,000/10,000 records with zero final duplicates in every replicate, an observed +20 percentage-point difference relative to B0. W1's eventual completeness required approximately 67.7–67.9 s of post-outage backlog drainage under the tested workload, showing that record survival and recovery timeliness are different endpoints. A separately executed POWDER reference characterization then examined LTE/ICMP and MQTT behavior under programmed attenuation and mechanism-specific recovery interventions. In an ascending sweep, ICMP loss reached 30% at 51 dB while MQTT remained 20/20; at 52 dB, ICMP loss reached 60% and MQTT completeness fell to 13/20. Repeated 52 dB cycles produced MQTT completeness of 60%, 25%, and 55%. Recovery was also mechanism-dependent: one RF-only timing observation did not recover within its preserved window, while restart-assisted cases produced endpoint-specific timings. FIT and POWDER are not statistically pooled. Together, the evidence supports a failure-domain-aware evaluation methodology in which record-state survival, communication-path recovery, and receiver-side reconciliation are measured explicitly rather than collapsed into one reliability score.

**Keywords:** IoT telemetry; MQTT; durable queues; offline-first; resilience; fault recovery; wireless testbeds; FIT IoT-LAB; POWDER; reproducibility

---

## 1. Introduction

Remote and distributed IoT systems often continue generating measurements while connectivity, infrastructure services, or local processes are unavailable. In such conditions, a successful transport reconnection does not guarantee that records generated during the disruption survived, and durable local storage does not guarantee that the underlying communication path has recovered. Treating these outcomes as one generic notion of “reliability” can therefore hide the actual failure domain and lead to misleading recovery claims.

MQTT is widely used for telemetry because of its lightweight publish/subscribe model and quality-of-service mechanisms. However, durable messaging across failures is not a new idea. MQTT clients may use persistent state, retransmission schemes can recover queued data after network disconnection, offline-first systems reconcile state after connectivity returns, and store-and-forward has been evaluated from edge/cloud to 5G/non-terrestrial-network settings [1–7]. Eclipse Paho, for example, provides file-based persistence specifically so in-flight QoS messages can survive client/device interruption [11]. Consequently, this paper does **not** claim novelty for buffering, persistence, or store-and-forward as standalone mechanisms.

The narrower scientific problem is how to evaluate a telemetry system when failures occur in different domains. Application record state can be lost even when the network later reconnects; conversely, records may remain durably preserved while the radio or service path is still impaired. A robust experiment should therefore distinguish at least: (i) record-state survival, (ii) communication-path recovery, (iii) the exact failure/restart domain, and (iv) end-to-end receiver evidence.

We study this problem through two intentionally non-overlapping evidence layers. The first uses FIT IoT-LAB real embedded hardware to compare W1, a durable application-level telemetry path, with B0, a non-durable publish-only baseline, under controlled healthy, outage, and outage-plus-gateway-process-restart conditions. The second uses POWDER as a controlled wireless instrument to characterize LTE/MQTT degradation and recovery under programmed attenuation, repeated transition-region trials, broker-only failure, and several recovery mechanisms. POWDER is **not** used to estimate a W1-versus-baseline architecture effect.

The paper makes four bounded contributions:

1. **Failure-domain-aware evaluation model.** We separate record-state survival from communication-path recovery and keep restart/failure semantics explicit rather than using a generic outage label.
2. **Receiver-reconciled embedded durability evidence.** Under the exact FIT failure treatments, W1 preserved all 10,000 generated records in every run while the non-durable B0 baseline permanently missed the 2,000 outage-period records; healthy operation was complete for both paths.
3. **Controlled physical-path characterization.** POWDER evidence shows an experiment-specific transition region, cross-layer differences between ICMP and MQTT, and mechanism-dependent recovery rather than one deterministic threshold or recovery clock.
4. **Evidence-preserving reproducibility.** Generated/sent identities are reconciled against receiver identities, and negative, censored, duplicate, anomalous, and setup evidence is retained through a claim-to-raw provenance chain.

The research questions are:

- **RQ1 — Record-state survival:** Under the controlled FIT outage/restart conditions, how does durable W1 record handling differ from the non-durable B0 baseline in final receiver-reconciled completeness, permanent loss, duplicates, and recovery cost?
- **RQ2 — Physical-path transition:** How does the tested LTE/MQTT path behave across the observed POWDER attenuation transition region, including direction dependence and near-transition variability?
- **RQ3 — Failure-domain recovery:** How do RF restoration, UE restart, CORE-related restart, combined recovery, and broker interruption differ in observed recovery behavior and endpoint semantics?

Cross-testbed integration is treated as a synthesis problem rather than as a fourth pooled experiment.

---

## 2. Related Work and Novelty Boundary

### 2.1 MQTT persistence, retransmission, and practical reliability

MQTT reliability depends on more than the nominal QoS label. Persistent client state is an established mechanism for preserving in-flight delivery state across interruptions. Eclipse Paho's Java client documentation explicitly notes that reliable delivery across network/client restarts requires safely stored messages and provides file-based persistence as a standard implementation [11]. This matters directly to the baseline boundary of the present paper: B0 is intentionally non-durable, so the FIT result cannot establish superiority over the strongest available durable MQTT client.

Domingues et al. studied retransmission of MQTT data accumulated during network disconnections and quantified payload-size and retransmission-time trade-offs [3]. Their work establishes local buffering and post-disconnection retransmission as prior art. Gaspar et al. subsequently reported practical MQTT reliability stress testing [4]. At the time of this revision, the bibliographic record and DOI of that article are verified, but no method/result detail not independently recovered from full text is attributed here.

The present contribution therefore lies neither in inventing local persistence nor in claiming a protocol-level MQTT advantage. It instead examines what record-level evidence survives when durability is explicitly present or absent, and how that application property relates to independently characterized path failures.

### 2.2 Robustness and fault injection in MQTT/IoT systems

Jesus et al. proposed a dedicated robustness-assessment approach for MQTT-based IoT systems using message-level fault injection and demonstrated failures in real case studies [2]. This establishes fault-oriented evaluation as an important IoT research problem. The failure model studied here is complementary: we manipulate delivery availability, process state, physical RF attenuation, radio/core restart, and broker availability rather than injecting malformed/perturbed application messages.

This distinction motivates explicit failure-domain labels. A broker interruption, a gateway-process restart, a UE restart, a CORE restart, and an RF impairment do not exercise the same state or recovery mechanism even if all are colloquially called an “outage.”

### 2.3 Offline-first, edge–cloud continuity, and store-and-forward

Colarusso et al. addressed business continuity during Edge–Cloud disconnection through replicated application components and consistency/reconciliation [5]. Herrera et al. proposed a context-aware offline-first edge system combining CRDT-based reconciliation with MQTT-SN [6]. At the network/core level, Monzon Baeza et al. experimentally validated store-and-forward functionality in a distributed 5G core for intermittently connected IoT sensing over LEO non-terrestrial networks [7]. These studies make it inappropriate to claim generic offline-first execution, reconciliation, or store-and-forward as unique WellPulse contributions.

WellPulse instead serves as a concrete durable telemetry implementation for testing how application record state behaves under a controlled loss-of-delivery opportunity and process restart, while a separate radio experiment examines the communication substrate.

### 2.4 Real testbeds, repeatability, and cross-layer experimentation

FIT IoT-LAB provides remotely accessible real embedded devices and has been used explicitly to support repeatable IoT experimentation [8,9]. Papadopoulos et al. argued that carefully characterized testbeds can turn environmental variation and failures into measurable experimental parameters rather than treating them as unexplained noise [9]. The current FIT experiment uses that infrastructure for an architecture-level record-survival comparison.

POWDER was designed for end-to-end wireless experimentation with control and visibility across layers from the radio environment to applications [10]. That property is used here to manipulate programmed attenuation and separate RF, radio/UE, CORE, and broker failure domains.

The two infrastructures therefore serve different inferential roles. They are complementary instruments, not exchangeable samples from one population.

### 2.5 Gap addressed in this study

Prior work separately establishes durable messaging, retransmission, offline-first continuity, robustness testing, store-and-forward, and controlled testbeds. The gap addressed here is **evaluation structure**: a telemetry system can preserve application records while its communication path remains unavailable, or recover the path while records generated during the fault have already been lost. The paper therefore asks whether record-state survival and communication-path recovery can be measured separately, reconciled at the receiver, and integrated without creating a false global reliability metric.

---

## 3. WellPulse Implementation and Failure-Domain Model

### 3.1 W1 durable record semantics

In the evaluated W1 implementation, each telemetry record carries a stable application identity derived from the run identifier, boot identifier, and an eight-digit sequence number:

`record_id = run_id:boot_id:sequence`

The record is serialized canonically using a deterministic JSON representation and assigned a SHA-256 checksum. Local durable state is stored in SQLite with write-ahead logging (`WAL`) and `PRAGMA synchronous=FULL`. Each row has an explicit `PENDING` or `SENT` state. Re-enqueuing an identical record identity/content is idempotent, while reuse of an existing identity with a conflicting payload or checksum raises an integrity error. Final delivery is assessed from receiver-side record identities rather than sender publish status alone.

These semantics are implementation facts from the evaluated code, not an additional experimental result. They explain why W1 can retain application record state across loss of immediate broker delivery and a gateway-process restart.

### 3.2 B0 comparator boundary

B0 is a **non-durable publish-only baseline**. It is intentionally useful for isolating the consequence of application-level durable state, but it is not the strongest MQTT reliability configuration available. Standard MQTT clients can be configured with persistent state, and a durable comparator could reduce or eliminate the observed difference [11].

Accordingly, the FIT comparison supports a bounded statement: under the exact tested outage/restart semantics, W1 retained outage-period records that the non-durable B0 path did not. It does not support “WellPulse beats MQTT” or superiority over a standard durable client.

### 3.3 Two-property resilience model

We define two evaluation properties:

1. **Record-state survival** — whether generated application records remain available for eventual receiver reconciliation after a failure removes immediate delivery opportunity.
2. **Communication-path recovery** — whether and when the underlying network/service path regains the capability to carry traffic after RF, radio, CORE, broker, or process intervention.

The properties interact operationally but are not equivalent. Reconnect can occur before a durable backlog is drained. Lower-layer degradation can appear while application delivery remains complete. A broker can fail while the LTE path remains healthy. This motivates mechanism-specific endpoints and receiver-side accounting.

### 3.4 Failure-domain taxonomy

The experiment set contains deliberately different failure/recovery domains:

| Domain | Representative experiment | Manipulated component | Principal endpoint |
|---|---|---|---|
| Healthy reference | FIT C0; POWDER E9 | none | completeness / clean path |
| Broker delivery outage | FIT C1 | broker reachability | final receiver completeness |
| Broker outage + application process restart | FIT C2 | broker reachability + gateway process | record survival + backlog drain |
| Physical RF impairment | POWDER E1–E4 | programmed attenuation | ICMP/MQTT path behavior |
| UE-assisted recovery | POWDER E5/E10-B | RF restore + UE restart | first ping/publish/receipt |
| CORE-related recovery | POWDER E6/E10-C-B | CORE services + RF restore | first ping/publish |
| Combined recovery | POWDER E7 | RF + CORE + UE sequence | restored path/application |
| Broker-only control | POWDER E8/E10-D | MQTT broker | MQTT versus healthy LTE path |

No timing endpoint from one row is treated as interchangeable with another.

---

## 4. Methods

### 4.1 Evidence roles, experimental unit, and analysis rules

The two testbeds were assigned non-overlapping inferential roles: **FIT IoT-LAB supports the architecture-level B0-versus-W1 record-survival comparison, whereas POWDER supports physical-path degradation and recovery characterization; results are not pooled across platforms.**

The analysis follows an evidence-first policy. Raw evidence is preserved in immutable archives, derived values are reconstructed from approved raw files, and receiver-side identity sets govern final delivery accounting. Failed prerequisites, setup artifacts, duplicate sends, censored observations, missing artifacts, and anomalies remain in the record rather than being silently cleaned.

For FIT, the run/replicate is the scientific unit. The 10,000 messages within a run are repeated observations used for deterministic identity reconciliation and do not create 10,000 independent samples. Because the three run-level completeness differences within each FIT failure condition were identical, we report the raw repeated effects rather than confidence intervals that would imply unsupported population precision.

POWDER is a separately executed controlled reference characterization campaign, not an architecture-effect experiment. Its results are descriptive and experiment-specific.

### 4.2 FIT IoT-LAB experiment

#### 4.2.1 Platform and matrix

The embedded experiment was executed at the Grenoble FIT IoT-LAB site on A8-100 hardware [8]. The final matrix was:

`B0/W1 × C0/C1/C2 × 3 replicates = 18 cells`

Each cell generated exactly 10,000 records.

- **B0:** non-durable publish-only baseline.
- **W1:** WellPulse durable queue with receiver reconciliation.
- **C0:** normal connectivity, no restart.
- **C1:** deterministic broker outage, no gateway-process restart.
- **C2:** deterministic broker outage plus a gateway-process `exec` restart after record 4000.

For C1 and C2, broker TCP/8883 delivery was rejected during records 3001–5000. The C2 treatment is a gateway-process restart, not a whole-node or hardware reboot.

#### 4.2.2 FIT endpoints

For every cell, generated record IDs were independently reconciled with receiver IDs. The final endpoints were:

- unique-record completeness;
- permanent missing count;
- final duplicate count;
- unexpected receiver IDs;
- reconnect time where valid;
- W1 backlog-drain time after recovery.

The principal architecture endpoint is final receiver-reconciled completeness, not successful publish calls.

### 4.3 POWDER reference characterization

#### 4.3.1 Platform and node roles

The POWDER component used a two-node LTE setup under profile `srslte-controlled-rf` [10]. Permanent node roles were:

- `nuc1 / CORE`: EPC/eNB-side functions, MQTT broker/receiver, and CORE-side observation;
- `nuc2 / UE`: srsUE, MQTT publisher, programmed attenuation control, and UE-side observation.

Each accepted experiment used a shared run identifier, pre-treatment LTE/MQTT gates, a declared treatment, node-local evidence capture, independent hashing, off-platform preservation, and sequence/timeline reconciliation.

#### 4.3.2 Transition-region experiments

Three accepted groups support RQ2:

- **E1R4:** ascending 48–52 dB fine sweep;
- **E2:** descending recovery sweep from a severely impaired 52 dB starting state;
- **E3:** three repeated cycles across 49–52 dB.

At each sampled attenuation level, ICMP loss/RTT and MQTT unique-sequence completeness were reconstructed. Programmed attenuation values describe this setup and are not interpreted as a universal link-budget threshold.

#### 4.3.3 Failure-domain and recovery experiments

Additional accepted/control runs separate mechanism classes:

- **E4:** RF-only impairment/recovery reference;
- **E5:** UE-restart-assisted recovery;
- **E6:** CORE-restart recovery;
- **E7:** combined RF/CORE/UE recovery stress case;
- **E8:** broker-only fault control;
- **E9:** no-fault duration-matched control;
- **E10-A–D:** timing-focused runs with exact, censored, or upper-bound semantics;
- **E11:** UE-side restart replications, limited by the absence of an independent CORE collector archive.

Recovery clocks are not collapsed into one metric. E10-A is censored because no recovery was observed inside the preserved window. E10-D is an upper bound because the first post-broker-restart successful MQTT probe was manually initiated.

### 4.4 Reconstruction, receiver-side accounting, and anomalies

FIT results were reconstructed from generated and receiver JSONL identity sets plus verified per-cell metric files. The three frozen FIT archives matched their durable SHA-256 anchors; all scientific source files used for reconstruction verified against the archive manifests.

POWDER values were reconstructed under a forensic validity register. Receiver-side unique sequence IDs govern completeness. This rule matters in several preserved cases. In E1R4, sequence 96 appeared in the sender evidence without a corresponding sender failure flag but was absent at the receiver. E3 sequence 150 showed the same type of disagreement. In E8, recovery records 41–60 were sent twice, producing 80 sender-log lines although only 60 unique IDs existed; receiver-side unique identities prevented the duplicate send from inflating completeness.

The reporting chain is:

`reported value → reconstructed table → raw source → frozen archive → SHA-256 → durable evidence authority`

No numerical conclusion is derived from the project's unclassified screenshots or from unresolved runtime radio/attenuator mappings.

---

## 5. Results

### 5.1 RQ1 — Record-state survival on FIT

Under healthy C0, both B0 and W1 delivered 10,000/10,000 records in all three runs. No healthy-path completeness difference was observed in this workload.

Under C1 broker outage, each B0 run ended with 8,000/10,000 unique receiver records, while each W1 run ended with 10,000/10,000. The same result occurred under C2 broker outage plus gateway-process restart. The observed W1–B0 difference was therefore +20 percentage points in every C1 and C2 run. The 2,000 B0 records missing from each failure run correspond exactly to the records generated during the imposed 3001–5000 outage interval.

Across W1 C0/C1/C2, final reconciliation found all generated record IDs exactly once: no permanent missing records, no final duplicates, and no unexpected receiver IDs. These outcomes demonstrate record-state survival relative to the **non-durable B0 baseline** under the exact treatment; they are not a population reliability probability and not a strongest-client MQTT comparison.

**[Main Figure: FIT architecture-level final completeness]**

Reconnect behavior was much faster than full durable recovery. In C1, mean reconnect time was 1.325412 s for B0 and 1.317088 s for W1. In C2, the corresponding means were 1.362121 s and 1.344870 s. These small differences are descriptive engineering values rather than a powered latency comparison.

W1 then required a measurable backlog-drain interval to reach final completeness: 67.731246 s on average in C1 and 67.870252 s in C2. Thus, eventual lossless reconciliation did not imply instantaneous recovery.

### 5.2 RQ2 — Physical-path transition on POWDER

#### 5.2.1 Ascending fine sweep

In E1R4, the 48–50 dB sampled windows had 0% ICMP loss and 20/20 MQTT delivery. At 51 dB, ICMP loss increased to 30% (14/20 ping replies), while MQTT remained complete at 20/20. At 52 dB, ICMP loss reached 60% and MQTT completeness fell to 13/20 (65%).

The path therefore showed a cross-layer transition: lower-layer impairment became visible before application-level incompleteness.

#### 5.2.2 Descending recovery

E2 began at 52 dB with 65% ICMP loss and 11/20 MQTT delivery (55%). At the sampled 51 dB point, ICMP improved to 10% loss while MQTT recovered to 20/20. At 50 dB and below, the sampled ICMP windows were clean and MQTT remained complete.

The ascending and descending observations support direction-dependent transition/recovery behavior in this setup, but do not define a universal hysteresis width.

**[Main Figure: POWDER transition/direction]**

#### 5.2.3 Near-transition repeated cycles

E3 repeated 49–52 dB three times. MQTT was 100% at 49 and 50 dB in all cycles. At 51 dB, MQTT completeness was 100%, 95%, and 100%, while ICMP loss ranged from 5% to 50%. At 52 dB, MQTT completeness diverged to 60%, 25%, and 55%, while ICMP loss was 80%, 65%, and 70%.

These repeated observations support an experiment-specific transition region rather than a deterministic 52 dB failure threshold.

**[Main Figure: POWDER E3 near-transition repeatability]**

### 5.3 RQ3 — Failure-domain recovery

A single generic “recovery latency” would misrepresent the experiment set.

#### RF-only restoration

E4 provides a valid RF-only reference in which the path recovered after attenuation was restored without restarting UE/CORE services. However, E10-A provides an equally important adverse observation: after RF restoration, neither ping nor MQTT recovered inside the preserved timing window. E10-A is therefore retained as censored non-recovery, demonstrating that RF-only restoration was not deterministic across all observations.

#### UE-restart-assisted recovery

In E10-B, RF restoration plus a UE restart produced the first successful MQTT publish 6.063318 s after the recovery action began and the first successful ping at 6.609430 s. Once the first successful publish occurred, the corresponding CORE receipt followed 0.060172 s later. The latter interval helps separate the dominant reattachment/recovery stage from post-recovery application delivery in this particular run; it is not generalized beyond the measured endpoint.

#### CORE-related recovery

In valid E10-C-B, RF restoration to first ping was 29.247733 s and RF restoration to first successful MQTT publish was 29.248129 s. A preceding E10-C attempt remains a setup artifact and is not combined with the valid run.

#### Broker-only control

E8 provides a particularly clean failure-domain isolation. During the broker interruption, both UE and reverse CORE ping tests remained 20/20 while MQTT records 21–40 were absent. The underlying LTE path therefore remained healthy while the application service failed. The duplicate recovery send was preserved and unique receiver IDs, not sender-line counts, determined the final 40/60 unique delivery result.

E9, the duration-matched no-fault control, delivered 60/60 MQTT records with clean bidirectional ping.

#### Broker timing upper bound

E10-D yielded only an upper bound: broker-start action-begin to the first manually initiated successful publish was ≤10.908749 s. The exact broker recovery time is unresolved and is not inferred.

**[Main Table: mechanism-specific recovery endpoints with exact/censored/upper-bound semantics]**

### 5.4 Cross-evidence synthesis

The FIT and POWDER experiments support different causal statements.

FIT asks whether generated application records survive a controlled loss of immediate broker delivery and a gateway-process restart. Under the tested C1/C2 treatments, W1 preserved them and non-durable B0 did not.

POWDER asks how the communication path itself moves between healthy, degraded, severely impaired, and recovered states under different interventions. It demonstrates transition variability, cross-layer disagreement between ICMP and MQTT, a broker fault with healthy LTE, and mechanism-specific recovery.

Together these results support a layered conclusion: **record-state survival and communication-path recovery are distinct resilience properties.** A system can succeed on one while remaining impaired on the other. The evidence classes are therefore integrated conceptually, not statistically.

---

## 6. Discussion

### 6.1 The FIT effect is a durability result, not a generic MQTT benchmark

The FIT result is experimentally clean but should not be oversold. The failure treatment removed immediate broker delivery for exactly 2,000 generated records. B0, by design, had no durable application state for those records and permanently missed exactly that block; W1 retained durable state and eventually reconciled the full set. Healthy C0 behavior was complete for both paths.

The scientific value is therefore not surprise that persistence preserves state. It is the exact receiver-reconciled demonstration of record survival across the controlled outage and gateway-process restart, including zero final duplicates and an explicit recovery cost. The result should be read as a bounded architecture-validation experiment relative to non-durable B0. A comparison with a strong durable MQTT client remains important future work for any claim of architecture superiority.

### 6.2 Completeness and timeliness are separate engineering objectives

W1's final completeness was 100% under the FIT failure treatments, yet complete backlog reconciliation took about 68 s after connectivity returned. Reconnect itself was around 1.3 s. These clocks answer different questions: reconnection indicates that a transport/session path is available again, while backlog drain indicates when the historical record set has caught up.

This distinction is operationally important. A monitoring application whose requirement is eventual archival integrity may accept a backlog, whereas a control loop with hard freshness deadlines requires latency/freshness endpoints that were not measured in the final FIT workflow. The current evidence therefore supports eventual record integrity, not hard-real-time recovery.

### 6.3 Lower-layer health is not an application-delivery proxy

POWDER provides two complementary counterexamples to simplistic health indicators. In E1R4 at 51 dB, ICMP had already degraded to 30% loss while MQTT remained complete. Conversely, E8 kept the LTE ping path clean while MQTT failed because the broker was unavailable. Lower-layer impairment can therefore precede application loss, and application failure can occur without lower-layer failure.

A resilience monitor should consequently avoid equating one health signal with end-to-end record delivery. The experiment also motivates keeping failure-domain identity explicit in logs and analysis.

### 6.4 Recovery mechanism matters

The recovery runs do not support one universal recovery time. RF-only restoration recovered in E4 but did not recover within the E10-A observation window. E10-B and E10-C-B recovered under different restart sequences and different clocks. E10-D cannot even provide an exact recovery latency because the first probe was manually initiated after broker restart.

The negative E10-A observation is particularly valuable because it prevents a cherry-picked statement that “restoring RF recovers the system.” The scientifically defensible conclusion is narrower: recovery behavior depends on the failure domain, platform state, intervention, and endpoint definition.

### 6.5 Receiver-side reconciliation changes what can be claimed

Sender logs alone did not always describe final delivery. E1R4 sequence 96 and E3 sequence 150 appeared in sender evidence without matching sender failure flags but were absent at the receiver. E8 contained 80 sender-log lines because one recovery sequence was transmitted twice, although only 60 unique IDs existed. A sender-line-based completeness calculation could therefore either miss loss or inflate activity.

The receiver-side unique-ID rule provides a stronger endpoint: a record counts as finally delivered only if its identity is independently present at the receiver. In FIT, generated identities are likewise reconciled against independent receiver identities. This shared practice is one of the strongest methodological links between the two evidence layers.

### 6.6 Negative evidence and provenance are part of the result

The project retains evidence that weakens or complicates a simple narrative: the initial invalid E1 prerequisite run, pre-science E5 setup attempts, the missing frozen E5 forward recovery ping, E8 duplicate sends, E10-A non-recovery, E10-C setup artifact A, E10-D upper-bound semantics, an E7 RTT outlier, sender/receiver disagreements, and manifest-generation anomalies that did not alter scientific source files.

Retaining these cases is scientifically useful. It constrains the claim envelope and makes it possible to distinguish what was observed live from what survived as durable evidence. The analysis workflow therefore reconstructs numerical results from immutable evidence, fixes claim wording against an evidence matrix, and generates displays reproducibly before manuscript interpretation.

### 6.7 Why the two testbeds belong in one study

A potential criticism is that the FIT and POWDER experiments are unrelated. They would be unrelated if both were treated as attempts to estimate one reliability effect. They are coherent when viewed as instruments for different failure properties.

FIT isolates application record state under controlled delivery loss and process restart. POWDER exposes the communication substrate and separates physical RF, UE, CORE, broker, and combined recovery. The first tells us whether records survive; the second tells us how the path itself can fail and recover. The central methodological point is precisely that one cannot substitute for the other.

---

## 7. Threats to Validity and Limitations

### 7.1 Non-durable comparator

B0 is intentionally non-durable and is not the strongest MQTT persistence configuration. Durable MQTT clients and persistent stores are established [11]. Therefore the FIT result demonstrates the effect of W1's durable application record state relative to B0 under the exact workload, not superiority over MQTT generally. A matched durable-client comparator would be the most valuable extension if future work seeks a stronger architecture-comparison claim.

### 7.2 Replication and inference

FIT uses three run-level replicates per architecture-condition cell. The repeated 0 or +20 percentage-point differences are exact observed outcomes under the treatment, not estimates of population reliability. The 10,000 messages within each run do not increase independent n.

POWDER is a controlled reference characterization rather than a powered comparative trial. E3 repeated cycles show local variability but do not estimate a universal probability of failure by attenuation.

### 7.3 Platform/workload scope

FIT and POWDER differ in hardware, workload, failure mechanism, and evidence structure. They are not pooled. The study validates the telemetry/resilience layer only. It does not establish field, industrial-process, rural, Siwa, pump, hydraulic, groundwater, agronomic, or crop performance.

For the same reason, the manuscript uses “IoT telemetry” rather than claiming that the experiment itself constitutes industrial-field validation.

### 7.4 RF instrumentation scope

Programmed attenuation is reported as the controlled experimental variable for the tested POWDER profile. The study does not infer an unresolved individual attenuator-ID-to-physical-path mapping, a universal 52 dB threshold, or unobserved runtime USRP serial/firmware identity.

E11 supplies UE-side replication evidence only because no independent CORE collector archive exists for those runs. E5 lacks the frozen forward recovery-ping artifact and no replacement metric is reconstructed.

### 7.5 Timing semantics

FIT reconnect, FIT backlog drain, POWDER first ping, POWDER first publish, receiver receipt, and broker-restart upper bounds are different endpoints. They are never combined into one recovery-latency distribution. E10-A is censored and E10-D remains an upper bound.

### 7.6 Literature completeness

The related-work survey was refreshed through 29 August 2026. The bibliographic record for Gaspar et al. [4] is verified, but a final full-text comparison remains a pre-submission gate if accessible. Submission-date searching should also check for newly published MQTT resilience, offline-first, and wireless-testbed work.

---

## 8. Reproducibility, Supplementary Material, and Evidence Availability

The project separates raw preservation from the scientific/control record.

- **Raw evidence:** authenticated frozen archives with SHA-256 anchors remain the primary measurement authority.
- **Scientific/control record:** analysis scripts, reconstructed CSVs, validity classes, anomaly registers, claim mappings, figure-generation code, and manuscript governance are versioned in the canonical repository.
- **Detailed experiment atlas:** the WellPulse Experimental Technical Dossier v2.2 documents the FIT matrix and POWDER E0–E11 experiments, run validity, timing semantics, anomalies, evidence roots, and figure provenance.
- **Supplementary manuscript package:** the consortium recommends deriving a reviewer-facing supplement from the dossier rather than copying the entire dossier into the paper.
- **Public/reviewer artifact:** analysis code, derived non-sensitive data, figure-generation scripts, manifests, and releasable evidence should be packaged after a privacy/security sanitization review. Credential-bearing or private platform captures are excluded from public release.

The proposed supplement should include the complete E0–E11 experiment atlas, run-validity register, anomaly register, FIT 18-cell ledger, recovery endpoint definitions, and claim-to-evidence map.

---

## 9. Conclusion

This study separates two resilience properties that are often collapsed into one reliability claim. On real embedded FIT IoT-LAB hardware, W1's durable application record state preserved the complete generated record set under controlled broker outage and outage-plus-gateway-process restart, whereas the **non-durable B0 baseline** permanently missed the 2,000 records generated during each outage interval. That eventual integrity came with a measurable backlog-drain period, demonstrating that record completeness and recovery timeliness are different objectives.

A separate controlled POWDER characterization showed that the communication path behaves differently. Programmed attenuation produced a variable transition region rather than a universal hard threshold; ICMP degradation could precede MQTT incompleteness; MQTT could fail while LTE remained healthy under broker interruption; and recovery depended on mechanism and endpoint. One RF-only timing observation did not recover within its preserved window, while restart-assisted sequences produced distinct, non-interchangeable recovery timings.

The combined evidence supports a failure-domain-aware approach to resilient IoT telemetry: **record-state survival, communication-path recovery, and receiver-side delivery evidence should be measured explicitly and kept distinct.** The study does not claim generic MQTT superiority, a universal RF threshold, or field/industrial-process validation. Its contribution is a bounded architecture experiment plus controlled path characterization, integrated through an evidence-preserving evaluation methodology.

---

## Acknowledgments

The author acknowledges **FIT IoT-LAB** for providing the experimental infrastructure used for the final embedded-hardware experiment and cites the facility reference as requested by its publication guidance [8]. The author also acknowledges **POWDER** for the controlled wireless experimentation infrastructure [10]. Additional collaborator, institutional, funding, and contributor acknowledgments must be verified against project records before submission; none are invented in this internal draft.

---

## References

[1] M. Asgari Araghi and F. Khendek, “A systematic literature review on IoT application layer protocol testing and future research directions,” *Discover Internet of Things*, vol. 6, art. 61, 2026. doi: `10.1007/s43926-026-00322-w`.

[2] B. A. Jesus, F. Lins, and N. Laranjeiro, “An approach to assess robustness of MQTT-based IoT systems,” *Internet of Things*, vol. 31, 101590, 2025. doi: `10.1016/j.iot.2025.101590`.

[3] M. Domingues, J. N. Faria, and D. Portugal, “Dimensioning payload size for fast retransmission of MQTT packets in the wake of network disconnections,” *EURASIP Journal on Wireless Communications and Networking*, vol. 2024, art. 2, 2024. doi: `10.1186/s13638-023-02327-3`.

[4] L. M. Gaspar, J. N. C. Faria, M. Domingues, F. Famá, L. Martins, and D. Portugal, “The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications,” *IEEE Internet of Things Magazine*, 2026. doi: `10.1109/MIOT.2026.3681190`.

[5] C. Colarusso, I. Falco, and E. Zimeo, “Business continuity of Cloud-based IoT applications through a seamless continuum,” *Internet of Things*, vol. 33, 101723, 2025. doi: `10.1016/j.iot.2025.101723`.

[6] N. I. Herrera, E. R. Gómez-Torres, E. E. González, R. M. Toasa, and P. Baldeón, “CAMS F Edge DTN: Context-Aware Offline-First Synchronization and Local Reasoning Using CRDTs and MQTT-SN,” *Future Internet*, vol. 18, no. 4, art. 180, 2026. doi: `10.3390/fi18040180`.

[7] V. Monzon Baeza, F. X. Romero Soto, R. Parada, and C. Monzo, “Experimental Validation of a Distributed 5G Core with Store-and-Forward for IoT Sensing over LEO Non-Terrestrial Networks,” *Sensors*, vol. 26, no. 15, art. 4919, 2026. doi: `10.3390/s26154919`.

[8] C. Adjih et al., “FIT IoT-LAB: A large scale open experimental IoT testbed,” in *2015 IEEE 2nd World Forum on Internet of Things (WF-IoT)*, pp. 459–464, 2015. doi: `10.1109/WF-IOT.2015.7389098`.

[9] G. Z. Papadopoulos, A. Gallais, G. Schreiner, E. Jou, and T. Noël, “Thorough IoT testbed characterization: From proof-of-concept to repeatable experimentations,” *Computer Networks*, vol. 119, pp. 86–101, 2017. doi: `10.1016/j.comnet.2017.03.012`.

[10] J. Breen et al., “Powder: Platform for Open Wireless Data-driven Experimental Research,” *Computer Networks*, vol. 197, 108281, 2021. doi: `10.1016/j.comnet.2021.108281`.

[11] Eclipse Paho Project, `MqttDefaultFilePersistence`, `MqttClient`, and `MqttAsyncClient` Java client documentation, accessed 2026-08-29. Technical documentation describing file-based persistent storage for reliable in-flight MQTT message delivery across client/device interruptions.

---

## Internal P17 control note — remove from any submitted copy

This consortium-revised draft remains governed by the P13 claim envelope and all immutable P16 prohibitions. It also opens a **publication-display recommendation**, not an automatic display change: the consortium recommends replacing the standalone FIT backlog-drain figure with an architecture/evidence-role schematic and moving the backlog plot to supplementary material. That display change requires a separate P17 figure/claim QA gate before becoming submission-facing.

`P17_MANUSCRIPT_REVISION=COMPLETE_INTERNAL_DRAFT`

`P17_NEW_EMPIRICAL_CLAIMS=0`

`P17_NEW_EXPERIMENT_REQUIRED=NO`

`P17_DISPLAY_REDESIGN=RECOMMENDED_PENDING_QA`

`SUBMISSION_AUTHORIZED=NO`
