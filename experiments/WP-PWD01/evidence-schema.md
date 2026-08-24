# WP-PWD01 Evidence Schema

Each scored run must have a unique run directory and immutable manifest.

## Required run artifacts

- `run_manifest.json`
- `telemetry_generated.csv`
- `telemetry_received.csv`
- `attenuation_timeline.csv`
- `network_capture.pcap` or equivalent packet capture when technically available
- `wellpulse.log` or `baseline.log`
- `ran.log` or equivalent radio/network log
- `system_metrics.csv`
- `checksums.sha256`

## Minimum run manifest fields

- experiment_id
- run_id
- UTC start/end timestamps
- Git commit SHA
- POWDER profile name/version
- POWDER experiment identifier
- allocated node identifiers
- mode (`B0` or `W1`)
- scenario (`S0`–`S3`)
- repetition index
- telemetry rate
- warm-up duration
- scored duration
- recovery-window definition
- frozen Q0–Q3 numeric RF settings
- software/package versions
- operator/orchestration path
- protocol deviation flag and explanation

## Minimum telemetry identity

Every generated record must preserve:

- `seq_id`
- `generated_ts`
- `payload_hash`

Every received record must additionally preserve:

- `received_ts`

## Derived metrics

- eventual unique-record completeness
- missing-record count/rate
- duplicate count/rate
- out-of-order count/rate
- recovery time
- backlog-drain time
- end-to-end latency distribution
- reconnect/session events

## Integrity rules

- Raw evidence is never edited to improve a result.
- A failed or negative scientifically valid run remains part of the scored corpus.
- Re-runs require a documented technical-invalidity reason, not an unfavorable outcome.
- Large raw evidence may be stored outside Git history, but its immutable checksum and location manifest must be committed.
- Plumbing checks under `evidence/powder/` are infrastructure evidence only and must not be mixed into the scored corpus.
