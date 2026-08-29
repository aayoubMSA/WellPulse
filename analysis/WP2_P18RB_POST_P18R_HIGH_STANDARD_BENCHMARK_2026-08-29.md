# WP2-P18RB — Post-P18R High-Standard Figure / File Benchmark

Date: 2026-08-29  
Status: **CONDITIONAL PASS / SCIENCE PASS / PRODUCTION NORMALIZATION REQUIRED**

## 1. Mandate

Benchmark the current P18R main-display system after the deterministic Figure-1 hotfix against high-standard, venue-neutral scientific-artwork and reproducibility criteria. Do not alter scientific claims or raw evidence.

Benchmark anchors were rechecked on 2026-08-29 against current official guidance from:
- IEEE Author Center graphics resolution/size/file-formatting/accessibility guidance;
- Elsevier artwork/file/font guidance;
- Nature Research Figure Guide and Nature formatting/image-integrity guidance;
- ACM-style artifact-evaluation / reproducibility criteria.

These anchors are used as a strict cross-publisher benchmark; final venue-specific normalization remains a P20 task after journal selection.

## 2. Current authority tested

### Figure 1

Current authority is the deterministic F1 hotfix:

`analysis/wp2_p18r_generate_f1_hotfix.py`

QA:

`manuscript/WP2_P18R_F1_HOTFIX_QA_2026-08-29.md`

Final F1 PDF SHA-256:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

### Figures 2–4

Current P18R release remains the authority for:
- Figure 2 — FIT record survival and recovery cost;
- Figure 3 — POWDER transition and repeatability;
- Figure 4 — failure-domain and recovery semantics.

## 3. Benchmark verdict by dimension

| Dimension | Verdict | Notes |
|---|---|---|
| Claim/display fidelity | PASS | No display exceeds the P13/P17V claim envelope. |
| FIT/POWDER inferential separation | PASS | No pooled quantitative axis/effect. |
| Run/cycle visibility | PASS | FIT runs and POWDER repeated cycles remain visible. |
| Percentage-axis integrity | PASS | Percentage panels include zero; no zoom exaggeration. |
| Threshold discipline | PASS | No fitted or universal 52 dB threshold. |
| Recovery semantics | PASS | Exact/censored/upper-bound status retained. |
| Figure 1 scientific topology | PASS | Local SENT/PUBACK separated from receiver reconciliation. |
| Figure 1 visual QA | PASS | No known clipping/overlap/crossing after hotfix. |
| Vector masters | PASS | PDF/SVG retained; raster fallback exists. |
| Figure sizing | PASS | Full-width figures remain within 7.16 in / 182 mm class. |
| Accessibility redundancy | PASS WITH PATCH | F3 uses marker + line-style redundancy; F2 needs encoding cleanup. |
| Semantic visual encoding | PATCH REQUIRED | F2 panels B/C inherit Matplotlib default color-cycle changes that do not encode a declared variable consistently. |
| Cross-publisher font family | PATCH REQUIRED | Matplotlib figures use DejaVu Sans; IEEE/Elsevier/Nature prefer Arial/Helvetica-class fonts. |
| Cross-publisher line/grid style | PATCH REQUIRED | Nature-neutral portability favors no background gridlines and <=1 pt strokes; current F2/F3 include gridlines and some >1 pt lines. |
| Figure-4 readability | PASS WITH MINOR POLISH | Semantically strong and legible; visually table-like but appropriate for mechanism/endpoint semantics. |
| Caption completeness | PASS / F1 | F1 caption frozen; F2–F4 captions exist in P18R release. |
| Accessibility alt text | PATCH REQUIRED | Final P18R release needs explicit alt text for all four main figures. |
| File-level attribution metadata | PATCH REQUIRED | F1 embeds author/institution metadata; F2–F4 rely mainly on package-level attribution and should be normalized. |
| Bitwise deterministic PDF rebuild | PASS / F1; NOT FROZEN / F2–F4 | F1 two-build PDF hash equality demonstrated. Whole main set should receive fixed metadata during final production normalization. |
| Artifact exercisability | P19 GATE | Generator + demo data exist; blank-environment/reviewer package belongs to P19. |

## 4. Strongest current properties

1. **Scientific richness is now structural, not decorative.** The main displays connect architecture, effect, recovery cost, transition behavior, repeated-cycle variability, and failure-domain semantics.
2. **Figure 1 is now publication-credible in provenance and semantics.** It is code-generated and source-validated; the AI visual is not canonical.
3. **F2 separates final completeness, reconnect, and durable catch-up**, preventing the common error of calling every interval “recovery latency.”
4. **F3 is scientifically dense and honest:** ascending/descending response plus independent E3 cycle variability without fitted threshold/probability.
5. **F4 preserves negative/censored/upper-bound evidence** instead of hiding it.

## 5. Mandatory production-normalization patch before P19

Create bounded patch **WP2-P18RC — MAIN-FIGURE PRODUCTION NORMALIZATION**.

Mandatory scope only:

### RC-01 — F2 semantic encoding cleanup

- architecture identity must be consistent across panels;
- eliminate accidental default color-cycle meaning;
- condition remains encoded by x-position;
- keep raw points and mean marks;
- no scientific aggregation change.

### RC-02 — venue-neutral typography family

Use an embedded Helvetica/Arial-compatible sans-serif family across F1–F4. Final point-size normalization remains venue-specific in P20 because current IEEE and Nature size preferences are not identical.

### RC-03 — line/grid normalization

- remove nonessential background gridlines from quantitative panels;
- cap ordinary figure strokes at `<=1 pt` for Nature-neutral compatibility;
- retain axis lines/ticks/units.

### RC-04 — accessibility package

Freeze explicit alt text for F1–F4 and verify grayscale interpretation.

### RC-05 — file metadata / rights normalization

Embed fixed author/affiliation/rights metadata where format supports it, while retaining package-level attribution/rights notice. Do not invent a public license.

### RC-06 — deterministic rebuild receipt

Run the final production-normalized main set twice and record hashes/visual-equivalence results. Exact byte equality is desirable where supported; scientific equivalence is mandatory.

## 6. What is deliberately deferred to P19/P20

### P19

- reviewer-facing supplement;
- sanitized artifact;
- blank-environment exercisability;
- runtime/dependency documentation;
- claim/result → script → output map;
- public/private evidence boundary.

### P20

- final target-journal figure point sizes/naming/placement;
- target-journal accepted file extensions;
- manuscript source package;
- final author/CRediT/funding/COI/permissions/license statements;
- final literature/venue verification.

## 7. Acceptance state

Scientific/display benchmark blockers: `0`.

Production normalization blockers before P19 freeze: `5 classes` (RC-01…RC-06, with RC-02 point-size portion deferred to P20).

No new experiment: `NO`.

No new empirical claim: `NO`.

`WP2_P18RB=CONDITIONAL_PASS_SCIENCE_PASS_PRODUCTION_NORMALIZATION_REQUIRED`

`P18RB_NEXT=WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION`

P19 must not be frozen until P18RC passes.
