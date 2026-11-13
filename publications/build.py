#!/usr/bin/env python3
"""Build HARDSET publication samples: placeholders, Polish typography, light and dark PDF.

For each <book>/sample/source.html:
  1. replaces {{logo}}, {{mark}}, {{lockup}}, {{ruler}}, {{wavecover}}, {{icon:NAME}}, {{chart:NAME}}
     (SVG is generated here from brand/system/logo and publications/charts.py);
  2. applies Polish typography: non-breaking spaces after single-letter words and before units,
     no line break inside numeric ranges, soft hyphens (pyphen, pl_PL) so justified text has no rivers;
  3. writes sample.html (light) and sample-dark.html, renders <book>-sample.pdf and <book>-sample-dark.pdf.

Run:  NODE_PATH=$(npm root -g) python3 publications/build.py [--html-only]
Needs: pyphen (soft hyphens; without it justified text gets gaps), fonttools only for brand/system/build_brand.py.
"""
import re
import subprocess
import sys
from pathlib import Path

try:
    import pyphen
except ImportError:
    pyphen = None

ROOT = Path(__file__).resolve().parent
LOGO_DIR = ROOT.parent / 'brand' / 'system' / 'logo'
sys.path.insert(0, str(ROOT))
import charts  # noqa: E402

BOOKS = ['hardset-v1', 'bench-priority-v1.1']
NBSP, SHY = ' ', '­'
SINGLE = re.compile(r'(?<![\wÀ-ſ])([aiouwzAIOUWZ]) (?=\S)')
UNITS = re.compile(r'(\d) (kg|%|min|s|mm|pt|RIR|RPE|powtórzeń|powtórzenia|serii|serie)\b')
RANGE = re.compile(r'\d[\d,]*–\d[\d,]*')
LONG = re.compile(r'(?<![A-Za-zÀ-ſ])[a-ząćęłńóśźż]{7,}(?![A-Za-zÀ-ſ])')
EN_WORDS = {'repetitions', 'reserve', 'exercise', 'training'}
VOID = {'br', 'hr', 'img', 'meta', 'link', 'input', 'path', 'rect', 'line', 'circle', 'polyline'}
NO_HYPHEN_TAGS = {'h1', 'h2', 'h3', 'h4', 'caption', 'th', 'cite', 'style', 'script', 'title', 'code', 'pre', 'svg', 'td'}
NO_HYPHEN_CLASSES = {'tg', 'doi', 'cover', 'nw', 'no', 'tablenote', 'principle', 'lead', 'bib', 'panel', 'stat', 'note', 'colophon', 'steps', 'two', 'chk', 'tl', 'toc', 'formula', 'quote', 'small'}
_dic = pyphen.Pyphen(lang='pl_PL', left=3, right=3) if pyphen else None


def fix_text(text):
    text = SINGLE.sub(lambda m: m.group(1) + NBSP, text)
    text = UNITS.sub(lambda m: m.group(1) + NBSP + m.group(2), text)
    return RANGE.sub(lambda m: '<span class="nw">' + m.group(0) + '</span>', text)


def hyphenate(text):
    if not _dic:
        return text
    return LONG.sub(lambda m: m.group(0) if m.group(0) in EN_WORDS else _dic.inserted(m.group(0), SHY), text)


def polish_typography(html):
    """Text nodes only: never markup, <style> or <svg> (charts keep their labels exactly)."""
    out, pos, stack = [], 0, []
    for m in re.finditer(r'<!--.*?-->|<style.*?</style>|<svg.*?</svg>|<[^>]+>', html, re.S):
        text = html[pos:m.start()]
        text = fix_text(text)
        if stack and not any(sk for _, sk in stack):
            text = hyphenate(text)
        out.append(text)
        tag = m.group(0)
        out.append(tag)
        pos = m.end()
        t = re.match(r'<(/?)([a-zA-Z0-9]+)([^>]*)>', tag)
        if t and not tag.startswith(('<!--', '<style', '<svg')):
            closing, name, rest = t.group(1), t.group(2).lower(), t.group(3)
            if closing:
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][0] == name:
                        del stack[i:]
                        break
            elif name not in VOID and not rest.rstrip().endswith('/'):
                cls = set(re.findall(r'class="([^"]*)"', rest)[0].split()) if 'class="' in rest else set()
                skip = name in NO_HYPHEN_TAGS or bool(cls & NO_HYPHEN_CLASSES)
                stack.append((name, skip))
    out.append(fix_text(html[pos:]))
    return ''.join(out)


def logo_file(name, cls):
    s = (LOGO_DIR / name).read_text(encoding='utf-8')
    return s.replace('<svg xmlns="http://www.w3.org/2000/svg"', f'<svg class="{cls}"', 1)


def fill_placeholders(html, dark):
    suffix = '-on-dark' if dark else ''
    html = html.replace('{{logo}}', logo_file(f'hardset-wordmark{suffix}.svg', 'logo'))
    html = html.replace('{{mark}}', logo_file(f'hardset-mark{suffix}.svg', 'mark'))
    html = html.replace('{{lockup}}', logo_file(f'hardset-powerbuilding-lockup{suffix}.svg', 'lockup'))
    html = html.replace('{{ruler}}', charts.ruler()).replace('{{wavecover}}', charts.wave_cover())
    html = re.sub(r'\{\{icon:(\w+)\}\}', lambda m: charts.icon(m.group(1)), html)
    html = re.sub(r'\{\{chart:(\w+)\}\}', lambda m: charts.CHARTS[m.group(1)](), html)
    return html


def themed(html, dark):
    if not dark:
        return html
    html = html.replace('<html lang="pl">', '<html lang="pl" class="hs-dark">', 1)
    return html.replace('</head>', '<style>@page { background: #101214; }</style>\n</head>', 1)


def main():
    html_only = '--html-only' in sys.argv
    for book in BOOKS:
        d = ROOT / book / 'sample'
        src = (d / 'source.html').read_text(encoding='utf-8')
        for dark in (False, True):
            name = 'sample-dark' if dark else 'sample'
            html = polish_typography(fill_placeholders(src, dark))
            (d / f'{name}.html').write_text(themed(html, dark), encoding='utf-8')
            if not html_only:
                pdf = d / f'{book}-{name}.pdf'
                subprocess.run(['node', str(ROOT / 'render_pdf.js'), str(d / f'{name}.html'), str(pdf)], check=True)


if __name__ == '__main__':
    main()
