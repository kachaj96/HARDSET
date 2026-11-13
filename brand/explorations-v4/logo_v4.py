"""HARDSET logo v4: Archivo Expanded ExtraBold outlines, wide tracking, two-bar device.

The two bars are the Two-Set default: a full-length bar (Lead Set) and a shorter one (Supporting Set).
Needs fontTools (pip install fonttools). Outlines are converted to paths, so the logo does not need the font.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for extra in (HERE.parent / 'system',):
    sys.path.insert(0, str(extra))
from build_brand import glyph_paths  # noqa: E402

FONT = HERE / 'fonts' / 'Archivo-800-expanded.ttf'
TRACK = 0.24   # em
SIZE = 100


def _cap_height():
    from fontTools.ttLib import TTFont
    f = TTFont(str(FONT))
    return f['OS/2'].sCapHeight * SIZE / f['head'].unitsPerEm


def wordmark(fg, acc, bars=True, text='HARDSET'):
    """Returns (inner_svg, width, height). fg/acc may be CSS colours or var(...)."""
    cap = _cap_height()
    paths, w = glyph_paths(text, FONT, SIZE, TRACK, 0, cap)
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
    """H in Archivo Expanded ExtraBold on a square, two bars underneath."""
    cap = _cap_height()
    paths, w = glyph_paths('H', FONT, SIZE, 0, 0, cap)
    s = 0.46 * size / cap
    ox = (size - w * s) / 2
    oy = size * 0.2
    inner = f'<rect width="{size}" height="{size}" fill="{bg}"/>'
    inner += f'<g transform="translate({ox:.2f} {oy:.2f}) scale({s:.4f})"><path d="{paths[0][1]}" fill="{fg}"/></g>'
    bw = size * 0.52
    bx = (size - bw) / 2
    by = size * 0.2 + cap * s + size * 0.1
    bh = size * 0.05
    inner += f'<rect x="{bx:.2f}" y="{by:.2f}" width="{bw:.2f}" height="{bh:.2f}" fill="{acc}"/>'
    inner += f'<rect x="{bx:.2f}" y="{by + bh * 1.8:.2f}" width="{bw * 0.58:.2f}" height="{bh:.2f}" fill="{acc}"/>'
    return inner, size, size


def svg(parts, pad=0, bg=None, label='HARDSET'):
    inner, w, h = parts
    vb = f'{-pad:g} {-pad:g} {w + 2 * pad:g} {h + 2 * pad:g}'
    rect = f'<rect x="{-pad:g}" y="{-pad:g}" width="{w + 2 * pad:g}" height="{h + 2 * pad:g}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}">{rect}{inner}</svg>'
