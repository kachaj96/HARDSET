"""Inline SVG charts and icons for the publication samples. Colours come from CSS roles in book.css.

All numbers are taken from the Bench Priority handoff (wave table, e1RM table) and from
programs/continuous-bench-priority/analysis/example_week_validator_output_d2a.json (week ledger).
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = json.loads((ROOT / 'programs/continuous-bench-priority/analysis/example_week_validator_output_d2a.json').read_text())['ledger']


def comma(x):
    return str(x).replace('.', ',')


ICONS = {
    'check': '<path d="M4 12l5 5 11-11"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'stop': '<rect x="4" y="4" width="16" height="16"/><path d="M8 12h8"/>',
    'down': '<path d="M12 4v14M6 12l6 6 6-6"/>',
    'bar': '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
}


def icon(name):
    return f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="square" aria-hidden="true">{ICONS[name]}</svg>'


def ruler():
    out = ['<line class="ax" x1="4" x2="156" y1="30" y2="30"/>']
    for i in range(17):
        x = 4 + i * 9.5
        big = i % 4 == 0
        out.append(f'<line class="tk" x1="{x}" x2="{x}" y1="{30 - (9 if big else 4)}" y2="30"/>')
        if big:
            out.append(f'<text x="{x}" y="43" text-anchor="middle">{4 - i // 4}</text>')
    out.append('<rect class="blk" x="118" y="12" width="38" height="8"/><rect class="blk" x="118" y="3" width="9.5" height="8"/>')
    out.append('<text class="cap" x="4" y="9">RIR: zapas powtórzeń</text>')
    return f'<svg class="ruler" viewBox="0 0 160 48" role="img" aria-label="Skala RIR od 4 do 0 z zaznaczonym zakresem 1 do 0">{"".join(out)}</svg>'


def wave_cover():
    pcts = [('T1', 88, 90), ('T2', 90, 91), ('T3', 91, 93), ('T4', 85, 88)]
    bars = ''
    for i, (lab, lo, hi) in enumerate(pcts):
        h = (hi - 80) * 3.6
        x = 8 + i * 38
        cls = 'blk' if lab == 'T3' else 'fl'
        bars += f'<rect class="{cls}" x="{x}" y="{52 - h:g}" width="26" height="{h:g}"/><text x="{x + 13}" y="62" text-anchor="middle">{lab}</text><text x="{x + 13}" y="{49 - h:g}" text-anchor="middle">{lo}–{hi}%</text>'
    return f'<svg class="wavec" viewBox="0 -8 160 74" role="img" aria-label="Singiel poniedziałkowy w kolejnych tygodniach fali"><line class="ax" x1="4" x2="156" y1="53" y2="53"/>{bars}</svg>'


def effort_scale():
    ticks = ''.join(f'<line class="tk" x1="{10 + i * 70}" x2="{10 + i * 70}" y1="36" y2="44"/><text x="{10 + i * 70}" y="58" text-anchor="middle">{4 - i}</text>' for i in range(5))
    return (f'<svg class="chart" viewBox="0 0 300 64" role="img" aria-label="Skala RIR od 4 do 0: seria prowadząca około 1, pomocnicza 0 do 1"><line class="ax" x1="10" x2="290" y1="40" y2="40"/>{ticks}'
            '<rect class="b2" x="220" y="22" width="70" height="14"/><text class="lb" x="290" y="17" text-anchor="end">pomocnicza 0–1</text>'
            '<rect class="b1" x="214" y="18" width="12" height="22"/><text class="lb" x="208" y="17" text-anchor="end">prowadząca ~1</text>'
            '</svg>')


def wave_chart():
    pcts = [('T1', 88, 90), ('T2', 90, 91), ('T3', 91, 93), ('T4', 85, 88)]
    bars = ''
    for i, (lab, lo, hi) in enumerate(pcts):
        x = 22 + i * 62
        y = 80 - (hi - 80) * 4.4
        h = (hi - lo) * 4.4
        cls = 'hi' if lab == 'T3' else ''
        bars += f'<rect class="fl base {cls}" x="{x}" y="{80 - (lo - 80) * 4.4:g}" width="40" height="{(lo - 80) * 4.4:g}"/><rect class="fl {cls}" x="{x}" y="{y:g}" width="40" height="{h:g}"/>'
        bars += f'<text x="{x + 20}" y="{y - 4:g}" text-anchor="middle">{lo}–{hi}%</text><text class="lb" x="{x + 20}" y="92" text-anchor="middle">{lab}</text>'
    return f'<svg class="chart compact" viewBox="0 0 280 96" role="img" aria-label="Singiel poniedziałkowy w procentach bazy fali, T1 do T4"><line class="ax" x1="14" x2="270" y1="80" y2="80"/>{bars}</svg>'


def e1rm_chart():
    pts = [(4, 116.7), (5, 120.0), (6, 123.3), (7, 126.7)]
    xs = lambda r: 30 + (r - 4) * 70
    ys = lambda v: 98 - (v - 114) * 6.2
    poly = ' '.join(f'{xs(r)},{ys(v):.1f}' for r, v in pts)
    dots = ''.join(f'<circle class="{"hi" if r == 5 else ""}" cx="{xs(r)}" cy="{ys(v):.1f}" r="3"/><text x="{xs(r)}" y="{ys(v) - 8:.1f}" text-anchor="middle">{comma(v)}</text><text class="lb" x="{xs(r)}" y="114" text-anchor="middle">{r} powt.</text>' for r, v in pts)
    return f'<svg class="chart compact" viewBox="0 0 260 120" role="img" aria-label="e1RM dla 100 kg przy 1 RIR w zależności od liczby powtórzeń"><line class="ax" x1="14" x2="250" y1="104" y2="104"/><polyline class="ln" points="{poly}"/>{dots}</svg>'


def days_chart():
    bars = ''.join(f'<rect class="fl {"hi" if i == 0 else ""}" x="{12 + i * 56}" y="{90 - h * 5:g}" width="40" height="{h * 5:g}"/><text x="{32 + i * 56}" y="{86 - h * 5:g}" text-anchor="middle">{h}</text><text class="lb" x="{32 + i * 56}" y="106" text-anchor="middle">{d}</text>' for i, (d, h) in enumerate([('Pn', 11), ('Śr', 12), ('Pt', 12)]))
    return f'<svg class="chart" viewBox="0 0 180 112" role="img" aria-label="Serie w poniedziałek, środę i piątek: 11, 12, 12"><line class="ax" x1="4" x2="176" y1="90" y2="90"/>{bars}</svg>'


def donut():
    r = 38
    c = 2 * math.pi * r
    return (f'<svg class="chart donut" viewBox="0 0 120 120" role="img" aria-label="7 z 35 serii tygodnia to wyciskanie"><circle class="dn0" cx="60" cy="60" r="{r}"/>'
            f'<circle class="dn1" cx="60" cy="60" r="{r}" stroke-dasharray="{c * 0.2:.1f} {c:.1f}" transform="rotate(-90 60 60)"/>'
            '<text x="60" y="62" text-anchor="middle" class="dv">7/35</text><text class="lb" x="60" y="76" text-anchor="middle">wyciskanie</text></svg>')


def ledger_rows():
    body = ''
    order = ['Chest', 'Back', 'Lateral Delts', 'Elbow Extensors', 'Elbow Flexors', 'Rear Delts', 'Quadriceps', 'Hamstrings', 'Glutes']
    for name in order:
        e = LEDGER[name]['exposures']
        cells = ''.join(f'<td>{"<i class=m>" + e[d] + "</i>" if d in e else "<i class=m0>·</i>"}</td>' for d in ('Pn', 'Sr', 'Pt'))
        extra = ' <em>z wyciskaniem</em>' if name == 'Chest' else ''
        body += f'<tr><td>{name}{extra}</td><td>{LEDGER[name]["priority"]}</td>{cells}</tr>'
    return body


CHARTS = {'effort': effort_scale, 'wave': wave_chart, 'e1rm': e1rm_chart, 'days': days_chart, 'donut': donut, 'ledger': ledger_rows}
