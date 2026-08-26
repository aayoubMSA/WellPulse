# WP-PWD01 — Recovery-Horizon Calibration Plan v1

**Date frozen:** 2026-08-26  
**Evidence class:** NON-SCORED WP2 calibration  
**Status:** FROZEN FOR EXECUTION; `scored_runs_authorized = false`

## Purpose
Freeze the smallest defensible W1-only pilot needed to measure post-outage backlog drain and calculate the common scored recovery horizon `H` required by `protocol.md` v0.4.

This plan does not reopen RF calibration, does not authorize WP3, and does not generate B1/W1 comparative scientific results.

## Fixed calibration condition
Use exactly **three valid W1 calibration trials** under an S2-style hard-outage schedule:

`30 s non-scored readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain is observed`

Frozen inputs:
- architecture: `W1_OFFLINE_FIRST` only;
- workload: 1 record/s;
- Q0: 0 dB programmed attenuation;
- Q3: 55 dB programmed attenuation;
- all POWDER attenuation IDs `1 33 2 34` changed together;
- frozen Paho target: `paho-mqtt==2.1.0`, MQTT v3.1.1, QoS1, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, queue 4096, inflight 20;
- W1 durable queue: SQLite WAL + `synchronous=FULL`;
- TLS must be enabled on the calibration MQTT path so reconnect/drain timing represents the scored transport stack.

No Q1/Q2 test and no attenuation search is permitted in this pilot.

## Mandatory validity gates for every trial
A trial is valid only if all of the following pass before its drain time enters the H calculation:

1. Live POWDER logical-to-physical bindings are captured for the new experiment; prior G4/G5 bindings are not assumed.
2. All four RF attenuation IDs are set to Q0=0 dB.
3. Explicit Q0 end-to-end LTE user-plane readiness passes through the experimental path; attach state or UE IP alone is insufficient.
4. Route evidence shows the MQTT destination `172.16.0.1` is reached through the UE experimental LTE tunnel rather than the POWDER control network.
5. The actual Paho/runtime configuration is captured and matches the frozen target.
6. Telemetry generation, receipt, RF transitions and queue state have UTC timestamps adequate to reconstruct the trial.
7. Generated record identity and SHA-256 checksum are preserved end-to-end.
8. Q3 is applied for the intended 120 s and Q0 restoration timestamp is captured exactly.
9. All pre-restoration generated records eventually arrive with valid identity/checksum and the W1 durable pending backlog reaches zero.

A failed validity gate produces an INVALID calibration trial that remains preserved. It is not included in the p95 calculation and is replaced only because of the recorded technical invalidity.

## Cohort and drain-time semantics
For H calibration only:

- `cohort_cutoff_utc` = the exact final Q3 -> Q0 restoration timestamp.
- calibration cohort = all valid records with `generated_ts_utc <= cohort_cutoff_utc`.
- `sink_cohort_complete_utc` = first timestamp by which every calibration-cohort record has been received with the generated SHA-256 checksum.
- `queue_pending_zero_utc` = first timestamp after Q0 restoration at which the W1 durable queue has zero PENDING calibration-cohort records.
- `backlog_drain_complete_utc = max(sink_cohort_complete_utc, queue_pending_zero_utc)`.
- `backlog_drain_time_s = backlog_drain_complete_utc - cohort_cutoff_utc`.

This conservative definition prevents broker PUBACK completion alone from being treated as end-to-end recovery.

## p95 estimator and H calculation
With the three valid calibration drain times, use the empirical nearest-rank percentile:

`p95 = sorted(drain_times)[ceil(0.95*n)-1]`

For `n=3`, this is the maximum valid observed drain time.

Then calculate exactly as frozen in protocol v0.4:

`H = max(120 s, ceil_to_30s(2 × p95))`

where `ceil_to_30s(x) = 30 × ceil(x/30)`.

If the calculated `H > 300 s`, **STOP AND INVESTIGATE**. Do not cap H and do not authorize scored runs.

Operationally, if a valid trial has not drained by 150 s after Q0 restoration, stop the calibration sequence for investigation because any subsequently observed drain time would force `H > 300 s` under the frozen formula.

## Required calibration bundle
Each trial must preserve, at minimum:
- sanitized experiment/profile identity and live bindings;
- WellPulse Git SHA and runtime manifest;
- Q0 readiness result and route evidence;
- generated telemetry ledger;
- all receiver attempts;
- attenuation timeline;
- process/MQTT events;
- queue-depth/pending timeline;
- exact cutoff and drain-complete timestamps;
- SHA-256 manifest of the bundle.

No credentials, SSH keys, passphrases, RPC tokens, private TLS keys, or raw credential-bearing portal manifests may enter the evidence bundle.

## Acceptance gate
**PASS** only when:
- three valid W1 calibration drain times are reconstructed from immutable evidence;
- the p95 and H calculation are deterministic;
- H is `<= 300 s`;
- the same H can be written into the pre-score protocol implementation artifacts without changing any scored outcome.

Until then, WP2 remains IN PROGRESS and scientific weighted completion remains 20%.
