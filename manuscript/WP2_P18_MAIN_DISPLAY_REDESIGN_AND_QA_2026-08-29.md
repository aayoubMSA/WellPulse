# WP2-P18 — Main-Display Redesign + Claim/Display QA

Date: 2026-08-29  
Status: **PASS / MAIN DISPLAY SET REDESIGNED / CLAIM-DISPLAY QA PASS**

## 1. Mandate

Redesign the publication-facing main display set so that the P17/P17V thesis is immediately legible without implying statistical or causal pooling between FIT and POWDER. Preserve the frozen P13 claim envelope and introduce no new empirical claim.

P18 does not change raw evidence, numerical results, experiment validity, P13 claims, or submission authorization.

## 2. Final main display set

### Main Figure 1 — Architecture + evidence-role schematic

New figure:

`Fig_P18_01_architecture_evidence_roles`

Scientific jobs:
- make W1 implementation semantics concrete at a glance;
- show generation → identity/hash → durable queue → MQTT attempt → receiver identity reconciliation;
- show failed delivery returning to durable state rather than disappearing;
- separate FIT (`record-state survival`) from POWDER (`communication-path degradation/recovery`);
- allow only structured synthesis downstream of the two non-overlapping evidence roles.

The figure explicitly states that there is no pooled cross-platform reliability statistic and no POWDER W1-versus-baseline effect.

### Main Figure 2 — FIT final completeness

New publication-facing redraw:

`Fig_P18_02_FIT_completeness`

Uses the frozen P11/P13 FIT values only. All three run-level observations remain visible. The y-axis now uses a full `0–100%` percentage scale rather than the historical P14 zoomed scale, reducing visual exaggeration risk.

Supports: `IC-01`, `IC-02`.

### Main Figure 3 — POWDER transition / direction response

New publication-facing redraw:

`Fig_P18_03_POWDER_transition_direction`

Uses E1R4 ascending and E2 descending values on a common 0–100% response/completeness scale. ICMP uses `100 - loss` so that both response and MQTT completeness share truthful percentage semantics without a dual y-axis.

Supports: `IC-04`, `IC-05`.

### Main Figure 4 — POWDER E3 repeatability

New publication-facing redraw:

`Fig_P18_04_POWDER_E3_repeatability`

Shows all three E3 cycles and uses a full `0–100%` completeness axis rather than the historical zoomed scale.

Supports: `IC-04`.

## 3. Main tables

### Main Table 1 — Failure-domain taxonomy

Canonical CSV:

`analysis/WP2_P18_FAILURE_DOMAIN_TAXONOMY_2026-08-29.csv`

Columns:
- failure domain;
- experiment;
- manipulated component;
- primary endpoint;
- admissible interpretation;
- prohibited overreach.

This table makes exact failure identity reader-visible and prevents `restart`, `outage`, and `recovery` from being treated as interchangeable terms.

Supports primarily: `IC-06`, `IC-07`, `IC-08`.

### Main Table 2 — FIT run-level summary

Retain the compact P14/P11 FIT run summary values. Supports `IC-01`, `IC-02`, `IC-03`.

### Main Table 3 — Recovery endpoint semantics

Retain exact/censored/upper-bound timing semantics from P11/P14. Supports `IC-06`, `IC-07`.

## 4. Main-versus-supplement split

Canonical split:

`analysis/WP2_P18_MAIN_SUPPLEMENT_DISPLAY_SPLIT_2026-08-29.csv`

Main paper:
1. architecture + evidence-role schematic;
2. FIT completeness;
3. POWDER transition/direction;
4. POWDER E3 repeatability;
5. failure-domain taxonomy;
6. FIT summary;
7. recovery-semantics table.

Move to supplement:
- standalone FIT backlog-drain plot while retaining the numerical values in main text/table;
- detailed E0/E4–E11 atlas figures;
- run-validity map;
- anomaly register;
- detailed provenance/hash tables.

Move to artifact:
- derived CSVs;
- reconstruction/figure scripts;
- non-sensitive manifests;
- releasable evidence after P19 sanitization.

## 5. Claim/display QA

| Display | Claims | QA result |
|---|---|---|
| Figure 1 architecture/evidence roles | IC-08, IC-09 + implementation Methods | PASS — no quantitative pooling or new effect |
| Figure 2 FIT completeness | IC-01, IC-02 | PASS — B0/W1 only, raw run outcomes, full percentage scale |
| Figure 3 POWDER transition/direction | IC-04, IC-05 | PASS — experiment-specific programmed attenuation, no universal threshold |
| Figure 4 E3 repeatability | IC-04 | PASS — all three cycles retained, no fitted threshold/probability |
| Table 1 failure taxonomy | IC-06, IC-07, IC-08 | PASS — mechanism and prohibited interpretation explicit |
| Table 2 FIT summary | IC-01, IC-02, IC-03 | PASS — no population probability or strongest-client claim |
| Table 3 recovery semantics | IC-06, IC-07 | PASS — exact/censored/upper-bound semantics preserved |

`P18_UNSUPPORTED_DISPLAY_CLAIMS=0`

`P18_CROSS_PLATFORM_QUANTITATIVE_POOLING=NONE`

## 6. Production QA

Final files were generated vector-first and raster-fallback:
- PDF;
- SVG;
- PNG at 600 dpi.

Measured final dimensions:
- Figure 1: exactly `7.16 in` wide (IEEE two-column width target);
- Figures 2–4: exactly `3.5 in` wide (IEEE one-column width target).

PDF fonts are embedded/subset. PNG exports are 600 dpi.

Figure 1 underwent multiple reject/redraw cycles because early versions had text collision. The final inspected version has no known clipping or text overlap.

Historical P14 percentage plots with zoomed y-axes were not reused as the P18 main quantitative displays; Figures 2 and 4 were re-rendered with full percentage axes to reduce visual exaggeration risk.

## 7. Reproducibility

Canonical generators:
- `analysis/wp2_p18_generate_main_display.py`;
- `analysis/wp2_p18_generate_quantitative_figures.py`.

Durable display pack:
- Drive parent: `P12_WellPulse`;
- Drive ID: `1tAj83-6rbDEdho9yKdREXU00w6h1pteh`;
- file: `WellPulse_P18_Display_Pack_2026-08-29.zip`;
- SHA-256: `332106ead2abf893f6cf042852c2f7e5e291a39c38e93db682c4020059ae5d09`.

Principal figure PDF SHA-256 values:
- Fig 1: `b2af596966f19b4bb7a1a645c175c67a4c8ef9191cc72fa774abd6aadbd77013`;
- Fig 2: `7339dd11a5b75d022fa7beaf02d381f4d38936926d333c79bbe7c566e434e08d`;
- Fig 3: `f06b8b536323f8fc55164516f084275e61400eb354d95c2f34a0b0c9a86368db`;
- Fig 4: `f9622c1f826e8796e1c8331a2d4bea44cebcbb19f185f4fff1c379b8fd849ff2`.

## 8. Acceptance gate

- architecture/evidence-role schematic: PASS;
- failure-domain taxonomy: PASS;
- final main/supplement split: PASS;
- quantitative percentage-axis integrity: PASS;
- claim-to-display mapping: PASS;
- visual inspection at final dimensions: PASS;
- vector/raster production formats: PASS;
- embedded fonts: PASS;
- new empirical claim introduced: `0`;
- new experiment required: `NO`;
- submission authorized: `NO`.

`WP2_P18=PASS_MAIN_DISPLAY_REDESIGN_CLAIM_DISPLAY_QA`

`P18_NEXT=WP2_P19_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`
