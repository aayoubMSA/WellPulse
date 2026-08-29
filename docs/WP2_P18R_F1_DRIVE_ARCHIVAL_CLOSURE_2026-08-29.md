# WP2-P18R-F1 — Drive Archival and Provenance Closure

Date: 2026-08-29  
Status: **PASS / DURABLE ARCHIVE VERIFIED / PROVENANCE REPAIRED**

## Purpose

Close the bounded storage/handover gap for the deterministic P18R Figure-1 hotfix without changing science, raw data, the P13 claim envelope, or manuscript conclusions.

## Final durable Drive archive

File: `WellPulse_P18R_F1_Hotfix_Final_2026-08-29.zip`  
Drive parent: `P12_WellPulse` / folder ID `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`  
Drive file ID: `12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M`  
Drive URL: `https://drive.google.com/file/d/12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M/view`  
ZIP SHA-256: `e9d5a54b24506b879a748b5a06b39699e6f6ec1ed31093491c27b2be7d7e6e1d`

The uploaded object was fetched back from Drive and its SHA-256 was rechecked against the local archival package: **MATCH / PASS**.

## Archive contents

- final Figure 1 PDF vector master;
- final Figure 1 SVG vector master;
- 600-dpi PNG fallback;
- exact current canonical generator `analysis/wp2_p18r_generate_f1_hotfix.py`;
- archive manifest;
- source-authority/rebuild receipt;
- provenance-repair note;
- attribution and rights notice.

The bundle intentionally does **not** duplicate or replace the canonical semantic implementation sources. Their authority remains GitHub `main`.

## Canonical generator identity

Path: `analysis/wp2_p18r_generate_f1_hotfix.py`  
Git blob SHA-1: `bf344808414b78d9b0c688140e9de9a755d9a1e7`  
Current exact SHA-256: `3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`

Canonical semantic-source blobs verified during closure:

- `src/wellpulse/powder_w1.py` — `f68866d19cf68dbd0ea0645a5eee449bdc1248d3`;
- `src/wellpulse/receiver.py` — `98c1e08ba660a2377d0bfdd58bbf32230797087c`;
- `src/wellpulse/reconcile.py` — `d274c24812d32966dee023875c0aad791649c372`;
- `src/wellpulse/records.py` — `b3c2a83946c64e1abe61698c6da11ab32834d1e5`;
- `src/wellpulse/store.py` — `da71be72760d4d138b3d37bba8787f5fd7ef3aee`.

## Exact rebuild validation

Frozen/current Figure-1 PDF SHA-256:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

Archival rebuild from the current generator produced the same PDF SHA-256 exactly.

`P18R_F1_PDF_HASH_MATCH=PASS`

## Provenance repair

The earlier F1 QA/release receipt recorded generator SHA-256:

`201897de563448037798678a73c998bd8b7a01f74bb4096995587f13d6667d48`

That value no longer matched the exact bytes of the current GitHub generator. The current generator is the Git blob/SHA-256 identified above and reproduces the already-frozen PDF bit-for-bit. Therefore the discrepancy is classified as **source-hash/provenance drift**, not a scientific or visual-content change.

This closure supersedes the stale generator-hash field wherever the earlier value appears.

## Rights / release boundary

Author/affiliation/rights metadata is retained in the archive. This is an internal research archive; it grants no public license. Public or reviewer-facing release still requires the later sanitization/release gate.

## Project-line consequence

P18RB is already canonically complete with verdict:

`WP2_P18RB=CONDITIONAL_PASS_SCIENCE_PASS_PRODUCTION_NORMALIZATION_REQUIRED`

Exact next gate:

`NEXT=WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION`

P19 must not be frozen until P18RC passes.

`DRIVE_ARCHIVE=PASS`

`DRIVE_READBACK_HASH=PASS`

`GITHUB_CONTROL_RECORD=PASS`

`PROVENANCE_DRIFT=REPAIRED`

`SCIENTIFIC_CONTENT_CHANGED=NO`

`SUBMISSION_AUTHORIZED=NO`
