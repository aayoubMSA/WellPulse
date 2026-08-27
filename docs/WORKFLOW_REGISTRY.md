# WellPulse GitHub Actions Workflow Registry

Canonical status date: 2026-08-27 — **P6 CLOSED / P7 HARDENING PASS / SCORED AUTHORIZATION BLOCKED**

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

No P6 or P7 live trigger remains.

## Retired live surface

All P6 one-shot, same-reservation recovery, G8 salvage, final escrow, and P7 temporary closure workflows/triggers were removed after terminal evidence was captured. They remain recoverable through Git history only and have **no current execution authority**.

P6 canonical result: `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`.

P7 canonical decision: `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`.

## Current authority boundary

- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`
- `WP2_P7_HARDENING_QA=PASS`
- `SCORED_AUTHORIZATION=BLOCKED`
- `scored_runs_authorized=false`
- `WP3=BLOCKED`

No current workflow may create a POWDER reservation or execute scored B1/W1/B2 work. A future live workflow requires a new bounded compatibility/authorization review and explicit continuation from the canonical handover.
