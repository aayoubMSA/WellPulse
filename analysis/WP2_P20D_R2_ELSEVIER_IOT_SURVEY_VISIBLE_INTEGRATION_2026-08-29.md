# WP2-P20D-R2 — Elsevier Internet of Things Manuscript + Survey-Visible Integration

Date: 2026-08-29
Status: **PASS / ELSEVIER PACKAGE BUILT / SURVEY EFFORT VISIBLE / NO SUBMISSION**

## Trigger

P20B-R6 switched the first route to **Internet of Things (Elsevier)** because the author elevated desk/editorial triage speed as a material objective. The author also required that the manuscript properly expose the substantial literature-survey effort rather than compress it into a few related-work paragraphs.

No experiment, empirical result, P13/P17V claim, novelty boundary or scientific conclusion was reopened.

## Venue-facing manuscript change

The manuscript is now built with an Elsevier `elsarticle` preprint layout. The expanded format removes the IEEE eight-page compression pressure and allows the literature work to remain visible.

Main manuscript:

`WellPulse_Elsevier_IoT_P20D_R2_SubmissionDraft.pdf`

- pages: **16**
- approximate manuscript PDF word count: **4,682**
- publication name: **Ahmed Ayoub**
- target journal: **Internet of Things (Elsevier)**
- route: **Subscription / non-OA initial route**

## Survey visibility upgrade

The prior IEEE version compressed P20A into a short Related Work section. R2 exposes the work explicitly through:

1. a dedicated main-text section: **Structured Literature Survey and Novelty Control**;
2. explicit survey purpose and scope;
3. seven predefined search/comparator axes;
4. transparent selection logic distinguishing scholarly prior art from deployed-platform technical evidence;
5. explicit three-class collision logic: `NO IMPACT / WORDING NARROWING / SCIENTIFIC BLOCKER`;
6. quantitative audit outcome: **17 retained source/axis groups; 11 wording-narrowing; 6 no-impact; 0 scientific blockers**;
7. a two-page main-text synthesis table mapping each survey axis to representative evidence, established prior art and exact manuscript consequence;
8. explicit discussion explaining that the survey actively constrains empirical interpretation rather than serving as decorative background;
9. a separate **Supplementary Material S1** preserving the complete 17-group source-by-source novelty/collision matrix in PDF and CSV form.

The work is accurately labelled a **targeted submission-date novelty audit**, not a systematic review/meta-analysis. This avoids overstating the survey methodology while making its real effort and scientific control role visible.

## Added survey evidence families

The visible synthesis now covers:

- MQTT client/broker persistence and persistent sessions;
- retransmission after disconnection;
- offline-first continuity and store-and-forward;
- downstream acknowledgment and subscriber/receiver confirmation;
- MQTT robustness, stress testing and flow control;
- real testbeds, repeatability and standardized physical assessment;
- receiver-side reconciliation/provenance as an evidence practice.

Current deployed-practice documentation from AWS IoT Core and Azure IoT Operations is identified as technical capability evidence only; it is not used to establish historical scientific priority.

## Elsevier-specific declarations

R2 replaces IEEE-specific front/end matter with Elsevier-compatible sections:

- corresponding author and MSA affiliation;
- CRediT authorship contribution statement;
- Funding;
- Declaration of competing interest;
- Acknowledgments;
- Data availability paragraph;
- separate `Declaration of generative AI and AI-assisted technologies in the manuscript preparation process` consistent with current Elsevier journal policy.

The AI statement explicitly says generative AI was not used to generate or alter experimental measurements, quantitative results or scientific figures.

## Highlights

A separate `highlights.txt` contains five concise claims, led by:

- structured seven-axis survey bounds novelty across 17 comparator groups;
- FIT separates durable record survival from communication-path recovery;
- W1 delivers 100% versus 80% for non-durable B0 under tested outages;
- POWDER shows transition variability and mechanism-specific recovery;
- receiver reconciliation preserves adverse evidence semantics.

## Scientific invariants rechecked

Submission-facing source/PDF retain:

- 10,000/10,000 W1 final completeness under the tested FIT failures;
- 8,000/10,000 B0 final completeness under C1/C2;
- repeated +20 percentage-point bounded W1-B0 difference;
- W1 backlog-drain means `67.731246 s` and `67.870252 s`;
- POWDER 51/52 dB observations as experiment-specific, not universal;
- E10-B `6.063318 s` first publish and `6.609430 s` first ping;
- E10-C-B `29.247733 s` first ping and `29.248129 s` first publish;
- E10-D `<=10.908749 s` upper-bound semantics;
- E8 `40/60` unique delivery and E9 `60/60` control;
- FIT/POWDER non-pooling;
- non-durable B0 comparator boundary;
- no generic MQTT superiority or historical firstness.

## Validation

- publication-name consistency: PASS;
- old IEEE target language in submission-facing manuscript: absent;
- survey row count: 17 PASS;
- wording-narrowing count: 11 PASS;
- no-impact count: 6 PASS;
- scientific-blocker count: 0 PASS;
- Elsevier AI declaration: PASS;
- funding/COI/CRediT/data availability: PASS;
- P19 isolated self-check: PASS;
- no `__pycache__`/`.pyc`: PASS;
- main PDF visual inspection: PASS;
- survey supplement visual inspection: PASS;
- fonts embedded: PASS.

## Durable package

Archive:
`WellPulse_P20D_R2_Elsevier_IoT_Submission_Package_2026-08-29.zip`

Drive ID:
`163sZVVq2qRQn8EPnZDniRLxgoOCY2lK7`

Archive size:
`2,132,191 bytes`

Archive SHA-256:
`43d9cba4c14fcfc17d0c8d11e18ff3ee82ab3a3a8ee7b57e60db46634e025f89`

Drive raw read-back SHA-256: **exact match / PASS**.

Main PDF SHA-256:
`46953e6f8c579faf040d8f7cbf342e200ec603b205832abbd73d3c3434b8f2a0`

Source TeX SHA-256:
`281e0f62e1412e2f0d45a74682a5e858097cf34843acbfb19935998cc0e92b6e`

Survey S1 PDF SHA-256:
`a098f1f366ff1d152b7e27524f454393620b93f31df563417749a28f86804017`

P19 reproducibility supplement SHA-256:
`99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`

## Control

`WP2_P20D_R2=PASS_ELSEVIER_IOT_SURVEY_VISIBLE_INTEGRATION`

`SURVEY_EFFORT_VISIBLE_IN_MAIN_PAPER=YES`

`SURVEY_FULL_AUDIT_SUPPLEMENTED=YES`

`SCIENTIFIC_REOPENING=NO`

`SUBMISSION_AUTHORIZED=NO`
