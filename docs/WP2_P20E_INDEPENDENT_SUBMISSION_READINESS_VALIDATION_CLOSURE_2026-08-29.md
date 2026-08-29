# WP2-P20E — Independent Submission-Readiness Validation Closure

Date: 2026-08-29
Status: **PASS / P21 UNLOCKED / NO SUBMISSION**

Authority:
`analysis/WP2_P20E_INDEPENDENT_SUBMISSION_READINESS_VALIDATION_2026-08-29.md`

## Validated package

Current submission-readiness authority:
`WellPulse_P20D_R1_IEEE_Submission_Package_2026-08-29.zip`

- Drive ID: `1j61flpHqrVlR_c-Hu1ueUjl5p2RQwhGG`
- Size: `3,601,271 bytes`
- Archive SHA-256: `73b46d0b19cfd74689bdc10efb27c71a5460ca1c9ab6843503155a87696eb73c`
- Drive raw read-back: **exact hash match / PASS**
- Manuscript PDF SHA-256: `95917105f9d03fce155b9cc2a579d2e0e6f567a30557f87f82382db193597fa1`
- IEEEtran author build: **6 pages**
- Abstract: **221 words**

## Independent validation result

The exact P20D-R1 package was independently extracted, rebuilt and inspected.

PASS controls include:

- independent TeX rebuild = 6 pages;
- rebuild-vs-packaged-PDF visual diff = **0 changed pages / 0.0% pixels**;
- all fonts embedded;
- F1-F4 visually legible and unchanged in scientific content;
- root manifest = 66 entries / 0 errors;
- root SHA list = 67 entries / 0 errors;
- nested P19 manifest = 53 entries / 0 errors;
- isolated P19 scientific self-check = PASS;
- no `__pycache__` or `.pyc` files;
- no expanded publication-name variant in submission-facing content;
- no detected private IPv4 address or exposed credential value in reviewer-facing material;
- key FIT and POWDER numerical claims independently recomputed and matched frozen authorities;
- P20A novelty boundaries/current comparator references preserved;
- no forbidden generic MQTT superiority, universal 52 dB, pooled inference, P7B-success, or unsupported field-validation claim;
- corresponding author, MSA affiliation/postal code, funding, COI, FIT/POWDER acknowledgments, CRediT and IEEE AI disclosure are present;
- supplementary-material README satisfies the current IEEE collection-description fields.

## P20D-R1 repair history

The first P20E pass returned four production-only defects to a bounded P20D-R1 lane:

1. corresponding-author/funding first-footnote placement;
2. MSA postal code `12451`;
3. IEEE-standard singular `Acknowledgment` heading while retaining the substantive AI disclosure;
4. complete supplementary-material README plus stale path correction.

The repair changed no scientific body/result/reference/figure/novelty line. P20E rerun then passed.

## Residual P21 authorization controls

These are not P20E defects. They must be surfaced to the author before any submission action:

1. verify the exact ORCID linked to **Ahmed Ayoub** in the submission account;
2. explicitly confirm the manuscript is not under active consideration elsewhere;
3. keep the selected route **Traditional / non-OA** unless the author explicitly changes it;
4. explicitly acknowledge the current IoT-J mandatory overlength condition: submission signifies acceptance of the journal's page-charge rule if the final published article exceeds eight pages, even though the validated author build is six pages;
5. map the main manuscript and supplementary files to their separate portal upload roles;
6. keep IEEE copyright-form acceptance as a separate downstream author-controlled action.

## Closure state

`WP2_P20E=PASS_INDEPENDENT_SUBMISSION_READINESS_VALIDATION`

`PUBLICATION_LANE_PROGRESS=90_OF_100`

`SCIENTIFIC_BLOCKERS=0`

`PRODUCTION_BLOCKERS=0`

`P21_UNLOCKED=YES`

`P22_LOCKED=YES`

`OVERLENGTH_PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_ACCEPTANCE_AUTHORIZED=NO`

`SUBMISSION_AUTHORIZED=NO`
