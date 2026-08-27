# WellPulse GitHub Actions Workflow Registry

Canonical status date: 2026-08-27

This registry is the authoritative classification of GitHub Actions workflow files on `main`.

## Operating rule

A workflow is runnable by normal GitHub Actions triggers only when its YAML file exists under `.github/workflows/` on the active branch. Archived workflow files are provenance only and must not be copied back or re-run as live testbed automation without a new compatibility review.

Historical workflow runs may remain visible in the GitHub Actions UI after archival. Their presence in the sidebar or run history does not make the archived YAML an approved active workflow.

## Active workflows

| Workflow | Class | Trigger | Repository permission | External/live-system contact | Allowed while `REBOOK_GOLDEN=false` | Notes |
|---|---|---|---|---|---|---|
| `local-gate-once.yml` | `ACTIVE_LOCAL_QA` | `.local-gate-trigger`, manual dispatch | contents: write | None | YES | Local unit/pre-score QA; writes sanitized local evidence only. |
| `local-unit-tests.yml` | `ACTIVE_LOCAL_QA` | changes to `src/wellpulse/**`, `tests/**`, `pyproject.toml`; PR equivalent | contents: write | None | YES | Deterministic local tests; evidence commit only on push. |
| `wp2-b2-semantics.yml` | `ACTIVE_LOCAL_SEMANTICS` | `.wp2-b2-semantics-trigger`, manual dispatch | contents: write | Localhost Mosquitto only; POWDER NONE | YES | Non-scored comparator semantics qualification; not a remote experiment. |
| `wp2-golden-offline-qa.yml` | `ACTIVE_OFFLINE_GOLDEN_QA` | selected Golden/A3 script changes, manual dispatch | contents: read | No POWDER mutation/contact | YES | Offline syntax/reconstruction/interlock QA only. It contains legacy A3 identifiers for regression checking and is not a launcher. |
| `wp2-h-preflight.yml` | `ACTIVE_LOCAL_PREFLIGHT` | `.wp2-h-preflight-trigger`, manual dispatch | contents: write | POWDER NONE | YES | Local pre-score implementation QA; records sanitized evidence. |
| `wp2-preintegration-static.yml` | `ACTIVE_STATIC_COMPATIBILITY_QA` | `.wp2-preintegration-static-trigger` on `main` | contents: read | POWDER NONE; Drive NONE | YES | Static integration-contract checks only. Uses pinned `actions/checkout` SHA and fixed `ubuntu-24.04`. |

## Active trigger sentinels

Exactly four root sentinel files are intentionally active:

- `.local-gate-trigger` -> `local-gate-once.yml`
- `.wp2-b2-semantics-trigger` -> `wp2-b2-semantics.yml`
- `.wp2-h-preflight-trigger` -> `wp2-h-preflight.yml`
- `.wp2-preintegration-static-trigger` -> `wp2-preintegration-static.yml`

`local-unit-tests.yml` and `wp2-golden-offline-qa.yml` use path filters rather than dedicated root trigger files.

## Archived workflow classes

| Archive | Count | Status | Authority |
|---|---:|---|---|
| `archive/workflows/a3-2026-08-27/` | 12 | `ARCHIVED_EXPIRED_A3` | Provenance only; A3 expired/removed. Never re-enable directly. |
| `archive/workflows/fit-final-2026-08-23/` | 16 | `ARCHIVED_CLOSED_FIT` | FIT science is FINAL PASS. Audit/reproducibility only. |
| `archive/workflows/powder-legacy-2026-08/` | 22 | `ARCHIVED_LEGACY_POWDER` | Historical live/probe/diagnostic/allocation workflows. No operational authority. |

Total workflow files removed from the active workflow path by cleanup C1-C3: **50**.

Archived trigger/request files are retained under the corresponding `archive/triggers/...` paths for provenance.

## Live POWDER prohibition

No active workflow is authorized to:

- create, schedule, start, terminate, extend, or otherwise mutate a POWDER experiment;
- SSH into a POWDER node;
- invoke `tmcc` against a live experiment;
- poll or probe a live scientific window independently;
- execute a Golden, H-calibration, B1/W1/B2 scored run;
- treat a historical `readonly`, `observer`, `status`, or `probe` label as evidence of non-mutating semantics.

Before any live GitHub Actions <-> POWDER workflow can be introduced or restored, both of the following must PASS:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Current mandatory state remains:

`H=UNFROZEN`

`scored_runs_authorized=false`

`REBOOK_GOLDEN=false`

## Historical Actions UI rule

GitHub may continue to show archived workflow names and their historical runs in the Actions sidebar/history. These entries are retained audit history. Do not use **Re-run jobs** or an old workflow's manual controls as a substitute for restoring an approved workflow through the current compatibility gate.

## Supply-chain note

Several local/offline workflows still reference version tags such as `actions/checkout@v4` or `actions/setup-python@v5`. This is acceptable only for their current local/offline classification. It does **not** satisfy the live-integration runtime pinning requirement. Any future workflow participating in GitHub Actions <-> POWDER integration must use the exact immutable revisions required by the compatibility matrix.
