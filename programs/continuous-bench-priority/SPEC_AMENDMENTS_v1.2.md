# Continuous Bench Priority: zmiany do wersji 1.2 (szkic)

Decyzje właściciela z 2026-11-13. Pakiet `handoff/` zostaje bez zmian. Ten plik opisuje, co od v1.2 obowiązuje zamiast odpowiednich fragmentów v1.1. Funkcje i testy: `rules_v1_2.py`, `tests/test_amendments_v1_2.py`. Zmiany nie dotykają zatwierdzonej metody HARDSET v1.0.

| # | Decyzja | Skutek |
|---|---|---|
| D-3 | Dodać regułę w górę dla serii wielopowtórzeniowych | sekcja 1 |
| D-4 | Próg zmiany bazy w powtórzeniach, nie w procentach | sekcja 2 |
| D-5 | „PB” zmienia nazwę na **baza fali** (angielskie: Wave Base, skrót WB) | sekcja 3 |
| D-6, D-7, D-1, D-2 | otwarte | `../../brand/DECISIONS.md` |

## 1. D-3: korekta w górę (klasa: Hipoteza programu)

Powód (N-1): przy bazie ostrożniejszej niż prawdziwe 1RM serie wielopowtórzeniowe wypadają lżej niż docelowe RPE. Przeliczenie wzorem Epleya przy bazie równej 1RM daje dla back-offów poniedziałku i serii piątku (T1, T2) od pół punktu do około 2 punktów RPE poniżej celu. Singiel jest skalibrowany dobrze.

Reguła: po pierwszej serii roboczej ćwiczenia wielopowtórzeniowego porównujesz RPE z dolną granicą celu.

- różnica mniejsza niż 1 pełny punkt RPE: bez zmian;
- różnica 1 pełny punkt: następna seria o około 2,5% więcej;
- różnica 2 punkty i więcej: o około 5% więcej (limit);
- zaokrąglenie do najbliższego kroku talerzy (domyślnie 2,5 kg), przy ciężarach poniżej 80 kg można przyjąć 1,25 kg; korekta nigdy nie jest mniejsza niż jeden krok.

Warunki: technika w normie i prędkość sztangi nie spada w trakcie serii. Reguła nie dotyczy singla, serii AMRAP ani tygodnia 4 (lżejszy tydzień jest zaplanowany, wyjątek W-4). Korekta nie zmienia bazy fali. Jeśli ta sama korekta w górę wychodzi w dwóch kolejnych treningach tego samego typu, następny zaczynasz od ciężaru skorygowanego. Jeśli korekta w górę dotyczy większości serii wielopowtórzeniowych w całej fali, baza jest za niska i sprawdzasz ją regułą z sekcji 2.

Skąd 2,5% na punkt: wzór Epleya daje 2,6–2,9% ciężaru na jeden punkt RPE dla 3–6 powtórzeń przy RPE 6–8 (test `test_step_per_point_is_below_epley_estimate_for_wave_rep_ranges`). Przyjęto dolną granicę, bo błąd szacowania RIR (Refalo i wsp. 2024, około 0,65 powtórzenia) jest tego samego rzędu co jeden punkt. Limit 5% na raz to decyzja ostrożnościowa, nie wynik badania. Liczby wymagają sprawdzenia na prawdziwych dziennikach.

## 2. D-4: zmiana bazy fali (klasa: Hipoteza programu)

Baza rośnie o krok (przykład: 2,5 kg), gdy zachodzą oba warunki:

1. seria kontrolna (AMRAP T3) dała co najmniej jedno powtórzenie więcej niż w poprzedniej fali przy tym samym ciężarze i RIR; jeśli ciężar się zmienił, porównuje się e1RM, a różnica musi wynosić co najmniej ciężar/30 (przy 100 kg około 3,3 kg);
2. singiel z poniedziałku tygodnia 3 został wykonany w planowanym RPE, bez obniżania ciężaru.

Rozstrzyga to N-5: odniesieniem jest poprzednia seria kontrolna, nie sama baza. W pierwszej fali nie ma odniesienia, więc baza zostaje, a wynik zapisujesz jako punkt wyjścia. To doprecyzowanie jest moje i wymaga potwierdzenia.

Pozostałe reguły v1.1 (obserwuj, sprawdź regenerację, „nierozstrzygnięte”, zmiana tylko przed T1) bez zmian. Zamiast progu „2–3%” obowiązuje kryterium powtórzenia. Przykład z handoffu (100×5 → 100×6 @9) spełnia je co do grosza: różnica e1RM 3,33 kg równa się ciężar/30.

Krok +2,5 kg nadal jest przykładowy (N-7): to 2,1% przy bazie 120 kg i 1,25% przy 200 kg.

## 3. D-5: nazwa

„PB” w trójboju znaczy rekord życiowy. Program mówi **baza fali**. Zapis osobnych liczb: 1RM (zaliczony wynik zawodniczy), e1RM (szacunek z serii kontrolnej), baza fali (liczba do procentów).
