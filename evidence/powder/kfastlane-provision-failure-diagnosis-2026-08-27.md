# WP2 K-Fastlane — Provisioning Failure Diagnosis

Date: 2026-08-27

## Scope

Read-only diagnosis of the already-failed compatibility experiment only.

- Target experiment UUID: `02bc305d-5d84-48f9-b518-dbebd1728ee6`
- Original compatibility workflow run: `33084240768`
- Diagnostic workflow run: `33086065236`
- New reservation created: **NO**
- POWDER mutation: **NO**
- Scientific run: **NO**

## Frozen Portal client

The diagnostic run installed and verified the already-frozen Portal client:

- Repository: `https://gitlab.flux.utah.edu/emulab/portal-api.git`
- Revision: `01be03b2f60c067815a7654437320dd981ca3617`
- Capture archive SHA-256: `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8`

## Authoritative observations

The diagnostic workflow queried the existing experiment with both standard and elaborated `experiment get`, and also queried `experiment list`.

Observed results:

- `GET_RC=148`
- `ELABORATE_GET_RC=148`
- `LIST_RC=0`
- Standard `get`: no JSON experiment record returned.
- Elaborated `get`: no JSON experiment record returned.
- `experiment list`: target UUID/name not present.
- Portal error for both `get` calls: `No such experiment`.

Therefore:

`FAILED_EXPERIMENT_RESOLUTION=ABSENT`

`FAILED_EXPERIMENT_LIST_PRESENCE=NO`

`COMPATIBILITY_CLEANUP_VERIFICATION=PASS`

This independently confirms that the failed compatibility experiment no longer resolves after cleanup.

## Provisioning failure root cause

The original live run observed only:

`provisioning -> failed`

before cleanup. It did not persist the detailed failed-state Portal record as an artifact before termination.

After cleanup, the authoritative Portal API no longer returns the experiment and the experiment is absent from the list. Consequently the detailed provisioning root cause cannot be recovered from the currently available Portal record.

Verdict:

`PROVISION_FAILURE_ROOT_CAUSE=NOT_RECOVERED_FROM_POST_CLEANUP_PORTAL_STATE`

No hardware shortage, quota issue, profile error, site outage, or other cause is inferred without evidence.

## Implication

This patch closes the cleanup-verification question but does not close K3 live semantics or authorize a replacement reservation by itself.

Current state remains:

- `K3_LIVE_PORTAL_BINDING=BLOCKED_ON_UNRESOLVED_PROVISIONING_FAILURE`
- `K4_LIVE_DETACH_GATE=NOT_RUN`
- `K5_LIVE_TIME_BINDING=NOT_RUN`
- `K6_CROSS_NODE_PROJ_GATE=NOT_RUN`
- `PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`
- `REBOOK_GOLDEN=false`
- `scored_runs_authorized=false`

## Shortest next technical correction

Before any replacement compatibility reservation, modify the compatibility workflow so that if Portal status becomes `failed`, the workflow freezes the failed-state JSON/error evidence before cleanup. Then, only after the already-known K7 static assertion defect is corrected, one bounded replacement compatibility-only reservation may be considered to finish K3-K6 live proofs.
