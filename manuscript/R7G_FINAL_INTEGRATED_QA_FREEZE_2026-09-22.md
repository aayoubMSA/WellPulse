# WellPulse IEEE Revival — R7g Final Integrated Compile / Visual / Evidence QA Freeze

**Date:** 2026-09-22
**Status:** PASS
**Scientific authority:** R7f-R4 source commit `ef2902e545668516ad30e1cd95751aecad314281`
**R7g manuscript edits:** NONE

## 1. Final candidate source

`manuscript/revival_2026-09-22/WellPulse_Revival_R7fR4_EvidencePresentation_20260922.tex`

Accepted source SHA-256:
`14c29c0d693bc696ae042b291b0528ab68c62ebfdb91e7c4d461bce8f05756eb`

Accepted source Git blob:
`167355aa580fbcaf19a1cc306d6053feae7db1cd`

R7g performed QA only and did not alter this source.

## 2. Integrated scientific/evidence gate

R7g rechecked the complete manuscript against the R6 claim ceiling and all R7f repairs.

Passed:
- M0–M5 are retained as distinct observables/evidence authorities, not taxonomy novelty;
- PUBACK/M2 is not used as subscriber receipt/M3;
- exact historical M3 latency remains explicitly uninstrumented;
- the old approximately 68 s receiver-completion interpretation does not return;
- historical W1 gaps remain exactly 68.992, 69.466, 68.944, 68.785, 70.264, 68.852 s;
- campaign mean remains 69.217 s and range 68.785–70.264 s;
- C1 and C2 remain separated descriptively: means 69.134 s and 69.300 s;
- prospective R1/R2/R3 remain 75.208, 76.308, 74.798 s;
- all three prospective M2→M3 intervals remain UNRESOLVED;
- 0/3 positive and NOT_CONFIRMED_STOP remain explicit;
- no Stage B is implied or authorized;
- no prospective stale-arrival/causal witness is invented;
- historical/prospective FIT are not pooled;
- FIT/POWDER are not pooled;
- POWDER stale carryover remains a single bounded existence observation;
- no prevalence/frequency claim is made;
- architecture novelty remains killed;
- generic MQTT durability/freshness causality remains blocked.

`R7G_R6_CLAIM_CEILING=PASS`

## 3. Reproducibility and privacy gate

R7g re-ran the R7f-R3 sanitized supplement self-check and verified the frozen supplement blob authorities:
- supplement: `ca80b83b753eb8f5f1980ee5f91cfd6cc500d88c`;
- execution config: `bc4b6c85037c5571bc8187b5fd1d3d1fd644ba6c`;
- code manifest: `d07cd79d3d82fba750809cf000bc0087174c647a`;
- self-check: `05751a640931facd25483235d1b65ad9445f9b2a`.

The executed-code provenance discrepancy remains disclosed:
- pre-final amendment documented intended SQLite DELETE mode;
- executed frozen runner requests WAL;
- executed code remains reproduction authority;
- no scientific result is attributed to journal-mode choice.

Static and package privacy gates exclude credentials, SSH private keys, and private storage identifiers.

`R7G_SUPPLEMENT_SELFCHECK=PASS`
`R7G_PACKAGE_PRIVACY=PASS`

## 4. Reference integrity

Final bibliography contains 14 unique references and all 14 citation keys resolve.

Independent final DOI/retraction audit:
- DOI-bearing references checked: 13;
- matched: 13/13;
- mismatch: 0;
- ambiguous: 0;
- not found: 0;
- retracted: 0.

The remaining reference is the non-DOI OASIS MQTT Version 5.0 standard.

`R7G_REFERENCE_AUDIT=PASS`

## 5. Compile / PDF gate

Final accepted GitHub Actions run:
`35723521958` — SUCCESS.

Compile result:
- IEEEtran PDF generated successfully;
- pages: 10;
- page size: US Letter;
- undefined citations: 0;
- undefined references: 0;
- LaTeX errors: 0;
- undefined control sequences: 0;
- overfull boxes: 0;
- rendered-text smoke: PASS;
- all 10 pages rasterized successfully at 160 dpi.

R7g build hashes:
- TEX: `14c29c0d693bc696ae042b291b0528ab68c62ebfdb91e7c4d461bce8f05756eb`;
- regenerated PDF: `c980ec9b4e9c58a711e25084f842d28d4c5fd2ea6c40424f32b0844e0beb0a58`;
- final candidate TAR.GZ: `a7b2f7a2cfddbde260c3fd0afbc1bd79287fcf57e5d36a8208730c56ce158aa1`.

## 6. Final visual regression

The R7g regenerated PDF was compared page-by-page against the already accepted R7f-R4 PDF using 160-dpi raster comparison.

Result:
- pages in R7f-R4 PDF: 10;
- pages in R7g PDF: 10;
- changed pages: 0/10;
- pixel change: 0.0% on every page;
- maximum channel difference: 0 on every page.

The PDF byte hash differs because PDF metadata includes a new creation/modification timestamp; the rendered document is pixel-identical.

Manual visual review of all ten R7f-R4 pages had already confirmed:
- no clipping;
- no overlaps;
- no broken glyphs;
- no table overflow;
- readable black/white evidence figure;
- no visual M2-before-M3 implication.

`R7G_VISUAL_REGRESSION=PASS`

## 7. Final R7g QA artifact

GitHub Actions artifact:
- ID: `10691804387`;
- name: `wellpulse-r7g-final-qa-35723521958`;
- size: 6,255,311 bytes;
- SHA-256: `10678dfd3f9f7b631653f65ad76522cb56fec5f78c62d6d892227408fed17ab8`;
- retention: 30 days.

The artifact contains:
- exact final TEX;
- compiled 10-page PDF;
- final sanitized candidate TAR.GZ;
- package/file SHA-256 manifests;
- PDF metadata report;
- all ten rendered QA pages.

## 8. Durable preservation

Drive folder:
`P12_WellPulse / R7g_Final_Integrated_QA_2026-09-22`

Drive folder ID:
`139nBX6aVUjLrfIWKduCM-8Nupk-Fa2wi`

Drive package:
`WellPulse_R7g_Final_QA_35723521958.zip`

Drive file ID:
`1UcuVvqfd-1rsqqbT0Bn75d9nnjp7yB4u`

Drive read-back:
- size: 6,255,311 bytes;
- SHA-256: `10678dfd3f9f7b631653f65ad76522cb56fec5f78c62d6d892227408fed17ab8`;
- exact match to the GitHub Actions artifact digest.

`R7G_DURABLE_PRESERVATION=PASS`

## 9. Superseded R7g QA attempts

The earlier R7g failures were checker-only refinements; the scientific source was never modified:
- `35722343978`: wording mismatch in a frozen-text assertion;
- `35722433118`: case-sensitive reproducibility wording assertion;
- `35722594980`: Python escape handling for LaTeX `texttt` test string;
- `35722748523`: small-caps heading extraction artifact in `pdftotext`;
- `35723056833`: line-break/hyphenation artifact in rendered-text smoke;
- `35723328890`: IoT-LAB line-break/hyphenation artifact in rendered-text smoke.

All integrated scientific/static gates had already passed before the final render-smoke refinements. Final accepted run is `35723521958`.

## 10. R7 closure

R7a authority/map: PASS.
R7b revival source skeleton: PASS.
R7c Methods + Results reconstruction: PASS.
R7d full prose reconstruction: PASS.
R7e IEEE editorial/compliance engineering: PASS.
R7f hostile scientific review: PASS; major repair package subsequently CLOSED.
R7f-R1 SOTA/claim boundary: PASS.
R7f-R2 contribution/evidence framing: PASS.
R7f-R3 reproducibility surface: PASS.
R7f-R4 evidence presentation: PASS.
R7g final integrated compile/visual/evidence QA: PASS.

## 11. Gate

`R7G_FINAL_INTEGRATED_QA=PASS`
`R7G_VISUAL_REGRESSION=PASS`
`R7G_REFERENCE_AUDIT=PASS`
`R7G_DURABLE_PRESERVATION=PASS`
`R7_RECONSTRUCTION_AND_HOSTILE_QA=CLOSED`
`R8_ENTRY=UNLOCKED`

Next:
R8 — venue requalification and submission decision. R8 must account for the remaining venue-fit risk: the strongest empirical result is an implementation-specific serialized-replay consequence rather than a new recovery mechanism. No venue decision is made in R7g.