# Continuous Bench Priority v1.1 (nazwa robocza)

Osobny program siłowo-hipertroficzny oparty na HARDSET v1.0. **Nie jest nową wersją metodologii HARDSET** i niczego w niej nie zmienia: rozdziały 01–09, aneksy, bibliografia i walidator pozostają źródłem nadrzędnym.

**Status:** specyfikacja robocza po audycie etapu 1, czeka na decyzje właściciela. Nazwy HARDSET, Repsmith i nazwa programu są robocze do czasu decyzji o marce.

| Ścieżka | Zawartość |
|---|---|
| `handoff/` | pakiet przekazania w wersji otrzymanej (bez zmian), wraz z `machine/` i `references/` |
| `AUDIT_v1.1.md` | wyniki audytu: zgodność z HARDSET, błędy, niejasności, decyzje |
| `analysis/` | przykładowy tydzień w formacie walidatora HARDSET i wynik walidacji |
| `tests/` | testy audytowe danych pakietu |

```bash
python -m unittest discover -s programs/continuous-bench-priority/tests -v
python programs/continuous-bench-priority/handoff/machine/e1rm.py --self-test
python validation/validator.py programs/continuous-bench-priority/analysis/example_week_validator_input.json
```

Zmiany w specyfikacji trafią do nowej wersji (np. 1.1.1) dopiero po decyzjach z `AUDIT_v1.1.md`, sekcja 9. Pliki w `handoff/` zostają jako zapis tego, co zostało przekazane.
