import copy
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'validation'))
from validator import evaluate, CORE


def base():
    areas={a:{'priority':'Optional','intent':'Development'} for a in CORE}
    areas['Chest']['priority']='Standard'
    areas['Back']['priority']='Priority'
    def exercise(name,stim):
        return {'name':name,'variant':name+' machine','sets':2,'rir_targets':[1,0],
                'safe_exit':True,'stimulus':stim,'progression_rule':'Lead-Set progression',
                'rest_sec':150,'seconds_per_set':45}
    return {'goals':['General resistance-training development'],
            'human_review':{'goal_fit':True,'ps_mechanics':True,'exercise_safety':True,'recovery':True},
            'constraints':{'session_time_limit_min':60,'time_includes_warmup':False,
             'transition_min_per_exercise':1.0,'margin_min_per_session':4},
            'areas':areas,'functional_overrides':{},
            'sessions':[{'name':'A','exercises':[exercise('Press A',{'Chest':'P'}),exercise('Pull A',{'Back':'P'})]},
                        {'name':'B','exercises':[exercise('Press B',{'Chest':'P'}),exercise('Pull B',{'Back':'P'})]}]}

class ValidationTests(unittest.TestCase):
    def test_pass(self): self.assertEqual(evaluate(base())['status'],'PASS')
    def test_missing_exposure_fails(self):
        p=base(); p['sessions'][1]['exercises'][0]['stimulus']={'Chest':'S?'}
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_explicit_missing_exposure_conditional(self):
        p=base();p['sessions'][1]['exercises'][0]['stimulus']={'Chest':'S?'}
        p['areas']['Chest']['accepted_exception']='Only one feasible exposure this week'
        p['areas']['Chest']['exception_accepted_by_user']=True
        self.assertEqual(evaluate(p)['status'],'CONDITIONAL')
    def test_failure_without_escape_is_fail(self):
        p=base();p['sessions'][0]['exercises'][0]['safe_exit']=False
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_secondary_only_without_primary_is_fail(self):
        p=base()
        for s in p['sessions']:
            s['exercises'][0]['stimulus']={'Chest':'S'}
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_different_exercises_same_session_only_one_exposure(self):
        p=base();p['sessions']=p['sessions'][:1]
        p['sessions'][0]['exercises'].append(copy.deepcopy(p['sessions'][0]['exercises'][0]))
        self.assertEqual(len(evaluate(p)['ledger']['Chest']['exposures']),1)
    def test_time_overrun(self):
        p=base();p['constraints']['session_time_limit_min']=4
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_three_sets_need_reason(self):
        p=base();e=p['sessions'][0]['exercises'][0];e['sets']=3;e['rir_targets']=[1,1,0]
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_three_sets_with_reason_pass(self):
        p=base();e=p['sessions'][0]['exercises'][0];e['sets']=3;e['rir_targets']=[1,1,0];e['set_reason']='Priority work and recoverable'
        self.assertEqual(evaluate(p)['status'],'PASS')
    def test_optional_not_required(self):
        p=base();self.assertEqual(evaluate(p)['ledger']['Trunk Musculature']['P_sets'],0)
    def test_extra_area_must_be_override(self):
        p=base();p['areas']['Hip Abductors']={'priority':'Standard','intent':'Development'}
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_override_collision_fails(self):
        p=base();p['functional_overrides']['Chest']={'priority':'Standard','intent':'Development'}
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_unknown_area(self):
        p=base();p['sessions'][0]['exercises'][0]['stimulus']['Unknown muscle']='P'
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_duplicate_session_name_rejected(self):
        p=base();p['sessions'][1]['name']='A'
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_ambiguous_warmup_budget_conditional(self):
        p=base();p['constraints'].pop('time_includes_warmup')
        self.assertEqual(evaluate(p)['status'],'CONDITIONAL')
    def test_unaccepted_exception_still_fails(self):
        p=base();p['sessions'][1]['exercises'][0]['stimulus']={'Chest':'S?'}
        p['areas']['Chest']['accepted_exception']='Someone wrote this, not user approved'
        self.assertEqual(evaluate(p)['status'],'FAIL')
    def test_no_goals_causes_conditional(self):
        p=base();p.pop('goals')
        self.assertEqual(evaluate(p)['status'],'CONDITIONAL')
    def test_no_mutation(self):
        p=base(); c=copy.deepcopy(p)
        evaluate(p)
        self.assertEqual(p,c)
    def test_no_external_profile_assumptions(self):
        p=base();self.assertEqual(set(p['areas']),set(CORE))
    def test_non_object_plan_rejected(self):
        for bad in ([1], 'plan', None, 3):
            with self.assertRaises(TypeError): evaluate(bad)
    def test_non_object_constraints_or_review_rejected(self):
        for key in ('constraints','human_review'):
            p=base(); p[key]=[]
            with self.assertRaises(ValueError): evaluate(p)
    def test_cli_malformed_input_exit_code_2(self):
        import subprocess, tempfile, os
        for payload in ('[1]', '"x"', '{"constraints": []}', '{not json'):
            with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False,encoding='utf-8') as f:
                f.write(payload)
            try:
                r=subprocess.run([sys.executable,str(ROOT/'validation'/'validator.py'),f.name],
                                 capture_output=True,text=True)
            finally:
                os.unlink(f.name)
            self.assertEqual(r.returncode,2,payload)
            self.assertNotIn('Traceback',r.stderr,payload)

if __name__=='__main__': unittest.main()
