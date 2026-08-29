# WP2-P17V — Superior Independent Consortium Validation

Date: 2026-08-29  
Status: **VALIDATED WITH PRE-SUBMISSION CONDITIONS / NO NEW EXPERIMENT REQUIRED**

## 1. Mandate

Perform a second, stricter validation of the P17 consortium-revised WellPulse manuscript. The task is to try to invalidate the revised thesis, effect interpretation, evidence integration, statistical language, novelty boundary, implementation description, and reproducibility claims.

The second consortium is role-based; no fictitious real-person identities are asserted.

The first consortium's conclusions are not treated as scientific evidence. Primary validation is against P11/P12/P13/P16, canonical source code, accepted forensic authorities, and an independent literature/baseline check.

## 2. Superior consortium composition

### V1 — Senior systems-paper editor / meta-reviewer
Tests whether one coherent paper exists and whether the title/abstract/contribution hierarchy match the actual evidence.

### V2 — MQTT protocol, QoS, session and persistence specialist
Tests comparator fairness, Paho/persistent-state prior art, durable-client attack surface and protocol overclaiming.

### V3 — Embedded storage and crash-consistency reviewer
Tests whether the W1 durability description is faithful to actual code and whether SQLite/WAL semantics are overstated.

### V4 — Wireless/RF experimentalist
Tests attenuation interpretation, direction/repeatability, recovery-domain semantics and universal-threshold risk.

### V5 — Cellular/LTE systems reviewer
Tests CORE/UE/broker path separation and whether radio/service recovery clocks are being conflated.

### V6 — Experimental design and statistical inference reviewer
Tests unit of analysis, replication, deterministic outcomes, pseudoreplication, effect wording, censoring and upper bounds.

### V7 — Causal-inference / measurement-methodology reviewer
Tests whether the manuscript attributes outcomes to the correct manipulated domain and whether the two-testbed synthesis implies unsupported causation.

### V8 — Reproducibility / forensic evidence auditor
Tests receiver-side accounting, anomalies, invalid/setup attempts, hashes and claim-to-raw traceability.

### V9 — Research-software reviewer
Tests implementation reproducibility, record identity/integrity semantics and source-to-method consistency.

### V10 — Literature / novelty meta-reviewer
Re-checks whether persistence, retransmission, offline-first, store-and-forward or testbed methodology are already established and whether the manuscript's novelty is still bounded correctly.

### V11 — Scientific visualization / information-design reviewer
Tests whether the proposed main-display strategy makes the two evidence roles legible without creating a false pooled result.

### V12 — Adversarial journal associate-editor simulation
Assumes a rejection posture and asks whether remaining weaknesses are fatal scientific blockers or transparent limitations.

## 3. Validation protocol

The consortium applies four stages:

1. **Authority reconstruction:** P11/P12/P13/P16 + code establish the permitted scientific state.
2. **Claim audit:** every P17 empirical/methodological claim is checked against that state.
3. **Independent prior-art/baseline check:** current MQTT persistence, store-and-forward and testbed literature is checked again rather than inherited from the first consortium.
4. **Meta-review:** remaining reviewer attacks are classified as `SCIENTIFIC BLOCKER`, `MANDATORY PRE-SUBMISSION GATE`, `TRANSPARENT LIMITATION`, or `NON-BLOCKING`.

Companion claim matrix:

`analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`

## 4. Independent reviewer verdicts

### V1 — Systems/meta-review

**VERDICT: VALIDATED.**

The P17 title and manuscript structure are substantially better aligned with the actual evidence than P15. The central thesis — separating record-state survival from communication-path recovery — explains why FIT and POWDER belong together without implying that they repeat the same treatment.

The strongest paper-level statement is methodological and experimental rather than algorithmic novelty.

No additional empirical RQ is needed. Cross-testbed integration is appropriately a synthesis section.

### V2 — MQTT protocol/persistence

**VERDICT: VALIDATED WITH COMPARATOR LIMITATION.**

The manuscript correctly states that persistence/retransmission are prior art and that B0 is a non-durable publish-only comparator. Independent official Paho documentation confirms that persistent message stores are provided specifically to support reliable delivery across network/client restarts and that memory-only state can be lost after client/runtime/device shutdown.

Therefore the +20 pp FIT result is publishable only as a bounded durability effect relative to B0. P17 does that correctly.

Absence of a strong durable standard-client comparator remains the largest scientific limitation, but it is **not a blocker** for the current bounded paper because no general superiority claim is made.

### V3 — Embedded storage/crash consistency

**VERDICT: VALIDATED.**

P17's implementation paragraph matches canonical source:

- stable `run_id:boot_id:sequence` identity;
- deterministic canonical JSON;
- SHA-256 checksum;
- SQLite WAL;
- `synchronous=FULL`;
- `PENDING` / `SENT` state;
- idempotent exact duplicate enqueue;
- explicit error on conflicting identity reuse.

P17 does not falsely convert these implementation choices into a universal power-failure guarantee. The experiment demonstrates survival under the executed gateway-process restart semantics, not arbitrary storage-device or whole-node power failure.

### V4 — Wireless/RF experimentalist

**VERDICT: VALIDATED AS CHARACTERIZATION.**

The transition-region language is appropriate. P17 avoids a universal 52 dB threshold and treats the programmed attenuation as experiment-specific. E1R4/E2/E3 jointly support a variable transition/recovery region and direction dependence.

The manuscript correctly avoids reconstructing unresolved attenuator-ID→physical-path mapping.

E4 versus E10-A supports the narrower statement that RF-only recovery was not observed uniformly across preserved cases; it does not justify a stochastic probability of RF recovery.

### V5 — LTE systems reviewer

**VERDICT: VALIDATED.**

The manuscript distinguishes:

- radio/path recovery;
- UE restart;
- CORE-related recovery;
- broker-only service failure;
- application gateway-process restart.

E8 is a strong control because LTE ping remains healthy while MQTT fails. E10 endpoint clocks are kept distinct and no generic recovery-latency distribution is created.

### V6 — Experimental design/statistics

**VERDICT: VALIDATED / STRONG DISCIPLINE.**

P17 correctly uses the FIT run as scientific unit and does not inflate n using 10,000 messages. It reports identical run-level effects descriptively and does not manufacture confidence intervals.

Censoring and upper bounds are handled correctly. E3 repetition is characterization rather than population inference.

No statistical blocker was identified.

### V7 — Causal/measurement methodology

**VERDICT: VALIDATED WITH WORDING DISCIPLINE.**

The two-property model is defensible because the evidence classes answer different causal questions. P17 explicitly states that FIT and POWDER have non-overlapping inferential roles and are not statistically pooled.

The exact 2,000-record B0 loss aligns with the treatment window and non-durable design; the manuscript appropriately interprets it as a treatment-bounded record-survival consequence, not a population effect.

### V8 — Reproducibility/forensics

**VERDICT: VALIDATED / MAJOR STRENGTH.**

P17 exploits the evidence chain substantially better than P15. In particular:

- seq 96 and seq 150 expose sender/receiver disagreement;
- E8 duplicate sender lines demonstrate why unique IDs, not line counts, govern completeness;
- E10-A remains negative/censored;
- E10-D remains upper-bound;
- missing artifacts and setup attempts remain visible;
- private raw evidence is not promised for public release.

The consortium considers receiver-side reconciliation plus anomaly preservation one of the strongest defenses of the paper.

### V9 — Research software

**VERDICT: VALIDATED.**

Methods now describe the actual W1 implementation instead of an abstract “buffer.” This materially improves reproducibility and reduces the risk that reviewers misinterpret the contribution as a generic queue.

Before artifact release, exact dependency/runtime versions should be captured in the sanitized package, but this is a packaging gate rather than a scientific blocker.

### V10 — Literature/novelty

**VERDICT: VALIDATED WITH OPEN FINAL LITERATURE GATE.**

Independent current checks reconfirm that:

- durable MQTT persistence is established;
- retransmission after disconnection is established;
- offline-first reconciliation is established;
- 5G/NTN store-and-forward is established;
- controlled real-testbed/repeatability methodology is established;
- POWDER is explicitly designed for controllable end-to-end wireless experimentation.

Thus, P17 is correct not to claim novelty for persistence/store-and-forward itself.

The defensible novelty remains the **combination of failure-domain-aware evaluation, bounded real-embedded durability evidence, controlled physical-path characterization, endpoint-specific recovery semantics, and evidence-preserving receiver reconciliation**.

Gaspar et al. 2026 is independently confirmed bibliographically; detailed full-text comparison remains a mandatory pre-submission condition if accessible.

The consortium does **not** certify historical uniqueness of the two-property model. The manuscript should present it as the study's evaluation framework unless a dedicated literature proof establishes priority.

### V11 — Visualization/information design

**VERDICT: SCIENCE VALIDATED; DISPLAY GATE OPEN.**

P17's science can be understood without new results, but reviewers will grasp the two-testbed logic faster if the main displays are redesigned.

Recommended P18 main display set remains:

1. architecture + evidence-role schematic;
2. FIT completeness figure;
3. POWDER transition/direction figure;
4. POWDER E3 repeatability figure;
5. compact failure-domain taxonomy table;
6. compact recovery-semantics table.

The 37-page experiment dossier should be transformed into reviewer supplement rather than inserted into the article.

### V12 — Adversarial associate editor

**VERDICT: VALIDATED WITH PRE-SUBMISSION CONDITIONS; NOT READY TO SUBMIT TODAY.**

Most likely rejection attacks and their status:

| Attack | P17V assessment |
|---|---|
| “B0 is a strawman” | Transparent and bounded; limitation remains but no invalid superiority claim |
| “Durable queue is not novel” | Neutralized: manuscript explicitly treats persistence as prior art |
| “Two unrelated testbeds stitched together” | Scientifically neutralized by non-overlapping evidence roles; visual cohesion still needs P18 |
| “Sample size is 10,000 messages” | Neutralized: run is unit of inference |
| “52 dB cherry-picked threshold” | Neutralized: transition region + E3 variability |
| “Recovery latency inconsistent” | Neutralized: mechanism-specific exact/censored/upper-bound semantics |
| “Sender log proves delivery” | Neutralized: receiver-side unique-ID reconciliation |
| “POWDER is anecdotal/manual” | Remains moderate; acceptable only as controlled reference characterization |
| “Architecture under-specified” | Neutralized by canonical implementation semantics |
| “Related work incomplete” | Improved; final submission-date search/full-text gate still mandatory |
| “Artifact not releasable” | Open but solvable through sanitized P19 artifact |

No fatal scientific blocker was identified.

## 5. Superior-consortium consensus

### Scientifically validated

- all 9 P13 claims remain supported in P17;
- no new empirical claim is required;
- no new experiment is required;
- no numerical contradiction was identified;
- W1 implementation description is faithful to source;
- failure-domain and statistical boundaries are substantially improved;
- adverse evidence is exploited rather than hidden;
- the two-testbed synthesis is defensible when presented as non-pooled complementary evidence.

### Not yet validated for external submission

- final main display set;
- reviewer-facing supplementary atlas;
- sanitized public/reviewer artifact;
- submission-date literature completeness / Gaspar full text;
- final authorship and CRediT roles;
- funding and collaborator acknowledgments;
- MSA/FIT/POWDER credit wording;
- copyright/license statement for released artifact;
- target-journal formatting and final proof.

## 6. Final verdict

**P17 is independently scientifically validated.**

The correct status is not `SUBMISSION_READY`; it is:

> **VALIDATED WITH PRE-SUBMISSION CONDITIONS.**

The second consortium finds no scientific justification for reopening FIT or POWDER experimentation for the current bounded manuscript. The remaining work should strengthen communication, auditability, literature closure, credits, and release packaging.

`P17V_SUPERIOR_CONSORTIUM_SIZE=12_ROLES`

`P17V_CLAIMS_VALIDATED=9_OF_9`

`P17V_NUMERICAL_CONTRADICTIONS=0`

`P17V_SCIENTIFIC_BLOCKERS=0`

`P17V_NEW_EMPIRICAL_CLAIMS=0`

`P17V_NEW_EXPERIMENT_REQUIRED=NO`

`P17V_DISPLAY_GATE=P18_OPEN`

`P17V_SUPPLEMENT_ARTIFACT_GATE=P19_OPEN`

`P17V_FINAL_LITERATURE_CREDITS_VENUE_GATE=P20_OPEN`

`P17V_VERDICT=VALIDATED_WITH_PRE_SUBMISSION_CONDITIONS`

`SUBMISSION_AUTHORIZED=NO`
