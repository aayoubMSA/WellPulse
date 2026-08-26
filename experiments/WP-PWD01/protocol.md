# WP-PWD01 — POWDER Real-RF Resilience Validation

**Protocol version:** v0.5  
**Status:** PRE-SCORE / H UNFROZEN / `scored_runs_authorized=false`

## Scientific purpose

Validate when WellPulse application-level durable record semantics add measurable value beyond a correctly configured matched MQTT QoS1 client under controlled physical-RF impairment. The radio access technology is an experimental carrier, not the novelty claim.

## Evidence boundary

This experiment may support networking, radio-link resilience, edge/cloud recovery, telemetry integrity/completeness, reconnect behavior, process-restart recovery, and resilience-overhead claims. It does not validate pump mechanics, hydraulics, groundwater, crop physiology, Siwa field performance, or broad rural generalization.

## Frozen matched transport

Both B1 and W1 use `PahoQoS1Session` with `paho-mqtt==2.1.0`, MQTT v3.1.1, QoS1, TLS, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, outgoing queue 4096, inflight 20. W1 adds SQLite durable application state, stable record identity/checksum, replay/reconciliation and idempotent receive semantics; B1 does not.

## Frozen RF state

Q0/Q1/Q2/Q3 = `0/40/52/55 dB`; attenuation IDs `1 33 2 34`, always coupled. Every physical run requires explicit Q0 end-to-end LTE user-plane PASS; attach/IP alone is insufficient.

## Scientific scenarios and endpoint

S0 healthy, S1 intermittent, S2 hard outage, S3 outage + gateway-process restart. Primary endpoint remains unique valid primary-cohort completeness at the prospectively frozen common H. Run is the statistical unit; paired architecture order and replication rules remain governed by the frozen run matrix/randomization plan. Claim remains bounded to the 1 Hz low-rate telemetry regime.

## Technical invalidity

Technical invalidity may be declared only for prospectively defined infrastructure/protocol failures, including wrong RF schedule, bypass of the experimental path, wrong architecture/configuration, severe clock/log failure, or missing/corrupt mandatory evidence preventing endpoint reconstruction. Raw invalid runs remain preserved. Unfavorable scientific outcomes are never grounds for replacement.

## Mandatory Evidence Escrow Gate — FAIL CLOSED

**Added 2026-08-26 after the WP-HCAL-E H1 evidence incident. This control is mandatory and cannot be waived by time pressure or reservation expiry.**

The H1 experiment produced valid raw archives and SHA-256 manifests, but they were left under node-local `/users/aayoub/wellpulse-powder-evidence/` and were not copied to persistent `/proj/WellPulse` or off POWDER before experiment destruction. A subsequent RS-0 probe found no raw H1 bundle in user-accessible persistent storage. Backend recovery is pending with POWDER support.

Therefore, for every future POWDER experiment/rehearsal/calibration/scored run/recovery test:

### Pre-termination requirements

1. Freeze raw sender, receiver, RF, LTE/EPC/eNB/UE, queue/database, runtime/configuration and analysis-input artifacts.
2. Compute a source-node SHA-256 manifest.
3. Copy the complete bundle to:

   `/proj/WellPulse/evidence-escrow/<experiment>/<run-id>/`

4. Verify every persistent copy against the source SHA-256 manifest.
5. Copy a second complete bundle off POWDER to the approved external evidence repository/workspace.
6. Verify the off-testbed copy against the same SHA-256 manifest.
7. Assert mandatory endpoint-reconstruction inputs exist and are non-empty, including generated ledger, received ledger/events, RF timeline, queue/durable-state evidence, runtime/configuration manifest and required diagnostic logs.
8. Record experiment UUID, profile revision, node bindings, code commit, runtime/package versions, evidence locations and integrity hashes in the canonical repository/handover.
9. Emit exactly:

   `EVIDENCE_ESCROW_GATE=PASS`

Only then may teardown be authorized.

### Hard prohibition

If the gate does not emit PASS, the required action is:

`STOP / DO_NOT_TERMINATE`

The following are **not** substitutes for escrow: hashes without files, console summaries, derived tables, screenshots, successful application checks, or an expiring reservation.

Any automated teardown must fail closed: it must refuse experiment destruction unless both persistent-storage verification and off-testbed verification are positively recorded. Shell automation should show a visible progress bar and identify the failing escrow sub-gate.

## Pre-score gates

Before `scored_runs_authorized` can become true:

1. Controlled physical-RF profile and exact identity frozen.
2. Matched Paho configuration reproduced in remote runtime.
3. Experimental path verified end-to-end.
4. Record identity/checksum preserved end-to-end.
5. Q0–Q3 frozen with radio context.
6. H/recovery semantics prospectively frozen after the Recovery-Semantics Consortium gate.
7. B1/W1 matching audited.
8. Evidence capture and clock alignment sufficient for mandatory endpoints.
9. Analysis code reconstructs the primary endpoint from a non-scored pilot without manual spreadsheet edits.
10. **Evidence Escrow Gate implementation is rehearsed end-to-end and demonstrated fail-closed before any scored run.**

## Current H1 provenance

`WP-HCAL-E`, UUID `9153e16a-1eb1-45f5-88bf-303636a9d1ec`, H1 run `wp2h1-a1-20260826-001`, remains `VALID_W1_RECOVERY_FAILURE`, non-scored. Do not reclassify or erase it. Raw record-level bundles are presently unavailable from user-accessible persistent storage; integrity hashes and derived observations remain provenance anchors, not substitutes for the missing raw files.

## Prohibited drift

Do not add GPU, massive-MIMO, O-RAN/RIC, mobility, traffic-rate sweeps, QoS sweeps, multi-site operation, outdoor/rural claims, or AI components unless the frozen scientific questions cannot otherwise be answered and a pre-score amendment is approved.