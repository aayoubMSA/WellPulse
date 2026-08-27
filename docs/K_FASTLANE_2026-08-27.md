# WP2 K-Fastlane — Shortest-Path / Highest-ROI K-Series Closure

Date: 2026-08-27

## Authority

The PI explicitly authorized working the remaining K-series as one bounded fastlane rather than stopping after every individual K patch.

This is a **K-series-only exception** to the ordinary patch-stop rule. It does not authorize a Golden run, H requalification, scored science, or scope expansion outside WP2.

## Objective

Close all K2–K8 work that can be closed without consuming POWDER reservation time, then use **one minimal non-scored compatibility reservation** for every irreducibly live proof.

Optimization rule:

`WP2 progress / (reservation time + manual burden + integration risk)`

## Fastlane structure

### Phase A — offline/controller-side batch

Execute without POWDER experiment contact:

- K2 transport redesign and controller-side off-POWDER escrow qualification;
- K3 conservative Portal lifecycle/error policy using the frozen Portal client;
- K4 receiver-detach implementation/static qualification;
- K5 reservation-time fail-close implementation/static qualification;
- K7 observation policy closure by eliminating independent RF polling from the protected path;
- K8 static compatibility reconciliation.

### Phase B — one minimal live compatibility reservation

Use one fresh non-scored reservation only to close facts that cannot be established offline:

1. exact profile/hardware/image/runtime fingerprints;
2. Portal live status/expiry field binding and authoritative time-budget input;
3. receiver detach/return timing on the actual POWDER SSH path;
4. `/proj/WellPulse` write → read → SHA-256 verification;
5. confirm no independent mutating RF observation is needed or used;
6. verify the safe controller-to-node topology required for later Golden automation.

No Golden workload, H calibration, or scored science is permitted in this compatibility reservation.

## K2 design decision — remove Drive from the pre-teardown critical path

The current rclone shared Google Drive OAuth client is a reliability/deprecation risk. The shortest robust path is:

- primary persistent safety copy: `/proj/WellPulse`;
- required off-POWDER pre-teardown copy: **GitHub Actions artifact**, produced by the same controller that launched the experiment;
- artifact upload/download round-trip must verify exact bytes/hash;
- Google Drive becomes a **post-run archival destination**, not a prerequisite for safe teardown.

This eliminates dedicated Google OAuth setup from the experiment-critical path while preserving a second copy outside POWDER. Drive archival may be added later without consuming reservation time.

## K3 lifecycle policy

Until stronger endpoint-specific semantics are needed, automation is deliberately conservative:

- only an explicit `ready` state can authorize node access/science preparation;
- API failure, 404, missing ID, malformed JSON, missing status, or unknown status can never authorize launch;
- experiment identity returned at creation must be rebound and verified by a subsequent `get` before use;
- expiry must come from the live Portal experiment record and must parse as an offset-aware timestamp before K5 can pass;
- termination is permitted only after evidence/teardown authorization and applies only to the exact bound experiment ID;
- retries may repeat read/status operations; mutating operations must not be blindly retried without identity reconciliation.

## K7 observation policy

There is no requirement to discover a read-only `tmcc attenuator` query before Golden if the design does not use one.

Protected-window rule:

- RF changes are performed only by the authoritative experiment process according to the frozen schedule;
- independent GitHub/HCI/status polling of RF attenuator state is prohibited;
- `tmcc attenuator` is classified as mutating unless a future separately qualified read-only interface is proven;
- HCI receives push events only.

This removes the unsafe observation dependency rather than trying to make it safe during science.

## Fastlane gate

Phase A may end as `PASS_OFFLINE_READY_FOR_SINGLE_LIVE_COMPATIBILITY_RESERVATION` even though K4/K5/K6 contain live evidence items.

Full K8 can pass only after the one live compatibility reservation closes those live items.

Until then:

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`
