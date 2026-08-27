# WellPulse GitHub Actions Workflow Registry

Canonical status date: 2026-08-27 — **P7B-E CANONICAL BLOCKED CLOSURE / ALL P7B LIVE SURFACES RETIRED**

This registry is the authoritative classification of workflow files under `.github/workflows/` on `main`.

## Operating rule

A workflow has current execution authority only when its YAML exists under `.github/workflows/` on the active branch and its trigger is permitted by current canonical state. Historical runs, deleted workflows, archived workflows, and historical trigger files are provenance only.

## Active workflows — canonical bounded surface

Exactly **6** workflows are active:

| Workflow | Class | External/live-system contact | Current authority |
|---|---|---|---|
| `local-gate-once.yml` | local pre-score QA | none | YES — offline/local only |
| `local-unit-tests.yml` | deterministic unit/regression QA | none | YES — offline/local only |
| `wp2-b2-semantics.yml` | B2 local semantics QA | localhost only | YES — non-scored local comparator semantics only |
| `wp2-golden-offline-qa.yml` | Golden/P7 offline QA | POWDER none; Drive none | YES — offline syntax/reconstruction/escrow/interlock QA only |
| `wp2-offpowder-artifact-qa.yml` | synthetic artifact transport QA | GitHub artifact transport only | YES — no POWDER science |
| `wp2-preintegration-static.yml` | static compatibility QA | none | YES — static only |

## Root trigger sentinels

Exactly **4** standing sentinels remain:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

No P6, P7, P7B-C, or P7B-D live trigger remains.

## Retired live surface

All P6 one-shot/recovery/final-escrow workflows and all temporary P7/P7B live workflows/triggers are removed from `main` after their terminal evidence/status was captured. They remain available through Git history only and have **no current execution authority**.

P7B retired surfaces include:

- `.github/workflows/wp2-p7b-c-live.yml`
- `.wp2-p7b-c-live-trigger`
- `.github/workflows/wp2-p7b-d-evidence-survival.yml`
- `.wp2-p7b-d-trigger`
- `.github/workflows/wp2-p7b-d-evidence-survival-retry.yml`
- `.wp2-p7b-d-retry-trigger`

Deleting the P7B-C and first P7B-D trigger files caused one fail-closed retirement run each because GitHub path filters react to deletion pushes. P7B-C retirement run `33115086371` failed at the premutation authority gate and skipped reservation execution. P7B-D retirement run `33115100803` failed at the authority-boundary gate and skipped all live/preservation/teardown actions. Neither created a reservation nor contacted POWDER. These are QA provenance only.

## Canonical results

- P6: `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
- P7: `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
- P7B-E blocked closure: `docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`
- P7B-C retained status: `evidence/powder/wp2-p7b-c-live-status.md`
- P7B-D retained strict status: `evidence/powder/wp2-p7b-d-live-status.md`

## Current authority boundary

- `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`
- `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`
- `WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`
- `SCORED_AUTHORIZATION=BLOCKED`
- `scored_runs_authorized=false`
- `WP3=BLOCKED`

No current workflow may create a POWDER reservation or execute physical/scored B1/W1/B2 work. The exact next patch is offline R1 repair/regression QA. Any future live workflow requires a fresh bounded review and separate explicit live authorization.
