# Archived POWDER workflows — August 2026

Status: ARCHIVE-ONLY / NOT ACTIVE

This directory preserves historical POWDER GitHub Actions workflows that were used for early API probing, SSH/plumbing checks, G3 attach/simstack work, H-calibration scheduling/status/release operations, lifecycle operations, and other live diagnostics.

They were removed from `.github/workflows/` during repository hygiene Patch C3 because the current project state requires:

- `REBOOK_GOLDEN=false`;
- `PRE_INTEGRATION_COMPATIBILITY_GATE` and `LIVE_HCI_AND_RAW_EVIDENCE_GATE` to pass before another live POWDER experiment;
- unknown or unqualified command/API side effects to be treated as mutating/unsafe;
- no independent live probes during protected scientific execution.

Archive policy:

- preserve exact workflow blobs and Git history;
- do not execute archived workflows directly;
- do not copy an archived workflow back into `.github/workflows/` without a new compatibility review and explicit current-purpose qualification;
- historical names such as `readonly`, `observer`, `probe`, or `status` are not evidence that an operation is non-mutating.

Active workflows after C3 are intentionally limited to local/offline/static QA and semantics checks that do not allocate, probe, mutate, or control POWDER resources.
