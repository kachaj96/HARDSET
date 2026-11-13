# Publikacje HARDSET

| Katalog | Książka | Stan |
|---|---|---|
| `hardset-v1/` | HARDSET. Controlled Brutality (metoda v1.0) | próbka 10 stron, czeka na akceptację |
| `bench-priority-v1.1/` | HARDSET Powerbuilding. Continuous Bench Priority v1.1 | próbka 10 stron, czeka na akceptację |

Źródłem jest `*/sample/source.html`. Szablon i tokeny: `../brand/system/`. Zasady tekstu: `../brand/system/EDITORIAL_STANDARD.md`.

Budowanie (Python 3, Node, Playwright z Chromium):

```
NODE_PATH=$(npm root -g) python3 publications/build.py          # HTML + PDF
python3 publications/build.py --html-only                        # tylko HTML
```

`build.py` dodaje polskie twarde spacje i zapisuje `sample.html` (plik pochodny, poza repozytorium). `render_pdf.js` przerywa pracę, jeśli fonty marki się nie załadowały.

Nic z tego katalogu nie jest opublikowane. Publikacja wymaga osobnej zgody właściciela.
