# HARDSET — Validation Test Suite Overview

The executable tests live in `validation/tests/test_validator.py` and run with:

```bash
python -m unittest discover -s validation/tests -v
```

## Cases covered

1. Completely declared generic 2-session plan with enough P exposures -> PASS.
2. S? cannot create a credible second exposure -> FAIL.
3. Same exposure defect with **documented, user-accepted exception** -> CONDITIONAL.
4. Written exception without explicit user acceptance still -> FAIL.
5. 0 RIR prescribed without positively verified safe exit -> FAIL.
6. S + S without P for Standard -> FAIL, not automatically valid.
7. Multiple exercises in one session yield at most one exposure per muscle.
8. Estimated time above agreed budget -> FAIL.
9. Three sets without reason -> FAIL; with valid reason can PASS.
10. Optional region may have zero meaningful P/S without affecting pass.
11. Unknown claimed muscle area -> FAIL; no fake Fixed Core expansion.
12. Missing goals / missing human review -> CONDITIONAL.
13. Validator must not mutate input data while evaluating.
14. Duplicate session identifiers are rejected rather than merged silently.
15. Missing warm-up/time-budget interpretation gives a Conditional warning.
16. Extra muscles must be declared as Functional Overrides and may not shadow Fixed Core.
17. Malformed input (non-object JSON, non-object `constraints`/`human_review`, invalid JSON) -> rejected with CLI exit code 2, never exit 1 (CONDITIONAL) and never an unhandled traceback.

Additional production cases to implement before any user-facing release: actual scenario-level safety review, reliability of exercise P/S tagging, explicit patient exclusion rules, time-estimation calibration, machine substitution provenance, inconsistent goals and priorities, repeated data imports, recovery/resilience checks and fuzz/property-based tests.

## Important contrast

- Validator output PASS only means *the information and declared tags supplied pass these tests*.
- The examples contain **synthetic, generic** data. They must never be used as training advice for a person whose goals or limits are unknown.
