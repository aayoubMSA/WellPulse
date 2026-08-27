# WellPulse GitHub Actions Workflow Registry

Canonical status date: 2026-08-27 — **P7B-R1 OFFLINE REPAIR QA PASS / ALL P7B LIVE SURFACES RETIRED**

This registry is the authoritative classification of workflow files under `.github/workflows/` on `main`.

## Operating rule

A workflow has current execution authority only when its YAML exists under `.github/workflows/` on the active branch and its trigger is permitted by current canonical state. Historical runs, deleted workflows, archived workflows and historical trigger files are provenance only.

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

Exactly **4** standing offline sentinels remain:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

No P6, P7, P7B-C or P7B-D live trigger remains.

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

## P7B-R1 offline repair surface

R1 introduced **no workflow and no trigger**. Its implementation is ordinary repository code exercised only by the standing offline `local-unit-tests.yml` gate:

- `scripts/wp2_p7b_path_contract.py`
- `scripts/wp2_p7b_c_node_r1.py`
- `scripts/wp2_p7b_preservation_helpers.sh`
- updated `tests/test_wp2_p7b_c_premutation.py`

Accepted R1 QA:

- Local Unit Tests run `33116073295`, job `98670934415`;
- SHA `695b31cba6c0256b3637223abdfef4f4b11bf6ca`;
- **65/65 PASS**;
- POWDER contact: NONE;
- scored execution: NONE.

The historical controller `powder/wp2_p7b_c_execute.sh` remains a provenance/implementation artifact and still names the old node runner. Because no live workflow reaches it, it has no current execution authority. A future R2 authority contract must explicitly bind any future controller to `scripts/wp2_p7b_c_node_r1.py` before a live workflow could be created.

## Canonical results

- P6: `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
- P7: `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
- P7B-E blocked closure: `docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`
- P7B-C retained status: `evidence/powder/wp2-p7b-c-live-status.md`
- P7B-D retained strict status: `evidence/powder/wp2-p7b-d-live-status.md`
- P7B-R1 repair closure: `docs/WP2_P7B_R1_RECEIVER_PATH_OBSERVABILITY_CLOSURE_2026-08-27.md`

## Current authority boundary

- `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`
- `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`
- `WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`
- `WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`
- `FUTURE_PHYSICAL_REQUALIFICATION_RECOMMENDATION=GO_CONDITIONAL`
- `SCORED_AUTHORIZATION=BLOCKED`
- `scored_runs_authorized=false`
- `WP3=BLOCKED`

No current workflow may create a POWDER reservation or execute physical/scored B1/W1/B2 work.

The exact next patch is offline-only `WP2-P7B-R2 — REQUALIFICATION AUTHORITY + CONTRACT FREEZE`. R2 must stop again before any live contact; any future replacement reservation requires separate explicit live authorization after R2.
