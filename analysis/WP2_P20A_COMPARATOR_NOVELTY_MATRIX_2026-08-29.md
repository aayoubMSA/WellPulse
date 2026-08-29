# WP2-P20A — Submission-Date Comparator / Novelty Matrix

Date: 2026-08-29  
Status: **COMPLETE / VENUE-NEUTRAL / CLAIM-BOUNDED**

## 1. Purpose

This matrix closes the pre-submission literature/novelty gate without changing experiments, measured values, P13 claims, P17/P17V conclusions, P18RC figures, P19 artifact semantics, or historical P7B state.

The governing rule is conservative: prior work may narrow novelty wording, but it does not create a scientific blocker unless it invalidates a currently supported empirical or methodological claim.

Allowed collision classes:

- `NO IMPACT` — relevant prior work, but no material collision with the bounded WellPulse contribution.
- `WORDING NARROWING` — prior work establishes a mechanism/concept that WellPulse must not imply is new or historically unique.
- `SCIENTIFIC BLOCKER` — prior work invalidates the current claim/contribution to a degree that cannot be repaired editorially inside the frozen evidence envelope.

## 2. Current search axes

Submission-date searching on 2026-08-29 covered:

1. MQTT persistence, sessions, QoS state and retransmission;
2. MQTT/IoT robustness, stress testing and fault injection;
3. offline-first, edge/cloud continuity and store-and-forward;
4. end-to-end acknowledgment / receiver confirmation and durable application persistence;
5. failure-domain-aware resilience/recovery evaluation;
6. real wireless/IoT testbeds, repeatability and reproducibility;
7. receiver-side identity reconciliation/provenance where materially related.

## 3. Comparator / novelty matrix

| Prior-art axis / source | What prior work establishes | Relation to WellPulse | Collision class | Mandatory consequence |
|---|---|---|---|---|
| **Eclipse Paho Java persistence** — `MqttDefaultFilePersistence`, `MqttClient`, `MqttAsyncClient`; current project/documentation | File-backed persistence can retain in-flight QoS state across network/client/device interruption; memory-only state may be lost. | Directly constrains interpretation of B0. | **WORDING NARROWING** | B0 must always be called a **non-durable publish-only baseline**. Never claim generic MQTT superiority or strongest-durable-client superiority. |
| **AWS IoT Core persistent sessions** — current technical documentation | Brokers can preserve subscriptions and qualifying queued/unacknowledged messages for persistent sessions and deliver them after reconnect, subject to limits/expiry. | Reinforces that broker/session persistence is established operational practice. | **WORDING NARROWING** | Do not imply that persistence across intermittent connectivity is novel to WellPulse. Distinguish application-record durability from MQTT session/broker semantics. |
| **Domingues, Faria & Portugal 2024**, DOI `10.1186/s13638-023-02327-3` | Local accumulation and retransmission of MQTT data after network disconnection, with retransmission/payload trade-offs. | Store/retransmit mechanism is prior art. | **WORDING NARROWING** | No novelty claim for buffering/retransmission after disconnection. |
| **Colarusso, Falco & Zimeo 2025**, DOI `10.1016/j.iot.2025.101723` | Edge–Cloud business continuity under transient network failures through replicated application components/data and reconciliation. | Offline continuity/reconciliation already established. | **WORDING NARROWING** | Do not claim offline-first continuity or reconciliation generically as new. |
| **Herrera et al. 2026**, DOI `10.3390/fi18040180` | Context-aware offline-first synchronization and local reasoning using CRDTs and MQTT-SN. | Strong prior art for offline-first + reconciliation. | **WORDING NARROWING** | WellPulse contribution must remain evaluation/evidence-focused, not generic offline-first novelty. |
| **Monzon Baeza et al. 2026**, DOI `10.3390/s26154919` | Distributed 5G Core with store-and-forward preserves and later delivers IoT sensing data across intermittent LEO backhaul. | Store-and-forward under disconnected operation is established experimentally at another layer. | **WORDING NARROWING** | No standalone S&F novelty claim. Keep layer/failure-domain differences explicit. |
| **Mohammed, Singh, Aslam & Wong 2026**, DOI `10.48084/etasr.16945` | Disk-backed edge persistence plus an application-level acknowledgment issued after fog/database insertion; complete recovery during tested network disruption; explicitly decouples sensing reliability from network availability. | **Closest newly identified conceptual comparator.** It overlaps application-level durable record lifecycle, end-to-end acknowledgment and the idea that sensing/data reliability can be decoupled from network availability. | **WORDING NARROWING — MATERIAL** | Add to final related work. Do **not** claim novelty for durable application persistence, end-to-end database acknowledgment, complete outage recovery as a generic idea, or historical priority for decoupling data reliability from network availability. Preserve novelty only in the bounded WellPulse evaluation structure/evidence package. |
| **Im & Lim 2023 E-MQTT**, DOI `10.3390/app132212419` | Extends MQTT to provide subscriber-side end-to-end reception confirmation through synchronous/asynchronous response mechanisms. | End-to-end receiver confirmation is prior art, although protocol-level design differs from WellPulse's identity reconciliation. | **WORDING NARROWING** | IC-09 remains a demonstrated methodological practice, not a claim that receiver confirmation/reconciliation is historically unique. Consider adding E-MQTT to final related work. |
| **Jesus, Lins & Laranjeiro 2025**, DOI `10.1016/j.iot.2025.101590` | Dedicated MQTT robustness assessment through message-level fault injection in real case studies. | Establishes fault-oriented MQTT evaluation; fault model differs from WellPulse domain manipulations. | **NO IMPACT** | Preserve explicit distinction: malformed/perturbed-message robustness testing vs delivery availability/process/RF/UE/CORE/broker failure domains. |
| **Asgari Araghi & Khendek 2026**, DOI `10.1007/s43926-026-00322-w` | Systematic review of IoT application-layer protocol testing; MQTT heavily studied; robustness/resilience/reliability testing and nondeterminism are active issues. | Broad field context; no collision with bounded WellPulse empirical claims. | **NO IMPACT** | Use as field-level testing anchor; avoid claiming failure testing itself is novel. |
| **Gaspar et al. 2026**, DOI `10.1109/MIOT.2026.3681190` | Bibliographic identity and title `The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications` verified from ISR/CTTC/author publication records. A current author publication page advertises a PDF link, but the linked full text could not be recovered through the available retrieval channel during P20A. | Detailed method/result overlap cannot be responsibly inferred without the article text. | **WORDING NARROWING — CONSERVATIVE** | Keep Gaspar at **bibliographic/scope level only**. Attribute no specific method, fault model, result, comparator or quantitative finding unless full text is later directly recovered. No present blocker is inferred from inaccessible detail. |
| **Radwan, Sheldon & Wang 2026**, DOI `10.1038/s41598-026-66865-8`, published 17 Aug 2026 | Backpressure-driven adaptive publishing for MQTT under varying traffic loads/network conditions, targeting broker congestion, latency and message loss. | New submission-date MQTT reliability work; primarily load/flow-control rather than durable record survival + failure-domain separation. | **NO IMPACT** | Add/consider in current related-work update to show awareness of very recent load-stability work; distinguish congestion/flow-control from failure-domain record-survival evaluation. |
| **Azure IoT Operations disk persistence/data-flow semantics** — current technical documentation | Source message acknowledgment can be deferred until destination delivery; disk persistence can preserve queued data/processing state across outages/restarts. | Strong industry evidence that destination-aware acknowledgment plus disk persistence is established engineering practice. | **WORDING NARROWING** | Reinforces prohibition on claiming mechanism novelty for ack-after-destination + disk persistence. Technical comparator; scholarly citation optional depending on venue. |
| **Adjih et al. 2015 FIT IoT-LAB**, DOI `10.1109/WF-IOT.2015.7389098` | Large-scale open real IoT testbed. | Platform authority, not novelty collision. | **NO IMPACT** | Cite/acknowledge FIT as required; do not imply the facility itself is a WellPulse contribution. |
| **Papadopoulos et al. 2017**, DOI `10.1016/j.comnet.2017.03.012` | Characterized real IoT testbeds support repeatable/reproducible experimentation and turn environmental variation/failures into explicit experimental parameters. | Repeatability/testbed methodology is prior art. | **WORDING NARROWING** | Do not claim use of controlled real testbeds or repeatability methodology as historically novel. |
| **Breen et al. 2021 POWDER**, DOI `10.1016/j.comnet.2021.108281` | POWDER provides controllable, visible, end-to-end wireless experimentation across radio-to-application layers. | Platform authority enabling the POWDER characterization. | **NO IMPACT** | Cite/acknowledge POWDER; describe WellPulse's specific experiment, not the platform capability as a contribution. |
| **NIST Hany et al. 2026**, DOI `10.1109/OJIM.2026.3679169` | Standardized, repeatable physical wireless-IoT assessment in characterized mmWave industrial work-cell channels with uncertainty propagation. | Recent evidence that controlled/repeatable physical wireless evaluation is an active established methodology. | **NO IMPACT** | Optional related-work context; no priority claim for controlled physical characterization. |

## 4. Novelty boundary after current literature closure

### Explicitly **not novel**

The final manuscript must not imply novelty for any of the following:

- MQTT persistent sessions or durable client persistence;
- local disk-backed queues/caching;
- retransmission after connectivity returns;
- generic store-and-forward;
- offline-first execution or generic reconciliation;
- application-level acknowledgment after downstream receipt/database insertion;
- generic end-to-end subscriber confirmation;
- generic MQTT robustness/fault testing;
- use of real testbeds or repeatable wireless experimentation;
- the historical idea that data/application state can be decoupled from network availability.

### Defensible bounded WellPulse contribution

The final related-work/novelty wording may defend the **compound evaluation contribution**, not historical uniqueness of its ingredients:

1. an explicit evaluation separation between **application record-state survival** and **communication-path recovery**;
2. a bounded real-embedded FIT architecture experiment quantifying receiver-reconciled record survival under exact outage and gateway-process-restart semantics relative to a **non-durable B0 baseline**;
3. a separate controlled POWDER physical-path/failure-domain characterization with mechanism-specific exact/censored/upper-bound recovery endpoints;
4. integration through receiver-side identity reconciliation, anomaly/negative-evidence preservation and claim-to-evidence traceability **without statistically pooling the two infrastructures**.

The paper must present this as **the evaluation framework used in this study**, not as a certified first-ever two-property model.

## 5. Exact wording constraints for P20D

### Prohibited novelty wording

Do not use or imply:

- `WellPulse introduces durable MQTT telemetry.`
- `WellPulse is the first system to preserve IoT data during disconnection.`
- `WellPulse is the first to decouple sensing/data reliability from network availability.`
- `WellPulse introduces end-to-end acknowledgment/reconciliation for MQTT.`
- `WellPulse is the first failure-domain-aware MQTT resilience framework.`
- `WellPulse achieves reliability that standard MQTT cannot provide.`
- any generic priority claim for persistence, store-and-forward, offline-first, end-to-end confirmation, testbed repeatability, or recovery testing.

### Preferred contribution wording

A defensible compact form is:

> This study uses a failure-domain-aware evaluation framework to measure application record-state survival separately from communication-path recovery. It combines a receiver-reconciled embedded durability experiment with a separately executed controlled-RF/path characterization, preserving mechanism-specific recovery semantics and integrating the evidence without a pooled reliability metric.

For FIT:

> Under the tested FIT outage conditions, W1 produced a repeated +20 percentage-point final-completeness difference relative to the **non-durable B0 baseline**; this is a bounded record-survival result and not a generic MQTT superiority claim.

For methodological contribution:

> Receiver-side identity reconciliation and explicit preservation of adverse/censored/anomalous evidence are used here as evidence practices supporting defensible resilience reporting; historical uniqueness is not claimed.

## 6. Final collision count

Material collision review result:

- `SCIENTIFIC BLOCKER`: **0**
- `WORDING NARROWING`: **11 source/axis groups** (including the material Mohammed et al. 2026 comparator and conservative Gaspar handling)
- `NO IMPACT`: **6 source/axis groups**

No collision requires a new experiment or a new empirical claim for the current bounded manuscript.

`P20A_COMPARATOR_MATRIX=COMPLETE`

`P20A_SCIENTIFIC_BLOCKERS=0`

`P20A_NEW_EXPERIMENT_REQUIRED=NO`

`P20A_NEW_EMPIRICAL_CLAIM_REQUIRED=NO`

`SUBMISSION_AUTHORIZED=NO`
