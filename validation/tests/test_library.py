"""Structural checks for the exercise library used by the plan builder."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'validation'))
sys.path.insert(0, str(ROOT / 'tools' / 'builder'))
from validator import CORE, ALLOWED_STIMULUS  # noqa: E402
import build_library_review  # noqa: E402

KNOWN_OVERRIDES = {'Hip Abduction'}
DATA = json.loads((ROOT / 'library' / 'exercises.json').read_text(encoding='utf-8'))
EX = DATA['exercises']


class LibraryTests(unittest.TestCase):
    def test_ids_unique(self):
        ids = [e['id'] for e in EX]
        self.assertEqual(len(ids), len(set(ids)))

    def test_stimulus_areas_and_tags(self):
        for e in EX:
            self.assertTrue(e['stimulus'], e['id'])
            for area, tag in e['stimulus'].items():
                self.assertTrue(area in CORE or area in KNOWN_OVERRIDES, (e['id'], area))
                self.assertIn(tag, ALLOWED_STIMULUS, e['id'])

    def test_safe_exit_consistency(self):
        for e in EX:
            self.assertIn(e['safe_exit'], (True, False, 'conditional'), e['id'])
            if e['safe_exit'] == 'conditional':
                self.assertTrue(e['safe_exit_condition'].strip(), e['id'])
            if e['safe_exit'] is False:
                self.assertGreaterEqual(e['rir_floor_default'], 1, e['id'])

    def test_defaults_valid(self):
        for e in EX:
            self.assertRegex(e['rep_template'], r'^\d+-\d+$', e['id'])
            lo, hi = map(int, e['rep_template'].split('-'))
            self.assertLess(lo, hi, e['id'])
            self.assertGreaterEqual(e['rest_sec'], 0, e['id'])
            self.assertGreater(e['seconds_per_set'], 0, e['id'])
            self.assertIn(e['family'], ('Compound Pattern', 'Targeted Function'), e['id'])
            self.assertIn(e['review']['status'], ('proposed', 'approved', 'rejected'), e['id'])

    def test_review_file_in_sync(self):
        text = build_library_review.render(DATA)
        self.assertEqual((ROOT / 'library' / 'REVIEW.md').read_text(encoding='utf-8'), text,
                         'Run tools/builder/build_library_review.py')


if __name__ == '__main__':
    unittest.main()
