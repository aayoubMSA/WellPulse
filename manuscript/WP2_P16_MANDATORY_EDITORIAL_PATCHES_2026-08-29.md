# WP2-P16 — Mandatory Publication-Facing Editorial Patches

Date: 2026-08-29  
Status: **FROZEN / APPLY BEFORE SUBMISSION-TYPESETTING**

These patches change publication presentation only. They do **not** change any result, claim, figure, table, evidence class, or experiment status.

## M1 — Title

Replace the P15 working title:

`WellPulse: Failure-Domain-Aware Validation of Durable IIoT Telemetry Across Embedded and Controlled-RF Testbeds`

with the more accurate publication-facing title:

`WellPulse: Failure-Domain-Aware Validation of Durable IIoT Telemetry with Embedded Durability and Controlled-RF Characterization`

Reason: the original title can be read as if the W1 architecture comparison itself was repeated on POWDER. The revised title preserves the two evidence roles explicitly.

## M2 — Remove internal scored/P7B language from the submitted manuscript

Repository/control files must continue to preserve:

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

However, publication-facing prose should not use `P7B`, `scored`, or `non-scored` as reader-facing scientific terminology.

Preferred publication wording:

> The POWDER component was a separately executed reference characterization campaign and was not used to estimate an architecture-level W1-versus-baseline effect.

Where the paper currently says that a scored comparison was not completed, use:

> The final POWDER evidence does not contain a completed architecture-level W1-versus-standard-MQTT comparison; therefore no such effect is claimed.

## M3 — Strengthen W1 implementation description from canonical source

Replace/extend the conceptual architecture description with the following evidence-grounded implementation paragraph:

> In the evaluated W1 implementation, each telemetry record carries a stable application identity derived from the run identifier, boot identifier, and monotonically formatted sequence number (`run_id:boot_id:sequence`). The record is serialized canonically and assigned a SHA-256 checksum. Local durable state is maintained in SQLite with write-ahead logging (`WAL`) and `synchronous=FULL`; records have explicit `PENDING` and `SENT` states. Re-enqueuing the identical record identity/content is treated idempotently, whereas reuse of an existing record identity with conflicting payload or checksum raises an integrity error. Final delivery is assessed from receiver-side identity reconciliation rather than sender publish status alone.

Canonical implementation authorities:

- `src/wellpulse/records.py`
- `src/wellpulse/store.py`

This is implementation description, not a new experimental result.

## M4 — Preserve baseline boundary every time the FIT effect is summarized

Any compact summary of the +20 percentage-point FIT result must identify B0 as a **non-durable publish-only baseline**.

Never shorten the result to:

- `WellPulse improves MQTT reliability by 20%.`
- `WellPulse outperforms MQTT by 20 pp.`

Preferred short form:

> Under the tested FIT outage conditions, W1 achieved a repeated +20 percentage-point final-completeness difference relative to the non-durable B0 baseline.

## M5 — Explicitly state the two evidence roles early in Methods

Add the following publication-facing sentence near the start of Methods:

> The two testbeds were assigned non-overlapping inferential roles: FIT IoT-LAB supports the architecture-level B0-versus-W1 record-survival comparison, whereas POWDER supports physical-path degradation and recovery characterization; results are not pooled across platforms.

## M6 — Remove internal workflow names from reader-facing prose

Replace manuscript wording such as:

`The P9–P14 workflow reconstructs...`

with:

> The analysis workflow reconstructs numerical results from immutable evidence, freezes claim wording against a claim–evidence matrix, and generates displays reproducibly before manuscript interpretation.

Do not mention WP/Patch identifiers in the submitted body unless needed in an artifact appendix.

## M7 — Remove the internal manuscript-control note from the submission manuscript

The section headed:

`Internal manuscript-control note`

is repository governance and must not appear in the submitted paper.

Its prohibitions remain authoritative internally.

## M8 — Abstract wording for POWDER

Replace publication-facing phrasing equivalent to:

`a separate manual non-scored POWDER campaign`

with:

> a separate manually executed POWDER reference characterization campaign

and, if space permits:

> not used for architecture-level effect estimation.

## M9 — Gaspar et al. treatment

Until full text is reviewed, keep the Gaspar et al. 2026 citation limited to bibliographic/scope-level positioning. Do not attribute a specific method, fault model, result, comparator, or quantitative finding that has not been independently recovered.

A final full-text comparison is required before submission if accessible.

## M10 — Reproducibility/public-data wording

Do not promise release of the complete private preservation archives.

Preferred wording:

> Analysis code, derived non-sensitive data, figure-generation scripts, manifests, and releasable evidence will be provided in a sanitized artifact package. Private platform captures and credential-bearing preservation material are excluded from public release.

## M11 — Do not expand the display set during typesetting

P14 remains authoritative:

- 4 final figures;
- 3 final quantitative tables;
- no combined FIT+POWDER reliability visualization;
- no generic recovery-latency plot mixing incompatible clocks;
- no threshold line labelled as a universal 52 dB failure point.

A publisher-required formatting transformation is allowed; scientific content changes require reopening QA.

## M12 — Submission-facing status line

Remove internal lines such as:

`Manuscript stage: P15...`

`Status: INTERNAL SCIENTIFIC DRAFT...`

from the submitted manuscript. Keep them only in repository-controlled working copies.

## Closure

`P16_EDITORIAL_PATCHES_FROZEN=12`

`P16_PATCHES_CHANGE_RESULTS=NO`

`P16_PATCHES_CHANGE_CLAIMS=NO`

`P16_PATCH_APPLICATION_REQUIRED_BEFORE_SUBMISSION=YES`
