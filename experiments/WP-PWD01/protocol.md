# WP-PWD01 — POWDER Real-RF Resilience Validation

**Protocol version:** v0.4

**Status:** DESIGN_FROZEN_PENDING_LIFECYCLE_AND_RF_CALIBRATION. No scored run is authorized by this file yet.

## Scientific purpose

Extend the completed FIT IoT-LAB embedded-hardware result into a real-radio causal validation layer without repeating the same experiment mechanically.

The POWDER study asks whether the WellPulse durable offline-first path provides measurable reliability/recovery value over a **strong standard MQTT baseline** when impairment is created in the physical radio path, and whether that value persists in a compact OTA replication.

The radio access technology is an experimental carrier, not the novelty claim. A currently executable controlled LTE profile may be used instead of a blocked 5G profile if it preserves programmable physical-RF attenuation, measurable radio context, matched B1/W1 data paths, and the same frozen scientific questions.

## Evidence boundary

This experiment may support networking, radio-link resilience, edge/cloud recovery, telemetry integrity/completeness, reconnect behavior, process-restart recovery, and resilience-overhead claims.

It does **not** validate pump mechanics, hydraulics, groundwater, crop physiology, Siwa environmental conditions, agricultural field performance, or rural generalization.

## Research questions

- **RQ1 — Network resilience:** Under controlled real RF intermittency and hard outage, how do standard MQTT QoS 1 + automatic reconnect and WellPulse differ in unique telemetry completeness, recovery behavior, and overhead?
- **RQ2 — Durable recovery:** When the gateway process is restarted during an RF outage, does application-level disk durability + idempotent reconciliation preserve records that a memory-only MQTT path cannot guarantee across client restart?
- **RQ3 — Transportability:** Are the observed patterns consistent with the existing FIT embedded-hardware evidence and reproducible in a compact POWDER OTA replication?

## Matched low-level MQTT transport — frozen

Both B1 and W1 use the same low-level session implementation, `PahoQoS1Session`, so the primary architectural contrast is application-level durability/reconciliation rather than transport tuning.

Frozen session parameters:
- package: `paho-mqtt==2.1.0`;
- protocol: MQTT v3.1.1;
- QoS: 1;
- TLS: enabled for the scored path;
- `clean_session=False`;
- keepalive: 60 s;
- automatic reconnect delay: minimum 1 s, maximum 8 s;
- maximum queued outgoing messages: 4096;
- maximum inflight QoS>0 messages: 20;
- application-level persistence inside this low-level session: none.

The Paho package version is pinned in `pyproject.toml`. Runtime manifests must record these values and the actual installed version. Credentials are never written to evidence.

Paho's volatile outgoing/session state may survive a network-only disconnect while the process remains alive but is not treated as application-level durable storage. A process restart destroys local volatile client state that has not been durably captured elsewhere.

## Architecture modes

### `B1_MQTT_QOS1`

**Primary comparator.** Generated telemetry is submitted directly to the frozen matched Paho QoS1 session. B1 has **no application-level disk queue and no application-level reconciliation/replay layer**.

This is intentionally stronger than the legacy publish-only baseline: it has standard QoS1 behavior, bounded in-memory outgoing queueing, and automatic reconnect.

### `W1_OFFLINE_FIRST`

WellPulse uses the **same frozen Paho QoS1 session beneath** its application layer, plus:
- SQLite-backed durable queue;
- WAL journaling and synchronous durability setting;
- stable record identity and SHA-256 payload checksum;
- explicit pending/sent state;
- reconnect/replay from durable application state;
- idempotent receiver keyed by record identity;
- reconciliation/backlog drain.

Thus B1/W1 differ in application-level durability and reconciliation, not in MQTT version, QoS, TLS, keepalive, reconnect delays, outgoing queue limit, inflight limit, broker, topic schema, RF path, or telemetry generator.

### `B0_PUBLISH_ONLY`

Legacy lower-bound baseline used in FIT and local tests. It may be retained for sanity checks and historical continuity, but **is not the primary inferential comparator in POWDER** and is not included in the primary scored matrix unless an explicit protocol amendment is made before scoring.

## Controlled-RF profile rule

The original preferred profile, `PowderTeam/srs-rf-matrix`, is currently blocked for project WellPulse because a live non-scored API dry run resolved a hidden `n310` requirement while the project has entitlement 0 for `n310`. The failed experiment was cleaned up and is infrastructure evidence only. Do not re-submit that profile unchanged.

A replacement conducted profile may be selected before scoring only if a non-scored feasibility run establishes:
1. real SDR/radio hardware inside POWDER's conducted environment;
2. programmatically adjustable physical RF attenuation sufficient to create repeatable Q0/Q2/Q3 conditions;
3. end-to-end user-plane traffic through the radio path;
4. accessible radio/link measurements adequate to characterize the imposed state;
5. automated create -> READY -> manifest -> SSH -> fail-safe terminate;
6. exact profile identity/revision and node bindings captured.

Changing RAT from 5G to LTE under this rule is **not** a protocol-outcome change because the RAT is not an experimental factor or novelty claim. The selected RAT/profile must be frozen before calibration and used consistently for the conducted campaign; OTA should use the same RAT when a scientifically adequate current profile is executable.

## Radio states

Numeric settings are deliberately not frozen until WP2 non-scored calibration.

- `Q0`: strong/stable reference link.
- `Q1`: degraded but continuously connected characterization point.
- `Q2`: near-threshold/intermittent operating point suitable for repeatable transient delivery degradation.
- `Q3`: effective application-data outage.

For each state record both the programmed attenuation/path setting and observable radio/link indicators when exposed by the stack, targeting RSRP, RSRQ, SINR, BLER and throughput/attach state where technically available.

## Scored scenarios

All scenarios use a 30 s non-scored readiness/warm-up before the scored schedule.

Let `H` be the post-recovery observation horizon frozen after non-scored calibration.

### `S0_HEALTHY`
`Q0 60 s -> Q0 120 s -> Q0 H`

Purpose: matched healthy-control cost and integrity check. No resilience advantage is assumed. The point after the first 180 s is the pseudo-restoration/cohort-cutoff point.

### `S1_INTERMITTENT`
`Q0 60 s -> [Q2 20 s / Q0 20 s] x 3 -> Q0 H`

Purpose: repeated near-threshold disruption/recovery while preserving a physical RF cause. The final transition to Q0 is the cohort-cutoff point.

### `S2_HARD_OUTAGE`
`Q0 60 s -> Q3 120 s -> Q0 H`

Purpose: deterministic RF-induced data-path outage followed by recovery. The Q3->Q0 transition is the cohort-cutoff point.

### `S3_OUTAGE_RESTART`
`Q0 60 s -> Q3 120 s -> Q0 H`, with one gateway-process restart 60 s into the Q3 interval.

Purpose: compound connectivity + process failure that directly tests volatile MQTT state versus durable application state. The restart is a **gateway-process restart**, not a node power cycle or hardware reboot. The Q3->Q0 transition is the cohort-cutoff point.

## Recovery-horizon rule

Calibration is non-scored. After calibration, freeze one common `H` for all architectures and scored scenarios:

`H = max(120 s, ceil_to_30s(2 × p95 observed W1 backlog-drain time in valid calibration trials))`

If the resulting H exceeds 300 s, stop and review the cause before authorizing scored runs rather than silently capping the observation window.

Each scored run records:
- `cohort_cutoff_utc` at final Q0 restoration (or the S0 pseudo-restoration point);
- `horizon_end_utc = cohort_cutoff_utc + H`.

## Telemetry workload

- Default scored rate: **1 record/s**.
- Record identity must be deterministic and unique within a run.
- Each record must preserve generated timestamp, sequence/record ID, canonical payload, and SHA-256 checksum.
- The same generator configuration and payload distribution are used for B1 and W1 within each paired block.
- Telemetry generation continues during impairment and recovery; transport calls must not serialize generation behind `wait_for_publish()`.
- Post-restoration generation continues through H to preserve realistic recovery load but is excluded from the primary completeness denominator to avoid unequal right-censoring.

## Primary analysis cohort

The confirmatory primary cohort is all valid records generated at or before `cohort_cutoff_utc`.

Records generated after `cohort_cutoff_utc` remain in raw evidence and may contribute to secondary/exploratory recovery diagnostics, but they are not part of the confirmatory primary denominator.

## Pairing and run order

The **run**, not the individual message, is the statistical unit.

For each scenario, B1 and W1 are executed as a paired block using:
- the same POWDER experiment/profile and frozen RF settings;
- the same telemetry-generator configuration;
- fresh application state before each run;
- pre-generated randomized architecture order;
- fixed randomization seed `26082401`.

The complete mandatory/reserve order is frozen in `randomization-plan.csv`. Do not run all B1 cells first and all W1 cells second.

## Replication rule

- `S0_HEALTHY`: exactly **3 paired blocks** = 6 scored runs.
- `S1`, `S2`, `S3`: begin with **3 paired blocks** each.
- After the first 3 valid paired blocks of an impairment scenario, calculate the two-sided 95% t-interval for the paired **run-level completeness difference** `W1 - B1`.
- If the CI half-width is `<= 2 percentage points` **and** there are no unresolved protocol deviations, stop that scenario at 3 pairs.
- Otherwise execute the two pre-authorized reserve paired blocks, for a maximum of **5 pairs**.

This stopping rule is based on **precision only**, never on effect direction, statistical significance, or whether WellPulse appears to win.

Thus the conducted campaign contains **24–36 scored runs**, not a mandatory 40.

## Primary endpoint

**Unique valid primary-cohort telemetry completeness at H:**

`unique valid primary-cohort records received no later than horizon_end_utc / primary-cohort generated records`

A received record is valid only if its record identity belongs to the generated primary cohort and its SHA-256 checksum matches the generated ledger.

The reference deterministic reconstruction is `wellpulse.powder_analysis.reconstruct_primary_endpoint` with CLI `scripts/analyze_wp_pwd01_run.py`.

## Secondary endpoints

Reliability/integrity:
- permanent missing count/rate;
- duplicate delivery attempts and final duplicate rate;
- checksum mismatch/corruption count;
- unexpected-record attempt count;
- out-of-order count/rate.

Recovery:
- transport reconnect time;
- time from Q0 restoration to first successful post-outage delivery;
- backlog-drain time for the pre-restoration cohort;
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

Message-level observations are not treated as thousands of independent replicates. Post-horizon delivery is retained but cannot retroactively count as primary on-time recovery.

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

1. One controlled physical-RF profile passes automated create -> READY -> manifest -> SSH -> fail-safe terminate and its exact identity is frozen.
2. Frozen `PahoQoS1Session` configuration passes local tests and is reproduced in the remote runtime manifest.
3. End-to-end telemetry passes through the experimental radio/data path, not the POWDER control network.
4. Record identity/checksum are preserved end-to-end.
5. Q0–Q3 are calibrated and numerically frozen with observed radio context.
6. H, `cohort_cutoff_utc` semantics, and `horizon_end_utc` are verified and frozen.
7. B1/W1 implementation matching is audited.
8. Evidence capture and clock alignment are sufficient for all mandatory endpoints.
9. Analysis code reconstructs the primary endpoint from a non-scored pilot bundle without manual spreadsheet edits.

## Prohibited drift

Do not add GPU, massive-MIMO, O-RAN/RIC, mobility, multiple traffic-rate sweeps, multiple MQTT-QoS sweeps, multi-site operation, outdoor/rural claims, or AI components to this paper unless the frozen questions cannot otherwise be answered and a pre-score protocol amendment is approved.
