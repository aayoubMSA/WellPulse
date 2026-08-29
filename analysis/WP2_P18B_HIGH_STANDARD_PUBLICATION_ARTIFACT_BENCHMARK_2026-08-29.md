# WP2-P18B — High-Standard Publication / Artwork / Artifact Benchmark

Date: 2026-08-29  
Status: **BENCHMARK COMPLETE / REMEDIATION GATES FROZEN**

## 1. Purpose

Benchmark the current WellPulse manuscript, figures, supplementary-material strategy, provenance files, and reproducibility assets against high-end cross-publisher expectations rather than a single target journal template.

This is a readiness benchmark, not a scientific-quality score and not an acceptance-probability estimate.

## 2. External benchmark anchors

The benchmark uses current official guidance from:

1. **IEEE Author Center — graphics**: vector-first artwork; high-resolution raster fallback; standard one-column (3.5 in) and two-column (7.16 in) widths; embedded fonts; approximately 9–10 pt full-size figure text; redundant marker/line encodings for color-vision accessibility.
2. **Elsevier artwork guidance**: EPS/PDF for vector drawings with embedded fonts; raster minima of 300 dpi for halftones, 500 dpi for mixed artwork, and 1000 dpi for bitmapped line art; minimal text inside figures; captions supplied separately.
3. **Nature Portfolio reporting/data/code availability**: explicit data-availability and code-availability statements; central custom code made available to editors/reviewers; restrictions disclosed; best practice is a persistent DOI-minting repository for released code/data.
4. **ACM artifact-evaluation practice**: artifacts should be documented, consistent with the paper, complete to the extent possible, exercisable, and ideally reusable; availability requires a stable archival location/identifier and license; reproducibility packages should identify results/claims and provide scripts for result figures/tables.

## 3. Benchmark result — P18 display system

### 3.1 Scientific visual integrity — PASS / VERY STRONG

- claim-to-display mapping is explicit;
- FIT and POWDER are never plotted as one pooled quantitative population;
- percentage figures use full 0–100% scales after P18 redraw;
- raw run/cycle observations remain visible;
- no fabricated confidence intervals;
- no universal attenuation threshold line;
- exact/censored/upper-bound timing semantics remain separated;
- main Figure 1 explicitly prevents POWDER architecture-effect interpretation.

Coverage score: **20/20**.

### 3.2 Artwork engineering — PASS / STRONG

- PDF/SVG vector masters: PASS;
- 600-dpi PNG fallback: PASS;
- PDF fonts embedded/subset: PASS;
- Figure 1 width = 7.16 in: PASS for IEEE two-column reference;
- Figures 2–4 width = 3.5 in: PASS for IEEE one-column reference;
- figures generated from scripts rather than hand-edited artwork: PASS;
- separate caption/alt-text authority: PASS.

Residual venue-dependent item:
- current font is embedded DejaVu Sans; IEEE lists Helvetica/Times New Roman/Arial/Cambria/Symbol as recommended families. Do not change now without a selected venue; apply final venue typography in P20.

Coverage score: **14/15**.

### 3.3 Accessibility / information design — PASS / STRONG

- line/marker shape redundancy: PASS;
- grayscale interpretable without relying on color alone: PASS by design;
- no 3-D/chartjunk/gradient encodings: PASS;
- no long paragraphs inside quantitative data regions: PASS;
- caption and alt text available for all four main figures: PASS;
- full percentage axes remove visual-exaggeration risk: PASS.

Residual item:
- final venue/template integration should recheck minimum rendered type size and contrast after scaling.

Coverage score: **9/10**.

**P18 display benchmark subtotal: 43/45 = 95.6%.**

## 4. Benchmark result — full publication package

### 4.1 Scientific and claim governance — PASS / EXCEPTIONALLY STRONG

- P13 claim envelope frozen;
- P16 adversarial QA;
- P17 consortium revision;
- P17V independent validation;
- no unsupported empirical expansion;
- exact failure-domain taxonomy;
- negative/censored/anomalous evidence preserved.

Coverage score: **20/20**.

### 4.2 Provenance and reproducible generation — PASS / STRONG

- raw binary authorities frozen separately from derived files;
- SHA-256 anchors and Drive authorities preserved;
- receiver-side reconciliation is canonical;
- P11 reconstruction code exists;
- P18 display generators committed;
- final display-pack hash receipt exists.

Still missing for gold-standard external artifact evaluation:
- fresh/blank-environment execution of the sanitized package;
- machine-readable environment/dependency lock;
- expected runtime/resource documentation;
- one command/path to recreate all manuscript quantitative displays from releasable derived data.

Coverage score: **13/15**.

### 4.3 Supplement / artifact availability — OPEN / P19 REQUIRED

Current strengths:
- detailed 37-page experiment dossier exists;
- E0–E11 atlas, validity/anomaly registers and reconstructed CSVs exist;
- public release boundaries are already identified.

Missing before a high-end reproducibility claim:
- reviewer-facing concise supplement derived from the dossier;
- sanitized artifact free of credentials/private platform captures;
- artifact README/inventory;
- explicit software/hardware environment and dependency versions;
- LICENSE or explicit reuse terms after legal/venue review;
- stable archival repository/DOI for released artifact;
- blank-environment functional test;
- claim/result reproduction map and scripts for every public quantitative figure/table.

Coverage score: **7/15**.

### 4.4 Manuscript/source-file engineering — OPEN / P20 REQUIRED

Current strengths:
- P17 manuscript is evidence-bounded and consortium validated;
- affiliation and infrastructure acknowledgments are controlled;
- P18 main display set is frozen.

Missing:
- target-journal source template and clean LaTeX manuscript;
- venue-specific figure naming/typography/placement checks;
- final reference normalization;
- final data-availability and code-availability statements;
- final author list/order and CRediT roles;
- funding/conflict declarations;
- venue-specific copyright/license terms;
- final proof against source/figures/supplement/artifact.

Coverage score: **7/10**.

### 4.5 Rights / credits / metadata — STRONG BUT OPEN

Current:
- Dr. Ahmed Elsayed Ayoub identity and MSA affiliation are controlled;
- FIT IoT-LAB and POWDER acknowledgments are required;
- no invented coauthors/funding/licenses.

Open:
- final coauthor/contributor validation;
- CRediT roles;
- funding declaration;
- selected venue copyright/license;
- public artifact license.

Coverage score: **8/10**.

## 5. Overall benchmark

- **P18 main-display system:** `95.6/100 equivalent` — publication-grade, with only venue-dependent typography/format normalization remaining.
- **Whole submission package:** `84/100 readiness-equivalent` — scientifically strong but intentionally incomplete because P19 and P20 remain open.

These percentages are checklist-coverage indicators, not scientific-effect or acceptance probabilities.

## 6. Required remediation to reach gold-standard package

### P19 — Supplement + sanitized artifact

Target a package capable of satisfying an ACM-style `Artifacts Evaluated — Functional` bar and approaching `Reusable`:

1. concise reviewer supplement, not the raw 37-page dossier pasted into the article;
2. sanitized derived datasets supporting every public number;
3. committed analysis and figure scripts;
4. README with inventory, environment, installation and one-command reproduction path;
5. dependency/runtime lock;
6. expected runtimes/resources;
7. claim/result → script → output map;
8. blank-environment execution and recorded receipt;
9. explicit exclusions/restrictions for private raw captures;
10. license decision only after rights/legal/venue review;
11. archive in DOI-capable repository when release is authorized.

### P20 — Venue / manuscript / rights normalization

1. select target journal and retrieve current author instructions;
2. convert manuscript to venue LaTeX/source package;
3. normalize final artwork typeface/naming to venue requirements;
4. verify every figure at final rendered size;
5. final literature/full-text closure;
6. final author/CRediT/funding/COI/acknowledgment audit;
7. Data Availability + Code Availability statements;
8. copyright/license/permissions audit;
9. final source↔PDF↔supplement↔artifact consistency QA;
10. explicit author authorization before submission.

## 7. Frozen benchmark verdict

`P18B_DISPLAY_BENCHMARK=PASS_95_6_PERCENT_CHECKLIST_COVERAGE`

`P18B_FULL_PACKAGE_READINESS=84_PERCENT_CHECKLIST_COVERAGE`

`P18B_SCIENTIFIC_BLOCKERS=0`

`P18B_P19_REQUIRED=YES`

`P18B_P20_REQUIRED=YES`

`P18B_SUBMISSION_READY=NO`

The correct next action is P19, not additional experimentation.
