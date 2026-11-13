#!/usr/bin/env python3
"""Build HARDSET publication samples: Polish typographic fixes + PDF render.

For each <book>/sample/source.html:
  1. non-breaking spaces after single-letter Polish words (a, i, o, u, w, z) and
     between numbers and units, so these never end a line;
  2. writes <book>/sample/sample.html;
  3. renders <book>/sample/<book>-sample.pdf via render_pdf.js (Node + Playwright).

Run: python publications/build.py [--html-only]
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOKS = ['hardset-v1', 'bench-priority-v1.1']
NBSP = ' '
SINGLE = re.compile(r'(?<![\wÀ-ſ])([aiouwzAIOUWZ]) (?=\S)')
RANGE = re.compile(r'\d[\d,]*–\d[\d,]*')
UNITS = re.compile(r'(\d) (kg|%|min|s|mm|pt|RIR|RPE|powtórzeń|powtórzenia|serii|serie)\b')


def fix_text(text):
    text = SINGLE.sub(lambda m: m.group(1) + NBSP, text)
    text = UNITS.sub(lambda m: m.group(1) + NBSP + m.group(2), text)
    text = RANGE.sub(lambda m: '<span class="nw">' + m.group(0) + '</span>', text)  # keep 0–1, 2,5–5 on one line
    return text


def polish_typography(html):
    # apply only to text between tags, never inside markup or <style>
    out, pos = [], 0
    for m in re.finditer(r'<style.*?</style>|<[^>]+>', html, re.S):
        out.append(fix_text(html[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fix_text(html[pos:]))
    return ''.join(out)


def main():
    html_only = '--html-only' in sys.argv
    for book in BOOKS:
        d = ROOT / book / 'sample'
        src = (d / 'source.html').read_text(encoding='utf-8')
        (d / 'sample.html').write_text(polish_typography(src), encoding='utf-8')
        if not html_only:
            subprocess.run(['node', str(ROOT / 'render_pdf.js'), str(d / 'sample.html'),
                            str(d / f'{book}-sample.pdf')], check=True)


if __name__ == '__main__':
    main()
