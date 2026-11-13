#!/usr/bin/env python3
"""Generate z_bib.html for Continuous Bench Priority. Run: python3 make_bib.py"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
E = [
    ('–', 'Currier B. S., McLeod J. C., Banfield L. i in. (2023). Resistance training prescription for muscle strength and hypertrophy in healthy adults: A systematic review and Bayesian network meta-analysis. <i>British Journal of Sports Medicine</i>, 57(18), 1211–1220.', '10.1136/bjsports-2023-106807'),
    ('–', 'Nuzzo J. L., Pinto M. D., Nosaka K. i in. (2024). Maximal number of repetitions at percentages of the one repetition maximum: A meta-regression and moderator analysis of sex, age, training status, and exercise. <i>Sports Medicine</i>, 54(2), 303–321.', '10.1007/s40279-023-01937-7'),
    ('–', 'Refalo M. C., Remmert J. F., Pelland J. C. i in. (2024). Accuracy of intraset repetitions-in-reserve predictions during the bench press exercise in resistance-trained male and female subjects. <i>Journal of Strength and Conditioning Research</i>, 38(3), e78–e85.', '10.1519/JSC.0000000000004653'),
    ('–', 'Winwood P. W., Travis S. K., Barnes M. J. i in. (2026). Tapering and peaking in the weight lifting sports: A systematic review of athletes’ self-reported strategies. <i>Sports Medicine</i>, 56(12), 3099–3123.', '10.1007/s40279-026-02500-w'),
    ('R17', 'Schoenfeld B. J., Grgic J., Ogborn D. i in. (2017). Strength and hypertrophy adaptations between low- vs. high-load resistance training: A systematic review and meta-analysis. <i>Journal of Strength and Conditioning Research</i>, 31(12), 3508–3523.', '10.1519/JSC.0000000000002200'),
]
rows = '\n'.join(f'    <li><span>{r}</span><div>{t} <span class="doi">doi.org/{d}</span></div></li>' for r, t, d in E)
(HERE / 'z_bib.html').write_text(f'''<style>@page bib {{ @top-left {{ content: "BIBLIOGRAFIA"; }} }}</style>
<div style="page:bib">
<section class="chap" id="bib">
  <div class="no">Źródła</div>
  <h1>Bibliografia</h1>
  <p class="principle">Literatura uzasadnia ogólne zasady. Konkretna fala, seria kontrolna i krok bazy są hipotezami programu.</p>
</section>
<section>
  <p>Pozycja R17 pochodzi z bibliografii metody HARDSET v1.0, pozostałe są specyficzne dla tego programu. Tytuły i DOI sprawdzono w listopadzie 2026 roku (PubMed, PMC, wydawcy), dane bibliograficzne w Crossref (13 listopada 2026).</p>
  <ol class="bib">
{rows}
  </ol>
  <div class="note open"><b>Wykluczona praca.</b> Hughes, Peiffer i Scott, <i>Estimating Repetitions in Reserve in Four Commonly Used Resistance Exercises</i> (DOI 10.1519/JSC.0000000000003865), została wycofana przez wydawcę (komunikat DOI 10.1519/JSC.0000000000003977). Nie jest cytowana jako dowód.</div>
  <div class="note">Regulamin federacji (IPF) i regulaminy krajowe nie są cytowane. Książka nie podaje komend ani wymogów technicznych. Przed startem w zawodach sprawdź aktualny regulamin swojej federacji.</div>
</section>
</div>
''', encoding='utf-8')
print('wrote z_bib.html')
