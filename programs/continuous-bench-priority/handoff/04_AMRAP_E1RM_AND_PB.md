# 04 — AMRAP, e1RM i aktualizacja Programming Baseline

## Co faktycznie mierzymy

AMRAP rejestruje: obciążenie, liczbę prawidłowych powtórzeń, ocenę RIR/RPE, technikę i warunki. To mierzalny benchmark **powtarzany w podobnych okolicznościach**, ale wartość e1RM jest **szacunkiem**, nie potwierdzonym 1RM.

## Standard testu T3 (piątek)

- Standard competition bench: jednakowe ustawienie, chwyt, pauza na każdym powtórzeniu i brak odbicia.
- Stała rozgrzewka, 4–5 minut odpoczynku przed próbą, bez wcześniejszej trudnej jedynki tego dnia.
- Domyślnie 82,5% PB, z wyborem obciążenia zapewniającego **około 4–7 prawidłowych powtórzeń** na @9 (1 RIR). Ten przedział jest tylko wskazówką. Za ciężko/za lekko? Zmień benchmark load w kolejnej fali.
- Zakończ przy około jednym poprawnym powtórzeniu w zapasie albo wcześniej, gdy zanikają technika i kontrola. Nigdy nie dąż do celowego nieudanego powtórzenia.
- Bezpieczny rack, właściwe safeties; przy trudnych próbach odpowiednia asekuracja.
- Nagraj, zanotuj rezultat; nie próbuj kolejnego AMRAP w tym samym dniu dla „poprawienia odczytu”.

## Wzór roboczy

`e1RM_Epley_RIR = load_kg * (1 + (repetitions + estimated_RIR) / 30)`.

Uwaga: modyfikacja wzoru Epleya przez dodanie szacowanego RIR jest **heurystyką**, nie pomiarem o ustalonej precyzji. W publikacji trzeba przedstawić ją jako orientacyjne narzędzie sterowania treningiem. Różne formuły mogą dawać różne wyniki.

Dla 100 kg @9 (=1 RIR):

| Reps | e1RM (kg) |
|---|---:|
| 4 | 116,7 |
| 5 | 120,0 |
| 6 | 123,3 |
| 7 | 126,7 |

Jedno dodatkowe powtórzenie to tu ~3,3 kg w estymacji. Nie utożsamiaj tej różnicy z dokładną zmianą prawdziwego 1RM.

## Trzy osobne liczby

- `actual_1RM`: najlepszy **zaliczony** wynik competition bench wg aktualnych wymogów federacji (jeśli znany).
- `measured_e1RM`: wynik AMRAP w T3, z dokumentacją obciążenia i RIR.
- `PB`: Programming Baseline dla następnej fali, konserwatywna wartość programowa.

## Konserwatywny silnik decyzyjny (reguły robocze; NIE naukowe progi diagnostyczne)

1. Sprawdź, czy benchmark jest porównywalny (pauza, chwyt, RIR, kolejność ćwiczeń, aparat i obciążenie) oraz czy wykonano go bez problemów zdrowotnych.
2. Porównaj z ostatnim benchmarkiem; najlepiej ten sam ciężar, podobny RIR i warunki.
3. Zwróć uwagę na poniedziałkowy T3 single @8, ale nie traktuj jego e1RM jako niezależnego, obiektywnego testu: też bazuje na subiektywnym RPE.
4. Jeśli AMRAP sugeruje wzrost ~2–3% lub więcej **i** singiel/serie robocze wspierają trend, kandydat do PB = poprzednie PB + 2,5 kg (przykładowy krok dla typowego poziomu siły z rozmowy, do dostosowania).
5. Jeśli zmiana AMRAP <~2%, nie wymuszaj zwiększenia PB; zachowaj bazę, obserwuj kolejną falę.
6. Jeśli AMRAP spada, ale single stabilne, nie obniżaj PB automatycznie; skontroluj zmęczenie i warunki.
7. Jeśli AMRAP i single systematycznie pogarszają się, najpierw oceniaj regenerację/akcesoria/żywienie/technikę, potem rozważ zmianę PB.
8. Jeśli dane rozbieżne lub nieważne: **PB bez zmian**, notatka „inconclusive”.
9. Nowy PB zatwierdź **dopiero przed T1 następnej fali**. T4 wykonaj na starej bazie.

### Przykład dwóch fal

Fala A, PB 120: 100×5 @9 → e1RM 120. PB zostaje 120.

Fala B, PB 120: 100×6 @9 → e1RM 123,3. Jeśli single potwierdza trend, następna fala PB 122,5. Jeśli nie, PB bez zmian, obserwacja kolejnej fali.

## Protokół danych do dziennika

Minimalne pola: data, numer fali, tydzień, dzień, ćwiczenie, seria, ciężar, powtórzenia, RPE, RIR, pauza/technika OK?, film?, PB w chwili serii, e1RM (gdy dotyczy), uwagi o zmęczeniu. Osobno trend aktualnego PB i realne PR. Nie wykresuj oszacowanego e1RM jako „wynik 1RM”.

## Obiektywność

Fakt „100×6 przy poprawnej pauzie” jest obiektywnym wynikiem testu powtórzeniowego. `@9` i e1RM mają niepewność; wnioski formułuj warunkowo. Użytkownik nie ma obowiązku testować realnego 1RM co 4 tygodnie.
