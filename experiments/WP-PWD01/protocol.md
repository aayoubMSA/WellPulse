# WP-PWD01 — POWDER Real-RF Resilience Validation

**Status:** PRE-FREEZE — plumbing bootstrap only. No scored run is authorized by this file.

## Scientific question

Does the existing WellPulse offline-first resilience path preserve eventual unique telemetry completeness and recover automatically under real wireless degradation/outage better than the same transport path without durable application buffering/reconciliation?

## Evidence boundary

This experiment may support networking, radio-link resilience, edge/cloud recovery, telemetry completeness, reconnect behavior, and related systems claims.

It does **not** validate pump mechanics, hydraulics, groundwater, crop physiology, Siwa environmental conditions, or agricultural field performance.

## Planned evidence ladder

1. Existing WellPulse implementation and prior real-node evidence.
2. POWDER conducted real-radio experiment with programmable physical RF attenuation.
3. Minimal POWDER indoor OTA confirmation if the conducted gate passes.
4. Outdoor/rural extension only by a later explicit decision.

## Modes

- `B0`: matched baseline without durable application queue/reconciliation.
- `W1`: WellPulse offline-first path with durable buffering, reconnect, reconciliation, and backlog drain.

Only the resilience mechanism should differ between modes.

## Primary endpoint

Eventual **unique-record completeness** after a predefined recovery window.

## Secondary endpoints

- recovery time;
- backlog-drain time;
- end-to-end latency;
- duplicate rate;
- out-of-order rate;
- missing-record count;
- reconnect/session events.

## Pre-score gates

Before any scored run:

- end-to-end telemetry passes through the experimental radio/data path, not the POWDER control network;
- record identity is preserved end-to-end;
- physical RF degradation can be controlled and logged;
- a true outage state can be induced and recovered;
- clocks/logging/evidence capture are adequate;
- B0 and W1 are implementation-matched except for the resilience mechanism;
- numeric RF levels and recovery window are frozen after non-scored calibration.

## Prohibited drift

Do not add GPU, massive-MIMO, O-RAN/RIC, mobility, multi-site, or outdoor claims unless they become necessary to answer the frozen question and are approved as a separate extension.
