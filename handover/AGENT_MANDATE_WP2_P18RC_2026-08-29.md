# AGENT MANDATE — WellPulse WP2-P18RC Main-Figure Production Normalization

Date: 2026-08-29
Status: **READY FOR NEXT AGENT**

## Canonical repository

- Repository: `aayoubMSA/WellPulse`
- Branch: `main`
- Canonical operational retrieval point: `HANDOVER_CURRENT.md`

## Mandatory read order

Read in this order before taking any action:

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

Use P9 forensic authorities only when exact POWDER trace/caveat semantics are needed. Treat P18/P18B as historical comparison only.

## Exact mandate

Resume **only at WP2-P18RC — MAIN-FIGURE PRODUCTION NORMALIZATION**.

P18RC is a publication-engineering gate. It is not a scientific redesign and it must not reopen the experiment, the P13 claim envelope, P17/P17V conclusions, or historical P7B state.

## Frozen state

- P17V: `VALIDATED_WITH_PRE_SUBMISSION_CONDITIONS`
- claims validated: `9/9`
- current scientific blockers: `0`
- new experiment required: `NO`
- new empirical claim required: `NO`
- live POWDER dependency: `NONE`
- submission authorization: `NO`
- P18R: current main-display authority
- F1 deterministic hotfix: current Figure-1 authority
- P18RB: `CONDITIONAL_PASS_SCIENCE_PASS_PRODUCTION_NORMALIZATION_REQUIRED`

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8+ result may be promoted or relabelled as scored P7B.

## Current Figure-1 authority

Canonical generator:

`analysis/wp2_p18r_generate_f1_hotfix.py`

Current generator SHA-256:

`3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`

Final Figure-1 PDF SHA-256:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

Durable F1 archive on Drive:

- file: `WellPulse_P18R_F1_Hotfix_Final_2026-08-29.zip`
- Drive ID: `12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M`
- ZIP SHA-256: `e9d5a54b24506b879a748b5a06b39699e6f6ec1ed31093491c27b2be7d7e6e1d`
- Drive read-back hash: PASS

The AI-generated F1 is **reference only and not canonical**.

## P18RC required work

Complete only the finite production-normalization patch required by P18RB:

1. **F2 semantic encoding cleanup**
   - remove accidental/default Matplotlib color-cycle meaning;
   - preserve all run-level data points and existing scientific values;
   - do not introduce a new statistic, aggregation, confidence interval, smoothing, or threshold.

2. **Typography normalization across F1–F4**
   - use embedded Helvetica/Arial-compatible venue-neutral sans typography;
   - preserve final-width readability;
   - no font substitution that changes scientific content or layout meaning.

3. **Grid/line discipline**
   - remove nonessential background gridlines;
   - normalize ordinary strokes to `<=1 pt` where applicable;
   - preserve meaningful markers, line-style redundancy, and grayscale interpretability.

4. **Accessibility**
   - freeze explicit alt text for F1–F4;
   - verify that no scientific distinction depends on color alone;
   - verify final-width label readability and zero clipping/overlap.

5. **Metadata / attribution / rights normalization**
   - normalize supported file-level author/affiliation/rights metadata for F2–F4 to match current project identity and F1 discipline;
   - do not invent a public license, coauthor, CRediT role, funding source, copyright ownership, or permissions statement.

6. **Deterministic rebuild and QA**
   - rebuild the complete normalized F1–F4 set;
   - produce PDF/SVG vector masters and high-resolution PNG fallback where applicable;
   - verify embedded fonts;
   - run render-first visual QA at final publication width;
   - rebuild again to verify deterministic hashes where feasible;
   - freeze manifests, hashes, source/data identities, caption/alt-text package, and V&V receipt.

## Scientific invariants — must not change

- FIT remains the architecture-level record-state-survival evidence layer.
- POWDER remains separately executed communication-path degradation/recovery characterization.
- no FIT+POWDER pooled statistic or pooled inferential effect;
- B0 remains explicitly non-durable;
- C2 remains gateway-process `exec` restart, not node reboot;
- run is the FIT scientific unit; message count does not inflate `n`;
- 52 dB remains experiment-specific, not a universal threshold;
- E10-A remains censored with no scalar recovery latency;
- E10-D remains an upper bound only;
- receiver-side unique-ID reconciliation remains authoritative for reported delivery;
- no generic `WellPulse beats MQTT` claim;
- no field/rural/Siwa/pump/hydraulic/agronomic validation claim.

Any proposed change to values, axes, aggregation, smoothing, statistical inference, failure-domain interpretation, or claim semantics **must stop P18RC and reopen P18R V&V instead of being applied silently**.

## Storage / provenance rules

- GitHub = canonical scientific/control/source record.
- Google Drive = durable authority for frozen/raw binary evidence and registered research packs.
- Raw evidence remains immutable.
- Never treat chat history as source of truth.
- Any final release package must be archived durably and read-back/hash verified before closure.

## Attribution / affiliation guard

Current internal project identity:

**Dr. Ahmed Elsayed Ayoub**  
Assistant Professor of Computer Engineering  
Department of Computer Systems Engineering  
Faculty of Engineering, MSA University  
Giza, Egypt

Before external release/submission, explicitly verify final author list/order, CRediT roles, funding/COI, collaborator acknowledgments, FIT IoT-LAB and POWDER acknowledgment/citation, and venue/institution/testbed copyright-license requirements.

## Acceptance gate for P18RC

P18RC may be marked PASS only if all of the following hold:

- F1–F4 scientific encodings unchanged except approved evidence-neutral production normalization;
- F2 accidental/default color semantics removed;
- typography normalized and fonts embedded;
- nonessential grids/line weights normalized;
- grayscale/non-color-only interpretation PASS;
- alt text complete for F1–F4;
- zero known clipping, text overlap, or arrow/text crossing at final width;
- PDF/SVG and high-resolution raster fallbacks present as required;
- deterministic/rebuild checks PASS where feasible;
- metadata/attribution normalized;
- manifest/hashes/source identities frozen;
- durable Drive archive + read-back hash PASS;
- GitHub canonical receipt + updated `HANDOVER_CURRENT.md` committed;
- scientific blockers remain `0`;
- submission remains `NOT AUTHORIZED`.

## Next gate after P18RC PASS

Proceed directly to:

### WP2-P19 — reviewer-facing supplementary atlas + sanitized artifact

P19 should package the reviewer supplement, E0–E11 atlas, FIT ledger, validity/anomaly evidence, endpoint semantics, analysis code, derived non-sensitive data, manifests, sanitized figures, and privacy/security review.

Do not jump to P20 or submission before P19 is complete.

## Stop state

`HANDOVER_STATUS=READY`

`CURRENT_PHASE=WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION`

`SCIENTIFIC_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

`SUBMISSION_AUTHORIZED=NO`

`NEXT_AFTER_PASS=WP2_P19_REVIEWER_SUPPLEMENT_AND_SANITIZED_ARTIFACT`
