# WellPulse — Current Handover

Last updated: 2026-08-29 after **P18RB benchmark + P18R F1 storage/provenance closure**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Repository and durable Drive evidence override conversation memory.

## Executive state

- WP2-P8 manual POWDER campaign: **COMPLETE / GOLDEN / MANUAL REFERENCE**
- WP2-P9 forensic reconciliation: **PASS / COMPLETE**
- WP2-P10 scientific analysis contract: **PASS / FROZEN**
- WP2-P11 full raw-data scientific analysis: **PASS / COMPLETE**
- WP2-P12 cross-evidence integration: **PASS / COMPLETE**
- WP2-P13 claim–evidence matrix: **PASS / FROZEN CLAIM AUTHORITY**
- WP2-P14: **PASS / HISTORICAL DISPLAY SET**
- WP2-P15: **PASS / HISTORICAL INTERNAL FULL DRAFT**
- WP2-P16: **PASS / ADVERSARIAL PUBLICATION QA**
- WP2-P17: **PASS / CONSORTIUM-REVISED INTERNAL MANUSCRIPT + DOSSIER RESEARCH PACK**
- WP2-P17V: **PASS / VALIDATED WITH PRE-SUBMISSION CONDITIONS**
- WP2-P18 first display redesign: **SUPERSEDED BY P18R**
- WP2-P18B: **HISTORICAL PRE-P18R BENCHMARK**
- WP2-P18R scientific figure engineering: **PASS / CURRENT MAIN-DISPLAY AUTHORITY**
- P18R Figure-1 deterministic hotfix: **PASS / CURRENT F1 AUTHORITY / DURABLY ARCHIVED**
- WP2-P18RB post-P18R benchmark: **CONDITIONAL PASS / SCIENCE PASS / PRODUCTION NORMALIZATION REQUIRED**
- current scientific blockers: **0**
- new experiment required for current bounded manuscript: **NO**
- new empirical claim required: **NO**
- live POWDER dependency: **NONE**
- submission authorization: **NO**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8+ result may be promoted or relabelled as scored P7B.

## Mandatory read order for continuation

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
3. `analysis/WP2_P11_FULL_RAW_DATA_SCIENTIFIC_ANALYSIS_2026-08-29.md`
4. `analysis/WP2_P12_CROSS_EVIDENCE_INTEGRATION_2026-08-29.md`
5. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
6. `manuscript/WP2_P16_ADVERSARIAL_PUBLICATION_QA_2026-08-29.md`
7. `manuscript/WP2_P16_MANDATORY_EDITORIAL_PATCHES_2026-08-29.md`
8. `docs/WP2_P17_EXPERIMENT_DOSSIER_V2_2_RESEARCH_PACK_2026-08-29.md`
9. `analysis/WP2_P17_EVIDENCE_EXPLOITATION_MATRIX_2026-08-29.md`
10. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`
11. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
12. `manuscript/WP2_P17V_SUPERIOR_INDEPENDENT_CONSORTIUM_VALIDATION_2026-08-29.md`
13. `analysis/WP2_P18R_FIGURE_REQUIREMENTS_SPEC_2026-08-29.md`
14. `manuscript/WP2_P18R_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE_2026-08-29.md`
15. `manuscript/WP2_P18R_F1_HOTFIX_QA_2026-08-29.md`
16. `analysis/WP2_P18R_GENERATOR_RELEASE_RECEIPT_2026-08-29.md`
17. `docs/WP2_P18R_F1_DRIVE_ARCHIVAL_CLOSURE_2026-08-29.md`
18. `analysis/WP2_P18RB_POST_P18R_HIGH_STANDARD_BENCHMARK_2026-08-29.md`
19. P9 forensic authorities when exact POWDER trace/caveat semantics are required.
20. P18/P18B only for historical comparison.

## Frozen evidence roles

### FIT — architecture-level record-state survival

Authority: `FINAL_WP_RT01_FIT_A8`.

Design: `B0/W1 × C0/C1/C2 × 3 runs = 18 cells`, exactly 10,000 records/run.

Core frozen outcome:

- C0: B0/W1 = 100% all runs;
- C1: B0 = 80%, W1 = 100% all runs;
- C2: B0 = 80%, W1 = 100% all runs;
- B0 C1/C2 permanently miss exactly 2,000 records/run;
- W1 final reconciliation has all 10,000 generated IDs exactly once;
- W1 backlog-drain means: C1 `67.731246 s`; C2 `67.870252 s`.

These are run-level repeated outcomes under the exact treatments, not population reliability probabilities.

### POWDER — communication-path degradation/recovery characterization

Campaign: `WP2-P8`, profile `srslte-controlled-rf`.

Publication role: **separately executed physical-RF/LTE/MQTT controlled reference characterization; not architecture-effect estimation**.

Key frozen interpretation:

- E1/E2/E3 characterize the experiment-specific transition region;
- 52 dB is **not** a universal threshold;
- E8 separates broker/service failure from healthy LTE connectivity;
- E9 is the no-fault control;
- E10 preserves exact/censored/upper-bound timing semantics;
- receiver-side unique-ID reconciliation is authoritative where sender/receiver records disagree.

## Frozen integration doctrine

FIT and POWDER are complementary and non-substitutable:

- FIT = record-state survival / bounded architecture comparison;
- POWDER = communication-path degradation and recovery characterization.

No pooled FIT+POWDER reliability statistic or inferential effect is allowed.

P13 remains the claim authority. P17/P17V/P18R/P18RB add no new empirical claims and do not expand the P13 envelope.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P13_STATISTICAL_POOLING=NONE`

## Current manuscript baseline

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`

Working title:

**WellPulse: Separating Record-State Survival from Communication-Path Recovery in Resilient IoT Telemetry**

P17V verdict: **VALIDATED WITH PRE-SUBMISSION CONDITIONS**.

- claims validated: `9/9`;
- numerical contradictions: `0`;
- unsupported new claims: `0`;
- scientific blockers: `0`;
- new experiment required: `NO`.

The bounded limitation remains explicit: B0 is non-durable and is not the strongest durable MQTT comparator. Do not generalize the result into generic MQTT superiority.

## Durable Drive authorities

### P17 dossier/research pack

Drive parent folder ID: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`

- dossier PDF `WellPulse_Experimental_Technical_Dossier_v2.2.pdf` — Drive ID `12ec22A89ybsNoBpYcglx9Im6pW8Vk55-`, SHA-256 `a9274514cbf21de58291c2640f560f6082711e0a8696890419e918e595b40f3e`;
- dossier reproducible package — Drive ID `1ts__z8kN0fORwDksQZoj4eeaG--UyCAw`;
- experiment figure suite — Drive ID `1y8rStzWdGEivWjuFCP0h5Y6Amv6267sY`;
- figure-centered QA report — Drive ID `1ukEvwr3_uOoZcCn3TknwOcZL6HRaLo1a`.

Raw FIT and POWDER frozen archives remain higher measurement authorities than the dossier.

### P18R historical full figure-engineering release

`WellPulse_P18R_Scientific_Figure_Engineering_Release_2026-08-29.zip`  
Drive ID `1alitbv9479Mq9URhXIBHkQql7zuuA51o`  
SHA-256 `5586091bc518cc541c3c9b75e9a0c965913877cd6bf83d1644fa6f05264e1083`

The Figure 1 inside that historical release is superseded by the deterministic F1 hotfix below. Figures 2–4 remain P18R authorities pending P18RC normalization.

### Current deterministic Figure 1

Canonical generator: `analysis/wp2_p18r_generate_f1_hotfix.py`  
Git blob SHA-1: `bf344808414b78d9b0c688140e9de9a755d9a1e7`  
Current generator SHA-256: `3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`  
Final PDF SHA-256: `4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

Durable archive:

`WellPulse_P18R_F1_Hotfix_Final_2026-08-29.zip`  
Drive ID: `12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M`  
ZIP SHA-256: `e9d5a54b24506b879a748b5a06b39699e6f6ec1ed31093491c27b2be7d7e6e1d`

Drive read-back hash: **PASS / exact match**.

The previous generator SHA `201897de...` is superseded as stale provenance. A rebuild from the current generator reproduces the frozen final PDF hash exactly. No scientific or visual-content change resulted from this correction.

## P18RB benchmark — current production verdict

Canonical authority:

`analysis/WP2_P18RB_POST_P18R_HIGH_STANDARD_BENCHMARK_2026-08-29.md`

Verdict:

`WP2_P18RB=CONDITIONAL_PASS_SCIENCE_PASS_PRODUCTION_NORMALIZATION_REQUIRED`

Scientific/display blockers: `0`.

Mandatory bounded production-normalization classes before P19:

1. F2 semantic encoding cleanup — remove accidental/default color-cycle meaning while preserving data and raw points.
2. Use embedded Helvetica/Arial-compatible venue-neutral sans typography across F1–F4.
3. Remove nonessential background grids and normalize ordinary strokes to `<=1 pt` where applicable.
4. Freeze explicit alt text for F1–F4 and verify grayscale interpretation.
5. Normalize author/affiliation/rights metadata in supported F2–F4 file formats; do not invent a public license.
6. Rebuild the normalized main set and freeze hashes/rebuild QA.

P19 must not be frozen until P18RC passes.

## Exact next gate

### WP2-P18RC — MAIN-FIGURE PRODUCTION NORMALIZATION

P18RC is a publication-engineering gate only. It must not silently alter science, raw evidence, axes, aggregations, P13 claims, experimental validity, or FIT/POWDER inferential boundaries.

After P18RC PASS, proceed directly to:

### WP2-P19 — reviewer-facing supplementary atlas + sanitized artifact

Then P20 handles final literature/venue/source-package/credits/rights normalization and explicit submission authorization.

## Authorship / credits / rights guard

Do not invent coauthors, CRediT roles, funding, copyright ownership, or licensing terms. Before any external submission/release, explicitly verify final author list/order, CRediT roles, affiliation wording, funding/COI, collaborator acknowledgments, FIT IoT-LAB and POWDER acknowledgment/citation, and venue/institution/testbed copyright-license requirements.

## Immutable prohibitions

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- generic `WellPulse beats MQTT`;
- universal 52 dB threshold;
- deterministic RF-only recovery;
- exact broker latency from E10-D;
- population reliability from message counts or three FIT runs;
- pooled FIT+POWDER inferential statistics;
- field/rural/Siwa/pump/hydraulic/groundwater/agronomic/industrial-process validation not supported by the frozen evidence.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence and registered research packs.**
2. **GitHub = canonical scientific/control/source record.**
3. **Home PC = independent third copy where applicable; not canonical.**

Raw evidence remains immutable.

## Stop state

`WP2_P18R=PASS_SCIENTIFIC_FIGURE_ENGINEERING_LIFECYCLE`

`P18R_F1_HOTFIX=PASS_DETERMINISTIC_F1_ACCEPTED`

`P18R_F1_DRIVE_ARCHIVE=PASS`

`PROVENANCE_DRIFT=REPAIRED`

`WP2_P18RB=CONDITIONAL_PASS_SCIENCE_PASS_PRODUCTION_NORMALIZATION_REQUIRED`

`CURRENT_SCIENTIFIC_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

`LIVE_POWDER_DEPENDENCY=NONE`

`SUBMISSION_AUTHORIZED=NO`

`NEXT_PHASE=WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION`
