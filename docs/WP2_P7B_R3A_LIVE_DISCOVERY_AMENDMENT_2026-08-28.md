# WP2-P7B-R3A — Live-Run Discovery Amendment

**Date:** 2026-08-28  
**Applies to:** `docs/WP2_P7B_R3A_CONTRACT_MICRO_AUDIT_2026-08-28.md`  
**Authority:** corrective provenance amendment; this file supersedes any R3A statement claiming that no live R3 workflow had started.

## Corrected live-state record

During the contract micro-audit, repository inspection discovered that a temporary R3 live workflow and trigger had already been created before the audit HOLD was established:

- workflow: `.github/workflows/wp2-p7b-r3-live.yml`;
- trigger: `.wp2-p7b-r3-live-trigger`;
- authority ID: `P7B-RQ1`;
- workflow run: `33119810043`;
- job: `98683578418`;
- run head SHA: `b174ca46fe3af2dae4e50b68bd489ce09a271ea9`;
- observed job state during audit: `in_progress`;
- completed steps: checkout, live authority/premutation gate, controller dependency installation;
- observed active step: `Execute one P7B-RQ1 reservation and persistent escrow`.

The available GitHub job-step state does **not** prove whether `portal-cli experiment create` had already completed. Therefore reservation creation is recorded as **PENDING VERIFICATION**, not inferred.

## Immediate containment

To prevent any additional R3 run from being started from `main` during the contract audit:

1. the R3 workflow was deleted first from `main` in commit `5b8633bc46ffec353fd565ccfc3b195571c9cebf`;
2. only after the workflow was removed, the R3 trigger was deleted in commit `1e0bccd910ddfb9312344921ea921a62eaade090`.

The order is deliberate: deleting the trigger while the workflow still existed could itself have matched the workflow's `paths` filter and launched another run.

These repository deletions prevent new R3 runs but do not cancel an already-running GitHub Actions job because that job executes from its checked-out head SHA.

The currently available GitHub connector exposes run/job inspection and rerun operations but no workflow-run cancellation operation. The user was therefore instructed to use GitHub Actions UI `Cancel workflow` for run `33119810043` if it was still running.

## Current safety state

- new R3 workflow on `main`: **NO**;
- new R3 trigger on `main`: **NO**;
- automatic retry: **NO**;
- second replacement authority: **NO**;
- scored authorization: **BLOCKED**;
- contract repair remains required before any future R3 execution surface may be recreated.

## Audit implication

The discovery strengthens the R3A finding: authority, trigger creation, contract review, and live execution were not sufficiently separated by one machine-enforced state transition. Future authority must therefore be represented as an explicit, one-shot, machine-readable state object and the live workflow must not exist before the complete audited contract gate passes.

`R3A_LIVE_DISCOVERY=RECORDED`

`R3_NEW_LIVE_SURFACE=DISARMED_ON_MAIN`

`EXISTING_RUN_33119810043=IN_PROGRESS_AT_LAST_VERIFICATION`

`RESERVATION_STATUS=PENDING_VERIFICATION`

`SCORED_AUTHORIZATION=BLOCKED`
