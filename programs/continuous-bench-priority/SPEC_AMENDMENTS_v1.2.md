# Continuous Bench Priority: zmiany do wersji 1.2 (szkic)

Decyzje właściciela z 2026-11-13. Pakiet `handoff/` zostaje bez zmian. Ten plik opisuje, co od v1.2 obowiązuje zamiast odpowiednich fragmentów v1.1. Funkcje i testy: `rules_v1_2.py`, `tests/test_amendments_v1_2.py`. Zmiany nie dotykają zatwierdzonej metody HARDSET v1.0.

| # | Decyzja | Skutek |
|---|---|---|
| D-3 | Dodać regułę w górę dla serii wielopowtórzeniowych | sekcja 1 |
| D-4 | Próg zmiany bazy w powtórzeniach, nie w procentach | sekcja 2 |
| D-5 | „PB” zmienia nazwę na **baza fali** (angielskie: Wave Base, skrót WB) | sekcja 3 |
| D-1 | Serie wyciskania zawodniczego liczone osobno jako serie siłowe, poza ledgerem Hard Sets | sekcja 4 |
| D-2 | (a): tylne aktony barków i pośladki mają w tym programie status Optional | sekcja 4 |
| D-6 | Lżejszy tydzień 4 wyciskania to nazwany wyjątek; reszta ćwiczeń bez luzowania | sekcja 4 |
| D-7 | Korekty techniczne: wycofane źródło i przykład B-2 | sekcja 5 |

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

## 4. D-1, D-2, D-6: status w ledgerze i granice programu

Program jest ułożony dla osoby, która trenuje **trzy razy w tygodniu po najwyżej 60 minut** (z rozgrzewką) i ma **priorytet w wyciskaniu leżąc**. Tego założenia nie wolno pominąć w żadnym planie opartym na tym programie.

- **D-1.** Serie wyciskania zawodniczego przy RPE 6–8 (zapas 2–4 powtórzeń) nie są liczone jako Hard Sets klatki w ledgerze hipertrofii. Są serią siłową i wchodzą do osobnego wiersza ledgera. Ekspozycje Chest dla hipertrofii wynikają z pozostałych serii zgodnych ze standardem Hard Set. Walidator liczy dziś wszystkie serie ćwiczeń, więc przed użyciem na planie z wyciskaniem zawodniczym trzeba oznaczyć te serie jako siłowe w danych wejściowych albo sprawdzić ledger ręcznie.
- **D-2 (a).** Rear Delts i Glutes mają status **Optional** z intencją Maintenance: bez wymaganego minimum ekspozycji. To skutek limitu 60 minut przy priorytecie wyciskania, a nie ocena ich ważności. Kto chce je rozwinąć, dodaje po jednym ćwiczeniu kosztem czasu albo zmienia program. Walidator dla przykładowego tygodnia z tymi statusami: PASS (`analysis/example_week_validator_output_d2a.json`). To jest wynik strukturalny, nie ocena biomechaniczna ani medyczna.
- **D-6.** Lżejszy tydzień wyciskania (T4) jest zaplanowany z kalendarza i odstępuje od zasady HARDSET „deload z potrzeby” (wyjątek W-4). Wyjątek dotyczy wyłącznie wyciskania. Pozostałe ćwiczenia działają według zwykłych zasad HARDSET bez luzowania: dwie serie, RIR 1 i 0–1 przy bezpiecznym zakończeniu, progresja serii prowadzącej, regeneracja z potrzeby.

## 5. D-7: korekty techniczne

- Usunięte źródło: Hughes, Peiffer, Scott (2020), wycofane (B-3). Nie występuje w książce.
- Przykład B-2: back-off w poniedziałek T3 przy bazie 120 kg to 97,5–102,5 kg, nie „około 100–102,5”.
- Singiel T3 przy bazie 120 kg: 110–112,5 kg.
Pakiet `handoff/` zostaje bez zmian. Poprawki są w książce i w tym pliku.
