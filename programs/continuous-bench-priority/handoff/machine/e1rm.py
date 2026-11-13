#!/usr/bin/env python3
"""Pomocniczy model e1RM. Educational heuristic, not a validated test of true 1RM."""
from __future__ import annotations
import argparse
import math
import unittest


def epley_rir(load: float, reps: int, rir: float = 1) -> float:
    if not math.isfinite(load) or load <= 0:
        raise ValueError("load must be positive and finite")
    if not isinstance(reps, int) or not 1 <= reps <= 20:
        raise ValueError("reps must be integer 1..20")
    if not math.isfinite(rir) or not 0 <= rir <= 4:
        raise ValueError("RIR must be between 0 and 4")
    return load * (1 + (reps + rir) / 30)


def nearest_plates(load: float, increment: float = 2.5) -> float:
    if increment <= 0 or not math.isfinite(increment):
        raise ValueError("increment must be positive")
    return math.floor(load / increment + 0.5) * increment


class ModelTests(unittest.TestCase):
    def test_benchmark_examples(self):
        expected = [(4, 116.6666666667), (5, 120), (6, 123.3333333333), (7, 126.6666666667)]
        for reps, result in expected:
            self.assertAlmostEqual(epley_rir(100, reps, 1), result, places=6)

    def test_rounding(self):
        self.assertEqual(nearest_plates(120*.825), 100.0)
        self.assertEqual(nearest_plates(120*.92), 110.0)

    def test_invalid(self):
        for args in [(0, 5, 1), (100, 0, 1), (100, 21, 1), (100, 5, -1)]:
            with self.assertRaises(ValueError): epley_rir(*args)


def main():
    parser = argparse.ArgumentParser(description="Heuristic AMRAP e1RM calculator")
    parser.add_argument('--load', type=float)
    parser.add_argument('--reps', type=int)
    parser.add_argument('--rir', type=float, default=1)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=['e1rm.py'], exit=False)
        return
    if args.load is None or args.reps is None:
        parser.error('Provide --load and --reps, or --self-test')
    print(f'e1RM (orientacyjny): {epley_rir(args.load, args.reps, args.rir):.1f} kg')


if __name__ == '__main__': main()
