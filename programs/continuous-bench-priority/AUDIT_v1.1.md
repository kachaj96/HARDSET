# Continuous Bench Priority v1.1 — audyt etapu 1

**Data:** 2026-11-13  
**Przedmiot:** pakiet `HARDSET_Bench_Priority_v1.1_Handoff.zip` (13 plików, SHA-256 `59d35447384bcec9bd134a3a88311ece6588052e7068842c026078fb18e4d664`), skopiowany bez zmian do `handoff/`.  
**Punkt odniesienia:** zatwierdzony HARDSET v1.0 w tym repozytorium (`chapters/01–09`, `appendices/`, `research/` w wersji 1.1.0, `validation/`).  
**Zakres:** zgodność z HARDSET, arytmetyka, spójność %/RPE, reguły AMRAP/e1RM/PB, fala czterotygodniowa, przykład 3 × 60 min, moduły testu i zawodów, źródła.  
**Status:** nic w pakiecie nie zostało zmienione. Poniższe punkty są propozycjami do decyzji właściciela.

Oznaczenia: **B** błąd, **N** niejasność, **D** decyzja do podjęcia, **W** wyjątek względem HARDSET v1.0 wymagający jawnego opisu.

---

## 1. Relacja do HARDSET v1.0

Pakiet sam definiuje się jako osobny program oparty na HARDSET, a nie nową wersję rozdziałów. To się zgadza z jego treścią. Poniżej punkty, w których program odchodzi od zatwierdzonych zasad.

| # | Zasada HARDSET | Bench Priority | Ocena |
|---|---|---|---|
| W-1 | Ch01 §3: Lead Set ~1 RIR, Supporting Set 0–1 RIR | competition bench @6–8, czyli ~2–4 RIR; AMRAP @9 | Wyjątek siłowy, zgodny z celem (performance), ale musi być nazwany. Zob. D-1. |
| W-2 | Ch03 §2: 2 Hard Sets domyślnie, 1 seria wymaga uzasadnienia | 1×1 single w poniedziałek | Zgodne, jeśli uzasadnienie (ekspozycja na intensywność, umiejętność) jest zapisane. |
| W-3 | Ch05 §2: Lead-Set Progression | bench prowadzony falą % + Programming Baseline | Wyjątek. Ch08 §8.1 dopuszcza periodyzację przy celu siłowym, więc mieści się w metodzie jako świadomy wybór. Akcesoria zostają przy Ch05. |
| W-4 | Ch05 §7 i CLAUDE.md: deload z potrzeby, bez kalendarza deloadów | T4: lżejszy bench co 4 tygodnie, z góry | Wyjątek. To zaplanowane odciążenie **jednego boju**, nie deload całego ciała. Musi być opisane wprost jako odstępstwo od reguły „z potrzeby”. |
| W-5 | Ch02 §5: Priority/Standard ≥ 2 ekspozycje, S+S niewystarczające | Rear Delts i Glutes mają tylko bodziec pośredni | Konflikt. Zob. B-1. |
| — | Ch02: „Pattern-Led, Muscle-Verified” | 6 wzorców jako warstwa programowania, 12 obszarów jako audyt | Zgodne z duchem rozdziału 02. |
| — | Ch04: bezpieczny stop przy 0 RIR | bench nigdy 0 RIR, rack z safeties | Zgodne, a nawet ostrożniejsze. |
| — | Ch07: dziennik nie dowodzi hipertrofii | e1RM opisany jako szacunek, nie 1RM | Zgodne. |

## 2. Błędy

**B-1. Pokrycie Rear Delts i Glutes (walidator HARDSET: FAIL).**
Przykładowy tydzień przepuszczony przez `validation/validator.py` (wejście i wynik w `analysis/`):
- Rear Delts: 0 wiarygodnych ekspozycji (wiosłowania dają co najwyżej S?);
- Glutes: tylko S+S (RDL i reverse lunge).

Pakiet (02, akapit o izolacjach) sam przyznaje, że to bodziec pośredni. Brakuje tylko formalnej decyzji: albo te obszary są Optional, albo mają jawny wyjątek, albo dostają ćwiczenie z P. Zob. D-2.

**B-2. Przykład Pn T3 back-off w `03_BENCH_WAVE.md`.**
Pakiet podaje „~100–102,5 kg” dla PB 120. 82–85% z 120 kg to 98,4–102 kg, po zaokrągleniu do 2,5 kg: **97,5–102,5 kg**. Pojedynczy przykład T3 („~110 kg”) też ma zakres 110–112,5 kg.

**B-3. Wycofane źródło w `references/RESEARCH_LINKS.md`, pozycja 6.**
Hughes, Peiffer, Scott, *Estimating Repetitions in Reserve in Four Commonly Used Resistance Exercises* (PMID 33337690, DOI 10.1519/JSC.0000000000003865) jest w PubMed oznaczona jako *Retracted Publication* (nota DOI 10.1519/JSC.0000000000003977). `research/RESEARCH_AUDIT.md` HARDSET v1.0 wprost zakazuje cytowania tej pracy. Do usunięcia; zamiennik: Refalo et al. 2024 (poz. 5 pakietu) oraz R19 i R20 z bibliografii HARDSET.

## 3. Arytmetyka i struktura (sprawdzone, OK)

- Tabela e1RM (100 kg @9): 116,7 / 120,0 / 123,3 / 126,7 kg. Zgadza się.
- `machine/e1rm.py --self-test`: 3 testy OK. `machine/bench_wave.json`: poprawny JSON, wartości zgodne z tabelami w `03`.
- Zaokrąglenia przykładów PB 120 (poza B-2): zgodne.
- Serie: 11 + 12 + 12 = 35; serie bench 3 + 2 + 2 = 7. Zgadza się.
- Budżety czasu w `05`: każdy dzień sumuje się do 60 minut.
- Fala: intensywność rośnie T1 → T3 w każdym slocie; T4 jest lżejszy od T1 w każdym slocie.
- Testy: `tests/test_bench_priority.py` (15 testów, w tym test, który utrwala B-2).

## 4. Spójność procentów i RPE

Kontrola heurystyczna wzorem Epleya (liczba powtórzeń do upadku przy danym %1RM). To przybliżenie: meta-regresja Nuzzo i wsp. (Sports Med 2024;54:303–321, DOI 10.1007/s40279-023-01937-7) pokazuje dużą zmienność między osobami. Zakładam PB = prawdziwe 1RM.

| Slot | Cel RPE | RPE wynikające z % |
|---|---|---|
| Pn T1 single | 7 | 6,9–7,7 |
| Pn T3 single | 8 | 8,0–8,7 |
| Pn T1 back-off 2×5 | 7 | 5,0–6,5 |
| Pn T2 back-off 2×4 | 7–8 | 5,5–7,0 |
| Pt T1 2×6 | 7 | 4,9–6,5 |
| Pt T4 2×5 | 6–7 | 2,1–5,0 |

**N-1.** Single są dobrze skalibrowane. Serie wielopowtórzeniowe wypadają w procentach wyraźnie lżej niż cel RPE, a ponieważ PB z założenia jest ostrożny (niższy od prawdziwego 1RM), rozjazd jest jeszcze większy. Pakiet ma regułę tylko w jedną stronę („RPE powyżej celu → zmniejsz o 2,5–5%”). Brakuje reguły dla sytuacji, w której RPE jest wyraźnie poniżej celu. Zob. D-3.

**N-2.** AMRAP przy 82,5% PB: przy PB = 1RM daje ~5,4 powtórzenia @9 (w środku celu 4–7). Przy PB = 95% prawdziwego 1RM daje ~7,3, przy 90% ~9,4, czyli powyżej celu. Pakiet przewiduje korektę ciężaru w następnej fali, ale zależność od „ostrożności” PB warto opisać w książce wprost.

**N-3.** Paused bench liczony od PB competition. Dłuższa pauza obniża liczbę powtórzeń, więc RPE będzie wyższe niż dla tych samych % w competition bench. Reguła „RPE ma pierwszeństwo” to pokrywa; w książce warto to nazwać.

## 5. Reguły PB (Programming Baseline)

**N-4. Próg „~2–3% lub więcej”.** Przykład z pakietu (100×6 → e1RM 123,3 przy PB 120) to wzrost 2,78%. Przy progu 2% przechodzi, przy progu 3% nie. Zob. D-4.

**N-5. Punkt odniesienia.** Reguła 4 mówi o wzroście, reguła 2 każe porównać z ostatnim benchmarkiem. Nie jest jasne, czy wzrost liczy się względem PB, czy względem poprzedniego e1RM.

**N-6. Rozdzielczość sygnału.** Przy 100 kg jedno dodatkowe powtórzenie to ~3,3 kg e1RM, czyli ~2,8% PB 120. Reguła w praktyce znaczy „o jedno powtórzenie więcej niż ostatnio przy tym samym ciężarze i RIR”. Błąd szacowania RIR jest tego samego rzędu (Refalo i wsp. 2024), więc wymóg potwierdzenia przez poniedziałkowy single jest istotny i powinien zostać obowiązkowy.

**N-7. Krok +2,5 kg** to 2,1% przy PB 120 i 1,25% przy PB 200. Pakiet zaznacza, że krok jest przykładowy. W książce potrzebna jest reguła dla innych poziomów siły (np. krok procentowy zaokrąglany do talerzy).

**N-8. Nazwa „PB”.** W trójboju „PB” powszechnie znaczy *personal best*. Użycie tego skrótu dla *Programming Baseline* będzie mylić czytelników. Zob. D-5.

## 6. Przykład 3 × 60 min

- Walidator HARDSET (model: serie, przerwy, 1,5 min na zmianę stanowiska, 5 min bufora, 9 min rozgrzewki) szacuje Pn 42, Śr 45, Pt 46 min. Model nie uwzględnia ładowania sztangi ani czekania na sprzęt, więc budżety z pakietu (po 60 min) są ostrożniejsze. Obie metody mieszczą się w limicie.
- **N-9.** Piątek ma 2 minuty na przejścia przy sześciu ćwiczeniach. To nierealne; pakiet sam to sygnalizuje. Do potwierdzenia na siłowni.
- Pakiet poprawnie oznacza, że 60 minut nie jest jeszcze zweryfikowane w praktyce.

## 7. Moduły testu i zawodów

- Moduł A (test 1RM) jest spójny z falą: brak wyciskania 1–3 dni przed testem, zakaz łączenia z AMRAP T3, moduł zastępuje fragment fali. Nie ma ryzyka podwójnego benchmarku, jeśli ta reguła zostanie zachowana.
- Moduł B (zawody): single do @8,5–9 to wyjątek w obrębie modułu. Do jawnego opisu.
- Źródło taperingu (Winwood i wsp., Sports Med 2026, DOI 10.1007/s40279-026-02500-w) zweryfikowane: dotyczy **samoopisu praktyk sportowców**. Podaje taper zwykle 5–9 dni i redukcję objętości o **~40–45%** (pakiet pisze 40–50%). Bench przed zawodami ostatni raz 3–5 dni wcześniej, co zgadza się z modułem A.
- **N-10.** Regulamin IPF (poz. 1) nie był jeszcze weryfikowany. Do sprawdzenia przy składzie książki, z datą dostępu.

## 8. Źródła z `RESEARCH_LINKS.md`

| Poz. | Praca | Wynik weryfikacji (PubMed / Crossref) |
|---|---|---|
| 2 | Pelland i wsp., Sports Med 2026 | OK, DOI 10.1007/s40279-025-02344-w |
| 3 | Currier i wsp., ACSM Position Stand 2026 | OK, to samo co R01 w bibliografii HARDSET |
| 4 | „Meta-analysis maximal repetitions by %1RM (2024)” | Nuzzo, Pinto, Nosaka, Steele, Sports Med 2024;54:303–321 (online 2023). W pakiecie brak autorów |
| 5 | Refalo i wsp., JSCR 2024 | OK, DOI 10.1519/JSC.0000000000004653 |
| 6 | Hughes, Peiffer, Scott 2020 | **wycofana** (B-3) |
| 7 | Winwood i wsp., Sports Med 2026 | OK, z korektą ~40–45% |
| 8 | Currier i wsp., BJSM 2023 | OK, DOI 10.1136/bjsports-2023-106807 |
| 1, 9–11 | IPF, EUIPO, Repsmith, HardSet | do etapu 2 (marka) i etapu 4 (regulamin) |

Żadna nota o korekcie ani zastrzeżeniu wydawcy nie dotyczy pozycji 2–5, 7, 8 na dzień 2026-11-13.

## 9. Decyzje do podjęcia

- **D-1.** Czy serie competition bench przy @6–8 liczą się jako Hard Sets i ekspozycje P dla Chest w ledgerze HARDSET? Jeśli tak, Chest ma 9 serii P tygodniowo, z czego 7 przy 2–4 RIR. Propozycja: liczyć jako ekspozycje siłowe, a w ledgerze hipertrofii oznaczać osobno.
- **D-2.** Rear Delts i Glutes: (a) Optional, (b) Standard z jawnym wyjątkiem, (c) dodać ćwiczenie z P (np. reverse pec deck, hip thrust) kosztem czasu.
- **D-3.** Dodać regułę symetryczną dla %/RPE: jeśli pierwsza seria jest ≥ 1 RPE poniżej celu przy dobrej technice, kolejna seria +2,5 kg. Albo zostawić % jako sufit i akceptować lżejsze serie.
- **D-4.** Próg aktualizacji PB: 2%, 3%, czy reguła w powtórzeniach (np. „≥ 1 powtórzenie więcej przy tym samym ciężarze i RIR, potwierdzone przez single”).
- **D-5.** Zmiana skrótu „PB” na nazwę, która nie koliduje z *personal best*.
- **D-6.** Akceptacja W-4 (lżejszy bench w T4) jako nazwanego wyjątku od reguły „deload z potrzeby”.
- **D-7.** Usunięcie wycofanego źródła (B-3) i poprawka przykładu (B-2) w wersji 1.1.1 specyfikacji.
