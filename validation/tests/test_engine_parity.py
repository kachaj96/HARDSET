"""Parity: the JavaScript engine (tools/builder/engine.js) must match validation/validator.py.

Runs every case through both implementations and compares status, findings,
ledger, summary and time estimates. Skipped when Node.js is not installed.
"""
import copy
import json
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'validation'))
sys.path.insert(0, str(ROOT / 'validation' / 'tests'))
from validator import evaluate  # noqa: E402
from test_validator import base  # noqa: E402

NODE = shutil.which('node')
RUNNER = """
const {evaluate}=require(process.argv[2]);
const cases=JSON.parse(require('fs').readFileSync(0,'utf8'));
console.log(JSON.stringify(cases.map(c=>{try{return {ok:evaluate(c)}}catch(e){return {error:true}}})));
"""


def named_cases():
    def m(fn):
        p = base(); fn(p); return p
    c = {'base': base()}
    c['s_question'] = m(lambda p: p['sessions'][1]['exercises'][0].__setitem__('stimulus', {'Chest': 'S?'}))
    c['accepted_exception'] = m(lambda p: (p['sessions'][1]['exercises'][0].__setitem__('stimulus', {'Chest': 'S?'}),
                                           p['areas']['Chest'].update(accepted_exception='time', exception_accepted_by_user=True)))
    c['unaccepted_exception'] = m(lambda p: (p['sessions'][1]['exercises'][0].__setitem__('stimulus', {'Chest': 'S?'}),
                                             p['areas']['Chest'].update(accepted_exception='time')))
    c['unsafe_failure'] = m(lambda p: p['sessions'][0]['exercises'][0].__setitem__('safe_exit', False))
    c['s_plus_s'] = m(lambda p: [e.__setitem__('stimulus', {'Chest': 'S'}) for s in p['sessions'] for e in s['exercises'][:1]])
    c['two_in_one_session'] = m(lambda p: p['sessions'][0]['exercises'].append(copy.deepcopy(p['sessions'][0]['exercises'][0])))
    c['time_over'] = m(lambda p: p['constraints'].__setitem__('session_time_limit_min', 5))
    c['time_tight'] = m(lambda p: p['constraints'].__setitem__('session_time_limit_min', 15.5))
    c['three_sets_no_reason'] = m(lambda p: p['sessions'][0]['exercises'][0].update(sets=3, rir_targets=[1, 1, 0]))
    c['three_sets_reason'] = m(lambda p: p['sessions'][0]['exercises'][0].update(sets=3, rir_targets=[1, 1, 0], set_reason='x'))
    c['four_sets'] = m(lambda p: p['sessions'][0]['exercises'][0].update(sets=4, rir_targets=[1, 1, 1, 0], set_reason='x'))
    c['unknown_area'] = m(lambda p: p['sessions'][0]['exercises'][0]['stimulus'].__setitem__('Forearms', 'P'))
    c['extra_area'] = m(lambda p: p['areas'].__setitem__('Forearms', {'priority': 'Optional', 'intent': 'Development'}))
    c['override_ok'] = m(lambda p: (p['functional_overrides'].__setitem__('Hip Abduction', {'priority': 'Standard', 'intent': 'Development'}),
                                    p['sessions'][0]['exercises'][0]['stimulus'].__setitem__('Hip Abduction', 'P')))
    c['override_collision'] = m(lambda p: p['functional_overrides'].__setitem__('Chest', {'priority': 'Standard', 'intent': 'Development'}))
    c['duplicate_session'] = m(lambda p: p['sessions'][1].__setitem__('name', 'A'))
    c['no_warmup_flag'] = m(lambda p: p['constraints'].pop('time_includes_warmup'))
    c['warmup_included'] = m(lambda p: p['constraints'].update(time_includes_warmup=True, warmup_min=10))
    c['warmup_missing_min'] = m(lambda p: p['constraints'].update(time_includes_warmup=True))
    c['no_goals'] = m(lambda p: p.pop('goals'))
    c['no_review'] = m(lambda p: p.pop('human_review'))
    c['no_sessions'] = m(lambda p: p.__setitem__('sessions', []))
    c['missing_core'] = m(lambda p: p['areas'].pop('Calves'))
    c['bad_priority'] = m(lambda p: p['areas']['Chest'].__setitem__('priority', 'High'))
    c['missing_intent'] = m(lambda p: p['areas']['Back'].pop('intent'))
    c['functional_gap'] = m(lambda p: p['areas']['Back'].__setitem__('functional_gap', True))
    c['invalid_tag'] = m(lambda p: p['sessions'][0]['exercises'][0]['stimulus'].__setitem__('Chest', 'X'))
    c['rir_wrong_len'] = m(lambda p: p['sessions'][0]['exercises'][0].__setitem__('rir_targets', [1]))
    c['no_variant'] = m(lambda p: p['sessions'][0]['exercises'][0].pop('variant'))
    c['no_progression'] = m(lambda p: p['sessions'][0]['exercises'][0].pop('progression_rule'))
    c['exit_unknown'] = m(lambda p: p['sessions'][0]['exercises'][1].update(safe_exit=None, rir_targets=[1, 1]))
    c['safety_blocker'] = m(lambda p: p['sessions'][0]['exercises'][0].__setitem__('known_safety_blocker', True))
    c['bad_time_input'] = m(lambda p: p['sessions'][0]['exercises'][0].__setitem__('rest_sec', -1))
    c['bad_transition'] = m(lambda p: p['constraints'].__setitem__('transition_min_per_exercise', -1))
    c['no_limit'] = m(lambda p: p['constraints'].pop('session_time_limit_min'))
    c['unnamed'] = m(lambda p: [s.pop('name') for s in p['sessions']])
    c['bad_session'] = m(lambda p: p['sessions'].append('X'))
    c['bad_exercises'] = m(lambda p: p['sessions'][0].__setitem__('exercises', 'abc'))
    c['bad_exercise'] = m(lambda p: p['sessions'][0]['exercises'].append(7))
    c['no_stimulus'] = m(lambda p: p['sessions'][0]['exercises'][0].pop('stimulus'))
    c['zero_sets'] = m(lambda p: p['sessions'][0]['exercises'][0].__setitem__('sets', 0))
    for f in sorted((ROOT / 'examples').glob('*.json')):
        c['example_' + f.stem] = json.loads(f.read_text(encoding='utf-8'))
    for bad in ([1], 'x', None, {'constraints': []}, {'areas': []}):
        c['malformed_' + repr(bad)] = bad
    return c


def fuzz_cases(n=300, seed=20261112):
    rnd = random.Random(seed)
    areas = list(base()['areas'])
    out = []
    for _ in range(n):
        p = base()
        for s in p['sessions']:
            for e in s['exercises']:
                e['sets'] = rnd.choice([1, 2, 2, 2, 3, 4])
                if e['sets'] != 2 and rnd.random() < 0.6:
                    e['set_reason'] = 'r'
                e['rir_targets'] = [rnd.choice([0, 0.5, 1, 1.5, 2, 3]) for _ in range(e['sets'] if rnd.random() < 0.9 else 1)]
                e['safe_exit'] = rnd.choice([True, True, False, None])
                e['stimulus'] = {a: rnd.choice(['P', 'S', 'S?', '-']) for a in rnd.sample(areas, rnd.randint(1, 3))}
                e['rest_sec'] = rnd.choice([60, 75, 90, 105, 120, 150, 180, 240])
                e['seconds_per_set'] = rnd.choice([30, 35, 40, 45, 50, 90, 100])
            for _ in range(rnd.randint(0, 4)):
                s['exercises'].append(copy.deepcopy(rnd.choice(s['exercises'])))
        for a in areas:
            p['areas'][a]['priority'] = rnd.choice(['Priority', 'Standard', 'Optional'])
            if rnd.random() < 0.1:
                p['areas'][a].update(accepted_exception='e', exception_accepted_by_user=rnd.random() < 0.5)
        p['constraints']['session_time_limit_min'] = rnd.choice([10, 15, 20, 30, 45, 60])
        p['constraints']['transition_min_per_exercise'] = rnd.choice([1, 1.5, 2])
        if rnd.random() < 0.3:
            p['constraints'].update(time_includes_warmup=True, warmup_min=rnd.choice([5, 7.5, 10]))
        out.append(p)
    return out


def py_eval(plan):
    try:
        return {'ok': evaluate(copy.deepcopy(plan))}
    except Exception:
        return {'error': True}


@unittest.skipUnless(NODE, 'Node.js not installed')
class EngineParityTests(unittest.TestCase):
    def run_js(self, cases):
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(RUNNER)
        try:
            r = subprocess.run([NODE, f.name, str(ROOT / 'tools' / 'builder' / 'engine.js')],
                               input=json.dumps(cases), capture_output=True, text=True, check=True)
        finally:
            Path(f.name).unlink()
        return json.loads(r.stdout)

    def compare(self, names, cases):
        js = self.run_js(cases)
        for name, case, j in zip(names, cases, js):
            with self.subTest(case=name):
                self.assertEqual(py_eval(case), json.loads(json.dumps(j)))

    def test_named_cases(self):
        c = named_cases()
        self.compare(list(c), list(c.values()))

    def test_fuzz_cases(self):
        cases = fuzz_cases()
        self.compare([f'fuzz_{i}' for i in range(len(cases))], cases)

    def test_cli_exit_codes(self):
        for name, code in (('generic_pass', 0), ('generic_conditional', 1), ('generic_fail', 2)):
            r = subprocess.run([NODE, str(ROOT / 'tools' / 'builder' / 'engine_cli.js'), str(ROOT / 'examples' / f'{name}.json')],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, code, name)


if __name__ == '__main__':
    unittest.main()
