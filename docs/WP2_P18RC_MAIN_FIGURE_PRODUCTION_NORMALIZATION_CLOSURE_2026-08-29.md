# WP2-P18RC — Main-Figure Production Normalization Closure

Date: 2026-08-29  
Status: **PASS / PRODUCTION NORMALIZATION COMPLETE / DRIVE READ-BACK VERIFIED**

## Scope
P18RC executed only the finite evidence-neutral production fixes required by P18RB. No experiment, P13 claim, P17/P17V conclusion, historical P7B state, scientific value, axis, aggregation, failure-domain semantic, or inferential boundary was reopened.

## Result
- RC-01 F2 semantic encoding cleanup: PASS. B0=open circle; W1=filled square consistently across relevant panels; condition remains x-position; all run-level points and mean marks retained.
- RC-02 typography: PASS. F1–F3 embed Liberation Sans; F4 embeds Arimo. Both are Arial-compatible venue-neutral sans families.
- RC-03 grid/line cleanup: PASS. Nonessential quantitative grids removed; ordinary Matplotlib strokes <=1 pt; structural F4 table borders retained.
- RC-04 accessibility: PASS. Explicit alt text frozen for F1–F4; grayscale/non-color-only interpretation PASS.
- RC-05 metadata/attribution: PASS. Fixed author/project metadata normalized across PDF/SVG/PNG where supported. No public license or unverified authorship/funding/rights claim invented.
- RC-06 deterministic rebuild: PASS. Two independent builds yielded identical SHA-256 for all 12 final PDF/SVG/PNG assets after deterministic metadata normalization.

## Current production-normalized PDF authorities
- F1: `7d7feb075731475747282cf0dd0081ec6afb1bc45c17bd16c754063ac83237cb`
- F2: `73b96a2b8c1fa2a4c15b3bd15b0065f77a2863dcacb84d8c3f2d7d0b57cef508`
- F3: `faccbef11762df7c293728992e59ac9b17e4b455e4d2023dcddeb50f41e5e9b8`
- F4: `87d2c703e4308477b3d89c5d0a9594a7380f2e0c8350d5d74721f779785a1b38`

F1 scientific/topological authority remains the deterministic P18R F1 hotfix; P18RC changes only typography/metadata production properties.

## Source/data identities
Canonical scientific inputs remain unchanged:
- FIT reconstructed CSV Git blob: `3e2eac3c6752d986489a507bc410c21467d99c60`
- POWDER derived metrics CSV Git blob: `970082e8a5e517dfedd634e282447639420b5f4d`
- recovery timing CSV Git blob: `3e42524d0339e5c2ada208a73508eb4ef94f98f2`
- current pre-RC F1 generator authority: `analysis/wp2_p18r_generate_f1_hotfix.py`, blob `bf344808414b78d9b0c688140e9de9a755d9a1e7`, SHA-256 `3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`.

The P18RC archive contains the exact production-normalization generator/post-processing sources used for the normalized release.

## Durable archive
File: `WellPulse_P18RC_Main_Figure_Production_Normalization_2026-08-29.zip`  
Drive parent: `P12_WellPulse` / `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`  
Drive ID: `1rdFq7ktppFBUp54UoeS5AP3kukDiU9sW`  
ZIP SHA-256: `97f0fd1e4c41bb67f6da70056935b60a1627695e082ea8d38eff657bce1d02a8`  
Drive read-back SHA-256: exact match / PASS.

## Scientific invariants
`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`  
`P13_STATISTICAL_POOLING=NONE`  
`CURRENT_SCIENTIFIC_BLOCKERS=0`  
`NEW_EXPERIMENT_REQUIRED=NO`  
`SCIENTIFIC_CONTENT_CHANGED=NO`  
`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`  
`SUBMISSION_AUTHORIZED=NO`

## Closure
`WP2_P18RC=PASS_MAIN_FIGURE_PRODUCTION_NORMALIZATION`  
`P18RC_DRIVE_ARCHIVE=PASS`  
`P18RC_DRIVE_READBACK_HASH=PASS`  
`P18RC_DETERMINISTIC_12_OF_12=PASS`  
`NEXT=WP2_P19_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`
