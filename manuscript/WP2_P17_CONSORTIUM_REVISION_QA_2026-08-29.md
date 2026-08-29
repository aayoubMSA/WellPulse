# WP2-P17 — Consortium Revision QA

Date: 2026-08-29  
Status: **PASS / INTERNAL CONSORTIUM-REVISED DRAFT ACCEPTED / SUBMISSION GATES REMAIN OPEN**

## 1. Scope

Audit `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md` against the frozen P13 claim envelope, P16 adversarial prohibitions/editorial requirements, P11 reconstructed values, P12 integration doctrine, canonical W1 implementation, and the v2.2 experiment dossier research pack.

This QA does not authorize submission and does not reopen experimentation.

## 2. Claim-envelope audit

- IC-01 FIT W1-vs-B0 record-survival effect: **PASS**. B0 is repeatedly identified as a non-durable publish-only baseline.
- IC-02 healthy FIT C0: **PASS**. No universal healthy-path reliability claim introduced.
- IC-03 backlog-drain cost: **PASS**. Kept distinct from reconnect and POWDER recovery clocks.
- IC-04 POWDER transition region: **PASS**. Uses experiment-specific programmed attenuation and rejects universal-threshold language.
- IC-05 ICMP degradation before MQTT incompleteness: **PASS**. Presented as path behavior, not W1 durability.
- IC-06 mechanism-dependent recovery: **PASS**. E10-A remains censored; E10-D remains upper bound.
- IC-07 broker-only isolation: **PASS**. Elevated without turning E8 into an architecture comparison.
- IC-08 two-property resilience synthesis: **PASS**. FIT/POWDER are integrated conceptually, not statistically.
- IC-09 receiver-side reconciliation/provenance: **PASS**. Strengthened using preserved seq96/seq150 disagreements and E8 duplicate-send evidence.

`P17_QA_UNSUPPORTED_CLAIMS=0`

## 3. P16 mandatory-patch audit

1. **Title risk:** PASS. Revised title does not imply that W1 was compared on POWDER.
2. **Reader-facing P7B/scored jargon:** PASS in the scientific body; internal P17 control note remains explicitly non-submission material.
3. **W1 implementation specificity:** PASS. Stable ID, canonical serialization, SHA-256, SQLite WAL, `synchronous=FULL`, PENDING/SENT, idempotent exact re-enqueue and conflicting-ID integrity failure are included.
4. **B0 boundary at +20 pp:** PASS.
5. **Non-overlapping FIT/POWDER inferential roles:** PASS and stated near Methods opening.
6. **WP/internal workflow jargon in scientific prose:** PASS; internal control note is clearly marked for removal from submitted copy.
7. **Internal manuscript-control content:** OPEN FOR SUBMISSION COPY ONLY; the current file is intentionally an internal draft.
8. **POWDER publication wording:** PASS; described as a separately executed controlled reference characterization rather than scored architecture evidence.
9. **Gaspar treatment:** PASS WITH OPEN GATE. Bibliographic/scope-level only; final full-text comparison remains required if accessible.
10. **Public artifact wording:** PASS; sanitized/releasable artifact only.
11. **Display set:** OPEN. P17 recommends a redesign but does not silently override P14.
12. **Submission-facing status lines:** OPEN FOR FINAL CLEAN COPY; retained because this is an internal draft.

## 4. Numerical consistency audit

Checked principal values against P11/P13:

- FIT C0 = 100%/100% in 3/3: PASS.
- FIT C1 = B0 80%, W1 100%, +20 pp in 3/3: PASS.
- FIT C2 = B0 80%, W1 100%, +20 pp in 3/3: PASS.
- outage-period records = 2,000: PASS.
- W1 backlog drain means 67.731246 s / 67.870252 s: PASS.
- E1R4 51 dB ICMP 30% loss + MQTT 20/20: PASS.
- E1R4 52 dB ICMP 60% loss + MQTT 13/20: PASS.
- E3 52 dB MQTT 60/25/55%: PASS.
- E10-B 6.063318 s first publish; 6.609430 s first ping; 0.060172 s publish→CORE: PASS.
- E10-C-B 29.247733 / 29.248129 s: PASS.
- E10-D <=10.908749 s upper bound: PASS.
- E8 unique delivery 40/60 with duplicate sender lines preserved: PASS.

`P17_QA_NUMERICAL_CONTRADICTIONS=0`

## 5. Consortium-exploitation audit

The revised draft now materially exploits previously underused evidence without adding claims:

- W1 durable-state semantics are concrete rather than conceptual.
- E8 is elevated as a clean broker-vs-LTE failure-domain control.
- E10-A is elevated as adverse evidence against deterministic RF-only recovery.
- sender/receiver disagreements and E8 duplicate sends concretely motivate receiver-side reconciliation.
- reconnect versus backlog-drain is sharpened as completeness-versus-timeliness distinction.
- recovery cases are organized by failure domain rather than narrated as a run diary.
- v2.2 dossier is explicitly positioned as the source for reviewer-facing supplementary experiment detail.
- related work is reorganized into persistence/retransmission, robustness/fault injection, offline-first/store-forward, and testbed/repeatability axes.

## 6. Remaining publication risks

### R1 — Strong durable comparator
Residual risk: **MODERATE and transparent**. A durable standard MQTT comparator could strengthen a future superiority study but is not needed for the current bounded report.

### R2 — Main-display cohesion
Residual risk: **MODERATE until redesigned/QA'd**. A new architecture + evidence-role schematic and failure-domain taxonomy could make the two-testbed logic immediately legible. P14 remains frozen until explicitly reopened.

### R3 — Supplementary evidence burden
Residual risk: **MODERATE**. The main paper should not absorb the entire 37-page dossier. A concise reviewer supplement must be derived from it.

### R4 — Literature completeness
Residual risk: **MODERATE until submission-date check**, especially Gaspar full text and any newly published MQTT resilience/testbed work.

### R5 — Credits/authorship/funding
Residual risk: **OPEN administrative gate**. Final author list, CRediT roles, collaborator acknowledgments, funding statements, MSA affiliation, FIT IoT-LAB acknowledgment/citation, POWDER acknowledgment/citation, copyright, and licensing must be verified before submission. No unverified attribution is invented in P17.

## 7. P17 decision

The P17 consortium revision is scientifically stronger than P15 and remains fully inside the frozen evidence/claim envelope.

No new experiment is required. No new empirical claim is authorized or needed.

The next work should be publication exploitation rather than more science generation:

1. **P18 — Main-display redesign and claim/display QA**: architecture + evidence-role schematic, failure-domain taxonomy, revised main/supplement split.
2. **P19 — Reviewer-facing supplementary experiment atlas + sanitized artifact** derived from dossier v2.2.
3. **P20 — Final literature/credits/venue/submission preparation** only after P18/P19 PASS.

`WP2_P17_QA=PASS_CONSORTIUM_REVISION_EVIDENCE_BOUNDED`

`P17_NEW_EXPERIMENT_REQUIRED=NO`

`P17_NEW_EMPIRICAL_CLAIMS=0`

`P17_DISPLAY_REDESIGN=OPEN_NEXT_GATE`

`P17_SUPPLEMENTARY_ATLAS=OPEN_NEXT_GATE`

`SUBMISSION_AUTHORIZED=NO`
