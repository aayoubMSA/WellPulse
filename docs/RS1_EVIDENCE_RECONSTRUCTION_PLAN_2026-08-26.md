# RS-1 — H1 Raw Evidence Reconstruction Plan

Date: 2026-08-26
Stage: POST-H1 / PRE-AMENDMENT / PRE-SCORE
Scientific completion: 20%
Scored runs authorized: false
H: UNFROZEN
H1 classification: VALID_W1_RECOVERY_FAILURE

## Objective

Reconstruct the physical H1 trial and its post-trial recovery chain directly from preserved raw artifacts. This step is evidence extraction only. It must not change RF state, LTE configuration, MQTT state, protocol semantics, H, or the H1 classification.

## Canonical run

- Experiment: WP-HCAL-E
- Run ID: `wp2h1-a1-20260826-001`
- Sender node: `nuc2`
- Receiver/core node: `nuc1`

## Required raw sources

Sender-side evidence:
- `telemetry_generated.csv`
- `attenuation_timeline.csv`
- `queue_timeline.csv`
- `mqtt_events.jsonl`
- `sender_summary.json`
- `calibration_manifest.json`
- `w1_queue.sqlite`
- UE logs captured in the H1 preservation bundle

Receiver/core-side evidence:
- `telemetry_received.csv`
- `receiver_events.jsonl`
- EPC/eNB logs captured in the H1 preservation bundle

The exact runner schemas are defined by:
- `scripts/wp_pwd01_h_sender.py`
- `scripts/wp_pwd01_h_receiver.py`

## Events to reconstruct

At minimum RS-1 must identify or explicitly mark unavailable:

1. sender/receiver start;
2. initial Q0 readiness;
3. MQTT connect and initial `session_present` evidence;
4. first generated record;
5. Q3 command start and full Q3 effective time;
6. application/MQTT disconnection evidence;
7. Q0 restore command start and completion (`t_rf_restore`);
8. post-restore LTE/RRC/EPC recovery attempts;
9. any evidence of radio-layer recovery;
10. whether usable user-plane service returned naturally during H1 (`t_service_ready`, expected absent for H1);
11. queue/pending state at stop;
12. last generated and last received records;
13. integrity relation between generated and received record IDs/checksums;
14. exact stop time and stop reason;
15. later diagnostic recovery actions kept strictly separate from the H1 trial.

## Required derived tables

RS-1 must produce three reconstruction tables:

### T1 — Event timeline
Columns: `event`, `utc`, `source_artifact`, `evidence_class`, `notes`.

### T2 — Record reconciliation
At minimum: generated count, received unique count, generated-before-cutoff count, received-before/after-cutoff counts where reconstructable, missing IDs, duplicate IDs, checksum mismatches, last generated timestamp, last received timestamp.

### T3 — Queue/MQTT state
At minimum: pre-Q3 pending/inflight, peak pending during outage, pending at Q0 restore, pending at stop, published calls, PUBACK callbacks, MQTT connected/disconnected transitions.

## Frozen interpretation boundary

RS-1 may report what the artifacts show, but it must not yet decide whether the clean-order LTE restart is scientifically admissible. That decision belongs to RS-2/RS-3.

H1 remains `VALID_W1_RECOVERY_FAILURE`; no evidence extracted in RS-1 may retroactively convert it to a successful calibration trial or a technically invalid trial.

## Exit condition

PASS only when the raw sender/receiver/LTE evidence has been enumerated, integrity-checked, and sufficient structured facts exist to reconstruct T1-T3 without relying on narrative summaries alone.
