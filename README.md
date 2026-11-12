# HARDSET — Knowledge Pack v1.0

**Date:** 2026-11-12  
**Language:** Polish explanations, English HARDSET technical terms.  
**Content:** nine approved methodology chapters (reconstructed/normalized text), supporting appendices, verified scholarly reference registry and evidence matrix, deterministic rule-checking prototype, and Claude handoff instructions.

## Start

**Claude Chat:** attach or paste `HARDSET_MASTER.md`, then use `claude/CLAUDE_CHAT_START_PROMPT.md`.  
**Claude Projects:** add the master as project knowledge, and apply `CLAUDE.md` as project instructions.  
**Claude Code:** open the extracted folder and read `CLAUDE.md`; test with `python -m unittest discover -s validation/tests -v`.

See `START_HERE.md` for details.

## Canonical rules (9 chapters)

1. Effort, Hard Sets & Muscular Failure
2. Pattern-Based Exercise Architecture
3. Set Architecture
4. Exercise Selection & Safety
5. Progression & Autoregulation
6. Weekly Programming & Recovery
7. Outcome Tracking & Program Evaluation
8. Long-Term Planning & Specialization
9. Program Construction & Validation

## Scientific backbone

- 23 scholarly references, DOI-verified for identity and relevant conclusions.
- 32 evidence-matrix claims labeled by epistemic type.
- Audit of exclusion and limitations in `research/RESEARCH_AUDIT.md`.
- Explicit warning that two sets/exercise, two exposures/week, P/S accounting, exact RIR targets, and heuristic volume bands are **HARDSET design decisions / implementation suggestions**, not universally proven optimal recipes.

## Integrity and scope

- **No personal profile or historical user workout** is included.
- No new interactive app or ebook is built in this release.
- CLI validator is an optional prototype and does not replace expert review, clinical assessment or measurement of actual hypertrophy.
- Chapters 01–05 are editorial reconstructions of approved rules; see `PROVENANCE.md`.

## Suggested update procedure

Any future revision must update the relevant chapter(s) with explicit approval, evidence matrix and bibliography as needed, examples, tests, master file and version metadata. Do not silently change a final chapter to match an application implementation.
