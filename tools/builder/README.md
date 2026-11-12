# HARDSET Kreator Planu

Prowadzony kreator planów zgodnych z HARDSET. Specyfikacja: `SPEC.md`.

| Plik | Rola |
|---|---|
| `index.html` | interfejs kreatora (strona artifactu, bez szkieletu `<html>`) |
| `engine.js` | silnik reguł: port `validation/validator.py` + kontrole kreatora |
| `engine_cli.js` | `node tools/builder/engine_cli.js plan.json` (kody wyjścia jak walidator) |
| `build_library_review.py` | generuje `library/REVIEW.md` z `library/exercises.json` |

Artifact publikuje `index.html` razem z `engine.js` i `library/exercises.json` (jako `exercises.json`).
Plany zapisują się w bazie artifactu, nie w repozytorium.

Testy: `python -m unittest discover -s validation/tests -v` (zgodność silników wymaga Node.js; bez niego test jest pomijany).
