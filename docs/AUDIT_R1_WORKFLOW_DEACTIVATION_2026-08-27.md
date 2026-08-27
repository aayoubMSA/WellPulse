# AUDIT-R1 Workflow Deactivation Provenance — 2026-08-27

Scope: offline governance reconciliation only. No workflow in this record was dispatched, and no POWDER resource was contacted or mutated.

## Governing rule

Completed K-series live/diagnostic workflows and the obsolete H-calibration preflight are removed from the active `.github/workflows/` surface. Their exact historical content remains preserved in Git history at the blob SHA recorded below. Trigger sentinels are likewise removed from the active repository root. This is deactivation, not evidence deletion.

K1-K8 remain PASS/CLOSED. H1 remains `VALID_W1_RECOVERY_FAILURE`. RF calibration remains PASS/FROZEN. This cleanup does not reopen or reinterpret any scientific result.

## Deactivated workflows

| Active path removed | Historical blob SHA | Reason |
|---|---|---|
| `.github/workflows/wp2-h-preflight.yml` | `f56dfff1ec5aca8ae679eebd12cdcdc0a2798e5b` | Obsolete pre-amendment W1-derived H calibration preflight; Recovery Semantics Amendment v1 freezes `H_app=300 s` from `t_service_ready`. |
| `.github/workflows/wp2-k3-portal-cli-contract-qa.yml` | `d7a42a685008886bfc5307f0de04709b1357961c` | K3 closed; no active operational authority required. |
| `.github/workflows/wp2-k7-observation-guard.yml` | `947da614a860a772dad04badfe441b551cc1052f` | K7 closed; historical compatibility evidence only. |
| `.github/workflows/wp2-kfastlane-failed-create-diagnostic.yml` | `0f26705710354be5aab10f71be63d2264801e4f5` | Completed K-fastlane diagnostic; no longer runnable. |
| `.github/workflows/wp2-kfastlane-live-compat.yml` | `a8f956e9c7f5f4541cf8b3e9ebaa8d9addcf9ac4` | Superseded completed live K-fastlane implementation. |
| `.github/workflows/wp2-kfastlane-live-compat-v2.yml` | `1014c8066db72466cdf426af1a93af62462bb255` | Decisive K-fastlane implementation is completed and closed; retain as history only. |
| `.github/workflows/wp2-kfastlane-provision-failure-diagnose.yml` | `8387ac82d8f06d9633c85b9cf388406c07d8e0af` | Completed provisioning diagnostic; no operational authority remains. |
| `.github/workflows/wp2-profile-metadata-readonly.yml` | `9e63d8c4eafbdc880116ed290d14ba3b1ed0784e` | K-era metadata probe; K compatibility is closed and future live integration is separately gated. |

## Deactivated root trigger sentinels

| Root path removed | Historical blob SHA |
|---|---|
| `.wp2-h-preflight-trigger` | `57b624256aaf307a002293f8bde843594f47e673` |
| `.wp2-k3-portal-cli-contract-trigger` | `098a77e0392df7a4e8fa68767fbc9d84b10dd59c` |
| `.wp2-k7-observation-guard-trigger` | `7bcd336773d8130589962d1c66899048fdff91f0` |
| `.wp2-kfastlane-failed-create-diagnostic-trigger` | `ee1cf0ceb50472f2e82c455c999700a67f2f0c35` |
| `.wp2-kfastlane-live-compat-trigger` | `72bf9f9d81ed2423c3131b50bc9569f94795b001` |
| `.wp2-kfastlane-live-compat-v2-trigger` | `f83348003c0adb990455d1ce6e4756e380893753` |
| `.wp2-kfastlane-provision-failure-diagnose-trigger` | `d31b3e5cebfef32f1e86225958974ddf66ed3721` |
| `.wp2-profile-metadata-readonly-trigger` | `3139a80d0f93ff19831fbdbe3222e7442a509345` |

## Intended post-reconciliation active workflow surface

The bounded active set is:

1. `local-gate-once.yml` — local QA.
2. `local-unit-tests.yml` — deterministic local unit tests.
3. `wp2-b2-semantics.yml` — localhost-only non-scored comparator semantics.
4. `wp2-golden-offline-qa.yml` — offline Golden syntax/reconstruction/interlock QA only.
5. `wp2-offpowder-artifact-qa.yml` — GitHub artifact transport round-trip QA; no POWDER/Drive contact.
6. `wp2-preintegration-static.yml` — static compatibility QA only.

The only root trigger sentinels intended to remain active are:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

`REBOOK_GOLDEN=false` and `scored_runs_authorized=false` remain unchanged.
