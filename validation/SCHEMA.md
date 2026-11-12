# HARDSET Validator — Input Contract v0.1

Machine-readable input: JSON object, UTF-8. Examples in `../examples/`. No JSON schema library is needed to run the prototype; the contract below is descriptive. A future production package should publish an executable JSON Schema and type definitions.

## Top-level required objects

| Property | Type | Meaning |
|---|---|---|
| `goals` | nonempty list of strings | User-declared intent, never inferred |
| `human_review` | object | Attestation, not a clinical clearance |
| `constraints` | object | Schedule time/buffer parameters |
| `areas` | object | Exactly the 12 Fixed Core keys as defined in Chapter 02 |
| `functional_overrides` | object | Optional additional named targeted functions, same area schema |
| `sessions` | list of objects | Actual physical sessions, not days automatically inferred from name |

## `human_review`

Boolean `true` for each independent reviewed item: `goal_fit`, `ps_mechanics`, `exercise_safety`, `recovery`. Missing items produce CONDITIONAL. Reviews **attest only** that a qualified human/programmer has considered the issue, not that the validator confirmed it independently.

## `constraints`

- `session_time_limit_min` (positive number; missing produces CONDITIONAL)
- `time_includes_warmup` (boolean)
- `warmup_min` if time includes it; otherwise not needed for working portion.
- `transition_min_per_exercise` (nonnegative, default 1.5)
- `margin_min_per_session` (nonnegative, default 5)

Time estimate = Σ `sets * seconds_per_set + (sets−1) * rest_sec` over exercises, converted to minutes, + transitions + margin + applicable warm-up. This estimates **intra-exercise recovery** and transitions; not all real world delays are predictable. Near-capacity session (>90% budget) becomes CONDITIONAL.

## Each `areas` entry

| Field | Allowed |
|---|---|
| `priority` | `Priority`, `Standard`, `Optional` |
| `intent` | `Development`, `Maintenance` |
| `functional_gap` | optional boolean; `true` must be resolved or accepted exception |
| `accepted_exception` | explicit rationale for departing from coverage; string |
| `exception_accepted_by_user` | `true` required with rationale to reduce coverage FAIL to CONDITIONAL |

The `priority` values must be supplied deliberately; no default priority for any specific region.

## Session and exercise

Each session has unique `name` and `exercises` list. Each exercise:

- `name`: descriptive label; used only for output (not physiology inference).
- `variant`: exact equipment/variant; missing gives CONDITIONAL.
- `sets`: positive integer; default policy 2.
- `set_reason`: required if sets != 2; >3 also produces CONDITIONAL review.
- `rir_targets`: numeric list of length == sets; individual values ≥0.
- `safe_exit`: boolean; must be **true** for any planned RIR below 1.
- `known_safety_blocker`: boolean; `true` always FAIL.
- `rest_sec`: number ≥0, suggested but not universal.
- `seconds_per_set`: number >0, rough estimate.
- `progression_rule`: nonempty string.
- `stimulus`: dictionary of area name -> `P`, `S`, `S?`, `?` or `-`.

The algorithm cannot validate whether a `P` classification is biomechanically appropriate. A human must review actual movement, equipment, execution and intended target.

## Output

`status`: PASS / CONDITIONAL / FAIL.  
`ledger`: per-area P/S counts and a session map `P` or `S`; uncertain S? sets separate.  
`summary`: session count and total physically executed Hard Sets.  
`session_time_estimates_min`: model estimate per session.  
`findings`: each with severity, code, scope and message.

`PASS` is **structural verification of the declarations only**. It is not a guarantee of hypertrophy, optimal weekly volume, medically safe performance, accurate RIR or equipment suitability.
