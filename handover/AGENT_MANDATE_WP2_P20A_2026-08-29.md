# AGENT MANDATE — WellPulse WP2-P20A Literature & Novelty Closure

Date: 2026-08-29  
Status: **READY / DO NOT EXECUTE WITHOUT CURRENT AUTHORIZATION**

## Canonical repository

- Repository: `aayoubMSA/WellPulse`
- Branch: `main`
- Operational retrieval point: `HANDOVER_CURRENT.md`
- WP architecture authority: `docs/WP2_POST_P19_CONSORTIUM_WP_ARCHITECTURE_REVIEW_2026-08-29.md`

## Exact mandate

Execute **only WP2-P20A — LITERATURE & NOVELTY CLOSURE**.

P20A is a venue-neutral external-knowledge closure gate. It may refine or narrow novelty/related-work wording but must not change experiments, measured values, axes, aggregations, P13 claims, P17/P17V conclusions, P18RC figures, P19 artifact semantics, or historical P7B state.

## Mandatory read order

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_POST_P19_CONSORTIUM_WP_ARCHITECTURE_REVIEW_2026-08-29.md`
3. `docs/WP2_P10_SCIENTIFIC_ANALYSIS_CONTRACT_2026-08-29.md`
4. `analysis/WP2_P13_CLAIM_EVIDENCE_MATRIX_2026-08-29.md`
5. `manuscript/WP2_P16_ADVERSARIAL_PUBLICATION_QA_2026-08-29.md`
6. `manuscript/WP2_P16_MANDATORY_EDITORIAL_PATCHES_2026-08-29.md`
7. `analysis/WP2_P17_EVIDENCE_EXPLOITATION_MATRIX_2026-08-29.md`
8. `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`
9. `analysis/WP2_P17V_INDEPENDENT_CLAIM_VALIDATION_MATRIX_2026-08-29.md`
10. `manuscript/WP2_P17V_SUPERIOR_INDEPENDENT_CONSORTIUM_VALIDATION_2026-08-29.md`
11. P9/P11 only when a literature statement needs exact comparison against experimental scope.

## Required work

1. Run a current submission-date literature search across the final novelty axes:
   - MQTT persistence/session/retransmission;
   - IoT/MQTT robustness and fault injection;
   - offline-first / edge-cloud continuity / store-and-forward;
   - failure-domain-aware resilience/recovery evaluation;
   - real wireless/IoT testbeds and reproducibility;
   - receiver-side reconciliation/provenance where materially relevant.

2. Recover and assess **Gaspar et al. 2026, DOI `10.1109/MIOT.2026.3681190`** at full-text level if legitimately accessible. If full text is unavailable, record that explicitly and keep all manuscript treatment at bibliographic/scope level.

3. Re-verify every material related-work bibliographic record used in the manuscript against authoritative sources.

4. Build a comparator/novelty matrix identifying:
   - what prior work already establishes;
   - what the current WellPulse evidence directly establishes;
   - where the current manuscript must narrow or remove novelty language;
   - whether any newly found work creates a genuine scientific blocker.

5. Produce a final literature/novelty closure receipt with source links/identifiers and exact wording constraints for P20D.

## Acceptance gate

P20A PASS requires:

- current literature search completed and dated;
- all material bibliographic anchors verified;
- Gaspar full-text comparison completed if accessible, otherwise explicit unavailable-status recorded;
- no unsupported method/result attribution to inaccessible sources;
- novelty claims remain bounded to the P13/P17V evidence envelope;
- any prior-art collision is explicitly classified as `NO IMPACT`, `WORDING NARROWING`, or `SCIENTIFIC BLOCKER`;
- no experiment or empirical claim is added;
- scientific blockers remain zero, or P20A stops with the exact newly discovered blocker;
- submission remains NOT AUTHORIZED.

## Dependency / next gate

P20B — Venue Qualification & Selection is locked until P20A passes.

Do not perform venue-specific manuscript formatting, authorship/rights lock, final source packaging, or submission during P20A.

## Stop state

`CURRENT_PHASE=WP2_P20A_LITERATURE_AND_NOVELTY_CLOSURE`

`P20B_LOCKED_UNTIL_P20A_PASS=YES`

`NEW_EXPERIMENT_AUTHORIZED=NO`

`SUBMISSION_AUTHORIZED=NO`
