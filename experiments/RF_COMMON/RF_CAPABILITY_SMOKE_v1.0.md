# WellPulse RF Capability Smoke v1.0

Status: FROZEN FOR ACCESS-READY SMOKE
Date: 2026-08-23
Scope: platform-agnostic capability qualification for POWDER, COSMOS/ORBIT, and ARA.

## Purpose
Qualify a newly approved wireless testbed quickly, without redesigning WellPulse or prematurely launching publication-final experiments.

This smoke is NOT publication-final evidence. Evidence class: `CAPABILITY_SMOKE_RF`.

## Reused WellPulse core
Reuse the existing WP-RT01 workload/reconciliation semantics wherever technically compatible:
- architectures: B0 non-durable publish-only baseline and W1 durable offline-first
- record identity: `run_id + boot_id + sequence`
- deterministic workload target: 10,000 records for the final experiment; capability smoke may use a smaller bounded count if needed
- independent receiver-side reconciliation
- no promotion of smoke/pre-final results into final claims

## Required RF states
Every candidate platform must demonstrate all three before a final protocol is frozen:

### R0 — REFERENCE
Healthy RF path with stable end-to-end traffic.

### R1 — DEGRADED_CONNECTED
RF-layer degradation that is measurable and repeatable while the path remains connected.

### R2 — LOSS_RECOVERY
RF-induced loss/detach or equivalent link failure, followed by controlled restoration and successful end-to-end recovery.

Application-layer blocking (`iptables`, broker blocking, synthetic packet dropping) is NOT an acceptable substitute for R1/R2 in this workstream.

## Required synchronized evidence
At minimum preserve:

### Application plane
- run_id
- architecture (`B0` or `W1`)
- generated record count
- locally committed count where applicable
- receiver unique count
- permanent missing count
- final duplicate count
- reconnect/recovery timestamp
- backlog drain completion timestamp where applicable
- queue high-water mark / queue age if available

### RF / link plane
Use the strongest platform-native metrics available, with timestamps:
- RSRP
- RSRQ
- SINR
- RSSI if applicable
- attach/detach state
- attenuation setting or platform-native impairment control
- throughput / packet delivery / latency / jitter only when directly and defensibly instrumented

Do not invent unavailable metrics.

## Time synchronization contract
All platform events and WellPulse events must be alignable on one timeline.
Preferred: UTC wall-clock timestamps plus monotonic local elapsed time.
Each RF-state transition must be logged with:
- platform
- resource ID(s)
- state (`R0`, `R1`, `R2`)
- control action
- requested value
- observed value if available
- UTC timestamp

## Capability-smoke sequence
1. Prove portal/project/resource access.
2. Prove SSH/container/terminal access.
3. Prove end-to-end user-plane traffic through the intended real RF path.
4. Run R0 reference traffic.
5. Apply one bounded RF degradation mechanism and prove R1.
6. Apply one bounded RF loss/detach mechanism and prove R2.
7. Restore RF and prove traffic recovery.
8. Run a bounded WellPulse workload through the same path.
9. Reconcile receiver-side records.
10. Preserve raw logs, platform/resource IDs, code commit, config, and checksums.
11. Decide GO / PIVOT / KILL before any final matrix.

## Kill / pivot rules
KILL or pivot the platform for this claim if any of the following holds:
- no real RF/OTA path is available to the user workload;
- only application-layer impairment is possible;
- RF state cannot be measured or timestamped sufficiently to support the intended claim;
- R1 cannot be reproduced in a bounded way;
- R2 cannot be induced/restored safely and reproducibly;
- custom traffic cannot traverse the intended path;
- WellPulse requires major architecture redesign unrelated to the research question;
- evidence/resource IDs cannot be preserved well enough for reproducibility;
- platform coordination burden materially exceeds the scientific value.

## Final-experiment freeze gate
Only after the smoke passes may a platform-specific final protocol freeze:
- exact resource IDs/classes
- exact RF control mechanism
- exact R0/R1/R2 values
- exact workload count
- exact replication count
- exact measured RF endpoints
- exact evidence-class name

Default candidate final matrix, subject to smoke confirmation:
`B0/W1 × R0/R1/R2 × 3 replicates`, 10,000 records per cell.

Do not execute this matrix automatically. First test whether it adds a material claim beyond existing FIT evidence and whether another testbed has already satisfied the same RF-layer claim.

## Platform adapter boundary
The WellPulse workload and receiver/reconciliation logic should remain unchanged. Only the thin platform adapter should know how to:
- acquire/release resources;
- discover resource identifiers;
- set/read RF controls;
- log RF metrics;
- mark R0/R1/R2 transitions.

Candidate adapters:
- `POWDER`: `srs-rf-matrix` / programmable conducted attenuation
- `COSMOS_ORBIT`: ORBIT `sb4` RF Attenuator Matrix first
- `ARA`: field COTS UE / RAN controls and timestamped radio-state metrics

## Evidence boundary
A passed controlled-RF smoke supports only testbed capability and experiment feasibility. It does not validate rural/Siwa field operation, pump/inverter hardware, hydraulics, groundwater, mechanical faults, or agronomic outcomes.
