# Standard redakcyjny HARDSET

Dotyczy obu książek, ich wersji angielskich i każdego tekstu wydawanego pod marką HARDSET.

## 1. Głos

Piszemy jak trener, który zna temat i szanuje czas czytelnika. Zwracamy się na „ty”. Zdania krótkie i średnie na zmianę. Wniosek idzie przed uzasadnieniem.

Tekst ma mówić, co zrobić, kiedy i dlaczego. Jeśli akapit tylko zapowiada, podsumowuje albo zachęca, wypada.

## 2. Zakazy (anti-AI-slop)

Nie używamy:
- pauzy (—). Wtrącenie robimy przecinkiem albo nawiasem, zakres półpauzą (–);
- pustych wzmacniaczy i zapowiedzi: „kluczowy”, „niezwykle”, „warto zauważyć”, „należy podkreślić”, „istotne jest”, „co więcej”, „ponadto”, „podsumowując”, „innymi słowy”, „bez wątpienia”, „tak naprawdę”;
- marketingu: „rewolucyjny”, „odkryj”, „potężny”, „optymalny” bez definicji optimum, „w świecie fitnessu”, „przenieś trening na wyższy poziom”;
- fałszywych kontrastów „to nie X, to Y”, gdy nikt nie twierdził, że to X;
- wyliczanek po trzy tylko dla rytmu;
- pytań retorycznych na początku akapitu;
- wykrzykników;
- zdań, które da się usunąć bez utraty informacji.

Kontrola automatyczna przed każdym składem:

```
sed -e 's/<[^>]*>/ /g' source.html | grep -noiE '—|kluczow|warto (zauważyć|pamiętać|podkreślić)|istotne jest|należy podkreślić|holistyczn|kompleksow|w dzisiejszych|podsumowując|nie tylko[^.]*ale (również|także)|innymi słowy|co więcej|ponadto|niezwykle|rewolucyj|odkryj|potężn|w świecie|zanurz|tak naprawdę|bez wątpienia|optymaln'
```

Pusty wynik jest warunkiem koniecznym. Nie wystarcza. Każdą stronę czyta się jeszcze w całości.

## 3. Trzy klasy twierdzeń i dwie klasy programowe

Każde twierdzenie normatywne ma klasę. Oznaczenie stoi przy pierwszym wystąpieniu w sekcji.

| Oznaczenie | Kiedy | Wymagania |
|---|---|---|
| Badanie | Twierdzenie wynika z opublikowanych prac. | Numer źródła, kogo badano, ograniczenia. Nie rozszerzamy wniosku poza to, co zmierzono. |
| Decyzja HARDSET | Konwencja metody (np. Two-Set Default, Fixed Core 12). | Nie przypisujemy jej dowodu, którego nie ma. |
| Heurystyka | Liczba lub rytm do zmiany w granicach metody. | Mówimy wprost, że można ją zmienić. |
| Wyjątek siłowy | Tylko książka programu: odstępstwo od zasady HARDSET wynikające z celu siłowego. | Nazwana zasada, od której to odstępstwo, i podstawa (Rozdział 08). |
| Hipoteza programu | Tylko książka programu: ustawienie do sprawdzenia w praktyce. | Bez sugerowania, że jest sprawdzone. |
| Do decyzji | Tylko w próbkach i wersjach roboczych. | W wydaniu publicznym nie może wystąpić. |

Twierdzeń oznaczonych w `research/EVIDENCE_MATRIX.md` jako NOT_SUPPORTED nie podajemy jako faktów. Jeśli o nich piszemy, to jako tezy, których dowody nie potwierdzają.

## 4. Źródła

- Cytujemy tylko prace, których metadane sprawdzono w PubMed, Crossref albo u wydawcy: autorzy, rok, tytuł, czasopismo, tom, zeszyt, strony, DOI.
- Przed składem sprawdzamy status wycofania (Retraction Watch, PubMed, strona wydawcy). Data sprawdzenia stoi w kolofonie.
- Praca wycofana nie jest dowodem. Hughes, Peiffer, Scott (2020), DOI 10.1519/JSC.0000000000003865, jest wycofana i nie występuje jako źródło.
- Numeracja R## pochodzi z `research/REFERENCES.md`. Źródła spoza tej listy dostają kreskę zamiast numeru i trafiają do bibliografii książki, w której są użyte.
- Opis badania w tekście podaje to, co zmierzono, i na kim. „U 24 osób trenujących, przy 75% 1RM” zamiast „badania pokazują”.
- Liczby z badań przepisujemy z abstraktu lub pełnego tekstu, nie z omówień.
- Format pozycji: Nazwisko I., Nazwisko I., Nazwisko I. i in. (rok). Tytuł oryginalny. *Czasopismo*, tom(zeszyt), strony. doi.org/…

## 5. Polska typografia

`publications/build.py` robi automatycznie:
- twardą spację po jednoliterowych wyrazach a, i, o, u, w, z;
- twardą spację między liczbą a jednostką (kg, %, min, s, RIR, RPE, powtórzeń, serii);
- blokadę łamania wewnątrz zakresów liczbowych (0–1, 2,5–5).

Ręcznie pilnujemy:
- przecinka dziesiętnego w tekście polskim (82,5%, 2,5 kg) i kropki w angielskim;
- półpauzy w zakresach bez spacji (6–8), a znaku × w zapisie serii (2×5, 100 × 6 przy opisie wyniku);
- cudzysłowów „polskich” w tekście polskim i “English” w angielskim;
- terminów HARDSET po angielsku (Hard Set, Lead Set, Supporting Set, Fixed Core, Priority, Standard, Optional) z polskim objaśnieniem przy pierwszym użyciu;
- jednej nazwy dla jednej rzeczy w całej książce.

## 6. Liczby i przykłady

- Każdy przykład liczbowy podaje bazę („przykład dla bazy 120 kg”).
- Każdą liczbę w tabeli da się odtworzyć ze specyfikacji. Tabele generujemy ze specyfikacji albo sprawdzamy testem (`programs/continuous-bench-priority/tests/`).
- Zaokrąglenia opisujemy wprost (do 2,5 kg).
- Nie dodajemy precyzji, której nie ma w danych: „około 0,65 powtórzenia”, nie „0,6512”.

## 7. Bezpieczeństwo i granice

- Kolofon każdej książki mówi, dla kogo jest tekst, i że nie zastępuje porady lekarza ani fizjoterapeuty.
- Zalecenie pracy blisko upadku zawsze idzie z warunkiem bezpiecznego zakończenia serii.
- Nie piszemy o leczeniu, rehabilitacji, suplementacji ani farmakologii.
- Wynik walidatora (PASS) opisujemy jako zgodność z regułami, nie jako gwarancję efektu.

## 8. Wersja angielska

Przekład robimy z zatwierdzonej wersji polskiej. Ten sam standard obowiązuje po angielsku, z angielską listą zakazów (em dash, „delve”, „crucial”, „robust”, „seamless”, „leverage”, „holistic”, „game-changer”, „unlock”, „It’s worth noting”, „In summary”).
