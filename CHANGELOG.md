# HARDSET Knowledge Pack — Changelog

## v1.1.0 — 2026-11-12

Research addition. Chapters 01–09 and appendices unchanged.

- Added 7 verified references R24–R30 on strength training for runners (running economy, performance, injury prevention, tendon adaptation).
- Added evidence-matrix rows E33–E38. E36 (exercise programmes reduce running-related injuries in endurance runners) is NOT_SUPPORTED per R28. E38 (run-support exercise selection) is a HARDSET Design Decision.
- `RESEARCH_AUDIT.md`: addendum with scope, method and interpretation controls.
- `test_integrity.py`: expected counts updated to 30 references / 38 evidence rows to match the deliberate addition.
- README / START_HERE counts updated; `HARDSET_MASTER.md` and `MANIFEST.json` regenerated.

## v1.0.1 — 2026-11-12

Tooling-only patch. Methodology (Chapters 01–09), appendices and research files unchanged.

- `validation/validator.py`: check that the plan is a JSON object before reading it, and that `constraints` / `human_review` are objects. Malformed input now exits with code 2 instead of an unhandled traceback with exit code 1 (which is the CONDITIONAL code).
- `validation/tests/test_validator.py`: 3 regression tests for malformed input (28 tests total).
- `scripts/build_manifest.py`: skip dot-paths (`.git/`, `.gitignore`, `.claude/`), so the manifest only covers pack content when run inside a git repository.
- `validation/TEST_CASES.md`: add case 17; remove duplicate session IDs from the "to implement" list, since case 14 already covers them.
- `HARDSET_MASTER.md` and `MANIFEST.json` regenerated.

## v1.0 — 2026-11-12

- Collected all nine approved HARDSET chapters at approved **rule** level.
- Editorially reconstructed early chapters and normalized later chapters, with provenance disclosure.
- Preserved the separate, non-normative Weekly Volume Reference Guide.
- Built 23-entry reference registry with verified DOI identities and claim limitations.
- Built 32-row evidence matrix separating scientific findings, HARDSET decisions, heuristics, and unsupported claims.
- Excluded a discovered retracted RIR estimation article; documented DOI and retraction notice.
- Added deterministic Python structural validator prototype, example inputs and executable tests.
- Added Claude Chat / Projects / Code instructions, and a single-file master.
- Excluded all personal training data and workout plans by design.
