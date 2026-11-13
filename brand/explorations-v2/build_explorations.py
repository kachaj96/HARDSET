#!/usr/bin/env python3
"""Builds brand/explorations-v2/index.html (four style directions) and logos/*.svg.

Run: python3 brand/explorations-v2/build_explorations.py
Logos come from logo_kit.py (constructed letterforms), contrast ratios are computed here.
"""
import html
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import logo_kit as k  # noqa: E402

# ---------------------------------------------------------------- directions
# Two base colours (black + one neutral family) and one accent.
DIRS = [
    dict(id='stal', n=1, name='Stal', line='Czerń i stal, akcent sygnałowa pomarańcza. Najbardziej techniczny.',
         black='#101214', light='#ECEEEF', mid='#B9C0C4', muted='#5F686D', acc='#FF5B1F', acc_text='#BF3708',
         mid_name='stal', cover1=('black', 'light', 'acc'), cover2=('mid', 'black', 'black')),
    dict(id='beton', n=2, name='Beton', line='Jasny beton i czerń, akcent żółty znak ostrzegawczy. Najbardziej surowy.',
         black='#15171A', light='#E6E3DC', mid='#CBC7BE', muted='#5E5C57', acc='#F2C200', acc_text='#15171A',
         mid_name='beton', cover1=('light', 'black', 'acc'), cover2=('black', 'light', 'acc')),
    dict(id='miedz', n=3, name='Miedź i patyna', line='Zielona czerń i szarość patyny, akcent miedź. Najcieplejszy, wciąż przemysłowy.',
         black='#0D1514', light='#E9EFED', mid='#A9B9B4', muted='#566561', acc='#D9783C', acc_text='#A24E1D',
         mid_name='patyna', cover1=('black', 'light', 'acc'), cover2=('mid', 'black', 'black')),
    dict(id='sygnal', n=4, name='Sygnał', line='Czerń i kość, akcent czerwień. Najbardziej plakatowy, najmniej kolorów.',
         black='#0B0B0C', light='#EDEAE3', mid='#CFCBC2', muted='#5F5D58', acc='#EE3B34', acc_text='#C21F1A',
         mid_name='kość', cover1=('black', 'light', 'acc'), cover2=('light', 'black', 'acc')),
]

COL = lambda d, key: d[key]


def logo_parts(d, on):
    """on: 'dark' or 'light' background. Returns (inner, w, h) for the wordmark."""
    fg = d['light'] if on == 'dark' else d['black']
    acc = d['acc'] if (on == 'dark' or d['id'] in ('stal', 'miedz', 'sygnal')) else d['black']
    acc = d['acc'] if on == 'dark' else d['acc_text']
    i = d['id']
    if i == 'stal':
        return k.wordmark('HARDSET', [fg] * 4 + [acc] * 3, bars=True, bar_color=acc)
    if i == 'beton':
        bar = d['acc']
        inner, w, h = k.wordmark('HARDSET', [fg] * 7, t_over=34)
        inner += f'<rect x="{w - 34 - 74 - 12 - 60 - 12 - 70:g}" y="{k.H + 14}" width="{34 + 74 + 12 + 60 + 12 + 70:g}" height="12" fill="{bar}"/>'
        return inner, w, k.H + 26
    if i == 'miedz':
        return k.stacked([fg] * 4, [acc] * 3, bar=acc)
    if i == 'sygnal':
        return k.wordmark('HARDSET', [fg] * 7, e_split=d['acc'] if on == 'dark' else d['acc_text'])
    raise ValueError(i)


def mark_parts(d, on):
    i = d['id']
    if i == 'stal':
        return k.mark_h2(d['black'], d['light'], d['acc'])
    if i == 'beton':
        return k.mark_h2(d['acc'], d['black'], d['black'])
    if i == 'miedz':
        return k.mark_hs(d['black'], d['light'], d['acc'], bar=d['acc'])
    if i == 'sygnal':
        return k.mark_hs(d['acc'], d['black'], d['black'])
    raise ValueError(i)


def lockup_parts(d, on):
    """Series lockup used on the Bench Priority cover: wordmark + POWERBUILDING label, as SVG text-free bars."""
    inner, w, h = logo_parts(d, on)
    return inner, w, h


def svg_str(parts, pad=0, bg=None, label='HARDSET'):
    inner, w, h = parts
    return k.svg(inner, w, h, pad=pad, bg=bg, label=label)


def svg_inline(parts, cls='lg'):
    inner, w, h = parts
    return f'<svg class="{cls}" viewBox="0 0 {w:g} {h:g}" role="img" aria-label="HARDSET">{inner}</svg>'


# ---------------------------------------------------------------- content
def wave_chart(fg, acc, muted):
    vals = [('T1', 89), ('T2', 90.5), ('T3', 92), ('T4', 86.5)]
    out = []
    for n, (lab, v) in enumerate(vals):
        h = (v - 80) * 6
        x = 20 + n * 52
        col = acc if lab == 'T3' else fg
        out.append(f'<rect x="{x}" y="{100 - h}" width="36" height="{h}" fill="{col}"/>')
        out.append(f'<text x="{x + 18}" y="114" text-anchor="middle" font-size="9" fill="{fg}" font-family="IBM Plex Mono, monospace">{lab}</text>')
    out.append(f'<line x1="14" x2="230" y1="100" y2="100" stroke="{fg}" stroke-width="1"/>')
    return f'<svg class="wave" viewBox="0 0 244 120" role="img" aria-label="Poniedziałkowy singiel, T1 do T4">{"".join(out)}</svg>'


def cover1(d):
    bgk, fgk, acck = d['cover1']
    bg, fg, acc = d[bgk], d[fgk], d[acck]
    on = 'dark' if bgk == 'black' else 'light'
    # mock logo recolored for the cover background
    parts = logo_parts(d, on)
    mk = mark_parts(d, on)
    return f'''<div class="cv" style="--bg:{bg};--fg:{fg};--acc:{acc}"><div class="in">
  <div class="cv-top">ADRIAN DROŻDŻYŃSKI</div>
  <div class="cv-logo">{svg_inline(parts)}</div>
  <div class="cv-sub">Controlled Brutality</div>
  <div class="cv-rule" style="background:{acc}"></div>
  <div class="cv-foot"><span>Metoda treningu<br>hipertroficznego<br>Wersja 1.0</span>{svg_inline(mk, 'mk')}</div>
</div></div>'''


def cover2(d):
    bgk, fgk, acck = d['cover2']
    bg, fg, acc = d[bgk], d[fgk], d[acck]
    on = 'dark' if bgk == 'black' else 'light'
    parts = logo_parts(d, on)
    if d['id'] == 'miedz':   # stacked logo is too tall for a lockup: use its horizontal variant
        fg_l = d['light'] if on == 'dark' else d['black']
        a_l = d['acc'] if on == 'dark' else d['acc_text']
        parts = k.wordmark('HARDSET', [fg_l] * 4 + [a_l] * 3, bars=True, bar_color=a_l)
    return f'''<div class="cv" style="--bg:{bg};--fg:{fg};--acc:{acc}"><div class="in">
  <div class="cv-lock">{svg_inline(parts, 'lg2')}<span>POWERBUILDING</span></div>
  <div class="cv-title">Continuous<br>Bench<br>Priority</div>
  <div class="cv-v">Wersja 1.2 · trzy treningi w tygodniu</div>
  {wave_chart(fg, acc if bgk != 'mid' else d['black'], fg)}
  <div class="cv-top low">ADRIAN DROŻDŻYŃSKI</div>
</div></div>'''


TAGS = [('study', 'Badanie'), ('decision', 'Decyzja HARDSET'), ('heuristic', 'Heurystyka'),
        ('exception', 'Wyjątek siłowy'), ('hypothesis', 'Hipoteza programu'), ('open', 'Do decyzji')]

WAVE_ROWS = [('T1', '1×1 @7', '88–90', '105–107,5'), ('T2', '1×1 @7,5', '90–91', '107,5–110'),
             ('T3', '1×1 @8', '91–93', '110–112,5'), ('T4', '1×1 @6–7', '85–88', '102,5–105')]


def spread(d):
    rows = ''.join(f'<tr{" class=hl" if r[0] == "T3" else ""}><td>{r[0]}</td><td>{r[1]}</td><td class="r">{r[2]}</td><td class="r">{r[3]}</td></tr>' for r in WAVE_ROWS)
    tags = ''.join(f'<span class="tg {c}">{t}</span>' for c, t in TAGS)
    return f'''<div class="spread">
 <div class="pg"><div class="in"><div class="rh"><span>01 · Wysiłek, Hard Set i upadek mięśniowy</span><span>HARDSET</span></div>
  <h4>RIR, czyli zapas powtórzeń</h4>
  <p>RIR (repetitions in reserve) mówi, ile poprawnych powtórzeń zostało jeszcze w zapasie w chwili zakończenia serii.</p>
  <p>RIR jest szacunkiem. Zależy od ćwiczenia, ciężaru, doświadczenia i zmęczenia, więc traktuj go jak sygnał sterujący, a nie pomiar laboratoryjny <cite>[R19, R20]</cite>.</p>
  <p>Powtórzenie wykonane z gorszą techniką nie podnosi wyniku. Granicę serii wyznacza zaplanowany standard ruchu, a nie chwilowy upadek mięśniowy.</p>
  <p><span class="tg decision">Decyzja HARDSET</span> Metoda przyjmuje wysoki wysiłek wokół 1 oraz 0–1 RIR tam, gdzie zakończenie serii jest bezpieczne. Nie twierdzi, że to najlepszy sposób dawkowania wysiłku.</p>
  <div class="pn">6</div></div></div>
 <div class="pg"><div class="in"><div class="rh"><span>03 · Fala czterotygodniowa</span><span>BENCH PRIORITY</span></div>
  <div class="cap">Poniedziałek · przykład dla bazy 120 kg</div>
  <table><thead><tr><th>Tydz.</th><th>Singiel</th><th class="r">% bazy</th><th class="r">kg</th></tr></thead><tbody>{rows}</tbody></table>
  <div class="aside"><b>Nazwa.</b> W trójboju skrót „PB” oznacza rekord życiowy, więc tu mówimy: baza fali (<i>Wave Base</i>).</div>
  <div class="tags">{tags}</div>
  <div class="pn r">7</div></div></div>
</div>'''


def swatches(d):
    items = [('czerń', d['black']), (d['mid_name'] + ' jasna', d['light']), (d['mid_name'] + ' średnia', d['mid']),
             ('szary tekst', d['muted']), ('akcent', d['acc'])]
    out = ''
    for n, c in items:
        tc = d['black'] if k.contrast(c, d['black']) > k.contrast(c, '#ffffff') else '#ffffff'
        out += f'<div class="sw" style="background:{c};color:{tc}"><b>{n}</b><span>{c.upper()}</span></div>'
    return out


def contrast_rows(d):
    pairs = [
        ('tekst na jasnym tle', d['black'], d['light']),
        ('szary tekst na jasnym', d['muted'], d['light']),
        ('jasny tekst na czerni', d['light'], d['black']),
        ('akcent na czerni', d['acc'], d['black']),
        ('akcent na jasnym', d['acc'], d['light']),
        (('akcent do tekstu na jasnym' if d['id'] != 'beton' else 'tekst akcentowy na jasnym (czerń, żółty nie nadaje się)'), d['acc_text'], d['light']),
        ('czerń na akcencie', d['black'], d['acc']),
    ]
    out = ''
    for lab, a, b in pairs:
        r = k.contrast(a, b)
        cls, verdict = ('ok', 'tekst') if r >= 4.5 else (('mid', 'duży tekst, elementy') if r >= 3 else ('no', 'tylko wypełnienie'))
        out += f'<tr><td>{lab}</td><td><i style="background:{a}"></i><i style="background:{b}"></i></td><td class="r">{r:.2f}:1</td><td><span class="v {cls}">{verdict}</span></td></tr>'
    return out


def section(d):
    wm_dark = svg_inline(logo_parts(d, 'dark'))
    wm_light = svg_inline(logo_parts(d, 'light'))
    mk = svg_inline(mark_parts(d, 'dark'), 'mk')
    small = ''.join(f'<span style="width:{w}px">{svg_inline(mark_parts(d, "dark"), "mk")}</span>' for w in (48, 32, 24, 16))
    return f'''
<section class="dir" id="{d['id']}" style="--black:{d['black']};--light:{d['light']};--mid:{d['mid']};--muted:{d['muted']};--acc:{d['acc']};--acct:{d['acc_text']}">
  <header><span class="num">{d['n']}</span><div><h2>{d['name']}</h2><p>{d['line']}</p></div></header>
  <div class="sws">{swatches(d)}</div>
  <h3>Logo</h3>
  <div class="logos">
    <div class="lg-box dark">{wm_dark}</div>
    <div class="lg-box light">{wm_light}</div>
    <div class="lg-box mk-box"><div class="mk-big">{mk}</div><div class="mk-small">{small}</div></div>
  </div>
  <h3>Okładki</h3>
  <div class="covers">{cover1(d)}{cover2(d)}</div>
  <h3>Rozkładówka i tabela</h3>
  {spread(d)}
  <h3>Kontrast</h3>
  <table class="ct"><thead><tr><th>Para</th><th></th><th class="r">Kontrast</th><th>Do czego</th></tr></thead><tbody>{contrast_rows(d)}</tbody></table>
</section>'''


CSS = '''
:root{--page:#E7E6E3;--ink:#18191A;--soft:#55585B;--rule:#C4C3BF;--card:#F4F3F0;--sans:'IBM Plex Sans Condensed','Arial Narrow',sans-serif;--serif:'Source Serif 4',Georgia,serif;--mono:'IBM Plex Mono','Courier New',monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:400 16px/1.5 var(--serif);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 64px}
.wrap{max-width:1100px;margin:0 auto}
h1{font:700 40px/1.05 var(--sans);margin:0 0 12px;text-wrap:balance}
.intro{max-width:62ch;margin:0 0 20px}
.nav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 40px;padding:0;list-style:none}
.nav a{font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink);text-decoration:none;border:1px solid var(--ink);padding:9px 12px}
.nav a:hover,.nav a:focus-visible{background:var(--ink);color:var(--page);outline:none}
.dir{margin:0 0 72px;padding-top:24px;border-top:3px solid var(--ink)}
.dir header{display:flex;gap:16px;align-items:flex-start;margin-bottom:20px}
.num{font:700 56px/0.9 var(--sans);color:var(--ink)}
.dir h2{font:700 32px/1.05 var(--sans);margin:0 0 4px}
.dir header p{margin:0;color:var(--soft);max-width:56ch}
.dir h3{font:600 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--soft);margin:36px 0 12px}
.sws{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:0}
.sw{padding:44px 12px 12px;font:400 12px/1.3 var(--mono);display:flex;flex-direction:column;gap:2px;min-width:0}
.sw b{font:600 13px var(--sans);letter-spacing:.04em;text-transform:uppercase}
.logos{display:grid;grid-template-columns:1.2fr 1.2fr .9fr;gap:12px}
.lg-box{padding:36px 28px;display:flex;align-items:center;justify-content:center;min-width:0}
.lg-box.dark{background:var(--black)}
.lg-box.light{background:var(--light)}
.lg-box.mk-box{background:var(--mid);flex-direction:column;gap:20px}
.lg-box svg.lg{width:100%;max-width:420px;height:auto}
.mk-big svg{width:96px;height:96px;display:block}
.mk-small{display:flex;gap:14px;align-items:flex-end}
.mk-small span{display:block}.mk-small svg{width:100%;height:auto;display:block}
.covers{display:grid;grid-template-columns:repeat(2,minmax(0,300px));gap:20px;justify-content:start}
.cv{container-type:inline-size;aspect-ratio:148/210;background:var(--bg);color:var(--fg);position:relative;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(0,0,0,.14)}
.cv>.in{position:absolute;inset:0;padding:9cqw}
.cv svg.lg{width:100%;height:auto;display:block}
.cv-top{font:500 3cqw/1 var(--mono);letter-spacing:.14em}
.cv-top.low{position:absolute;left:9cqw;bottom:8cqw}
.cv-logo{margin-top:19cqw;width:84%}
.cv-sub{font:italic 400 7.6cqw/1.1 var(--serif);margin-top:7cqw}
.cv-rule{width:36%;height:.9cqw;margin-top:7cqw}
.cv-foot{position:absolute;left:9cqw;right:9cqw;bottom:8cqw;display:flex;justify-content:space-between;align-items:flex-end;font:400 3cqw/1.45 var(--mono)}
.cv-foot svg.mk{width:11cqw;height:11cqw}
.cv-lock{display:flex;align-items:baseline;gap:3cqw;width:100%}
.cv-lock svg{width:44%;height:auto;flex:none}
.cv-lock span{font:500 2.4cqw/1 var(--mono);letter-spacing:.16em}
.cv-title{font:700 17cqw/.92 var(--sans);margin-top:12cqw;letter-spacing:-.01em}
.cv-v{font:400 3cqw/1 var(--mono);margin-top:6cqw}
.cv svg.wave{position:absolute;left:9cqw;bottom:20cqw;width:82cqw;height:auto}
.spread{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px;max-width:760px;background:var(--rule);padding:2px}
.pg{container-type:inline-size;aspect-ratio:148/210;background:var(--light);color:var(--black);position:relative;overflow:hidden}
.pg>.in{position:absolute;inset:0;padding:8cqw 8cqw 9cqw;font:400 3.5cqw/1.5 var(--serif)}
.rh{display:flex;justify-content:space-between;font:600 2.3cqw/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);border-bottom:.3cqw solid var(--mid);padding-bottom:2cqw;margin-bottom:6cqw;gap:2cqw}
.pg h4{font:700 6cqw/1.1 var(--sans);margin:0 0 3cqw}
.pg p{margin:0 0 2.6cqw;text-align:justify;hyphens:auto}
.pg cite{font:500 2.7cqw var(--mono);font-style:normal;color:var(--acct)}
.pn{position:absolute;left:8cqw;bottom:5cqw;font:500 2.5cqw var(--mono);color:var(--muted)}.pn.r{left:auto;right:8cqw}
.cap{font:600 2.5cqw/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:2cqw}
.pg table{border-collapse:collapse;width:100%;font:400 2.9cqw/1.3 var(--mono)}
.pg th{font:600 2.3cqw var(--sans);letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:.5cqw solid var(--black);padding:1.4cqw 1cqw}
.pg td{padding:1.5cqw 1cqw;border-bottom:.25cqw solid var(--mid)}
.pg .r{text-align:right}
.pg tr.hl td{background:var(--mid)}
.pg td:nth-child(2){color:var(--acct)}
.aside{border-left:.7cqw solid var(--acct);padding:1cqw 0 1cqw 3cqw;margin:5cqw 0 4cqw;font:400 3cqw/1.4 var(--sans);color:var(--muted)}
.aside b{color:var(--black)}
.tags{display:flex;flex-wrap:wrap;gap:1.6cqw}
.tg{display:inline-block;font:500 2.2cqw/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;padding:.9cqw 1.6cqw;border:.3cqw solid currentColor;white-space:nowrap;vertical-align:.2cqw;margin-right:1cqw}
.tg.study{color:var(--muted)}
.tg.decision{color:var(--paper-ink,var(--black))}
.tg.heuristic{color:var(--muted);border-style:dotted}
.tg.exception{color:var(--acct)}
.tg.hypothesis{color:var(--black);border-style:dashed}
.tg.open{background:var(--acct);border-color:var(--acct);color:var(--light)}
.ct{border-collapse:collapse;width:100%;max-width:760px;font:400 13px/1.3 var(--mono)}
.ct th{font:600 11px var(--sans);letter-spacing:.08em;text-transform:uppercase;text-align:left;border-bottom:2px solid var(--ink);padding:6px 8px}
.ct td{padding:7px 8px;border-bottom:1px solid var(--rule)}
.ct .r{text-align:right;font-variant-numeric:tabular-nums}
.ct i{display:inline-block;width:18px;height:18px;border:1px solid var(--rule);margin-right:-1px;vertical-align:middle}
.v{font:500 11px var(--mono);padding:2px 6px;border:1px solid currentColor;white-space:nowrap}
.v.ok{color:#2F6B3A}.v.mid{color:#8A5A00}.v.no{color:#9C2B22}
.how{max-width:62ch}.how h2{font:700 26px var(--sans);margin:0 0 8px}
.how li{margin-bottom:6px}
@media (max-width:760px){.logos{grid-template-columns:1fr}.covers{grid-template-columns:1fr 1fr;gap:10px}.spread{grid-template-columns:1fr}h1{font-size:32px}}
@media (max-width:480px){.covers{grid-template-columns:1fr}}
'''


def main():
    (HERE / 'logos').mkdir(exist_ok=True)
    for d in DIRS:
        for on in ('dark', 'light'):
            (HERE / 'logos' / f"{d['id']}-wordmark-on-{on}.svg").write_text(
                svg_str(logo_parts(d, on), pad=24, bg=d['black'] if on == 'dark' else d['light']), encoding='utf-8')
        (HERE / 'logos' / f"{d['id']}-mark.svg").write_text(svg_str(mark_parts(d, 'dark')), encoding='utf-8')
    nav = ''.join(f'<li><a href="#{d["id"]}">{d["n"]} · {d["name"]}</a></li>' for d in DIRS)
    body = ''.join(section(d) for d in DIRS)
    page = f'''<title>HARDSET Style</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap">
<style>{CSS}</style>
<div class="wrap" lang="pl">
<h1>HARDSET: cztery style do wyboru</h1>
<p class="intro">Każdy kierunek ma czerń, drugą rodzinę kolorów i jeden akcent, własne logo i te same treści: okładki obu książek, rozkładówkę z tabelą fali i oznaczenia klas twierdzeń. Logo jest nowe i rysowane od zera: proste kreski, ścięte rogi, bez rodziny fontów.</p>
<ul class="nav">{nav}</ul>
{body}
<div class="how"><h2>Jak wybrać</h2><ol>
<li>Oceń okładki w małym rozmiarze, tak jak zobaczysz je w bibliotece plików.</li>
<li>Sprawdź kontrast: akcent służy do wypełnień i dużych napisów, tekst ciągły jest zawsze czarny albo jasny.</li>
<li>Powiedz numer. Można też połączyć: np. paleta z jednego, logo z drugiego.</li>
</ol></div>
</div>'''
    (HERE / 'index.html').write_text(page, encoding='utf-8')
    print('wrote', HERE / 'index.html')


if __name__ == '__main__':
    main()
