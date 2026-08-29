# WP2-P20D — Final IEEE Manuscript & Source Package Integration

Date: 2026-08-29
Status: **PASS / IEEE AUTHOR BUILD = 6 PAGES / DRIVE READ-BACK PASS / NO SUBMISSION**

## Target

- Journal: **IEEE Internet of Things Journal**
- Route: **Traditional / non-OA**
- Canonical publication identity: **Ahmed Ayoub** (global authority: LL-048)

## Current IEEE controls reverified

Current IoT-J author guidance states that mandatory page charges are USD 175 per published page beyond the first eight pages and that submission signifies acceptance of that requirement. IEEE Author Center guidance supports IEEE journal templates and separate supplementary-material uploads. IEEE policy requires disclosure when AI-generated article content is used, identifying the system, affected sections, and level of use.

Therefore P20D used the official IEEEtran journal format as the page-count simulation basis and preserved the author-controlled no-payment/no-submission gates.

## Main manuscript build

Production source: `wellpulse_ieee_iotj_p20d.tex` in the archived P20D package.

Result:

- IEEEtran journal class;
- US Letter;
- 10 pt;
- two-column;
- **6 pages**;
- all four P18RC main figures retained;
- PDF preflight: openable, unencrypted, non-scanned;
- visual inspection: no clipping/overlap/black glyph failures detected.

The 6-page author build provides two pages of author-build headroom relative to the current 8-page no-overlength threshold. Final IEEE production pagination can still change, so P21/P22 must preserve the explicit no-unapproved-payment control.

## P20A integration

Added/accounted for:

1. Mohammed et al. 2026, DOI `10.48084/etasr.16945`;
2. Im and Lim 2023 E-MQTT, DOI `10.3390/app132212419`;
3. Radwan et al. 2026, DOI `10.1038/s41598-026-66865-8`.

Novelty wording was narrowed accordingly. The manuscript does not claim firstness for application persistence, downstream/end-to-end acknowledgment, generic outage recovery, subscriber confirmation, or decoupling of data reliability from network availability.

Gaspar et al. remains bibliographic/scope-only unless full text is recovered; no unsupported detailed attribution was introduced.

## P20C integration

Inserted:

- author and corresponding author: **Ahmed Ayoub**;
- MSA affiliation;
- FIT IoT-LAB acknowledgment and citation;
- POWDER acknowledgment and citation;
- no-external-funding statement;
- current no-competing-interest statement;
- CRediT contribution statement;
- IEEE generative-AI disclosure identifying OpenAI ChatGPT, the affected manuscript sections, and editorial/language-assistance level.

## Publication-identity normalization

The P18RC/P19 internal artifacts predated LL-048 and carried an expanded legacy name in metadata/source comments. P20D did **not** alter the frozen authorities. Instead it created publication-safe derivatives using `Ahmed Ayoub` only.

For F1-F4:

- displayed scientific content unchanged;
- only publication metadata normalized;
- render comparison at 160 dpi: **0 changed pages, 0.0% changed pixels for every figure**;
- original P18RC PDF hashes remain the scientific-figure authorities and are recorded in `FIGURE_DERIVATIVE_PROVENANCE.csv`.

No prohibited legacy publication-name variant remains in the text/source files of the P20D external package.

## Reviewer supplement

The P19 sanitized reviewer artifact was externalized for P20D:

- all `__pycache__` directories removed;
- all `.pyc` files removed;
- publication-facing identity metadata/text normalized to Ahmed Ayoub;
- derivative manifest regenerated;
- isolated `python -I artifact_selfcheck.py` result: **PASS**.

Scientific invariants and the P13 claim envelope therefore remain intact.

## Scientific-preservation checks

Preserved:

- B0 is explicitly non-durable;
- no generic MQTT superiority;
- FIT run/replicate remains the scientific unit;
- 10,000 messages/run are not treated as independent n;
- FIT and POWDER are not statistically pooled;
- POWDER remains controlled reference characterization;
- 52 dB remains experiment-specific rather than universal;
- E10-A remains censored with no scalar recovery latency;
- E10-D remains an upper bound;
- field/rural/pump/hydraulic/groundwater/agronomic/process validation remains prohibited;
- adverse/anomalous evidence remains retained in the supplement.

## Hashes and durable archive

Submission-draft PDF SHA-256:
`a3737379e4688ef64b4b95ba3350ad29ae5e90563a5a45f384f92b50e2d729ca`

TeX SHA-256:
`249b73d004728cb39cd5e34621985b3b8c5794185824951ecdb549a7db52fd01`

Submission-safe P19 supplement ZIP SHA-256:
`a8dc2e789fed93c5f18ebc17cbf7ae2f66514dfdc157770d5fd5abded3d7fac5`

Full P20D package:
`WellPulse_P20D_IEEE_Submission_Package_2026-08-29.zip`

Package SHA-256:
`3377b6c13c53f47594d75c50419bceaee87e81e4450f000dcf01054b78706f0b`

Drive ID:
`19K3gB9TY4znMZmGHw_DQHZnM9ee_eMSx`

Drive read-back size: `3,597,127 bytes`.

Drive raw read-back SHA-256 matched the local archive exactly: **PASS**.

## Gate

`WP2_P20D=PASS_FINAL_IEEE_MANUSCRIPT_SOURCE_PACKAGE_INTEGRATION`

`IEEE_AUTHOR_BUILD_PAGES=6`

`P20E_UNLOCKED=YES`

`OVERLENGTH_PAYMENT_AUTHORIZED=NO`

`COPYRIGHT_ACCEPTANCE_AUTHORIZED=NO`

`SUBMISSION_AUTHORIZED=NO`
