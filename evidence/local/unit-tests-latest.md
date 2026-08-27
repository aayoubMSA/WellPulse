# Local unit-test gate — latest

- Checked UTC: 2026-08-27T16:04:30Z
- GitHub SHA: 99b7b7e25eb24c7497575cb13e9cf165fbca2c3b
- Python: Python 3.12.14
- Paho MQTT: 2.1.0
- Gate: **FAIL**
- Exit code: `1`

```text
test_b0_normal_path (test_harness.HarnessTests.test_b0_normal_path) ... ok
test_b0_publish_only_loses_entire_outage_window (test_harness.HarnessTests.test_b0_publish_only_loses_entire_outage_window) ... ok
test_b1_volatile_baseline_loses_only_pre_restart_pending_state (test_harness.HarnessTests.test_b1_volatile_baseline_loses_only_pre_restart_pending_state) ... ok
test_b1_volatile_baseline_recovers_network_only_outage (test_harness.HarnessTests.test_b1_volatile_baseline_recovers_network_only_outage) ... ok
test_w1_recovers_network_outage (test_harness.HarnessTests.test_w1_recovers_network_outage) ... ok
test_w1_recovers_outage_and_process_restart (test_harness.HarnessTests.test_w1_recovers_outage_and_process_restart) ... ok
test_ceil_to_30 (test_horizon.RecoveryHorizonTests.test_ceil_to_30) ... ok
test_exact_150_second_drain_yields_300_second_horizon (test_horizon.RecoveryHorizonTests.test_exact_150_second_drain_yields_300_second_horizon) ... ERROR
test_horizon_rounds_twice_p95_up_to_30_seconds (test_horizon.RecoveryHorizonTests.test_horizon_rounds_twice_p95_up_to_30_seconds) ... ERROR
test_invalid_values_rejected (test_horizon.RecoveryHorizonTests.test_invalid_values_rejected) ... ok
test_nearest_rank_p95_for_three_trials_is_maximum (test_horizon.RecoveryHorizonTests.test_nearest_rank_p95_for_three_trials_is_maximum) ... ok
test_over_150_second_drain_forces_stop_not_cap (test_horizon.RecoveryHorizonTests.test_over_150_second_drain_forces_stop_not_cap) ... ERROR
test_protocol_minimum_horizon_is_120_seconds (test_horizon.RecoveryHorizonTests.test_protocol_minimum_horizon_is_120_seconds) ... ERROR
test_duplicate_corrupt_unexpected_and_post_horizon_attempts_are_separated (test_powder_analysis.PowderAnalysisTests.test_duplicate_corrupt_unexpected_and_post_horizon_attempts_are_separated) ... ok
test_empty_primary_cohort_is_invalid (test_powder_analysis.PowderAnalysisTests.test_empty_primary_cohort_is_invalid) ... ok
test_inconsistent_declared_horizon_is_rejected (test_powder_analysis.PowderAnalysisTests.test_inconsistent_declared_horizon_is_rejected) ... ok
test_non_300_application_horizon_is_rejected (test_powder_analysis.PowderAnalysisTests.test_non_300_application_horizon_is_rejected) ... ok
test_recovery_clocks_are_reported_without_changing_primary_horizon (test_powder_analysis.PowderAnalysisTests.test_recovery_clocks_are_reported_without_changing_primary_horizon) ... ok
test_rf_restore_freezes_primary_denominator_and_service_ready_anchors_300s_horizon (test_powder_analysis.PowderAnalysisTests.test_rf_restore_freezes_primary_denominator_and_service_ready_anchors_300s_horizon) ... ok
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

======================================================================
ERROR: test_exact_150_second_drain_yields_300_second_horizon (test_horizon.RecoveryHorizonTests.test_exact_150_second_drain_yields_300_second_horizon)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/WellPulse/WellPulse/tests/test_horizon.py", line 23, in test_exact_150_second_drain_yields_300_second_horizon
    result = compute_recovery_horizon([120.0, 149.0, 150.0])
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/WellPulse/WellPulse/src/wellpulse/horizon.py", line 47, in compute_recovery_horizon
    raise RuntimeError(
RuntimeError: WP-PWD01 outcome-derived recovery-horizon calibration is superseded; use H_app=300s from t_service_ready per experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md

======================================================================
ERROR: test_horizon_rounds_twice_p95_up_to_30_seconds (test_horizon.RecoveryHorizonTests.test_horizon_rounds_twice_p95_up_to_30_seconds)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/WellPulse/WellPulse/tests/test_horizon.py", line 17, in test_horizon_rounds_twice_p95_up_to_30_seconds
    result = compute_recovery_horizon([40.0, 61.0, 55.0])
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/WellPulse/WellPulse/src/wellpulse/horizon.py", line 47, in compute_recovery_horizon
    raise RuntimeError(
RuntimeError: WP-PWD01 outcome-derived recovery-horizon calibration is superseded; use H_app=300s from t_service_ready per experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md

======================================================================
ERROR: test_over_150_second_drain_forces_stop_not_cap (test_horizon.RecoveryHorizonTests.test_over_150_second_drain_forces_stop_not_cap)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/WellPulse/WellPulse/tests/test_horizon.py", line 28, in test_over_150_second_drain_forces_stop_not_cap
    result = compute_recovery_horizon([120.0, 150.1, 130.0])
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/WellPulse/WellPulse/src/wellpulse/horizon.py", line 47, in compute_recovery_horizon
    raise RuntimeError(
RuntimeError: WP-PWD01 outcome-derived recovery-horizon calibration is superseded; use H_app=300s from t_service_ready per experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md

======================================================================
ERROR: test_protocol_minimum_horizon_is_120_seconds (test_horizon.RecoveryHorizonTests.test_protocol_minimum_horizon_is_120_seconds)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/WellPulse/WellPulse/tests/test_horizon.py", line 11, in test_protocol_minimum_horizon_is_120_seconds
    result = compute_recovery_horizon([10.0, 20.0, 30.0])
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/WellPulse/WellPulse/src/wellpulse/horizon.py", line 47, in compute_recovery_horizon
    raise RuntimeError(
RuntimeError: WP-PWD01 outcome-derived recovery-horizon calibration is superseded; use H_app=300s from t_service_ready per experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md

----------------------------------------------------------------------
Ran 37 tests in 25.698s

FAILED (errors=4)
```
