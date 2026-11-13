"""Owner-approved amendments to Continuous Bench Priority v1.1 (draft v1.2).

Pure functions, no I/O. They implement decisions D-3 and D-4 from AUDIT_v1.1.md and
leave the handoff package (handoff/) untouched. See SPEC_AMENDMENTS_v1.2.md.

Sources of the numbers: e1RM = load * (1 + (reps + RIR) / 30) (Epley, as in the handoff).
This is a heuristic estimate, not a measured 1RM.
"""

PLATE_STEP_KG = 2.5
UP_PCT_PER_RPE_POINT = 2.5   # program hypothesis, below the Epley estimate of ~2.6-3.0%
UP_PCT_CAP = 5.0             # at most two RPE points of correction in one go
BASE_STEP_KG = 2.5           # D-4: wave base step (still an example step, see N-7)


def e1rm(load_kg, reps, rir):
    return load_kg * (1 + (reps + rir) / 30)


def epley_pct_per_rpe_point(reps, rir):
    """Load change (%) that makes a set exactly one RIR harder at the same e1RM."""
    return ((30 + reps + rir) / (29 + reps + rir) - 1) * 100


def round_to_plate(kg, step=PLATE_STEP_KG):
    return round(kg / step) * step


def upward_correction(load_kg, target_rpe_low, actual_rpe, technique_ok=True,
                      week=1, multi_rep=True, plate=PLATE_STEP_KG):
    """D-3: load for the next set when the first multi-rep set was clearly too light.

    Applies only when the set was a multi-rep set (not a single, not AMRAP), technique and
    bar speed were fine, the gap to the lower end of the target RPE is at least one full
    point, and it is not week 4 (the lighter week is planned, exception W-4).
    Returns the new load in kg (unchanged when no correction applies).
    """
    if not multi_rep or not technique_ok or week == 4:
        return load_kg
    points = int(target_rpe_low - actual_rpe)   # full points only; whole-point gap or no change
    if points < 1:
        return load_kg
    pct = min(UP_PCT_PER_RPE_POINT * points, UP_PCT_CAP)
    new = round_to_plate(load_kg * (1 + pct / 100), plate)
    return max(new, load_kg + plate)


def base_decision(prev, cur, single_ok, comparable=True):
    """D-4: wave base decision from two consecutive control sets (T3 AMRAP).

    prev, cur: dicts with load, reps, rir. The criterion is one repetition more at the
    same load and RIR, i.e. e1RM higher by at least load/30. If the load changed between
    waves, the same criterion is applied through e1RM. Returns one of:
    'raise', 'hold', 'hold_unconfirmed', 'check_recovery', 'inconclusive'.
    """
    if not comparable or prev is None:
        return 'inconclusive'
    diff = e1rm(cur['load'], cur['reps'], cur['rir']) - e1rm(prev['load'], prev['reps'], prev['rir'])
    one_rep = cur['load'] / 30
    eps = 1e-9
    if diff >= one_rep - eps:
        return 'raise' if single_ok else 'hold_unconfirmed'
    if diff <= -one_rep + eps:
        return 'check_recovery'
    return 'hold'
