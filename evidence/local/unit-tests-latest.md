# Local unit-test gate — latest

- Checked UTC: 2026-08-24T17:22:43Z
- GitHub SHA: 4039a5e65849ad196cce3ca1a74e4697830f452e
- Python: Python 3.12.14
- Gate: **PASS**

```text
test_b0_normal_path (test_harness.HarnessTests.test_b0_normal_path) ... ok
test_b0_publish_only_loses_entire_outage_window (test_harness.HarnessTests.test_b0_publish_only_loses_entire_outage_window) ... ok
test_b1_volatile_baseline_loses_only_pre_restart_pending_state (test_harness.HarnessTests.test_b1_volatile_baseline_loses_only_pre_restart_pending_state) ... ok
test_b1_volatile_baseline_recovers_network_only_outage (test_harness.HarnessTests.test_b1_volatile_baseline_recovers_network_only_outage) ... ok
test_w1_recovers_network_outage (test_harness.HarnessTests.test_w1_recovers_network_outage) ... ok
test_w1_recovers_outage_and_process_restart (test_harness.HarnessTests.test_w1_recovers_outage_and_process_restart) ... ok
test_queue_is_idempotent (test_records.WellPulseKernelTests.test_queue_is_idempotent) ... ok
test_reconciliation_detects_loss_and_duplicate (test_records.WellPulseKernelTests.test_reconciliation_detects_loss_and_duplicate) ... ok
test_record_id_is_deterministic (test_records.WellPulseKernelTests.test_record_id_is_deterministic) ... ok

----------------------------------------------------------------------
Ran 9 tests in 39.274s

OK
```
