import unittest

from wellpulse.horizon import ceil_to_30s, compute_recovery_horizon, nearest_rank_percentile


class RecoveryHorizonTests(unittest.TestCase):
    def test_nearest_rank_p95_for_three_trials_is_maximum(self):
        self.assertEqual(nearest_rank_percentile([12.0, 18.5, 15.0], 0.95), 18.5)

    def test_protocol_minimum_horizon_is_120_seconds(self):
        result = compute_recovery_horizon([10.0, 20.0, 30.0])
        self.assertEqual(result.p95_drain_s, 30.0)
        self.assertEqual(result.recovery_horizon_s, 120)
        self.assertFalse(result.stop_and_investigate)

    def test_horizon_rounds_twice_p95_up_to_30_seconds(self):
        result = compute_recovery_horizon([40.0, 61.0, 55.0])
        self.assertEqual(result.p95_drain_s, 61.0)
        self.assertEqual(result.recovery_horizon_s, 150)
        self.assertFalse(result.stop_and_investigate)

    def test_exact_150_second_drain_yields_300_second_horizon(self):
        result = compute_recovery_horizon([120.0, 149.0, 150.0])
        self.assertEqual(result.recovery_horizon_s, 300)
        self.assertFalse(result.stop_and_investigate)

    def test_over_150_second_drain_forces_stop_not_cap(self):
        result = compute_recovery_horizon([120.0, 150.1, 130.0])
        self.assertEqual(result.recovery_horizon_s, 330)
        self.assertTrue(result.stop_and_investigate)

    def test_ceil_to_30(self):
        self.assertEqual(ceil_to_30s(120), 120)
        self.assertEqual(ceil_to_30s(121), 150)

    def test_invalid_values_rejected(self):
        with self.assertRaises(ValueError):
            compute_recovery_horizon([])
        with self.assertRaises(ValueError):
            compute_recovery_horizon([1, -1, 2])


if __name__ == "__main__":
    unittest.main()
