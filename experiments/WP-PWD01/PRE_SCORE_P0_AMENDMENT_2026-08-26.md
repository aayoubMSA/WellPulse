# WP-PWD01 — P0 Pre-Score Amendment

**Date:** 2026-08-26  
**Authority:** approved independent pre-WP3 consortium review  
**Status:** FROZEN PRE-SCORE AMENDMENT  
**Scored runs authorized:** **NO**

This amendment is authoritative for the affected rules below and is read together with `protocol.md` v0.4, `analysis-plan.md` v0.3, `evidence-schema.md` v0.3, `H_CALIBRATION_PLAN_v1.md`, and `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`.

It does not reopen RF calibration, alter Q0-Q3, change the H formula, authorize WP3, or change the frozen B1/W1 randomization order.

## P0-1 — Separate technical invalidity from adverse W1 recovery outcome

For WP2 H calibration, only predefined infrastructure/protocol failures are `TECHNICALLY_INVALID` and replaceable.

A correctly applied W1 trial that loses a cohort record, fails to drain durable pending state, or exceeds the frozen recovery bound is:

`VALID_W1_RECOVERY_FAILURE`

It is adverse evidence, is not replaceable as invalid, and blocks H freeze pending investigation.

A successful calibration trial is:

`VALID_W1_RECOVERY_SUCCESS`

H requires exactly three successful technically valid trials. Extra successful trials are not authorized.

Implementation authority:

- `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`
- `scripts/finalize_wp_pwd01_h_calibration.py`

## P0-2 — MQTT run/session isolation

Every future calibration or scored run must use run-isolated MQTT state.

Required rules:

1. deterministic run-unique publisher client identity;
2. deterministic run-unique receiver client identity;
3. deterministic run-unique topic namespace;
4. first connection for a fresh run must record `session_present=false` for each run-specific client whose prior state could affect the endpoint;
5. client ID, topic, connection count, and session-present evidence must be preserved;
6. client/topic identity must never be reused across independent runs;
7. the only intended reuse of a run-specific gateway client identity is the intra-run gateway-process restart in `S3_OUTAGE_RESTART`.

Helpers are implemented in `src/wellpulse/transport.py`.

The H-calibration sender/receiver now derive isolated identities/topics automatically and fail the first-connection isolation gate if an unexpected prior session is resumed.

## P0-3 — Freeze the S3 failure domain before scored execution

`S3_OUTAGE_RESTART` must test loss of volatile gateway/client process state, not loss of the telemetry source itself.

Before scored authorization, the implementation must demonstrate non-scored that:

- the telemetry generator/source is outside the gateway restart domain;
- generation continues at the frozen 1 record/s across the restart;
- only the gateway/client process is intentionally restarted;
- restart start/end/downtime are timestamped;
- W1 durable SQLite state survives the process restart;
- B1 recreates the volatile Paho client using the same run-specific client identity within that S3 run;
- source record sequence/identity remains continuous across the restart;
- no node power cycle or hardware reboot is substituted for the frozen gateway-process restart.

This is a new explicit pre-score gate. It does not add a new scored scenario.

## P0-4 — B1 accepted-message instrumentation semantics

The B1 Paho instrumentation must not equate a local counter with exact Paho internal queue occupancy.

`PahoQoS1Session` now records:

- total publish calls;
- publish calls accepted into the volatile QoS1 path, including accepted disconnected submissions;
- PUBACK callbacks;
- accepted-but-unacknowledged message IDs/count;
- connection count and latest `session_present` state.

The compatibility field `outstanding_mid_count` has the same accepted-but-unacknowledged semantics. It must not be described as exact internal queue occupancy.

Any scientific claim about B1 loss/completeness is reconstructed from generated/received record identity and checksum evidence, not from this internal counter alone.

## P0-5 — Fail closed on record-identity collision

`DurableQueue.enqueue()` must not silently ignore conflicting reuse of `record_id`.

Frozen behavior:

- exact same canonical payload + checksum with the same `record_id` is idempotent;
- same `record_id` with different payload/checksum raises an integrity error;
- conflicting identity reuse must be visible in evidence and cannot be silently converted into a successful enqueue.

Implementation authority:

- `src/wellpulse/store.py`
- `tests/test_store.py`

## Added WP2 pre-score gates

The following must be PASS before `scored_runs_authorized=true`:

- H technical-invalidity/adverse-outcome classification verified;
- MQTT client/topic/session isolation verified on the physical pilot path;
- record-identity collision fail-closed behavior verified;
- B1 accepted/unacknowledged instrumentation semantics verified;
- S3 restart-domain separation verified non-scored;
- all previously open WP2 runtime/path/identity/clock/analysis/comparator gates remain applicable.

## Frozen state preserved

The following remain unchanged:

```text
Q0 = 0 dB
Q1 = 40 dB
Q2 = 52 dB
Q3 = 55 dB
attenuator IDs = 1 33 2 34
scored_runs_authorized = false
scientific weighted completion = 20%
WP3 = BLOCKED
```

No further RF attenuation hunting is authorized.
