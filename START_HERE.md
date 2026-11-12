# START HERE — HARDSET Knowledge Pack v1.0

## Purpose

Kompletna, samodzielna baza zasad **HARDSET** do użycia w Claude Chat / Claude Projects / Claude Code. Obejmuje **9 zatwierdzonych rozdziałów (na poziomie zasad)**, aneksy, 30 zweryfikowanych naukowych źródeł, 38 pozycji matrycy dowodów, opis konstrukcji planów, audyt P/S oraz uruchamialny **prototyp walidatora strukturalnego**.

**Paczka nie zawiera żadnego profilu ani planu treningowego konkretnej osoby.** Nowy program należy projektować od zera.

## Najprostsza opcja — Claude Chat

1. Prześlij do czatu plik **`HARDSET_MASTER.md`**. To kompletny tekst zasad, aneksów, bibliografii i reguł audytu w jednym dokumencie.
2. Wklej tekst z `claude/CLAUDE_CHAT_START_PROMPT.md`.
3. Poproś Claude o krótkie potwierdzenie liczby rozdziałów, 12 obszarów Fixed Core, zasad P/S i trybów oceny wyników, **zanim** zacznie układać plan.
4. Dopiero wtedy odpowiedz na nowe pytania o profil treningowy.

**Uwaga:** jeśli Claude Chat nie potrafi korzystać z przesłanych plików, można wkleić tekst `HARDSET_MASTER.md` bezpośrednio, a potem prompt. Przy zbyt małym oknie kontekstu użyj projektu z plikami; nie twierdź, że załadował materiał, którego nie dostał.

## Claude Projects

1. Utwórz nowy projekt HARDSET.
2. Dodaj `HARDSET_MASTER.md` do plików wiedzy projektu albo odpowiednie pliki `chapters`, `appendices`, `research` i `validation`.
3. Użyj `CLAUDE.md` jako instrukcji projektu (lub skopiuj go do ustawień instrukcji projektu, jeśli wymagane).
4. W nowym czacie rozpocznij od promptu `claude/CLAUDE_CHAT_START_PROMPT.md`.

## Claude Code

1. Rozpakuj ZIP do katalogu projektu, zachowując strukturę.
2. Otwórz Claude Code w katalogu zawierającym `CLAUDE.md`.
3. Poleć: 'Read CLAUDE.md and START_HERE.md, then all 9 chapter files and research matrix. Report any contradictions; do not assume a user profile.'
4. Uruchom testy:

   ```bash
   python -m unittest discover -s validation/tests -v
   python validation/validator.py examples/generic_pass.json
   ```

5. Program użytkownika twórz **dopiero po osobnym wywiadzie**. Validator działa tylko na oznaczonych danych i nie jest silnikiem automatycznego doboru P/S.

## Struktura paczki

```text
HARDSET_MASTER.md           — jedno wejście dla Claude Chat
CLAUDE.md                   — stałe instrukcje
START_HERE.md               — instrukcja uruchomienia
README.md                   — indeks i zakres
PROVENANCE.md               — pochodzenie/ograniczenia rekonstrukcji
CHANGELOG.md                — historia wydania
chapters/01...09             — zatwierdzone reguły rozdziałów
appendices/                 — 5 aneksów pomocniczych
research/REFERENCES.md      — 30 publikacji, DOI i interpretacja
research/EVIDENCE_MATRIX.md — 38 reguł/tez z typem dowodu
research/RESEARCH_AUDIT.md  — metoda weryfikacji i wycofane źródło
validation/README.md        — walidator CLI i zakres
validation/SCHEMA.md        — kontrakt wejścia/wyjścia
validation/RULE_CATALOG.md  — automatyzacja vs osąd ekspercki
validation/validator.py     — deterministyczny prototyp
validation/tests/           — testy
examples/                   — wyłącznie syntetyczne JSON-y
claude/                     — prompt handoff
```

## Czego paczka nie robi

Nie zawiera danych osobowych, gotowego planu dla konkretnej osoby, katalogu automatycznie klasyfikowanych ćwiczeń, aplikacji, ebooka ani medycznego systemu oceny bezpieczeństwa. Nie zapewnia też, że ChatGPT/Claude przeczytał wszystkie pliki; sprawdź to w nowym czacie.
