# WellPulse pre-score local gate — latest

- Checked UTC: 2026-08-24T17:49:33Z
- GitHub SHA: 67e268896d8059c42f4d1898724e51b719b8a456
- Python: Python 3.12.14
- Paho MQTT: 2.1.0
- Tests discovered: 15
- Gate: **PASS**

```text
test_b0_normal_path (test_harness.HarnessTests.test_b0_normal_path) ... ok
test_b0_publish_only_loses_entire_outage_window (test_harness.HarnessTests.test_b0_publish_only_loses_entire_outage_window) ... ok
test_b1_volatile_baseline_loses_only_pre_restart_pending_state (test_harness.HarnessTests.test_b1_volatile_baseline_loses_only_pre_restart_pending_state) ... ok
test_b1_volatile_baseline_recovers_network_only_outage (test_harness.HarnessTests.test_b1_volatile_baseline_recovers_network_only_outage) ... ok
test_w1_recovers_network_outage (test_harness.HarnessTests.test_w1_recovers_network_outage) ... ok
test_w1_recovers_outage_and_process_restart (test_harness.HarnessTests.test_w1_recovers_outage_and_process_restart) ... ok
test_duplicate_corrupt_unexpected_and_late_attempts_are_separated (test_powder_analysis.PowderAnalysisTests.test_duplicate_corrupt_unexpected_and_late_attempts_are_separated) ... ok
test_empty_primary_cohort_is_invalid (test_powder_analysis.PowderAnalysisTests.test_empty_primary_cohort_is_invalid) ... ok
test_post_cutoff_generation_is_not_in_primary_denominator (test_powder_analysis.PowderAnalysisTests.test_post_cutoff_generation_is_not_in_primary_denominator) ... ok
test_queue_is_idempotent (test_records.WellPulseKernelTests.test_queue_is_idempotent) ... ok
test_reconciliation_detects_loss_and_duplicate (test_records.WellPulseKernelTests.test_reconciliation_detects_loss_and_duplicate) ... ok
test_record_id_is_deterministic (test_records.WellPulseKernelTests.test_record_id_is_deterministic) ... ok
test_frozen_public_config_is_reproducible_and_secret_safe (test_transport.PahoTransportTests.test_frozen_public_config_is_reproducible_and_secret_safe) ... ok
test_session_constructs_with_explicit_volatile_queue (test_transport.PahoTransportTests.test_session_constructs_with_explicit_volatile_queue) ... ok
test_unbounded_queue_is_rejected (test_transport.PahoTransportTests.test_unbounded_queue_is_rejected) ... ok

----------------------------------------------------------------------
Ran 15 tests in 16.142s

OK
```
