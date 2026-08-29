# WP2-P20E-R2 — Independent Elsevier Submission-Readiness Validation

Date: 2026-08-29
Status: **PASS / ZERO SCIENTIFIC BLOCKERS / ZERO PRODUCTION BLOCKERS / NO SUBMISSION**

Target: **Internet of Things (Elsevier)**
Production authority under test: **P20D-R2**

## Independence rule

This gate validates the exact P20D-R2 package as a fixed artifact. It does not rewrite science, tune claims, add experiments, alter figures, or optimize the survey after seeing the result.

## Exact artifact under test

Archive:
`WellPulse_P20D_R2_Elsevier_IoT_Submission_Package_2026-08-29.zip`

Drive ID:
`163sZVVq2qRQn8EPnZDniRLxgoOCY2lK7`

Expected/archive SHA-256:
`43d9cba4c14fcfc17d0c8d11e18ff3ee82ab3a3a8ee7b57e60db46634e025f89`

Drive raw read-back: **exact match / PASS**.

## 1. Build reproducibility

The packaged source was copied into a fresh temporary build root and compiled independently with `pdflatex`.

Result:

- packaged PDF pages: **16**;
- independent rebuild pages: **16**;
- packaged-versus-independent render comparison: **0 changed pages / 0.0% maximum changed pixels**;
- all PDF fonts embedded: PASS;
- visual page-by-page inspection: PASS.

The PDF binary hash is not required to be deterministic because PDF build metadata can differ; rendered content is exact.

## 2. Survey audit validation

Submission-facing main manuscript contains:

- section `Structured Literature Survey and Novelty Control`;
- seven search/comparator axes;
- explicit targeted novelty-audit scope;
- collision categories linked to claim consequences;
- synthesis table in main text;
- explicit aggregate audit counts.

Supplementary S1 CSV independently checked:

- rows: **17**;
- `WORDING NARROWING`: 9;
- `WORDING NARROWING - MATERIAL`: 1;
- `WORDING NARROWING - CONSERVATIVE`: 1;
- total wording-narrowing groups: **11**;
- `NO IMPACT`: **6**;
- scientific blockers: **0**.

These counts exactly match the main manuscript and P20A authority.

The manuscript does **not** call the targeted audit a PRISMA/systematic review/meta-analysis. PASS.

## 3. Literature / novelty boundary validation

Spot checks confirm the current manuscript preserves the P20A constraints around:

- MQTT persistence and persistent sessions;
- retransmission after disconnection;
- offline-first/store-and-forward prior art;
- application/downstream acknowledgment and receiver-confirmation prior art;
- robustness/stress/fault-testing prior art;
- real-testbed/repeatability prior art;
- receiver reconciliation as an evidence practice rather than historical firstness.

Material comparators Mohammed et al. 2026, E-MQTT, and Radwan et al. 2026 remain represented. Gaspar et al. remains bibliographic/scope-only for detailed attribution.

`SCIENTIFIC_BLOCKERS_FROM_LITERATURE=0`

## 4. Frozen numerical-claim spot checks

The submission-facing PDF/source preserve the frozen values:

- W1 `10,000/10,000` under tested FIT failure conditions;
- B0 `8,000/10,000` under C1/C2;
- repeated `+20` percentage-point bounded difference;
- W1 backlog drain `67.731246 s` and `67.870252 s`;
- 51/52 dB observations retained as experiment-specific;
- E10-B `6.063318 s` first publish and `6.609430 s` first ping;
- E10-C-B `29.247733 s` first ping and `29.248129 s` first publish;
- E10-D `<=10.908749 s` upper-bound semantics;
- E8 `40/60` unique delivery;
- E9 `60/60` control;
- no FIT/POWDER statistical pooling.

No generic MQTT-superiority, strongest-durable-client, universal-52-dB, deterministic-RF-recovery, field-validation, or historical-firstness claim was found.

## 5. Publication identity / declarations

- author name: **Ahmed Ayoub** — PASS;
- expanded publication-name variants: absent submission-facing — PASS;
- MSA affiliation: PASS;
- corresponding author/email: PASS;
- CRediT: PASS;
- Funding: PASS / no external research funding;
- Declaration of competing interest: PASS;
- FIT/POWDER acknowledgments: PASS;
- Data availability: PASS;
- Elsevier generative-AI declaration immediately before References: PASS.

Current Elsevier journal AI policy requires an AI-use disclosure on submission when generative AI is used in manuscript preparation and provides a dedicated declaration format. The package follows that structure.

## 6. Highlights / discovery controls

Five Highlights are present.

Character counts including bullet prefix:

1. 74 characters;
2. 73 characters;
3. 71 characters;
4. 70 characters;
5. 79 characters.

All are within Elsevier's current 85-character guidance.

The first Highlight deliberately exposes the literature-control contribution:

`Structured seven-axis survey bounds novelty across 17 comparator groups.`

## 7. Supplement / reproducibility validation

P19 reproducibility supplement was independently extracted and checked:

- isolated `python -I artifact_selfcheck.py`: **PASS**;
- `__pycache__` / `.pyc` files: **0**;
- scientific invariants and claim envelope: PASS;
- privacy/security sanitized packaging remains intact.

Survey S1 and P19 reproducibility supplement are separated so the literature audit remains readable while the full experimental atlas/code/evidence remains available.

## 8. Venue-scope consistency

Current official Elsevier journal description explicitly welcomes Full Research papers and Survey Papers, emphasizes IoT reliability, software engineering, testbeds and quality assurance, and states high priority on timely publication. The R2 manuscript remains a Full Research paper; the structured survey is evidence/novelty control within that paper, not a change of article type.

## 9. Independent verdict

- scientific blockers: **0**;
- production blockers: **0**;
- authorship/identity blockers: **0**;
- survey-audit contradictions: **0**;
- supplement/self-check blockers: **0**;
- external submission performed: **NO**.

`WP2_P20E_R2=PASS_INDEPENDENT_ELSEVIER_SUBMISSION_READINESS_VALIDATION`

`P21_R2_UNLOCKED=YES`

`SUBMISSION_AUTHORIZED=NO`
