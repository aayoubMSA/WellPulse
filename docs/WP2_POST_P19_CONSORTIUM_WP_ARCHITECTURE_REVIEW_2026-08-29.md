# WP2 — Post-P19 Consortium Work-Package Architecture Review

Date: 2026-08-29  
Status: **PASS / FUTURE-WP ARCHITECTURE REFACTORED / NO SCIENCE REOPENED**

## 1. Mandate

Validate the WellPulse publication-preparation work-package architecture after P18RC and P19, and refactor the remaining lane where necessary. This is a governance/process review, not a scientific re-analysis.

Frozen authorities remain unchanged: P10 scientific contract, P11 reconstructed values, P12 integration doctrine, P13 claim envelope, P17/P17V manuscript validation, P18RC production main displays, and P19 reviewer supplement/sanitized artifact.

Submission remains NOT AUTHORIZED.

## 2. Consortium

The review uses the same role-based 12-member consortium logic previously applied in P17V, now focused on work-package architecture:

1. systems-paper editor / meta-reviewer;
2. MQTT persistence/protocol specialist;
3. embedded storage/crash-consistency reviewer;
4. wireless/RF experimentalist;
5. LTE systems reviewer;
6. experimental-design/statistics reviewer;
7. causal/measurement-methodology reviewer;
8. reproducibility/forensic-evidence auditor;
9. research-software/artifact reviewer;
10. literature/novelty meta-reviewer;
11. scientific-visualization/publication-production reviewer;
12. adversarial journal associate-editor simulation.

No fictitious real-person identities are asserted.

## 3. Retrospective validation verdict

### P18RC

**VALIDATED / DO NOT REOPEN.**

P18RC is a properly bounded production-normalization gate. It changed no scientific values, axes, aggregations, claims, or failure-domain semantics; it closed the exact production issues raised by P18RB and demonstrated two-build equality across all 12 PDF/SVG/PNG outputs.

### P19

**VALIDATED / DO NOT REOPEN SCIENTIFICALLY.**

Independent post-closure checks performed during this consortium review found:

- archived ZIP SHA-256 exactly matches the frozen P19 authority: `5a9ed4fa197ea5c3aa43447fabf16d7928aeabe58722e16af63afe25bc7cfdc7`;
- package manifest verified `54/54` listed files;
- `artifact_selfcheck.py` passed under isolated Python invocation (`python -I`) using only the standard library;
- the frozen scientific invariants and 9/9 P13 claim envelope remained intact.

One **non-scientific packaging-hygiene exception** was found: the reviewer artifact contains two `__pycache__/*.pyc` files. No obvious secret, credential, email, absolute user path, or scientific-content issue was found in those bytecode files. This does not invalidate P19 PASS, but compiled-cache files must be excluded from the final externally distributed source/reviewer package.

Classification: `NON_BLOCKING_PACKAGING_DEBT`.

## 4. Consortium diagnosis of the original P20 design

The existing P20 description is scientifically safe but operationally over-coupled. It combines:

- final literature/novelty verification;
- target-journal selection;
- venue-specific formatting;
- authorship and CRediT;
- affiliation/funding/COI/acknowledgments;
- testbed credit and rights/licensing;
- final manuscript/source packaging;
- final proof QA;
- submission authorization.

A single monolithic PASS would make it difficult to identify which dependency failed and would mix reversible technical preparation with material author decisions and external submission authorization.

**Consortium consensus: retain P20 as an umbrella only; execute it through bounded sub-WPs.**

Completed historical WPs are not renumbered or rewritten.

## 5. Refactored publication-preparation lane

Weights below define the remaining lane from the post-P19 state through documented submission execution. Progress is awarded only after each acceptance gate passes.

| WP | Weight | Output | Acceptance gate | Dependency |
|---|---:|---|---|---|
| **P20A — Literature & Novelty Closure** | **15%** | submission-date related-work audit, Gaspar full-text assessment if accessible, comparator/novelty boundary lock, verified bibliography | current search completed; all material citations verified; no unsupported prior-art attribution; novelty wording remains inside P13/P17V envelope | P19 PASS |
| **P20B — Venue Qualification & Selection** | **15%** | ranked primary/backup venue matrix using official current guidance: scope/article type/indexing/APC/limits/artifact & supplement policy/format requirements/editorial fit | at least one defensible GO venue; kill reasons recorded; primary recommendation produced; material venue choice requires author validation before venue-specific lock | P20A PASS |
| **P20C — Authorship / Credits / Rights Lock** | **15%** | verified author list/order, CRediT, affiliation, funding/COI, acknowledgments, FIT IoT-LAB/POWDER credit/citations, copyright/license/permission boundary | every field verified or explicit N/A/TBD blocker; no invented author/funding/license/rights claim; author approves material authorship/rights decisions | P20B PASS |
| **P20D — Final Manuscript & Source Package Integration** | **25%** | final venue-shaped manuscript source, P18RC main figures, P19 supplement references/artifact links, bibliography, metadata, clean build package | clean reproducible manuscript build; zero internal WP/P7B reader-facing leakage; all figures/tables/citations resolve; scientific values and P13 claims unchanged; external package excludes cache/temp files including `__pycache__`/`.pyc` | P20C PASS |
| **P20E — Independent Submission-Readiness Validation** | **20%** | fresh red-team / independent validation of final PDF, source package, supplement, artifact, metadata, accessibility, privacy, and venue compliance | numerical/claim audit PASS; no critical/major production blocker; clean-room or isolated artifact checks PASS to the extent required by venue; privacy/metadata scan PASS; final proof visually inspected | P20D PASS |
| **P21 — Author Submission Authorization Packet** | **5%** | concise final decision packet showing venue, manuscript PDF, source/package identities, author/credit/rights declarations, costs, and remaining commitments | author explicitly approves the exact venue and exact final submission package; no external submission occurs inside P21 | P20E PASS |
| **P22 — Submission Execution & Receipt** | **5%** | portal submission, final uploaded-file verification, manuscript ID/receipt, canonical archival update | execute only after explicit P21 authorization; verify portal receipt and uploaded identities; archive submission evidence; no post-submit scientific rewrite silently applied | P21 explicit authorization |

**Total remaining-lane weight: 100%.**

## 6. Gate rules

### P20A — Literature & Novelty Closure

Must be venue-neutral. It may narrow novelty wording but may not change measured results or add a new empirical claim. Gaspar et al. 2026 must remain scope/bibliographic only unless full text is actually recovered and assessed.

### P20B — Venue Qualification & Selection

Must use current official venue guidance. Venue selection is a material author decision: the consortium produces the recommendation, but the target is not silently committed.

### P20C — Authorship / Credits / Rights Lock

No inferred coauthors, CRediT roles, funding source, license, copyright ownership, or permissions statement. All unresolved material fields block P20C.

### P20D — Final Manuscript & Source Package Integration

This is the only gate that may perform venue-specific manuscript/source-package transformation. Such transformations are production/editorial only unless a disclosed scientific conflict forces re-opening an earlier authority. The final external package must exclude temporary/compiled cache artifacts such as `__pycache__`, `.pyc`, editor backups, local credentials, and build residue.

### P20E — Independent Submission-Readiness Validation

The validation team must not treat the P20D builder's own QA as independent evidence. It rechecks numerical values, claim boundaries, artifacts, formatting, accessibility, privacy, references, and submission-file identities from the finished package.

### P21 — Author Authorization

P21 is an internal authorization gate, not submission. It must expose any APC/charges, declarations, license/copyright choices, data/code availability wording, and final author metadata before approval.

### P22 — External Submission

No portal submission, copyright acceptance, license selection, payment commitment, or external declaration may occur without explicit P21 author authorization.

## 7. Scientific change-control

None of P20A–P22 may silently alter:

- FIT/POWDER evidence roles;
- P13 claim wording envelope;
- numerical values, axes, aggregation, statistical interpretation, failure-domain semantics;
- B0 non-durable comparator boundary;
- E10 censor/upper-bound semantics;
- scored P7B historical state.

If a required venue/editorial transformation materially changes any of the above, stop and reopen the relevant scientific V&V authority instead of treating it as formatting.

## 8. Consortium consensus

- P18RC remains PASS: **12/12 roles support no reopening**.
- P19 scientific/artifact closure remains PASS: **12/12 roles support no scientific reopening**.
- P19 compiled-cache hygiene issue: **non-blocking now; mandatory removal before external final package**.
- original monolithic P20: **REFACTOR REQUIRED**.
- refactored P20A–P20E + P21 + P22 architecture: **CONSENSUS ACCEPTED**.
- next executable gate: **P20A only**.
- P20B–P22 are dependency-locked until predecessor gates pass.
- new experiment required: **NO**.
- new empirical claim required: **NO**.
- submission authorization: **NO**.

## 9. Stop state

`WP_ARCHITECTURE_REVIEW=PASS`

`P18RC_REOPEN=NO`

`P19_REOPEN_SCIENCE=NO`

`P19_PACKAGING_EXCEPTION=NON_BLOCKING_PYCACHE_REMOVE_BEFORE_EXTERNAL_PACKAGE`

`P20_MONOLITHIC_EXECUTION=REJECTED`

`P20_UMBRELLA=RETAINED`

`NEXT_EXECUTABLE=WP2_P20A_LITERATURE_AND_NOVELTY_CLOSURE`

`SUBMISSION_AUTHORIZED=NO`
