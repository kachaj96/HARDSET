# HARDSET — deterministic structural validator (prototype)

**This is not an app and is not a complete AI plan generator.** It is a small Python command-line prototype that demonstrates testable rule checks required by Chapter 09. Python 3.10+; standard library only.

```bash
python validation/validator.py examples/generic_pass.json
python -m unittest discover -s validation/tests -v
```

The CLI prints JSON with `status` and messages; exit code 0 = PASS, 1 = CONDITIONAL, 2 = FAIL or malformed input.

## Core behaviors

- Expects all 12 Fixed Core areas to be declared explicitly (no default Priority assignments).
- Separately records P sets, credible S sets, uncertain S? counts, and session-level P/S exposures.
- Counts max one exposure per area per session, with P taking precedence.
- Requires ≥2 credible exposures for Priority/Standard, including at least one P; `S+S` is not automatically enough.
- An accepted and documented exposure exception can produce CONDITIONAL, not PASS.
- Inspects work set count and whether nondefault set counts have documented justification.
- Blocks any planned `rir_targets` below 1 if safe termination has not been positively declared.
- Estimates session time with per-set duration, within-exercise rest, transitions and a buffer; conservatively marks near-limit estimates CONDITIONAL.
- Checks progression rule presence but does not implement all training decisions or compute hypertrophy.

## Deliberate limitations

- **P/S tags are supplied by the planner, not guessed from names.** The tool cannot judge biomechanics from a string.
- **Risk and safety flags are supplied, not certified.** Even PASS is not a medical clearance or guarantee of zero injury risk.
- The time model is approximate and does not know gym crowding, warm-up length if not provided, machine maintenance or actual tempo.
- It cannot decide baseline suitability, actual recovery, development vs maintenance dose or realized biological outcome. These require human/AI **interpretation with evidence limits**.
- Python implementation is a demonstration. For production integration, require a documented schema, independent test cases, versioning, security review and real exercise-selection data.

## Example JSON shape

```json
{
  "constraints": {
    "session_time_limit_min": 60,
    "time_includes_warmup": false,
    "transition_min_per_exercise": 1.5,
    "margin_min_per_session": 5
  },
  "areas": {
    "Chest": {"priority":"Standard","intent":"Development"},
    "Back": {"priority":"Standard","intent":"Development"},
    "Lateral Delts": {"priority":"Optional","intent":"Development"}
  },
  "functional_overrides": {},
  "sessions": [
    {"name":"Session A","exercises":[{
      "name":"Stable press","variant":"Machine model A",
      "sets":2,"rir_targets":[1,0],"safe_exit":true,
      "rest_sec":150,"seconds_per_set":45,
      "progression_rule":"Lead-Set upper bound, Support floor",
      "stimulus":{"Chest":"P","Elbow Extensors":"S"}
    }]}
  ]
}
```

**Note:** sample shape above intentionally omits the remaining required Fixed Core declarations. Use `examples/generic_pass.json` for a complete valid input.

## Authoring directives for Claude

Never mark a program PASS just because the validator prints PASS. First inspect the input tags, risk declarations, personal suitability, volume baseline and accepted deviations. The validator checks **consistency**, not scientific certainty or actual training success.
