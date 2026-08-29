# WP2-P17 — Consortium Manuscript Review

Date: 2026-08-29  
Status: **CONSORTIUM REVIEW COMPLETE / MAJOR REVISION RECOMMENDED / NO NEW EXPERIMENT REQUIRED**

## 1. Mandate

Review the full WellPulse paper against the complete scientific record rather than the P15 draft alone. The consortium was instructed to maximize defensible scientific value from the existing evidence while preserving P13 claim boundaries and P16 prohibitions.

Primary review inputs:

1. P10 scientific analysis contract;
2. P11 raw-data analysis;
3. P12 cross-evidence integration;
4. P13 claim–evidence matrix;
5. P14 publication displays;
6. P15 manuscript;
7. P16 adversarial publication QA and frozen editorial patches;
8. P9 POWDER validity/anomaly/trace records;
9. Experimental Technical Dossier v2.2 and experiment figure suite;
10. refreshed 2024–2026 MQTT/offline-first/testbed literature.

## 2. Consortium composition

This is a role-based scientific review consortium; no fictitious individual identities are asserted.

### C1 — Systems / IoT scientific editor
Mandate: paper thesis, contribution hierarchy, title/abstract/RQ coherence, systems-paper structure.

### C2 — MQTT protocol and persistence specialist
Mandate: QoS/persistence semantics, baseline fairness, durable-client comparator risk, application durability boundary.

### C3 — Wireless/RF and experimental-testbed specialist
Mandate: POWDER attenuation semantics, transition/recovery interpretation, cross-layer validity, testbed reproducibility.

### C4 — Experimental design / statistics reviewer
Mandate: unit of analysis, replication, deterministic outcomes, censoring, upper bounds, pseudoreplication and inference language.

### C5 — Reproducibility / artifact reviewer
Mandate: receiver-side reconciliation, anomaly preservation, hash/provenance chains, sanitized artifact design.

### C6 — Literature / novelty reviewer
Mandate: closest prior art, novelty boundary, missing citations, current-state literature survey.

### C7 — Scientific visualization / information-design reviewer
Mandate: main-text versus supplementary displays, architecture figure, failure-domain taxonomy, figure density.

### C8 — Adversarial journal reviewer / associate-editor simulation
Mandate: rejection risks, perceived triviality, stitched-testbed risk, scope inflation, whether evidence supports the manuscript pitch.

## 3. Independent reviewer findings

### C1 — Systems / IoT scientific editor

**Verdict: MAJOR REVISION, strong publishable core.**

The manuscript already contains the correct scientific idea but does not foreground it strongly enough. The strongest thesis is not “a durable queue improves MQTT reliability.” It is:

> Resilient telemetry must be evaluated separately for record-state survival and communication-path recovery because the two properties fail and recover in different domains.

The paper should be reorganized around that thesis. W1 becomes the concrete architecture/case study used to evaluate record-state survival; POWDER becomes the controlled communication-path characterization. The two testbeds then become complementary by design rather than appearing stitched together.

Recommendation:
- keep the claim envelope;
- reduce RQ4 from a separate empirical RQ to an integration/synthesis section;
- use three primary RQs and make cross-evidence triangulation the paper-level conclusion.

### C2 — MQTT protocol / persistence specialist

**Verdict: baseline transparency is mandatory; architecture novelty must not be oversold.**

The strongest residual attack remains that B0 is deliberately non-durable. Eclipse Paho documentation explicitly provides file-based persistence for reliable QoS delivery across client/device restart, which confirms that durable MQTT clients are a real comparator class, not a hypothetical future alternative.

Therefore:
- never write “W1 beats MQTT”;
- never present the +20 pp result as a generic protocol improvement;
- explicitly state that W1 demonstrates the effect of durable application record state relative to a non-durable publish-only baseline;
- strengthen W1 implementation detail: stable identity, canonical serialization, SHA-256, SQLite WAL, `synchronous=FULL`, `PENDING/SENT`, idempotent duplicate enqueue, collision failure.

The exact match between the 2,000-record outage window and B0's 2,000 permanent missing records should be treated as an experimentally verified causal consequence of the non-durable design, not as an unexpected stochastic discovery.

### C3 — Wireless/RF / testbed specialist

**Verdict: POWDER is valuable if framed as controlled characterization, not confirmatory architecture evidence.**

The strongest POWDER results are:
- transition-region behavior across E1R4/E2/E3;
- cross-layer mismatch at 51 dB;
- broker-only fault isolation in E8;
- non-deterministic RF-only recovery evidenced by E4 versus E10-A;
- mechanism-specific recovery clocks in E10;
- preservation of caveats and failed/setup attempts.

Recommendations:
- use “programmed attenuation” consistently;
- avoid universal link-budget language;
- prefer “direction dependence / descending recovery” to strong hysteresis language unless the operational definition is stated;
- elevate E8 and E10-A because they provide clean scientific separation of failure domains;
- leave E11 detailed replications to supplementary material because the collector is UE-side only.

### C4 — Experimental design / statistics reviewer

**Verdict: inference discipline is already strong; keep it conservative.**

Required rules:
- FIT run/replicate remains the scientific unit;
- 10,000 records per run are not independent n;
- no population reliability probability from three runs;
- no fabricated CI around identical +20 pp outcomes;
- E3 cycles are repeated characterization within the observed transition regime, not population failure probabilities;
- E10-A remains censored;
- E10-D remains an upper bound;
- FIT backlog-drain time and POWDER recovery clocks are different constructs.

The consortium recommends emphasizing absolute engineering effects and exact run-level values rather than p-values.

### C5 — Reproducibility / artifact reviewer

**Verdict: this is an unusually strong part of the project and should be exploited more explicitly.**

The manuscript currently states evidence-first reconciliation but underuses its most convincing examples:
- E1R4 sequence 96 appears sent without a sender failure flag but is absent at the receiver;
- E3 sequence 150 shows the same type of disagreement;
- E8 has 80 sender-log lines but only 60 unique IDs because recovery IDs 41–60 were sent twice;
- receiver-side unique IDs prevent false completeness inflation;
- setup artifacts, missing frozen evidence, censoring, outliers, and post-manifest append anomalies remain visible.

Recommendation: include one concise concrete example in the main Discussion and move the complete anomaly/validity register to a reviewer-facing supplement.

Public artifact package should contain only sanitized/releasable analysis code, derived data, manifests and figures. Private credential-bearing preservation bundles must remain private.

### C6 — Literature / novelty reviewer

**Verdict: current related work is directionally correct but too thin for a full journal paper.**

The paper needs a structured survey rather than eight isolated citations. Recommended four literature axes:

1. MQTT persistence / QoS / retransmission.
2. Robustness and fault injection in MQTT/IoT systems.
3. Offline-first, edge–cloud continuity and store-and-forward.
4. Testbed repeatability, controlled wireless experimentation and reproducibility.

High-priority verified anchors:
- Asgari Araghi & Khendek 2026 systematic review;
- Jesus et al. 2025 MQTT robustness, DOI `10.1016/j.iot.2025.101590`;
- Domingues et al. 2024 retransmission, DOI `10.1186/s13638-023-02327-3`;
- Gaspar et al. 2026 MQTT stress-testing, DOI `10.1109/MIOT.2026.3681190`;
- Colarusso et al. 2025 Edge–Cloud continuity, DOI `10.1016/j.iot.2025.101723`;
- Herrera et al. 2026 offline-first CRDT/MQTT-SN, DOI `10.3390/fi18040180`;
- Monzon Baeza et al. 2026 5G store-and-forward, DOI `10.3390/s26154919`;
- Adjih et al. 2015 FIT IoT-LAB, DOI `10.1109/WF-IOT.2015.7389098`;
- Papadopoulos et al. 2017 repeatable IoT testbed methodology, DOI `10.1016/j.comnet.2017.03.012`;
- Breen et al. 2021 POWDER, DOI `10.1016/j.comnet.2021.108281`.

Gaspar full-text comparison remains a mandatory submission-date gate if accessible.

### C7 — Visualization / information design reviewer

**Verdict: results figures are strong, but the main paper lacks a visual explanation of the architecture and why the two testbeds belong in one paper.**

Recommended new main Figure 1:
- left panel: W1 record lifecycle (`generate → stable identity/hash → durable PENDING state → MQTT attempt → SENT → receiver reconciliation`);
- right panel: evidence-role separation (`FIT = architecture record survival`, `POWDER = communication-path degradation/recovery`).

Recommended main display set if P14 is explicitly reopened:
1. architecture + evidence-role schematic;
2. FIT completeness;
3. POWDER transition/direction;
4. POWDER E3 repeatability.

Move standalone FIT backlog-drain plot to supplement and retain its values in the main table/text.

Add one compact main table mapping failure domain → manipulated component → experiment → endpoint → admissible interpretation.

### C8 — Adversarial journal reviewer

**Likely rejection arguments if submitted as P15:**

1. “The baseline result is trivial because B0 cannot persist outage-period records.”
2. “The paper stitches an embedded software experiment to a separate RF experiment.”
3. “The durable queue itself is not novel.”
4. “The word IIoT implies industrial validation that the experiments do not actually provide.”
5. “The related-work survey is too short.”
6. “The architecture is under-specified.”

**How to neutralize them:**
- make failure-domain-aware evaluation, not buffering novelty, the contribution;
- state the B0 limitation before reviewers do;
- show the two evidence roles in Figure 1 and Methods;
- consider `IoT telemetry` rather than `IIoT telemetry` in title/abstract unless the industrial scope is explicitly justified;
- expand related work substantially;
- exploit receiver-side reconciliation and negative evidence as methodological strengths;
- use the v2.2 experiment dossier as supplementary evidence rather than bloating the main manuscript.

## 4. Consortium consensus

### 4.1 What the paper is

A failure-domain-aware experimental validation paper showing that:

1. durable application record state changes final record survival relative to a non-durable baseline under exact embedded outage/restart semantics;
2. the communication path can degrade and recover independently under physical RF and service/process faults;
3. application delivery, lower-layer health, reconnect, backlog drain, and recovery clocks are distinct endpoints;
4. receiver-side reconciliation and preserved negative evidence are necessary for defensible reporting.

### 4.2 What the paper is not

It is not:
- a proof that a novel buffering algorithm beats MQTT;
- a POWDER architecture comparison;
- a strongest-client benchmark;
- a field/industrial/agronomic validation;
- a universal RF-threshold study;
- a pooled cross-testbed reliability estimate.

## 5. Recommended title strategy

### Consortium preferred title

**WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

Why: this title foregrounds the actual scientific thesis and avoids implying that the same architecture comparison was executed on both testbeds.

### Conservative alternative

**WellPulse: Failure-Domain-Aware Validation of Durable IoT Telemetry with Embedded Record Survival and Controlled-RF Characterization**

The consortium recommends using **IoT** rather than **IIoT** in the title unless the manuscript adds a precise rationale for industrial scope, because the current experiments validate the telemetry/resilience layer with synthetic Modbus-like records rather than an industrial field process.

## 6. Recommended research-question structure

### RQ1 — Record-state survival
Under the frozen FIT outage/restart conditions, how does durable W1 record handling differ from a non-durable publish-only baseline in final receiver-reconciled completeness and recovery cost?

### RQ2 — Physical-path transition
How does the LTE/MQTT path behave across the observed POWDER attenuation transition region, including direction dependence and near-transition variability?

### RQ3 — Failure-domain recovery
How do RF restoration, UE restart, CORE-related restart and broker interruption differ in observable recovery behavior and endpoint semantics?

Cross-testbed triangulation should become a synthesis section rather than a fourth empirical RQ.

## 7. Recommended contribution structure

1. **Failure-domain-aware validation model** separating record-state survival from communication-path recovery.
2. **Receiver-reconciled embedded durability evidence** for W1 versus non-durable B0 under healthy, outage and outage-plus-process-restart conditions.
3. **Controlled physical-path characterization** showing transition variability, cross-layer disagreement and mechanism-specific recovery on POWDER.
4. **Evidence-preserving reproducibility workflow** retaining negative, censored, anomalous and setup evidence with claim-to-raw traceability.

Architecture durability is demonstrated, but generic store-and-forward is explicitly prior art.

## 8. Required manuscript changes

### Mandatory before the next manuscript can be called consortium-revised

- apply all 12 P16 editorial patches;
- strengthen W1 implementation description from canonical code;
- remove P7B/scored/non-scored/work-package language from publication prose;
- explicitly state non-overlapping FIT/POWDER inferential roles near the start of Methods;
- make B0's non-durable nature visible every time the +20 pp result is summarized;
- elevate E8 and E10-A;
- add concrete sender/receiver disagreement example to Discussion;
- expand literature review to the four-axis structure;
- add mandatory FIT IoT-LAB citation/acknowledgment in accordance with the testbed's publication guidance;
- preserve POWDER citation/acknowledgment;
- replace “IIoT” in title/abstract unless industrial scope is explicitly defended;
- prepare supplementary experiment atlas from dossier v2.2;
- perform final Gaspar full-text comparison if accessible before submission.

## 9. Supplementary-material strategy

The experiment dossier should not be copied wholesale into the main article. Instead derive a reviewer-facing supplement containing:

- complete E0–E11 experiment atlas;
- run-validity register;
- anomaly register;
- recovery endpoint semantics;
- FIT 18-cell ledger;
- figure provenance / hashes;
- sanitized derived CSVs and analysis scripts;
- evidence-to-claim map.

This is the correct way to **exhaustively exploit** the project record without destroying the main narrative.

## 10. Final consortium verdict

**The manuscript should undergo a major editorial/scientific-communication revision, not a new experiment.**

The evidence base is stronger than the P15 manuscript currently communicates. The revision should increase defensive depth and exploitation of controls/negative evidence, while decreasing architecture-novelty overtones and internal workflow detail.

`P17_CONSORTIUM_SIZE=8_ROLES`

`P17_NEW_EXPERIMENT_REQUIRED=NO`

`P17_NEW_EMPIRICAL_CLAIMS_REQUIRED=NO`

`P17_MAJOR_MANUSCRIPT_REVISION=YES`

`P17_SUPPLEMENTARY_EXPERIMENT_ATLAS=RECOMMENDED`

`P17_LITERATURE_EXPANSION=MANDATORY`

`P17_GASPAR_FULLTEXT_GATE=OPEN`
