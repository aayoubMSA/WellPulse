# WP2-P18R — Generator / Release Receipt

Date: 2026-08-29  
Status: **REGISTERED / DURABLE RELEASE / F1 HOTFIX ARCHIVED / P18RB COMPLETE / PROVENANCE REPAIRED**

## Generator

Primary generator inside the historical registered P18R release package:

`src/wellpulse_scifig.py`

Historical release-generator SHA-256:

`5a313546fd88b6e06d7d3c473bb6742e214723287bdd37a9b84cf26faadf87f6`

Execution model:

```text
canonical CSVs -> invariant assertions -> deterministic rendering -> PDF/SVG/PNG -> QA -> manifest
```

The generator consumes no AI-generated image asset.

## Canonical scientific inputs

- `analysis/WP2_P11_FIT_RECONSTRUCTED_RUNS_2026-08-29.csv`
- `analysis/WP2_P11_POWDER_DERIVED_METRICS_2026-08-29.csv`
- `analysis/WP2_P14_TABLE3_POWDER_RECOVERY_TIMING_2026-08-29.csv`
- canonical WellPulse source semantics under `src/wellpulse/`.

## Durable historical P18R release

File: `WellPulse_P18R_Scientific_Figure_Engineering_Release_2026-08-29.zip`  
Drive parent: `P12_WellPulse`  
Drive ID: `1alitbv9479Mq9URhXIBHkQql7zuuA51o`  
ZIP SHA-256: `5586091bc518cc541c3c9b75e9a0c965913877cd6bf83d1644fa6f05264e1083`

The original P18R package remains preserved as an immutable historical release. Its Figure 1 is superseded for publication-facing use by the deterministic F1 hotfix.

Historical/main-set PDF hashes:

- historical Figure 1 — `179b3201b63a5910473885e2005d2ba2bfd55c9fe888f0d1ed42980d21a09ea1` — **SUPERSEDED**;
- Figure 2 — `a38e321ec4a6b51ede1fff89601432852ac0c9e0e56d32ac880724a3b9ad0eff`;
- Figure 3 — `bc23a25a53beb13396b056b22bdd93af62ec7c7f91b3d81199028dd4496887ee`;
- Figure 4 — `a2be6684ddd339f6b60c1406cb9673a2d14a2c6c038cdb8a0ec748b6b93f5d0c`.

## F1 deterministic hotfix — current Figure-1 authority

Canonical hotfix generator:

`analysis/wp2_p18r_generate_f1_hotfix.py`

Current Git blob SHA-1:

`bf344808414b78d9b0c688140e9de9a755d9a1e7`

Current exact generator SHA-256:

`3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`

The previously recorded generator SHA-256 `201897de563448037798678a73c998bd8b7a01f74bb4096995587f13d6667d48` is retained only as a historical pre-closure receipt value and is **superseded for current source identity**.

QA/caption authority:

`manuscript/WP2_P18R_F1_HOTFIX_QA_2026-08-29.md`

Current final Figure 1 PDF SHA-256:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

Scientific corrections remain frozen:

- sender-local `SENT` occurs after QoS1 PUBACK and is not shown as a consequence of receiver reconciliation;
- receiver-side unique-ID evidence and generated-versus-received reconciliation are an independent evidence path for reported final completeness;
- internal `IC-xx` identifiers are removed from publication-facing artwork;
- FIT design includes `3 runs/cell` and `10,000 records/run`;
- POWDER is represented as the full `E0–E11` controlled characterization campaign;
- synthesis wording is reader-facing and preserves explicit non-pooling.

Reproducibility/QA:

- no AI-generated asset dependency;
- source semantics asserted before render;
- final PDF/SVG vector masters plus 600-dpi PNG fallback;
- exact width `7.16 in`;
- embedded PDF fonts PASS;
- known overlap/clipping/arrow-text-crossing defects `0` after final visual QA.

## F1 durable Drive archive — storage closure

Canonical archival bundle:

`WellPulse_P18R_F1_Hotfix_Final_2026-08-29.zip`

Drive file ID:

`12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M`

Drive URL:

`https://drive.google.com/file/d/12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M/view`

ZIP SHA-256:

`e9d5a54b24506b879a748b5a06b39699e6f6ec1ed31093491c27b2be7d7e6e1d`

The uploaded Drive object was fetched back and re-hashed. Read-back SHA-256 equals the local archival-package SHA-256.

The archive contains the final F1 PDF/SVG/PNG, exact current generator, manifest, source-authority receipt, provenance-repair note, and attribution/rights notice. Canonical semantic implementation sources remain GitHub authorities and are not replaced by archive copies.

Independent archival rebuild using the current generator reproduced the frozen F1 PDF SHA-256 exactly:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

Therefore the generator-hash discrepancy was provenance drift only; no scientific or visual-content change occurred.

Canonical closure receipt:

`docs/WP2_P18R_F1_DRIVE_ARCHIVAL_CLOSURE_2026-08-29.md`

## V&V

`P18R_RELEASE_REGISTERED=YES`

`P18R_AI_ASSET_DEPENDENCY=NONE`

`P18R_FIGURE_ENGINE_VV=PASS`

`P18R_F1_HOTFIX=PASS_DETERMINISTIC_F1_ACCEPTED`

`P18R_F1_BITWISE_PDF_REBUILD=PASS`

`P18R_F1_CURRENT_PDF_SHA256=4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

`P18R_F1_CURRENT_GENERATOR_SHA256=3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`

`P18R_F1_DRIVE_ARCHIVE=PASS`

`PROVENANCE_DRIFT=REPAIRED`

## P18RB post-P18R high-standard benchmark

Canonical benchmark:

`analysis/WP2_P18RB_POST_P18R_HIGH_STANDARD_BENCHMARK_2026-08-29.md`

Verdict:

**CONDITIONAL PASS / SCIENCE PASS / PRODUCTION NORMALIZATION REQUIRED**.

Scientific/display blockers: `0`.

Required finite production-normalization patch before P19:

**WP2-P18RC — MAIN-FIGURE PRODUCTION NORMALIZATION**

Required classes:

- F2 semantic encoding cleanup;
- Helvetica/Arial-compatible venue-neutral font-family normalization;
- nonessential gridline / >1 pt line-weight normalization;
- explicit alt text for all four main figures;
- F2–F4 file-level attribution/rights metadata normalization;
- final deterministic/rebuild receipt for the normalized set.

No science, raw data, P13 claim or experimental validity change is authorized by this benchmark.

`WP2_P18RB=CONDITIONAL_PASS_SCIENCE_PASS_PRODUCTION_NORMALIZATION_REQUIRED`

## Return to project line

Current exact next bounded gate:

**P18RC — main-figure production normalization**.

P19 must not be frozen until P18RC passes.

After P18RC PASS, proceed directly to **P19 — reviewer-facing supplement + sanitized artifact**.

`SCIENTIFIC_CONTENT_CHANGED=NO`

`SUBMISSION_AUTHORIZED=NO`
