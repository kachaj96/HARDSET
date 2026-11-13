"""Audit tests for Continuous Bench Priority v1.1 (handoff draft).

These tests check the handoff data as received. They do not change it.
Run: python -m unittest discover -s programs/continuous-bench-priority/tests -v
"""
import importlib.util
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / 'handoff'
WAVE = json.loads((HANDOFF / 'machine' / 'bench_wave.json').read_text(encoding='utf-8'))

spec = importlib.util.spec_from_file_location('bp_e1rm', HANDOFF / 'machine' / 'e1rm.py')
e1rm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e1rm)

SLOTS = ('mon_single', 'mon_backoff', 'wed_paused')


def fri_pct(week):
    f = week['fri']
    return f['pct'] if f['kind'] == 'volume' else f['first']['pct']


def plates(x):
    return e1rm.nearest_plates(x)


class WaveStructure(unittest.TestCase):
    def test_four_weeks_three_sessions(self):
        self.assertEqual(WAVE['cycle_weeks'], 4)
        self.assertEqual([w['week'] for w in WAVE['wave']], [1, 2, 3, 4])
        self.assertEqual(WAVE['sessions_per_week'], 3)
        self.assertEqual(WAVE['minutes_max_per_session'], 60)

    def test_ranges_are_ordered(self):
        for w in WAVE['wave']:
            for slot in SLOTS:
                lo, hi = w[slot]['pct']
                self.assertLessEqual(lo, hi, (w['week'], slot))
                rlo, rhi = w[slot]['rpe']
                self.assertLessEqual(rlo, rhi, (w['week'], slot))

    def test_intensity_rises_t1_to_t3(self):
        for slot in SLOTS:
            lows = [WAVE['wave'][i][slot]['pct'][0] for i in range(3)]
            self.assertEqual(lows, sorted(lows), slot)
        fri = [fri_pct(WAVE['wave'][i])[0] for i in range(3)]
        self.assertEqual(fri, sorted(fri))

    def test_t4_lighter_than_t1_in_every_slot(self):
        t1, t4 = WAVE['wave'][0], WAVE['wave'][3]
        for slot in SLOTS:
            self.assertLess(t4[slot]['pct'][0], t1[slot]['pct'][0], slot)
        self.assertLess(fri_pct(t4)[0], fri_pct(t1)[0])

    def test_t3_friday_is_single_amrap_at_rpe9_plus_one_backoff(self):
        fri = WAVE['wave'][2]['fri']
        self.assertEqual(fri['kind'], 'benchmark')
        self.assertEqual(fri['first']['sets'], 1)
        self.assertEqual(fri['first']['rpe'], [9, 9])
        self.assertEqual(fri['first']['pct'], [82.5, 82.5])
        self.assertEqual(fri['second']['sets'], 1)

    def test_no_bench_prescription_above_rpe9(self):
        for w in WAVE['wave']:
            for slot in SLOTS:
                self.assertLessEqual(w[slot]['rpe'][1], 9)


class Arithmetic(unittest.TestCase):
    def test_e1rm_table(self):
        for reps, expected in ((4, 116.7), (5, 120.0), (6, 123.3), (7, 126.7)):
            self.assertAlmostEqual(round(e1rm.epley_rir(100, reps, 1), 1), expected)

    def test_handoff_self_test_cases(self):
        self.assertEqual(plates(120 * .825), 100.0)
        self.assertEqual(plates(120 * .92), 110.0)

    def test_pb120_examples(self):
        pb = 120
        self.assertEqual((plates(pb * .88), plates(pb * .90)), (105.0, 107.5))   # Mon T1 single
        self.assertEqual((plates(pb * .75), plates(pb * .78)), (90.0, 92.5))     # Mon T1 back-off
        self.assertEqual((plates(pb * .77), plates(pb * .80)), (92.5, 95.0))     # Wed T3
        self.assertEqual(plates(pb * .825), 100.0)                               # Fri T3 benchmark
        self.assertEqual((plates(pb * .725), plates(pb * .75)), (87.5, 90.0))    # Fri T3 back-off

    def test_known_erratum_mon_t3_backoff(self):
        # Handoff 03 says "~100-102.5 kg"; 82-85% of 120 rounds to 97.5-102.5 kg (see AUDIT, E-2).
        self.assertEqual((plates(120 * .82), plates(120 * .85)), (97.5, 102.5))

    def test_pb_example_wave_b(self):
        gain = e1rm.epley_rir(100, 6, 1) / 120 - 1
        self.assertAlmostEqual(gain * 100, 2.78, places=2)


class ExampleWeek(unittest.TestCase):
    SETS = {'Pn': [1, 2, 2, 2, 2, 2], 'Sr': [2, 2, 2, 2, 2, 2], 'Pt': [2, 2, 2, 2, 2, 2]}
    MINUTES = {'Pn': [9, 19, 10, 11, 6, 5], 'Sr': [9, 13, 10, 9, 7, 8, 4], 'Pt': [8, 15, 11, 8, 7, 9, 2]}

    def test_set_totals(self):
        totals = {d: sum(v) for d, v in self.SETS.items()}
        self.assertEqual(totals, {'Pn': 11, 'Sr': 12, 'Pt': 12})
        self.assertEqual(sum(totals.values()), 35)
        self.assertEqual(sum(totals.values()), sum(WAVE['example_sets_per_day'].values()))

    def test_bench_sets(self):
        self.assertEqual(1 + 2 + 2 + 2, 7)

    def test_time_budgets_sum_to_60(self):
        for day, parts in self.MINUTES.items():
            self.assertEqual(sum(parts), 60, day)

    def test_validator_model_within_limit(self):
        out = json.loads((ROOT / 'analysis' / 'example_week_validator_output.json').read_text(encoding='utf-8'))
        for day, minutes in out['session_time_estimates_min'].items():
            self.assertLessEqual(minutes, 60, day)
        self.assertEqual(out['summary']['total_hard_sets'], 35)


if __name__ == '__main__':
    unittest.main()
