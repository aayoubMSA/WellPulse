# WP-PWD01 — Recovery-Horizon Calibration Plan v1

> **AUDIT-R1 SUPERSESSION NOTICE — 2026-08-27**  
> **STATUS: HISTORICAL PROVENANCE ONLY — DO NOT EXECUTE.**  
> This pre-amendment W1-derived H-selection procedure is superseded by `RECOVERY_SEMANTICS_AMENDMENT_v1.md`. The current prospective application observation horizon is **`H_app = 300 s` from `t_service_ready`**. No W1-only calibration, Golden outcome, or scored outcome may re-estimate it. H1 remains `VALID_W1_RECOVERY_FAILURE`; this notice does not relabel or erase H1.

**Historical date frozen:** 2026-08-26  
**Historical P0 amendment:** 2026-08-26 after independent pre-WP3 consortium review  
**Evidence class:** NON-SCORED WP2 calibration  
**Current status:** SUPERSEDED / PROVENANCE ONLY / `scored_runs_authorized = false`

## Historical purpose

This plan originally froze a W1-only pilot intended to measure post-outage backlog drain and calculate a common scored recovery horizon under protocol v0.4. That selection rule is no longer operational authority.

This historical plan did not reopen RF calibration, did not authorize WP3, and did not generate B1/W1 comparative scientific results.

## Historical fixed calibration condition

The original design required exactly **three successful, technically valid W1 calibration trials** under an S2-style hard-outage schedule:

`30 s non-scored readiness/warm-up -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain is observed`

Historical frozen inputs were:
- architecture: `W1_OFFLINE_FIRST` only;
- workload: 1 record/s;
- Q0: 0 dB programmed attenuation;
- Q3: 55 dB programmed attenuation;
- all POWDER attenuation IDs `1 33 2 34` changed together;
- Paho target: `paho-mqtt==2.1.0`, MQTT v3.1.1, QoS1, `clean_session=False`, keepalive 60 s, reconnect 1–8 s, queue 4096, inflight 20;
- W1 durable queue: SQLite WAL + `synchronous=FULL`;
- TLS enabled on the calibration MQTT path.

No Q1/Q2 test and no attenuation search was permitted.

## Historical technical-validity semantics

A trial was technically valid only if the frozen bindings/RF/user-plane/route/runtime/timestamp/identity/session-isolation gates passed. Failure of those predefined technical gates produced `TECHNICALLY_INVALID`; raw evidence remained preserved and replacement was permitted only for those predefined technical failures.

## Scientific recovery outcome was not a validity gate

The original plan correctly distinguished adverse scientific evidence from technical invalidity. If the experiment was correctly applied but W1 lost a cohort record, failed to drain, or exceeded the then-frozen bound, the classification was:

`VALID_W1_RECOVERY_FAILURE`

Such evidence could not be relabeled invalid or replaced to erase the outcome.

A successful historical calibration attempt was `VALID_W1_RECOVERY_SUCCESS`.

**This classification logic remains important provenance, but the procedure for collecting additional W1 calibration trials and deriving H from them is superseded.**

## Historical cohort/drain semantics

For that historical calibration only:

- `cohort_cutoff_utc` = final Q3 -> Q0 restoration timestamp;
- calibration cohort = valid records with `generated_ts_utc <= cohort_cutoff_utc`;
- `sink_cohort_complete_utc` = first timestamp by which every calibration-cohort record had arrived with matching SHA-256;
- `queue_pending_zero_utc` = first post-restoration timestamp with zero pending calibration-cohort records;
- `backlog_drain_complete_utc = max(sink_cohort_complete_utc, queue_pending_zero_utc)`;
- `backlog_drain_time_s = backlog_drain_complete_utc - cohort_cutoff_utc`.

These definitions remain useful to interpret historical H1/calibration provenance but do not define the current confirmatory endpoint.

## Historical p95/H calculation — RETIRED

The old procedure used:

`p95 = sorted(drain_times)[ceil(0.95*n)-1]`

and then:

`H = max(120 s, ceil_to_30s(2 × p95))`.

**RETIRED:** do not execute this formula to select the current WP-PWD01 application horizon. Current authority fixes:

`H_app = 300 s from t_service_ready`.

## Historical required bundle

The historical design required sanitized experiment/profile identity, runtime manifest, Q0 readiness/route evidence, run-specific MQTT session identity, generated/received telemetry, attenuation/process/queue timelines, exact timing, classification and SHA-256 manifest. Credentials/private keys were prohibited from evidence.

## Current operational rule

- Do not run H calibration.
- Do not reopen H1 salvage.
- Do not derive a new horizon from outcomes.
- Preserve H1 as valid adverse non-scored evidence.
- Use `t_rf_restore` to freeze the primary cohort.
- Use `t_service_ready` to anchor fixed `H_app=300 s`.
- Use `completeness_300` as the primary endpoint.
- Follow `HANDOVER_CURRENT.md`, `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`, and `docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`.
