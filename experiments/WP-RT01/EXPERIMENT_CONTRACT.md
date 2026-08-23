# WP-RT01-v1.0 — Experiment Contract

## Claim under test
An offline-first gateway can preserve and reconcile records under connectivity interruption and restart more reliably than a publish-only/non-durable baseline.

## Evidence class
Real embedded-hardware / communications evidence only. No pump-mechanical or Siwa-field claim.

## Target platform
FIT IoT-LAB, subject to an execution-time capability smoke check.

## Input
Exactly 10,000 uniquely identified synthetic Modbus-like records per final run. Synthetic input is intentionally used because sensor/pump physics are outside the experiment claim.

## Conditions
- C0: normal connectivity, no restart.
- C1: connectivity interruption, no restart.
- C2: connectivity interruption with gateway restart during interruption.

Each condition is run for:
- B0: publish-only/non-durable baseline.
- W1: WellPulse durable offline-first queue and reconciliation.

Minimum final replication target: 3 runs per condition/architecture cell, unless platform constraints force a preregistered amendment before the first final run.

## Primary endpoints
- generated records
- cloud unique records
- permanent missing records
- duplicate final records
- completeness percentage
- reconnect time
- backlog drain time
- p50/p95/p99 delivery latency
- recovery after restart

## Primary success criterion for W1
For a 10,000-record run: 10,000 unique final cloud records, zero permanent missing records, and zero duplicate final records.

## Capability gate
Before final runs, verify on the reserved FIT node: runtime, persistent storage path, outbound MQTT/TLS, clock, disk, and whether reproducible traffic impairment via `tc/netem` is actually available. If `tc/netem` is unavailable, use a deterministic transport-blocking/disconnection method and record the amendment before final data collection.

## Change control
No post-hoc change to the primary claim, primary endpoints, or success criterion after final data collection begins. Any necessary change is versioned before the affected final run.
