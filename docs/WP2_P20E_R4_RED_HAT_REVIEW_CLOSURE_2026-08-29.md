# WP2-P20E-R4 — Red-Hat Review Closure

Date: 2026-08-29
Status: **PASS AFTER FINITE PRODUCTION REPAIR / P21-R4 UNLOCKED / NO SUBMISSION**

Target: **Internet of Things (Elsevier)**  
Article type: **Full Research paper**  
Current manuscript authority: **R4-R1**

## Closure result

The from-scratch R4 manuscript underwent a fresh independent red-hat. Three submission-production defects were found and repaired without changing frozen science:

1. abstract reduced from **269 to 250 words**;
2. keywords reduced from **8 to 7**;
3. Highlights rewritten to remove project/testbed acronyms and jargon; five highlights remain within Elsevier's 85-character limit and an editable `highlights.docx` is included.

The generative-AI declaration heading was also normalized to current Elsevier wording. No experiment, numerical result, figure, reference set, claim class, statistical unit or inferential role changed.

## Current exact authority

Main manuscript:
`WellPulse_Consortium_Rewrite_R4R1_SubmissionDraft.pdf`

- pages: **21**;
- references: **32 / 32 cited**;
- abstract: **250 words**;
- keywords: **7**;
- PDF SHA-256: `6ebd6a07a7ed512cb2a53fb75f778536a2fad86b5d0de690e1ddbcd3d685c6ac`;
- TeX SHA-256: `ac85fac31af5d203ffbb04d7f191ee283e02e55fe4529ac6b8f4558359d85dcb`;
- publication-facing author: **Ahmed Ayoub**;
- all fonts embedded;
- PDF preflight warnings: **0**.

Submission-preparation archive:
`WellPulse_CONSORTIUM_REWRITE_R4R1_Package_2026-08-29.zip`

- size: **2,228,500 bytes**;
- SHA-256: `290b89fff927f2e4bfeeade3031844be2c3f94333584496ff04718ce58cc6b67`;
- manifest rows: **16**;
- manifest mismatches: **0**;
- ZIP integrity: **PASS**.

Supplement S1:
- 32-row literature/novelty audit;
- SHA-256: `e9bcda5b7ec5b3993b51eb69a4da6a52d15bfa2da9e14774d65db88cb65721d8`.

Supplement S2:
- sanitized reproducibility artifact;
- SHA-256: `99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`;
- no `__pycache__` / `.pyc`;
- isolated `python -I artifact_selfcheck.py`: **PASS**.

Editable Highlights:
- `highlights.docx`;
- SHA-256: `3248fe4ad6be9fe23503517b10783c38a3be4c3a9536f207f326b6667ff5a640`.

## Independent red-hat evidence

- FIT reconstruction independently recomputed and matched all frozen completeness, missing-count, reconnect-mean and backlog-drain values;
- POWDER exact/censored/upper-bound timing semantics matched frozen authority;
- run-level statistical discipline preserved;
- no FIT+POWDER statistical pooling;
- B0 remains explicitly non-durable and no strongest-durable-MQTT superiority is claimed;
- 32/32 bibliography entries cited; unresolved citation keys = 0;
- literature audit remains targeted/claim-bounding, not systematic/PRISMA/meta-analysis;
- no affirmative forbidden field/agronomic/industrial validation claim;
- no legacy expanded publication-name variant;
- no private RFC1918 addresses in the main manuscript;
- four main figures remain byte-identical to the R4 scientific figure inputs;
- deterministic independent rebuild = **21 pages / 0 changed pages / 0.0% changed pixels**.

## Residual reviewer risks — disclosed, not blockers

1. a reviewer may request a matched durable MQTT comparator;
2. a reviewer may request additional FIT run-level replicates;
3. the 32-source audit is targeted rather than systematic/exhaustive;
4. detailed Gaspar et al. method/result overlap is not asserted;
5. the 21-page survey-visible preprint is intentional and no verified journal page-limit blocker has been identified.

## Gate state

`WP2_P20E_R4=PASS_AFTER_FINITE_PRODUCTION_REPAIR`

`CURRENT_MANUSCRIPT_AUTHORITY=R4R1`

`SCIENTIFIC_BLOCKERS=0`

`PRODUCTION_BLOCKERS=0`

`PUBLICATION_LANE_PROGRESS=90_OF_100`

`P21_R4_UNLOCKED=YES`

`P21_R4=NEXT_NOT_STARTED`

`P22_LOCKED=YES`

`PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`

`SUBMISSION_AUTHORIZED=NO`
