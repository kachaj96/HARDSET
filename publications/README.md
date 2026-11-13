# Publikacje HARDSET

| Katalog | Książka | Próbka |
|---|---|---|
| `hardset-v1/` | HARDSET. Controlled Brutality (metoda v1.0) | 9 stron, wydanie jasne i ciemne |
| `bench-priority-v1.1/` | HARDSET Powerbuilding. Continuous Bench Priority (szkic v1.2) | 10 stron, wydanie jasne i ciemne |

Źródłem jest `*/sample/source.html` (HTML z miejscami na logo, wykresy i ikony). Szablon i tokeny: `../brand/system/`. Wykresy: `charts.py` (dane z programu i walidatora). Zasady tekstu: `../brand/system/EDITORIAL_STANDARD.md`.

Budowanie (Python 3 z pyphen, Node, Playwright z Chromium):

```
NODE_PATH=$(npm root -g) python3 publications/build.py        # HTML i PDF, jasne i ciemne
python3 publications/build.py --html-only                      # tylko HTML
```

`build.py` podmienia znaczniki `{{logo}}`, `{{chart:...}}`, `{{icon:...}}`, dodaje polskie twarde spacje i miękkie dzielniki, zapisuje `sample.html` i `sample-dark.html` (pliki pochodne, poza repozytorium) i renderuje PDF. `render_pdf.js` przerywa pracę, jeśli fonty marki się nie załadowały.

Nic z tego katalogu nie jest opublikowane. Publikacja wymaga osobnej zgody właściciela.
