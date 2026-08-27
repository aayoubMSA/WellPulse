# WellPulse GitHub Actions Workflow Registry

Canonical status date: 2026-08-27 — **WP2-P6 ACTIVE after short QA PASS**

This registry is the authoritative classification of GitHub Actions workflow files on `main`.

## Operating rule

A workflow is runnable by normal GitHub Actions triggers only when its YAML file exists under `.github/workflows/` on the active branch. Historical workflow runs and deleted/archived YAML are provenance only and must not be restored or re-run as live testbed automation without a new compatibility review and explicit authorization.

## Active workflows — bounded surface during P6

Exactly **7** workflows are active during the one-shot P6 execution window:

| Workflow | Class | Trigger | External/live-system contact | Current authority | Notes |
|---|---|---|---|---|---|
| `local-gate-once.yml` | `ACTIVE_LOCAL_QA` | `.local-gate-trigger`, manual dispatch | None | YES | Local unit/pre-score QA only. |
| `local-unit-tests.yml` | `ACTIVE_LOCAL_QA` | code/test paths; PR equivalent | None | YES | Deterministic local tests. |
| `wp2-b2-semantics.yml` | `ACTIVE_LOCAL_SEMANTICS` | `.wp2-b2-semantics-trigger`, manual dispatch | Localhost only | YES | Non-scored local comparator semantics QA. |
| `wp2-golden-offline-qa.yml` | `ACTIVE_OFFLINE_GOLDEN_QA` | selected Golden implementation paths, manual dispatch | POWDER NONE; Drive NONE | YES | Offline syntax, passive-HCI, reconstruction, escrow/interlock QA. |
| `wp2-offpowder-artifact-qa.yml` | `ACTIVE_OFFLINE_ARTIFACT_QA` | `.wp2-offpowder-artifact-qa-trigger` | POWDER NONE; Drive NONE | YES | Synthetic artifact upload/download/hash QA. |
| `wp2-preintegration-static.yml` | `ACTIVE_STATIC_COMPATIBILITY_QA` | `.wp2-preintegration-static-trigger` | POWDER NONE; Drive NONE | YES | Static integration-contract checks. |
| `wp2-p6-golden.yml` | `ACTIVE_ONE_SHOT_LIVE_P6` | `.wp2-p6-golden-trigger` | **POWDER + GitHub artifact transport** | **AUTHORIZED FOR EXACTLY ONE NON-SCORED P6 RUN** | Performs short premutation offline QA, advisory `resinfo.php` check, exact Portal/profile identity gates, one Golden G0-G10 node phase, `/proj` escrow, controller pull, GitHub artifact round-trip, and teardown only after verified evidence closure. |

The P6 workflow is a new bounded launcher derived from the accepted K8/AUDIT-R1/P5 contracts. It does **not** reactivate historical K/A3 workflows and does not use Google Drive/rclone as teardown authority.

## Root trigger sentinels

The four standing offline/static sentinels remain:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

During the P6 one-shot window, one additional sentinel is authorized:

- `.wp2-p6-golden-trigger` -> `wp2-p6-golden.yml`

This P6 sentinel must not be reused for a second Golden run. After P6 reaches a terminal verdict, retire the P6 live workflow/sentinel or otherwise remove its live authority during canonical closure.

## P6 live authority boundary

User continuation on 2026-08-27 explicitly authorizes WP2-P6 after the recorded short QA PASS.

Current controls:

`P6_SHORT_QA=PASS`

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

`HCI_CONTROL_ACTIONS_ENABLED=false`

`REBOOK_GOLDEN=true` — **one P6 non-scored reservation/run only**

`scored_runs_authorized=false`

The P6 workflow may:

1. perform the read-only advisory resource-information check immediately before booking;
2. create exactly one reservation using the frozen profile/bindings;
3. use authoritative Portal READY/manifest/time guards;
4. SSH to the exact manifested nodes for pre-science setup and the single Golden run;
5. execute the frozen RF treatment inside the Golden orchestrator;
6. preserve raw evidence to `/proj/WellPulse` after protected observation/reconstruction;
7. controller-pull the verified persistent bundle;
8. upload/download the exact TAR through the already-qualified GitHub artifact actions;
9. emit teardown authority only after outer/internal SHA-256 verification;
10. terminate the experiment only after `EVIDENCE_ESCROW_GATE=PASS` and `TEARDOWN_AUTHORIZED=YES`.

It may **not** execute H calibration, B1/W1/B2 scored work, reopen RF calibration/K1-K8/H1 salvage, add independent HCI probes, silently substitute hardware/profile/bindings, or use Drive as mandatory evidence authority.

If execution fails **before protected science starts**, bounded reservation cleanup is allowed. If it fails **after protected science starts** without verified final evidence closure, automatic teardown is prohibited and the experiment is left live to protect evidence.

## Historical retired surface

The following remain retired and provenance-only:

- `wp2-h-preflight.yml`;
- `wp2-k3-portal-cli-contract-qa.yml`;
- `wp2-k7-observation-guard.yml`;
- `wp2-kfastlane-failed-create-diagnostic.yml`;
- `wp2-kfastlane-live-compat.yml`;
- `wp2-kfastlane-live-compat-v2.yml`;
- `wp2-kfastlane-provision-failure-diagnose.yml`;
- `wp2-profile-metadata-readonly.yml`;
- archived A3/legacy Golden owner workflows.

Historical Actions UI entries are not current authority and must not be re-run to bypass P6 control.
