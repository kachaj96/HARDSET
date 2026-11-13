#!/usr/bin/env python3
"""Build HARDSET brand assets from tokens.json and the bundled fonts.

Outputs (in brand/system/):
  tokens.css           CSS custom properties for print, screen light (paper) and dark (ink)
  logo/*.svg           wordmark, stamp mark and lockups with text converted to outlines

Requires fontTools + brotli only for the logo step (dev dependency):
  pip install fonttools brotli
Run: python brand/system/build_brand.py [--check]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOK = json.loads((HERE / 'tokens.json').read_text(encoding='utf-8'))
C = {k: v['value'] for k, v in TOK['color'].items()}


def build_css():
    lines = ['/* Generated from tokens.json by build_brand.py. Do not edit by hand. */',
             "@import url('fonts/fonts.css');", ':root{']
    for k, v in C.items():
        lines.append(f'  --hs-{k}:{v};')
    for k, v in TOK['font'].items():
        lines.append(f'  --hs-font-{k}:{v["value"]};')
    for k, v in TOK['type-scale-px'].items():
        if not k.startswith('$'):
            lines.append(f'  --hs-size-{k}:{v}px;')
    for k, v in TOK['space'].items():
        lines.append(f'  --hs-space-{k}:{v};')
    for k, v in TOK['radius'].items():
        lines.append(f'  --hs-radius-{k}:{v};')
    # semantic roles, light (paper) theme
    lines += ['  --hs-bg:var(--hs-paper);', '  --hs-fg:var(--hs-ink);', '  --hs-fg-muted:var(--hs-muted);',
              '  --hs-surface:var(--hs-tint);', '  --hs-line:var(--hs-rule);', '  --hs-accent:var(--hs-oxide);',
              '  --hs-data:var(--hs-slate);', '  --hs-evidence:var(--hs-moss);', '}']
    dark = ['--hs-bg:var(--hs-ink);', '--hs-fg:var(--hs-paper);', '--hs-fg-muted:var(--hs-paper-muted);',
            '--hs-surface:var(--hs-ink-raised);', '--hs-line:#3A4240;', '--hs-accent:var(--hs-oxide-on-ink);',
            '--hs-data:var(--hs-slate-on-ink);', '--hs-evidence:#A9B59B;', 'color-scheme:dark;']
    lines.append('@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){' + ''.join(dark) + '}}')
    lines.append(':root[data-theme="dark"]{' + ''.join(dark) + '}')
    print_scale = TOK['type-scale-pt']
    lines.append('@media print{:root{' + ''.join(
        f'--hs-size-{k}:{v}pt;' for k, v in print_scale.items() if not k.startswith('$')) + '}}')
    return '\n'.join(lines) + '\n'


# ---------------- logos ----------------
def glyph_paths(text, font_file, size, tracking_em=0.0, x0=0.0, baseline=0.0):
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    font = TTFont(str(font_file))
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font['head'].unitsPerEm
    scale = size / upem
    x = x0
    out = []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x, baseline))
        gs[name].draw(tpen)
        out.append((ch, pen.getCommands()))
        x += gs[name].width * scale + tracking_em * size
    width = x - x0 - tracking_em * size
    return out, width


def wordmark_svg(colors, size=48, pad=0):
    f = HERE / 'fonts' / 'IBMPlexSansCondensed-700-latin.woff2'
    parts, w = glyph_paths('HARDSET', f, size, 0.08, pad, size * 0.72 + pad)
    cap = size * 0.72
    paths = ''.join(f'<path fill="{colors[i]}" d="{d}"/>' for i, (_, d) in enumerate(parts))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 2 * pad:.1f} {cap + 2 * pad:.1f}" '
            f'role="img" aria-label="HARDSET">{paths}</svg>\n')


def mark_svg(frame, letters, bar, bg=None, size=64):
    f = HERE / 'fonts' / 'IBMPlexSansCondensed-700-latin.woff2'
    s = size
    fs = s * 0.36
    cap = fs * 0.72
    base = s / 2 + cap / 2
    h, wh = glyph_paths('H', f, fs, 0, 0, base)
    sh, ws = glyph_paths('S', f, fs, 0, 0, base)
    gap = s * 0.11
    hx = s / 2 - gap - wh
    sx = s / 2 + gap
    h, _ = glyph_paths('H', f, fs, 0, hx, base)
    sh, _ = glyph_paths('S', f, fs, 0, sx, base)
    bw = s * 0.047
    stroke = s * 0.047
    rect_bg = f'<rect width="{s}" height="{s}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}" role="img" aria-label="HARDSET">'
            f'{rect_bg}<rect x="{stroke / 2:.2f}" y="{stroke / 2:.2f}" width="{s - stroke:.2f}" height="{s - stroke:.2f}" '
            f'fill="none" stroke="{frame}" stroke-width="{stroke:.2f}"/>'
            f'<rect x="{s / 2 - bw / 2:.2f}" y="{s * 0.13:.2f}" width="{bw:.2f}" height="{s * 0.74:.2f}" fill="{bar}"/>'
            f'<path fill="{letters}" d="{h[0][1]}"/><path fill="{letters}" d="{sh[0][1]}"/></svg>\n')


def lockup_svg(word_colors, sub_color, sub='POWERBUILDING', size=48):
    fb = HERE / 'fonts' / 'IBMPlexSansCondensed-700-latin.woff2'
    fs = HERE / 'fonts' / 'IBMPlexSansCondensed-600-latin.woff2'
    cap = size * 0.72
    parts, w = glyph_paths('HARDSET', fb, size, 0.08, 0, cap)
    sub_size = size * 0.34
    gap = size * 0.4
    sparts, sw = glyph_paths(sub, fs, sub_size, 0.14, w + gap, cap)
    paths = ''.join(f'<path fill="{word_colors[i]}" d="{d}"/>' for i, (_, d) in enumerate(parts))
    paths += ''.join(f'<path fill="{sub_color}" d="{d}"/>' for _, d in sparts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + gap + sw:.1f} {cap:.1f}" role="img" '
            f'aria-label="HARDSET {sub.title()}">{paths}</svg>\n')


def build_logos():
    ink, paper, oxide = C['ink'], C['paper'], C['oxide']
    two = lambda a, b: [a] * 4 + [b] * 3
    return {
        'hardset-wordmark.svg': wordmark_svg(two(ink, oxide)),
        'hardset-wordmark-on-ink.svg': wordmark_svg(two(paper, C['oxide-on-ink'])),
        'hardset-wordmark-mono-ink.svg': wordmark_svg([ink] * 7),
        'hardset-wordmark-mono-paper.svg': wordmark_svg([paper] * 7),
        'hardset-mark.svg': mark_svg(ink, ink, oxide),
        'hardset-mark-on-ink.svg': mark_svg(paper, paper, C['oxide-on-ink'], bg=ink),
        'hardset-mark-mono-ink.svg': mark_svg(ink, ink, ink),
        'hardset-powerbuilding-lockup.svg': lockup_svg(two(ink, oxide), C['slate']),
        'hardset-powerbuilding-lockup-on-slate.svg': lockup_svg([paper] * 7, paper),
    }


def main():
    check = '--check' in sys.argv
    outputs = {HERE / 'tokens.css': build_css()}
    try:
        for name, svg in build_logos().items():
            outputs[HERE / 'logo' / name] = svg
    except ImportError:
        print('fontTools not installed: logos skipped (pip install fonttools brotli)')
    stale = []
    for path, content in outputs.items():
        if check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                stale.append(path.name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    if check:
        if stale:
            print('stale:', ', '.join(stale)); sys.exit(1)
        print('brand assets up to date')
    else:
        print('wrote', len(outputs), 'files')


if __name__ == '__main__':
    main()
