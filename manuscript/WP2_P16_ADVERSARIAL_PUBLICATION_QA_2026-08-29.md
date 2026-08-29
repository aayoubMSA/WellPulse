# WP2-P16 — Adversarial Publication QA

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **PASS / SCIENTIFIC QA COMPLETE / MANDATORY EDITORIAL PATCH SET FROZEN**

## 1. Mandate

Stress-test the P15 manuscript as if reviewed by skeptical systems, IoT, wireless, statistics, reproducibility, and artifact reviewers. P16 may tighten wording and publication presentation, but it may not create new scientific claims, reinterpret P8 as scored P7B, pool FIT and POWDER, authorize new experiments, or alter raw evidence.

Canonical manuscript reviewed:

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P15_2026-08-29.md`

Governing scientific authorities remain P10–P14 and the P9 forensic authorities.

## 2. Executive verdict

**SCIENTIFICALLY DEFENSIBLE WITH MANDATORY PUBLICATION-FACING EDITORIAL PATCHES.**

No contradiction was found between the P15 manuscript and the P13 claim envelope. No reported number requires a new experiment. No statistical pooling was introduced. The principal residual risk is **interpretive**, not evidentiary: a reviewer could misread the paper as a claim that WellPulse outperformed MQTT across both FIT and POWDER, or as a strong-comparator study, unless publication-facing wording is tightened.

P16 therefore freezes a mandatory editorial patch set in:

`manuscript/WP2_P16_MANDATORY_EDITORIAL_PATCHES_2026-08-29.md`

Those patches do not change results, claims, figures, tables, evidence classes, or scientific conclusions.

## 3. Adversarial reviewer attacks

### A1 — “This is just store-and-forward.”

**Pre-QA risk:** HIGH  
**Post-QA risk:** LOW–MODERATE  
**Verdict:** PASS WITH BOUNDED NOVELTY

Prior work already establishes MQTT retransmission, database-backed recovery, offline-first reconciliation, edge/cloud continuity, and 5G store-and-forward. The manuscript correctly avoids claiming buffering as novelty.

The defensible contribution is compound:

- real-embedded record-survival evidence under exact outage/restart semantics;
- failure-domain decomposition;
- controlled physical-RF characterization;
- receiver-side reconciliation and immutable traceability.

The final paper must continue to state explicitly that buffering/store-and-forward is prior art.

### A2 — “B0 is a strawman baseline.”

**Pre-QA risk:** SEVERE  
**Post-QA risk:** MODERATE / TRANSPARENT LIMITATION  
**Verdict:** PASS ONLY WITH EXPLICIT BOUNDARY

This is the strongest residual scientific limitation. FIT B0 is intentionally non-durable and is not the strongest durable MQTT configuration available. The observed +20 percentage-point difference demonstrates the consequence of application-level durability relative to B0 under the exact treatment; it does **not** demonstrate superiority over MQTT generally or a durable standard client.

A durable comparator could strengthen a future study but is **not required to report the existing bounded experiment honestly**. P16 does not authorize or require a new comparator experiment for this manuscript.

### A3 — “The two testbeds are unrelated studies stitched together.”

**Pre-QA risk:** HIGH  
**Post-QA risk:** MODERATE  
**Verdict:** PASS WITH EXPLICIT ROLE SEPARATION

The paper is coherent only under the P12 two-property model:

- FIT measures **record-state survival / architecture durability**;
- POWDER measures **communication-path degradation and recovery**.

The two classes must never be described as replication of the same treatment. The manuscript title, abstract, Methods, and Discussion must prevent readers from inferring that W1 was compared against B0/B1 on POWDER.

### A4 — “POWDER is an uncontrolled/manual anecdote.”

**Pre-QA risk:** HIGH  
**Post-QA risk:** MODERATE  
**Verdict:** PASS AS CHARACTERIZATION, NOT CONFIRMATORY EFFECT ESTIMATION

P8/P9 are evidence-rich but were manually executed and are not a scored architecture comparison. Their appropriate scientific role is controlled **reference characterization** of physical-RF transition, direction/repeatability, failure-domain separation, and endpoint-specific recovery.

The publication-facing manuscript should avoid internal terms such as `scored`, `P7B`, and `non-scored`; instead state that POWDER is a manually executed reference characterization not used for architecture-effect estimation.

### A5 — “The sample size is inflated by 10,000 messages.”

**Pre-QA risk:** MEDIUM  
**Post-QA risk:** LOW  
**Verdict:** PASS

P15 correctly identifies the FIT replicate/run as the scientific unit. The 10,000 messages are within-run observations used for record reconciliation. No message-level p-value or confidence interval is used as if messages were independent replicates.

The identical three-replicate outcomes are reported descriptively rather than converted into unsupported population reliability probabilities.

### A6 — “The paper cherry-picks a 52 dB threshold.”

**Pre-QA risk:** HIGH  
**Post-QA risk:** LOW  
**Verdict:** PASS

P11/P14/P15 report an experiment-specific transition region rather than a universal threshold. E1R4, E2, and E3 visibly preserve direction and cycle variability. No smoothing or fitted threshold is introduced.

The unresolved attenuator-ID→physical-path mapping remains explicitly outside the claim envelope.

### A7 — “Recovery latency is inconsistently defined.”

**Pre-QA risk:** HIGH  
**Post-QA risk:** LOW  
**Verdict:** PASS

Recovery clocks remain mechanism- and endpoint-specific:

- E10-A = censored non-recovery within the observation window;
- E10-B = action-begin→first publish / first ping and publish→CORE receipt;
- E10-C-B = RF restore→first ping/publish;
- E10-D = upper bound only;
- FIT backlog drain is distinct from reconnect time and from all POWDER recovery clocks.

P14 correctly avoids a generic recovery-latency bar chart.

### A8 — “Sender logs cannot prove delivery.”

**Pre-QA risk:** MEDIUM  
**Post-QA risk:** LOW  
**Verdict:** PASS

The manuscript uses receiver-side unique identity reconciliation. FIT reconstructs generated vs received record IDs. POWDER reconciles UE sent vs CORE received unique sequences and preserves sender/receiver disagreements and duplicate sends.

This is one of the strongest methodological defenses in the paper.

### A9 — “The architecture is underspecified.”

**Pre-QA risk:** MODERATE–HIGH  
**Post-QA risk after mandatory patch:** LOW–MODERATE  
**Verdict:** PATCH REQUIRED

P15 describes W1 conceptually but not with enough implementation specificity for a systems reviewer. Canonical source inspection confirms:

- record identity = `run_id:boot_id:sequence`;
- canonical serialized payload with SHA-256 checksum;
- SQLite durable queue;
- WAL journal mode;
- `PRAGMA synchronous=FULL`;
- explicit `PENDING` / `SENT` state;
- identical re-enqueue is idempotent;
- conflicting reuse of an existing record ID raises an integrity error.

These details must be inserted into the publication-facing architecture/Methods text. They describe the actual implementation and introduce no new claim.

### A10 — “Internal project-control language weakens the paper.”

**Pre-QA risk:** HIGH  
**Post-QA risk after mandatory patch:** LOW  
**Verdict:** PATCH REQUIRED

Terms such as `P7B`, `scored`, `P9–P14 workflow`, and the internal manuscript-control note are useful in the repository but inappropriate in the submitted scientific text. They expose abandoned/internal workflow details that are unnecessary for interpreting the final evidence.

The public manuscript should express the same boundaries using standard scientific language.

### A11 — “The literature positioning is incomplete or stale.”

**Pre-QA risk:** MODERATE  
**Post-QA risk:** MODERATE UNTIL SUBMISSION-DATE CHECK  
**Verdict:** PASS FOR P16 / FINAL CHECK REQUIRED BEFORE SUBMISSION

P16 re-verified the key bibliographic anchors used in the manuscript, including the 2026 systematic review, MQTT robustness work, retransmission work, 5G store-and-forward work, and POWDER platform paper. The Gaspar et al. 2026 bibliographic record and DOI are independently confirmed, but a detailed methods/results comparison remains unavailable from the sources inspected.

Therefore the manuscript may cite Gaspar et al. only at bibliographic/scope level until full-text comparison is completed. A final submission-date literature check remains mandatory.

### A12 — “The artifact cannot actually be released.”

**Pre-QA risk:** MODERATE  
**Post-QA risk:** MODERATE  
**Verdict:** SCIENTIFIC PASS / RELEASE PACKAGING PENDING

The reproducibility chain is strong, but some preservation archives contain private or credential-bearing material and cannot be released as-is. This is not a scientific validity failure. Before submission or artifact review, produce a sanitized public artifact containing analysis code, derived data, figure generation, non-sensitive manifests, and only releasable evidence.

Do not promise public release of private raw bundles before that privacy/security gate.

## 4. Reference verification during P16

Current web verification on 2026-08-29 confirmed:

- Asgari Araghi & Khendek, *Discover Internet of Things* 6, article 61 (2026), DOI `10.1007/s43926-026-00322-w`;
- Jesus et al., *Internet of Things* 31, 101590 (2025), DOI `10.1016/j.iot.2025.101590`;
- Colarusso et al., *Internet of Things* 33, 101723 (2025), DOI `10.1016/j.iot.2025.101723`;
- Domingues et al., *EURASIP Journal on Wireless Communications and Networking* 2024, article 2, DOI `10.1186/s13638-023-02327-3`;
- Gaspar et al., *IEEE Internet of Things Magazine* (2026), DOI `10.1109/MIOT.2026.3681190` — bibliographic record confirmed;
- Herrera et al., *Future Internet* 18(4), 180 (2026), DOI `10.3390/fi18040180`;
- Monzon Baeza et al., *Sensors* 26(15), 4919 (2026), DOI `10.3390/s26154919`;
- Breen et al., *Computer Networks* 197, 108281 (2021), DOI `10.1016/j.comnet.2021.108281`.

## 5. Scientific consistency audit

- P13 primary claims represented without expansion: PASS.
- FIT architecture effect restricted to B0-vs-W1: PASS.
- POWDER not used as W1/B1 architecture evidence: PASS.
- 52 dB not promoted to universal threshold: PASS.
- E10-A adverse/censored result retained: PASS.
- E10-D kept as upper bound: PASS.
- FIT message count not treated as independent n: PASS.
- FIT and POWDER statistical pooling: NONE.
- field/agronomic/pump claims: NONE.
- scored P7B promoted to positive evidence: NO.
- new experiment required to support current bounded conclusions: NO.

## 6. Reviewer-severity summary

| Attack | Residual severity after P16 | Status |
|---|---|---|
| Store-and-forward novelty | Low–Moderate | Controlled |
| Weak/non-durable baseline | Moderate | Explicit limitation |
| Two-testbed cohesion | Moderate | Controlled by two-property framing |
| Manual POWDER characterization | Moderate | Descriptive role only |
| Statistical pseudoreplication | Low | Controlled |
| Universal threshold interpretation | Low | Controlled |
| Recovery-clock ambiguity | Low | Controlled |
| Sender-vs-receiver accounting | Low | Controlled |
| Architecture specification | Low–Moderate after patch | Mandatory patch |
| Internal workflow jargon | Low after patch | Mandatory patch |
| Literature completeness | Moderate until final check | Final gate |
| Public artifact privacy | Moderate | Packaging gate |

## 7. P16 decision

The existing evidence is sufficient for a defensible paper **without a new experiment**, provided the paper remains bounded to the current claims and the mandatory editorial patches are applied.

A stronger durable MQTT comparator would improve generality and reviewer resistance, but adding one now would create a new scientific campaign and is not necessary to make the existing findings publishable as presently framed.

P16 therefore does **not** reopen experimentation.

## 8. Acceptance gate

- adversarial scientific review completed: PASS;
- unsupported claim discovered in P15: `0`;
- numerical contradiction with P11/P13: `0`;
- statistical pooling discovered: `0`;
- mandatory scientific rerun: `NO`;
- mandatory new comparator experiment: `NO`;
- mandatory publication-facing editorial patches: `YES`;
- sanitized public artifact still required before release/submission package: `YES`;
- final literature/venue verification at submission date: `YES`.

`P16_SCIENTIFIC_BLOCKERS=0`

`P16_NEW_EXPERIMENT_REQUIRED=NO`

`P16_MANDATORY_EDITORIAL_PATCHES=YES`

`P16_PUBLIC_ARTIFACT_SANITIZATION_REQUIRED=YES`

`WP2_P16=PASS_ADVERSARIAL_PUBLICATION_QA`
