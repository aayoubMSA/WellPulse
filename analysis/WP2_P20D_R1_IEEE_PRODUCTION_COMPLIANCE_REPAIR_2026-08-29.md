# WP2-P20D-R1 — IEEE Production-Compliance Repair

Date: 2026-08-29
Status: **PASS / BOUNDED PRODUCTION-ONLY REPAIR / SCIENCE UNCHANGED**

## Trigger

Independent P20E red-team validation of the exact P20D package identified four production/compliance defects. None affected scientific claims, numerical results, figures, novelty boundaries, authorship, or the venue decision.

The repair lane was therefore reopened only as P20D-R1.

## Repairs

1. **IEEE first-footnote compliance**
   - explicitly identifies `Ahmed Ayoub` as corresponding author;
   - places the no-external-research-funding statement in the first footnote.

2. **Affiliation completeness**
   - adds official MSA postal code `12451` to the affiliation;
   - official MSA pages list the 6th October campus postal code as 12451.

3. **Acknowledgment heading / AI-disclosure placement**
   - replaces `Acknowledgment and Author Statements` with IEEE-standard singular `Acknowledgment`;
   - substantive OpenAI ChatGPT disclosure remains inside that section and still identifies the system, affected manuscript sections, and level/responsibility of use.

4. **Supplementary-material README compliance**
   - adds `supplement/P19_submission/SUPPLEMENT_README.txt` containing IEEE-requested description, size, platform, environment, component map, setup instructions, run instructions, expected output, contact information, and rights/privacy note;
   - outer package README stale `supplement/P19_clean` path corrected to `supplement/P19_submission`.

## Scientific non-change proof

The TeX diff from P20D to P20D-R1 contains only:

- corresponding-author / funding first-footnote insertion;
- postal-code insertion;
- acknowledgment-heading normalization;
- removal of the duplicate no-funding sentence from the acknowledgment.

No body-science, result, table, figure, reference, or novelty-boundary line changed.

P13/P17V/P20A invariants remain frozen.

## R1 build result

- IEEEtran build: **6 pages**.
- Page size: US Letter.
- Abstract: **221 words**, inside IoT-J's current 150–250-word requirement.
- Main figures: F1–F4 unchanged.
- Independent source rebuild: **6 pages / 0 changed rendered pages / 0.0% changed pixels** relative to the packaged R1 PDF.
- Fonts embedded: **PASS**.
- P19 isolated `python -I artifact_selfcheck.py`: **PASS**.
- root package manifest: **66 entries / 0 errors**.
- root SHA list: **67 entries / 0 errors**.
- nested P19 manifest: **53 entries / 0 errors**.
- `__pycache__` / `.pyc`: **0**.
- expanded publication-name variants: **0** in submission-facing text corpus.
- exact private IPv4 values in reviewer package: **0 detected**.

## R1 durable package

Archive: `WellPulse_P20D_R1_IEEE_Submission_Package_2026-08-29.zip`

Drive ID: `1j61flpHqrVlR_c-Hu1ueUjl5p2RQwhGG`

Size: `3,601,271 bytes`

Archive SHA-256: `73b46d0b19cfd74689bdc10efb27c71a5460ca1c9ab6843503155a87696eb73c`

Drive raw read-back SHA-256: **exact match / PASS**.

R1 manuscript PDF SHA-256: `95917105f9d03fce155b9cc2a579d2e0e6f567a30557f87f82382db193597fa1`

R1 TeX SHA-256: `0e0c64ba0552f2e71e8a00e4cc29a35da908b7f0996a5a94db34e36d2ef644ef`

R1 supplementary ZIP SHA-256: `99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`

## Stop state

`WP2_P20D_R1=PASS_BOUNDED_IEEE_PRODUCTION_COMPLIANCE_REPAIR`

`SCIENTIFIC_REOPENING=NO`

`PAGE_COUNT=6`

`OVERLENGTH_PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_ACCEPTANCE_AUTHORIZED=NO`

`SUBMISSION_AUTHORIZED=NO`
