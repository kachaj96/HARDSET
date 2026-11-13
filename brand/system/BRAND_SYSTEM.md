# HARDSET Brand System v1.0

Kierunek: Industrial editorial (decyzja M-7 w `../DECISIONS.md`). System obsługuje książki, programy i proste strony. Nie obejmuje aplikacji Repsmith, która ma własną markę (M-8).

Jedynym źródłem wartości jest `tokens.json`. `build_brand.py` generuje z niego `tokens.css` i logotypy. `python3 build_brand.py --check` sprawdza, czy pliki wygenerowane są aktualne. Wymaga fontTools.

## 1. Zasada

Marka wygląda jak dokumentacja techniczna dobrego warsztatu: papier, tusz, tabela, linijka. Dekoracja musi coś mierzyć albo porządkować. Jeśli element nie niesie informacji, wypada.

Nie stosujemy: gradientów, zdjęć stockowych, sylwetek kulturystów, płomieni, wykrzykników, efektów „grunge”, ikon mięśni, zaokrąglonych kart z cieniem.

## 2. Logo

### Warianty

| Plik | Użycie |
|---|---|
| `logo/hardset-wordmark.svg` | Podstawowy. HARD w kolorze ink, SET w oxide, na papierze. |
| `logo/hardset-wordmark-on-ink.svg` | Na ciemnym tle. SET w `oxide-on-ink`. |
| `logo/hardset-wordmark-mono-ink.svg` | Jeden kolor, druk czarno-biały, pieczątka. |
| `logo/hardset-wordmark-mono-paper.svg` | Jeden kolor na ciemnym albo kolorowym tle serii. |
| `logo/hardset-mark.svg` | Znak H\|S: favicon, stopka, grzbiet, awatar. |
| `logo/hardset-mark-on-ink.svg`, `-mono-ink.svg` | Znak na ciemnym tle i w jednym kolorze. |
| `logo/hardset-powerbuilding-lockup.svg` | Seria HARDSET Powerbuilding, podtytuł w slate. |
| `logo/hardset-powerbuilding-lockup-on-slate.svg` | Lockup serii na okładce w kolorze slate. |

Litery są zamienione na krzywe (IBM Plex Sans Condensed Bold), więc logo nie zależy od zainstalowanych fontów.

### Pole ochronne i minimalne rozmiary

- Pole ochronne: wysokość litery H z każdej strony. Wewnątrz nie stoi żaden tekst ani krawędź obrazu.
- Wordmark: co najmniej 18 mm szerokości w druku, 96 px na ekranie.
- Znak H|S: co najmniej 6 mm w druku, 16 px na ekranie. Poniżej 24 px pionowa kreska może się zlewać, więc trzeba sprawdzić wynik na docelowym ekranie.
- Lockup serii: co najmniej 40 mm albo 220 px, inaczej podtytuł przestaje być czytelny.

### Czego nie robimy z logo

- Nie zmieniamy podziału kolorów (zawsze HARD neutralnie, SET w akcencie albo całość jednym kolorem).
- Nie rozstrzeliwujemy, nie pochylamy, nie obrysowujemy, nie dodajemy cienia.
- Nie składamy słowa HARDSET innym krojem i nie piszemy go „HardSet” ani „Hard Set”, gdy chodzi o markę. „Hard Set” (dwa słowa) to termin metody, czyli seria robocza.
- Nie łączymy logo HARDSET z logo Repsmith w jeden znak.

## 3. Kolor

| Token | Wartość | Rola |
|---|---|---|
| `ink` | #1F2524 | Tekst, linie tabel, tło trybu ciemnego. |
| `paper` | #F2EFE8 | Tło stron, tekst na kolorze. |
| `oxide` | #A64B32 | Akcent HARDSET: SET w logo, numery rozdziałów, RPE, oznaczenie „do decyzji”. |
| `oxide-text` | #963F29 | Oxide w małym tekście na tle `tint`. |
| `slate` | #355D6D | Seria HARDSET Powerbuilding, odnośniki do źródeł, heurystyki. |
| `moss` | #56634A | Oznaczenie „Badanie”, rezerwowy kolor kolejnej serii. |
| `rule` | #C9C3B6 | Cienkie linie podziału. |
| `tint` | #E7E2D8 | Wyróżnione wiersze, ramki „do decyzji”. |
| `muted` | #5E6461 | Paginacja, podpisy, żywa pagina. |
| `ink-raised` | #2A3130 | Powierzchnie w trybie ciemnym. |
| `paper-muted` | #B9B4A9 | Tekst drugorzędny w trybie ciemnym. |
| `oxide-on-ink`, `slate-on-ink` | #D9805F, #8FB5C4 | Akcenty w trybie ciemnym. |

Proporcja na stronie: mniej więcej 90% papier i tusz, akcent tylko tam, gdzie oznacza coś konkretnego. Jedna strona nie potrzebuje więcej niż jednego koloru akcentu poza oznaczeniami dowodów.

### Kontrast (WCAG 2.x, policzony z tokenów)

| Para | Kontrast | Dopuszczalne |
|---|---|---|
| ink / paper | 13,56 | każdy tekst |
| slate / paper | 6,22 | każdy tekst |
| moss / paper | 5,58 | każdy tekst |
| muted / paper | 5,27 | każdy tekst |
| oxide / paper | 4,98 | każdy tekst |
| oxide-text / tint | 5,35 | każdy tekst |
| muted / tint | 4,69 | każdy tekst |
| oxide / tint | 4,43 | tylko tekst duży (od 14 pt pogrubiony albo 18 pt) |
| paper / slate | 6,22 | każdy tekst |
| paper / oxide | 4,98 | każdy tekst |
| oxide-on-ink / ink | 5,34 | każdy tekst |
| slate-on-ink / ink | 7,10 | każdy tekst |
| ink / oxide | 2,72 | nie używać do tekstu |

## 4. Typografia

| Rola | Krój | Użycie |
|---|---|---|
| Display | IBM Plex Sans Condensed 600/700 | Logo, tytuły, nagłówki, etykiety, kolofon. |
| Tekst | Source Serif 4 400/400i/600 | Tekst ciągły, tabele opisowe, bibliografia. |
| Dane | IBM Plex Mono 400/500 | Liczby w tabelach, ciężary, RPE, wzory, oznaczenia dowodów, paginacja. |

Wszystkie trzy rodziny są na licencji SIL Open Font License 1.1 (pliki `fonts/OFL-*.txt`). Można je osadzać w PDF i EPUB oraz rozpowszechniać. Nazwa „Plex” jest zastrzeżona (Reserved Font Name), więc nie wolno zmieniać tych plików i dalej nazywać ich Plex. Pliki `woff2` są podzbiorami latin i latin-ext, wystarczają dla polskiego i angielskiego.

Skala (pt, druk A5): 7,5 podpis · 8,5 mały · 10 tekst · 11,5 lead · 12 h4 · 14 h3 · 18 h2 · 26 h1 · 44 display. Ekran używa skali px z `tokens.json`.

Zasady:
- Tekst ciągły jest justowany (decyzja T-1), ostatnia linia akapitu do lewej. Chromium nie ma polskiego słownika dzielenia, więc `publications/build.py` wstawia miękkie dzielniki słownikiem pyphen (pl_PL): wyrazy od 7 liter, minimum 3 znaki z każdej strony, bez nagłówków, tabel danych, odnośników, bibliografii i terminów angielskich. Kolofon, podpisy i okładki są wyrównane do lewej. Przy każdym składzie czytamy strony pod kątem szerokich spacji i złych podziałów.
- Wersaliki tylko w krótkich etykietach, zawsze z rozstrzałem 0,08 do 0,14 em.
- Kursywa tylko dla tytułów czasopism, terminów obcych i zdania-zasady pod tytułem rozdziału.
- Liczby w tabelach zawsze w kroju Mono, wyrównane do prawej.
- Polskie reguły w `EDITORIAL_STANDARD.md`.

## 5. Książka (A5)

Szablon: `book.css`. Format 148 × 210 mm, marginesy: góra 16, dół 18, wewnętrzny 18, zewnętrzny 16 mm. Strony lustrzane, paginacja na zewnętrznym brzegu w kroju Mono.

Struktura:
- `section.cover`: okładka bez marginesów i paginacji.
- `section.plain`: kolofon bez paginacji.
- `section.chapter-open`: nowa strona, numer rozdziału 44 pt w oxide, tytuł 22 pt, jedno zdanie-zasada kursywą.
- `.runhead`: żywa pagina na pierwszej stronie sekcji. Chromium nie obsługuje `position: running()`, więc na kolejnych stronach rozdziału żywej paginy nie ma. Do wydania pełnego to ograniczenie zostaje albo zmieniamy silnik składu.

Komponenty:
- Oznaczenia klas twierdzeń: `.ev.study` (Badanie, moss), `.ev.decision` (Decyzja HARDSET, ink), `.ev.heuristic` (Heurystyka, slate), `.ev.exception` (Wyjątek siłowy, oxide), `.ev.hypothesis` (Hipoteza programu, slate, linia przerywana), `.ev.open` (Do decyzji, wypełnione oxide). Znaczenie klas opisuje `EDITORIAL_STANDARD.md`.
- `.aside.evidence`: komentarz do badania z ograniczeniami. `.aside.open`: sprawa nierozstrzygnięta. W wydaniu publicznym `.open` nie może wystąpić.
- `ul.defs`: lista definicji (termin, opis).
- `table.data`: tabela danych. `tr.hl` wyróżnia wiersz, `.rpe` oznacza wysiłek, `td.r` wyrównuje liczby do prawej, `td.nw` blokuje łamanie.
- `ol.bib`: bibliografia z numerem R## albo kreską dla źródeł spoza matrycy dowodów.

### Okładki serii

| Seria | Tło | Logo | Motyw |
|---|---|---|---|
| HARDSET (książka metody) | paper | wordmark dwukolorowy | siatka 12 obszarów Fixed Core |
| HARDSET Powerbuilding | slate | lockup on-slate | wykres prawdziwych danych programu, np. fali T1 do T4 |
| Kolejna seria | moss | lockup z nazwą serii | dane tego programu |

Motyw okładki zawsze pokazuje treść książki. Żadnych zdjęć ani ilustracji sylwetki.

## 6. Wykresy i tabele

- Słupek, linia albo tabela. Bez wykresów kołowych, 3D i gradientów.
- Jeden kolor danych (paper albo ink) plus oxide dla jednej wyróżnionej wartości.
- Etykiety wartości bezpośrednio przy danych, bez legendy, jeśli da się jej uniknąć.
- Tabela ma podpis (`caption`) nad sobą i źródło albo objaśnienie skrótów pod sobą.
- Przykładowe liczby zawsze z podaną bazą, np. „przykład dla bazy 120 kg”.

## 7. Produkty cyfrowe

Dotyczy stron WWW, PDF do czytania na ekranie, EPUB i ewentualnych prostych narzędzi HARDSET. Nie dotyczy Repsmith.

- `tokens.css` udostępnia role semantyczne `--hs-bg`, `--hs-fg`, `--hs-fg-muted`, `--hs-surface`, `--hs-line`, `--hs-accent`, `--hs-data`, `--hs-evidence`. Komponenty używają ról, nie surowych kolorów.
- Tryb ciemny włącza się z `prefers-color-scheme: dark` albo `[data-theme="dark"]`. Tło ink, powierzchnie ink-raised, akcenty w wariantach `-on-ink`.
- Cele dotykowe co najmniej 44 × 44 px. Fokus widoczny: obrys 2 px w kolorze akcentu z odstępem 2 px.
- Promień zaokrąglenia: 0 dla bloków i tabel, 4 px dla pól formularza (`--hs-radius-field`). `--hs-radius-device` (22 px) służy tylko do makiet ekranu telefonu. Bez cieni. Hierarchię budują linie i odstępy.
- Ikony liniowe, 1,5 px, kwadratowe zakończenia. Ikona tylko wtedy, gdy przyspiesza rozpoznanie. Ikona nigdy nie występuje bez etykiety tekstowej.
- Ruch: tylko przejścia stanu do 150 ms. `prefers-reduced-motion` wyłącza wszystkie.
- Liczby treningowe (ciężar, powtórzenia, RPE) zawsze w kroju Mono.

## 8. HARDSET i Repsmith

Repsmith to osobna aplikacja z własną paletą, krojem Barlow i ikoną. Gdy książka wspomina aplikację, pisze jej nazwę zwykłym tekstem, bez logo. Wspólna strona lub materiał pokazuje oba znaki obok siebie, oddzielone polem ochronnym, nigdy połączone. Integracja lub zmiana wyglądu Repsmith to osobna decyzja.

## 9. Pliki

```
brand/system/
  tokens.json        źródło wartości
  tokens.css         wygenerowane: zmienne CSS, role, tryb ciemny
  build_brand.py     generator i --check
  book.css           szablon publikacji A5
  fonts/             woff2 + fonts.css + licencje OFL
  logo/              9 plików SVG
  BRAND_SYSTEM.md    ten dokument
  EDITORIAL_STANDARD.md
```
