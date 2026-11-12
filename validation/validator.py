#!/usr/bin/env python3
"""HARDSET deterministic structural validator v0.1.

This is a reproducible rule-checking prototype, NOT a plan generator, medical
clearance, proof of hypertrophy, or automated exercise-biomechanics classifier.
All P/S assignments, individual risks, constraints and justifications are
provided by the human planner and require appropriate review.

Usage: python validation/validator.py examples/generic_pass.json
Stdlib only. Python 3.10+.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any

CORE = (
    'Chest', 'Lateral Delts', 'Elbow Extensors', 'Back', 'Rear Delts',
    'Elbow Flexors', 'Quadriceps', 'Hamstrings', 'Glutes',
    'Hip Adductors', 'Calves', 'Trunk Musculature'
)
PRIORITIES = {'Priority','Standard','Optional'}
INTENTS = {'Development','Maintenance'}
ALLOWED_STIMULUS = {'P','S','S?','?','-'}
PRIORITY_ORDER = {'PASS':0,'CONDITIONAL':1,'FAIL':2}


def finding(level: str, code: str, msg: str, *, scope: str = 'plan') -> dict:
    return {'level':level,'code':code,'scope':scope,'message':msg}


def _valid_num(value: Any, low: float | None = None) -> bool:
    return isinstance(value, (int,float)) and not isinstance(value,bool) and (low is None or value >= low)


def evaluate(plan: dict) -> dict:
    """Pure evaluation; never change the input, never silently infer P/S or goals."""
    issues = []
    ledger = {}
    session_estimates = {}
    profile = plan.get('constraints', {})
    area_data = plan.get('areas', {})
    sessions = plan.get('sessions', [])
    overrides = plan.get('functional_overrides', {})
    if not isinstance(plan,dict):
        raise TypeError('Plan must be a JSON object')
    if not isinstance(area_data,dict) or not isinstance(sessions,list) or not isinstance(overrides,dict):
        raise ValueError('areas and functional_overrides must be objects; sessions must be list')
    if not isinstance(plan.get('goals'),list) or not plan.get('goals'):
        issues.append(finding('CONDITIONAL','GOALS_UNSPECIFIED','Provide at least one explicit declared goal; no goal fit can be inferred.'))
    reviews = plan.get('human_review', {})
    for check in ('goal_fit', 'ps_mechanics', 'exercise_safety', 'recovery'):
        if reviews.get(check) is not True:
            issues.append(finding('CONDITIONAL','HUMAN_REVIEW_PENDING',f'Human review not attested: {check}'))
    if not sessions:
        issues.append(finding('FAIL','NO_SESSIONS','Plan has no training sessions.'))
    missing = [a for a in CORE if a not in area_data]
    if missing:
        issues.append(finding('FAIL','MISSING_CORE','Missing Fixed Core priority records: '+', '.join(missing)))
    extra=[a for a in area_data if a not in CORE]
    if extra:
        issues.append(finding('FAIL','EXTRA_FIXED_CORE','Non-core targets must be explicitly placed in functional_overrides: '+', '.join(extra)))
    overlap=set(overrides).intersection(CORE)
    if overlap:
        issues.append(finding('FAIL','OVERRIDE_COLLISION','Functional Override must not shadow Fixed Core: '+', '.join(sorted(overlap))))
    allareas = {**area_data, **overrides}
    for area,cfg in allareas.items():
        if not isinstance(cfg,dict):
            issues.append(finding('FAIL','BAD_AREA','Area configuration must be an object',scope=area)); continue
        p=cfg.get('priority')
        if p not in PRIORITIES:
            issues.append(finding('FAIL','BAD_PRIORITY',f'{area}: priority must be Priority/Standard/Optional',scope=area))
        intent=cfg.get('intent')
        if intent not in INTENTS:
            issues.append(finding('CONDITIONAL','MISSING_INTENT',f'{area}: set Training Intent Development or Maintenance',scope=area))
        ledger[area]={'priority':p,'intent':intent,'P_sets':0,'S_sets':0,'S_uncertain_sets':0,
                      'exposures':{},'functional_gap':bool(cfg.get('functional_gap',False))}
    used_session_names = set()
    if 'time_includes_warmup' not in profile:
        issues.append(finding('CONDITIONAL','WARMUP_BUDGET_UNKNOWN',
                  'Clarify whether session_time_limit_min includes warm-up.'))
    for session_index,session in enumerate(sessions):
        if not isinstance(session,dict):
            issues.append(finding('FAIL','BAD_SESSION','Session is not an object.'))
            continue
        sname=str(session.get('name') or f'Session {session_index+1}')
        if sname in used_session_names:
            issues.append(finding('FAIL','DUPLICATE_SESSION_NAME',
                  f'Duplicate session identifier {sname}; exposures cannot be distinguished.',scope=sname))
        used_session_names.add(sname)
        exercises=session.get('exercises',[])
        if not isinstance(exercises,list):
            issues.append(finding('FAIL','BAD_EXERCISES','Exercises must be a list.',scope=sname));continue
        rest=0.0
        for i,ex in enumerate(exercises):
            if not isinstance(ex,dict):
                issues.append(finding('FAIL','BAD_EXERCISE','Exercise must be object.',scope=sname));continue
            ename=str(ex.get('name') or f'Exercise {i+1}')
            scope=f'{sname} / {ename}'
            sets=ex.get('sets')
            if not isinstance(sets,int) or isinstance(sets,bool) or sets<1:
                issues.append(finding('FAIL','SETS_INVALID','Hard Sets must be a positive integer.',scope=scope)); continue
            if sets!=2 and not ex.get('set_reason'):
                issues.append(finding('FAIL','SET_JUSTIFICATION',f'{sets} Hard Sets requires explicit Purpose/Value/Recovery justification.',scope=scope))
            if sets>3:
                issues.append(finding('CONDITIONAL','UNUSUAL_SET_COUNT','More than three sets: review fatigue, purpose and workload even with justification.',scope=scope))
            if not ex.get('variant'):
                issues.append(finding('CONDITIONAL','VARIANT_MISSING','Missing equipment/variant; progression comparability may suffer.',scope=scope))
            if not ex.get('progression_rule'):
                issues.append(finding('CONDITIONAL','PROGRESSION_MISSING','No per-exercise progression rule.',scope=scope))
            rir=ex.get('rir_targets')
            if not isinstance(rir,list) or len(rir)!=sets or not all(_valid_num(x,0) for x in rir):
                issues.append(finding('FAIL','RIR_INVALID','rir_targets must contain a nonnegative value per Hard Set.',scope=scope))
            else:
                if any(x<1 for x in rir):
                    if ex.get('safe_exit') is not True:
                        issues.append(finding('FAIL','UNSAFE_FAILURE_ACCESS','0–<1 RIR requires positively verified safe set termination; no conditional waiver.',scope=scope))
            if ex.get('known_safety_blocker') is True:
                issues.append(finding('FAIL','SAFETY_BLOCKER','Known safety blocker for prescribed exercise.',scope=scope))
            if ex.get('safe_exit') is None:
                issues.append(finding('CONDITIONAL','EXIT_NOT_EVALUATED','Safe stop/exit procedure not declared.',scope=scope))
            if not isinstance(ex.get('stimulus'),dict):
                issues.append(finding('FAIL','NO_P_S','Provide explicit stimulus map; names do not establish P/S.',scope=scope));continue
            for area,tag in ex['stimulus'].items():
                if area not in ledger:
                    issues.append(finding('FAIL','UNKNOWN_AREA',f'{area} not in Fixed Core or activated Override.',scope=scope));continue
                if tag not in ALLOWED_STIMULUS:
                    issues.append(finding('FAIL','INVALID_STIMULUS',f'{area}: invalid tag {tag}',scope=scope));continue
                if tag=='P':
                    ledger[area]['P_sets']+=sets
                    ledger[area]['exposures'][sname]='P'
                elif tag=='S':
                    ledger[area]['S_sets']+=sets
                    if ledger[area]['exposures'].get(sname)!='P': ledger[area]['exposures'][sname]='S'
                elif tag in ('S?','?'):
                    ledger[area]['S_uncertain_sets']+=sets
            per_set_sec=ex.get('seconds_per_set',45)
            rest_sec=ex.get('rest_sec',120)
            if not _valid_num(per_set_sec,1) or not _valid_num(rest_sec,0):
                issues.append(finding('FAIL','TIME_INPUT_INVALID','Invalid seconds_per_set / rest_sec.',scope=scope))
            else:
                rest += (sets*per_set_sec + max(sets-1,0)*rest_sec) / 60.0
        # capacity: underestimates some logistics; time is therefore conditional near limit
        transition = profile.get('transition_min_per_exercise',1.5)
        margin = profile.get('margin_min_per_session',5)
        if not _valid_num(transition,0) or not _valid_num(margin,0):
            issues.append(finding('FAIL','TIME_CONFIGURATION','Invalid transition/margin setting.',scope=sname))
            transition=1.5; margin=5
        estimate=rest+len(exercises)*transition+margin
        if profile.get('time_includes_warmup') is True:
            warmup = profile.get('warmup_min')
            if not _valid_num(warmup,0):
                issues.append(finding('CONDITIONAL','WARMUP_UNSPECIFIED','Time includes warm-up but minutes not provided.',scope=sname))
            else:
                estimate+=warmup
        limit = profile.get('session_time_limit_min')
        session_estimates[sname] = round(estimate,2)
        if not _valid_num(limit,1):
            issues.append(finding('CONDITIONAL','TIME_LIMIT_UNKNOWN','Session capacity not specified; cannot confirm fit.',scope=sname))
        elif estimate>limit:
            issues.append(finding('FAIL','TIME_OVER',f'Estimated {estimate:.1f} min exceeds {limit:.1f}-min limit.',scope=sname))
        elif estimate>limit*0.9:
            issues.append(finding('CONDITIONAL','TIME_TIGHT',f'Estimated {estimate:.1f}/{limit:.1f} min; real-world delays could exceed limit.',scope=sname))
    for area, entry in ledger.items():
        p=entry['priority']
        exposure=list(entry['exposures'].values())
        if p not in ('Priority','Standard'): continue
        # accepted exception must be explicit, never silently inferred
        exc=allareas[area].get('accepted_exception') if isinstance(allareas[area],dict) else None
        if len(exposure)<2:
            if isinstance(exc,str) and exc.strip() and allareas[area].get('exception_accepted_by_user') is True:
                issues.append(finding('CONDITIONAL','EXPOSURE_EXCEPTION',f'{area}: {len(exposure)} credible exposures; documented exception: {exc}',scope=area))
            else:
                issues.append(finding('FAIL','TOO_FEW_EXPOSURES',f'{area}: {len(exposure)} credible exposures; default is two.',scope=area))
        elif 'P' not in exposure:
            if isinstance(exc,str) and exc.strip() and allareas[area].get('exception_accepted_by_user') is True:
                issues.append(finding('CONDITIONAL','S_ONLY_EXCEPTION',f'{area}: S+S not automatically sufficient; accepted exception: {exc}',scope=area))
            else:
                issues.append(finding('FAIL','SECONDARY_ONLY',f'{area}: S+S lacks a Primary exposure.',scope=area))
        elif entry['functional_gap']:
            if isinstance(exc,str) and exc.strip() and allareas[area].get('exception_accepted_by_user') is True:
                issues.append(finding('CONDITIONAL','FUNCTIONAL_GAP_EXCEPTION',f'{area}: known functional gap; accepted: {exc}',scope=area))
            else:
                issues.append(finding('FAIL','FUNCTIONAL_GAP',f'{area}: marked functional gap unresolved.',scope=area))
    severity='PASS'
    for item in issues:
        if PRIORITY_ORDER[item['level']]>PRIORITY_ORDER[severity]: severity=item['level']
    return {'status':severity,'summary':{'sessions':len(sessions), 'total_hard_sets':sum(
        int(ex.get('sets',0)) for s in sessions if isinstance(s,dict)
        for ex in s.get('exercises',[]) if isinstance(ex,dict) and isinstance(ex.get('sets'),int))},
        'ledger':ledger,'session_time_estimates_min':session_estimates,'findings':issues, 'disclaimer': 'Structural checks only; no medical clearance, P/S biomechanics inference, or prediction of hypertrophy.'}


def main() -> int:
    if len(sys.argv)!=2:
        print('Usage: python validation/validator.py path/to/plan.json',file=sys.stderr)
        return 2
    try:
        plan=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
        result=evaluate(plan)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result['status']=='PASS' else (1 if result['status']=='CONDITIONAL' else 2)
    except (OSError, ValueError, TypeError) as error:
        print(f'Cannot validate: {error}',file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
