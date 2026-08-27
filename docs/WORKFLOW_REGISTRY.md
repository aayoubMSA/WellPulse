# WellPulse GitHub Actions Workflow Registry

Canonical status date: 2026-08-27 — **AUDIT-R1 reconciled**

This registry is the authoritative classification of GitHub Actions workflow files on `main`.

## Operating rule

A workflow is runnable by normal GitHub Actions triggers only when its YAML file exists under `.github/workflows/` on the active branch. Historical workflow runs and deleted/archived YAML are provenance only and must not be restored or re-run as live testbed automation without a new compatibility review and explicit authorization.

## Active workflows — verified inventory

Exactly **6** workflows are active:

| Workflow | Class | Trigger | External/live-system contact | Allowed while `REBOOK_GOLDEN=false` | Notes |
|---|---|---|---|---|---|
| `local-gate-once.yml` | `ACTIVE_LOCAL_QA` | `.local-gate-trigger`, manual dispatch | None | YES | Local unit/pre-score QA only. |
| `local-unit-tests.yml` | `ACTIVE_LOCAL_QA` | changes to `src/wellpulse/**`, `tests/**`, `pyproject.toml`; PR equivalent | None | YES | Deterministic local tests. |
| `wp2-b2-semantics.yml` | `ACTIVE_LOCAL_SEMANTICS` | `.wp2-b2-semantics-trigger`, manual dispatch | Localhost test services only; POWDER NONE | YES | Non-scored local comparator semantics QA; no remote experiment. |
| `wp2-golden-offline-qa.yml` | `ACTIVE_OFFLINE_GOLDEN_QA` | selected Golden/A3 implementation paths, manual dispatch | POWDER NONE | YES | Offline syntax/reconstruction/interlock QA only; not a launcher. |
| `wp2-offpowder-artifact-qa.yml` | `ACTIVE_OFFLINE_ARTIFACT_QA` | `.wp2-offpowder-artifact-qa-trigger` | POWDER NONE; Drive NONE | YES | Synthetic GitHub artifact upload/download/hash round-trip QA only. |
| `wp2-preintegration-static.yml` | `ACTIVE_STATIC_COMPATIBILITY_QA` | `.wp2-preintegration-static-trigger` on `main` | POWDER NONE; Drive NONE | YES | Static integration-contract checks only. |

The active directory was re-enumerated after AUDIT-R1 cleanup. No K-series live/diagnostic workflow and no H-calibration/preflight workflow remains under `.github/workflows/`.

## Active root trigger sentinels — verified inventory

Exactly **4** root sentinel files remain:

- `.local-gate-trigger` -> `local-gate-once.yml`
- `.wp2-b2-semantics-trigger` -> `wp2-b2-semantics.yml`
- `.wp2-offpowder-artifact-qa-trigger` -> `wp2-offpowder-artifact-qa.yml`
- `.wp2-preintegration-static-trigger` -> `wp2-preintegration-static.yml`

`local-unit-tests.yml` and `wp2-golden-offline-qa.yml` use path filters rather than dedicated root sentinels.

## AUDIT-R1 retired active surface

The following workflows were removed from the active Actions path because their gates are closed/superseded and keeping them runnable created unnecessary accidental-execution surface:

- `wp2-h-preflight.yml` — superseded old W1-derived H procedure;
- `wp2-k3-portal-cli-contract-qa.yml` — K3 closed;
- `wp2-k7-observation-guard.yml` — K7 closed;
- `wp2-kfastlane-failed-create-diagnostic.yml` — completed diagnostic;
- `wp2-kfastlane-live-compat.yml` — completed live compatibility path;
- `wp2-kfastlane-live-compat-v2.yml` — decisive completed K-fastlane path;
- `wp2-kfastlane-provision-failure-diagnose.yml` — completed diagnostic;
- `wp2-profile-metadata-readonly.yml` — K-era profile metadata probe.

Their corresponding eight root trigger sentinels were removed **only after** their workflow YAML was removed, preventing trigger deletion commits from dispatching them. Historical content and runs remain recoverable from Git history; K1-K8 scientific/infrastructure evidence is unchanged.

## Earlier archived workflow classes

| Archive | Count | Status | Authority |
|---|---:|---|---|
| `archive/workflows/a3-2026-08-27/` | 12 | `ARCHIVED_EXPIRED_A3` | Provenance only; A3 expired/removed. |
| `archive/workflows/fit-final-2026-08-23/` | 16 | `ARCHIVED_CLOSED_FIT` | FIT science is FINAL PASS; audit only. |
| `archive/workflows/powder-legacy-2026-08/` | 22 | `ARCHIVED_LEGACY_POWDER` | Historical live/probe/diagnostic/allocation workflows. |

Earlier cleanup C1-C3 removed **50** workflows from the active path. AUDIT-R1 retired **8 additional** stale H/K-era workflows from the active path; these eight are retained by Git history rather than duplicated into the archive tree.

## Live POWDER prohibition

No active workflow is authorized to:

- create, schedule, start, terminate, extend, or otherwise mutate a POWDER experiment;
- SSH into a POWDER node;
- invoke `tmcc` against a live experiment;
- poll or probe a live scientific window independently;
- execute Golden, H calibration, or B1/W1/B2 scored work;
- reopen K1-K8 or RF calibration.

Current mandatory state:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`

`H_app=300 s from t_service_ready (FROZEN)`

`outcome_derived_H_calibration=PROHIBITED`

`scored_runs_authorized=false`

`REBOOK_GOLDEN=false`

## Historical Actions UI rule

GitHub may continue to show deleted/archived workflow names and historical runs in the Actions UI. Those entries are audit history, not current authorization. Do not use **Re-run jobs** or historical manual controls to bypass the current gates.

## Supply-chain note

Local/offline workflows are not automatically qualified for live integration. Any future GitHub Actions <-> POWDER path must satisfy the frozen compatibility matrix and use the required immutable action/runtime revisions before it gains live authority.
