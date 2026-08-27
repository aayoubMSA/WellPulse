# Repository Workflow Hygiene — Final QA

Date: 2026-08-27
Original patch: C4
Current reconciliation: **AUDIT-R1**
Repository: `aayoubMSA/WellPulse`
Branch: `main`

## Current verdict

`REPOSITORY_WORKFLOW_HYGIENE=PASS_AUDIT_R1_RECONCILED`

This verdict concerns repository workflow/trigger hygiene only. It does not authorize a POWDER reservation, Golden rehearsal, H calibration, or scored run.

## AUDIT-R1 correction to the original C4 record

The original C4 snapshot was accurate when written, but later K-fastlane work added K-era QA/diagnostic/live compatibility workflows and trigger sentinels. It also retained the now-superseded `wp2-h-preflight.yml`. Therefore the original statement that the active tree still contained exactly the original six workflows and four sentinels became stale.

AUDIT-R1 re-enumerated the actual tree, retired the stale runnable H/K surface without dispatching it, then re-enumerated again.

## Verified current active set

Exactly **6** workflow YAML files remain under `.github/workflows/`:

1. `local-gate-once.yml`
2. `local-unit-tests.yml`
3. `wp2-b2-semantics.yml`
4. `wp2-golden-offline-qa.yml`
5. `wp2-offpowder-artifact-qa.yml`
6. `wp2-preintegration-static.yml`

All six are local/offline/static. None has current authority to create/control/terminate a POWDER experiment, SSH to POWDER, run Golden, run H calibration, execute scored work, or reopen K1-K8/RF calibration.

Exactly **4** root sentinel trigger files remain:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

## Retired by AUDIT-R1

Removed from the active Actions path:

- `wp2-h-preflight.yml`;
- `wp2-k3-portal-cli-contract-qa.yml`;
- `wp2-k7-observation-guard.yml`;
- `wp2-kfastlane-failed-create-diagnostic.yml`;
- `wp2-kfastlane-live-compat.yml`;
- `wp2-kfastlane-live-compat-v2.yml`;
- `wp2-kfastlane-provision-failure-diagnose.yml`;
- `wp2-profile-metadata-readonly.yml`.

Their eight corresponding root sentinels were removed only after the YAML files were no longer active. No workflow was dispatched as part of this cleanup. Historical content/runs remain preserved in Git history and the K closure evidence remains authoritative.

## Acceptance checks

| Check | Result | Evidence / interpretation |
|---|---|---|
| Active workflow inventory bounded/intentional | PASS | Re-enumerated current tree: exactly 6. |
| Active root sentinel integrity | PASS | Re-enumerated current root: exactly 4. |
| Active K live/diagnostic execution surface | PASS | 0 K-era live/diagnostic workflows remain active. |
| Active old-H preflight surface | PASS | 0; old W1-derived H procedure is superseded/fail-closed. |
| Active FIT execution surface | PASS | 0 FIT workflows active. |
| Active expired-A3 execution surface | PASS | 0 A3-specific workflows active. |
| Active POWDER allocation/control/SSH | PASS | None in the six active workflows. |
| Scientific state unchanged | PASS | `scored_runs_authorized=false`; Q0-Q3 and H1/K evidence untouched. |
| Golden authorization unchanged | PASS | `REBOOK_GOLDEN=false`. |
| Current horizon terminology | PASS | `H_app=300 s from t_service_ready`; outcome-derived H recalibration prohibited. |
| Provenance preserved | PASS | Earlier archives remain; AUDIT-R1 deletions remain in Git history. |
| Canonical workflow registry reconciled | PASS | `docs/WORKFLOW_REGISTRY.md`. |

## Earlier cleanup provenance

Earlier C1-C3 archived 12 expired A3 workflows, 16 FIT workflows, and 22 legacy/live POWDER workflows: **50** workflows removed from the active path before AUDIT-R1.

AUDIT-R1 then retired **8 additional** stale H/K-era workflows from the active path. These eight are preserved by Git history rather than duplicated into the archive tree.

## Current gate state

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

`H_app=300 s from t_service_ready`

## Scope boundary

This AUDIT-R1 hygiene reconciliation does **not** implement or accept the passive HCI/raw-evidence runtime gate. It only removes stale executable surfaces and restores the repository control record. HCI/raw-evidence closure remains the next separately authorized patch after AUDIT-R1 stops.
