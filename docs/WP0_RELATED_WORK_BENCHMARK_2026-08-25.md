# WP0 — Related-Work Benchmark and Reviewer-Attack Audit — 2026-08-25

**Status:** PRE-G4 MANUSCRIPT-GRADE RAPID STRUCTURED BENCHMARK

**Purpose:** stress-test the frozen WellPulse novelty position and POWDER experimental design against the closest prior and current work before physical-RF experimentation proceeds.

**Methodological label:** this is a targeted rapid structured benchmark, not a new PRISMA systematic review. It uses publisher pages, authoritative author/institution pages, official software documentation, and an existing 2026 systematic literature review as an anchor. Claims below are limited to what those sources exposed at the time of review. Where full text was not available, the entry is explicitly marked as abstract/metadata-limited.

**Search date:** 2026-08-25.

## 1. Executive verdict

The survey **does not invalidate the current WellPulse paper design**, but it makes the novelty boundary much sharper.

The following ingredients are already established in prior work and must **not** be presented as standalone novelty:

- MQTT reliability/robustness testing;
- QoS/retransmission tuning;
- local buffering/database-backed retransmission;
- store-and-forward under intermittent connectivity;
- offline-first execution;
- edge/cloud reconciliation;
- DTN-enhanced MQTT or MQTT-SN;
- cellular/5G/NB-IoT use for resilient IoT;
- smart-farming / remote-agriculture MQTT monitoring;
- testbed-based experimental validation itself.

The defensible WellPulse contribution remains a **compound experimental and architectural contribution**, not a new buffering primitive:

1. **Matched strong comparator:** standard MQTT v3.1.1 QoS1 + automatic reconnect with the same Paho transport/session parameters, but without application-level disk durability or application-level reconciliation.
2. **Explicit process-restart durability test:** separate network-only impairment from network + gateway-process restart, exploiting the documented boundary between broker-side MQTT session semantics and client application state that is lost when the Paho client process restarts.
3. **Record-level integrity semantics:** durable application record identity, checksum, explicit durable state, replay, idempotent cloud ingestion, and deterministic reconciliation.
4. **Causal physical-RF experiment:** programmable conducted RF impairment with recorded radio context rather than software-only disconnection.
5. **Validation ladder:** real embedded hardware (FIT IoT-LAB) -> controlled physical RF (POWDER) -> compact OTA replication, with each layer kept as a separate validity claim.
6. **Run-level inferential discipline and reproducibility:** paired randomized run-level design, precision-based replication, complete manifests/evidence, and deterministic endpoint reconstruction.

**Protocol decision:** **NO PRE-G4 SCIENTIFIC PROTOCOL AMENDMENT REQUIRED.** The existing B1/W1 contrast, S0-S3 scenario structure, physical-RF requirement, run-level statistical unit, evidence design, and compact OTA replication remain justified. Several measurement emphases are reinforced below.

## 2. Anchor evidence about the state of IoT protocol testing

### 2.1 2026 systematic literature review

Asgari Araghi and Khendek, *A systematic literature review on IoT application layer protocol testing and future research directions*, Discover Internet of Things 6, 61 (2026), DOI: `10.1007/s43926-026-00322-w`.

The review searched work from 2010-2025, retrieved 822 records, and retained 47 primary studies under PRISMA. It identifies MQTT as the most investigated application-layer protocol and highlights persistent challenges including non-determinism, narrow testing tools, limited reproducible testbed configurations, and lack of real-world environments. It explicitly calls for larger/domain-specific testbeds and more real-world validation, including in IIoT.

**WellPulse implication:** a paper framed as merely "testing MQTT" is weak. A reproducible, causal, multi-layer validation study in IIoT is better aligned with the identified research gap.

## 3. Closest related work benchmark

Threat levels below mean threat to a **potential novelty claim**, not paper quality.

| # | Work | What it already establishes | Evidence mode exposed in review | Threat to naive WellPulse claim | What remains distinct/relevant for WellPulse |
|---:|---|---|---|---|---|
| 1 | Jesus, Lins, Laranjeiro, **An approach to assess robustness of MQTT-based IoT systems**, Internet of Things 31 (2025), 101590. DOI `10.1016/j.iot.2025.101590` | Dedicated MQTT robustness assessment through message-level fault injection; demonstrated on two real case studies (Smart Rural and MInA). | Real case studies; application-level fault injection. | **HIGH** to "MQTT robustness evaluation is novel". | WellPulse should emphasize recovery/integrity under controlled connectivity/RF state, not malformed-message robustness. |
| 2 | Colarusso, Falco, Zimeo, **Business continuity of Cloud-based IoT applications through a seamless continuum**, Internet of Things 33 (2025), 101723. DOI `10.1016/j.iot.2025.101723` | Edge mirroring of cloud components/data and reconciliation through EdgeCloudWPaxos during transient network failure. | Emulated retail-shop activity and network failure. | **HIGH** to generic "edge/cloud continuity and reconciliation" novelty. | WellPulse is narrower: append-only industrial telemetry integrity, matched MQTT comparator, process restart, physical RF, cross-testbed evidence. |
| 3 | Domingues, Faria, Portugal, **Dimensioning payload size for fast retransmission of MQTT packets in the wake of network disconnections**, EURASIP JWCN (2024), Art. 2. DOI `10.1186/s13638-023-02327-3` | Local database-backed recovery of data accumulated during disconnection; real hardware; systematic retransmission-time/throughput optimization; 4300 tests; configurations repeated 100 times. | Real-world healthcare hardware; controlled disconnection/recovery. | **VERY HIGH** to "database/store then retransmit over MQTT" novelty. | No evidence in the reviewed paper of the full WellPulse causal package: same-transport B1/W1 matched contrast, explicit client-process restart durability, record checksum/idempotent final reconciliation, controlled physical RF, FIT->RF->OTA ladder. |
| 4 | Gaspar et al., **The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications**, IEEE Internet of Things Magazine (2026). DOI `10.1109/MIOT.2026.3681190` | Current title/metadata establish a 2026 practical MQTT reliability stress-test paper from the same Coimbra research line. | **FULL TEXT / ABSTRACT NOT RECOVERED IN THIS REVIEW.** Metadata confirmed from author/institution pages. | **POTENTIALLY VERY HIGH — unresolved.** | Mandatory full-text comparison before final manuscript novelty freeze. Do not infer methods/results that were not accessible. Does not block G4 because current design already uses a strong comparator and causal RF/restart decomposition. |
| 5 | Baumgärtner, **Dtnmqtt: A Resilient Drop-In Solution for MQTT in Challenging Network Conditions**, FICC 2024, pp. 524-543. DOI `10.1007/978-3-031-54053-0_36` | Drop-in MQTT semantic replacement mapped to DTN Bundle Protocol; targets challenged connectivity; reports higher delivery than pure MQTT/mesh and low resource footprint. | Challenging-network evaluation; abstract available. | **HIGH** to broad "resilient MQTT under disruption" novelty. | Different mechanism: DTN protocol mapping/opportunistic networking rather than application-level durable record semantics over matched ordinary MQTT. |
| 6 | Bauer, Aschenbruck, **Measuring and Adapting MQTT in Cellular Networks for Collaborative Smart Farming**, IEEE LCN 2017, pp. 294-302. DOI `10.1109/LCN.2017.81` | Real-world cellular smart-farming MQTT under handovers/dead zones; evaluates publisher-broker and broker-subscriber links; studies MQTT parameterization and alternate queue strategies. | Real-world mobile cellular scenarios. | **VERY HIGH** to "MQTT + rural/smart farming + cellular disruptions" novelty. | WellPulse must not sell the application/rural/cellular combination as novelty. Distinction is durable process-restart integrity plus controlled causal RF and reproducibility ladder. |
| 7 | Herrera et al., **CAMS F Edge DTN: Context-Aware Offline-First Synchronization and Local Reasoning Using CRDTs and MQTT-SN**, Future Internet 18(4), 180 (2026). DOI `10.3390/fi18040180` | Offline-first runtime; CRDT reconciliation; opportunistic Bluetooth/Wi-Fi Direct; MQTT-SN; controlled rural-logistics/healthcare cases; deterministic convergence. | Controlled experiments/case studies. | **VERY HIGH** to generic "offline-first + reconciliation" novelty. | Broader context-aware/DTN state replication problem. WellPulse remains telemetry-integrity-focused with matched MQTT baseline, restart failure decomposition, physical RF and cross-testbed evidence. |
| 8 | Monzon Baeza et al., **Experimental Validation of a Distributed 5G Core with Store-and-Forward for IoT Sensing over LEO Non-Terrestrial Networks**, Sensors 26(15), 4919 (2026). DOI `10.3390/s26154919` | 5G-core-integrated store-and-forward preserving IoT sensing data through intermittent LEO backhaul; functional prototype with Open5GS, UERANSIM and emulated satellite node. | Functional prototype; intermittent-connectivity experimental validation. | **VERY HIGH** to "5G + store-and-forward + lossless recovery" novelty. | Core/NTN architecture rather than ordinary MQTT application durability; user-plane/RF question differs; no basis to claim physical-RF causal attenuation from this paper. |
| 9 | **A Disruption Tolerant Architecture based on MQTT for IoT Applications** (2017) | MQTT-SN combined with IBR-DTN; validated on real devices with publishers/subscribers; shows robustness under unstable/partitioned links. | Real devices; DTN architecture. | **HIGH** to broad MQTT disruption-tolerance novelty. | Historical prior art reinforces that generic DTN/offline connectivity is not WellPulse's contribution. |
| 10 | Bozorgi, Assaf, Katsanis, **Configuration and execution of a scalable IoT architecture for smart home automation**, Internet of Things 37 (2026), 101900. DOI `10.1016/j.iot.2026.101900` | Scalable NB-IoT + MQTT + serverless-cloud smart-appliance architecture and evaluation. | Prototype/evaluation per available abstract. | **MEDIUM** to generic scalable MQTT/NB-IoT system architecture. | Available abstract does not establish the WellPulse-specific durable restart/reconciliation/RF experiment; do not overstate similarity without full text. |
| 11 | Matias, Macêdo, **Resilient IIoT Communication via Edge-Based Store-and-Forward and SLO Monitoring**, WTF 2026. DOI `10.5753/wtf.2026.24074` | WIP IIoT architecture combining OPC UA-MQTT translation, edge store-and-forward and SLO monitoring for WAN instability. | WIP; abstract/metadata-limited in this review. | **HIGH** to generic "IIoT edge store-and-forward" novelty. | Preliminary scope; WellPulse needs stronger real-RF causal evidence, matched baseline, integrity/reconciliation and run-level replication. |
| 12 | Chang et al., **Gateway-Assisted Retransmission for Lightweight and Reliable IoT Communications**, Sensors 16(10), 1560 (2016). DOI `10.3390/s16101560` | Retransmission/RTO optimization for MQTT-SN/CoAP reliability. | Simulation models. | **MEDIUM** to generic retransmission reliability. | Different level and protocol question; supports retaining recovery/overhead metrics. |
| 13 | **Stress-Testing MQTT Brokers: A Comparative Analysis of Performance Measurements**, Energies 14(18), 5817 (2021). DOI `10.3390/en14185817` | Broker performance/stress benchmarking. | Experimental broker-performance evaluation. | **LOW-MEDIUM** to generic MQTT performance testing. | WellPulse is architecture/failure recovery, not broker benchmark. |
| 14 | Papadopoulos et al., **Thorough IoT testbed characterization: From proof-of-concept to repeatable experimentations**, Computer Networks 119 (2017), 86-101. DOI `10.1016/j.comnet.2017.03.012` | Shows how FIT IoT-LAB can support repeatable/reproducible experiments and why stable links/hardware/environment characterization matter. | FIT IoT-LAB real testbed. | Not a novelty threat; **methodological anchor**. | Supports our separation of PoC from repeated testbed evidence and explicit characterization. |
| 15 | Breen et al., **POWDER: Platform for Open Wireless Data-driven Experimental Research**, WiNTECH 2020. DOI `10.1145/3411276.3412204` | POWDER as end-to-end programmable wireless research infrastructure; PhantomNet controlled-RF environment with Faraday cages and software-controlled attenuator matrix; transition toward real-world wireless environments. | Controlled RF + real wireless platform. | Not a novelty threat; **methodological anchor**. | Directly supports controlled-RF first and OTA second as distinct validation layers. |
| 16 | Mimouni et al., **Design of an Energy-Optimized IoT System for Off-Grid Agriculture: Solar-Powered Monitoring and Irrigation Control**, Scientific African (online 24 Jul 2026), e03533. DOI `10.1016/j.sciaf.2026.e03533` | PV/battery-powered rural agriculture monitoring/control using GSM/GPRS + MQTT + ThingsBoard; seven-day real agricultural deployment; ~96.8% telemetry success. | Real agricultural deployment. | **VERY HIGH** to "solar/agriculture/MQTT remote monitoring" novelty. | Confirms WellPulse must keep agriculture as application motivation, not novelty; our current remote-testbed evidence cannot substitute for field validation. |
| 17 | Bicamumakuba et al., **Real-Time Remote Monitoring of Environmental Conditions and Actuator Status in Smart Greenhouses Using a Smartphone Application**, Sensors 26(5), 1548 (2026). DOI `10.3390/s26051548` | 54 sensing + 12 actuator nodes, LoRaWAN gateway, MQTT/cloud supervisory monitoring; commercial-greenhouse feasibility and resource profiling. | Large real greenhouse deployment. | **MEDIUM-HIGH** to generic agricultural IoT monitoring/scalability. | Different primary question; again reinforces that WellPulse paper should be resilience/integrity, not a generic smart-agriculture platform paper. |
| 18 | Zhang et al., **A Survey on Industrial Internet of Things (IIoT) Testbeds for Connectivity Research**, arXiv:2404.17485 (2024) | Surveys IIoT connectivity testbeds across TSN, 802.15.4, 802.11, 5G; argues for controlled evaluation before real deployment and summarizes testbed design practices. | Survey/preprint. | Not direct novelty threat; **contextual anchor**. | Supports the use of testbeds as staged validation instruments; lower evidentiary weight than peer-reviewed primary studies. |

## 4. Official Paho evidence and why S3 matters

The Eclipse Paho Python project documents a critical limitation of the client library used in the frozen WellPulse comparison:

- with `clean_session=False`, the client's session is stored **in memory** rather than durably persisted by the library;
- restarting/recreating the client process loses that in-memory client session;
- QoS1/QoS2 outbound messages not fully acknowledged may therefore be lost across a client restart.

The same documentation notes that acknowledgement tracking (`on_publish()` / `wait_for_publish()`) can mitigate specific unacknowledged-publish risk, but it does not turn the Paho client into an application-level durable record store across process restart.

**Design implication:** `S3_OUTAGE_RESTART` is not an artificial trick. It is the cleanest scenario for testing a documented semantic boundary between standard volatile MQTT client state and WellPulse's application-level disk durability + deterministic reconciliation.

**Fairness rule retained:** B1 and W1 must continue using the same low-level Paho configuration. WellPulse must not gain an advantage from different QoS, reconnect delays, keepalive, broker, topic schema, TLS setting, inflight limit, or network path.

## 5. Reviewer attack surface after this survey

### Attack A — "This is just store-and-forward."

**Risk: severe.** Domingues 2024, the 2026 5G NTN work, CAMS F Edge DTN, Dtnmqtt and older DTN-MQTT work make generic buffering/store-and-forward impossible to claim as novel.

**Defense:** lead with causal decomposition and evidence package: strong matched MQTT comparator, process-restart durability, record-level integrity/idempotence, controlled physical RF, separate FIT/RF/OTA layers, run-level inference.

### Attack B — "The baseline is a strawman."

**Risk: severe if B0 is used as primary comparator.**

**Defense:** the POWDER primary comparator remains `B1_MQTT_QOS1`, not FIT's legacy B0. Same Paho transport and QoS1/reconnect parameters are mandatory.

### Attack C — "You only simulated a network outage."

**Risk: severe.** Many competitors already evaluate software/network disconnections.

**Defense:** POWDER must produce a measured controlled physical-RF trace. Q0-Q3 need programmed RF settings plus observable radio/link context. If the impairment cannot be shown to be physical and causally linked to the data-path effect, redirect the paper rather than overclaim.

### Attack D — "MQTT already handles reconnect and QoS."

**Risk: expected.**

**Defense:** explicitly distinguish network reconnect from client-process durability. Paho's own documentation states the in-memory client session is lost on process restart. B1 is therefore allowed to be strong under network-only outages; the point is to measure whether application durability adds value, especially under S3.

### Attack E — "Agricultural monitoring with MQTT is old."

**Risk: certain.** Bauer 2017 and current 2026 agriculture systems establish this clearly.

**Defense:** agriculture/solar pumping is motivation and future field translation only. Do not use it as the paper novelty claim and do not extrapolate POWDER/FIT results to Siwa/pump/agronomic behavior.

### Attack F — "The result is a demo, not a scientific experiment."

**Defense:** preserve run as statistical unit; paired randomized B1/W1 blocks; pre-frozen precision rule; invalid-run criteria; deterministic primary endpoint; complete run manifests; no p-value-dependent stopping; separate validity layers.

## 6. Design implications before G4

### 6.1 Keep unchanged

- `B1_MQTT_QOS1` as primary comparator.
- Same Paho low-level session for B1/W1.
- `S0/S1/S2/S3` scenario family.
- Explicit S3 gateway-process restart.
- 1 record/s primary workload unless calibration exposes a technical flaw.
- Run-level statistical unit and paired randomization.
- Precision-based 3-to-5 paired-block rule for impairment scenarios.
- Conducted RF before OTA.
- OTA as compact external replication, not a second full campaign.
- Strong non-claim boundary around pump/hydraulic/groundwater/agronomy/rural generalization.

### 6.2 Reinforce during G5/WP2

The survey increases the importance of recording:

1. **Backlog-drain/recovery time and throughput**, because prior MQTT retransmission work explicitly optimizes these.
2. **CPU, RSS/memory, durable-queue/disk bytes and network overhead**, because "reliability at what cost?" is an obvious reviewer question and current literature explicitly frames reliability/performance tradeoffs.
3. **Simultaneous new telemetry during recovery**, to avoid an unrealistically protected recovery phase. Do not serialize record generation behind `wait_for_publish()`.
4. **Physical RF causality evidence:** attenuation/path setting, attach state and available radio metrics such as RSRP/RSRQ/SINR/BLER/throughput, synchronized with application events.
5. **Process identity/restart timestamp** in S3, so the paper can distinguish reconnection from actual client-state destruction.
6. **Record checksum/idempotence evidence**, so "eventual delivery" is not confused with integrity-preserving reconciliation.

These are already compatible with protocol v0.4; they do not require a pre-G4 amendment.

## 7. Novelty statement after adversarial review

### Unsafe statement

> WellPulse is novel because it buffers MQTT data offline and retransmits after connectivity returns.

**REJECT.** Prior work directly establishes this class of mechanism.

### Defensible working statement

> WellPulse is evaluated as a lightweight durable telemetry architecture whose application-level record persistence and idempotent reconciliation are isolated from standard MQTT QoS1/reconnect behavior through a matched comparator and a separated network-versus-process-restart failure model. Its contribution is assessed through a reproducible validation ladder spanning real embedded hardware, controlled physical-RF impairment, and compact OTA replication, with run-level causal evidence rather than message-level pseudoreplication.

This is a **compound contribution claim**. It remains subject to final full-text comparison and the actual POWDER results.

## 8. Priority unresolved literature item

### The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications — 2026

Confirmed metadata:

- Luís Gaspar, José N. C. Faria, Marco Domingues, Fernanda Famá, Lúcia Martins, David Portugal.
- IEEE Internet of Things Magazine, 2026.
- DOI `10.1109/MIOT.2026.3681190`.

The title and author lineage make this a **high-priority direct competitor**, but the publisher/author pages available in this review did not expose sufficient abstract/full-text content to classify its experiment without speculation.

**Rule:** obtain/read full text before final manuscript novelty freeze. Until then, do not attribute methods, baselines, failure modes or results to this paper beyond confirmed metadata.

This unresolved item does **not** justify delaying G4: the existing protocol has already adopted the conservative strong-baseline, physical-RF, process-restart and reproducibility controls that a close MQTT reliability competitor would most likely force us to defend.

## 9. Reference set reviewed

1. Asgari Araghi, M.; Khendek, F. Discover Internet of Things 6, 61 (2026). DOI `10.1007/s43926-026-00322-w`.
2. Jesus, B.; Lins, F.; Laranjeiro, N. Internet of Things 31, 101590 (2025). DOI `10.1016/j.iot.2025.101590`.
3. Colarusso, C.; Falco, I.; Zimeo, E. Internet of Things 33, 101723 (2025). DOI `10.1016/j.iot.2025.101723`.
4. Domingues, M.; Faria, J.N.; Portugal, D. EURASIP JWCN 2024, 2. DOI `10.1186/s13638-023-02327-3`.
5. Gaspar, L.M.; Faria, J.N.C.; Domingues, M.; Famá, F.; Martins, L.; Portugal, D. IEEE Internet of Things Magazine (2026). DOI `10.1109/MIOT.2026.3681190`.
6. Baumgärtner, L. FICC 2024 / LNNS 921, 524-543. DOI `10.1007/978-3-031-54053-0_36`.
7. Bauer, J.; Aschenbruck, N. IEEE LCN 2017, 294-302. DOI `10.1109/LCN.2017.81`.
8. Herrera, N.I. et al. Future Internet 18(4), 180 (2026). DOI `10.3390/fi18040180`.
9. Monzon Baeza, V. et al. Sensors 26(15), 4919 (2026). DOI `10.3390/s26154919`.
10. Bozorgi, M.; Assaf, G.J.; Katsanis, C.J. Internet of Things 37, 101900 (2026). DOI `10.1016/j.iot.2026.101900`.
11. Matias, J.A.; Macêdo, R.J.A. Workshop de Testes e Tolerância a Falhas (2026). DOI `10.5753/wtf.2026.24074`.
12. Chang, H.-L. et al. Sensors 16(10), 1560 (2016). DOI `10.3390/s16101560`.
13. *Stress-Testing MQTT Brokers: A Comparative Analysis of Performance Measurements*. Energies 14(18), 5817 (2021). DOI `10.3390/en14185817`.
14. Papadopoulos, G.Z. et al. Computer Networks 119, 86-101 (2017). DOI `10.1016/j.comnet.2017.03.012`.
15. Breen, J. et al. WiNTECH 2020. DOI `10.1145/3411276.3412204`.
16. Mimouni, A. et al. Scientific African, e03533 (2026). DOI `10.1016/j.sciaf.2026.e03533`.
17. Bicamumakuba, E. et al. Sensors 26(5), 1548 (2026). DOI `10.3390/s26051548`.
18. Zhang, T. et al. *A Survey on Industrial Internet of Things (IIoT) Testbeds for Connectivity Research*, arXiv:2404.17485 (2024).
19. Eclipse Paho MQTT Python project documentation, known limitations for MQTT v3 persistent sessions/client restart, accessed 2026-08-25.

## 10. Gate conclusion

**WP0 related-work benchmark: PASS WITH ONE MANDATORY MANUSCRIPT-STAGE FULL-TEXT CHECK.**

- Current C1-C5 novelty lock is **reaffirmed but narrowed**.
- No claim is made that any individual WellPulse mechanism is unprecedented.
- No change to scientific completion: **20%**.
- No scored run authorization: `scored_runs_authorized=false`.
- G4 remains infrastructure qualification only.
- The experiment should proceed only if G4/G5 can demonstrate a real experimental user-plane and controlled physical-RF causality.
- `The Price of Reliability` must be fully read before final manuscript novelty freeze.
