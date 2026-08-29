# WP2-P18R — Generator / Release Receipt

Date: 2026-08-29  
Status: **REGISTERED / DURABLE RELEASE / SOURCE HASHED**

## Generator

Primary generator inside the registered release package:

`src/wellpulse_scifig.py`

SHA-256:

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

## Durable release

File:

`WellPulse_P18R_Scientific_Figure_Engineering_Release_2026-08-29.zip`

Drive parent:

`P12_WellPulse`

Drive ID:

`1alitbv9479Mq9URhXIBHkQql7zuuA51o`

ZIP SHA-256:

`5586091bc518cc541c3c9b75e9a0c965913877cd6bf83d1644fa6f05264e1083`

## Final main figure PDF hashes

- Figure 1 — `179b3201b63a5910473885e2005d2ba2bfd55c9fe888f0d1ed42980d21a09ea1`
- Figure 2 — `a38e321ec4a6b51ede1fff89601432852ac0c9e0e56d32ac880724a3b9ad0eff`
- Figure 3 — `bc23a25a53beb13396b056b22bdd93af62ec7c7f91b3d81199028dd4496887ee`
- Figure 4 — `a2be6684ddd339f6b60c1406cb9673a2d14a2c6c038cdb8a0ec748b6b93f5d0c`

## V&V

The release contains:
- source-data receipt;
- figure manifest;
- QA report;
- PDF/SVG/PNG outputs;
- reproducible generator;
- demo mirror of the exact canonical scientific CSV values for independent package execution;
- consortium decision;
- FRS;
- lifecycle record;
- attribution/rights notice.

Final PDFs were rendered independently for visual verification after the successful code build.

`P18R_RELEASE_REGISTERED=YES`

`P18R_AI_ASSET_DEPENDENCY=NONE`

`P18R_FIGURE_ENGINE_VV=PASS`
