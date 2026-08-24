# WP-PWD01 — POWDER Real-RF Resilience Validation

**Protocol version:** v0.2

**Status:** DESIGN_FROZEN_PENDING_CALIBRATION_AND_BASELINE_GATE. No scored run is authorized by this file yet.

## Scientific purpose

Extend the completed FIT IoT-LAB embedded-hardware result into a real-radio causal validation layer without repeating the same experiment mechanically.

The POWDER study asks whether the WellPulse durable offline-first path provides measurable reliability/recovery value over a **strong standard MQTT baseline** when impairment is created in the physical radio path, and whether that value persists in a compact OTA replication.

## Evidence boundary

This experiment may support networking, radio-link resilience, edge/cloud recovery, telemetry integrity/completeness, reconnect behavior, process-restart recovery, and resilience-overhead claims.

It does **not** validate pump mechanics, hydraulics, groundwater, crop physiology, Siwa environmental conditions, agricultural field performance, or rural generalization.

## Research questions

- **RQ1 — Network resilience:** Under controlled real RF intermittency and hard outage, how do standard MQTT QoS 1 + automatic reconnect and WellPulse differ in unique telemetry completeness, recovery behavior, and overhead?
- **RQ2 — Durable recovery:** When the gateway process is restarted during an RF outage, does application-level disk durability + idempotent reconciliation preserve records that a memory-only MQTT path cannot guarantee across client restart?
- **RQ3 — Transportability:** Are the observed patterns consistent with the existing FIT embedded-hardware evidence and reproducible in a compact POWDER OTA replication?

## Architecture modes

### `B1_MQTT_QOS1`

**Primary comparator.** Standard MQTT v3.1.1 / QoS 1 / TLS with automatic reconnect and the same telemetry generation, broker, receiver-facing payload schema, keepalive, and network path as W1, but **without application-level disk queueing or application-level reconciliation**.

The exact Paho MQTT package version, clean-session/session configuration, reconnect-delay settings, outgoing queue limits, and process-restart semantics must be recorded and frozen before scored runs.

This is intentionally stronger than the legacy publish-only baseline.

### `W1_OFFLINE_FIRST`

Current WellPulse durable path:
- SQLite-backed durable queue;
- WAL journaling and synchronous durability setting;
- stable record identity and SHA-256 payload checksum;
- explicit pending/sent state;
- reconnect/replay;
- idempotent receiver keyed by record identity;
- reconciliation/backlog drain.

### `B0_PUBLISH_ONLY`

Legacy lower-bound baseline used in FIT and local tests. It may be retained for sanity checks and historical continuity, but **is not the primary inferential comparator in POWDER** and is not included in the primary scored matrix unless an explicit protocol amendment is made before scoring.

## Radio states

Numeric settings are deliberately not frozen until WP2 non-scored calibration.

- `Q0`: strong/stable reference link.
- `Q1`: degraded but continuously connected characterization point.
- `Q2`: near-threshold/intermittent operating point suitable for repeatable transient delivery degradation.
- `Q3`: effective application-data outage.

For each state record both the programmed attenuation/path setting and observable radio/link indicators when exposed by the stack (target: RSRP, RSRQ, SINR, BLER and throughput/attach state where technically available).

## Scored scenarios

All scenarios use a 30 s non-scored readiness/warm-up before the scored schedule.

Let `H` be the post-recovery observation horizon frozen after non-scored calibration.

### `S0_HEALTHY`
`Q0 60 s -> Q0 120 s -> Q0 H`

Purpose: matched healthy-control cost and integrity check. No resilience advantage is assumed.

### `S1_INTERMITTENT`
`Q0 60 s -> [Q2 20 s / Q0 20 s] x 3 -> Q0 H`

Purpose: repeated near-threshold disruption/recovery while preserving a physical RF cause.

### `S2_HARD_OUTAGE`
`Q0 60 s -> Q3 120 s -> Q0 H`

Purpose: deterministic RF-induced data-path outage followed by recovery.

### `S3_OUTAGE_RESTART`
`Q0 60 s -> Q3 120 s -> Q0 H`, with one gateway-process restart 60 s into the Q3 interval.

Purpose: compound connectivity + process failure that directly tests volatile MQTT state versus durable application state.

The restart is a **gateway-process restart**, not a node power cycle or hardware reboot.

## Recovery-horizon rule

Calibration is non-scored. After calibration, freeze one common `H` for all architectures and scored scenarios:

`H = max(120 s, ceil_to_30s(2 × p95 observed W1 backlog-drain time in valid calibration trials))`

If the resulting H exceeds 300 s, stop and review the cause before authorizing scored runs rather than silently capping the observation window.

## Telemetry workload

- Default scored rate: **1 record/s**.
- Record identity must be deterministic and unique within a run.
- Each record must preserve generated timestamp, sequence/record ID, canonical payload, and SHA-256 checksum.
- The same generator configuration and payload distribution are used for B1 and W1 within each paired block.

## Pairing and run order

The **run**, not the individual message, is the statistical unit.

For each scenario, B1 and W1 are executed as a paired block using:
- the same POWDER experiment/profile and frozen RF settings;
- the same telemetry-generator configuration;
- fresh application state before each run;
- pre-generated randomized architecture order;
- fixed randomization seed `26082401` recorded in the run ledger.

Do not run all B1 cells first and all W1 cells second.

## Replication rule

- `S0_HEALTHY`: exactly **3 paired blocks** = 6 scored runs.
- `S1`, `S2`, `S3`: begin with **3 paired blocks** each.
- After the first 3 valid paired blocks of an impairment scenario, calculate the two-sided 95% t-interval for the paired **run-level completeness difference** `W1 - B1`.
- If the CI half-width is `<= 2 percentage points` **and** there are no unresolved protocol deviations, stop that scenario at 3 pairs.
- Otherwise execute two additional pre-authorized paired blocks, for a maximum of **5 pairs**.

This stopping rule is based on **precision only**, never on effect direction, statistical significance, or whether WellPulse appears to win.

Thus the conducted campaign contains **24–36 scored runs**, not a mandatory 40.

## Primary endpoint

**Unique telemetry completeness at the frozen post-recovery horizon H:**

`unique valid expected records received by H / records generated in the scored interval`

A record is valid only if record identity and checksum match the generated ledger.

## Secondary endpoints

Reliability/integrity:
- permanent missing count/rate;
- duplicate delivery attempts and final duplicate rate;
- checksum mismatch/corruption count;
- out-of-order count/rate.

Recovery:
- transport reconnect time;
- time from Q0 restoration to first successful post-outage delivery;
- backlog-drain time;
- time to complete reconciliation.

Performance/overhead:
- end-to-end latency p50/p95/p99 where instrumentation is valid;
- CPU utilization;
- RSS/memory;
- durable queue occupancy and disk bytes;
- network bytes/packets and retransmission indicators where available.

Radio context:
- programmed attenuation/path state;
- RSRP/RSRQ/SINR/BLER/throughput/attach state when exposed;
- exact timestamps for RF state transitions.

## Analysis principle

Primary reporting is effect-size first: paired run-level differences with confidence intervals and absolute engineering meaning. P-values, if reported, are secondary and never used as the sole evidence of value.

Message-level observations are not treated as thousands of independent replicates.

## Technical invalidity / rerun rule

A scored run may be marked technically invalid only for a pre-defined infrastructure/protocol failure such as:
- incorrect or incomplete RF schedule;
- payload bypassing the experimental data path through the POWDER control network;
- missing/corrupt mandatory evidence that prevents endpoint reconstruction;
- wrong architecture/configuration deployed;
- testbed failure that prevents the frozen condition from being applied;
- clock/log failure severe enough that the required time-based metrics cannot be reconstructed.

The raw invalid run remains preserved and labeled. Replacement is permitted only for technical invalidity, never for an unfavorable scientific result.

## OTA replication rule

OTA is a separate replication layer, not a repeat of the entire conducted matrix.

If the conducted gate passes, run B1/W1 for:
- `S1_INTERMITTENT`;
- `S2_HARD_OUTAGE`;

with **3 paired blocks per scenario** = 12 scored OTA runs, subject to resource availability. `S3_OUTAGE_RESTART` is not required in OTA because its distinguishing factor is application durability rather than propagation mode.

## Pre-score gates

Before `scored_runs_authorized` can become true:

1. Automated POWDER lifecycle can create -> wait-ready -> retrieve manifest -> SSH -> terminate with fail-safe cleanup.
2. B1 strong-baseline implementation exists, passes local tests, and its exact MQTT semantics are documented.
3. End-to-end telemetry passes through the experimental radio/data path, not the POWDER control network.
4. Record identity/checksum are preserved end-to-end.
5. Q0–Q3 are calibrated and numerically frozen with observed radio context.
6. H is calculated from non-scored calibration and frozen.
7. B1/W1 implementation matching is audited.
8. Evidence capture and clock alignment are sufficient for all mandatory endpoints.
9. Analysis code can reconstruct the primary endpoint from a pilot evidence bundle without manual spreadsheet edits.

## Prohibited drift

Do not add GPU, massive-MIMO, O-RAN/RIC, mobility, multiple traffic-rate sweeps, multiple MQTT-QoS sweeps, multi-site operation, outdoor/rural claims, or AI components to this paper unless the frozen questions cannot otherwise be answered and a pre-score protocol amendment is approved.
