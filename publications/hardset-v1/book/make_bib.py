#!/usr/bin/env python3
"""Generate z_bib.html (bibliography R01-R30) from Crossref metadata saved in refs.json.

refs.json comes from research/REFERENCES.md (R##, DOI, verified title) plus Crossref
(authors, journal, volume, issue, pages) fetched 2026-11-13. Run: python3 make_bib.py
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
refs = json.loads((HERE / 'refs.json').read_text(encoding='utf-8'))


def norm(s):
    return re.sub(r'[^a-z0-9]', '', html.unescape(re.sub(r'<[^>]+>', '', s)).lower())


def fixcase(fam):
    if fam.isupper() and len(fam) > 3:
        fam = fam.title()
        if fam.startswith('Mc'):
            fam = 'Mc' + fam[2:].capitalize()
    return fam


def authors(a):
    a = [(fixcase(f), g) for f, g in a]
    names = [f"{fam} {' '.join(p[0] + '.' for p in re.split(r'[ \-]+', giv) if p)}".strip() for fam, giv in a]
    return ', '.join(names) if len(names) <= 3 else ', '.join(names[:3]) + ' i in.'


rows, problems = [], []
for rid, d in refs.items():
    c = d['cr']
    year = re.search(r'\((\d{4})\)', d['head']).group(1)
    ct = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', c['ctitle']))).strip().rstrip('.')
    if rid == 'R20':
        ct = d['title']
    if norm(ct) != norm(d['title']):
        problems.append((rid, ct, d['title']))
    journal = html.unescape(c['journal']).replace('&', '&amp;')
    vol = f", {c['volume']}" if c['volume'] else ''
    iss = f"({c['issue']})" if c['issue'] and c['issue'] != 'Publish Ahead of Print' else ''
    pages = f", {c['page'].replace('-', '–')}" if c['page'] else ''
    online = ' (publikacja online)' if c['issue'] == 'Publish Ahead of Print' or (not c['page'] and rid in ('R20',)) else ''
    if c['journal'].startswith(('BMC', 'Frontiers', 'Sports Medicine - Open')) and not c['page']:
        pages = ''
    rows.append(f'<li><span>{rid}</span><div>{authors(c["authors"])} ({year}). {html.escape(ct)}. <i>{journal}</i>{vol}{iss}{pages}{online}. <span class="doi">doi.org/{d["doi"]}</span></div></li>')

body = f'''<style>@page bib {{ @top-left {{ content: "BIBLIOGRAFIA"; }} }}</style>
<div style="page:bib">
<section class="chap" id="bib">
  <div class="no">Źródła</div>
  <h1>Bibliografia</h1>
  <p class="principle">Cytowanie badania nie nadaje statusu „udowodnione” regule autora.</p>
</section>
<section>
  <p>Trzydzieści prac, numeracja R01–R30 wspólna z matrycą dowodów. Tytuły i DOI sprawdzono w PubMed, PMC lub u wydawców (12 listopada 2026). Autorów, czasopismo, tom, numer i strony pobrano z Crossref 13 listopada 2026. W metadanych Crossref żadna z prac nie ma powiadomienia o wycofaniu ani korekcie. Praca wycofana przez wydawcę, Hughes, Peiffer i Scott (DOI 10.1519/JSC.0000000000003865), nie jest tu cytowana.</p>
  <ol class="bib">
{chr(10).join(rows)}
  </ol>
  <div class="note">Opis wniosków i ich ograniczeń każdej pracy jest w matrycy dowodów. Cytowanie nie zastępuje lektury pracy. Większość badań dotyczy zdrowych dorosłych, więc zastosowanie do rehabilitacji, dzieci, ciąży albo specjalistycznych populacji medycznych wymaga osobnych dowodów i oceny specjalisty.</div>
</section>
</div>
'''
(HERE / 'z_bib.html').write_text(body, encoding='utf-8')
print('wrote z_bib.html', len(rows), 'entries;', 'title mismatches:', problems)
