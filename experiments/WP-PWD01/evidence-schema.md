# WP-PWD01 Evidence Schema — v0.3

Each scored run must have a unique immutable run directory. Raw evidence is preserved even for technically invalid or scientifically negative runs.

## Required run directory

```text
run_<run_id>/
├── run_manifest.json
├── config/
│   ├── architecture.json
│   ├── mqtt.json
│   ├── rf.json
│   └── workload.json
├── telemetry_generated.csv
├── telemetry_received.csv
├── attenuation_timeline.csv
├── radio_metrics.csv
├── process_events.csv
├── system_metrics.csv
├── network_capture.pcap
├── application.log
├── ran.log
├── environment.json
└── checksums.sha256
```

If a technically unavailable artifact cannot be produced, the manifest must explicitly record `not_available` and the reason. Do not silently omit expected artifacts.

## Minimum `run_manifest.json` fields

### Identity/provenance
- `protocol_version`;
- campaign/experiment ID;
- `run_id`, scenario, architecture, paired-block index;
- UTC run start/end;
- WellPulse Git SHA;
- analysis-code Git SHA;
- randomization seed and pre-frozen architecture order;
- orchestration path (`github_actions` or documented emergency path).

### Frozen endpoint timing
- `cohort_cutoff_utc`: final Q0-restoration timestamp after impairment, or analogous pseudo-restoration point in S0;
- `recovery_horizon_s`: frozen H;
- `horizon_end_utc = cohort_cutoff_utc + H`;
- clock synchronization/offset evidence sufficient to interpret these timestamps.

Only records generated at or before `cohort_cutoff_utc` enter the confirmatory primary denominator. Post-cutoff generation continues for realistic load but is not included in the primary cohort.

### POWDER context
- Portal experiment UUID/name/project;
- profile name/project/ID/version or repository revision/hash when exposed;
- profile bindings/parameters;
- aggregate/cluster;
- logical and physical node IDs when exposed;
- hostnames;
- image/OS/kernel;
- SDR/RAN/core-network versions;
- RAT and relevant band/frequency/channel configuration.

### Experimental condition
- architecture (`B1_MQTT_QOS1` or `W1_OFFLINE_FIRST`);
- scenario (`S0`–`S3`);
- paired-block/repetition index;
- telemetry rate;
- warm-up duration;
- exact scored schedule;
- exact Q0–Q3 RF settings;
- restart event timestamp/semantics when applicable;
- protocol-deviation classification and explanation;
- technical-validity state and reason.

### Matched MQTT transport
Record actual runtime values for:
- Python version;
- `paho-mqtt` version — frozen target `2.1.0`;
- MQTT protocol — frozen `MQTTv311`;
- TLS state;
- QoS — frozen `1`;
- `clean_session` — frozen `false`;
- keepalive — frozen `60 s`;
- reconnect minimum/maximum — frozen `1 s / 8 s`;
- outgoing queue limit — frozen `4096`;
- inflight limit — frozen `20`;
- application-level persistence enabled/disabled;
- SQLite version and relevant durability pragmas for W1;
- broker software/version and experiment-relevant broker configuration.

Credentials must never be written to evidence.

## Required telemetry identity

`telemetry_generated.csv` must contain at least:
- `record_id`;
- `generated_ts_utc`;
- `payload_sha256`;
- canonical payload or durable payload reference where publication policy permits.

`telemetry_received.csv` must contain at least:
- `record_id`;
- `received_ts_utc`;
- `payload_sha256`;
- optional transport/session metadata useful for recovery diagnostics.

All delivery attempts should be retained, including duplicate, corrupted, unexpected, and post-horizon attempts. The analysis code, not data deletion, determines confirmatory inclusion.

## Radio evidence

`attenuation_timeline.csv` must contain timestamped programmed RF-state changes and the mapping to Q0–Q3.

`radio_metrics.csv` should contain all exposed measurements needed to characterize the physical condition, targeting:
- RSRP;
- RSRQ;
- SINR;
- BLER;
- throughput;
- attach/session/link state;
- other stack-specific radio metrics that are available and time-aligned.

Absence of a metric is not automatically a failed run if the profile does not expose it, but the absence must be documented before scoring if the metric is part of a frozen claim.

## Process/system evidence

`process_events.csv` must timestamp when observable:
- application/process start;
- MQTT connect/disconnect/reconnect;
- Q0/Q2/Q3 transitions;
- final Q0 restoration / primary `cohort_cutoff_utc`;
- intentional gateway-process restart in S3;
- application-ready state;
- queue-drain/reconciliation start/end.

`system_metrics.csv` should include at least:
- CPU utilization;
- RSS/memory;
- durable queue depth/bytes for W1;
- disk usage attributable to resilience state;
- network byte/packet counters where available.

## Derived metrics

Primary:
- unique valid **primary-cohort** telemetry completeness at frozen H.

Secondary:
- permanent missing count/rate;
- duplicate delivery-attempt count and final duplicate rate;
- checksum mismatch/corruption attempts;
- unexpected-record attempts;
- out-of-order count/rate;
- reconnect time;
- time to first successful post-recovery delivery;
- backlog-drain time;
- reconciliation completion time;
- latency p50/p95/p99 when valid;
- CPU/RAM/disk/network overhead;
- RF/link metrics associated with each state.

The reference run-level reconstruction is `wellpulse.powder_analysis.reconstruct_primary_endpoint` and the CLI is `scripts/analyze_wp_pwd01_run.py`.

## Integrity and anti-bias rules

- Raw evidence is immutable.
- A scientifically valid negative/null run remains in the scored corpus.
- Re-runs require documented pre-defined technical invalidity, never an unfavorable outcome.
- Invalid runs remain archived/listed; replacements receive new run IDs.
- Receiver attempts after `horizon_end_utc` remain in raw evidence but do not count as on-time primary-endpoint delivery.
- Post-cutoff generated records remain in raw evidence but do not enter the primary denominator.
- No manual spreadsheet editing may be required to obtain the primary endpoint or paper figures.
- Large raw evidence may live outside Git history, but SHA-256, durable location, and retrieval metadata must be committed.
- Plumbing/API/feasibility checks under `evidence/powder/` are infrastructure evidence only and are never pooled with scored scientific data.
- Message-level rows are observations inside a run, not independent experimental replicates.

## Publication-artifact gate

Before manuscript freeze, a pinned environment and one documented command must verify evidence hashes/schema and regenerate manuscript tables/figures from raw or immutable processed evidence without manual spreadsheet edits.
