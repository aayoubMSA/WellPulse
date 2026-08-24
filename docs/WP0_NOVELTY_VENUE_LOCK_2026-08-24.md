# WP0 — Novelty & Venue Lock — 2026-08-24

**Status:** DESIGN LOCK FOR THE POWDER CAMPAIGN, WITH PRE-SCORE COMPARATOR REVIEW OPENED 2026-08-25. This is not a submission decision and does not claim a current quartile without re-verification at submission.

## Publication objective

Produce one strong full research paper in which WellPulse is evaluated as a lightweight, durable, offline-first IIoT edge-gateway architecture under real embedded and real-radio impairments, with a complete reproducibility artifact.

The paper must not rely on "store-and-forward exists" as the novelty claim. Store-and-forward, offline-first operation, MQTT robustness evaluation, and edge/cloud continuity are already represented in recent literature.

## Targeted 2023–2026 literature audit

| Work | What it establishes | Implication for WellPulse |
|---|---|---|
| *An approach to assess robustness of MQTT-based IoT systems*, Internet of Things 31 (2025), 101590 | MQTT robustness deserves explicit practical evaluation under stressful conditions | Robustness evaluation itself is relevant, but must be more than a functional demo |
| *Business continuity of Cloud-based IoT applications through a seamless continuum*, Internet of Things 33 (2025), 101723 | Edge/cloud continuity and reconciliation during transient network failures are active research topics | Edge continuity alone is not novel; our differentiation must be empirical rigor + lightweight durable record semantics + real RF |
| *Dimensioning payload size for fast retransmission of MQTT packets in the wake of network disconnections*, EURASIP JWCN (2024) | MQTT recovery after disconnection is already studied quantitatively | Avoid claiming generic MQTT reconnection as novelty |
| *Experimental Validation of a Distributed 5G Core with Store-and-Forward for IoT Sensing over LEO Non-Terrestrial Networks*, Sensors 26(15) (2026) | 5G/IoT store-and-forward can achieve lossless recovery in disconnected operation | Store-and-forward itself cannot carry the novelty claim |
| *CAMS F Edge DTN: Context-Aware Offline-First Synchronization and Local Reasoning Using CRDTs and MQTT-SN*, Future Internet 18(4) (2026) | Offline-first synchronization and eventual convergence are active design patterns | Position WellPulse as a narrower industrial telemetry architecture with durable identity/idempotent reconciliation and physical testbed evidence |
| *Group-based link modeling for wireless digital twins: Towards accurate network performance prediction* (2026) and earlier FIT IoT-LAB testbed-characterization literature | Repeated testbed experiments and link characterization are important for repeatability/reproducibility | RF characterization and run-level reproducibility must be first-class evidence, not ancillary logging |
| *Powder: Platform for Open Wireless Data-driven Experimental Research* (Computer Networks, 2021) | POWDER is explicitly designed as a controllable, reproducible real-wireless research platform | Use POWDER as a scientific instrument: controlled real RF first, OTA as external replication |

## Locked novelty position

The contribution is **not** "we invented buffering" or "we used MQTT over 5G".

The defensible contribution package is:

1. **C1 — Lightweight durable telemetry semantics.** A record-identity preserving edge path with durable local queueing, checksums, explicit pending/sent state, and an idempotent sink/reconciliation path suitable for read-only industrial telemetry.
2. **C2 — Matched primary baseline plus durable-client sensitivity requirement.** The primary causal comparison remains standard MQTT QoS 1 with automatic reconnect using the same low-level Paho Python transport as WellPulse, but without application-level disk durability/reconciliation. A deeper 2026-08-25 audit established that other standard Eclipse Paho clients provide file-backed persistence and persistent disconnected buffering, so B1 must not be described as the strongest durability configuration available in the MQTT ecosystem. A targeted durable-client comparator/sensitivity check must be resolved before scored execution.
3. **C3 — Cross-layer validation ladder.** Real embedded hardware (FIT IoT-LAB) -> controlled physical RF impairment (POWDER attenuator matrix) -> compact over-the-air replication. Each layer answers a different validity question; evidence is not pooled as if it came from one population.
4. **C4 — Failure-model separation.** Distinguish network-only impairment from compound network + gateway-process restart so the value of volatile transport state versus application-level durable record semantics is measured rather than assumed.
5. **C5 — Publication-grade reproducibility.** Run-level manifests, frozen randomization, radio state, raw telemetry, packet/RAN logs where available, system overhead, checksums, and one-command reconstruction of paper tables/figures.

## Primary research questions

- **RQ1 — Network resilience:** Under controlled real RF intermittency and hard outage, how do a matched MQTT QoS 1 + reconnect baseline and WellPulse differ in unique telemetry completeness, recovery behavior, integrity, and overhead?
- **RQ2 — Durable recovery:** When a gateway process restarts during a real RF outage, what additional record-level integrity/reconciliation value does WellPulse provide relative to volatile matched MQTT behavior, and does that value remain meaningful against a standard client configured with durable MQTT persistence?
- **RQ3 — Transportability:** Are the observed effects consistent across the existing real embedded FIT evidence, POWDER conducted RF, and a compact POWDER OTA replication without claiming field/agricultural validation?

## Venue-fit lock

### Primary target: **Internet of Things (Elsevier)**

Rationale:
- direct scope fit for IoT reliability, edge/cloud engineering, platforms, and high-quality full research papers;
- recent publication of MQTT robustness and edge/cloud continuity work shows topical fit;
- WellPulse is fundamentally an IoT/edge systems paper, not a new physical-layer technique.

### Backup A: **Computer Networks (Elsevier)**

Use if the final manuscript emphasizes network reliability, controlled RF measurement, performance evaluation, and experimental methodology strongly enough. The journal explicitly covers network reliability/performance and supports dataset/open-source-software article pathways, which is useful for the artifact trajectory.

### Backup B: **Computer Communications (Elsevier)**

Use if the final emphasis is IoT + edge/cloud + experimental testbeds/research platforms and the primary venue fit weakens.

**Quartile rule:** Q1 status, indexing, APC/open-access route, and current author guidance must be re-verified immediately before submission. No static quartile claim is frozen here.

## Paper-story lock

Provisional story:

> WellPulse is a lightweight offline-first IIoT telemetry gateway whose value is tested not by simulation alone but through a validation ladder spanning real embedded hardware, controlled physical RF impairment, and over-the-air replication. The study isolates application-level record durability and idempotent reconciliation from matched MQTT transport behavior, and stress-tests the interpretation against a durable standard MQTT-client comparator while preserving complete run-level provenance.

Possible working title:

> **WellPulse: Reproducible Cross-Testbed Validation of Durable Offline-First IIoT Telemetry under Real Wireless Disruption**

## Explicit non-claims

The POWDER/FIT campaign does not validate:
- pump mechanics or hydraulic behavior;
- groundwater or Siwa propagation/environment;
- crop/agronomic outcomes;
- field deployment reliability;
- rural generalization unless a later outdoor experiment is explicitly added;
- novelty of MQTT, generic store-and-forward, 5G, buffering, client-side persistence, or offline buffering as standalone mechanisms.

## Kill/redirect criteria

Before manuscript submission, redirect the paper if any of the following holds:
- a strong durable standard MQTT comparator eliminates any meaningful WellPulse distinction in integrity/recovery/overhead;
- POWDER cannot produce a controlled physical-RF impairment trace distinguishable from software-only impairment;
- OTA replication cannot be obtained and the final story overstates generalization;
- the final contribution reduces to an implementation demo without a publishable empirical question.

Negative or null results do **not** by themselves trigger a kill; a rigorously bounded negative result may still be publishable if the cross-testbed evidence is informative.

## 2026-08-25 pre-G4 benchmark status

A broader manuscript-grade rapid structured benchmark is preserved in:

`docs/WP0_RELATED_WORK_BENCHMARK_2026-08-25.md`

The expanded benchmark covered current MQTT robustness/retransmission work, DTN/offline-first systems, edge/cloud reconciliation, cellular smart-farming, 5G store-and-forward, IIoT store-and-forward, reproducible FIT/POWDER testbed methodology, agricultural MQTT deployments, and official MQTT-client implementation semantics.

A subsequent deeper comparator audit is preserved in:

`docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`

### Material finding

The official Eclipse Paho Python documentation confirms that the current B1 implementation does not persist its MQTT client session across a process restart. However, official Eclipse Paho Java documentation provides file-backed client persistence, and its disconnected-buffer API supports a persist option; source-level inspection shows buffered outgoing messages can be written to the persistence layer.

Therefore:

- the C1-C5 contribution package remains viable, but its interpretation is narrower;
- B1 remains useful as the **matched same-implementation causal comparator**;
- B1 is no longer described as the strongest durable MQTT client configuration available generally;
- a candidate `B2_MQTT_DURABLE_CLIENT` sensitivity comparator must be qualified locally and resolved before the scored scientific matrix is authorized;
- G4 controlled-RF infrastructure qualification is unaffected and should proceed as scheduled;
- `scored_runs_authorized=false` remains mandatory.

The preferred provisional route is to retain B1 for the full matched primary comparison and add only a compact B2 sensitivity experiment in the failure scenarios where durable client persistence matters most, if a non-scored local semantics gate confirms B2's behavior. Exact B2 implementation, replication, and analysis remain **unfrozen** until that gate is completed.

One additional mandatory manuscript-stage literature check remains: obtain and fully compare Gaspar et al., *The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications*, IEEE Internet of Things Magazine (2026), DOI `10.1109/MIOT.2026.3681190`. Its bibliographic metadata is confirmed, but its methods/results were not sufficiently exposed by the sources available during this review and therefore were not inferred.
