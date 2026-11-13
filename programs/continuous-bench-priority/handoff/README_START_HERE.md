# HANDOFF — HARDSET Powerbuilding / Continuous Bench Priority v1.1

**Stan:** specyfikacja robocza do wdrożenia i recenzji; nie jest zatwierdzonym, wydanym e-bookiem.  
**Data przekazania:** 2026-11-13.  
**Język docelowy:** polski.  
**Cel:** przekazać Claude Code wszystkie uzgodnienia dotyczące osobnego kierunku Bench Priority, ponieważ istniejący projekt zawiera już główny HARDSET v1.0.

## Ważne granice

1. Nie rekonstruuj z tego ZIP-a oryginalnego HARDSET. **Prawdziwy, zatwierdzony HARDSET v1.0 znajduje się w istniejącym repozytorium**. Odszukaj dziewięć rozdziałów, aneksy, reguły, validator i bibliografię; to źródło nadrzędne.
2. Ten pakiet jest specyfikacją **rozszerzenia POWERBUILDING**, nie nową wersją dziewięciu rozdziałów HARDSET. Nie zmieniaj ich milcząco.
3. Zachowaj osobną przestrzeń, np. `programs/continuous-bench-priority/` albo dopasuj ścieżkę do zastanej architektury repozytorium. Nie niszcz istniejących plików.
4. Uzgodnienia treningowe są do audytu naukowego, matematycznego i praktycznego, zanim powstanie finalna książka. Jeśli znajdziesz błąd, wypisz go i zaproponuj poprawkę, zamiast przemycać zmianę.
5. Nazwy HARDSET i Repsmith są **robocze do decyzji brandingowej**; nie przeprowadzaj automatycznego rebrandingu aplikacji ani publikacji.
6. Bez wyraźnej akceptacji właściciela **nie generuj finalnych e-booków, nie publikuj, nie kupuj domen, nie przenoś nazw i nie twórz ostatecznych znaków marki**.

## Zawartość

- `01_DECISIONS_AND_BOUNDARIES.md` — cel, zakres, ustalenia i nierozstrzygnięte tematy.
- `02_TRAINING_SYSTEM.md` — 6 patternów + izolacje, relacja z głównym HARDSET.
- `03_BENCH_WAVE.md` — 4-tygodniowa, powtarzana fala bench z %/RPE.
- `04_AMRAP_E1RM_AND_PB.md` — benchmark T3, e1RM, decyzje o PB.
- `05_EXAMPLE_3X60MIN_PLAN.md` — pełny mikrocykl, serie i audyt czasu.
- `06_OPTIONAL_TEST_AND_MEET.md` — test 1RM oraz moduł startowy.
- `07_VALIDATION_AND_EVIDENCE.md` — ryzyka, kryteria, literatura i zasady źródeł.
- `08_BRAND_AND_EDITORIAL_HANDOFF.md` — wymagania marki oraz reżim redakcyjny „bez AI slop”.
- `machine/bench_wave.json` — wersja danych do kalkulatorów i testów.
- `machine/e1rm.py` — pomocniczy, niewymagający bibliotek kalkulator e1RM + testy jednostkowe.
- `references/RESEARCH_LINKS.md` — sprawdzone źródła i zakres ich zastosowania.
- `CLAUDE_CODE_MASTER_PROMPT.md` — gotowy prompt do wklejenia.

## Kolejność prac dla Claude Code

0. Inspekcja repozytorium, identyfikacja zatwierdzonego HARDSET v1.0; rozbieżności raportuj.
1. Import niniejszego modułu i kontrola matematyczna oraz czasowa.
2. Przedstaw właścicielowi kwestię nazewnictwa i 2–3 spójne kierunki identyfikacji (z faktycznymi makietami do oceny).
3. Zadaj tylko pytania decyzyjne potrzebne do akceptacji marki.
4. **STOP.** Czekaj na wyraźne zatwierdzenie marki i planu publikacji.
5. Dopiero potem skład książki głównej z istniejących plików HARDSET v1.0 oraz osobnego podręcznika Continuous Bench Priority.
6. Oddaj próbki stron, a potem dopracowane publikacje; publikacja zewnętrzna wyłącznie na osobne polecenie.

## Zasady odniesienia

To materiał edukacyjny, nie indywidualna porada medyczna. Competition bench wymaga bezpiecznej asekuracji i zweryfikowania aktualnych przepisów federacji. 60 min to limit operacyjny, nie gwarancja: każdy prototyp treningu musi go przetestować na realnej siłowni.
