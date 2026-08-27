import unittest

from wellpulse.horizon import (
    H_APP_S,
    ceil_to_30s,
    compute_recovery_horizon,
    frozen_application_horizon_s,
    nearest_rank_percentile,
)


class RecoveryHorizonTests(unittest.TestCase):
    def test_application_horizon_is_prospectively_frozen_at_300_seconds(self):
        self.assertEqual(H_APP_S, 300)
        self.assertEqual(frozen_application_horizon_s(), 300)

    def test_outcome_derived_h_calculation_is_fail_closed(self):
        with self.assertRaisesRegex(RuntimeError, "superseded"):
            compute_recovery_horizon([10.0, 20.0, 30.0])
        with self.assertRaisesRegex(RuntimeError, "H_app=300s"):
            compute_recovery_horizon([120.0, 149.0, 150.0])

    def test_historical_math_helpers_do_not_define_current_horizon(self):
        self.assertEqual(nearest_rank_percentile([12.0, 18.5, 15.0], 0.95), 18.5)
        self.assertEqual(ceil_to_30s(121), 150)
        self.assertEqual(frozen_application_horizon_s(), 300)

    def test_invalid_historical_helper_values_rejected(self):
        with self.assertRaises(ValueError):
            nearest_rank_percentile([], 0.95)
        with self.assertRaises(ValueError):
            ceil_to_30s(-1)


if __name__ == "__main__":
    unittest.main()
