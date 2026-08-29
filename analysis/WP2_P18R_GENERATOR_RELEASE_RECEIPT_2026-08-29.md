# WP2-P18R — Generator / Release Receipt

Date: 2026-08-29  
Status: **REGISTERED / DURABLE RELEASE / SOURCE HASHED / F1 HOTFIX APPLIED**

## Generator

Primary generator inside the registered P18R release package:

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
- canonical `src/wellpulse/records.py` / `src/wellpulse/store.py` semantics for the architecture panel.

## Durable P18R release

File:

`WellPulse_P18R_Scientific_Figure_Engineering_Release_2026-08-29.zip`

Drive parent:

`P12_WellPulse`

Drive ID:

`1alitbv9479Mq9URhXIBHkQql7zuuA51o`

ZIP SHA-256:

`5586091bc518cc541c3c9b75e9a0c965913877cd6bf83d1644fa6f05264e1083`

## Historical P18R main-figure PDF hashes

The original P18R package remains preserved as an immutable historical release. Its Figure 1 is superseded for publication-facing use by the deterministic F1 hotfix below.

- historical Figure 1 — `179b3201b63a5910473885e2005d2ba2bfd55c9fe888f0d1ed42980d21a09ea1` — **SUPERSEDED**;
- Figure 2 — `a38e321ec4a6b51ede1fff89601432852ac0c9e0e56d32ac880724a3b9ad0eff`;
- Figure 3 — `bc23a25a53beb13396b056b22bdd93af62ec7c7f91b3d81199028dd4496887ee`;
- Figure 4 — `a2be6684ddd339f6b60c1406cb9673a2d14a2c6c038cdb8a0ec748b6b93f5d0c`.

## F1 deterministic hotfix — current Figure-1 authority

Trigger: the author rejected text slipping/overlap in the original Figure 1 and rejected an AI-generated redesign as a canonical scientific asset.

Canonical hotfix generator:

`analysis/wp2_p18r_generate_f1_hotfix.py`

Generator SHA-256:

`201897de563448037798678a73c998bd8b7a01f74bb4096995587f13d6667d48`

QA/caption authority:

`manuscript/WP2_P18R_F1_HOTFIX_QA_2026-08-29.md`

Current final Figure 1 PDF SHA-256:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

Scientific corrections:
- sender-local `SENT` occurs after QoS1 PUBACK and is not shown as a consequence of receiver reconciliation;
- receiver-side unique-ID evidence and generated-versus-received reconciliation are an independent evidence path for reported final completeness;
- internal `IC-xx` identifiers are removed from the publication-facing artwork;
- FIT design includes `3 runs/cell` and `10,000 records/run`;
- POWDER is represented as the full `E0–E11` controlled characterization campaign;
- synthesis wording is reader-facing and preserves explicit non-pooling.

Reproducibility/QA:
- no AI-generated asset dependency;
- source semantics are asserted before render;
- two consecutive builds produced the identical PDF SHA-256;
- PDF/SVG vector masters and 600-dpi PNG fallback;
- exact width `7.16 in`;
- embedded PDF fonts PASS;
- known overlap/clipping/arrow-text-crossing defects `0` after final visual QA.

The AI-generated visual prototype is **reference only** and is not canonical artwork.

## V&V

The P18R release and F1 hotfix collectively provide:
- source-data/source-code semantic receipts;
- figure manifests and hashes;
- QA reports;
- PDF/SVG/PNG outputs;
- reproducible generators;
- consortium/FRS/lifecycle records;
- attribution/rights notices.

`P18R_RELEASE_REGISTERED=YES`

`P18R_AI_ASSET_DEPENDENCY=NONE`

`P18R_FIGURE_ENGINE_VV=PASS`

`P18R_F1_HOTFIX=PASS_DETERMINISTIC_F1_ACCEPTED`

`P18R_F1_BITWISE_PDF_REBUILD=PASS`

`P18R_F1_CURRENT_PDF_SHA256=4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

## Return to project line

The F1 hotfix is a bounded correction and does not change raw evidence, P13 claims, P17/P17V manuscript conclusions, or submission authorization.

After this hotfix the project returns to the main path:

**P18RB — post-P18R high-standard benchmark**, then **P19 — reviewer-facing supplement + sanitized artifact** if P18RB passes.
