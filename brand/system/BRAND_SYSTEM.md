# HARDSET Brand System v2.0

Styl: modułowy raport, czerń i biel z jednym zgaszonym zielonym akcentem (Eukaliptus). Wybrane przez właściciela 2026-11-13 (`../DECISIONS.md`: T-3, T-4, T-5). System obsługuje książki, programy i proste strony. Nie obejmuje aplikacji Repsmith, która ma własną markę.

Jedynym źródłem wartości jest `tokens.json`. `build_brand.py` generuje z niego `tokens.css`, `fonts/fonts.css`, logo i raport kontrastów. `python3 build_brand.py --check` kończy się błędem, gdy pliki są nieaktualne albo któraś para kolorów nie spełnia progu kontrastu. Wymaga fontTools (`pip install fonttools`).

## 1. Zasada

Strona wygląda jak dobrze złożony raport techniczny: siatka modułów, liczba najpierw, wykres obok tekstu, ciemny panel „Co z tego wynika”. Dekoracja musi coś mierzyć albo porządkować. Nie stosujemy gradientów, zdjęć stockowych, sylwetek, ikon mięśni, cieni ani zaokrąglonych kart.

## 2. Logo

Wordmark HARDSET jest narysowany z konturów Archivo Expanded ExtraBold, z rozstrzałem 0,24 em. Dwie kreski pod napisem to Lead Set (pełna długość) i Supporting Set (58%). Znak to litera H z tymi samymi kreskami na kwadracie. Litery są zamienione na krzywe, więc logo nie zależy od fontu.

| Plik | Użycie |
|---|---|
| `logo/hardset-wordmark.svg` | Podstawowy, na jasnym tle (ink, kreski w `accent-text`). |
| `logo/hardset-wordmark-on-dark.svg` | Na czerni (paper, kreski w `accent`). |
| `logo/hardset-wordmark-mono-ink.svg`, `-mono-paper.svg` | Jeden kolor: druk czarno-biały, pieczątka, tłoczenie. |
| `logo/hardset-mark.svg`, `-on-dark.svg`, `-mono-ink.svg` | Znak: stopka okładki, awatar, favicon. |
| `logo/hardset-powerbuilding-lockup.svg`, `-on-dark.svg` | Seria HARDSET Powerbuilding: wordmark bez kresek i napis POWERBUILDING pod spodem. |

- **Pole ochronne:** wysokość litery H z każdej strony.
- **Minimalne rozmiary:** wordmark 24 mm w druku i 120 px na ekranie, znak 7 mm i 24 px, lockup serii 40 mm i 200 px. Na tych rozmiarach nie sprawdzono jeszcze optycznie dwóch kresek, przy 24 px znaku mogą się zlewać. Sprawdzić przed użyciem na favicon.
- **Nie robimy:** nie zmieniamy rozstrzału ani proporcji kresek, nie pochylamy, nie obrysowujemy, nie dodajemy cienia, nie składamy marki innym krojem. „HARDSET” to marka, „Hard Set” (dwa słowa) to seria robocza w metodzie.
- Nie łączymy logo HARDSET z logo Repsmith w jeden znak.

## 3. Kolor

| Token | Wartość | Rola |
|---|---|---|
| `ink` | #101214 | Tekst, tło wydania ciemnego, ciemny panel w jasnym. |
| `paper` | #F3F4F4 | Tło wydania jasnego, tekst na czerni. |
| `steel` | #B9C0C4 | Podstawa wykresów, wtórne wypełnienia. |
| `line`, `tint` | #CBD0D3, #E3E6E8 | Linie tabel, wyróżnione wiersze, ramka wzoru. |
| `muted` | #5F686D | Tekst drugorzędny na jasnym. |
| `accent` | #54877A | Eukaliptus: wypełnienia i duże elementy. Nie do małego tekstu. |
| `accent-text` | #436C62 | Akcent jako mały tekst na jasnym i na `tint`. |
| `accent-on-panel` | #5C9485 | Akcent jako mały tekst na czerni i na ciemnym panelu. |
| `panel`, `panel-line`, `ink-line`, `ink-muted`, `ink-tint` | #1D2124, #4B5359, #30363A, #9AA3A8, #1A1E21 | Wydanie ciemne: panel, linie, tekst drugorzędny, wyróżnione wiersze. |

Proporcje: około 90% czerń, biel i szarości. Akcent służy do jednej wyróżnionej wartości na wykresie (np. T3), do wskaźników liczbowych, znaczników i krawędzi cytatu.

### Kontrast (policzony przez `build_brand.py`, WCAG 2.x)

| Para | Kontrast | Dopuszczalne |
|---|---|---|
| ink / paper | 17,04 | każdy tekst |
| muted / paper | 5,17 | każdy tekst |
| accent-text / paper | 5,35 | każdy tekst |
| accent-text / tint | 4,71 | każdy tekst |
| paper / panel | 14,71 | każdy tekst |
| ink-muted / ink, / panel | 7,31, 6,31 | każdy tekst |
| accent-on-panel / panel | 4,66 | każdy tekst |
| accent-on-panel / ink | 5,39 | każdy tekst |
| accent / ink | 4,58 | wypełnienia i duży tekst; mały tekst używa `accent-on-panel` |
| accent / paper | 3,72 | tylko elementy graficzne (wykres, znacznik), nie tekst |

Żaden kolor średniej jasności nie da 4,5:1 jednocześnie na czerni i bieli, bo nie ma takiej wartości. Dlatego akcent ma trzy role: wypełnienie, tekst na jasnym i tekst na ciemnym.

## 4. Typografia

| Rola | Krój | Użycie |
|---|---|---|
| Tytuły | Archivo 800, szerokość 125%, wersaliki, rozstrzał 0,04 em | Okładki i tytuł serii. |
| Nagłówki | Archivo 800, szerokość 112% | Tytuły rozdziałów (24 pt), nagłówki sekcji (15 pt). |
| Etykiety | Archivo 600–700, szerokość 125%, wersaliki, rozstrzał 0,08–0,16 em | Żywa pagina, podpisy tabel, `h3`, `h4`. |
| Tekst | Archivo 400, szerokość 100% | Tekst ciągły 9,3/13,6 pt. |
| Liczby | IBM Plex Mono 400/500 | Tabele, wskaźniki, jednostki, znaczniki klas twierdzeń, odnośniki do źródeł. |

Archivo i IBM Plex Mono są na licencji SIL OFL 1.1 (`fonts/OFL-*.txt`). Archivo jest fontem zmiennym (szerokość 62–125%, grubość 100–900), więc jeden plik daje wszystkie użyte warianty. Pliki są podzbiorami latin i latin-ext, wystarczają dla polskiego i angielskiego. `fonts/Archivo-800-expanded.ttf` służy tylko do rysowania logo.

Skala (pt, B5): 6,5 podpis · 7,5 mały · 9,3 tekst · 10,8 lead · 15 h2 · 24 h1 · 40 display. Skala ekranowa w px: `tokens.json`.

Zasady:
- Tekst ciągły jest justowany (ostatni wiersz akapitu do lewej). Chromium nie ma polskiego słownika dzielenia, więc `publications/build.py` wstawia miękkie dzielniki (pyphen, `pl_PL`): wyrazy od 7 liter, minimum 3 znaki z każdej strony, bez nagłówków, tabel, paneli, odnośników, bibliografii i terminów angielskich. Panele, podpisy, wskaźniki i kolofon są wyrównane do lewej bez dzielenia.
- Wersaliki tylko w etykietach i tytułach okładek, zawsze z rozstrzałem.
- Liczby w tabelach w Mono, kolumny liczbowe do prawej.
- Polskie reguły w `EDITORIAL_STANDARD.md`.

## 5. Książka (B5, pion)

Szablon: `book.css`. Format 176 × 250 mm, marginesy: góra 22, dół 24, wewnętrzny 20, zewnętrzny 16 mm. Strony lustrzane, numer strony na zewnętrznym brzegu w Mono, żywa pagina z nazwą rozdziału (strony nazwane `@page nazwa`, tekst w marginesie górnym).

Wydania: **jasne** (domyślne) i **ciemne** (klasa `hs-dark` na `<html>` oraz `@page { background: #101214 }`, robi to `build.py`). Oba z tego samego źródła HTML.

Elementy:
- `.cover` (okładka, strona `cover` bez marginesów), `.plain` (kolofon bez numeracji), `.chap` (otwarcie rozdziału: etykieta „Rozdział 03”, tytuł, zdanie-zasada z krawędzią w akcencie).
- `.stats` (trzy wskaźniki: liczba, jednostka, opis), `.tl` (oś czasu), `.steps` (kroki z ikoną), `.formula`, `.quote`, `.note`.
- `.panel` (ciemny panel „Co z tego wynika”, pełna szerokość) i `.with-side` (treść po lewej, panel 54 mm po prawej; blok niepodzielny). **Panele nie pływają** (`float`), bo w druku zostawiają dziury i nachodzą na ramki.
- `.tg` (znaczniki klas twierdzeń): `study` (Badanie, obrys), `decision` (Decyzja HARDSET, obrys mocny), `heuristic` (kropkowany), `exception` (Wyjątek siłowy, w akcencie), `hypothesis` (Hipoteza programu, przerywany), `open` (Do decyzji, wypełniony; w wydaniu publicznym nie może wystąpić). Różnią się kreską, nie kolorem, więc działają w druku czarno-białym.
- `table.dt` (czarny nagłówek, wiersz wyróżniony `tr.hl`, kolumny `.r`), warianty `.text` i `.mx` (macierz ekspozycji).
- Wykresy: SVG z klasami `.chart` i ról kolorystycznych, generowane z danych w `publications/charts.py`. Słupek, linia, wskaźnik kołowy, oś czasu. Bez wykresów kołowych wielosektorowych, 3D i gradientów. Wartości podpisane bezpośrednio, jeden element w akcencie.
- Okładki: wielki tytuł Archivo Expanded z logo, własna grafika z treści (skala RIR w HARDSET, wykres fali w Bench Priority). Żadnych zdjęć ani sylwetek.

Stałe ograniczenia składu w Chromium: `@page` nie rozwiązuje zmiennych CSS (tło strony jest wpisane literalnie), nie ma `position: running()` (nagłówek robimy stronami nazwanymi), nie ma polskiego dzielenia (pyphen).

## 6. Produkty cyfrowe

Dotyczy stron WWW, PDF do czytania na ekranie i prostych narzędzi HARDSET. Nie dotyczy Repsmith.

- `tokens.css` udostępnia role: `--hs-bg`, `--hs-fg`, `--hs-panel`, `--hs-panel-fg`, `--hs-mid`, `--hs-line`, `--hs-muted`, `--hs-tint`, `--hs-a` (akcent), `--hs-at` (tekst akcentowy), `--hs-ap` (tekst akcentowy na panelu). Komponenty używają ról, nie surowych kolorów.
- Tryb ciemny: `prefers-color-scheme: dark`, `[data-theme="dark"]` albo klasa `.hs-dark`. Wydanie ciemne jest równorzędne z jasnym, a nie odwróceniem kolorów.
- Cele dotykowe co najmniej 44 × 44 px, widoczny fokus (obrys 2 px, odstęp 2 px).
- Promień: 0 dla bloków, 4 px dla pól formularza. Bez cieni. Hierarchię budują linie, odstępy i panele.
- Ikony liniowe, kreska 1,8 w siatce 24, zakończenia kwadratowe, nigdy bez etykiety.
- Ruch tylko jako przejście stanu do 150 ms, wyłączany przez `prefers-reduced-motion`.
- Liczby treningowe (ciężar, powtórzenia, RPE) zawsze w Mono.

## 7. HARDSET i Repsmith

Repsmith to osobna aplikacja z własną paletą, krojem Barlow i ikoną. Gdy książka wspomina aplikację, pisze jej nazwę zwykłym tekstem, bez logo. Wspólny materiał pokazuje oba znaki obok siebie, nigdy połączone.

## 8. Pliki

```
brand/system/
  tokens.json            źródło wartości
  tokens.css             wygenerowane: zmienne, role, tryb ciemny
  build_brand.py         generator, raport kontrastów i --check
  book.css               szablon publikacji B5
  fonts/                 Archivo (woff2 + ttf logo), IBM Plex Mono, fonts.css, licencje OFL
  logo/                  9 plików SVG
  BRAND_SYSTEM.md        ten dokument
  EDITORIAL_STANDARD.md  zasady tekstu
```
