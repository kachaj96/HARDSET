#!/usr/bin/env python3
"""Portrait modular-report mockup (v4): Archivo type, new outlined logo, original covers, muted-green accents.

Run: python3 brand/explorations-v4/build_v4.py -> brand/explorations-v4/index.html + logos/*.svg
Needs fontTools (logo outlines). Data: handoff tables and analysis/example_week_validator_output_d2a.json.
D-1 (b): competition bench sets count as Chest P, so Chest shows P in all three sessions.
"""
import colorsys
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'brand' / 'explorations-v2'))
sys.path.insert(0, str(ROOT / 'brand' / 'explorations-v3'))
import logo_kit as k  # noqa: E402  (contrast helper)
import logo_v4 as L  # noqa: E402
from build_v3 import icon, tag, stat  # noqa: E402

LEDGER = json.loads((ROOT / 'programs/continuous-bench-priority/analysis/example_week_validator_output_d2a.json').read_text())['ledger']
BLACK, WHITE, PANEL = '#101214', '#F3F4F4', '#1D2124'


def hex2hls(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hls(r, g, b)


def hls2hex(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255))


def tune(hexc, bg, want, direction):
    """Move lightness until contrast with bg >= want (direction -1 darker, +1 lighter)."""
    h, l, s = hex2hls(hexc)
    for _ in range(200):
        c = hls2hex(h, l, s)
        if k.contrast(c, bg) >= want:
            return c
        l += direction * 0.005
    return c


# muted greens, tuned so the base value works as a fill on both black and off-white
BASE = [('Szałwia', '#5A8663'), ('Oliwka', '#6A8541'), ('Eukaliptus', '#54877A')]
ACCENTS = []
for n, c in BASE:
    ACCENTS.append(dict(name=n, acc=c, acct=tune(c, WHITE, 4.6, -1), accd=tune(c, PANEL, 4.6, +1)))


def wm(fg, acc, bars=True):
    inner, w, h = L.wordmark(fg, acc, bars=bars)
    return f'<svg class="logo" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="HARDSET">{inner}</svg>'


def mk(bg='var(--fg)', fg='var(--bg)', acc='var(--a)', cls='mark'):
    inner, w, h = L.mark(bg, fg, acc)
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="HARDSET">{inner}</svg>'


def head(l, r):
    return f'<div class="ph"><span>{l}</span><span>{r}</span></div>'


def foot(n, side='r'):
    return f'<div class="pf"><span>HARDSET</span><span>{n}</span></div>'


def ruler():
    """RIR ruler: ticks every half step from 4 to 0, accent block on the 1..0 interval (supporting 0-1, lead ~1)."""
    out = ['<line class="ax" x1="4" x2="156" y1="30" y2="30"/>']
    for i in range(0, 17):
        x = 4 + i * 9.5
        big = i % 4 == 0
        out.append(f'<line class="tk" x1="{x}" x2="{x}" y1="{30 - (9 if big else 4)}" y2="30"/>')
        if big:
            out.append(f'<text x="{x}" y="43" text-anchor="middle">{4 - i // 4}</text>')
    out.append('<rect class="blk" x="118" y="12" width="38" height="8"/>')
    out.append('<rect class="blk" x="118" y="3" width="9.5" height="8"/>')
    out.append('<text class="cap" x="4" y="9">RIR · zapas powtórzeń</text>')
    return f'<svg class="ruler" viewBox="0 0 160 48" role="img" aria-label="Skala RIR od 4 do 0 z zaznaczonym zakresem 1 do 0">{"".join(out)}</svg>'


def cover_hardset():
    return f'''<div class="pgx cover"><div class="in">
  <div class="cv-top"><span>ADRIAN DROŻDŻYŃSKI</span><span>WYDANIE 1 · 2026</span></div>
  <div class="cv-title">{wm('var(--fg)', 'var(--a)')}</div>
  <div class="cv-sub">CONTROLLED BRUTALITY</div>
  <p class="cv-p">Metoda treningu hipertroficznego. Dwie serie, dwanaście obszarów kontrolnych, jasne reguły, oznaczone źródła.</p>
  {ruler()}
  <div class="cv-foot"><span>Wersja 1.0</span>{mk(cls='mark')}</div>
</div></div>'''


def cover_bench():
    pcts = [('T1', 89), ('T2', 90.5), ('T3', 92), ('T4', 86.5)]
    bars = ''
    for i, (lab, v) in enumerate(pcts):
        h = (v - 80) * 3.6
        x = 8 + i * 38
        cls = 'blk' if lab == 'T3' else 'fl'
        bars += f'<rect class="{cls}" x="{x}" y="{52 - h:g}" width="26" height="{h:g}"/><text x="{x + 13}" y="62" text-anchor="middle">{lab}</text><text class="vl" x="{x + 13}" y="{49 - h:g}" text-anchor="middle">{v:g}%</text>'.replace('.5%', ',5%')
    chart = f'<svg class="wavec" viewBox="0 0 160 66" role="img" aria-label="Poniedziałkowy singiel w kolejnych tygodniach fali"><line class="ax" x1="4" x2="156" y1="53" y2="53"/>{bars}</svg>'
    return f'''<div class="pgx cover"><div class="in">
  <div class="cv-top"><span>ADRIAN DROŻDŻYŃSKI</span><span>WERSJA 1.2</span></div>
  <div class="cv-lock">{wm('var(--fg)', 'var(--a)', bars=False)}<span>POWERBUILDING</span></div>
  <div class="cv-title2">Continuous<br>Bench<br>Priority</div>
  <p class="cv-p">Trzy treningi w tygodniu po 60 minut. Czterotygodniowa fala, seria kontrolna, jasne reguły zmiany bazy.</p>
  {chart}
  <div class="cv-foot"><span>Program oparty na metodzie HARDSET v1.0</span>{mk(cls='mark')}</div>
</div></div>'''


def page_toc():
    items = [('01', 'Wysiłek, Hard Set i upadek mięśniowy'), ('02', 'Architektura oparta na wzorcach ruchu'), ('03', 'Architektura serii'),
             ('04', 'Dobór ćwiczeń i bezpieczeństwo'), ('05', 'Progresja i autoregulacja'), ('06', 'Tydzień treningowy i regeneracja'),
             ('07', 'Śledzenie i ocena wyników'), ('08', 'Planowanie długoterminowe i specjalizacja'), ('09', 'Budowa i walidacja programu')]
    rows = ''.join(f'<li><b>{n}</b><span>{t}</span><i></i></li>' for n, t in items)
    return f'''<div class="pgx"><div class="in">
  {head('Spis treści', 'HARDSET')}
  <h2 class="big">Spis<br>treści</h2>
  <ol class="toc">{rows}</ol>
  <div class="panel legend"><h3>Jak czytać</h3>
    <p>Każde twierdzenie ma oznaczenie. Badanie to opublikowana praca ze źródłem R##. Decyzja HARDSET to konwencja metody. Heurystyka to liczba, którą możesz zmienić.</p>
    <div class="tags">{tag('study', 'Badanie')}{tag('decision', 'Decyzja HARDSET')}{tag('heuristic', 'Heurystyka')}{tag('exception', 'Wyjątek siłowy')}{tag('hypothesis', 'Hipoteza programu')}</div></div>
  {foot('')}</div></div>'''


def page_effort():
    ticks = ''.join(f'<line class="tk" x1="{10 + i * 70}" x2="{10 + i * 70}" y1="36" y2="44"/><text x="{10 + i * 70}" y="58" text-anchor="middle">{4 - i}</text>' for i in range(5))
    scale = f'''<svg class="chart" viewBox="0 0 300 74" role="img" aria-label="Skala RIR od 4 do 0: seria prowadząca około 1, pomocnicza 0 do 1"><line class="ax" x1="10" x2="290" y1="40" y2="40"/>{ticks}
      <rect class="b2" x="220" y="22" width="70" height="14"/><text class="lb" x="290" y="17" text-anchor="end">pomocnicza 0–1</text>
      <rect class="b1" x="214" y="18" width="12" height="22"/><text class="lb" x="208" y="17" text-anchor="end">prowadząca ~1</text>
      <text class="lb" x="10" y="72">RIR: poprawne powtórzenia w zapasie</text></svg>'''
    return f'''<div class="pgx"><div class="in">
  {head('01 · Wysiłek, Hard Set i upadek mięśniowy', 'HARDSET')}
  <div class="cols">
    <div class="main">
      <h2>Wysiłek: RIR i Hard Set</h2>
      <p class="lead">Hard Set to prawdziwa seria robocza: powtarzalna technika, wysiłek odpowiedni do ćwiczenia i jasny cel. Rozgrzewka się nie liczy.</p>
      <div class="stats">{stat('2', 'serie', 'na ćwiczenie, domyślnie')}{stat('~1', 'RIR', 'seria prowadząca')}{stat('0–1', 'RIR', 'seria pomocnicza, gdy stop jest bezpieczny')}</div>
      <h4>Gdzie leży cel wysiłku</h4>{scale}
      <table class="dt"><caption>Domyślna architektura wysiłku</caption><thead><tr><th>Seria</th><th>Cel</th><th>Rola</th></tr></thead>
      <tbody><tr><td>Hard Set 1</td><td class="ac">~1 RIR</td><td>Lead Set, główny sygnał progresji</td></tr><tr><td>Hard Set 2</td><td class="ac">0–1 RIR</td><td>Supporting Set, bez zbędnych prób</td></tr></tbody></table>
    </div>
    <aside class="side"><h3>Co z tego wynika</h3>
      <ul class="chk"><li>{icon('check')}<span>Liczy się seria zgodna ze standardem ruchu, a nie sam fakt zmęczenia.</span></li>
      <li>{icon('check')}<span>0 RIR tylko wtedy, gdy możesz bezpiecznie zakończyć serię.</span></li>
      <li>{icon('check')}<span>Ciężkie ruchy ze swobodną sztangą: 1–2 RIR w obu seriach.</span></li></ul>
      <div class="tags">{tag('study', 'Badanie')}<cite>R04, R19, R20</cite></div>
      <p class="small">RIR jest szacunkiem. W badaniu Mansfielda uczestnicy częściej zaniżali faktyczny zapas.</p>
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
        bars += f'<rect class="fl base {cls}" x="{x}" y="{80 - (lo - 80) * 4.4:g}" width="40" height="{(lo - 80) * 4.4:g}"/><rect class="fl {cls}" x="{x}" y="{y:g}" width="40" height="{h:g}"/>'
        bars += f'<text x="{x + 20}" y="{y - 4:g}" text-anchor="middle" class="vl">{lo}–{hi}%</text><text x="{x + 20}" y="92" text-anchor="middle" class="lb">{lab}</text>'
    chart = f'<svg class="chart" viewBox="0 0 280 96" role="img" aria-label="Singiel poniedziałkowy w procentach bazy fali, T1 do T4"><line class="ax" x1="14" x2="270" y1="80" y2="80"/>{bars}</svg>'
    tl = ''.join(f'<li class="{"hi" if i == 2 else ""}"><b>{t}</b><span>{d}</span></li>' for i, (t, d) in enumerate([
        ('T1', 'więcej powtórzeń'), ('T2', 'rośnie ciężar'), ('T3', 'najcięższa ekspozycja i seria kontrolna'), ('T4', 'lżejszy tydzień')]))
    rows = ''.join(f'<tr{" class=hl" if r[0] == "T3" else ""}><td>{r[0]}</td><td class="ac">{r[1]}</td><td class="r">{r[2]}</td><td class="r">{r[3]}</td><td class="r">{r[4]}</td></tr>' for r in [
        ('T1', '1×1 @7', '88–90', '105–107,5', '90–92,5'), ('T2', '1×1 @7,5', '90–91', '107,5–110', '92,5–97,5'),
        ('T3', '1×1 @8', '91–93', '110–112,5', '97,5–102,5'), ('T4', '1×1 @6–7', '85–88', '102,5–105', '87,5–92,5')])
    return f'''<div class="pgx"><div class="in">
  {head('03 · Fala czterotygodniowa', 'BENCH PRIORITY')}
  <div class="cols">
    <div class="main">
      <h2>Fala czterotygodniowa</h2>
      <ol class="tl">{tl}</ol>
      <h4>Singiel w poniedziałek, % bazy fali</h4>{chart}
      <table class="dt"><caption>Poniedziałek · przykład dla bazy 120 kg</caption><thead><tr><th>Tydz.</th><th>Singiel</th><th class="r">% bazy</th><th class="r">Singiel kg</th><th class="r">Back-off kg</th></tr></thead><tbody>{rows}</tbody></table>
    </div>
    <aside class="side"><h3>Gdy RPE nie zgadza się z tabelą</h3>
      <div class="two"><div><b>Za ciężko</b><p>RPE wyższe o stopień lub więcej: zdejmij 2,5–5%.</p></div><div><b>Za lekko</b><p>Pełny punkt poniżej celu: następna seria o około 2,5% więcej. Dwa punkty: około 5%, to limit.</p></div></div>
      <div class="tags">{tag('hypothesis', 'Hipoteza programu')}</div>
      <p class="small">Nie dotyczy singla, serii kontrolnej ani tygodnia 4. Technika w normie, prędkość sztangi nie spada.</p>
      <div class="quote">Procent wyznacza punkt startowy. RPE wyznacza granicę.</div></aside>
  </div>{foot(13)}</div></div>'''


def page_amrap():
    pts = [(4, 116.7), (5, 120.0), (6, 123.3), (7, 126.7)]
    xs = lambda r: 30 + (r - 4) * 70
    ys = lambda v: 98 - (v - 114) * 6.2
    poly = ' '.join(f'{xs(r)},{ys(v):.1f}' for r, v in pts)
    dots = ''.join(f'<circle class="{"hi" if r == 5 else ""}" cx="{xs(r)}" cy="{ys(v):.1f}" r="3"/><text x="{xs(r)}" y="{ys(v) - 8:.1f}" text-anchor="middle" class="vl">{str(v).replace(".", ",")}</text><text x="{xs(r)}" y="114" text-anchor="middle" class="lb">{r}</text>' for r, v in pts)
    chart = f'<svg class="chart" viewBox="0 0 260 120" role="img" aria-label="e1RM dla 100 kg przy 1 RIR w zależności od liczby powtórzeń"><line class="ax" x1="14" x2="250" y1="104" y2="104"/><polyline class="ln" points="{poly}"/>{dots}</svg>'
    steps = [('check', 'Technika', 'Ten sam chwyt i ustawienie co w zawodach, pauza na każdym powtórzeniu.'), ('clock', 'Przygotowanie', 'Zwykła rozgrzewka, 4–5 minut odpoczynku, żadnego ciężkiego singla tego dnia.'),
             ('stop', 'Koniec serii', 'Przy 1 powtórzeniu w zapasie albo wcześniej, gdy siada technika.'), ('down', 'Po serii', 'Jedna łatwa seria 1×4 i koniec wyciskania.')]
    st = ''.join(f'<li>{icon(i)}<div><b>{t}</b><p>{d}</p></div></li>' for i, t, d in steps)
    return f'''<div class="pgx"><div class="in">
  {head('04 · AMRAP, e1RM i baza fali', 'BENCH PRIORITY')}
  <div class="cols">
    <div class="main">
      <h2>Seria kontrolna w tygodniu 3</h2>
      <p class="lead">W piątek pierwsza seria robocza to AMRAP przy około 82,5% bazy fali, z jednym powtórzeniem w zapasie (@9). Zastępuje cięższą serię objętościową.</p>
      <ul class="steps">{st}</ul>
      <h4>e1RM dla 100 kg przy @9</h4>{chart}
      <div class="formula">e1RM = ciężar × (1 + (powtórzenia + RIR) / 30)</div>
      <div class="tags">{tag('heuristic', 'Heurystyka')}</div><p class="small">Wzór Epleya służy do sterowania treningiem. Jedno powtórzenie to tu około 3,3 kg szacunku.</p>
    </div>
    <aside class="side"><h3>Kiedy baza rośnie o 2,5 kg</h3>
      <ul class="chk"><li>{icon('check')}<span>Seria kontrolna: co najmniej jedno powtórzenie więcej niż w poprzedniej fali, przy tym samym ciężarze i RIR.</span></li>
      <li>{icon('check')}<span>Singiel z poniedziałku T3 w planowanym RPE, bez obniżania ciężaru.</span></li>
      <li>{icon('check')}<span>Zmiana tylko na wejściu do nowej fali. T4 robisz na starej bazie.</span></li></ul>
      <div class="tags">{tag('hypothesis', 'Hipoteza programu')}</div>
      <div class="tags">{tag('study', 'Badanie')}<cite>Refalo 2024</cite></div>
      <p class="small">24 osoby, 75% 1RM: błąd przewidywania zapasu około 0,65 powtórzenia.</p></aside>
  </div>{foot(15)}</div></div>'''


def page_ledger():
    days = ['Pn', 'Sr', 'Pt']
    order = ['Chest', 'Back', 'Lateral Delts', 'Elbow Extensors', 'Elbow Flexors', 'Rear Delts', 'Quadriceps', 'Hamstrings', 'Glutes']
    body = ''
    for name in order:
        e = LEDGER[name]['exposures']
        pr = LEDGER[name]['priority']
        cells = ''.join(f'<td>{"<i class=m>" + e[d] + "</i>" if d in e else "<i class=m0>·</i>"}</td>' for d in days)
        mark_ = ' <em>z wyciskaniem</em>' if name == 'Chest' else ''
        body += f'<tr><td>{name}{mark_}</td><td>{pr}</td>{cells}</tr>'
    r_ = 38
    c = 2 * math.pi * r_
    donut = f'<svg class="chart donut" viewBox="0 0 120 120" role="img" aria-label="7 z 35 serii tygodnia to wyciskanie"><circle class="dn0" cx="60" cy="60" r="{r_}"/><circle class="dn1" cx="60" cy="60" r="{r_}" stroke-dasharray="{c * 0.2:.1f} {c:.1f}" transform="rotate(-90 60 60)"/><text x="60" y="62" text-anchor="middle" class="dv">7/35</text><text x="60" y="76" text-anchor="middle" class="lb">wyciskanie</text></svg>'
    bars = ''.join(f'<rect class="fl {"hi" if i == 0 else ""}" x="{12 + i * 56}" y="{90 - h * 5:g}" width="40" height="{h * 5:g}"/><text x="{32 + i * 56}" y="{86 - h * 5:g}" text-anchor="middle" class="vl">{h}</text><text x="{32 + i * 56}" y="106" text-anchor="middle" class="lb">{d}</text>' for i, (d, h) in enumerate([('Pn', 11), ('Sr', 12), ('Pt', 12)]))
    bar = f'<svg class="chart" viewBox="0 0 180 112" role="img" aria-label="Serie w poniedziałek, środę, piątek: 11, 12, 12"><line class="ax" x1="4" x2="176" y1="90" y2="90"/>{bars}</svg>'
    return f'''<div class="pgx"><div class="in">
  {head('05 · Tydzień w liczbach', 'BENCH PRIORITY')}
  <div class="cols">
    <div class="main">
      <h2>Gotowy tydzień: 3 × 60 minut</h2>
      <div class="stats">{stat('35', 'serii', 'w tygodniu: 11 + 12 + 12')}{stat('3×60', 'min', 'z rozgrzewką, do sprawdzenia')}{stat('7', 'serii', 'wyciskania zawodniczego')}</div>
      <table class="dt mx"><caption>Ekspozycje w tygodniu (P = główna, S = pomocnicza)</caption><thead><tr><th>Obszar</th><th>Priorytet</th><th>Pn</th><th>Śr</th><th>Pt</th></tr></thead><tbody>{body}</tbody></table>
      <div class="two2"><div><h4>Serie na trening</h4>{bar}</div><div>{donut}</div></div>
    </div>
    <aside class="side"><h3>Dla kogo ten tydzień</h3>
      <ul class="chk"><li>{icon('clock')}<span>Trzy treningi po najwyżej 60 minut.</span></li><li>{icon('bar')}<span>Priorytet: wyciskanie leżąc.</span></li>
      <li>{icon('check')}<span>Rear Delts i Glutes mają status Optional. To skutek limitu czasu, a nie ocena ich ważności.</span></li></ul>
      <div class="tags">{tag('exception', 'Wyjątek siłowy')}</div><p class="small">Serie wyciskania zawodniczego (RPE 6–8) liczą się do Chest P. To wyjątek od standardu Hard Set, nie wynik badania.</p>
      <div class="note">Walidator: PASS strukturalny. To nie jest ocena biomechaniczna ani medyczna.</div></aside>
  </div>{foot(21)}</div></div>'''


PAGES = [('Okładka: HARDSET', cover_hardset), ('Okładka: Continuous Bench Priority', cover_bench), ('Spis treści i legenda', page_toc),
         ('Rozdział z panelem wniosków', page_effort), ('Fala: oś czasu, wykres, tabela', page_wave),
         ('Seria kontrolna: kroki, wykres, reguły', page_amrap), ('Tydzień: macierz ekspozycji i wykresy', page_ledger)]

CSS = '''
:root{--page:#E7E6E3;--ink:#18191A;--soft:#55585B;--rule:#C4C3BF;--sans:'Archivo','Arial Narrow',sans-serif;--mono:'IBM Plex Mono','Courier New',monospace;--acc:#5A8663;--acct:#3F6B4A;--accd:#8FB59A}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:400 16px/1.5 var(--sans);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 64px}
.wrap{max-width:1160px;margin:0 auto}
h1{font:800 38px/1.05 var(--sans);font-stretch:112%;margin:0 0 12px;text-wrap:balance}
.intro{max-width:66ch;margin:0 0 20px}
.sec{font:600 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--soft);margin:32px 0 10px}
.feat{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin:0 0 24px;border-top:2px solid var(--ink)}
.feat div{padding:14px 16px 14px 0}.feat b{font:600 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;display:block;margin-bottom:6px}.feat p{margin:0;font-size:15px;color:var(--soft)}
.ctl{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 12px;font:500 12px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.ctl button{font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--ink);background:transparent;color:var(--ink);padding:9px 12px;cursor:pointer;display:inline-flex;gap:8px;align-items:center}
.ctl button[aria-pressed=true]{background:var(--ink);color:var(--page)}
.ctl button:focus-visible,.zoom:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.ctl i{width:12px;height:12px;display:inline-block;border:1px solid var(--ink)}
table.ac{border-collapse:collapse;width:100%;max-width:900px;font:400 13px/1.3 var(--mono);margin-bottom:8px}
table.ac th{font:600 11px var(--sans);letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px}
table.ac td{padding:7px 8px;border-bottom:1px solid var(--rule)}
table.ac .r{text-align:right;font-variant-numeric:tabular-nums}
table.ac i{display:inline-block;width:18px;height:18px;border:1px solid var(--rule);vertical-align:middle;margin-right:6px}
.v{font:500 11px var(--mono);padding:2px 6px;border:1px solid currentColor;white-space:nowrap}.v.ok{color:#2F6B3A}.v.mid{color:#8A5A00}
.note2{max-width:70ch;color:var(--soft);font-size:15px}
.row{margin:0 0 28px}
.rowhead{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:22px 0 8px}
.rowhead h3{margin:0;font:800 19px var(--sans);font-stretch:112%}
.zoom{font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--ink);background:transparent;color:var(--ink);padding:6px 10px;cursor:pointer}
.pair{display:grid;grid-template-columns:repeat(2,minmax(0,560px));gap:14px;justify-content:start;margin-top:26px}
.pair.stack{grid-template-columns:minmax(0,760px)}
.pwrap{position:relative;min-width:0}
.pwrap>b{position:absolute;left:0;top:-16px;font:500 11px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--soft)}
/* page: B5 portrait 176 x 250 mm */
.pgx{container-type:inline-size;aspect-ratio:176/250;position:relative;overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,.16);background:var(--bg);color:var(--fg)}
.light{--bg:#F3F4F4;--fg:#101214;--panel:#101214;--panelfg:#ECEEEF;--mid:#B9C0C4;--line:#CBD0D3;--muted:#5F686D;--tint:#E3E6E8;--a:var(--acc);--at:var(--acct)}
.dark{--bg:#101214;--fg:#ECEEEF;--panel:#1D2124;--panelfg:#ECEEEF;--mid:#4B5359;--line:#30363A;--muted:#9AA3A8;--tint:#1A1E21;--a:var(--acc);--at:var(--accd)}
.pgx .in{position:absolute;inset:0;padding:7.5cqw 7cqw 8cqw 8cqw;font:400 1.95cqw/1.5 var(--sans);display:flex;flex-direction:column}
.ph{display:flex;justify-content:space-between;gap:3cqw;font:600 1.45cqw/1.2 var(--sans);font-stretch:125%;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);border-bottom:.2cqw solid var(--line);padding-bottom:1.6cqw;margin-bottom:4cqw}
.pf{position:absolute;left:8cqw;right:7cqw;bottom:4cqw;display:flex;justify-content:space-between;font:500 1.5cqw var(--mono);color:var(--muted)}
.cols{display:grid;grid-template-columns:1.75fr 1fr;gap:3.4cqw;flex:1;min-height:0;margin-bottom:5.5cqw}
.main{min-width:0}
h2{font:800 4.6cqw/1.06 var(--sans);font-stretch:112%;margin:0 0 2cqw}
h2.big{font-size:9cqw;font-stretch:125%;letter-spacing:.02em;margin-bottom:5cqw;text-transform:uppercase}
h3{font:700 1.8cqw/1.25 var(--sans);font-stretch:125%;letter-spacing:.08em;text-transform:uppercase;margin:0 0 1.6cqw}
h4{font:600 1.5cqw/1.2 var(--sans);font-stretch:125%;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:3cqw 0 1.2cqw}
p{margin:0 0 1.4cqw}.lead{font-size:2.3cqw;line-height:1.45}.small{font-size:1.55cqw;line-height:1.45;color:var(--muted)}
cite{font:500 1.45cqw var(--mono);font-style:normal;color:var(--at)}
.side{background:var(--panel);color:var(--panelfg);padding:3.4cqw 2.8cqw;display:flex;flex-direction:column;gap:1.2cqw;min-width:0}
.side h3{border-bottom:.2cqw solid var(--mid);padding-bottom:1.4cqw}
.side .small{color:var(--panelfg);opacity:.8}
.side .tg.study,.side .tg.decision,.side .tg.heuristic,.side .tg.hypothesis{color:var(--panelfg)}
.side .tg.exception,.side cite{color:var(--accd)}
.light .side .tg.exception,.light .side cite{color:var(--accd)}
.panel{background:var(--panel);color:var(--panelfg);padding:3.4cqw 3.6cqw;margin-top:auto;margin-bottom:5cqw}
.panel h3{border-bottom:.2cqw solid var(--mid);padding-bottom:1.4cqw}.panel .tg{color:var(--panelfg)}.panel .tg.exception{color:var(--accd)}
.note{border:.2cqw solid var(--mid);padding:1.4cqw 1.6cqw;font:400 1.5cqw/1.45 var(--sans);margin-top:auto}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:2.2cqw;margin:2.2cqw 0 1cqw}
.stat{border-top:.5cqw solid var(--fg);padding-top:1.2cqw}
.stat .n{font:800 5.6cqw/1 var(--sans);font-stretch:112%}.stat small{font:500 1.8cqw var(--mono);margin-left:.6cqw;color:var(--at)}
.stat p{font:400 1.5cqw/1.35 var(--sans);color:var(--muted);margin:.8cqw 0 0}
.dt{border-collapse:collapse;width:100%;font:400 1.55cqw/1.3 var(--mono);margin-top:2cqw}
.dt caption{caption-side:top;text-align:left;font:600 1.4cqw var(--sans);font-stretch:125%;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding-bottom:1.1cqw}
.dt th{font:600 1.3cqw var(--sans);letter-spacing:.06em;text-transform:uppercase;text-align:left;background:var(--fg);color:var(--bg);padding:1.1cqw 1.2cqw}
.dt td{padding:1cqw 1.2cqw;border-bottom:.18cqw solid var(--line)}
.dt .r,.dt th.r{text-align:right}.dt .ac{color:var(--at)}
.dt tr.hl td{background:var(--tint)}
.dt.mx td{text-align:center}.dt.mx td:first-child{text-align:left}.dt.mx td:nth-child(2){text-align:left;color:var(--muted)}
.dt.mx em{font:italic 400 1.35cqw var(--sans);color:var(--muted)}
.m{font-style:normal;font-weight:600;display:inline-block;min-width:2.6cqw;padding:.2cqw .5cqw;background:var(--fg);color:var(--bg)}
.m0{font-style:normal;color:var(--mid)}
.tags{display:flex;flex-wrap:wrap;gap:1cqw;align-items:center;margin:.8cqw 0}
.tg{display:inline-block;font:500 1.3cqw/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;padding:.7cqw 1cqw;border:.2cqw solid currentColor;white-space:nowrap}
.tg.study{color:var(--muted)}.tg.decision{color:var(--fg)}.tg.heuristic{color:var(--muted);border-style:dotted}.tg.exception{color:var(--at)}.tg.hypothesis{border-style:dashed;color:var(--fg)}
.chk{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1.6cqw}
.chk li{display:grid;grid-template-columns:2.6cqw 1fr;gap:1.2cqw;font:400 1.6cqw/1.4 var(--sans)}
.ic{width:2.6cqw;height:2.6cqw;color:var(--accd)}
.chart{width:100%;height:auto;display:block;color:var(--fg)}
.chart .ax{stroke:var(--fg);stroke-width:.8}.chart .tk{stroke:var(--fg);stroke-width:.8}
.chart text{font:500 6.6px var(--mono);fill:var(--fg)}.chart .lb{fill:var(--muted)}.chart .vl{font-size:6.8px}
.chart .fl{fill:var(--fg)}.chart .fl.base{fill:var(--mid)}.chart .fl.hi{fill:var(--a)}.chart .fl.base.hi{fill:var(--a);opacity:.45}
.chart .b1{fill:var(--a)}.chart .b2{fill:var(--mid)}
.chart .ln{fill:none;stroke:var(--fg);stroke-width:1.4}.chart .ln~circle{fill:var(--fg)}.chart circle.hi{fill:var(--a)}
.donut{max-width:30cqw;margin:auto}.chart circle.dn0{fill:none;stroke:var(--mid);stroke-width:12}.chart circle.dn1{fill:none;stroke:var(--a);stroke-width:12}.chart .dv{font:800 15px var(--sans)}
.two2{display:grid;grid-template-columns:1.4fr 1fr;gap:3cqw;align-items:end}
.tl{list-style:none;margin:1.4cqw 0 0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);border-top:.5cqw solid var(--fg)}
.tl li{padding:1.4cqw 1.2cqw 0 0;position:relative}.tl li::before{content:"";position:absolute;left:0;top:-1.4cqw;width:2.2cqw;height:2.2cqw;background:var(--fg)}
.tl li.hi::before{background:var(--a)}
.tl b{font:800 2.8cqw var(--sans);font-stretch:112%;display:block;margin-top:.8cqw}.tl span{font:400 1.45cqw/1.35 var(--sans);color:var(--muted)}
.two{display:grid;grid-template-columns:1fr;gap:1.6cqw}.two div{border-top:.3cqw solid var(--accd);padding-top:1cqw}.two b{font:700 1.5cqw var(--sans);font-stretch:125%;text-transform:uppercase;letter-spacing:.06em}.two p{font:400 1.5cqw/1.4 var(--sans);margin:.4cqw 0 0}
.quote{font:600 2.2cqw/1.3 var(--sans);font-stretch:112%;border-left:.7cqw solid var(--accd);padding-left:2cqw;margin-top:auto}
.steps{list-style:none;margin:2cqw 0 0;padding:0;display:flex;flex-direction:column;gap:1.8cqw}
.steps li{display:grid;grid-template-columns:4.4cqw 1fr;gap:1.8cqw;border-top:.2cqw solid var(--line);padding-top:1.4cqw}.steps .ic{width:4cqw;height:4cqw;color:var(--at)}
.steps b{font:700 1.6cqw var(--sans);font-stretch:125%;text-transform:uppercase;letter-spacing:.06em}.steps p{font:400 1.6cqw/1.4 var(--sans);margin:.3cqw 0 0}
.formula{font:500 1.7cqw var(--mono);background:var(--tint);padding:1.6cqw 2cqw;margin:2cqw 0 1.4cqw}
.toc{list-style:none;margin:0 0 4cqw;padding:0}.toc li{display:grid;grid-template-columns:5cqw 1fr;gap:1.4cqw;padding:1.5cqw 0;border-bottom:.2cqw solid var(--line);font:600 2.3cqw var(--sans)}
.toc b{font:500 1.8cqw var(--mono);color:var(--at)}.toc i{display:none}
.cover .in{padding:8cqw 8cqw}
.cv-top{display:flex;justify-content:space-between;font:600 1.5cqw var(--sans);font-stretch:125%;letter-spacing:.16em}
.cv-title{margin-top:30cqw}.cv-title .logo{width:100%;height:auto;display:block}
.cv-sub{font:700 2.6cqw var(--sans);font-stretch:125%;letter-spacing:.3em;margin-top:5cqw}
.cv-p{font:400 2.1cqw/1.5 var(--sans);color:var(--muted);margin-top:3.4cqw;max-width:104cqw}
.ruler{position:absolute;left:8cqw;right:8cqw;bottom:20cqw;width:84cqw;height:auto}.ruler .ax,.ruler .tk{stroke:var(--fg);stroke-width:.6}.ruler text{font:500 4px var(--mono);fill:var(--fg)}.ruler .cap{fill:var(--muted)}.ruler .blk{fill:var(--a)}
.cv-foot{position:absolute;left:8cqw;right:8cqw;bottom:8cqw;display:flex;justify-content:space-between;align-items:flex-end;font:500 1.6cqw var(--mono);color:var(--muted)}.cv-foot .mark{width:9cqw;height:9cqw}
.cv-lock{margin-top:14cqw;display:flex;flex-direction:column;gap:2.4cqw;width:52%}.cv-lock .logo{width:100%;height:auto}.cv-lock span{font:600 1.7cqw var(--sans);font-stretch:125%;letter-spacing:.3em}
.cv-title2{font:800 8.4cqw/1.05 var(--sans);font-stretch:125%;letter-spacing:.04em;text-transform:uppercase;margin-top:9cqw}
.wavec{position:absolute;left:8cqw;width:84cqw;bottom:21cqw;height:auto}.wavec .ax{stroke:var(--fg);stroke-width:.5}.wavec text{font:500 4px var(--mono);fill:var(--fg)}.wavec .fl{fill:var(--fg)}.wavec .blk{fill:var(--a)}
@media (max-width:760px){.pair{grid-template-columns:minmax(0,1fr)}h1{font-size:30px}}
'''

JS = '''
document.querySelectorAll('.zoom').forEach(function(b){b.addEventListener('click',function(){var p=b.closest('.row').querySelector('.pair');var s=p.classList.toggle('stack');b.textContent=s?'Zmniejsz':'Powiększ';});});
document.querySelectorAll('.ctl [data-acc]').forEach(function(b){b.addEventListener('click',function(){var r=document.documentElement.style;r.setProperty('--acc',b.dataset.acc);r.setProperty('--acct',b.dataset.acct);r.setProperty('--accd',b.dataset.accd);document.querySelectorAll('.ctl [data-acc]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});});});
'''


def accent_table():
    rows = ''
    for a in ACCENTS:
        cb, cw = k.contrast(a['acc'], BLACK), k.contrast(a['acc'], WHITE)
        ct, cd = k.contrast(a['acct'], WHITE), k.contrast(a['accd'], PANEL)
        v = lambda r: '<span class="v ok">tekst</span>' if r >= 4.5 else ('<span class="v mid">duży tekst, elementy</span>' if r >= 3 else '<span class="v">tylko wypełnienie</span>')
        rows += (f'<tr><td><i style="background:{a["acc"]}"></i>{a["name"]} {a["acc"]}</td><td class="r">{cb:.2f}:1 {v(cb)}</td><td class="r">{cw:.2f}:1 {v(cw)}</td>'
                 f'<td class="r"><i style="background:{a["acct"]}"></i>{a["acct"]} {ct:.2f}:1</td><td class="r"><i style="background:{a["accd"]}"></i>{a["accd"]} {cd:.2f}:1</td></tr>')
    return f'<table class="ac"><thead><tr><th>Akcent (wypełnienia)</th><th class="r">Na czerni #101214</th><th class="r">Na bieli #F3F4F4</th><th class="r">Tekst na jasnym</th><th class="r">Tekst na ciemnym panelu</th></tr></thead><tbody>{rows}</tbody></table>'


def main():
    (HERE / 'logos').mkdir(exist_ok=True)
    a0 = ACCENTS[0]
    (HERE / 'logos' / 'hardset-wordmark-on-light.svg').write_text(L.svg(L.wordmark(BLACK, a0['acct']), pad=24, bg=WHITE), encoding='utf-8')
    (HERE / 'logos' / 'hardset-wordmark-on-dark.svg').write_text(L.svg(L.wordmark(WHITE, a0['acc']), pad=24, bg=BLACK), encoding='utf-8')
    (HERE / 'logos' / 'hardset-mark.svg').write_text(L.svg(L.mark(BLACK, WHITE, a0['accd'])), encoding='utf-8')
    rows = ''
    for title, fn in PAGES:
        html = fn()
        rows += f'''<div class="row"><div class="rowhead"><h3>{title}</h3><button class="zoom" type="button">Powiększ</button></div>
<div class="pair"><div class="pwrap"><b>Jasna</b><div class="light">{html}</div></div><div class="pwrap"><b>Ciemna</b><div class="dark">{html}</div></div></div></div>'''
    acc = ''.join(f'<button type="button" data-acc="{a["acc"]}" data-acct="{a["acct"]}" data-accd="{a["accd"]}" aria-pressed="{"true" if i == 0 else "false"}"><i style="background:{a["acc"]}"></i>{a["name"]}</button>' for i, a in enumerate(ACCENTS))
    page = f'''<title>HARDSET Raport Pion</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style>
<div class="wrap" lang="pl">
<h1>Raport w pionie, nowa typografia i logo</h1>
<p class="intro">Format B5 w pionie (176 × 250 mm). Krój Archivo na nagłówki, etykiety i tekst, IBM Plex Mono na liczby. Logo jest narysowane z konturów Archivo Expanded ExtraBold z szerokim rozstrzeleniem, jak tytuły w twoich przykładach. Dwie kreski pod napisem to Lead Set i Supporting Set. Okładki mają własną grafikę: skalę RIR w pierwszej książce i prawdziwy wykres fali w drugiej.</p>
<div class="feat">
<div><b>Tytuły</b><p>Szeroki, ciężki, wersaliki z rozstrzałem. Nagłówki rozdziałów w węższej szerokości tego samego kroju.</p></div>
<div><b>Tekst</b><p>Archivo normalnej szerokości. Krótkie akapity, wyjaśnienia w panelu obok.</p></div>
<div><b>Liczby</b><p>IBM Plex Mono w tabelach i wskaźnikach, żeby cyfry się wyrównywały.</p></div>
<div><b>Akcent</b><p>Jeden zgaszony zielony, tak dobrany, żeby działał jako wypełnienie na czerni i na bieli.</p></div>
</div>
<div class="sec">Akcent: trzy zgaszone zielenie</div>
<div class="ctl" role="group" aria-label="Kolor akcentu"><span>Pokaż na stronach:</span>{acc}</div>
{accent_table()}
<p class="note2">Żaden kolor średniej jasności nie da 4,5:1 jednocześnie na czerni i na bieli, bo fizycznie nie ma takiej wartości (najlepszy kompromis to około 4:1 na obu). Dlatego akcent służy do wypełnień i dużych elementów, a mały tekst w kolorze akcentu używa ciemniejszego odcienia na jasnym i jaśniejszego na ciemnym tle.</p>
{rows}
</div>
<script>{JS}</script>'''
    (HERE / 'index.html').write_text(page, encoding='utf-8')
    print('wrote', HERE / 'index.html')


if __name__ == '__main__':
    main()
