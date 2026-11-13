# 07 — Walidator programu (wymagany przed wydaniem)

## Główne kryteria

1. **Source of truth:** wszystkie twierdzenia o oryginalnym HARDSET oparte na rzeczywistych plikach repo. Żadnego dopisywania rozdziałów z pamięci tego pakietu.
2. **Cel:** performance competition bench nadrzędny, hipertrofia kontynuowana; nie obiecuj maksymalizacji obu równocześnie.
3. **Fala:** T1→T2→T3→T4→T1, wzrost intensywności w T1–T3, T4 lżejszy bench, stałe akcesoria warunkowo.
4. **AMRAP:** T3 pt @9, docelowo 4–7 reps, pauza, 1 RIR, jedna seria, brak „grindu” z technicznym załamaniem.
5. **e1RM:** rzeczywiste przykłady muszą zgadzać się arytmetycznie; nie oznaczaj e1RM jako zmierzonego 1RM.
6. **PB:** zmieniany dopiero przed kolejną falą, nigdy automatycznie o pełny wzrost e1RM.
7. **%/RPE:** % to zakres, RPE to limit; sporządź testy wartości i realistycznych zakresów.
8. **Program 3×60:** 11+12+12=35 serii; każda jednostka uwzględnia pełne 60 minut. Jeśli brak pewności, oznacz „do potwierdzenia w praktyce”.
9. **Ćwiczenia:** 6 patternów, izolacje i triceps 2× bezpośrednio; transparentne braki (calves, adductors, trunk).
10. **HARDSET:** domyślne dwie ciężkie serie i Qualified Progression przy bezpiecznych akcesoriach; competition bench ma odrębne reguły.
11. **Bezpieczeństwo:** bez 0 RIR w bench; rack z safeties; na maksymalnym teście odpowiednia asekuracja; oddzielna procedura dla bólu/urazu.
12. **Źródła:** weryfikacja w recenzowanych artykułach i oficjalnym regulaminie, a nie w blogach marketingowych.
13. **Brand gate:** nie kończyć wizerunku / ebooków bez wyraźnej decyzji właściciela i zbadania ryzyk nazw.

## Znane niepewności

- %1RM↔RPE u konkretnych osób ma dużą wariancję; nie wymuszać idealnego mapowania.
- Epley z poprawką RIR jest heurystyką; wzór nie może ustanawiać samodzielnego „progresu naukowego”.
- Dodatkowa praca tricepsa i pec deck może w pewnych warunkach pogarszać piątkowy bench lub sam test.
- Trening nóg i bieganie mogą interferować z regeneracją; czas i zakres zależą od trenującego.
- 1 ekspozycja Vertical Pull może być wystarczająca w programie o tym celu, ale nie twierdź, że jest optymalna dla każdej osoby.
- 4-tygodniowa fala to organizacja pracy, nie uniwersalny okres adaptacji biologicznej.
- Stała objętość akcesoriów jest regułą domyślną, a nie zakazem lżejszych tygodni przy potrzebie regeneracji.

## Minimum walidacji technicznej

- Program po imporcie jest w osobnym katalogu, bez uszkodzenia dziewięciu rozdziałów głównych.
- Parser JSON akceptuje `machine/bench_wave.json`.
- `python machine/e1rm.py --self-test` przechodzi poprawnie.
- Przykładowe procenty i obciążenia zaokrąglają się do 2,5 kg.
- Nie ma błędów typu „11+12+12=34”.
- Test stanu przed/po testowym module nie prowadzi do podwójnego benchmarku.
- Bibliografia przypisuje źródła do rzeczywistych twierdzeń i notuje datę dostępu.

## Reguła konfliktu z oryginalnym HARDSET

Jeżeli programowy punkt odbiega od zatwierdzonego HARDSET (np. 1×1, RPE 7, lżejszy tydzień), wyjaśnij to jako **specyficzny wyjątek powerbuildingowy**, a nie ciche przepisanie oryginalnej metody. Jeśli zdaniem Claude Code nie da się pogodzić go z metodologią, opisz i przedstaw właścicielowi wybór.
