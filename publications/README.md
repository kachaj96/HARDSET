# Publikacje HARDSET

Dwie gotowe książki w PDF (język polski, B5 pionowo, wydanie jasne i ciemne):

| Książka | Plik (jasne) | Stron |
|---|---|---|
| HARDSET. Controlled Brutality (metoda v1.0) | `hardset-v1/HARDSET_Controlled_Brutality_PL.pdf` | 56 |
| HARDSET Powerbuilding. Continuous Bench Priority (v1.2) | `bench-priority-v1.1/HARDSET_Powerbuilding_Continuous_Bench_Priority_PL.pdf` | 29 |

Wydanie ciemne ma przyrostek `_dark`. Nic z tego katalogu nie jest opublikowane. Publikacja wymaga osobnej zgody właściciela.

## Źródła do edycji

- `<książka>/book/*.html`: części książki (`00_front` okładka, kolofon, spis, wstęp; `01`–`09` rozdziały; `a` aneksy; `y_matrix` matryca dowodów; `z_bib` bibliografia). Kolejność składu wynika z nazw plików.
- `hardset-v1/book/refs.json` i `make_bib.py`: dane bibliograficzne (REFERENCES.md i Crossref, 13 listopada 2026) i generator `z_bib.html`. Bibliografia Bench Priority: `bench-priority-v1.1/book/make_bib.py`.
- `charts.py`: wykresy SVG z danych programu i walidatora. `../brand/system/`: szablon i tokeny. Zasady tekstu: `../brand/system/EDITORIAL_STANDARD.md`.
- Znaczniki w częściach: `{{logo}}`, `{{mark}}`, `{{lockup}}`, `{{ruler}}`, `{{wavecover}}`, `{{icon:nazwa}}`, `{{chart:nazwa}}`, `{{pg:id}}` (numer strony w spisie).

## Budowanie

Wymagane: Python 3 z pyphen, Node z Playwright i Chromium, pdftotext (poppler).

```
NODE_PATH=$(npm root -g) python3 publications/build.py            # obie książki, jasne i ciemne
NODE_PATH=$(npm root -g) python3 publications/build.py --samples  # stare próbki 10-stronicowe
python3 publications/build.py --html-only                          # tylko HTML
```

`build.py` składa części, podmienia znaczniki, dodaje polskie twarde spacje i miękkie dzielniki, renderuje PDF dwa razy (pierwszy przebieg służy do ustalenia numerów stron w spisie treści) i zapisuje `book.html` i `book-dark.html` (pliki pochodne, poza repozytorium). `render_pdf.js` przerywa pracę, jeśli fonty marki się nie załadowały.

## Kontrole

`python3 brand/system/build_brand.py --check` (kontrasty, aktualność plików marki), `python3 -m unittest discover -s programs/continuous-bench-priority/tests` (reguły programu i arytmetyka). Skan fraz zakazanych: `brand/system/EDITORIAL_STANDARD.md`.
