# WP-PWD01 Evidence Schema — v0.2

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

If a technically unavailable artifact cannot be produced (for example a particular RAN metric or packet capture), the manifest must explicitly record `not_available` and the reason. Do not silently omit files expected by the protocol.

## Minimum `run_manifest.json` fields

Identity/provenance:
- protocol version;
- experiment campaign ID;
- run ID and paired-block ID;
- UTC start/end timestamps;
- Git commit SHA for WellPulse;
- analysis-code commit SHA;
- randomization seed and architecture order;
- operator/orchestration path (`github_actions`, manual emergency path, etc.).

POWDER context:
- Portal experiment UUID/name/project;
- profile name, project, immutable identifier/revision/hash if exposed;
- profile bindings/parameters;
- aggregate/cluster;
- logical node IDs;
- physical node IDs when exposed;
- hostnames;
- image/OS/kernel;
- SDR/RAN/core-network versions;
- clock synchronization status/offset evidence.

Experimental condition:
- architecture (`B1_MQTT_QOS1` or `W1_OFFLINE_FIRST`);
- scenario (`S0`–`S3`);
- paired-block/repetition index;
- telemetry rate;
- warm-up duration;
- scored schedule;
- frozen recovery horizon `H`;
- exact Q0–Q3 RF settings;
- restart event timestamp and semantics when applicable;
- protocol-deviation flag and explanation;
- technical-validity state and reason.

Baseline/treatment configuration:
- Python version;
- Paho MQTT version;
- MQTT protocol version;
- TLS state;
- QoS;
- clean-session/session-expiry semantics;
- reconnect-delay configuration;
- outgoing/inflight queue limits;
- application-level persistence enabled/disabled;
- SQLite version and relevant durability pragmas for W1;
- broker software/version/config relevant to experiment.

## Required telemetry identity

Every generated record must preserve at minimum:
- `record_id` or deterministic `seq_id`;
- `generated_ts_utc`;
- canonical payload or payload reference;
- `payload_sha256`.

Every delivery attempt/received record should preserve when technically possible:
- `received_ts_utc`;
- `record_id`;
- `payload_sha256`;
- duplicate/first-seen status;
- transport/session metadata needed to interpret recovery.

## Radio evidence

`attenuation_timeline.csv` must contain timestamped programmed RF-state changes.

`radio_metrics.csv` should contain all exposed measurements needed to characterize the physical condition, targeting:
- RSRP;
- RSRQ;
- SINR;
- BLER;
- throughput;
- attach/session/link state;
- other srsRAN/5G metrics that are available and time-aligned.

Absence of a requested radio metric is not a failed run if the platform/profile does not expose it, but the absence must be documented before scored-run authorization if the metric is part of a frozen claim.

## Process/system evidence

`process_events.csv` must timestamp:
- process start;
- MQTT connect/disconnect/reconnect;
- Q0/Q2/Q3 transitions as observed by orchestration;
- intentional process restart in S3;
- application ready state;
- queue-drain start/end where observable.

`system_metrics.csv` should include at least:
- CPU utilization;
- RSS/memory;
- durable queue depth/bytes for W1;
- disk usage attributable to resilience state;
- network byte/packet counters where technically available.

## Derived metrics

Primary:
- unique valid telemetry completeness at frozen horizon H.

Secondary:
- permanent missing count/rate;
- duplicate attempts and final duplicate rate;
- checksum mismatch/corruption count;
- out-of-order count/rate;
- reconnect time;
- time to first successful post-recovery delivery;
- backlog-drain time;
- reconciliation completion time;
- latency p50/p95/p99 when valid;
- CPU/RAM/disk/network overhead;
- RF/link metrics associated with each condition.

## Integrity and anti-bias rules

- Raw evidence is immutable.
- A scientifically valid negative/null run remains in the scored corpus.
- Re-runs require a documented technical-invalidity reason, never an unfavorable outcome.
- Invalid runs remain archived and listed in the run ledger; replacements receive new run IDs.
- No manual spreadsheet editing may be required to obtain the primary endpoint or paper figures.
- Large raw evidence may live outside Git history, but its SHA-256, durable location, and retrieval metadata must be committed.
- Plumbing/API checks under `evidence/powder/` are infrastructure evidence only and are never pooled with scored scientific data.
- Message-level rows are observations inside a run; they are not treated as independent experimental replicates.

## Publication-artifact gate

Before manuscript freeze, the artifact must be able to regenerate all manuscript tables/figures from raw or immutable processed evidence with one documented command and a pinned environment.
