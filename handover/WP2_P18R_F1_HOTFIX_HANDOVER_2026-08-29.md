# WellPulse — P18R Figure-1 Hotfix Handover

Date: 2026-08-29  
Status: **PASS / HANDOVER READY / STORAGE CLOSURE COMPLETE**

## Purpose

This file is the continuation delta for the accepted deterministic Figure-1 hotfix. `HANDOVER_CURRENT.md` remains the broad project retrieval point and must be read first.

## Frozen project state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Current manuscript baseline: `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`.
- P13 claim envelope remains authoritative.
- P17V verdict remains **VALIDATED WITH PRE-SUBMISSION CONDITIONS**.
- No new experiment is required.
- No new empirical claim is required.
- Submission remains **NOT AUTHORIZED**.
- Live POWDER dependency: **NONE**.

## Figure-1 hotfix result

The prior P18R Figure 1 was rejected for layout/readability problems. An AI-generated redesign was also rejected as a canonical publication asset. The accepted replacement is deterministic and code-generated.

Frozen scientific corrections:

1. Sender-local `SENT` is separated from receiver-side evidence.
2. Local `SENT` occurs after MQTT QoS 1 PUBACK in the canonical W1 implementation.
3. Receiver-side evidence is independent: unique receiver IDs → generated/received reconciliation → reported final completeness.
4. Publication-facing artwork contains no internal `IC-xx` project-control identifiers.
5. FIT design states `3 runs/cell` and `10,000 records/run`.
6. POWDER is represented as the full `E0–E11` controlled RF/service/recovery characterization campaign.
7. Synthesis uses the reader-facing concept of two distinct resilience properties: record-state survival and communication-path recovery.
8. Complementary evidence only; no FIT+POWDER quantitative pooling and no POWDER W1-vs-baseline effect.

## Accepted current artifact identities

Final deterministic Figure-1 PDF SHA-256:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

Canonical generator:

`analysis/wp2_p18r_generate_f1_hotfix.py`

Git blob SHA-1:

`bf344808414b78d9b0c688140e9de9a755d9a1e7`

Current exact generator SHA-256:

`3de810672749001e9fb2d50c43b531e87fec7c359878a5aa7c58deb8ad0e7be5`

The earlier handover value `201897de563448037798678a73c998bd8b7a01f74bb4096995587f13d6667d48` is superseded for current generator identity. A fresh rebuild from the current generator reproduced the final PDF hash exactly; this was provenance drift only, not a figure-content change.

## Durable Drive archive

File:

`WellPulse_P18R_F1_Hotfix_Final_2026-08-29.zip`

Drive ID:

`12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M`

Drive URL:

`https://drive.google.com/file/d/12Q6QOTQWH2-t-Ryxy32ys2bXB3tw-B1M/view`

ZIP SHA-256:

`e9d5a54b24506b879a748b5a06b39699e6f6ec1ed31093491c27b2be7d7e6e1d`

Drive read-back hash verification: **PASS**.

Canonical closure record:

`docs/WP2_P18R_F1_DRIVE_ARCHIVAL_CLOSURE_2026-08-29.md`

## QA verdict

- known text overlaps: `0`;
- known clipping: `0`;
- known arrow/text crossings: `0`;
- PDF width: `7.16 in`;
- PDF fonts embedded: `PASS`;
- current-generator → frozen-PDF exact hash match: `PASS`;
- AI-generated asset dependency: `NONE`;
- Drive archive/read-back: `PASS`.

`P18R_F1_HOTFIX=PASS_DETERMINISTIC_F1_ACCEPTED`

`P18R_F1_DRIVE_ARCHIVE=PASS`

`PROVENANCE_DRIFT=REPAIRED`

`AI_F1=REFERENCE_ONLY_NOT_CANONICAL`

## Supersession correction — P18RB

The earlier version of this handover incorrectly stated that P18RB was not canonically complete. That statement is **SUPERSEDED**.

Canonical P18RB authority exists at:

`analysis/WP2_P18RB_POST_P18R_HIGH_STANDARD_BENCHMARK_2026-08-29.md`

Verdict:

`WP2_P18RB=CONDITIONAL_PASS_SCIENCE_PASS_PRODUCTION_NORMALIZATION_REQUIRED`

Scientific/display blockers: `0`.

## Exact next move

### WP2-P18RC — MAIN-FIGURE PRODUCTION NORMALIZATION

Mandatory bounded scope only:

- F2 semantic-encoding cleanup;
- Helvetica/Arial-compatible venue-neutral font-family normalization;
- remove nonessential grids and normalize ordinary strokes to <=1 pt where applicable;
- explicit alt text for F1–F4 and grayscale verification;
- fixed author/affiliation/rights metadata for supported figure formats;
- deterministic rebuild receipt for the normalized main set.

P18RC may not alter raw evidence, experimental validity, P13 claims, or inferential boundaries.

**P19 must not be frozen until P18RC passes.**

After P18RC PASS, proceed to **WP2-P19 — reviewer-facing supplementary atlas + sanitized artifact**.

## Immutable prohibitions

Do not claim scored P7B success, POWDER B1-vs-W1 advantage, generic `WellPulse beats MQTT`, a universal 52 dB threshold, deterministic RF-only recovery, exact broker latency from E10-D, population reliability from message counts/three FIT replicates, pooled FIT+POWDER inference, or field/agronomic validation not supported by the evidence.

## Handover close

`BRANCH_RESULT=PASS`

`VERIFIED_RESULT=F1_DETERMINISTIC_HOTFIX_ACCEPTED_AND_DURABLY_ARCHIVED`

`REMAINING_SCIENTIFIC_BLOCKERS=0`

`SCIENTIFIC_CONTENT_CHANGED=NO`

`SUBMISSION_AUTHORIZED=NO`

`NEXT_EXACT_MOVE=WP2_P18RC_MAIN_FIGURE_PRODUCTION_NORMALIZATION`
