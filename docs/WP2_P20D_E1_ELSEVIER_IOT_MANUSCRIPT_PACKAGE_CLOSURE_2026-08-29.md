# WP2-P20D-E1 — Elsevier Internet of Things Manuscript / Package Closure

Date: 2026-08-29
Status: **PASS / ELSEVIER ROUTE PRODUCTION COMPLETE / NO SUBMISSION**

## Main manuscript

Target: **Internet of Things (Elsevier)**

Article type: **Full Research paper**

Publication name: **Ahmed Ayoub**

Submission-facing PDF:
`WellPulse_Internet_of_Things_SubmissionDraft_2026-08-29.pdf`

- preprint build: **16 pages**;
- SHA-256: `5cc8b2c3829ff51d95b1953c3b6c434967427a752606b46fe563ecb0b66e7fae`;
- exact author identity check: PASS;
- visual QA across all pages: PASS;
- no clipping/overlap/broken glyphs observed.

Source:
`source/wellpulse_elsevier_iot_p20d.tex`

SHA-256:
`76e6b23a311481dd1139c34ae0986ff4c50bec199cc26a5b4b90e7c76302ede3`

## Literature-survey visibility change

A dedicated main-paper section now reports the existing P20A work as:

**Structured Comparator Survey and Novelty Boundary**

It makes the following project effort explicit:

- 7 search axes;
- 17 source/axis groups;
- 11 wording-narrowing groups;
- 6 no-impact groups;
- 0 scientific blockers.

A multi-page comparator table appears immediately inside that section and records prior-art layer, representative evidence, collision class and mandatory claim consequence.

This is deliberately described as a **structured submission-date comparator survey**, not a systematic review/PRISMA contribution. The manuscript remains a Full Research paper.

The survey explicitly shows that prior work narrowed novelty rather than being ignored. It prevents firstness claims for persistent MQTT state, buffering/retransmission, store-and-forward, offline-first recovery, downstream acknowledgment, end-to-end subscriber confirmation, generic failure testing and use of real testbeds.

## Scientific invariants

The route conversion changes no frozen science:

- B0 remains non-durable;
- FIT failure cells remain 8,000/10,000 B0 versus 10,000/10,000 W1;
- +20 percentage-point run-level final-completeness difference remains bounded to the tested B0 comparison;
- W1 backlog-drain means remain approximately 67.7–67.9 s;
- POWDER remains separate path/failure-domain characterization;
- 52 dB remains experiment-specific, not universal;
- E10-A remains censored;
- E10-D remains an upper bound;
- FIT and POWDER are not statistically pooled;
- generic MQTT superiority remains prohibited.

## Declarations

Submission-facing paper includes:

- Ahmed Ayoub only;
- MSA affiliation and institutional email;
- no external research funding;
- competing-interest declaration;
- CRediT statement;
- FIT IoT-LAB and POWDER acknowledgment;
- generative-AI writing-process declaration.

## Reproducibility / supplement

P19 submission-safe supplement remains included unchanged as scientific/reviewer evidence authority.

## Durable archive

Archive:
`WellPulse_Internet_of_Things_Submission_Package_2026-08-29.zip`

Drive ID:
`1s3BydyBafI4nCza-wdOXrem_U0P-PO6B`

Size:
`2,374,123 bytes`

SHA-256:
`8931994e142ba355687e41b48a4abded5adf0e5e419b8e88103ae4786513249c`

Drive raw read-back: exact size/hash PASS.

## Independent rebuild

A clean independent LaTeX rebuild produced 16 pages. Render comparison against the packaged submission PDF returned:

- changed pages: **0/16**;
- rendered-pixel difference: **0.0% on every page**.

## Stop state

`WP2_P20D_E1=PASS`

`P20E_ELSEVIER=PASS_INDEPENDENT_REBUILD_AND_VISUAL_QA`

`P21_IEEE_PACKET=SUPERSEDED_BY_ROUTE_SWITCH`

`SUBMISSION_AUTHORIZED=NO`
