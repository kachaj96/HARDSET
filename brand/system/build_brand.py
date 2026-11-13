#!/usr/bin/env python3
"""Generate brand/system/tokens.css, fonts.css, logo/*.svg and the contrast report from tokens.json.

Run:   python3 brand/system/build_brand.py          (writes files)
       python3 brand/system/build_brand.py --check  (fails if generated files are stale or a contrast rule breaks)
Needs fontTools (pip install fonttools): logo letters are outlined from the Archivo Expanded ExtraBold file.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
T = json.loads((HERE / 'tokens.json').read_text(encoding='utf-8'))
C = {k: v['value'] for k, v in T['color'].items()}


# ------------------------------------------------------------------ contrast
def lum(h):
    h = h.lstrip('#')
    r = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in r]
    return 0.2126 * r[0] + 0.7152 * r[1] + 0.0722 * r[2]


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# pair, minimum ratio, use
RULES = [
    ('ink', 'paper', 4.5, 'text on paper'), ('muted', 'paper', 4.5, 'secondary text on paper'),
    ('accent-text', 'paper', 4.5, 'accent text on paper'), ('accent-text', 'tint', 4.5, 'accent text on tint'),
    ('paper', 'ink', 4.5, 'text on ink'), ('ink-muted', 'ink', 4.5, 'secondary text on ink'),
    ('ink-muted', 'panel', 4.5, 'secondary text on panel'), ('paper', 'panel', 4.5, 'text on panel'),
    ('accent-on-panel', 'panel', 4.5, 'accent text on panel'), ('accent-on-panel', 'ink', 4.5, 'accent text on ink'),
    ('accent', 'ink', 4.5, 'accent fill and large text on ink'), ('accent', 'paper', 3.0, 'accent fill on paper (graphics only)'),
    ('ink', 'accent', 4.5, 'ink on accent fill'),
]


def contrast_report():
    rows = []
    for a, b, need, use in RULES:
        r = contrast(C[a], C[b])
        rows.append((a, b, r, need, use, r >= need))
    return rows


# ------------------------------------------------------------------ css
def build_css():
    lines = ['/* Generated from tokens.json by build_brand.py. Do not edit by hand. */', "@import url('fonts/fonts.css');", ':root{']
    for k, v in C.items():
        lines.append(f'  --hs-{k}:{v};')
    for k, v in T['font'].items():
        lines.append(f"  --hs-font-{k}:{v['value']};")
    for k, v in T['type-scale-px'].items():
        if k != '$description':
            lines.append(f'  --hs-size-{k}:{v}px;')
    for k, v in T['radius'].items():
        lines.append(f'  --hs-radius-{k}:{v};')
    # semantic roles, light edition
    light = dict(bg='paper', fg='ink', panel='ink', **{'panel-fg': 'paper'}, mid='steel', line='line', muted='muted', tint='tint', a='accent', at='accent-text', ap='accent-on-panel')
    dark = dict(bg='ink', fg='paper', panel='panel', **{'panel-fg': 'paper'}, mid='panel-line', line='ink-line', muted='ink-muted', tint='ink-tint', a='accent', at='accent-on-panel', ap='accent-on-panel')
    lines += ['  /* roles: light edition */'] + [f'  --hs-{r}:var(--hs-{v});' for r, v in light.items()] + ['}']
    block = ''.join(f'  --hs-{r}:var(--hs-{v});\n' for r, v in dark.items())
    lines.append(f'@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{\n{block}  color-scheme:dark;}}}}')
    lines.append(f':root[data-theme="dark"],.hs-dark{{\n{block}  color-scheme:dark;}}')
    return '\n'.join(lines) + '\n'


def build_fonts_css():
    out = ['/* HARDSET fonts: Archivo (variable, width 62-125%, weight 100-900) and IBM Plex Mono. SIL OFL 1.1, see OFL-*.txt. latin + latin-ext. */']
    ranges = {
        'latin-ext': 'U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF',
        'latin': 'U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD',
    }
    for sub in ('latin-ext', 'latin'):
        out.append(f"@font-face{{font-family:'Archivo';font-style:normal;font-weight:100 900;font-stretch:62% 125%;font-display:swap;src:url('Archivo-var-{sub}.woff2') format('woff2');unicode-range:{ranges[sub]};}}")
    for w in (400, 500):
        for sub in ('latin-ext', 'latin'):
            out.append(f"@font-face{{font-family:'IBM Plex Mono';font-style:normal;font-weight:{w};font-display:swap;src:url('IBMPlexMono-{w}-{sub}.woff2') format('woff2');unicode-range:{ranges[sub]};}}")
    return '\n'.join(out) + '\n'


# ------------------------------------------------------------------ logo
def glyph_paths(text, font_file, size, tracking_em=0.0, x0=0.0, baseline=0.0):
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
    font = TTFont(str(font_file))
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale = size / font['head'].unitsPerEm
    x, out = x0, []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        out.append((ch, pen.getCommands()))
        x += gs[name].width * scale + tracking_em * size
    return out, x - x0 - tracking_em * size


def _font():
    return HERE / T['logo']['font-file']


def _cap(size=100):
    from fontTools.ttLib import TTFont
    f = TTFont(str(_font()))
    return f['OS/2'].sCapHeight * size / f['head'].unitsPerEm


def wordmark(fg, acc, bars=True, text='HARDSET', size=100, tracking=None):
    tracking = T['logo']['tracking-em'] if tracking is None else tracking
    cap = _cap(size)
    paths, w = glyph_paths(text, _font(), size, tracking, 0, cap)
    inner = ''.join(f'<path d="{d}" fill="{fg}"/>' for _, d in paths)
    h = cap
    if bars:
        bh = cap * 0.11
        y1 = cap + cap * 0.2
        inner += f'<rect x="0" y="{y1:.2f}" width="{w:.2f}" height="{bh:.2f}" fill="{acc}"/>'
        inner += f'<rect x="0" y="{y1 + bh * 1.9:.2f}" width="{w * 0.58:.2f}" height="{bh:.2f}" fill="{acc}"/>'
        h = y1 + bh * 2.9
    return inner, w, h


def mark(bg, fg, acc, size=100):
    cap = _cap(100)
    paths, w = glyph_paths('H', _font(), 100, 0, 0, cap)
    s = 0.46 * size / cap
    ox, oy = (size - w * s) / 2, size * 0.2
    inner = f'<rect width="{size}" height="{size}" fill="{bg}"/>'
    inner += f'<g transform="translate({ox:.2f} {oy:.2f}) scale({s:.4f})"><path d="{paths[0][1]}" fill="{fg}"/></g>'
    bw = size * 0.52
    bx, by, bh = (size - bw) / 2, size * 0.2 + cap * s + size * 0.1, size * 0.05
    inner += f'<rect x="{bx:.2f}" y="{by:.2f}" width="{bw:.2f}" height="{bh:.2f}" fill="{acc}"/>'
    inner += f'<rect x="{bx:.2f}" y="{by + bh * 1.8:.2f}" width="{bw * 0.58:.2f}" height="{bh:.2f}" fill="{acc}"/>'
    return inner, size, size


def lockup(fg, label_fg, size=100):
    """HARDSET (no bars) with POWERBUILDING underneath, same tracking family, smaller."""
    inner, w, h = wordmark(fg, fg, bars=False, size=size)
    cap = _cap(size)
    lab, lw = glyph_paths('POWERBUILDING', _font(), size * 0.3, 0.3, 0, 0)
    sc = lw
    y = h + cap * 0.45 + size * 0.3 * 0.7
    inner += ''.join(f'<path d="{d}" fill="{label_fg}" transform="translate(0 {y:.2f})"/>' for _, d in lab)
    return inner, max(w, lw), y + size * 0.04


def svg(parts, pad=0, bg=None, label='HARDSET'):
    inner, w, h = parts
    vb = f'{-pad:g} {-pad:g} {w + 2 * pad:g} {h + 2 * pad:g}'
    rect = f'<rect x="{-pad:g}" y="{-pad:g}" width="{w + 2 * pad:g}" height="{h + 2 * pad:g}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}">{rect}{inner}</svg>\n'


def build_logos():
    ink, paper, at, acc, ap = C['ink'], C['paper'], C['accent-text'], C['accent'], C['accent-on-panel']
    return {
        'hardset-wordmark.svg': svg(wordmark(ink, at)),
        'hardset-wordmark-on-dark.svg': svg(wordmark(paper, acc)),
        'hardset-wordmark-mono-ink.svg': svg(wordmark(ink, ink)),
        'hardset-wordmark-mono-paper.svg': svg(wordmark(paper, paper)),
        'hardset-mark.svg': svg(mark(ink, paper, ap)),
        'hardset-mark-on-dark.svg': svg(mark(paper, ink, at)),
        'hardset-mark-mono-ink.svg': svg(mark(ink, paper, paper)),
        'hardset-powerbuilding-lockup.svg': svg(lockup(ink, at), label='HARDSET Powerbuilding'),
        'hardset-powerbuilding-lockup-on-dark.svg': svg(lockup(paper, paper), label='HARDSET Powerbuilding'),
    }


def outputs():
    files = {HERE / 'tokens.css': build_css(), HERE / 'fonts' / 'fonts.css': build_fonts_css()}
    for name, s in build_logos().items():
        files[HERE / 'logo' / name] = s
    return files


def main():
    check = '--check' in sys.argv
    bad = [r for r in contrast_report() if not r[5]]
    for a, b, r, need, use, ok in contrast_report():
        print(f'{"OK  " if ok else "FAIL"} {a:16s} on {b:7s} {r:5.2f}:1 (need {need}) {use}')
    stale = []
    (HERE / 'logo').mkdir(exist_ok=True)
    for path, text in outputs().items():
        if check:
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                stale.append(path.name)
        else:
            path.write_text(text, encoding='utf-8')
    if check:
        print('brand assets up to date' if not stale and not bad else f'PROBLEM: stale={stale} contrast_fail={[(b[0], b[1]) for b in bad]}')
        sys.exit(1 if stale or bad else 0)
    print(f'wrote {len(outputs())} files')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
