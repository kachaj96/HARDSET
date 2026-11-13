#!/usr/bin/env python3
"""Build HARDSET publication samples: Polish typographic fixes + PDF render.

For each <book>/sample/source.html:
  1. non-breaking spaces after single-letter Polish words (a, i, o, u, w, z) and
     between numbers and units, so these never end a line;
  2. writes <book>/sample/sample.html;
  3. renders <book>/sample/<book>-sample.pdf via render_pdf.js (Node + Playwright).

Run: python publications/build.py [--html-only]\nNeeds: pyphen (pip install pyphen) for Polish soft hyphens, otherwise justified text gets gaps.
"""
import re
import subprocess
import sys
from pathlib import Path

try:
    import pyphen
except ImportError:  # soft hyphens are optional; justified text needs them
    pyphen = None

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


SHY = '\u00ad'
_dic = pyphen.Pyphen(lang='pl_PL', left=3, right=3) if pyphen else None
LONG = re.compile(r'(?<![A-Za-zÀ-ſ])[a-ząćęłńóśźż]{7,}(?![A-Za-zÀ-ſ])')  # lowercase words only: skips English terms (Hard Set, Priority...)
VOID = {'br', 'hr', 'img', 'meta', 'link', 'input'}
NO_HYPHEN_TAGS = {'h1', 'h2', 'h3', 'h4', 'caption', 'th', 'cite', 'style', 'script', 'title', 'code', 'pre'}
NO_HYPHEN_CLASSES = {'ev', 'doi', 'cover', 'runhead', 'rpe', 'nw', 'no', 'tablenote', 'tag', 'principle', 'lead', 'bib'}


EN_WORDS = {'repetitions', 'reserve', 'exercise', 'training'}  # English terms used inside Polish sentences


def hyphenate(text):
    if not _dic:
        return text
    return LONG.sub(lambda m: m.group(0) if m.group(0) in EN_WORDS else _dic.inserted(m.group(0), SHY), text)


def polish_typography(html):
    """Non-breaking spaces + soft hyphens, applied to text nodes only (never markup, <style>)."""
    out, pos, stack = [], 0, []   # stack of (tag, skip_hyphen)
    for m in re.finditer(r'<!--.*?-->|<style.*?</style>|<[^>]+>', html, re.S):
        text = fix_text(html[pos:m.start()])
        if stack and not any(sk for _, sk in stack):
            text = hyphenate(text)
        out.append(text)
        tag = m.group(0)
        out.append(tag)
        pos = m.end()
        t = re.match(r'<(/?)([a-zA-Z0-9]+)([^>]*)>', tag)
        if t and not tag.startswith('<!--'):
            closing, name, rest = t.group(1), t.group(2).lower(), t.group(3)
            if closing:
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][0] == name:
                        del stack[i:]
                        break
            elif name not in VOID and not rest.rstrip().endswith('/'):
                cls = set(re.findall(r'class="([^"]*)"', rest)[0].split()) if 'class="' in rest else set()
                skip = name in NO_HYPHEN_TAGS or bool(cls & NO_HYPHEN_CLASSES)
                skip = skip or (name == 'table' and 'data' in cls and 'text' not in cls)
                stack.append((name, skip))
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
