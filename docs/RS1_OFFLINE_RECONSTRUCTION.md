# WP2 RS-1 — Offline Evidence Reconstruction

**Status:** ACTIVE / OFFLINE ONLY  
**Parent gate:** `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`  
**H1 classification:** `VALID_W1_RECOVERY_FAILURE`  
**H:** `UNFROZEN`  
**Scored runs:** `NOT AUTHORIZED`

## Purpose

RS-1 reconstructs the 2026-08-26 H1 physical trial from the preserved raw artifacts. It is analysis/reconciliation work only. It must not issue RF, LTE, MQTT, broker, or other live-testbed control commands.

The objective is to recover the actual scientific timeline and record-level evidence needed for the recovery-semantics consortium:

`t_rf_restore -> service state -> application queue state -> record delivery/completion state`

The reconstruction must be grounded in raw CSV/JSON/SQLite/log artifacts rather than narrative summaries alone.

## Canonical RS-1A tool

Canonical script:

`scripts/wp2_rs1a_sender_reconstruct.py`

Role: reconstruct the H1 **sender-side** timeline and durable-queue state.

It is intentionally read-only with respect to admitted evidence. It:

- locates and SHA-256 hashes the preserved sender artifacts;
- reconstructs Q3 and Q0/RF-restoration timestamps;
- reconstructs the attenuation command timeline;
- counts generated records, unique IDs, duplicates, and the pre-restoration cohort;
- reconstructs queue state around Q3 and RF restoration;
- reports first disconnected sender sample, peak backlog, and final queue state;
- summarizes MQTT event transitions without emitting payload bodies;
- opens the preserved SQLite queue in read-only mode and reports state counts;
- cross-checks the raw reconstruction against `sender_summary.json`;
- emits a deterministic text reconstruction and SHA-256 digest.

## Required preserved sender artifacts

RS-1A expects these artifacts somewhere under the supplied evidence root:

- `sender_summary.json`
- `calibration_manifest.json`
- `attenuation_timeline.csv`
- `telemetry_generated.csv`
- `queue_timeline.csv`
- `mqtt_events.jsonl`
- `w1_queue.sqlite`

Default historical root from the POWDER session:

`~/wellpulse-powder-evidence/wp2-h1-valid-failure-20260826/nuc2`

Because the script searches recursively, the exact copied subdirectory structure under that root is not required to match `/tmp`.

## Offline use

Default invocation on a machine where the preserved evidence tree has been restored:

```bash
python3 scripts/wp2_rs1a_sender_reconstruct.py
```

Portable invocation:

```bash
python3 scripts/wp2_rs1a_sender_reconstruct.py \
  --root /path/to/restored/wp2-h1-valid-failure-20260826/nuc2 \
  --output-dir /path/to/rs1-output
```

No POWDER reservation is required.

## RS-1 decomposition

RS-1A alone is not the final H1 scientific reconstruction. The complete gate is:

| Subtask | Evidence domain | Intended result |
|---|---|---|
| RS-1A | sender / durable queue / RF schedule | generated cohort, queue trajectory, MQTT sender transitions |
| RS-1B | receiver | actual received records, timestamps, hashes, duplicates/missing records |
| RS-1C | UE/eNB/EPC/SPGW logs | service-loss and LTE recovery chronology |
| RS-1D | cross-side reconciliation | generated vs received vs durable state, record-level integrity |
| RS-1E | derived scientific outputs | timeline table, recovery table, queue curve, evidence for RS-2/RS-3 |

## Evidence doctrine

- H1 remains `VALID_W1_RECOVERY_FAILURE` regardless of whether later reconstruction is favorable or unfavorable.
- Reconstruction cannot retroactively change H1 validity.
- Raw evidence and its existing chain-of-custody hashes remain the authority; derived RS-1 outputs are secondary artifacts.
- Do not publish raw private keys, credentials, or sensitive experiment material.
- No H rerun is authorized by completion of RS-1 alone.

## Exit condition

RS-1 closes only when sender, receiver, and LTE/core evidence are reconciled into one explicit event timeline with record-level accounting sufficient for the consortium to distinguish:

1. RF restoration;
2. usable network-service restoration/non-restoration;
3. application backlog recovery/non-recovery.

Only then may the project proceed to RS-2 LTE recovery-mechanism review and RS-3 estimand/H review.
