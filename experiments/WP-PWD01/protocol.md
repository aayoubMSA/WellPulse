# WP-PWD01 — POWDER Real-RF Resilience Validation

**Protocol version:** v0.6  
**Status:** PRE-SCORE / RECOVERY SEMANTICS AMENDED / `scored_runs_authorized=false`

## Scientific purpose

Validate when WellPulse application-level durable record semantics add measurable value beyond a correctly configured matched MQTT QoS1 client under controlled physical-RF impairment. The radio access technology is an experimental carrier, not the novelty claim.

## Evidence boundary

This experiment may support networking, radio-link resilience, edge/cloud recovery, telemetry integrity/completeness, reconnect behavior, process-restart recovery, and resilience-overhead claims. It does not validate pump mechanics, hydraulics, groundwater, crop physiology, Siwa field performance, or broad rural generalization.

## Frozen matched transport

Both B1 and W1 use `PahoQoS1Session` with `paho-mqtt==2.1.0`, MQTT v3.1.1, QoS1, TLS, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, outgoing queue 4096, inflight 20. W1 adds SQLite durable application state, stable record identity/checksum, replay/reconciliation and idempotent receive semantics; B1 does not.

## Frozen RF state

Q0/Q1/Q2/Q3 = `0/40/52/55 dB`; attenuation IDs `1 33 2 34`, always coupled. Every physical run requires explicit Q0 end-to-end LTE user-plane PASS; attach/IP alone is insufficient.

## Recovery-semantics amendment — governing

The prospective amendment frozen after RS-2/RS-3/RS-4 is:

`experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`

It governs all future rehearsal/calibration/scored execution and supersedes the old arm-informed H-calibration logic.

Frozen consequences:

- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct clocks;
- primary cohort cutoff remains `t_rf_restore`;
- `T_service`, `T_app`, `T_total` are mandatory;
- common architecture-independent application horizon is **300 s from `t_service_ready`**;
- primary completeness endpoint is observed at `t_service_ready + 300 s` for every architecture;
- no W1-only or outcome-driven horizon calibration is permitted;
- S2/S3 use the same scripted clean-order LTE service-restoration boundary across architectures;
- S0/S1 do not receive a forced LTE reset and use the same architecture-blind service-ready probe;
- service restoration and evidence escrow must be deterministic, scripted, timestamped, and architecture-blind.

## Scientific scenarios

S0 healthy, S1 intermittent, S2 hard outage, S3 outage + gateway-process restart. Scenario definitions, Q0–Q3 states, the S3 gateway-process restart treatment, workload, pairing/randomization and architecture comparators remain unchanged by the recovery-semantics amendment.

## Primary endpoint

For each valid run:

`completeness_300 = unique valid primary-cohort records received no later than (t_service_ready + 300 s) / primary-cohort generated records`

with:

`primary cohort = all valid records generated at or before t_rf_restore`.

Run remains the statistical unit. Paired B1/W1 comparisons and precision-based replication remain governed by the frozen analysis/randomization plan, subject to the endpoint clock amendment above.

## Technical invalidity

Technical invalidity may be declared only for prospectively defined infrastructure/protocol failures, including wrong RF schedule, bypass of the experimental path, wrong architecture/configuration, severe clock/log failure, missing/corrupt mandatory evidence preventing endpoint reconstruction, or failure of the standardized architecture-blind service-restoration boundary under the exact RS-6 rule before application outcomes are inspected.

Raw invalid attempts remain preserved and counted. Replacement is permitted only under the predeclared rule with a new run ID. Unfavorable application outcomes are never grounds for replacement.

## Mandatory Evidence Escrow Gate — FAIL CLOSED

Every future POWDER experiment/rehearsal/calibration/scored run/recovery test must, before teardown:

1. freeze raw sender, receiver, RF, LTE/EPC/eNB/UE, queue/database, runtime/configuration and analysis-input artifacts;
2. compute source SHA-256 manifest;
3. copy complete bundle to `/proj/WellPulse/evidence-escrow/<experiment>/<run-id>/`;
4. verify persistent copy against source manifest;
5. copy a second complete bundle off POWDER;
6. verify the off-testbed copy against the same manifest;
7. confirm mandatory endpoint-reconstruction inputs are present and non-empty;
8. record experiment UUID/profile revision/node bindings/code commit/runtime versions/evidence locations/hashes in the canonical repository;
9. emit `EVIDENCE_ESCROW_GATE=PASS`.

Anything else is `STOP / DO_NOT_TERMINATE`. Hashes, console summaries, screenshots, successful checks, or reservation expiry do not waive this gate.

## Negative/null-result interpretation — frozen

- B1 approximately W1 in S1/S2: standard QoS1 is sufficient while volatile process state survives; informative boundary result.
- W1 > B1 in S3: evidence for application-level durability across volatile-state destruction.
- B2 approximately W1 in S3: standard durable MQTT can close much of the gap; narrow WellPulse contribution accordingly.
- B2 > W1 or W1 shows no material advantage: valid negative result; do not alter RF states, scenarios, horizon, exclusions or replication to recover a preferred story.

## Pre-score gates

Before `scored_runs_authorized` can become true:

1. controlled physical-RF profile and exact identity frozen;
2. matched Paho configuration reproduced remotely;
3. experimental path verified end-to-end;
4. record identity/checksum preserved end-to-end;
5. Q0–Q3 frozen with radio context;
6. recovery clocks and fixed 300 s service-ready horizon frozen;
7. B1/W1 matching audited;
8. evidence capture and clock alignment sufficient for mandatory endpoints;
9. analysis code reconstructs the amended primary endpoint from a non-scored pilot without manual spreadsheet edits;
10. Golden E2E rehearsal passes the exact RS-6 service restoration and readiness procedure;
11. Evidence Escrow Gate is demonstrated end-to-end and fail-closed;
12. RS-7 issues explicit GO.

## H1 provenance

`WP-HCAL-E`, UUID `9153e16a-1eb1-45f5-88bf-303636a9d1ec`, H1 run `wp2h1-a1-20260826-001`, remains `VALID_W1_RECOVERY_FAILURE`, non-scored. It is not retroactively reclassified and is not used to choose the new fixed horizon. Raw record-level bundles are presently unavailable from user-accessible persistent storage; backend recovery remains pending.

## Prohibited drift

Do not add GPU, massive-MIMO, O-RAN/RIC, mobility, traffic-rate sweeps, QoS sweeps, multi-site operation, outdoor/rural claims, or AI components unless the frozen scientific questions cannot otherwise be answered and a new pre-score amendment is approved.
