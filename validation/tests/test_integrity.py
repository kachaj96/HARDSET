"""Documentation inventory and reference integrity checks; no network calls."""
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class DocumentIntegrityTests(unittest.TestCase):
    def test_nine_chapters(self):
        self.assertEqual(len(list((ROOT/'chapters').glob('[0-9][0-9]_*.md'))),9)
    def test_master_includes_nine(self):
        text=(ROOT/'HARDSET_MASTER.md').read_text(encoding='utf-8')
        self.assertEqual(len(re.findall(r'^# HARDSET — Chapter 0[1-9]:',text,re.M)),9)
    def test_all_cited_reference_ids_exist(self):
        text='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'chapters').glob('*.md'))
        cited=set(re.findall(r'\bR\d{2}\b',text))
        actual={d['id'] for d in json.loads((ROOT/'research/references.json').read_text(encoding='utf-8'))}
        self.assertFalse(cited-actual, f'Unknown references: {cited-actual}')
        self.assertEqual(len(actual),30)
    def test_retracted_source_not_in_active_bibliography(self):
        refs=json.loads((ROOT/'research/references.json').read_text(encoding='utf-8'))
        self.assertFalse(any('0000000000003865' in d['doi'] for d in refs))
    def test_evidence_rows_and_types(self):
        import csv
        with (ROOT/'research/evidence_matrix.csv').open(encoding='utf-8',newline='') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),38)
        for d in rows:
            self.assertIn(d['classification'],{'SCIENTIFIC_EVIDENCE','HARDSET_DESIGN_DECISION',
                    'IMPLEMENTATION_HEURISTIC','PRACTICAL_SAFETY_RULE',
                    'PRACTICAL_MEASUREMENT','NOT_SUPPORTED'})
    def test_no_embedded_contact_info(self):
        # Personal-data checks should be run externally, without placing any real
        # user identifiers or workout records into the distributable project.
        text=(ROOT/'HARDSET_MASTER.md').read_text(encoding='utf-8')
        self.assertNotRegex(text, r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b')
        self.assertNotIn('## PERSONAL TRAINING PROFILE', text)

if __name__=='__main__':unittest.main()
