# WP2-P18R — Scientific Figure Engineering Lifecycle

Date: 2026-08-29  
Status: **PASS / CODE-GENERATED SCIENTIFIC FIGURE SYSTEM / P18 MAIN DISPLAY SUPERSEDED**

## 1. Trigger

The author rejected the P18 main figures as scientifically too simple/naive and rejected subsequent AI-generated redesigns as non-credible publication artifacts. P18 was therefore reopened rather than cosmetically edited.

AI-generated figure images have **no scientific or canonical authority** in this project.

## 2. Reconsulted consortium

The prior P17/P17V review roles were re-engaged for a figure-specific design round:

1. systems / IoT scientific editor;
2. MQTT persistence/protocol specialist;
3. embedded storage/crash-consistency reviewer;
4. wireless/RF experimentalist;
5. LTE systems reviewer;
6. experimental-design/statistics reviewer;
7. causal/measurement-methodology reviewer;
8. reproducibility/forensic-evidence auditor;
9. research-software reviewer;
10. literature/novelty meta-reviewer;
11. scientific-visualization/information-design reviewer;
12. adversarial associate-editor/journal-production reviewer.

This is role-based review; no fictitious individual identities are asserted.

## 3. Consortium diagnosis

P18 was numerically correct but under-exploited the scientific record. Its one-narrow-message-per-figure implementation was safe but visually and scientifically thin. The consortium required composite, code-generated displays that expose multiple logically related endpoints while preserving the P13 claim envelope.

The required design principle is:

> **Richness must come from scientific structure, not decoration.**

## 4. Frozen main-figure architecture

### Figure 1 — System and evidence architecture

Scientific jobs:
- code-grounded W1 durable record-state machine;
- stable identity/checksum;
- SQLite WAL/PENDING state;
- publish/retry path;
- receiver reconciliation and SENT state;
- FIT design/treatment/endpoints;
- POWDER transition/recovery/control roles;
- IC-01…IC-09 mapping;
- explicit no-pooling guard.

### Figure 2 — FIT record survival and recovery cost

Composite empirical figure:
- **A:** run-level B0/W1 final receiver-reconciled completeness for C0/C1/C2;
- **B:** reconnect time by architecture and failure condition;
- **C:** W1 backlog-drain time.

This figure makes the effect and its operational cost visible together while keeping final integrity, reconnect, and catch-up as distinct constructs.

### Figure 3 — POWDER transition and repeatability

Four empirical panels:
- **A:** E1R4 ascending / E2 descending ICMP response;
- **B:** E1R4 ascending / E2 descending MQTT completeness;
- **C:** E3 cycle-level ICMP loss;
- **D:** E3 cycle-level MQTT completeness.

This exposes cross-layer transition, direction dependence, and near-transition variability without fitting a threshold.

### Figure 4 — Failure-domain and recovery semantics

Figure-table hybrid:
- **A:** intervention-domain matrix for RF / UE / CORE / broker / no-fault cases E4–E10;
- **B:** E10 endpoint semantics preserving exact, censored, and upper-bound observations.

This makes IC-06/IC-07 visible instead of burying the recovery claim in prose.

## 5. Main/supplement boundary

### Main article

Figures 1–4 above.

### Supplement

- detailed E0/E4–E11 experiment atlas;
- individual timeline plots;
- FIT full run ledger;
- run-validity register;
- anomaly register;
- detailed provenance/hash tables.

### Sanitized artifact

- canonical derived CSVs supporting public values;
- generator source;
- figure specification;
- manifests and QA receipts;
- releasable evidence after P19 privacy/security review.

## 6. SDLC-like lifecycle

### Phase 0 — problem definition

P18 visual implementation rejected by author; AI alternatives explicitly rejected.

**Gate: PASS — redesign required.**

### Phase 1 — requirements engineering

Requirements derived from P13/P17/P17V and the reconsulted consortium.

**Gate: PASS — FRS frozen.**

### Phase 2 — design architecture

Selected code-first toolchain:
- Matplotlib/Pandas/Numpy for quantitative figures;
- Graphviz only for deterministic structured figure-tables where appropriate;
- no AI image input;
- no manually edited raster source.

**Gate: PASS.**

### Phase 3 — implementation

Reusable CLI generator implemented in the P18R release package.

Canonical input paths:
- `analysis/WP2_P11_FIT_RECONSTRUCTED_RUNS_2026-08-29.csv`;
- `analysis/WP2_P11_POWDER_DERIVED_METRICS_2026-08-29.csv`;
- `analysis/WP2_P14_TABLE3_POWDER_RECOVERY_TIMING_2026-08-29.csv`.

Generator source SHA-256:

`5a313546fd88b6e06d7d3c473bb6742e214723287bdd37a9b84cf26faadf87f6`

**Gate: PASS.**

### Phase 4 — unit/data verification

The generator hard-fails unless the frozen scientific values remain consistent, including:
- FIT 18 cells and 10,000 records/cell;
- C0 B0/W1 = 100/100;
- C1/C2 B0 = 80 and W1 = 100 in R1–R3;
- B0 C1/C2 exactly 2,000 permanent missing records;
- E1R4 51/52 dB cross-layer values;
- E2 severe 52 dB values;
- E3 52 dB MQTT `60/25/55%` and ICMP loss `80/65/70%`;
- E10 censored and upper-bound semantics.

**Gate: PASS.**

### Phase 5 — visual verification

The first code build was **rejected internally** despite successful execution because of production-scale and text-layout defects. F1–F4 were redesigned/rebuilt. Final PDFs were rendered independently at 200 dpi and visually inspected.

**Gate: PASS.**

### Phase 6 — scientific validation

Validation confirmed:
- all main empirical claim families now have visible displays;
- raw run/cycle patterns remain visible;
- percentage axes include zero;
- no unsupported CI or threshold fit;
- no FIT+POWDER quantitative pooling;
- recovery clocks and semantic classes remain distinct;
- negative/censored observations remain represented.

**Gate: PASS.**

### Phase 7 — release/configuration management

Durable release package:

`WellPulse_P18R_Scientific_Figure_Engineering_Release_2026-08-29.zip`

Drive ID:

`1alitbv9479Mq9URhXIBHkQql7zuuA51o`

ZIP SHA-256:

`5586091bc518cc541c3c9b75e9a0c965913877cd6bf83d1644fa6f05264e1083`

Final figure PDF SHA-256 values:
- F1 `179b3201b63a5910473885e2005d2ba2bfd55c9fe888f0d1ed42980d21a09ea1`;
- F2 `a38e321ec4a6b51ede1fff89601432852ac0c9e0e56d32ac880724a3b9ad0eff`;
- F3 `bc23a25a53beb13396b056b22bdd93af62ec7c7f91b3d81199028dd4496887ee`;
- F4 `a2be6684ddd339f6b60c1406cb9673a2d14a2c6c038cdb8a0ec748b6b93f5d0c`.

## 7. Production requirements satisfied

- no AI-generated figure assets;
- PDF/SVG vector masters;
- 600-dpi PNG fallback;
- embedded PDF fonts;
- main figures constrained to full-width publication scale;
- deterministic source-to-output path;
- source-data receipt and QA report included;
- figures reproducible from declared canonical CSVs.

## 8. Scientific prohibitions unchanged

P18R introduces no new empirical claim. It does not authorize:
- generic MQTT superiority;
- a universal 52 dB threshold;
- pooled FIT+POWDER reliability;
- deterministic RF-only recovery;
- scalar E10-A latency;
- exact E10-D broker latency;
- population reliability from message counts.

## 9. Final status

`P18R_CONSORTIUM_DECISION=CONSENSUS_CODE_GENERATED_COMPOSITE_FIGURES`

`P18R_AI_GENERATED_ASSETS=REJECTED_NOT_CANONICAL`

`P18R_DATA_INVARIANTS=PASS`

`P18R_RENDER_FIRST_VISUAL_QA=PASS`

`P18R_FIGURE_ENGINE_VV=PASS`

`WP2_P18R=PASS_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE`

`P18_PREVIOUS_MAIN_DISPLAY_AUTHORITY=SUPERSEDED_BY_P18R`

`SUBMISSION_AUTHORIZED=NO`
