/* HARDSET rule engine (JavaScript port of validation/validator.py).
 *
 * evaluate(plan) must produce the same status, findings, ledger and time
 * estimates as the Python validator for the same input. This is enforced by
 * validation/tests/test_engine_parity.py. Change both implementations together.
 *
 * Structural checks only: no P/S inference from names, no medical clearance,
 * no prediction of hypertrophy. Works in browsers (window.HardsetEngine) and Node.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.HardsetEngine = api;
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const CORE = ['Chest', 'Lateral Delts', 'Elbow Extensors', 'Back', 'Rear Delts',
    'Elbow Flexors', 'Quadriceps', 'Hamstrings', 'Glutes',
    'Hip Adductors', 'Calves', 'Trunk Musculature'];
  const PRIORITIES = new Set(['Priority', 'Standard', 'Optional']);
  const INTENTS = new Set(['Development', 'Maintenance']);
  const ALLOWED_STIMULUS = new Set(['P', 'S', 'S?', '?', '-']);
  const PRIORITY_ORDER = { PASS: 0, CONDITIONAL: 1, FAIL: 2 };
  const DISCLAIMER = 'Structural checks only; no medical clearance, P/S biomechanics inference, or prediction of hypertrophy.';

  /* ---- Python-compatible helpers ---- */
  const isDict = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
  const has = (o, k) => Object.prototype.hasOwnProperty.call(o, k);
  const get = (o, k, d) => (has(o, k) ? o[k] : d);
  function pyFalsy(v) {
    if (v === null || v === undefined || v === false || v === 0 || v === '') return true;
    if (Array.isArray(v)) return v.length === 0;
    if (isDict(v)) return Object.keys(v).length === 0;
    return false;
  }
  const pyNum = (v) => typeof v === 'number' || typeof v === 'boolean';      // isinstance(v,(int,float))
  const pyInt = (v) => (typeof v === 'number' && Number.isInteger(v)) || typeof v === 'boolean'; // isinstance(v,int)
  function validNum(v, low) {
    return typeof v === 'number' && Number.isFinite(v) && (low === undefined || v >= low);
  }
  function pyStr(v) {
    if (v === null || v === undefined) return 'None';
    if (v === true) return 'True';
    if (v === false) return 'False';
    return String(v);
  }
  function pyRound(x, nd) {
    const m = Math.pow(10, nd); const y = x * m; const f = Math.floor(y);
    const r = (y - f === 0.5) ? (f % 2 === 0 ? f : f + 1) : Math.round(y);
    return r / m;
  }
  const fmt1 = (x) => pyRound(x, 1).toFixed(1);

  function finding(level, code, msg, scope) {
    return { level, code, scope: scope === undefined ? 'plan' : scope, message: msg };
  }

  function evaluate(plan) {
    const issues = [];
    const ledger = {};
    const sessionEstimates = {};
    if (!isDict(plan)) throw new TypeError('Plan must be a JSON object');
    const profile = get(plan, 'constraints', {});
    const areaData = get(plan, 'areas', {});
    const sessions = get(plan, 'sessions', []);
    const overrides = get(plan, 'functional_overrides', {});
    if (!isDict(areaData) || !Array.isArray(sessions) || !isDict(overrides))
      throw new RangeError('areas and functional_overrides must be objects; sessions must be list');
    if (!isDict(profile) || !isDict(get(plan, 'human_review', {})))
      throw new RangeError('constraints and human_review must be objects');
    if (!Array.isArray(get(plan, 'goals')) || pyFalsy(get(plan, 'goals')))
      issues.push(finding('CONDITIONAL', 'GOALS_UNSPECIFIED', 'Provide at least one explicit declared goal; no goal fit can be inferred.'));
    const reviews = get(plan, 'human_review', {});
    for (const check of ['goal_fit', 'ps_mechanics', 'exercise_safety', 'recovery'])
      if (get(reviews, check) !== true)
        issues.push(finding('CONDITIONAL', 'HUMAN_REVIEW_PENDING', `Human review not attested: ${check}`));
    if (sessions.length === 0) issues.push(finding('FAIL', 'NO_SESSIONS', 'Plan has no training sessions.'));
    const missing = CORE.filter((a) => !has(areaData, a));
    if (missing.length) issues.push(finding('FAIL', 'MISSING_CORE', 'Missing Fixed Core priority records: ' + missing.join(', ')));
    const extra = Object.keys(areaData).filter((a) => !CORE.includes(a));
    if (extra.length) issues.push(finding('FAIL', 'EXTRA_FIXED_CORE', 'Non-core targets must be explicitly placed in functional_overrides: ' + extra.join(', ')));
    const overlap = Object.keys(overrides).filter((a) => CORE.includes(a)).sort();
    if (overlap.length) issues.push(finding('FAIL', 'OVERRIDE_COLLISION', 'Functional Override must not shadow Fixed Core: ' + overlap.join(', ')));
    const allareas = Object.assign({}, areaData, overrides);
    for (const area of Object.keys(allareas)) {
      const cfg = allareas[area];
      if (!isDict(cfg)) { issues.push(finding('FAIL', 'BAD_AREA', 'Area configuration must be an object', area)); continue; }
      const p = get(cfg, 'priority', null);
      if (!PRIORITIES.has(p)) issues.push(finding('FAIL', 'BAD_PRIORITY', `${area}: priority must be Priority/Standard/Optional`, area));
      const intent = get(cfg, 'intent', null);
      if (!INTENTS.has(intent)) issues.push(finding('CONDITIONAL', 'MISSING_INTENT', `${area}: set Training Intent Development or Maintenance`, area));
      ledger[area] = { priority: p, intent, P_sets: 0, S_sets: 0, S_uncertain_sets: 0,
        exposures: {}, functional_gap: !pyFalsy(get(cfg, 'functional_gap', false)) };
    }
    const usedNames = new Set();
    if (!has(profile, 'time_includes_warmup'))
      issues.push(finding('CONDITIONAL', 'WARMUP_BUDGET_UNKNOWN', 'Clarify whether session_time_limit_min includes warm-up.'));
    sessions.forEach((session, si) => {
      if (!isDict(session)) { issues.push(finding('FAIL', 'BAD_SESSION', 'Session is not an object.')); return; }
      const rawName = get(session, 'name', null);
      const sname = pyStr(pyFalsy(rawName) ? `Session ${si + 1}` : rawName);
      if (usedNames.has(sname))
        issues.push(finding('FAIL', 'DUPLICATE_SESSION_NAME', `Duplicate session identifier ${sname}; exposures cannot be distinguished.`, sname));
      usedNames.add(sname);
      const exercises = get(session, 'exercises', []);
      if (!Array.isArray(exercises)) { issues.push(finding('FAIL', 'BAD_EXERCISES', 'Exercises must be a list.', sname)); return; }
      let rest = 0.0;
      exercises.forEach((ex, i) => {
        if (!isDict(ex)) { issues.push(finding('FAIL', 'BAD_EXERCISE', 'Exercise must be object.', sname)); return; }
        const rawEx = get(ex, 'name', null);
        const ename = pyStr(pyFalsy(rawEx) ? `Exercise ${i + 1}` : rawEx);
        const scope = `${sname} / ${ename}`;
        const sets = get(ex, 'sets', null);
        if (!pyInt(sets) || typeof sets === 'boolean' || sets < 1) {
          issues.push(finding('FAIL', 'SETS_INVALID', 'Hard Sets must be a positive integer.', scope)); return;
        }
        if (sets !== 2 && pyFalsy(get(ex, 'set_reason', null)))
          issues.push(finding('FAIL', 'SET_JUSTIFICATION', `${sets} Hard Sets requires explicit Purpose/Value/Recovery justification.`, scope));
        if (sets > 3)
          issues.push(finding('CONDITIONAL', 'UNUSUAL_SET_COUNT', 'More than three sets: review fatigue, purpose and workload even with justification.', scope));
        if (pyFalsy(get(ex, 'variant', null)))
          issues.push(finding('CONDITIONAL', 'VARIANT_MISSING', 'Missing equipment/variant; progression comparability may suffer.', scope));
        if (pyFalsy(get(ex, 'progression_rule', null)))
          issues.push(finding('CONDITIONAL', 'PROGRESSION_MISSING', 'No per-exercise progression rule.', scope));
        const rir = get(ex, 'rir_targets', null);
        if (!Array.isArray(rir) || rir.length !== sets || !rir.every((x) => validNum(x, 0))) {
          issues.push(finding('FAIL', 'RIR_INVALID', 'rir_targets must contain a nonnegative value per Hard Set.', scope));
        } else if (rir.some((x) => x < 1) && get(ex, 'safe_exit', null) !== true) {
          issues.push(finding('FAIL', 'UNSAFE_FAILURE_ACCESS', '0–<1 RIR requires positively verified safe set termination; no conditional waiver.', scope));
        }
        if (get(ex, 'known_safety_blocker', null) === true)
          issues.push(finding('FAIL', 'SAFETY_BLOCKER', 'Known safety blocker for prescribed exercise.', scope));
        if (get(ex, 'safe_exit', null) === null)
          issues.push(finding('CONDITIONAL', 'EXIT_NOT_EVALUATED', 'Safe stop/exit procedure not declared.', scope));
        const stim = get(ex, 'stimulus', null);
        if (!isDict(stim)) { issues.push(finding('FAIL', 'NO_P_S', 'Provide explicit stimulus map; names do not establish P/S.', scope)); return; }
        for (const area of Object.keys(stim)) {
          const tag = stim[area];
          if (!has(ledger, area)) { issues.push(finding('FAIL', 'UNKNOWN_AREA', `${area} not in Fixed Core or activated Override.`, scope)); continue; }
          if (!ALLOWED_STIMULUS.has(tag)) { issues.push(finding('FAIL', 'INVALID_STIMULUS', `${area}: invalid tag ${pyStr(tag)}`, scope)); continue; }
          if (tag === 'P') { ledger[area].P_sets += sets; ledger[area].exposures[sname] = 'P'; }
          else if (tag === 'S') { ledger[area].S_sets += sets; if (ledger[area].exposures[sname] !== 'P') ledger[area].exposures[sname] = 'S'; }
          else if (tag === 'S?' || tag === '?') { ledger[area].S_uncertain_sets += sets; }
        }
        const perSet = get(ex, 'seconds_per_set', 45);
        const restSec = get(ex, 'rest_sec', 120);
        if (!validNum(perSet, 1) || !validNum(restSec, 0))
          issues.push(finding('FAIL', 'TIME_INPUT_INVALID', 'Invalid seconds_per_set / rest_sec.', scope));
        else rest += (sets * perSet + Math.max(sets - 1, 0) * restSec) / 60.0;
      });
      let transition = get(profile, 'transition_min_per_exercise', 1.5);
      let margin = get(profile, 'margin_min_per_session', 5);
      if (!validNum(transition, 0) || !validNum(margin, 0)) {
        issues.push(finding('FAIL', 'TIME_CONFIGURATION', 'Invalid transition/margin setting.', sname));
        transition = 1.5; margin = 5;
      }
      let estimate = rest + exercises.length * transition + margin;
      if (get(profile, 'time_includes_warmup', null) === true) {
        const warmup = get(profile, 'warmup_min', null);
        if (!validNum(warmup, 0)) issues.push(finding('CONDITIONAL', 'WARMUP_UNSPECIFIED', 'Time includes warm-up but minutes not provided.', sname));
        else estimate += warmup;
      }
      const limit = get(profile, 'session_time_limit_min', null);
      sessionEstimates[sname] = pyRound(estimate, 2);
      if (!validNum(limit, 1)) issues.push(finding('CONDITIONAL', 'TIME_LIMIT_UNKNOWN', 'Session capacity not specified; cannot confirm fit.', sname));
      else if (estimate > limit) issues.push(finding('FAIL', 'TIME_OVER', `Estimated ${fmt1(estimate)} min exceeds ${fmt1(limit)}-min limit.`, sname));
      else if (estimate > limit * 0.9) issues.push(finding('CONDITIONAL', 'TIME_TIGHT', `Estimated ${fmt1(estimate)}/${fmt1(limit)} min; real-world delays could exceed limit.`, sname));
    });
    for (const area of Object.keys(ledger)) {
      const entry = ledger[area];
      const p = entry.priority;
      const exposure = Object.values(entry.exposures);
      if (p !== 'Priority' && p !== 'Standard') continue;
      const cfg = allareas[area];
      const exc = isDict(cfg) ? get(cfg, 'accepted_exception', null) : null;
      const accepted = typeof exc === 'string' && exc.trim() !== '' && get(cfg, 'exception_accepted_by_user', null) === true;
      if (exposure.length < 2) {
        if (accepted) issues.push(finding('CONDITIONAL', 'EXPOSURE_EXCEPTION', `${area}: ${exposure.length} credible exposures; documented exception: ${exc}`, area));
        else issues.push(finding('FAIL', 'TOO_FEW_EXPOSURES', `${area}: ${exposure.length} credible exposures; default is two.`, area));
      } else if (!exposure.includes('P')) {
        if (accepted) issues.push(finding('CONDITIONAL', 'S_ONLY_EXCEPTION', `${area}: S+S not automatically sufficient; accepted exception: ${exc}`, area));
        else issues.push(finding('FAIL', 'SECONDARY_ONLY', `${area}: S+S lacks a Primary exposure.`, area));
      } else if (entry.functional_gap) {
        if (accepted) issues.push(finding('CONDITIONAL', 'FUNCTIONAL_GAP_EXCEPTION', `${area}: known functional gap; accepted: ${exc}`, area));
        else issues.push(finding('FAIL', 'FUNCTIONAL_GAP', `${area}: marked functional gap unresolved.`, area));
      }
    }
    let severity = 'PASS';
    for (const it of issues) if (PRIORITY_ORDER[it.level] > PRIORITY_ORDER[severity]) severity = it.level;
    let total = 0;
    for (const s of sessions) {
      if (!isDict(s)) continue;
      const exs = get(s, 'exercises', []);
      if (!Array.isArray(exs)) continue;
      for (const ex of exs) if (isDict(ex) && pyInt(get(ex, 'sets', null))) total += Number(ex.sets);
    }
    return { status: severity, summary: { sessions: sessions.length, total_hard_sets: total },
      ledger, session_time_estimates_min: sessionEstimates, findings: issues, disclaimer: DISCLAIMER };
  }

  /* ---- Builder-level checks (not part of the Python validator) ---- */
  // Library status and safe-exit conditions are builder concerns (tools/builder/SPEC.md §5).
  // Level INFO never changes the status.
  function builderChecks(plan, library) {
    const byId = new Map((library && library.exercises ? library.exercises : []).map((e) => [e.id, e]));
    const out = [];
    const profile = isDict(plan.profile) ? plan.profile : {};
    let anyNearFailure = false;
    for (const s of (Array.isArray(plan.sessions) ? plan.sessions : [])) {
      for (const ex of (s && Array.isArray(s.exercises) ? s.exercises : [])) {
        const scope = `${s.name} / ${ex.name}`;
        const rir = Array.isArray(ex.rir_targets) ? ex.rir_targets.filter((x) => typeof x === 'number') : [];
        if (rir.some((x) => x < 1)) anyNearFailure = true;
        const lib = ex.library_id ? byId.get(ex.library_id) : null;
        if (!lib) { out.push(finding('CONDITIONAL', 'LIBRARY_UNVERIFIED', 'Exercise outside the approved library; P/S assigned manually and not reviewed.', scope)); continue; }
        if (!lib.review || lib.review.status !== 'approved') out.push(finding('CONDITIONAL', 'LIBRARY_NOT_APPROVED', `Library entry ${lib.id} is not approved.`, scope));
        if (rir.some((x) => x < lib.rir_floor_default))
          out.push(finding('CONDITIONAL', 'RIR_BELOW_FLOOR', `RIR below the library default minimum ${lib.rir_floor_default} for ${lib.id}.`, scope));
      }
    }
    if (profile.safety_answered !== true) {
      out.push(finding(anyNearFailure ? 'FAIL' : 'CONDITIONAL', 'SAFETY_GATE_OPEN',
        anyNearFailure ? 'Safety questions unanswered; near-failure (RIR < 1) work cannot be released.' : 'Safety questions unanswered.'));
    }
    const pr = Object.values(isDict(plan.areas) ? plan.areas : {}).concat(Object.values(isDict(plan.functional_overrides) ? plan.functional_overrides : {}))
      .filter((a) => isDict(a) && a.priority === 'Priority').length;
    if (pr >= 5) out.push(finding('INFO', 'PRIORITY_DILUTED', `${pr} areas marked Priority; priority loses meaning when most areas have it.`));
    if (isDict(plan.focus_block) && plan.focus_block.enabled === true && plan.focus_block.accepted !== true)
      out.push(finding('CONDITIONAL', 'FOCUS_BLOCK_PENDING', 'Focus Block is a departure from Continuous Progression and needs explicit acceptance.'));
    return out;
  }
  function combinedStatus(result, extra) {
    let sev = result.status;
    for (const it of extra) if (it.level in PRIORITY_ORDER && PRIORITY_ORDER[it.level] > PRIORITY_ORDER[sev]) sev = it.level;
    return sev;
  }

  return { CORE, ALLOWED_STIMULUS: Array.from(ALLOWED_STIMULUS), evaluate, builderChecks, combinedStatus, _pyRound: pyRound };
});
