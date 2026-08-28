# WellPulse GitHub Actions Workflow Registry

Canonical status date: 2026-08-28 — **H2 OFFLINE / LIVE ACTION SURFACE RETIRED**

This registry is the authoritative classification of workflow files under `.github/workflows/` on `main`.

## Operating rule

A workflow has current execution authority only when its YAML exists under `.github/workflows/` on `main` and its trigger is permitted by the current canonical handover. Historical runs, deleted workflows, archived workflows and historical trigger files are provenance only.

For live/temporary workflows, retirement order is fail-safe: remove the workflow definition first, then remove its trigger/sentinel. Deleting a trigger while its workflow still exists is prohibited because trigger retirement can itself dispatch a path-filtered workflow.

## Active workflows — canonical bounded surface

Exactly **6** workflows remain active:

| Workflow | Class | External/live-system contact | Current authority |
|---|---|---|---|
| `local-gate-once.yml` | local pre-score QA | none | YES — offline/local only |
| `local-unit-tests.yml` | deterministic unit/regression QA | none | YES — offline/local only |
| `wp2-b2-semantics.yml` | B2 local semantics QA | localhost only | YES — non-scored local comparator semantics only |
| `wp2-golden-offline-qa.yml` | Golden/P7 offline QA | POWDER none; Drive none | YES — offline syntax/reconstruction/escrow/interlock QA only |
| `wp2-offpowder-artifact-qa.yml` | synthetic artifact transport QA | GitHub artifact transport only | YES — no POWDER science |
| `wp2-preintegration-static.yml` | static compatibility QA | none | YES — static only |

GitHub API read-back after cleanup confirmed that these are the complete contents of `.github/workflows/` on `main`.

## Root trigger sentinels

Exactly **4** standing offline sentinels remain:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

No P7B/RQ2/R3F live trigger remains on `main`.

## 2026-08-28 action-surface cleanup

Cleanup commit:

`ad37cf28bfb21e5bf9d3817a1e1f3aa3fd7332e8`

The cleanup retired **14 stale/temporary workflows** and **10 associated live/recovery triggers** that had accumulated after the earlier six-workflow baseline.

Retired workflow classes included:

- H1 aborted-run preservation workflow after evidence closure;
- R3F one-shot/existing-reservation live qualification workflows;
- RQ2 reservation, bootstrap, SSH cleanup, target-preflight and discriminator workflows;
- RQ2 install-only recovery workflows;
- CR2 recovery-preflight workflow;
- manual POWDER SSH environment-inventory workflow.

The associated P7B/RQ2/R3F path triggers were removed in the same atomic repository commit after the workflow definitions were removed from the resulting tree.

The reusable scripts, contracts, tests and evidence records were **not** deleted. Only executable GitHub Actions surfaces and their live/recovery trigger files were retired.

## Active-run verification

Immediately before cleanup:

- GitHub Actions `status=in_progress`: **0 runs**;
- GitHub Actions `status=queued`: **0 runs**.

After cleanup:

- GitHub Actions `status=in_progress`: **0 runs**.

Therefore no active run required cancellation. The cleanup prevents the retired workflows from being launched again from `main`.

## Scientific and authority state

This workflow cleanup changes **no scientific result, protocol, RF control, evidence classification or retry rule**.

Current project frontier remains:

`WP2-P7B-H2 — CONTROLLER/RESTORE-DOMAIN CONTRACT AMENDMENT QA + FUTURE REQUALIFICATION AUTHORITY DECISION`

with:

- `H2=OFFLINE_NOT_STARTED`;
- `B1=NULL_ABORTED_AFTER_Q3`;
- `W1=NOT_STARTED`;
- `B2=NOT_STARTED`;
- `SCORED=NO`;
- `LIVE_POWDER_AUTHORIZATION=NO`;
- `NEW_RESERVATION_AUTHORIZATION=NO`;
- `RF_AUTHORIZATION=NO`;
- `TEARDOWN_AUTHORIZATION=NO`;
- `WP3=BLOCKED`.

No current workflow may create a POWDER reservation, SSH to POWDER, mutate RF, restart testbed services, retry B1, execute W1/B2, teardown a reservation or run scored science.

Historical workflow provenance remains available through Git history and the existing P6/P7/P7B closure documents.
