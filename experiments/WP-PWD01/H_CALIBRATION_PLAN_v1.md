# WP-PWD01 — Recovery-Horizon Calibration Plan v1

**Date frozen:** 2026-08-26  
**P0 amendment:** 2026-08-26 after independent pre-WP3 consortium review  
**Evidence class:** NON-SCORED WP2 calibration  
**Status:** FROZEN FOR EXECUTION AS AMENDED; `scored_runs_authorized = false`

## Purpose
Freeze the smallest defensible W1-only pilot needed to measure post-outage backlog drain and calculate the common scored recovery horizon `H` required by `protocol.md` v0.4.

This plan does not reopen RF calibration, does not authorize WP3, and does not generate B1/W1 comparative scientific results.

## Fixed calibration condition
Use exactly **three successful, technically valid W1 calibration trials** under an S2-style hard-outage schedule:

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

## Mandatory technical-validity gates for every attempted trial
A trial is technically valid only if all of the following pass:

1. Live POWDER logical-to-physical bindings are captured for the new experiment; prior G4/G5 bindings are not assumed.
2. All four RF attenuation IDs are set to Q0=0 dB before readiness.
3. Explicit Q0 end-to-end LTE user-plane readiness passes through the experimental path; attach state or UE IP alone is insufficient.
4. Route evidence shows the MQTT destination `172.16.0.1` is reached through the UE experimental LTE tunnel rather than the POWDER control network.
5. The actual Paho/runtime configuration is captured and matches the frozen target.
6. Telemetry generation, receipt, RF transitions and queue state have UTC timestamps adequate to reconstruct the trial.
7. Generated record identity and SHA-256 checksum are preserved in the evidence needed to assess the outcome.
8. Q3 is applied for the intended 120 s and Q0 restoration timestamp is captured exactly.
9. MQTT state is isolated for the trial: use a deterministic run-unique publisher client identity and run-unique topic namespace; capture client ID, topic and initial `session_present` evidence. A prior calibration attempt must not contribute stale publisher/subscriber session state to a later attempt.

Failure of any item above produces:

`TECHNICALLY_INVALID`

The raw attempt remains preserved. Replacement is allowed only for this predefined technical invalidity.

## Scientific recovery outcome is not a validity gate
The following are **measured W1 outcomes**, not technical-validity conditions:

- whether every pre-restoration record reaches the sink with matching identity/checksum;
- whether the W1 durable queue reaches zero pending cohort records;
- how long full end-to-end backlog drain takes.

If the frozen experiment is applied correctly but W1 loses a cohort record, fails to drain the durable cohort, or exceeds the frozen recovery bound, classify the attempt as:

`VALID_W1_RECOVERY_FAILURE`

This is valid adverse scientific/implementation evidence. It must **not** be relabeled as invalid and must **not** be replaced to erase the outcome. Stop the H freeze and investigate.

A successful technically valid calibration attempt is classified:

`VALID_W1_RECOVERY_SUCCESS`

The H calculation requires exactly three such successful outcomes. Additional attempts are permitted only as replacements for documented `TECHNICALLY_INVALID` attempts. Do not collect extra successful trials.

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
With the three `VALID_W1_RECOVERY_SUCCESS` drain times, use the empirical nearest-rank percentile:

`p95 = sorted(drain_times)[ceil(0.95*n)-1]`

For `n=3`, this is exactly the **maximum of the three observed successful drain times**. It is an operational calibration statistic and must not be described as a stable population 95th-percentile estimate.

Then calculate exactly as frozen in protocol v0.4:

`H = max(120 s, ceil_to_30s(2 × p95))`

where `ceil_to_30s(x) = 30 × ceil(x/30)`.

If the calculated `H > 300 s`, **STOP AND INVESTIGATE**. Do not cap H and do not authorize scored runs.

Operationally, if a technically valid trial has not drained by 150 s after Q0 restoration, stop the calibration sequence for investigation because any subsequently observed drain time would force `H > 300 s` under the frozen formula. This is not technical invalidity.

## Required calibration bundle
Each attempted trial must preserve, at minimum:
- sanitized experiment/profile identity and live bindings;
- WellPulse Git SHA and runtime manifest;
- Q0 readiness result and route evidence;
- run-specific MQTT client identity, topic namespace and session evidence;
- generated telemetry ledger;
- all receiver attempts;
- attenuation timeline;
- process/MQTT events;
- queue-depth/pending timeline;
- exact cutoff and drain-complete timestamps when available;
- trial classification and reason;
- SHA-256 manifest of the bundle.

No credentials, SSH keys, passphrases, RPC tokens, private TLS keys, or raw credential-bearing portal manifests may enter the evidence bundle.

## Acceptance gate
**PASS** only when:
- exactly three `VALID_W1_RECOVERY_SUCCESS` drain times are reconstructed from immutable evidence;
- no `VALID_W1_RECOVERY_FAILURE` has occurred in the calibration sequence;
- any replacement attempt is traceable only to predefined `TECHNICALLY_INVALID` evidence;
- the p95 and H calculation are deterministic;
- H is `<= 300 s`;
- the same H can be written into the pre-score protocol implementation artifacts without changing any scored outcome.

Until then, WP2 remains IN PROGRESS and scientific weighted completion remains 20%.
