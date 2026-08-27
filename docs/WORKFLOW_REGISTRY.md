# WellPulse GitHub Actions Workflow Registry

Canonical status date: 2026-08-27 — **P7B-R2 OFFLINE CONTRACT FREEZE PASS / ALL P7B LIVE SURFACES RETIRED**

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

There is no P7B-RQ1 live trigger and no P6/P7/P7B live trigger on `main`.

## Retired live surface

All P6 one-shot/recovery/final-escrow workflows and all temporary P7/P7B live workflows/triggers are removed from `main` after terminal evidence/status capture. They remain available through Git history only and have no current execution authority.

P7B retired surfaces include:

- `.github/workflows/wp2-p7b-c-live.yml`
- `.wp2-p7b-c-live-trigger`
- `.github/workflows/wp2-p7b-d-evidence-survival.yml`
- `.wp2-p7b-d-trigger`
- `.github/workflows/wp2-p7b-d-evidence-survival-retry.yml`
- `.wp2-p7b-d-retry-trigger`

Retirement deletion runs `33115086371` and `33115100803` failed closed before live actions. Neither created a reservation nor contacted POWDER.

## P7B-R1 offline repair surface

R1 introduced no workflow or trigger. Its ordinary repository code is exercised only through offline QA:

- `scripts/wp2_p7b_path_contract.py`
- `scripts/wp2_p7b_c_node_r1.py`
- `scripts/wp2_p7b_preservation_helpers.sh`
- `tests/test_wp2_p7b_c_premutation.py`

Accepted R1 QA: Local Unit Tests run `33116073295`, job `98670934415`, **65/65 PASS**; POWDER contact NONE.

## P7B-R2 offline authority-freeze surface

R2 also introduced **no workflow and no trigger**. It added only offline contract/validation artifacts:

- `experiments/WP-PWD01/p7b-requalification-r2-contract.json`
- `scripts/wp2_p7b_r2_validate_controller.py`
- `tests/test_wp2_p7b_r2_contract.py`
- `docs/WP2_P7B_R2_REQUALIFICATION_CONTRACT_FREEZE_2026-08-27.md`

Accepted R2 QA:

- Local Unit Tests run `33117108893`, job `98674462071`;
- SHA `b77609bfb9256a0eb189c0e5dd29a2f1f68c3bc2`;
- **73/73 PASS**;
- POWDER contact: NONE;
- reservation: NONE;
- scored execution: NONE.

R2 freezes replacement authority ID `P7B-RQ1`, but `P7B_RQ1_LIVE_AUTHORIZED=false`. The static validator proves the retired historical controller is not acceptable for RQ1 because it points to the old node runner. A future authority-bearing controller must use `scripts/wp2_p7b_c_node_r1.py`, exactly one reservation create, no automatic/second replacement, and evidence/read-back gates before teardown.

## Canonical results

- P6: `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
- P7: `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
- P7B-E blocked closure: `docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`
- P7B-C retained status: `evidence/powder/wp2-p7b-c-live-status.md`
- P7B-D retained strict status: `evidence/powder/wp2-p7b-d-live-status.md`
- P7B-R1 repair closure: `docs/WP2_P7B_R1_RECEIVER_PATH_OBSERVABILITY_CLOSURE_2026-08-27.md`
- P7B-R2 authority closure: `docs/WP2_P7B_R2_REQUALIFICATION_CONTRACT_FREEZE_2026-08-27.md`

## Current authority boundary

- `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`
- `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`
- `WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`
- `WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`
- `WP2_P7B_R2=PASS_ONE_REPLACEMENT_CONTRACT_FREEZE`
- `P7B_RQ1_AUTHORITY_CONTRACT=FROZEN`
- `P7B_RQ1_LIVE_AUTHORIZED=false`
- `SCORED_AUTHORIZATION=BLOCKED`
- `scored_runs_authorized=false`
- `WP3=BLOCKED`

No current workflow may create a POWDER reservation or execute physical/scored B1/W1/B2 work.

The exact next patch is live `WP2-P7B-R3 — ONE REPLACEMENT NON-SCORED PHYSICAL REQUALIFICATION + EVIDENCE SURVIVAL`, but it is **NOT AUTHORIZED**. A separate explicit live authorization is required before any workflow/trigger or POWDER contact is created.
