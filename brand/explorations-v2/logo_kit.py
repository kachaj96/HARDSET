"""Constructed HARDSET letterforms (no font dependency): straight strokes, 45-degree chamfers.

Cap height 100, stroke 22. Letters are polygons; holes are wound in the opposite
direction (nonzero fill). Used by build_explorations.py for the style mockups.
"""
H, T = 100, 22
C = 18          # outer chamfer
GAP = 12
W = dict(H=74, A=80, R=72, D=72, S=70, E=60, T=74)


def P(pts, dx=0):
    return 'M' + ' L'.join(f'{x + dx:g} {y:g}' for x, y in pts) + ' Z'


def rev(pts):
    return list(reversed(pts))


def letter(ch, dx=0, t_over=0, e_mid=None, h_bars=1):
    w = W[ch]
    if ch == 'H':
        if h_bars == 1:
            return [P([(0, 0), (T, 0), (T, 39), (w - T, 39), (w - T, 0), (w, 0), (w, H), (w - T, H), (w - T, 61), (T, 61), (T, H), (0, H)], dx)]
        # two thinner crossbars: the two sets
        a, b = (30, 44), (56, 70)
        return [P([(0, 0), (T, 0), (T, H), (0, H)], dx), P([(w - T, 0), (w, 0), (w, H), (w - T, H)], dx),
                P([(T, a[0]), (w - T, a[0]), (w - T, a[1]), (T, a[1])], dx), P([(T, b[0]), (w - T, b[0]), (w - T, b[1]), (T, b[1])], dx)]
    if ch == 'A':
        outer = [(0, H), (0, C), (C, 0), (w - C, 0), (w, C), (w, H), (w - T, H), (w - T, 74), (T, 74), (T, H)]
        hole = [(T, 52), (T, T + 10), (T + 10, T), (w - T - 10, T), (w - T, T + 10), (w - T, 52)]
        return [P(outer, dx) + ' ' + P(rev(hole), dx)]
    if ch == 'R':
        hb = 64
        outer = [(0, 0), (w - C, 0), (w, C), (w, hb - 10), (w - 10, hb), (T, hb), (T, H), (0, H)]
        hole = [(T, T), (w - T - 8, T), (w - T, T + 8), (w - T, hb - T), (T, hb - T)]
        leg = [(w - 46, hb - 4), (w - 22, hb - 4), (w, H), (w - 25, H)]
        return [P(outer, dx) + ' ' + P(rev(hole), dx), P(leg, dx)]
    if ch == 'D':
        outer = [(0, 0), (w - C, 0), (w, C), (w, H - C), (w - C, H), (0, H)]
        hole = [(T, T), (w - T - 8, T), (w - T, T + 8), (w - T, H - T - 8), (w - T - 8, H - T), (T, H - T)]
        return [P(outer, dx) + ' ' + P(rev(hole), dx)]
    if ch == 'S':
        return [P([(C, 0), (w, 0), (w, T), (T, T), (T, 39), (w, 39), (w, H - C), (w - C, H), (0, H), (0, 78), (w - T, 78), (w - T, 61), (0, 61), (0, C)], dx)]
    if ch == 'E':
        if e_mid is None:
            return [P([(0, 0), (w, 0), (w, T), (T, T), (T, 39), (w - 8, 39), (w - 8, 61), (T, 61), (T, 78), (w, 78), (w, H), (0, H)], dx)]
        # middle arm drawn separately so it can take the accent colour
        return [P([(0, 0), (w, 0), (w, T), (T, T), (T, 78), (w, 78), (w, H), (0, H)], dx),
                P([(T, 39), (w - 8, 39), (w - 8, 61), (T, 61)], dx)]
    if ch == 'T':
        ww = w + t_over
        return [P([(0, 0), (ww, 0), (ww, T), (w / 2 + T / 2, T), (w / 2 + T / 2, H), (w / 2 - T / 2, H), (w / 2 - T / 2, T), (0, T)], dx)]
    raise ValueError(ch)


def wordmark(word='HARDSET', colors=None, t_over=0, e_split=None, h_bars=1, bars=False, bar_color=None, width_only=False):
    """Returns (svg_inner, width, height). colors: list per letter."""
    colors = colors or ['currentColor'] * len(word)
    x, out = 0, []
    for i, ch in enumerate(word):
        kw = {}
        if ch == 'T' and i == len(word) - 1:
            kw['t_over'] = t_over
        if ch == 'E' and e_split:
            kw['e_mid'] = True
        if ch == 'H':
            kw['h_bars'] = h_bars
        paths = letter(ch, x, **kw)
        for k, d in enumerate(paths):
            fill = colors[i]
            if ch == 'E' and e_split and k == 1:
                fill = e_split
            if ch == 'H' and h_bars == 2 and k >= 2 and bar_color:
                fill = bar_color
            out.append(f'<path d="{d}" fill="{fill}" fill-rule="evenodd"/>')
        x += W[ch] + (t_over if (ch == 'T' and i == len(word) - 1) else 0) + GAP
    width = x - GAP
    height = H
    if bars:   # two bars under the word: Lead Set and Supporting Set
        out.append(f'<rect x="0" y="{H + 14}" width="{width}" height="8" fill="{bar_color}"/>')
        out.append(f'<rect x="0" y="{H + 28}" width="{width * 0.58:g}" height="8" fill="{bar_color}"/>')
        height = H + 36
    return ''.join(out), width, height


def svg(inner, w, h, pad=0, bg=None, label='HARDSET'):
    vb = f'{-pad:g} {-pad:g} {w + 2 * pad:g} {h + 2 * pad:g}'
    rect = f'<rect x="{-pad:g}" y="{-pad:g}" width="{w + 2 * pad:g}" height="{h + 2 * pad:g}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}">{rect}{inner}</svg>'


def stacked(colors_top, colors_bottom, bar=None):
    """HARD over SET, left aligned, optional full-width bar between lines."""
    top, wt, _ = wordmark('HARD', colors_top)
    bot, wb, _ = wordmark('SET', colors_bottom)
    gap = 26
    inner = top
    inner += f'<g transform="translate(0 {H + gap})">{bot}</g>'
    if bar:
        inner += f'<rect x="0" y="{H + 8}" width="{wt}" height="10" fill="{bar}"/>'
    return inner, wt, H * 2 + gap


def mark_h2(bg, stems, bars, size=100, pad=14):
    """Monogram: H with two crossbars on a square."""
    h2 = letter('H', 0, h_bars=2)
    s = size - 2 * pad
    sc = s / H
    ox = (size - W['H'] * sc) / 2
    inner = f'<rect width="{size}" height="{size}" fill="{bg}"/>'
    inner += f'<g transform="translate({ox:g} {pad}) scale({sc:g})">'
    inner += f'<path d="{h2[0]}" fill="{stems}"/><path d="{h2[1]}" fill="{stems}"/><path d="{h2[2]}" fill="{bars}"/><path d="{h2[3]}" fill="{bars}"/></g>'
    return inner, size, size


def mark_hs(bg, c1, c2, size=100, pad=15, bar=None):
    """Monogram: H over S, small bar between."""
    s = (size - 2 * pad - 8) / 2
    sc = s / H
    inner = f'<rect width="{size}" height="{size}" fill="{bg}"/>'
    oxh = (size - W['H'] * sc) / 2
    oxs = (size - W['S'] * sc) / 2
    inner += f'<g transform="translate({oxh:g} {pad}) scale({sc:g})">' + ''.join(f'<path d="{d}" fill="{c1}"/>' for d in letter('H')) + '</g>'
    inner += f'<g transform="translate({oxs:g} {pad + s + 8}) scale({sc:g})">' + ''.join(f'<path d="{d}" fill="{c2}"/>' for d in letter('S')) + '</g>'
    if bar:
        inner += f'<rect x="{pad}" y="{pad + s + 2:g}" width="{size - 2 * pad}" height="4" fill="{bar}"/>'
    return inner, size, size


def contrast(a, b):
    def lum(h):
        h = h.lstrip('#')
        r = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        r = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in r]
        return 0.2126 * r[0] + 0.7152 * r[1] + 0.0722 * r[2]
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
