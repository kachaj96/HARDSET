#!/usr/bin/env python3
"""Render library/exercises.json as library/REVIEW.md (review table). Source of truth is the JSON."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'library' / 'exercises.json'
OUT = ROOT / 'library' / 'REVIEW.md'
ORDER = ['Chest', 'Lateral Delts', 'Elbow Extensors', 'Back', 'Rear Delts', 'Elbow Flexors',
         'Quadriceps', 'Hamstrings', 'Glutes', 'Hip Adductors', 'Calves', 'Trunk Musculature']
STATUS = {'proposed': 'do przeglądu', 'approved': 'zatwierdzone', 'rejected': 'odrzucone'}


def primary(ex):
    p = [a for a, t in ex['stimulus'].items() if t == 'P']
    return p[0] if p else next(iter(ex['stimulus']), 'Inne')


def tags(ex, tag):
    return ', '.join(a for a, t in ex['stimulus'].items() if t == tag) or '-'


def render(data):
    groups = {}
    for ex in data['exercises']:
        groups.setdefault(primary(ex), []).append(ex)
    keys = [k for k in ORDER if k in groups] + sorted(k for k in groups if k not in ORDER)
    counts = {}
    for ex in data['exercises']:
        counts[ex['review']['status']] = counts.get(ex['review']['status'], 0) + 1
    out = ['# HARDSET — biblioteka ćwiczeń: przegląd', '',
           f"Wersja {data['version']} · ćwiczeń: {len(data['exercises'])} · "
           + ' · '.join(f"{STATUS.get(k, k)}: {v}" for k, v in sorted(counts.items())), '',
           'Plik generowany z `library/exercises.json` przez `tools/builder/build_library_review.py`. Nie edytuj go ręcznie.', '',
           'Tagi P/S opisują typowe wykonanie i są decyzją planisty, nie uniwersalną prawdą biomechaniczną (Appendix C). '
           'S? nie liczy się do ekspozycji. „Min RIR” to najniższy domyślnie dopuszczalny RIR; 0 oznacza, że stop jest bezpieczny '
           '(bezwarunkowo albo po spełnieniu warunku).', '']
    for k in keys:
        out += [f'## {k}', '', '| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |',
                '|---|---|---|---|---|---|---:|---|---|---|']
        for ex in groups[k]:
            stop = 'tak' if ex['safe_exit'] is True else ('nie' if ex['safe_exit'] is False else 'warunkowo: ' + ex['safe_exit_condition'])
            notes = ex['functional_notes'] or '-'
            name = f"{ex['name_pl']}<br><sub>{ex['name_en']}" + (f" · {ex['variant']}" if ex['variant'] else '') + '</sub>'
            out.append(f"| `{ex['id']}` | {name} | {tags(ex, 'P')} | {tags(ex, 'S')} | {tags(ex, 'S?')} | {stop} | "
                       f"{ex['rir_floor_default']} | {ex['rep_template']} | {notes} | {STATUS.get(ex['review']['status'], ex['review']['status'])} |")
        out.append('')
    return '\n'.join(out)


if __name__ == '__main__':
    text = render(json.loads(SRC.read_text(encoding='utf-8')))
    if '--check' in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text(encoding='utf-8') == text else 1)
    OUT.write_text(text, encoding='utf-8')
    print('Wrote', OUT.relative_to(ROOT))
