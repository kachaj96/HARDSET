"""Tests for the v1.2 amendments (D-3 upward correction, D-4 repetition-based base rule)."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('rules_v1_2', ROOT / 'rules_v1_2.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class UpwardCorrection(unittest.TestCase):
    def test_one_point_gap_adds_one_step_at_100kg(self):
        self.assertEqual(r.upward_correction(100, 7, 6), 102.5)

    def test_two_point_gap_is_capped_at_5_percent(self):
        self.assertEqual(r.upward_correction(100, 7, 5), 105)
        self.assertEqual(r.upward_correction(100, 7, 3), 105)   # cap, not 15%

    def test_half_point_gap_does_nothing(self):
        self.assertEqual(r.upward_correction(100, 7, 6.5), 100)

    def test_no_correction_for_single_amrap_week4_or_bad_technique(self):
        self.assertEqual(r.upward_correction(100, 7, 5, multi_rep=False), 100)
        self.assertEqual(r.upward_correction(100, 7, 5, week=4), 100)
        self.assertEqual(r.upward_correction(100, 7, 5, technique_ok=False), 100)

    def test_light_loads_still_move_by_a_plate(self):
        self.assertEqual(r.upward_correction(60, 7, 6), 62.5)
        self.assertEqual(r.upward_correction(60, 7, 6, plate=1.25), 61.25)

    def test_step_per_point_is_below_epley_estimate_for_wave_rep_ranges(self):
        # reps 3-6, target RPE 6-8 (RIR 4-2): Epley says one RPE point is 2.6-2.9% of load.
        for reps in range(3, 7):
            for rir in (2, 3, 4):
                est = r.epley_pct_per_rpe_point(reps, rir)
                self.assertGreater(est, r.UP_PCT_PER_RPE_POINT, (reps, rir))
                self.assertLess(est, 3.0, (reps, rir))


class BaseDecision(unittest.TestCase):
    A = dict(load=100, reps=5, rir=1)
    B = dict(load=100, reps=6, rir=1)

    def test_handoff_example_wave_b_raises_when_single_confirms(self):
        self.assertEqual(r.base_decision(self.A, self.B, single_ok=True), 'raise')

    def test_same_without_single_confirmation_holds(self):
        self.assertEqual(r.base_decision(self.A, self.B, single_ok=False), 'hold_unconfirmed')

    def test_unchanged_result_holds(self):
        self.assertEqual(r.base_decision(self.A, self.A, single_ok=True), 'hold')

    def test_one_rep_fewer_points_to_recovery_check(self):
        self.assertEqual(r.base_decision(self.B, self.A, single_ok=True), 'check_recovery')

    def test_load_change_between_waves_uses_e1rm(self):
        # base +2.5 kg moved the control load from 100 to 102 kg; same reps and RIR must not trigger a raise
        prev = dict(load=100, reps=6, rir=1)
        cur = dict(load=102, reps=6, rir=1)
        self.assertEqual(r.base_decision(prev, cur, single_ok=True), 'hold')

    def test_first_wave_has_no_reference(self):
        self.assertEqual(r.base_decision(None, self.A, single_ok=True), 'inconclusive')

    def test_not_comparable_is_inconclusive(self):
        self.assertEqual(r.base_decision(self.A, self.B, single_ok=True, comparable=False), 'inconclusive')


if __name__ == '__main__':
    unittest.main()
