# WP2-P14 — Publication Tables & Figures

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **PASS / COMPLETE**

## 1. Scope

P14 converts only P13-approved evidence into publication-ready quantitative displays. No manuscript prose, venue selection, new experiment, scored-P7B reinterpretation, or cross-platform pooled statistic is introduced.

Source authorities:

- `analysis/WP2_P11_FIT_RECONSTRUCTED_RUNS_2026-08-29.csv`
- `analysis/WP2_P11_POWDER_DERIVED_METRICS_2026-08-29.csv`
- `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
- P9 trace/validity/anomaly authorities for POWDER timing semantics.

## 2. Figure-design standard

The frozen figure policy is publication-grade and journal-agnostic:

- vector-first source: SVG;
- submission vector: PDF with embedded TrueType/Type-42 fonts;
- raster fallback: 600-dpi PNG;
- nominal single-column width: 3.45 in;
- final-size figure typography: approximately 7–9.5 pt;
- no 3-D effects, gradients, decorative backgrounds, pictograms, or chartjunk;
- no dual y-axis when a common physical scale is possible;
- no smoothing/interpolation/model fitting over the raw POWDER attenuation points;
- raw replicate/cycle observations remain visible where they are the scientific unit;
- color is not the sole discriminator: marker shape and/or line style also encode series identity;
- no internal titles; interpretation belongs in the journal caption;
- no error bars or confidence intervals are manufactured for the deterministic three-replicate FIT completeness outcomes;
- no combined FIT+POWDER reliability visualization is permitted.

## 3. Final authorized figures

### Figure 1 — FIT architecture-level final completeness

Purpose: supports IC-01 and IC-02.

Displays all three replicate-level observations for B0 and W1 under C0/C1/C2. Replicate separation is achieved only by small categorical x-position jitter; y values are unchanged.

Scientific content:

- C0: B0 100%, W1 100% in 3/3;
- C1: B0 80%, W1 100% in 3/3;
- C2: B0 80%, W1 100% in 3/3.

The figure does not imply population reliability or strongest-durable-MQTT superiority.

Final file hashes:

- PDF `d8656c85c4cdb66cac4b1555e89a1d62216c5db107f44ebba8aed0544b362152`
- PNG `de01055fd10f9d2cd6267917e3443116b97cfdcc4423def09fe5e10234664830`
- SVG `0aea280a153a32397b118117c7211d4b7709880f3f0be26b6bd61664e0e1b750`

### Figure 2 — FIT W1 backlog-drain cost

Purpose: supports IC-03.

Displays all three run-level W1 backlog-drain values for C1/C2 and a short arithmetic-mean segment. Transport reconnect is deliberately excluded because reconnect and backlog drain are different recovery constructs.

Final file hashes:

- PDF `329f940d31392b0273876d410231fde6616aa0a54c53fa1bced41d1f7c15fabe`
- PNG `ce4569bcce7e791b46c731191b01735a3eeedfe6db81e09fff6f69f051974ee1`
- SVG `1e08513ed93ff2ecac78a3b2e304c70d8496bbc54cc2d23cf8840bba186edf85`

### Figure 3 — POWDER cross-layer transition and direction

Purpose: supports IC-04 and IC-05.

Displays E1R4 ascending and E2 descending sweeps. ICMP is converted from packet-loss percentage to response-success percentage (`100 - loss`) so both ICMP and MQTT share one truthful 0–100% axis; this avoids a dual-axis graphic.

No attenuation interpolation is used. The figure remains experiment-specific and does not label 52 dB as a universal threshold.

Final file hashes:

- PDF `759b280aba44ede0b0111e258994963ec1ad094dddd9a055d9d14d5e903d4401`
- PNG `078471191efeb1335c7cefb129a6d88486c6309618a4e5286a52ecbdb960fc6a`
- SVG `cfa580aa7cb4f2e33d672fc269526fcd22925b56aa83c65b1a114a5af1f9707e`

### Figure 4 — POWDER E3 near-transition repeatability

Purpose: supports IC-04.

Displays MQTT completeness for each of three E3 cycles at 49–52 dB. No mean or fitted line replaces the cycles because the scientific result is the observed variability itself, especially the 60% / 25% / 55% spread at 52 dB.

Final file hashes:

- PDF `5c751c72c7fb3a54d7abe28228f165449fe6768dde210f3b6f047bd28437d729`
- PNG `7a6d107df9015d1ccd52f7454b060dd675a8f3fa8075e7aa2cf4e0731d8bf9ab`
- SVG `7c42fbe563a10c4e009199e914c7303149cde9974aee0859a138f98b375f0277`

## 4. Publication tables

### Table 1 — FIT architecture summary

Contains condition-level run values for B0/W1 final completeness, W1-B0 absolute percentage-point differences, and permanent-missing counts.

### Table 2 — POWDER transition summary

Contains E1R4/E2 attenuation, ICMP loss/RTT, MQTT unique sent/received, completeness, direction and anomaly notes.

### Table 3 — POWDER recovery timing semantics

Contains E10-A/B/C-B/D mechanism, exact endpoint definition, censor/upper-bound status and numerical value where valid. This table is the publication safeguard against collapsing distinct recovery clocks into one generic latency.

## 5. Captions and accessibility

`analysis/WP2_P14_FIGURE_CAPTIONS_AND_ALT_TEXT_2026-08-29.md` freezes journal-ready captions and accessibility text. Captions preserve the exact experiment boundary and prohibit universal-threshold or generic-recovery wording.

## 6. Visual QA

Each final PNG was visually inspected at rendered single-column scale after generation.

QA checks:

- labels not clipped: PASS;
- legend does not obscure primary data: PASS;
- raw replicate/cycle observations visible: PASS;
- no accidental extra visual variable from replicate color assignment: PASS after revision;
- no misleading dual axes: PASS;
- percentage scales and axis direction truthful: PASS;
- categorical x jitter changes position only, never outcome values: PASS;
- E3 variability remains unsmoothed: PASS;
- grayscale/low-color discrimination supported by marker/line-style redundancy: PASS;
- figure caption can carry caveats without embedding narrative text into graphics: PASS.

## 7. Claim-display mapping

| Claim | Display authority |
|---|---|
| IC-01 | Figure 1 + Table 1 |
| IC-02 | Figure 1 + Table 1 |
| IC-03 | Figure 2 + Table 1 / P11 run table |
| IC-04 | Figures 3–4 + Table 2 |
| IC-05 | Figure 3 + Table 2 |
| IC-06 | Table 3; no single generic recovery bar chart |
| IC-07 | Table 3 / bounded E8 text result; no architecture comparison graphic |
| IC-08 | no quantitative combined figure; manuscript methodological synthesis only |
| IC-09 | no effect chart; reproducibility/provenance description only |

## 8. Explicit non-figures

P14 intentionally does **not** create:

- a FIT+POWDER combined reliability score;
- a POWDER B1-vs-W1 plot;
- a 52-dB threshold line labelled as failure threshold;
- a generic recovery-latency bar chart mixing E10-B, E10-C-B, E10-D and FIT backlog drain;
- confidence intervals fabricated from message counts;
- field/Siwa/agronomic schematics implying validation not performed.

## 9. Acceptance gate

- all quantitative displays map to P13-PASS claims: PASS;
- source values trace to P11/P9 evidence: PASS;
- raw observations retained where scientifically material: PASS;
- no manual spreadsheet editing required: PASS;
- vector + 600-dpi outputs produced: PASS;
- captions/alt text frozen: PASS;
- visual QA at final scale: PASS;
- unsupported combined inference: NONE.

`P14_FIGURES_FINAL=4`

`P14_TABLES_FINAL=3`

`P14_VISUAL_QA=PASS`

`P14_UNSUPPORTED_VISUAL_CLAIMS=0`

`P14_STATISTICAL_POOLING=NONE`

`WP2_P14=PASS_PUBLICATION_TABLES_AND_FIGURES_FROZEN`

`P14_NEXT=WP2_P15_MANUSCRIPT_CONSTRUCTION`
