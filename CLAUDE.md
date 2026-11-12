# CLAUDE.md — HARDSET / Project Operating Instructions

## Mission

Treat this repository as the **general-purpose HARDSET resistance-training methodology v1.0**, reconstructed from nine already-approved chapters. Help apply, evaluate or extend it faithfully. **No particular user's personal training profile is present. Start individual programming from zero.**

## Read order

1. `START_HERE.md`
2. `HARDSET_MASTER.md` or `chapters/01_...md` through `chapters/09_...md` in order.
3. `research/EVIDENCE_MATRIX.md` and `research/REFERENCES.md`; `research/RESEARCH_AUDIT.md` for exclusion notice.
4. `appendices/` for non-normative implementation guidance.
5. `validation/README.md`, `validation/SCHEMA.md`, `validation/RULE_CATALOG.md`, `validation/TEST_CASES.md` and Python validator when generating or validating plans.

## Authority order

1. **Approved Chapters 01–09:** normative HARDSET program rules (at the level of the approved decisions).
2. **Verified research:** establishes evidence and limitations; it is not a backdoor to pretend an author-defined rule has been scientifically proven.
3. **Appendices:** non-normative organizational defaults, examples and numeric heuristics; cannot contradict approved chapters.
4. **Validator code:** structural prototype, not arbiter of biomechanical appropriateness or medical safety.
5. **Examples:** synthetic data only; never personalize them by assuming they describe the user.

If you discover a conflict, explain it explicitly, offer a change proposal and request approval **before changing the accepted methodology**. Never silently revise final chapters.

## Three evidence classes you MUST keep separate

- **Scientific Evidence:** studies actually support a claim; cite exact `R##` ID and DOI; report limitations, especially indirect vs direct work and study populations.
- **HARDSET Design Decision:** an intentional methodological convention, such as Two-Set Default, two exposure default, Fixed Core 12, Lead-Set Progression.
- **Implementation Heuristic:** a practical number or cadence, such as rep-band templates, 5–10% backoff, rest ranges, volume labels and review windows.

When a claim is explicitly tagged **NOT_SUPPORTED** in `research/EVIDENCE_MATRIX.md`, never assert it as a fact. Never cite the **retracted** RIR study listed in `research/RESEARCH_AUDIT.md` as positive evidence.

## Mandatory HARDSET integrity rules

- A Hard Set excludes warm-ups; work must meet technique/ROM/safe-stop standards.
- Two sets per exercise default; not mandatory weekly set dose or proven universal optimum.
- First ~1 RIR and second ~0–1 RIR **only if the stop is safe**; free-weight and high-risk movements can be 1–2 RIR.
- No fictional `S = 0.5 P`; P, S, S? and — are meaningfully distinct.
- At most one Exposure per area per session. Priority: P+P preferred, credible P+S allowed without relevant gap. Standard: P+P or P+S. S+S insufficient by default. Optional no required minimum.
- Fixed Core has 12 areas; Overrides are dynamic. Priority cannot be silently changed to solve time constraints.
- Machine bias is preference under otherwise comparable conditions, not a hypertrophy superiority claim.
- Lead Set upper-bound + Supporting Set lower-bound and comparable execution = candidate for load progression; both upper bounds NOT required.
- Split follows goals and weekly stimulus, not reverse.
- Volume Baseline + Response; heuristic numeric categories only in Appendix A.
- No compulsory mesocycles or deload calendar.
- Evidence-Limited Evaluation: performance log does not prove hypertrophy; classify outcomes separately Not Assessed / Inconclusive / Supported Progress / Concern.
- A validator PASS is structural, not biological success or clinical safety guarantee.

## New plan workflow (from zero)

1. Ask only necessary personal questions; **do not inherit any prior user's profile**. At minimum need: training objective(s), relative muscle priorities/intent, experience and recent tolerated training exposure, available days and session duration (clarify inclusion of warm-up), equipment, relevant safety limitations and other physical activities.
2. If crucial safety information is missing, avoid prescribing risky near-failure exercises and flag unresolved gate.
3. Build priority + intent map for all Fixed Core areas; activated Functional Overrides are explicit.
4. Build weekly P/S/Exposure ledger before choosing split.
5. Choose suitable exercises and safe RIR, then Hard Sets/rep ranges/rest and Lead-Set progression.
6. Validate time, coverage, recoverability, safety and output requirements. Use runnable validator only on appropriately annotated JSON; check **real** mechanical meaning of tags manually.
7. Deliver the plan and candid PASS/CONDITIONAL/FAIL findings; include evidence limits and how to review the program.
8. Gather actual results before claiming adaptive adequacy.

## Working style

Direct Polish prose unless asked for another language; retain HARDSET terms in English. Be skeptical of unsupported precision. Keep structure understandable, avoid needless models/variables or an app-specific bias. Write explicit assumptions, constraints, missing evidence and exceptions. Do not mention or reconstruct any particular earlier personal training records.

## If asked to build an app or an ebook later

Propose a separate approved workstream. Keep this repository as a single version-controlled source of training rules, with a deterministic, tested rule engine separated from AI explanations. **Do not build an app or ebook in the initial Knowledge Pack task.**
