# WellPulse — Next Gate

Status date: 2026-08-27

## Current frontier

- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`
- `WP2_P7_HARDENING_QA=PASS`
- `SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`
- `scored_runs_authorized=false`
- `WP3=BLOCKED`
- scientific weighted completion: **20%**

P6 completed one scientifically valid **non-scored** Golden rehearsal with verified raw evidence, persistent `/proj` escrow, independent GitHub artifact round-trip/hash verification, and confirmed teardown. P7 then hardened the reusable execution/reconstruction path and passed offline closure QA, but the scored campaign is still blocked by mandatory arm/restart-domain physical qualification.

## Next bounded patch — not started

`WP2-P7B — SINGLE NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION`

Status: **BLOCKED / NOT STARTED pending explicit continuation**.

The purpose is to close all remaining physical pre-score gates with one minimum-information reservation rather than several independent experiments.

### P7B must prove, prospectively and non-scored

1. **B1 accepted/unacknowledged instrumentation** on the real remote LTE/MQTT path.
2. **B1/W1 matching**: identical low-level Paho/runtime/session settings, with W1 differing only by application-level durable SQLite/reconciliation semantics.
3. **S3 restart-domain separation**:
   - telemetry generator outside the restarted gateway/client process;
   - generation continues at 1 Hz;
   - process restart only, no node reboot;
   - W1 durable state survives;
   - B1 volatile client state is recreated with same intra-run identity;
   - source sequence continuity + exact restart timestamps/downtime preserved.
4. **B2 remote qualification**: exact Eclipse Paho Java 1.2.5 durable-client configuration on the same LTE/TLS/payload/evidence path, including persistence across the required client-process restart.
5. **Full washout/readiness enforcement** for B1/W1/B2 before any scored campaign: Q0 user plane, experimental route, fresh namespace/application state, no unresolved broker/session residue, calibrated radio envelope, frozen runtime/config, healthy clocks/evidence capture.

Any application behavior observed in P7B is qualification evidence only. It may not be used to tune the protocol, choose H, select a favorable arm, change Q0-Q3, or replace an unfavorable future scored outcome.

### If P7B PASS

STOP the live experiment only after the same evidence-survival chain used in P6 has closed. Then, offline:

1. reconcile `run-matrix.yaml` gate-status fields;
2. freeze the immutable pre-score reproducibility snapshot;
3. issue a separate explicit `SCORED_AUTHORIZATION=PASS|BLOCKED` decision;
4. only after PASS may WP3 scored execution be opened.

### If P7B fails

Preserve the failure and classify it as a pre-score qualification result. Do not create another reservation or relax the protocol automatically. Return to an explicit decision gate.

## Prohibited before P7B is explicitly resumed

- no POWDER reservation or mutation;
- no SSH to POWDER;
- no new Golden;
- no H calibration;
- no RF recalibration;
- no B1/W1/B2 scored run;
- no OTA replication;
- no WP3 execution;
- no `scored_runs_authorized=true`;
- no immutable authorization snapshot claiming readiness while physical gates remain open.

Canonical P7 authority: `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`.
