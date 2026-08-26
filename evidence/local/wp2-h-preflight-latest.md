# WP2 H Calibration Preflight — latest

- Checked UTC: 2026-08-26T09:29:58Z
- Tested GitHub SHA: e20da2fb186eeab047080cbd851f46c3c96c81f0
- Python: Python 3.12.14
- Paho MQTT: 2.1.0
- Evidence class: **LOCAL PRE-SCORE IMPLEMENTATION QA ONLY**
- POWDER resource interaction: **NONE**
- Scored run interaction: **NONE**
- Gate: **PASS**

```text
## Unit tests
test_b0_normal_path (test_harness.HarnessTests.test_b0_normal_path) ... ok
test_b0_publish_only_loses_entire_outage_window (test_harness.HarnessTests.test_b0_publish_only_loses_entire_outage_window) ... ok
test_b1_volatile_baseline_loses_only_pre_restart_pending_state (test_harness.HarnessTests.test_b1_volatile_baseline_loses_only_pre_restart_pending_state) ... ok
test_b1_volatile_baseline_recovers_network_only_outage (test_harness.HarnessTests.test_b1_volatile_baseline_recovers_network_only_outage) ... ok
test_w1_recovers_network_outage (test_harness.HarnessTests.test_w1_recovers_network_outage) ... ok
test_w1_recovers_outage_and_process_restart (test_harness.HarnessTests.test_w1_recovers_outage_and_process_restart) ... ok
test_ceil_to_30 (test_horizon.RecoveryHorizonTests.test_ceil_to_30) ... ok
test_exact_150_second_drain_yields_300_second_horizon (test_horizon.RecoveryHorizonTests.test_exact_150_second_drain_yields_300_second_horizon) ... ok
test_horizon_rounds_twice_p95_up_to_30_seconds (test_horizon.RecoveryHorizonTests.test_horizon_rounds_twice_p95_up_to_30_seconds) ... ok
test_invalid_values_rejected (test_horizon.RecoveryHorizonTests.test_invalid_values_rejected) ... ok
test_nearest_rank_p95_for_three_trials_is_maximum (test_horizon.RecoveryHorizonTests.test_nearest_rank_p95_for_three_trials_is_maximum) ... ok
test_over_150_second_drain_forces_stop_not_cap (test_horizon.RecoveryHorizonTests.test_over_150_second_drain_forces_stop_not_cap) ... ok
test_protocol_minimum_horizon_is_120_seconds (test_horizon.RecoveryHorizonTests.test_protocol_minimum_horizon_is_120_seconds) ... ok
test_duplicate_corrupt_unexpected_and_late_attempts_are_separated (test_powder_analysis.PowderAnalysisTests.test_duplicate_corrupt_unexpected_and_late_attempts_are_separated) ... ok
test_empty_primary_cohort_is_invalid (test_powder_analysis.PowderAnalysisTests.test_empty_primary_cohort_is_invalid) ... ok
test_post_cutoff_generation_is_not_in_primary_denominator (test_powder_analysis.PowderAnalysisTests.test_post_cutoff_generation_is_not_in_primary_denominator) ... ok
test_does_not_hand_durable_backlog_to_paho_while_disconnected (test_powder_w1.DurablePahoReplayTests.test_does_not_hand_durable_backlog_to_paho_while_disconnected) ... ok
test_inflight_is_bounded_and_sent_only_after_ack (test_powder_w1.DurablePahoReplayTests.test_inflight_is_bounded_and_sent_only_after_ack) ... ok
test_queue_is_idempotent (test_records.WellPulseKernelTests.test_queue_is_idempotent) ... ok
test_reconciliation_detects_loss_and_duplicate (test_records.WellPulseKernelTests.test_reconciliation_detects_loss_and_duplicate) ... ok
test_record_id_is_deterministic (test_records.WellPulseKernelTests.test_record_id_is_deterministic) ... ok
test_conflicting_duplicate_record_id_fails_closed (test_store.DurableQueueIntegrityTests.test_conflicting_duplicate_record_id_fails_closed) ... ok
test_exact_duplicate_is_idempotent (test_store.DurableQueueIntegrityTests.test_exact_duplicate_is_idempotent) ... ok
test_disconnected_qos1_publish_is_counted_as_accepted_unacked (test_transport.PahoTransportTests.test_disconnected_qos1_publish_is_counted_as_accepted_unacked) ... ok
test_frozen_public_config_is_reproducible_and_secret_safe (test_transport.PahoTransportTests.test_frozen_public_config_is_reproducible_and_secret_safe) ... ok
test_run_isolation_identifiers_are_deterministic_and_distinct (test_transport.PahoTransportTests.test_run_isolation_identifiers_are_deterministic_and_distinct) ... ok
test_session_constructs_with_explicit_volatile_queue (test_transport.PahoTransportTests.test_session_constructs_with_explicit_volatile_queue) ... ok
test_unbounded_queue_is_rejected (test_transport.PahoTransportTests.test_unbounded_queue_is_rejected) ... ok
test_broker_shell_script_passes_bash_syntax (test_wp2_h_pilot_scripts.WP2HPilotScriptTests.test_broker_shell_script_passes_bash_syntax) ... ok
test_finalizer_reconstructs_conservative_drain_time (test_wp2_h_pilot_scripts.WP2HPilotScriptTests.test_finalizer_reconstructs_conservative_drain_time) ... ok
test_missing_cohort_record_is_valid_adverse_outcome_not_invalidity (test_wp2_h_pilot_scripts.WP2HPilotScriptTests.test_missing_cohort_record_is_valid_adverse_outcome_not_invalidity) ... ok
test_predefined_sender_technical_failure_remains_replaceable (test_wp2_h_pilot_scripts.WP2HPilotScriptTests.test_predefined_sender_technical_failure_remains_replaceable) ... ok
test_python_pilot_scripts_compile (test_wp2_h_pilot_scripts.WP2HPilotScriptTests.test_python_pilot_scripts_compile) ... ok
test_q0_packet_loss_parser_rejects_100_percent_loss (test_wp2_h_pilot_scripts.WP2HPilotScriptTests.test_q0_packet_loss_parser_rejects_100_percent_loss) ... ok

----------------------------------------------------------------------
Ran 34 tests in 11.473s

OK

## Python script compile

## Shell syntax

## Frozen-state and P0 guards
frozen-state and P0 guards: PASS
```
