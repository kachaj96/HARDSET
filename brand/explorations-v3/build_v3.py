#!/usr/bin/env python3
"""Mockup of the "modular report" style (light + dark) with real HARDSET and Bench Priority data.

Run: python3 brand/explorations-v3/build_v3.py  ->  brand/explorations-v3/index.html
Data: wave table and e1RM table from the handoff, ledger from analysis/example_week_validator_output_d2a.json.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'brand' / 'explorations-v2'))
import logo_kit as k  # noqa: E402

LEDGER = json.loads((ROOT / 'programs/continuous-bench-priority/analysis/example_week_validator_output_d2a.json').read_text())['ledger']

ACCENTS = [('Pomarańcza', '#FF5B1F', '#BF3708'), ('Żółć', '#F2C200', '#15171A'), ('Miedź', '#D9783C', '#A24E1D'), ('Czerwień', '#EE3B34', '#C21F1A')]

ICONS = {
    'check': '<path d="M4 12l5 5 11-11"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'stop': '<rect x="4" y="4" width="16" height="16"/><path d="M8 12h8"/>',
    'down': '<path d="M12 4v14M6 12l6 6 6-6"/>',
    'bar': '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
}


def icon(name, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="square" aria-hidden="true">{ICONS[name]}</svg>'


def logo_svg(theme, small=False):
    fg = 'var(--fg)'
    inner, w, h = k.wordmark('HARDSET', [fg] * 4 + ['var(--acc)'] * 3, bars=not small, bar_color='var(--acc)')
    return f'<svg class="logo" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="HARDSET">{inner}</svg>'


def mark_svg():
    inner, w, h = k.mark_h2('var(--fg)', 'var(--bg)', 'var(--acc)')
    return f'<svg class="mark" viewBox="0 0 {w} {h}" role="img" aria-label="HARDSET">{inner}</svg>'


def head(l, r, n):
    return f'<div class="ph"><span>{l}</span><span>{r}</span></div>'


def foot(n):
    return f'<div class="pf"><span>HARDSET</span><span>{n}</span></div>'


def tag(kind, text):
    return f'<span class="tg {kind}">{text}</span>'


# ------------------------------------------------------------------ pages
def page_cover():
    labels = ['Chest', 'Lateral Delts', 'Elbow Ext.', 'Back', 'Rear Delts', 'Elbow Flex.', 'Quads', 'Hamstrings', 'Glutes', 'Hip Add.', 'Calves', 'Trunk']
    nodes, lines = [], []
    for i, lab in enumerate(labels):
        c, r = i % 3, i // 3
        x, y = 20 + c * 70 + (r % 2) * 8, 14 + r * 26
        nodes.append((x, y, lab))
    for i, (x, y, _) in enumerate(nodes):
        c, r = i % 3, i // 3
        if c < 2:
            lines.append((x, y, nodes[i + 1][0], nodes[i + 1][1]))
        if r < 3:
            lines.append((x, y, nodes[i + 3][0], nodes[i + 3][1]))
            if c < 2:
                lines.append((x, y, nodes[i + 4][0], nodes[i + 4][1]))
    svg = ''.join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a, b, c, d in lines)
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="1.6"/><text x="{x + 3}" y="{y - 3}">{lab}</text>' for x, y, lab in nodes)
    return f'''<div class="pgx cover"><div class="in">
  <div class="cv-brand">{mark_svg()}<span>HARDSET</span></div>
  <div class="cv-main">{logo_svg('x')}<div class="cv-sub">Controlled Brutality</div>
  <p class="cv-p">Metoda treningu hipertroficznego, wersja 1.0. Dwanaście obszarów kontrolnych, jasne reguły, oznaczone źródła.</p></div>
  <svg class="net" viewBox="0 0 220 96" aria-label="Dwanaście obszarów Fixed Core jako siatka"><g class="nl">{svg}</g><g class="nd">{dots}</g></svg>
  <div class="cv-foot"><span>Adrian Drożdżyński</span><span>Wydanie 1 · 2026</span></div>
</div></div>'''


def page_toc():
    items = [('01', 'Wysiłek, Hard Set i upadek mięśniowy', 5), ('02', 'Architektura oparta na wzorcach ruchu', 11), ('03', 'Architektura serii', 17),
             ('04', 'Dobór ćwiczeń i bezpieczeństwo', 23), ('05', 'Progresja i autoregulacja', 29), ('06', 'Tydzień treningowy i regeneracja', 35),
             ('07', 'Śledzenie i ocena wyników', 41), ('08', 'Planowanie długoterminowe i specjalizacja', 47), ('09', 'Budowa i walidacja programu', 53)]
    rows = ''.join(f'<li><b>{n}</b><span>{t}</span><i></i><em>{p}</em></li>' for n, t, p in items)
    return f'''<div class="pgx"><div class="in">
  {head('Spis treści', 'HARDSET', 3)}
  <div class="grid g-toc">
    <div><h2 class="big">Spis treści</h2><ol class="toc">{rows}</ol></div>
    <aside class="side"><h3>Jak czytać</h3>
      <p>Każde twierdzenie ma oznaczenie. Badanie to opublikowana praca ze źródłem R##. Decyzja HARDSET to konwencja metody. Heurystyka to liczba, którą możesz zmienić.</p>
      <div class="tags">{tag('study', 'Badanie')}{tag('decision', 'Decyzja HARDSET')}{tag('heuristic', 'Heurystyka')}{tag('exception', 'Wyjątek siłowy')}{tag('hypothesis', 'Hipoteza programu')}</div>
      <div class="note">Status PASS walidatora oznacza zgodność z regułami, nie gwarancję efektu.</div></aside>
  </div>{foot(3)}</div></div>'''


def stat(num, unit, label):
    return f'<div class="stat"><div class="n">{num}<small>{unit}</small></div><p>{label}</p></div>'


def page_effort():
    # RIR scale 4..0 with bands
    scale = '''<svg class="chart" viewBox="0 0 300 74" role="img" aria-label="Skala RIR od 4 do 0 z zakresami serii prowadzącej i pomocniczej">
      <line class="ax" x1="10" x2="290" y1="40" y2="40"/>
      <g class="tick">''' + ''.join(f'<line x1="{10 + i * 70}" x2="{10 + i * 70}" y1="36" y2="44"/><text x="{10 + i * 70}" y="58" text-anchor="middle">{4 - i}</text>' for i in range(5)) + '''</g>
      <rect class="b2" x="220" y="22" width="70" height="14"/><text class="lb" x="290" y="17" text-anchor="end">seria pomocnicza 0–1</text>
      <rect class="b1" x="214" y="18" width="12" height="22"/><text class="lb" x="208" y="17" text-anchor="end">prowadząca ~1</text>
      <text class="lb" x="10" y="72">RIR: poprawne powtórzenia w zapasie</text></svg>'''
    return f'''<div class="pgx"><div class="in">
  {head('01 · Wysiłek, Hard Set i upadek mięśniowy', 'HARDSET', 6)}
  <div class="grid g-main">
    <div>
      <h2>Wysiłek: RIR i Hard Set</h2>
      <p class="lead">Hard Set to prawdziwa seria robocza: powtarzalna technika, wysiłek odpowiedni do ćwiczenia i jasny cel. Rozgrzewka się nie liczy.</p>
      <div class="stats">{stat('2', 'serie', 'na ćwiczenie, domyślnie')}{stat('~1', 'RIR', 'seria prowadząca (Lead Set)')}{stat('0–1', 'RIR', 'seria pomocnicza, gdy stop jest bezpieczny')}</div>
      <h4>Gdzie leży cel wysiłku</h4>
      {scale}
      <table class="dt"><caption>Domyślna architektura wysiłku</caption><thead><tr><th>Seria</th><th>Cel</th><th>Rola</th></tr></thead>
      <tbody><tr><td>Hard Set 1</td><td class="ac">~1 RIR</td><td>Lead Set: główny sygnał progresji</td></tr><tr><td>Hard Set 2</td><td class="ac">0–1 RIR</td><td>Supporting Set, bez zbędnych nieudanych prób</td></tr></tbody></table>
    </div>
    <aside class="side"><h3>Co z tego wynika</h3>
      <ul class="chk"><li>{icon('check')}<span>Liczy się seria zgodna ze standardem ruchu, a nie sam fakt zmęczenia.</span></li>
      <li>{icon('check')}<span>0 RIR tylko wtedy, gdy możesz bezpiecznie zakończyć serię.</span></li>
      <li>{icon('check')}<span>Bardzo ciężkie ruchy ze swobodną sztangą: 1–2 RIR w obu seriach.</span></li></ul>
      <div class="tags">{tag('study', 'Badanie')} <cite>R04, R19, R20</cite></div>
      <p class="small">RIR jest szacunkiem. W badaniu Mansfielda uczestnicy częściej zaniżali faktyczny zapas powtórzeń.</p>
      <div class="tags">{tag('decision', 'Decyzja HARDSET')}</div><p class="small">Dwie serie i wokół 1 RIR to konwencja metody, nie wynik badania.</p></aside>
  </div>{foot(6)}</div></div>'''


def page_wave():
    pcts = [('T1', 88, 90), ('T2', 90, 91), ('T3', 91, 93), ('T4', 85, 88)]
    bars = ''
    for i, (lab, lo, hi) in enumerate(pcts):
        x = 22 + i * 62
        y = 80 - (hi - 80) * 4.4
        h = (hi - lo) * 4.4
        cls = 'hi' if lab == 'T3' else ''
        bars += f'<rect class="fl {cls}" x="{x}" y="{80 - (lo - 80) * 4.4:g}" width="40" height="{(lo - 80) * 4.4:g}" opacity=".35"/>'
        bars += f'<rect class="fl {cls}" x="{x}" y="{y:g}" width="40" height="{h:g}"/>'
        bars += f'<text x="{x + 20}" y="{y - 4:g}" text-anchor="middle" class="vl">{lo}–{hi}%</text><text x="{x + 20}" y="92" text-anchor="middle" class="lb">{lab}</text>'
    chart = f'<svg class="chart" viewBox="0 0 280 96" role="img" aria-label="Singiel poniedziałkowy w procentach bazy fali, T1 do T4"><line class="ax" x1="14" x2="270" y1="80" y2="80"/>{bars}</svg>'
    tl = ''.join(f'<li class="{"hi" if i == 2 else ""}"><b>{t}</b><span>{d}</span></li>' for i, (t, d) in enumerate([
        ('T1', 'więcej powtórzeń'), ('T2', 'rośnie ciężar'), ('T3', 'najcięższa ekspozycja i seria kontrolna'), ('T4', 'lżejszy tydzień')]))
    rows = ''.join(f'<tr{" class=hl" if r[0] == "T3" else ""}><td>{r[0]}</td><td class="ac">{r[1]}</td><td class="r">{r[2]}</td><td class="r">{r[3]}</td><td>{r[4]}</td><td class="r">{r[5]}</td></tr>' for r in [
        ('T1', '1×1 @7', '88–90', '105–107,5', '2×5 @7', '90–92,5'), ('T2', '1×1 @7,5', '90–91', '107,5–110', '2×4 @7–8', '92,5–97,5'),
        ('T3', '1×1 @8', '91–93', '110–112,5', '2×3 @7–8', '97,5–102,5'), ('T4', '1×1 @6–7', '85–88', '102,5–105', '2×4 @6–7', '87,5–92,5')])
    return f'''<div class="pgx"><div class="in">
  {head('03 · Fala czterotygodniowa', 'BENCH PRIORITY', 13)}
  <div class="grid g-main">
    <div>
      <h2>Fala czterotygodniowa</h2>
      <ol class="tl">{tl}</ol>
      <h4>Singiel w poniedziałek, % bazy fali</h4>{chart}
      <table class="dt"><caption>Poniedziałek · przykład dla bazy 120 kg</caption><thead><tr><th>Tydz.</th><th>Singiel</th><th class="r">% bazy</th><th class="r">kg</th><th>Back-off</th><th class="r">kg</th></tr></thead><tbody>{rows}</tbody></table>
    </div>
    <aside class="side"><h3>Gdy RPE nie zgadza się z tabelą</h3>
      <div class="pair2"><div><b>Za ciężko</b><p>RPE wyższe o stopień lub więcej: zdejmij 2,5–5%.</p></div><div><b>Za lekko</b><p>Pełny punkt poniżej celu: następna seria o około 2,5% więcej. Dwa punkty: około 5%, to limit.</p></div></div>
      <div class="tags">{tag('hypothesis', 'Hipoteza programu')}</div>
      <p class="small">Nie dotyczy singla, serii kontrolnej ani tygodnia 4. Technika w normie, prędkość sztangi nie spada.</p>
      <div class="quote">Procent wyznacza punkt startowy. RPE wyznacza granicę.</div></aside>
  </div>{foot(13)}</div></div>'''


def page_amrap():
    pts = [(4, 116.7), (5, 120.0), (6, 123.3), (7, 126.7)]
    xs = lambda r: 30 + (r - 4) * 70
    ys = lambda v: 98 - (v - 114) * 6.2
    poly = ' '.join(f'{xs(r)},{ys(v):.1f}' for r, v in pts)
    dots = ''.join(f'<circle class="{"hi" if r == 5 else ""}" cx="{xs(r)}" cy="{ys(v):.1f}" r="3"/><text x="{xs(r)}" y="{ys(v) - 8:.1f}" text-anchor="middle" class="vl">{v:.1f}</text><text x="{xs(r)}" y="114" text-anchor="middle" class="lb">{r}</text>' for r, v in pts)
    chart = f'<svg class="chart" viewBox="0 0 260 120" role="img" aria-label="e1RM dla 100 kg przy 1 RIR w zależności od liczby powtórzeń"><line class="ax" x1="14" x2="250" y1="104" y2="104"/><polyline class="ln" points="{poly}"/>{dots}</svg>'
    steps = [('check', 'Technika', 'Ten sam chwyt i ustawienie co w zawodach, pauza na każdym powtórzeniu.'), ('clock', 'Przygotowanie', 'Zwykła rozgrzewka, 4–5 minut odpoczynku, żadnego ciężkiego singla tego dnia.'),
             ('stop', 'Koniec serii', 'Przy 1 powtórzeniu w zapasie albo wcześniej, gdy siada technika.'), ('down', 'Po serii', 'Jedna łatwa seria 1×4 i koniec wyciskania.')]
    st = ''.join(f'<li>{icon(i)}<div><b>{t}</b><p>{d}</p></div></li>' for i, t, d in steps)
    return f'''<div class="pgx"><div class="in">
  {head('04 · AMRAP, e1RM i baza fali', 'BENCH PRIORITY', 15)}
  <div class="grid g-main">
    <div>
      <h2>Seria kontrolna w tygodniu 3</h2>
      <p class="lead">W piątek pierwsza seria robocza to AMRAP przy około 82,5% bazy fali, z jednym powtórzeniem w zapasie (@9). Zastępuje cięższą serię objętościową.</p>
      <ul class="steps">{st}</ul>
    </div>
    <div>
      <h4>e1RM dla 100 kg przy @9</h4>{chart}
      <div class="formula">e1RM = ciężar × (1 + (powtórzenia + RIR) / 30)</div>
      <div class="tags">{tag('heuristic', 'Heurystyka')}</div><p class="small">Wzór Epleya służy do sterowania treningiem. Jedno powtórzenie to tu około 3,3 kg szacunku.</p>
      <div class="tags">{tag('study', 'Badanie')} <cite>Refalo 2024</cite></div><p class="small">24 osoby, 75% 1RM: błąd przewidywania zapasu około 0,65 powtórzenia.</p>
    </div>
    <aside class="side"><h3>Kiedy baza rośnie o 2,5 kg</h3>
      <ul class="chk"><li>{icon('check')}<span>Seria kontrolna: co najmniej jedno powtórzenie więcej niż w poprzedniej fali, przy tym samym ciężarze i RIR.</span></li>
      <li>{icon('check')}<span>Singiel z poniedziałku T3 w planowanym RPE, bez obniżania ciężaru.</span></li>
      <li>{icon('check')}<span>Zmiana tylko na wejściu do nowej fali. T4 robisz na starej bazie.</span></li></ul>
      <div class="tags">{tag('hypothesis', 'Hipoteza programu')}</div></aside>
  </div>{foot(15)}</div></div>'''


def page_ledger():
    days = ['Pn', 'Sr', 'Pt']
    rows_def = [('Chest', 'siła, osobno', 'strength'), ('Chest', 'hipertrofia', 'Chest'), ('Back', '', 'Back'), ('Lateral Delts', '', 'Lateral Delts'),
                ('Elbow Extensors', '', 'Elbow Extensors'), ('Elbow Flexors', '', 'Elbow Flexors'), ('Rear Delts', '', 'Rear Delts'),
                ('Quadriceps', '', 'Quadriceps'), ('Hamstrings', '', 'Hamstrings'), ('Glutes', '', 'Glutes')]
    body = ''
    for name, sub, key in rows_def:
        if key == 'strength':
            cells = ''.join(f'<td><i class="m s">●</i></td>' for _ in days)
            body += f'<tr><td>{name} <em>{sub}</em></td><td>Siła</td>{cells}</tr>'
            continue
        e = LEDGER[key]['exposures']
        pr = LEDGER[key]['priority']
        if key == 'Chest':     # D-1: bench sets are counted separately, so only Pec Deck remains
            e = {'Sr': 'P'}
            pr = 'Priority'
        cells = ''.join(f'<td>{"<i class=m>" + e[d] + "</i>" if d in e else "<i class=m0>·</i>"}</td>' for d in days)
        body += f'<tr><td>{name} <em>{sub}</em></td><td>{pr}</td>{cells}</tr>'
    donut_r = 38
    import math
    c = 2 * math.pi * donut_r
    bench = 7 / 35
    donut = f'''<svg class="chart donut" viewBox="0 0 120 120" role="img" aria-label="7 z 35 serii tygodnia to wyciskanie"><circle class="dn0" cx="60" cy="60" r="{donut_r}"/><circle class="dn1" cx="60" cy="60" r="{donut_r}" stroke-dasharray="{c * bench:.1f} {c:.1f}" transform="rotate(-90 60 60)"/><text x="60" y="58" text-anchor="middle" class="dv">7/35</text><text x="60" y="74" text-anchor="middle" class="lb">wyciskanie</text></svg>'''
    days_bar = ''.join(f'<rect class="{"hi" if i == 0 else ""} fl" x="{12 + i * 56}" y="{90 - h * 5:g}" width="40" height="{h * 5:g}"/><text x="{32 + i * 56}" y="{86 - h * 5:g}" text-anchor="middle" class="vl">{h}</text><text x="{32 + i * 56}" y="106" text-anchor="middle" class="lb">{d}</text>' for i, (d, h) in enumerate([('Pn', 11), ('Sr', 12), ('Pt', 12)]))
    bar = f'<svg class="chart" viewBox="0 0 180 112" role="img" aria-label="Serie w poniedziałek, środę, piątek: 11, 12, 12"><line class="ax" x1="4" x2="176" y1="90" y2="90"/>{days_bar}</svg>'
    return f'''<div class="pgx"><div class="in">
  {head('05 · Tydzień w liczbach', 'BENCH PRIORITY', 21)}
  <div class="grid g-main">
    <div>
      <h2>Gotowy tydzień: 3 × 60 minut</h2>
      <div class="stats">{stat('35', 'serii', 'w tygodniu: 11 + 12 + 12')}{stat('3×60', 'min', 'z rozgrzewką, do sprawdzenia na siłowni')}{stat('7', 'serii', 'wyciskania zawodniczego')}</div>
      <table class="dt mx"><caption>Ekspozycje w tygodniu (P = główna, S = pomocnicza)</caption><thead><tr><th>Obszar</th><th>Priorytet</th><th>Pn</th><th>Śr</th><th>Pt</th></tr></thead><tbody>{body}</tbody></table>
    </div>
    <div class="col2"><h4>Serie na trening</h4>{bar}{donut}</div>
    <aside class="side"><h3>Dla kogo ten tydzień</h3>
      <ul class="chk"><li>{icon('clock')}<span>Trzy treningi po najwyżej 60 minut.</span></li><li>{icon('bar')}<span>Priorytet: wyciskanie leżąc.</span></li>
      <li>{icon('check')}<span>Rear Delts i Glutes mają status Optional. To skutek limitu czasu, a nie ocena ich ważności.</span></li></ul>
      <div class="tags">{tag('exception', 'Wyjątek siłowy')}</div><p class="small">Serie wyciskania zawodniczego są liczone osobno. Lżejszy tydzień 4 dotyczy tylko wyciskania.</p>
      <div class="note">Walidator: PASS strukturalny. To nie jest ocena biomechaniczna ani medyczna.</div></aside>
  </div>{foot(21)}</div></div>'''


PAGES = [('Okładka', page_cover), ('Spis treści i legenda', page_toc), ('Rozdział z panelem wniosków', page_effort),
         ('Fala: oś czasu, wykres, tabela', page_wave), ('Seria kontrolna: kroki, wykres, reguły', page_amrap), ('Tydzień: macierz ekspozycji i wykresy', page_ledger)]

CSS = '''
:root{--page:#E7E6E3;--ink:#18191A;--soft:#55585B;--rule:#C4C3BF;--sans:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;--serif:'Source Serif 4',Georgia,serif;--mono:'IBM Plex Mono','Courier New',monospace;--acc:#FF5B1F;--acct:#BF3708}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:400 16px/1.5 var(--serif);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 64px}
.wrap{max-width:1160px;margin:0 auto}
h1{font:700 40px/1.05 var(--sans);margin:0 0 12px;text-wrap:balance}
.intro{max-width:64ch;margin:0 0 20px}
.feat{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0;margin:0 0 28px;border-top:2px solid var(--ink)}
.feat div{padding:14px 16px 14px 0}.feat b{font:600 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;display:block;margin-bottom:6px}.feat p{margin:0;font-size:15px;color:var(--soft)}
.ctl{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 28px;font:500 12px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.ctl button{font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--ink);background:transparent;color:var(--ink);padding:9px 12px;cursor:pointer;display:inline-flex;gap:8px;align-items:center}
.ctl button[aria-pressed=true]{background:var(--ink);color:var(--page)}
.ctl button:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.ctl i{width:12px;height:12px;display:inline-block;border:1px solid var(--ink)}
h2.sec{font:600 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--soft);margin:36px 0 10px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.pair.stack{grid-template-columns:1fr}
.pwrap{position:relative;min-width:0}
.pwrap > b{position:absolute;left:0;top:-18px;font:500 11px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--soft)}
.zoom{font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--ink);background:transparent;color:var(--ink);padding:6px 10px;cursor:pointer;margin:0 0 22px}
.zoom:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.row{margin:0 0 30px}
.rowhead{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:24px 0 8px}
.rowhead h3{margin:0;font:700 20px var(--sans)}
/* the page itself */
.pgx{container-type:inline-size;aspect-ratio:297/210;position:relative;overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,.16);background:var(--bg);color:var(--fg)}
.light{--bg:#F3F4F4;--fg:#101214;--panel:#101214;--panelfg:#ECEEEF;--mid:#B9C0C4;--line:#CBD0D3;--muted:#5F686D;--tint:#E3E6E8;--a:var(--acc);--at:var(--acct)}
.dark{--bg:#101214;--fg:#ECEEEF;--panel:#1D2124;--panelfg:#ECEEEF;--mid:#4B5359;--line:#30363A;--muted:#9AA3A8;--tint:#1A1E21;--a:var(--acc);--at:var(--acc)}
.pgx .in{position:absolute;inset:0;padding:3.4cqw 4cqw 3.6cqw;font:400 1.08cqw/1.5 var(--serif);display:flex;flex-direction:column}
.ph{display:flex;justify-content:space-between;font:600 .8cqw/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--muted);border-bottom:.1cqw solid var(--line);padding-bottom:.9cqw;margin-bottom:1.8cqw}
.pf{position:absolute;left:4cqw;right:4cqw;bottom:1.6cqw;display:flex;justify-content:space-between;font:500 .8cqw var(--mono);color:var(--muted)}
.grid{display:grid;gap:2.4cqw;flex:1;min-height:0;margin-bottom:2.2cqw}
.g-main{grid-template-columns:2.2fr 1fr}
.g-main:has(> div + div + aside){grid-template-columns:1.25fr 1fr .85fr}
.g-toc{grid-template-columns:2fr 1fr}
h2{font:700 2.9cqw/1.05 var(--sans);margin:0 0 1cqw;letter-spacing:-.005em}
h2.big{font-size:5cqw;margin-bottom:2cqw}
h3{font:600 1.2cqw/1.2 var(--sans);letter-spacing:.06em;text-transform:uppercase;margin:0 0 1cqw}
h4{font:600 .95cqw/1.2 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:1.4cqw 0 .6cqw}
p{margin:0 0 .8cqw}.lead{font-size:1.25cqw;line-height:1.45}.small{font-size:.92cqw;line-height:1.4;color:var(--muted)}
cite{font:500 .85cqw var(--mono);font-style:normal;color:var(--at)}
.side{background:var(--panel);color:var(--panelfg);padding:1.8cqw 1.6cqw;margin:-0cqw 0 0;display:flex;flex-direction:column;gap:.6cqw;min-width:0}
.side h3{border-bottom:.1cqw solid var(--mid);padding-bottom:.8cqw;margin-bottom:.6cqw}
.side .small{color:var(--panelfg);opacity:.78}
.side .tg.study,.side .tg.decision,.side .tg.heuristic{color:var(--panelfg)}
.side .tg.exception,.side cite{color:var(--acc)}
.side .tg.hypothesis{color:var(--panelfg)}
.note{border:.1cqw solid var(--mid);padding:.8cqw 1cqw;font:400 .9cqw/1.4 var(--sans);margin-top:auto}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4cqw;margin:1cqw 0 .6cqw}
.stat{border-top:.25cqw solid var(--fg);padding-top:.7cqw}
.stat .n{font:700 3.6cqw/1 var(--sans)}.stat small{font:500 1.1cqw var(--mono);margin-left:.4cqw;color:var(--at)}
.stat p{font:400 .95cqw/1.35 var(--sans);color:var(--muted);margin:.4cqw 0 0}
.dt{border-collapse:collapse;width:100%;font:400 .98cqw/1.3 var(--mono);margin-top:1cqw}
.dt caption{caption-side:top;text-align:left;font:600 .85cqw var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding-bottom:.6cqw}
.dt th{font:600 .8cqw var(--sans);letter-spacing:.08em;text-transform:uppercase;text-align:left;background:var(--fg);color:var(--bg);padding:.6cqw .8cqw}
.dt td{padding:.55cqw .8cqw;border-bottom:.1cqw solid var(--line)}
.dt .r,.dt th.r{text-align:right}.dt .ac{color:var(--at)}
.dt tr.hl td{background:var(--tint)}
.dt.mx td{text-align:center}.dt.mx td:first-child{text-align:left}.dt.mx td:nth-child(2){text-align:left;color:var(--muted)}
.dt.mx em{font:italic 400 .85cqw var(--serif);color:var(--muted)}
.m{font-style:normal;font-weight:600;display:inline-block;min-width:1.6cqw;padding:.1cqw .3cqw;background:var(--fg);color:var(--bg)}
.m.s{background:var(--a);color:#101214}.m0{font-style:normal;color:var(--mid)}
.tags{display:flex;flex-wrap:wrap;gap:.6cqw;align-items:center;margin:.4cqw 0}
.tg{display:inline-block;font:500 .78cqw/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;padding:.35cqw .6cqw;border:.12cqw solid currentColor;white-space:nowrap}
.tg.study{color:var(--muted)}.tg.decision{color:var(--fg)}.tg.heuristic{color:var(--muted);border-style:dotted}.tg.exception{color:var(--at)}.tg.hypothesis{border-style:dashed;color:var(--fg)}
.chk{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.9cqw}
.chk li{display:grid;grid-template-columns:1.8cqw 1fr;gap:.8cqw;font:400 1cqw/1.4 var(--sans)}
.ic{width:1.8cqw;height:1.8cqw;color:var(--acc)}
.chart{width:100%;height:auto;display:block;color:var(--fg)}
.chart .ax{stroke:var(--fg);stroke-width:.8}.chart .tick line{stroke:var(--fg);stroke-width:.8}
.chart text{font:500 6.6px var(--mono);fill:var(--fg)}.chart .lb{fill:var(--muted)}.chart .vl{font-size:6.8px}
.chart .fl{fill:var(--fg)}.chart .fl.hi{fill:var(--a)}
.chart .b1{fill:var(--a)}.chart .b2{fill:var(--mid)}
.chart .ln{fill:none;stroke:var(--fg);stroke-width:1.4}.chart .ln~circle{fill:var(--fg)}.chart circle.hi{fill:var(--a)}
.donut{max-width:15cqw}.chart circle.dn0{fill:none;stroke:var(--mid);stroke-width:12}.chart circle.dn1{fill:none;stroke:var(--a);stroke-width:12}.chart .dv{font:700 14px var(--sans)}
.tl{list-style:none;margin:.8cqw 0 0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-top:.25cqw solid var(--fg)}
.tl li{padding:.7cqw 1cqw 0 0;position:relative}.tl li::before{content:"";position:absolute;left:0;top:-.75cqw;width:1.2cqw;height:1.2cqw;background:var(--fg)}
.tl li.hi::before{background:var(--a)}
.tl b{font:700 1.5cqw var(--sans);display:block;margin-top:.5cqw}.tl span{font:400 .95cqw/1.35 var(--sans);color:var(--muted)}
.pair2{display:grid;grid-template-columns:1fr 1fr;gap:1cqw}.pair2 div{border-top:.15cqw solid var(--acc);padding-top:.6cqw}.pair2 b{font:600 1cqw var(--sans);text-transform:uppercase;letter-spacing:.06em}.pair2 p{font:400 .95cqw/1.4 var(--sans);margin:.3cqw 0 0}
.quote{font:italic 400 1.5cqw/1.3 var(--serif);border-left:.35cqw solid var(--acc);padding-left:1.2cqw;margin-top:auto}
.steps{list-style:none;margin:1cqw 0 0;padding:0;display:flex;flex-direction:column;gap:1cqw}
.steps li{display:grid;grid-template-columns:2.6cqw 1fr;gap:1cqw;border-top:.1cqw solid var(--line);padding-top:.8cqw}.steps .ic{width:2.4cqw;height:2.4cqw}
.steps b{font:600 1.1cqw var(--sans);text-transform:uppercase;letter-spacing:.06em}.steps p{font:400 1cqw/1.4 var(--sans);margin:.2cqw 0 0}
.formula{font:500 1.05cqw var(--mono);background:var(--tint);padding:.9cqw 1.1cqw;margin:1cqw 0 .8cqw}
.col2{display:flex;flex-direction:column;gap:.4cqw;min-width:0}
.toc{list-style:none;margin:0;padding:0}.toc li{display:grid;grid-template-columns:3.2cqw 1fr 3cqw 2.4cqw;align-items:baseline;gap:.6cqw;padding:.75cqw 0;border-bottom:.1cqw solid var(--line);font:500 1.35cqw var(--sans)}
.toc b{font:500 1.1cqw var(--mono);color:var(--at)}.toc i{border-bottom:.1cqw dotted var(--mid);height:.1cqw}.toc em{font:500 1.1cqw var(--mono);font-style:normal;text-align:right;color:var(--muted)}
.cover .in{padding:3.6cqw 4.4cqw}
.cv-brand{display:flex;gap:1cqw;align-items:center;font:600 1.1cqw var(--sans);letter-spacing:.18em}.cv-brand .mark{width:2.6cqw;height:2.6cqw}
.cv-main{margin-top:11cqw;width:52%}.cv-main .logo{width:100%;height:auto;display:block}
.cv-sub{font:italic 400 2.6cqw/1.1 var(--serif);margin-top:2.4cqw}.cv-p{font:400 1.2cqw/1.5 var(--sans);color:var(--muted);margin-top:1.4cqw;max-width:38cqw}
.net{position:absolute;right:3.4cqw;bottom:3.4cqw;width:46cqw;height:auto}
.net .nl line{stroke:var(--mid);stroke-width:.4}.net .nd circle{fill:var(--a)}.net .nd text{font:500 3.6px var(--mono);fill:var(--muted)}
.cv-foot{position:absolute;left:4.4cqw;bottom:3.4cqw;font:500 1cqw/1.6 var(--mono);color:var(--muted);display:flex;flex-direction:column}
@media (max-width:760px){.pair{grid-template-columns:1fr}h1{font-size:32px}}
'''

JS = '''
document.querySelectorAll('.zoom').forEach(function(b){b.addEventListener('click',function(){var p=b.closest('.row').querySelector('.pair');var s=p.classList.toggle('stack');b.textContent=s?'Zmniejsz':'Powiększ';});});
document.querySelectorAll('.ctl [data-acc]').forEach(function(b){b.addEventListener('click',function(){document.documentElement.style.setProperty('--acc',b.dataset.acc);document.documentElement.style.setProperty('--acct',b.dataset.acct);document.querySelectorAll('.ctl [data-acc]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});});});
'''


import re


def scale_cqw(css, f=1.26):
    return re.sub(r'(\d*\.?\d+)cqw', lambda m: f'{float(m.group(1)) * f:.2f}cqw', css)


def main():
    rows = ''
    for title, fn in PAGES:
        html = fn()
        rows += f'''<div class="row"><div class="rowhead"><h3>{title}</h3><button class="zoom" type="button">Powiększ</button></div>
<div class="pair"><div class="pwrap"><b>Jasna</b><div class="light">{html}</div></div><div class="pwrap"><b>Ciemna</b><div class="dark">{html}</div></div></div></div>'''
    acc = ''.join(f'<button type="button" data-acc="{a}" data-acct="{t}" aria-pressed="{"true" if i == 0 else "false"}"><i style="background:{a}"></i>{n}</button>' for i, (n, a, t) in enumerate(ACCENTS))
    page = f'''<title>HARDSET Raport</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap">
<style>{scale_cqw(CSS)}</style>
<div class="wrap" lang="pl">
<h1>Styl modułowego raportu</h1>
<p class="intro">Z twoich przykładów wyciągnąłem zasady składu i zastosowałem je do prawdziwej treści HARDSET i Bench Priority. Poniżej wersja jasna i ciemna każdej strony, z danymi z programu i z walidatora. Format poziomy (A4 w poziomie), do czytania na ekranie i do druku.</p>
<div class="feat">
<div><b>Siatka modułów</b><p>Strona to 2–3 kolumny: treść, wykres lub tabela, ciemny panel wniosków po prawej.</p></div>
<div><b>Liczba najpierw</b><p>Kluczowe liczby (2 serie, ~1 RIR, 35 serii) jako duże wskaźniki z jednozdaniowym opisem.</p></div>
<div><b>Wykres obok tekstu</b><p>Słupki, linia, wskaźnik kołowy, oś czasu. Zawsze z prawdziwymi danymi i podpisem.</p></div>
<div><b>Tabela z czarnym nagłówkiem</b><p>Liczby w kroju Mono, wyróżniony wiersz, bez ozdobnych kratek.</p></div>
<div><b>Panel „Co z tego wynika”</b><p>Trzy punkty z ikoną, klasa twierdzenia i źródło w jednym miejscu.</p></div>
<div><b>Okładka z wielkim tytułem</b><p>Logo jako grafika, siatka 12 obszarów Fixed Core zamiast ogólnej dekoracji.</p></div>
</div>
<div class="ctl" role="group" aria-label="Kolor akcentu"><span>Akcent:</span>{acc}</div>
{rows}
</div>
<script>{JS}</script>'''
    (HERE / 'index.html').write_text(page, encoding='utf-8')
    print('wrote', HERE / 'index.html')


if __name__ == '__main__':
    main()
