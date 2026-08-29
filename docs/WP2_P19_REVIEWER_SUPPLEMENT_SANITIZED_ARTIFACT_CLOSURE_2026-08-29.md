# WP2-P19 — Reviewer-Facing Supplement + Sanitized Artifact Closure

Date: 2026-08-29  
Status: **PASS / REVIEWER PACKAGE BUILT / PRIVACY-SANITIZED / DRIVE READ-BACK VERIFIED**

## Scope
P19 packages reviewer-facing experiment detail and an exercisable sanitized artifact. It does not change experiments, raw evidence, P13 claims, P17/P17V conclusions, P18RC figures, historical P7B state, authorship/credits, licensing, venue choice, or submission authorization.

## Reviewer supplement
Included:
- FIT design matrix, full 18-cell completeness display, and recovery-cost display;
- POWDER campaign map and E0–E11 atlas;
- recovery-mechanism comparison;
- run-validity map;
- traceability-chain figure;
- sanitized validity/anomaly register preserving negative, censored, duplicate, missing-artifact, setup-artifact, and one-sided-evidence cases.

E11 sanitization: exact private RFC1918 session addresses were replaced by the evidence-neutral label `session address changed`. The fact of address transition and the one-sided-collector limitation are retained.

## Sanitized artifact
Included:
- P11 FIT reconstructed run CSV;
- P11 POWDER derived metrics CSV;
- P14 E10 recovery timing CSV;
- P13 nine-claim CSV;
- production-normalized P18RC main-figure PDFs + alt text;
- sanitized/reference P11 analysis helper;
- P18RC quantitative figure generator/post-processing source;
- `artifact_selfcheck.py` using only the Python standard library;
- quantitative F2–F4 rebuild wrapper;
- claim/result → script → output map;
- dependency list;
- privacy/security review;
- package manifest and hashes.

Private raw FIT/POWDER archives, credential-bearing captures, unclassified screenshots, tokens/secrets, and files requiring testbed credentials are intentionally excluded.

## Exercisability / QA
- Standard-library artifact self-check: **PASS**.
- Self-check verifies 18 FIT cells, 10,000 records/cell, C1/C2 80% vs 100% run-level outcomes, E1R4 52 dB values, E3 52 dB MQTT 25/55/60%, E10-A censoring, E10-D upper-bound semantics, and 9/9 P13 claim status.
- Sanitized derived-data quantitative rebuild F2–F4: **PASS** in the current scientific-Python/Graphviz/Inkscape environment.
- Reviewer-PDF privacy text scan: no password/passwd/API-key/private-key/token/secret/email-address pattern; exact E11 private IPv4 values removed from the reviewer package.
- No FIT+POWDER statistical pooling introduced.
- No new empirical claim introduced.

## Durable archive
File: `WellPulse_P19_Reviewer_Supplement_Sanitized_Artifact_2026-08-29.zip`  
Drive parent: `P12_WellPulse` / `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`  
Drive ID: `1t5S_L-S0hfmyMPLdXh8Fd-jGBOH8SCkl`  
ZIP SHA-256: `5a9ed4fa197ea5c3aa43447fabf16d7928aeabe58722e16af63afe25bc7cfdc7`  
Drive read-back SHA-256: exact match / **PASS**.

## Authority / release boundary
Raw frozen archives remain the primary measurement authorities. P9 remains the POWDER validity/anomaly/trace authority; P11 the reconstructed-value authority; P13 the claim authority; P17/P17V the manuscript scientific baseline; P18RC the production main-display authority.

This package is reviewer-facing and sanitized but **does not grant a public license**. Final public-release rights, authorship/order, CRediT, funding/COI, acknowledgments, FIT/POWDER credits, literature/venue checks, and publisher-specific source-package requirements remain P20 gates.

## Closure
`WP2_P19=PASS_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`  
`P19_PRIVACY_SECURITY_REVIEW=PASS`  
`P19_STDLIB_SELFCHECK=PASS`  
`P19_QUANTITATIVE_REBUILD=PASS`  
`P19_DRIVE_ARCHIVE=PASS`  
`P19_DRIVE_READBACK_HASH=PASS`  
`CURRENT_SCIENTIFIC_BLOCKERS=0`  
`NEW_EXPERIMENT_REQUIRED=NO`  
`SCIENTIFIC_CONTENT_CHANGED=NO`  
`SUBMISSION_AUTHORIZED=NO`  
`NEXT=WP2_P20_FINAL_LITERATURE_VENUE_SOURCE_PACKAGE_CREDITS_RIGHTS_NORMALIZATION`
