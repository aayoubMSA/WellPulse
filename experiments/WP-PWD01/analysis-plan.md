# WP-PWD01 Analysis Plan — v0.3

**Status:** PRE-SCORE ANALYSIS FREEZE. This plan may be amended only before scored-run authorization, or later through an explicit timestamped amendment that distinguishes confirmatory from exploratory analysis.

## Statistical unit

The **run** is the experimental/statistical unit. Individual telemetry messages are repeated observations within a run and must not be counted as independent replicates.

The primary design is paired: within each scenario/block, one `B1_MQTT_QOS1` run and one `W1_OFFLINE_FIRST` run are executed under the same frozen POWDER profile/RF condition, workload generator configuration, and experiment session, with architecture order randomized in advance.

The run order is pre-generated in `randomization-plan.csv` using seed `26082401`; reserve pairs 4–5 exist before outcome inspection and may be executed only under the precision rule.

## Primary analysis cohort and censoring rule

Telemetry generation continues during recovery so B1/W1 experience realistic post-recovery traffic. However, records generated late in the observation window would otherwise have less time to arrive than earlier records.

Therefore the **confirmatory primary cohort is frozen as:**

> all valid records generated at or before the final transition back to `Q0` after the impairment schedule.

The corresponding UTC timestamp is stored as `cohort_cutoff_utc` in the run manifest. In `S0_HEALTHY`, the analogous pseudo-restoration point after the 60 s + 120 s control interval is used.

The endpoint observation closes at `horizon_end_utc = cohort_cutoff_utc + H`.

Records generated after `cohort_cutoff_utc` continue to create realistic traffic/load but are **not** included in the primary completeness denominator. They may support exploratory steady-state/recovery diagnostics.

## Primary endpoint

For each valid run:

`completeness_H = unique valid primary-cohort records received no later than horizon_end_utc / primary-cohort generated records`

A received record is valid only when its record identity belongs to the generated cohort and its SHA-256 payload checksum matches the generated ledger.

Report completeness as both proportion and percentage, together with numerator and denominator.

The deterministic implementation is `wellpulse.powder_analysis.reconstruct_primary_endpoint`; the one-run CLI is `scripts/analyze_wp_pwd01_run.py`.

## Primary estimand

For each impairment scenario separately:

`delta_completeness = completeness_H(W1) - completeness_H(B1)`

Report:
- each paired-block difference;
- mean paired difference;
- median paired difference;
- two-sided 95% confidence interval for the mean paired difference;
- raw run-level completeness values.

Effect magnitude and engineering meaning are primary. Do not reduce the conclusion to a binary p-value decision.

## Precision-based replication

`S0_HEALTHY` always uses 3 pairs.

For `S1_INTERMITTENT`, `S2_HARD_OUTAGE`, and `S3_OUTAGE_RESTART`:
1. execute 3 valid paired blocks;
2. compute the two-sided 95% Student-t interval for the three paired run-level completeness differences;
3. if CI half-width <= 2 percentage points and there are no unresolved protocol deviations, stop that scenario;
4. otherwise execute exactly 2 additional pre-authorized paired blocks (5 total pairs).

Do not inspect p-values, effect direction, or manuscript desirability when deciding whether to add the two pairs.

## Secondary endpoints

### Reliability/integrity
- permanent missing rate in the primary cohort;
- duplicate delivery attempts;
- final duplicate rate after idempotent sink;
- checksum mismatch count;
- unexpected record attempt count;
- out-of-order rate.

### Recovery
- transport reconnect time;
- time from physical Q0 restoration to first successful post-outage delivery;
- backlog-drain time for the pre-restoration cohort;
- reconciliation-completion time.

### Performance/overhead
- end-to-end latency p50/p95/p99 where timestamp quality is valid;
- CPU utilization;
- RSS/memory;
- queue depth and durable disk bytes;
- network byte/packet overhead and retransmission indicators where available.

### Radio characterization
Summarize programmed attenuation and all valid exposed RSRP/RSRQ/SINR/BLER/throughput/attach-state measurements by RF state and run.

## Analysis methods

- Preserve and visualize all run-level observations; do not report only aggregate means.
- Use paired differences for B1 vs W1 comparisons.
- Use bootstrap confidence intervals as a sensitivity analysis when sample size reaches 5 pairs; the frozen precision stopping rule itself remains the t-interval rule above.
- Use non-parametric paired tests only as secondary/sensitivity analyses if distributions make them meaningful; no test result determines run inclusion.
- Report absolute differences before relative percentages when the baseline approaches 0% or 100%.
- For latency/recovery distributions, report median and p95/p99 where sample support and timestamp quality are adequate.
- Do not infer statistical independence from the number of messages.
- Receiver rows after `horizon_end_utc` are excluded from the confirmatory endpoint but retained immutably for exploratory diagnostics.

## Scenario interpretation hierarchy

- `S0`: healthy-path equivalence/overhead sanity; no resilience win is expected or required.
- `S1`: repeated physical-RF intermittency; primary evidence for intermittent-connectivity behavior.
- `S2`: hard RF outage/recovery; primary evidence for deterministic disconnection behavior.
- `S3`: hard outage + gateway-process restart; evidence for durability across loss of volatile client state.

Do not generalize an S3 durability advantage to a claim that W1 always outperforms B1 under network-only impairment.

## FIT integration

Existing FIT WP-RT01 results remain a separate evidence class. They are used for triangulation and cross-layer discussion, not pooled statistically with POWDER runs.

The manuscript may compare patterns such as completeness/recovery qualitatively or through clearly separated tables, but must retain platform, hardware, impairment mechanism, and baseline differences.

## OTA replication

The OTA layer is external replication, not extra samples for the conducted-RF inferential dataset.

Run B1/W1 x 3 paired blocks for `S1` and `S2` only. Report OTA effects separately, then assess whether effect direction/magnitude is consistent with the conducted layer.

## Missing data and invalid runs

- Do not impute missing telemetry records; missingness is often the endpoint.
- A technically invalid run is excluded from confirmatory estimates only under the protocol's pre-defined invalidity rules.
- The invalid run and reason remain visible in the ledger and artifact.
- A replacement run is new evidence with a new run ID and cannot overwrite the invalid run.
- Late delivery after H is not imputed as on-time delivery; it remains visible as a post-horizon observation.

## Protocol deviations

Each deviation is classified before outcome analysis as:
- `NONE`;
- `MINOR_NON_ENDPOINT_AFFECTING`;
- `MAJOR_ENDPOINT_AFFECTING`.

Major deviations require exclusion from the confirmatory estimate but retention in the artifact. Minor deviations are retained and disclosed.

## Confirmatory vs exploratory outputs

Confirmatory:
- completeness_H and scenario-specific paired W1-B1 differences;
- pre-defined integrity and recovery endpoints;
- pre-defined overhead metrics;
- conducted/OTA separation.

Exploratory, unless frozen before scoring:
- post-hoc subgrouping by unplanned RF thresholds;
- alternative traffic-rate or MQTT-QoS sweeps;
- correlations chosen after looking at outcomes;
- new composite resilience scores;
- post-horizon late-delivery behavior;
- any model fitted after outcome inspection.

Exploratory analyses may be useful, but must be labeled and cannot rewrite the confirmatory question.

## Reproducible output target

A pinned analysis environment must provide one documented command that:
1. verifies SHA-256 evidence manifests;
2. validates run manifests/schema;
3. reconstructs generated/received identity sets;
4. computes run-level endpoints using the frozen cohort/censoring rule;
5. applies the frozen pairing/precision rules;
6. produces publication tables and figures without manual spreadsheet editing.

No scored result is considered publication-ready until it can be reconstructed from immutable evidence plus a specific analysis-code commit.
