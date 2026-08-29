# WP2-P20E-R3 — Red-Hat Adversarial Submission Review

Date: 2026-08-29
Target venue: **Internet of Things (Elsevier)**
Article type: **Full Research paper**
Status: **PASS / RED-HAT CLEARED / NO SCIENTIFIC OR PRODUCTION BLOCKER / NOT SUBMITTED**

## 1. Review object

This review evaluates the exact current Elsevier R3-R2 production authority after the literature/reference expansion:

- archive: `WellPulse_P20D_R3R2_Elsevier_IoT_Submission_Package_2026-08-29.zip`;
- Drive ID: `1Th-aO9_2wOnhD6EWyh5b6qml4fPmGDSb`;
- archive SHA-256: `6ca12912711f9f7b9f255bb161399244fac4572c7d902db0ad2270741b38496d`;
- archive size: `2,157,349 bytes`;
- Drive raw read-back: exact-hash PASS;
- main PDF: `WellPulse_Elsevier_IoT_P20D_R3R2_SubmissionDraft.pdf`;
- PDF SHA-256: `d68c7b19a0785a4c8527156e93213ee4ac0582cccaccd95c28f815da6641c768`;
- manuscript pages: `19`;
- bibliography/source groups: `32`.

P20E-R3 is an adversarial review, not another authoring pass. It attacks the paper as a skeptical desk editor, domain reviewer, systems reviewer, wireless reviewer, statistics reviewer, reproducibility reviewer and publication-integrity reviewer.

## 2. Attack dimensions

The review challenged:

1. venue/article identity and desk-editor plausibility;
2. novelty and closest-prior-art collision;
3. literature-survey legitimacy and completeness framing;
4. comparator fairness;
5. statistical and experimental-unit inference;
6. FIT treatment semantics;
7. POWDER failure/recovery semantics;
8. cross-testbed coherence;
9. numerical fidelity to frozen evidence;
10. figure/evidence readability;
11. reproducibility and supplementary-package integrity;
12. reference/citation integrity;
13. authorship/identity/funding/COI/AI declarations;
14. privacy/security leakage;
15. prohibited-claim regression;
16. package/build reproducibility and submission usability.

## 3. Red-hat findings and dispositions

### RH-01 — Survey-count regression after reference expansion

**Attack:** The expanded manuscript carried one stale statement saying Supplement S1 contained the earlier 17-group audit while the new audit contained 32 groups.

**Severity:** production blocker if left unresolved.

**Disposition:** **FIXED** in R3-R1. Main text now consistently identifies the complete `32`-group audit.

### RH-02 — Risk of pseudo-systematic-review overclaiming

**Attack:** Reporting exact search/audit counts without qualification could lead a reviewer to infer PRISMA-style exhaustiveness and demand formal systematic-review search/reproducibility criteria.

**Severity:** material editorial risk.

**Disposition:** **FIXED** in R3-R1. The paper now states that the literature component is a **targeted, claim-bounding submission-date novelty audit**, not a PRISMA systematic review, meta-analysis or exhaustive bibliographic census. Sources are retained because they support, constrain or invalidate manuscript claims, not to estimate literature prevalence.

### RH-03 — Internal retrieval-process language in scholarly narrative

**Attack:** A Gaspar et al. sentence described internal full-text retrieval limitations, which reads as workflow provenance rather than publication-quality scholarly synthesis.

**Severity:** production/editorial quality defect.

**Disposition:** **FIXED** in R3-R2. The paper now treats Gaspar et al. as current practical MQTT stress-testing context and makes no detailed method/result comparison. No unsupported attribution is made.

### RH-04 — Supplement label/file-role mismatch

**Attack:** The manuscript called the reproducibility package `Supplement S2` while the submission-facing file retained a historical P19 internal filename.

**Severity:** submission usability defect.

**Disposition:** **FIXED** in R3-R2. Submission-facing artifact is now `Supplement_S2_Reproducibility_Artifact.zip` with unchanged verified bytes.

### RH-05 — Non-durable B0 comparator is not strongest MQTT

**Attack:** A skeptical systems reviewer can argue that a durable MQTT client/session comparator may reduce or eliminate the observed W1-versus-B0 difference.

**Severity:** **major scientific limitation, but controlled and already disclosed**.

**Disposition:** **PASS WITH LIMITATION**. The paper explicitly labels B0 a **non-durable publish-only baseline**, prohibits generic MQTT superiority, and states that comparison with a strong durable client is the most valuable extension for any future architecture-superiority claim. No new experiment is required for the current bounded contribution.

### RH-06 — FIT independent sample size

**Attack:** Three run-level replicates per architecture-condition cell are limited. Treating 10,000 messages as independent n would constitute pseudoreplication.

**Severity:** material statistical risk if mishandled.

**Disposition:** **PASS / CONTROLLED**. The manuscript defines the run/replicate as the scientific unit, reports repeated run outcomes without population-probability inference, and treats small timing differences descriptively rather than as powered comparisons.

### RH-07 — C2 restart scope could be overstated

**Attack:** `gateway-process restart` could be misread as hardware/node reboot.

**Disposition:** **PASS / CONTROLLED**. The manuscript explicitly states C2 is gateway-process `exec` restart, not a whole-node/hardware reboot.

### RH-08 — POWDER timing semantic collapse

**Attack:** Combining RF-only, UE restart, CORE restart and broker-restart observations into one recovery-latency result would be scientifically invalid.

**Disposition:** **PASS**. Exact/censored/upper-bound endpoint semantics remain separate. E10-A has no scalar recovery latency; E10-D remains an upper bound only; mechanism-specific timings are not pooled.

### RH-09 — Cross-testbed causal incoherence

**Attack:** FIT and POWDER could appear to be unrelated experiments or, worse, pooled evidence for one reliability effect.

**Disposition:** **PASS**. The paper assigns non-overlapping inferential roles: FIT evaluates architecture-level record-state survival; POWDER characterizes communication-path degradation/recovery. Main Figure 1 and the text make the relationship explicit; no pooled statistic is used.

### RH-10 — Survey/reference depth

**Attack:** The former 17-reference version did not visibly reflect the literature effort and risked appearing under-positioned for a manuscript making a methodology/novelty-boundary argument.

**Disposition:** **FIXED / PASS**. Current manuscript contains `32` references/source groups:

- 25 peer-reviewed scholarly articles;
- 1 normative MQTT standard;
- 6 official technical/platform documentation sources.

The full audit classifies `17` wording-narrowing groups, `15` contextual/no-impact groups, and `0` scientific blockers. All 32 bibliography entries are cited; there are no uncited or missing citation keys.

### RH-11 — Closest same-journal and mechanism prior art

**Attack:** Recent persistence/store-and-forward/acknowledgment work, including current `Internet of Things` papers, could narrow WellPulse's novelty materially.

**Disposition:** **PASS WITH NARROWED CLAIM**. The expanded survey explicitly includes relevant same-journal and adjacent prior art, including Bozorgi et al. 2026, and constrains mechanism novelty. The paper does not claim persistence, retransmission, store-and-forward, offline-first operation, receiver confirmation, testbed use or generic failure testing as new.

### RH-12 — Numerical drift after literature expansion

**Attack:** Large editorial restructuring could accidentally alter frozen empirical values.

**Disposition:** **PASS**. Red-hat spot checks match frozen authorities, including FIT 10,000-record cell size, B0 8,000/10,000 versus W1 10,000/10,000 under C1/C2, +20 percentage-point bounded difference, W1 backlog means 67.731246/67.870252 s, POWDER transition values and E10 exact/censored/upper-bound timing semantics.

### RH-13 — Reproducibility package

**Attack:** Reviewer supplement could contain stale caches, broken rebuild paths or unverifiable derived data.

**Disposition:** **PASS**. `Supplement_S2_Reproducibility_Artifact.zip` retains SHA-256 `99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`; isolated `python -I artifact_selfcheck.py` passes; cache files are absent from the submission package.

### RH-14 — Reference integrity

**Disposition:** **PASS**.

- bibliography entries: 32;
- unique cited bibliography keys: 32;
- uncited bibliography entries: 0;
- cited keys without bibliography entry: 0;
- unresolved citation markers: 0.

### RH-15 — Publication identity and declarations

**Disposition:** **PASS**.

- publication name: **Ahmed Ayoub** only;
- legacy expanded publication names: absent submission-facing;
- sole/corresponding author state preserved;
- funding: no external research funding;
- competing-interest declaration present;
- CRediT present;
- data availability present;
- Elsevier generative-AI declaration present.

### RH-16 — Privacy/security

**Disposition:** **PASS**. No private IPv4 addresses were detected in the current main manuscript; sanitized P19/S2 handling remains in force.

### RH-17 — Forbidden-claim regression

**Disposition:** **PASS**. No generic `WellPulse beats/outperforms MQTT`, no universal 52 dB threshold, no scored-P7B success, no strongest-durable-MQTT superiority, no exact E10-D broker latency, no population reliability inference and no pooled FIT+POWDER claim were detected.

### RH-18 — Manuscript length / survey prominence

**Attack:** At 19 preprint pages, a desk editor could regard the literature/novelty section as unusually prominent for a Full Research article.

**Severity:** residual editorial risk, not a current rule violation.

**Disposition:** **ACCEPT / AUTHOR-OBJECTIVE CONTROLLED**. The author explicitly requires the paper to show the literature-survey effort. No current concrete venue page-limit blocker has been identified. The survey should not be cut merely to imitate a shorter article; only a verified venue instruction or a later editorial request should trigger lossless compression.

## 4. Strongest surviving reviewer vulnerabilities

After all finite repairs, the strongest real vulnerabilities are:

1. **Comparator strength:** B0 is non-durable, so the paper cannot establish superiority over strongest durable MQTT configurations.
2. **Replication depth:** FIT has three independent run-level replicates per cell; inference remains deliberately bounded/descriptive.
3. **Literature audit identity:** the survey is targeted and claim-bounding rather than exhaustive/systematic; it must not be sold as a systematic review.
4. **Gaspar detailed overlap:** no detailed method/result comparison is made; if authoritative full text is later directly recovered before submission, it can be checked as due diligence without reopening experiments.
5. **Survey prominence / 19-page preprint:** intentional under the author's current objective and not a scientific defect.

None of these constitutes a blocker under the current claim envelope.

## 5. Red-hat verdict

- scientific blockers: **0**;
- production blockers after finite fixes: **0**;
- unresolved citation errors: **0**;
- forbidden claim regressions: **0**;
- new experiment required: **NO**;
- new empirical claim required: **NO**;
- manuscript may proceed to a new P21-R3 internal authorization-packet gate when the author chooses to resume submission preparation;
- previous P21-R2 packet is superseded because it names old R2 bytes;
- no external submission is authorized.

`WP2_P20E_R3=PASS_RED_HAT_ADVERSARIAL_SUBMISSION_REVIEW`

`P20E_R3_SCIENTIFIC_BLOCKERS=0`

`P20E_R3_PRODUCTION_BLOCKERS=0`

`P21_R2=SUPERSEDED_BY_NEW_R3R2_BYTES`

`P21_R3=LOCKED_NOT_STARTED`

`P22_LOCKED=YES`

`SUBMISSION_AUTHORIZED=NO`
