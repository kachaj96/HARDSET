#!/usr/bin/env python3
"""Rebuild single-file HARDSET_MASTER.md from the component Markdown source files."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parts=[
    ('PRIMARY CHAPTERS: APPROVED RULES', list(sorted((ROOT/'chapters').glob('[0-9][0-9]_*.md')))),
    ('SUPPORTING APPENDICES: NON-NORMATIVE', list(sorted((ROOT/'appendices').glob('*.md')))),
    ('SCIENTIFIC EVIDENCE: VERIFIED BIBLIOGRAPHY, CLAIM MATRIX AND AUDIT',
         [ROOT/'research'/'REFERENCES.md', ROOT/'research'/'EVIDENCE_MATRIX.md', ROOT/'research'/'RESEARCH_AUDIT.md']),
    ('IMPLEMENTATION: VALIDATOR SPECIFICATION AND TEST PROCEDURE',
         [ROOT/'validation'/'README.md',ROOT/'validation'/'SCHEMA.md',ROOT/'validation'/'RULE_CATALOG.md',ROOT/'validation'/'TEST_CASES.md']),
]
header='''# HARDSET — Master Knowledge Base v1.0

**Read this whole document before proposing a plan.**

- The nine chapters are approved at the rule level (see `PROVENANCE.md` about editorial reconstruction vs verbatim text).
- The scientific references support specific bounded statements; HARDSET design decisions and numeric heuristics are not universal research findings.
- This file contains **no personal training profile**. Any individual plan **MUST be created from a new interview**, never from assumptions about an earlier user.
- `R##` citations refer to the verified research bibliography contained in this same master.
- Supporting appendices and the prototype validator do not override approved rules.
- The retracted RIR source described under Research Audit is **not valid supporting evidence**.
- For Claude: read `CLAUDE.md` and `claude/CLAUDE_CHAT_START_PROMPT.md` from the pack if available; if only this master is provided, obey the above rules and start any personal program from zero.

**Source timestamp: 2026-11-12.**

---
'''
contents=[header]
for section,files in parts:
    contents.append(f'\n---\n\n# PART — {section}\n')
    for path in files:
        txt=path.read_text(encoding='utf-8')
        # Keep Markdown source readable when standalone; source link paths are not required here.
        contents.append(f'\n<!-- SOURCE: {path.relative_to(ROOT)} -->\n\n{txt.rstrip()}\n\n---\n')
(ROOT/'HARDSET_MASTER.md').write_text('\n'.join(contents),encoding='utf-8')
print('Wrote',ROOT/'HARDSET_MASTER.md', 'bytes:', (ROOT/'HARDSET_MASTER.md').stat().st_size)
