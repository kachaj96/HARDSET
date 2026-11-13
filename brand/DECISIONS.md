# Decyzje marki

Rejestr decyzji właściciela. Każda zmiana poniższych ustaleń wymaga nowego wpisu, a nie edycji starego.

## 2026-11-13 · Etap 2: architektura i kierunek

| # | Decyzja | Źródło |
|---|---|---|
| M-1 | Odbiorca: osoby trenujące samodzielnie. | odpowiedź właściciela, pkt 1 |
| M-2 | Języki: polski i angielski, najpierw polski. | pkt 2 |
| M-3 | Autor na okładkach i w stopce: Adrian Drożdżyński. | pkt 3 |
| M-4 | Dystrybucja bezpłatna. | pkt 4 |
| M-5 | Podtytuł „Controlled Brutality” zostaje. | pkt 6 |
| M-6 | Architektura C: HARDSET jest marką parasolową książek i programów. Bez nazwy „Kreska”. Seria programów: „HARDSET Powerbuilding”. | „C, nie kreska, normalnie HARDSET” |
| M-7 | Kierunek wizualny 1, Industrial editorial, bez domieszek innych kierunków. | „Czysty kierunek” + wybór „1” |
| M-8 | Aplikacja Repsmith zostaje osobną marką, bez zmiany nazwy i wyglądu. | „Nie” |

### Przyjęte ryzyka nazwy

Stan sprawdzony 2026-11-13, szczegóły w `BRAND_ANALYSIS_v0.1.md`. To przegląd internetowy, a nie opinia prawna.

- „HardSet Coaching” (hard-set.com) działa w tej samej branży pod podobną nazwą.
- Domena hardset.com jest zarejestrowana od 1996 roku.
- Rejestrów znaków towarowych nie sprawdzono maszynowo (TMview zwracał błąd 503). Przed jakimkolwiek zgłoszeniem znaku albo płatną dystrybucją potrzebne jest wyszukiwanie przez rzecznika patentowego.
- Repsmith ma w sklepach dwie obce aplikacje o tej samej nazwie. Dotyczy to marki aplikacji, nie HARDSET.

Bezpłatna dystrybucja zmniejsza to ryzyko, ale go nie usuwa.

## 2026-11-13 · Etap 3: zmiany techniczne w systemie

| # | Zmiana | Powód |
|---|---|---|
| S-1 | Dodany token `oxide-text` #963F29, tylko dla małego tekstu na tle `tint`. | Oxide na tint ma kontrast 4,43:1, poniżej progu WCAG AA 4,5:1. Nowy odcień ma 5,35:1. Kolor marki się nie zmienia. |

## 2026-11-13 · Etap 3: odpowiedzi właściciela na próbki

| # | Decyzja | Wdrożenie |
|---|---|---|
| L-1 | Licencja: wszelkie prawa zastrzeżone, bezpłatne udostępnianie (opcja 2). | kolofony próbek; treść zapisu do potwierdzenia, to nie jest porada prawna |
| D-3 | Reguła w górę dla serii zbyt lekkich: 2,5% na punkt RPE, limit 5%. | `programs/continuous-bench-priority/SPEC_AMENDMENTS_v1.2.md`, `rules_v1_2.py`, testy |
| D-4 | Próg zmiany bazy w powtórzeniach (zaakceptowane). | jw. |
| D-5 | Nowa nazwa zamiast „PB”: baza fali (Wave Base, WB). | próbka Bench Priority |
| T-1 | Tekst w e-bookach justowany, z dzieleniem wyrazów. | `book.css`, `publications/build.py` (pyphen) |
| T-2 | Nowa kolorystyka (czerń, dwa kolory + akcent, industrial) i nowe logo: wybór spośród min. 3 makiet. | `brand/explorations-v2/` |

## Otwarte (do decyzji właściciela)

- Wybór stylu i logo (T-2). Po wyborze Brand System zostanie przebudowany, a kontrasty przeliczone.
- Decyzje treningowe D-1, D-2, D-6, D-7 z `programs/continuous-bench-priority/AUDIT_v1.1.md`.
