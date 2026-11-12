# HARDSET Builder — specyfikacja v0.1 (do akceptacji)

**Status:** projekt, etap 1 z 4. Kod powstaje dopiero po akceptacji tego dokumentu.
**Zakres:** narzędzie osobiste, po polsku, cele: hipertrofia i siła.
**Źródło reguł:** rozdziały 01–09 tego repozytorium. Specyfikacja niczego w nich nie zmienia.

## 1. Cel

Prowadzony kreator, w którym układasz plan HARDSET samodzielnie, a narzędzie pilnuje reguł i na bieżąco pokazuje, co jest spełnione, co warunkowe, a co blokuje plan. Po zatwierdzeniu plan przechodzi do dziennika z progresją Lead-Set i pomiarami.

Narzędzie **nie** układa planu za Ciebie. Decyzje wymagające osądu (`validation/RULE_CATALOG.md`, kolumna „Necessary manual judgment”) zostają Twoje. Narzędzie je nazywa, ale ich nie zgaduje.

## 2. Architektura

| Warstwa | Plik / miejsce | Rola |
|---|---|---|
| Reguły (źródło) | `chapters/`, `appendices/`, `research/` | bez zmian |
| Biblioteka ćwiczeń | `library/exercises.json` | zamknięta lista ćwiczeń z przeglądniętymi tagami P/S |
| Silnik reguł | `tools/builder/engine.js` | deterministyczny port `validation/validator.py` + logika Lead-Set i faz |
| Testy zgodności | `validation/tests/parity_cases/*.json` + test w Pythonie i w Node | te same przypadki muszą dać ten sam status, ledger i czas w obu silnikach |
| Interfejs | artifact (HTML) budowany z plików repozytorium | kreator + dziennik |
| Twoje dane | baza artifactu | plany, wpisy, pomiary; **nie trafiają do repozytorium** |

Brak AI w pętli decyzji. Wyjaśnienia w interfejsie to stałe teksty pomocy z odwołaniem do rozdziału.

## 3. Przepływ kreatora

| Krok | Co robisz | Co robi narzędzie | Źródło |
|---|---|---|---|
| 1. Profil | cele, doświadczenie, ostatnia tolerowana objętość, dni, czas sesji i czy obejmuje rozgrzewkę, sprzęt, bezpieczeństwo, inne aktywności, pomiary | brak odpowiedzi w polach bezpieczeństwa blokuje planowanie 0 RIR i oznacza bramkę jako nierozstrzygniętą | Ch09 §9.1, §9.2 |
| 2. Priorytety | Priority / Standard / Optional i Development / Maintenance dla 12 obszarów; Functional Notes; Functional Overrides | brak domyślnych priorytetów; przy ≥5 obszarach Priority pokazuje ostrzeżenie, że priorytet traci znaczenie | Ch02 §6–7, Ch08 §8.3 |
| 3. Dawka wyjściowa | docelowe P sets i ekspozycje na obszar | pokazuje etykietę z Appendix A wyłącznie informacyjnie; nie wylicza dawki | Ch06 §6.4, App. A |
| 4. Sesje | liczba sesji, nazwy, odstępy | podpowiada konfiguracje z tabeli Ch06 §6.6 jako punkt wyjścia | Ch06 §6.6 |
| 5. Ćwiczenia | wybór z biblioteki, liczba serii, zakres, RIR, przerwa, supersety | 2 serie domyślnie, 1 lub 3 wymagają uzasadnienia; RIR < 1 tylko przy `safe_exit`; ćwiczenie spoza biblioteki tylko z ręcznym P/S oznaczonym jako niezweryfikowane | Ch01, Ch03, Ch04 |
| 6. Walidacja na żywo | - | ledger P/S, ekspozycje, czas sesji, lista findings z odwołaniem do rozdziału, status | Ch02 §8, Ch09 |
| 7. Focus Block (opcjonalnie) | cel siłowy, fazy, zakresy i RIR na fazę, test | oznacza jako odstępstwo od Continuous Progression wymagające akceptacji | Ch08 §8.1, §8.4 |
| 8. Akceptacja | 4 potwierdzenia przeglądu: dopasowanie do celu, mechanika P/S, bezpieczeństwo ćwiczeń, regeneracja | bez nich maksymalny status to CONDITIONAL | Ch09 §9.7 |
| 9. Dziennik | wpisy serii, pomiary | podpowiedzi progresji (jak obecny dziennik), harmonogram pomiarów i przeglądów, statusy wyników | Ch05, Ch07 |

## 4. Automatyczne czy Twoja decyzja

| Reguła | Narzędzie | Ty |
|---|---|---|
| 12 obszarów Fixed Core, Overrides jawne | sprawdza | wybierasz priorytety |
| P/S na ćwiczeniu | bierze z biblioteki | zatwierdzasz bibliotekę; poza nią przypisujesz ręcznie |
| S? nie liczy się do ekspozycji, max 1 ekspozycja na sesję | liczy | - |
| ≥2 ekspozycje dla Priority/Standard, S+S niewystarczające | sprawdza | akceptujesz jawne wyjątki |
| 2 serie domyślnie, 1/3 z uzasadnieniem | sprawdza obecność uzasadnienia | oceniasz, czy uzasadnienie ma sens |
| 0 RIR tylko przy bezpiecznym stopie | sprawdza flagę | fizycznie weryfikujesz stop na sprzęcie |
| Czas sesji | szacuje (model jak w walidatorze) | sprawdzasz w realnych sesjach |
| Dawka wyjściowa | pokazuje etykietę informacyjną | decydujesz (Baseline + Response) |
| Progresja Lead-Set | podpowiada po wpisach | oceniasz porównywalność wykonania |
| Ocena wyników (Ch07) | przypomina terminy, zbiera pomiary | nadajesz status: Not Assessed / Inconclusive / Supported Progress / Concern |

## 5. Biblioteka ćwiczeń

**Rekord:**

| Pole | Znaczenie |
|---|---|
| `id` | stały identyfikator |
| `name_pl`, `name_en` | nazwa |
| `family` | Compound Pattern / Targeted Function (Ch02 §2) |
| `movement_tag` | jeden główny tag ruchu |
| `equipment`, `variant` | sprzęt i wariant (np. kąt ławki, chwyt) |
| `stimulus` | mapa obszar → P / S / S? |
| `functional_notes` | np. „proste kolano”, „akcent na górną część klatki” |
| `safe_exit` | `true` / `false` / `conditional` z warunkiem (np. „safety bars ustawione”) |
| `rir_floor_default` | najniższy domyślny RIR (np. 1 dla wolnych ciężarów bez bezpiecznego stopu) |
| `rep_template`, `rest_sec`, `seconds_per_set` | wartości domyślne (heurystyki z Ch03) |
| `review` | `proposed` / `approved` + data |

**Zakres v1:** ~60–80 ćwiczeń. Zawiera wszystkie ćwiczenia z Twoich obecnych planów, maszyny i wyciągi na każdy obszar, warianty bench pressu (paused, touch-and-go, close-grip, incline). Przysiad i martwy ciąg w wersji klasycznej są w bibliotece jako opcja, oznaczone `rir_floor_default: 1`.

**Proces:** przygotowuję tagi jako `proposed`, Ty przeglądasz tabelę i zatwierdzasz lub poprawiasz. Do `approved` trafia tylko to, co zatwierdzisz. Tylko ćwiczenia `approved` dają PASS. `proposed` daje najwyżej CONDITIONAL.

## 6. Silnik reguł

- `evaluate(plan)`: ten sam kontrakt wejścia i wyjścia co `validation/validator.py` (`validation/SCHEMA.md`).
- `leadSetDecision(prev, rx)`: logika z obecnego dziennika, łącznie z regułą kalibracji („ciężar wyraźnie za lekki”).
- Fazy Focus Block jako dane planu, nie zakodowane w silniku.
- **Zgodność:** każdy przypadek z `validation/tests/` jest zapisany jako plik JSON i wykonywany przez oba silniki. Różnica w statusie, ledgerze lub czasie to błąd testu.

## 7. Dane i prywatność

- Plany, wpisy i pomiary tylko w bazie artifactu (prywatny).
- Repozytorium nie zawiera żadnych danych osobowych ani planów osobistych.
- Eksport CSV / JSON z interfejsu.
- Twój obecny dziennik zostaje bez zmian. Przeniesienie wpisów do nowego narzędzia nastąpi dopiero po Twojej akceptacji.

## 8. Poza zakresem v1

Ebook; automatyczny dobór ćwiczeń; wyliczanie dawki; AI w decyzjach; wielu użytkowników; rehabilitacja i populacje kliniczne; pomiar zdjęć poza zapisem daty i warunków.

## 9. Kryteria akceptacji v1

1. Twój obecny plan (v1.1) da się odtworzyć z biblioteki i daje **PASS** z tym samym ledgerem i czasem co walidator w Pythonie.
2. Wszystkie przypadki zgodności przechodzą w obu silnikach.
3. Plan z celowo wprowadzonym błędem (np. 0 RIR bez bezpiecznego stopu, S+S dla Standard, przekroczony czas) daje ten sam FAIL co walidator.
4. Strona działa na telefonie bez przewijania w poziomie.

## 10. Pytania otwarte

1. Czy kreator ma obsługiwać kilka planów naraz (np. Twój i testowy), czy jeden aktywny plan z historią wersji?
2. Czy pomiary (masa, obwody, daty zdjęć) mają być w tym samym dzienniku co serie?
3. Czy po zatwierdzeniu narzędzia przenieść do niego obecny dziennik, czy prowadzić oba do końca 11-tygodniowego bloku?
