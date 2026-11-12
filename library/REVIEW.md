# HARDSET — biblioteka ćwiczeń: przegląd

Wersja 1.0 · ćwiczeń: 70 · zatwierdzone: 70

Plik generowany z `library/exercises.json` przez `tools/builder/build_library_review.py`. Nie edytuj go ręcznie.

Tagi P/S opisują typowe wykonanie i są decyzją planisty, nie uniwersalną prawdą biomechaniczną (Appendix C). S? nie liczy się do ekspozycji. „Min RIR” to najniższy domyślnie dopuszczalny RIR; 0 oznacza, że stop jest bezpieczny (bezwarunkowo albo po spełnieniu warunku).

## Chest

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `bench_paused` | Wyciskanie leżąc z pauzą (zawodnicze)<br><sub>Paused Bench Press · płaska ławka, pauza na klatce</sub> | Chest | Elbow Extensors | - | warunkowo: ławka w racku, safety bars tuż pod najniższym punktem ruchu | 0 | 5-8 | - | zatwierdzone |
| `bench_tng` | Wyciskanie leżąc touch-and-go<br><sub>Bench Press (touch-and-go) · płaska ławka</sub> | Chest | Elbow Extensors | - | warunkowo: ławka w racku, safety bars tuż pod najniższym punktem ruchu | 0 | 5-8 | - | zatwierdzone |
| `bench_close_grip` | Wyciskanie wąsko<br><sub>Close-Grip Bench Press · chwyt na szerokość barków</sub> | Chest | Elbow Extensors | - | warunkowo: ławka w racku, safety bars tuż pod najniższym punktem ruchu | 0 | 6-10 | większy udział tricepsa niż w zwykłym bench pressie | zatwierdzone |
| `bench_incline_bb` | Wyciskanie na skosie sztangą<br><sub>Incline Barbell Press · skos ~30°</sub> | Chest | Elbow Extensors | - | warunkowo: ławka w racku, safety bars tuż pod najniższym punktem ruchu | 0 | 6-10 | akcent na górną część klatki | zatwierdzone |
| `db_bench` | Wyciskanie hantli na płaskiej<br><sub>Dumbbell Bench Press · płaska ławka</sub> | Chest | Elbow Extensors | - | warunkowo: umiejętność bezpiecznego odłożenia hantli przy upadku | 1 | 6-10 | - | zatwierdzone |
| `db_incline` | Wyciskanie hantli na skosie<br><sub>Incline Dumbbell Press · skos ~30°</sub> | Chest | Elbow Extensors | - | warunkowo: umiejętność bezpiecznego odłożenia hantli przy upadku | 1 | 6-10 | akcent na górną część klatki | zatwierdzone |
| `machine_chest_press` | Chest press na maszynie<br><sub>Machine Chest Press · płaski</sub> | Chest | Elbow Extensors | - | tak | 0 | 6-10 | - | zatwierdzone |
| `machine_incline_press` | Incline press na maszynie<br><sub>Machine Incline Press · skos</sub> | Chest | Elbow Extensors | - | tak | 0 | 6-10 | akcent na górną część klatki | zatwierdzone |
| `smith_bench` | Wyciskanie na suwnicy Smitha<br><sub>Smith Machine Bench Press · płaska ławka</sub> | Chest | Elbow Extensors | - | warunkowo: stopy bezpieczeństwa ustawione | 0 | 6-10 | - | zatwierdzone |
| `smith_incline` | Wyciskanie na skosie na suwnicy Smitha<br><sub>Smith Machine Incline Press · skos ~30°</sub> | Chest | Elbow Extensors | - | warunkowo: stopy bezpieczeństwa ustawione | 0 | 6-10 | akcent na górną część klatki | zatwierdzone |
| `pec_deck` | Pec deck<br><sub>Pec Deck</sub> | Chest | - | - | tak | 0 | 12-20 | - | zatwierdzone |
| `cable_fly` | Rozpiętki na wyciągu<br><sub>Cable Fly · na wysokości klatki</sub> | Chest | - | - | tak | 0 | 12-15 | - | zatwierdzone |
| `cable_fly_low_high` | Rozpiętki z dołu do góry<br><sub>Low-to-High Cable Fly · z dołu do góry</sub> | Chest | - | - | tak | 0 | 12-15 | akcent na górną część klatki | zatwierdzone |

## Lateral Delts

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `db_lateral` | Wznosy bokiem z hantlami<br><sub>Dumbbell Lateral Raise</sub> | Lateral Delts | - | - | tak | 0 | 12-20 | - | zatwierdzone |
| `cable_lateral` | Wznosy bokiem na wyciągu<br><sub>Cable Lateral Raise · jednorącz</sub> | Lateral Delts | - | - | tak | 0 | 12-20 | - | zatwierdzone |
| `machine_lateral` | Wznosy bokiem na maszynie<br><sub>Machine Lateral Raise</sub> | Lateral Delts | - | - | tak | 0 | 12-20 | - | zatwierdzone |

## Elbow Extensors

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `dips_bw` | Pompki na poręczach<br><sub>Dips · pochylenie zależne od celu</sub> | Elbow Extensors | Chest | - | warunkowo: możliwość zejścia na podest przy upadku | 1 | 6-12 | udział klatki rośnie z pochyleniem tułowia | zatwierdzone |
| `machine_shoulder_press` | Wyciskanie nad głowę na maszynie<br><sub>Machine Shoulder Press</sub> | - | Elbow Extensors | Lateral Delts | tak | 0 | 6-10 | główny cel to przedni akton barku, którego nie ma w Fixed Core (możliwy Functional Override) | zatwierdzone |
| `db_shoulder_press` | Wyciskanie hantli nad głowę<br><sub>Seated Dumbbell Shoulder Press · siedząc</sub> | - | Elbow Extensors | Lateral Delts | warunkowo: umiejętność bezpiecznego odłożenia hantli | 1 | 6-10 | jak wyżej | zatwierdzone |
| `pushdown` | Prostowanie ramion na wyciągu<br><sub>Cable Triceps Pushdown · drążek lub lina</sub> | Elbow Extensors | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `overhead_cable_ext` | Prostowanie ramion nad głową na wyciągu<br><sub>Overhead Cable Triceps Extension · lina</sub> | Elbow Extensors | - | - | tak | 0 | 8-12 | ramię uniesione: większe rozciągnięcie głowy długiej | zatwierdzone |
| `machine_triceps_ext` | Prostowanie ramion na maszynie<br><sub>Machine Triceps Extension</sub> | Elbow Extensors | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `dip_machine` | Dipy na maszynie<br><sub>Seated Dip Machine · siedząc</sub> | Elbow Extensors | - | Chest | tak | 0 | 8-12 | - | zatwierdzone |
| `skullcrusher` | Wyciskanie francuskie leżąc<br><sub>EZ-Bar Skullcrusher · leżąc</sub> | Elbow Extensors | - | - | warunkowo: kontrola sztangi nad twarzą; bez prób na upadek | 1 | 8-12 | - | zatwierdzone |
| `db_overhead_ext` | Wyciskanie francuskie hantlą nad głową<br><sub>Overhead Dumbbell Triceps Extension · oburącz</sub> | Elbow Extensors | - | - | warunkowo: bez prób na upadek | 1 | 8-12 | - | zatwierdzone |

## Back

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `lat_pulldown` | Ściąganie drążka wyciągu górnego<br><sub>Lat Pulldown · chwyt nachwytem, akcent na najszersze</sub> | Back | Elbow Flexors | - | tak | 0 | 8-12 | akcent: najszersze grzbietu | zatwierdzone |
| `lat_pulldown_neutral` | Ściąganie wąskim chwytem neutralnym<br><sub>Close Neutral-Grip Pulldown · chwyt neutralny</sub> | Back | Elbow Flexors | - | tak | 0 | 8-12 | akcent: najszersze grzbietu | zatwierdzone |
| `pull_up` | Podciąganie nachwytem<br><sub>Pull-Up</sub> | Back | Elbow Flexors | - | tak | 0 | 5-10 | - | zatwierdzone |
| `chin_up` | Podciąganie podchwytem<br><sub>Chin-Up</sub> | Back | Elbow Flexors | - | tak | 0 | 5-10 | - | zatwierdzone |
| `assisted_pull_up` | Podciąganie na maszynie z odciążeniem<br><sub>Assisted Pull-Up Machine</sub> | Back | Elbow Flexors | - | tak | 0 | 6-10 | - | zatwierdzone |
| `chest_supported_row` | Wiosłowanie z podparciem klatki (maszyna)<br><sub>Chest-Supported Machine Row · chwyt neutralny, łokcie blisko</sub> | Back | Elbow Flexors | Rear Delts | tak | 0 | 6-10 | - | zatwierdzone |
| `wide_machine_row` | Wiosłowanie szerokim chwytem (maszyna)<br><sub>Wide-Grip Machine Row · łokcie ~45-60°</sub> | Back | Rear Delts, Elbow Flexors | - | tak | 0 | 8-12 | akcent: górna część pleców; Rear Delts S zależy od toru łokci | zatwierdzone |
| `seated_cable_row` | Wiosłowanie siedząc na wyciągu<br><sub>Seated Cable Row · uchwyt neutralny</sub> | Back | Elbow Flexors | Rear Delts | tak | 0 | 8-12 | - | zatwierdzone |
| `db_row` | Wiosłowanie hantlą jednorącz<br><sub>One-Arm Dumbbell Row · podparcie na ławce</sub> | Back | Elbow Flexors | - | tak | 0 | 8-12 | - | zatwierdzone |
| `tbar_row_supported` | Wiosłowanie T-bar z podparciem<br><sub>Chest-Supported T-Bar Row</sub> | Back | Elbow Flexors | Rear Delts | tak | 0 | 6-10 | - | zatwierdzone |
| `barbell_row` | Wiosłowanie sztangą w opadzie<br><sub>Barbell Row</sub> | Back | Elbow Flexors | Rear Delts | warunkowo: odłożenie sztangi na podłogę; bez prób na upadek | 1 | 6-10 | duże obciążenie prostowników grzbietu | zatwierdzone |
| `straight_arm_pulldown` | Ściąganie prostymi ramionami<br><sub>Straight-Arm Pulldown</sub> | Back | - | - | tak | 0 | 10-15 | akcent: najszersze grzbietu | zatwierdzone |

## Rear Delts

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `reverse_pec_deck` | Reverse pec deck<br><sub>Reverse Pec Deck</sub> | Rear Delts | - | - | tak | 0 | 12-20 | - | zatwierdzone |
| `cable_rear_fly` | Odwrotne rozpiętki na wyciągu<br><sub>Cable Rear Delt Fly</sub> | Rear Delts | - | - | tak | 0 | 12-20 | - | zatwierdzone |
| `face_pull` | Face pull<br><sub>Face Pull · lina, na wysokości twarzy</sub> | Rear Delts | - | - | tak | 0 | 12-20 | z rotacją zewnętrzną | zatwierdzone |
| `db_rear_raise` | Wznosy w opadzie z hantlami<br><sub>Bent-Over Dumbbell Rear Delt Raise</sub> | Rear Delts | - | - | tak | 0 | 12-20 | - | zatwierdzone |

## Elbow Flexors

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `machine_preacher` | Uginanie na modlitewniku (maszyna)<br><sub>Machine Preacher Curl</sub> | Elbow Flexors | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `machine_curl` | Uginanie ramion na maszynie<br><sub>Machine Biceps Curl</sub> | Elbow Flexors | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `bayesian_curl` | Uginanie na wyciągu zza pleców<br><sub>Bayesian Cable Curl · ramię za tułowiem</sub> | Elbow Flexors | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `cable_curl` | Uginanie ramion na wyciągu<br><sub>Cable Curl · drążek</sub> | Elbow Flexors | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `incline_db_curl` | Uginanie hantlami na skosie<br><sub>Incline Dumbbell Curl · ramię za tułowiem</sub> | Elbow Flexors | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `ez_curl` | Uginanie sztangą łamaną<br><sub>EZ-Bar Curl</sub> | Elbow Flexors | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `hammer_curl` | Uginanie młotkowe<br><sub>Dumbbell Hammer Curl · chwyt neutralny</sub> | Elbow Flexors | - | - | tak | 0 | 8-12 | większy udział ramiennego i ramienno-promieniowego | zatwierdzone |

## Quadriceps

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `back_squat` | Przysiad ze sztangą<br><sub>Back Squat</sub> | Quadriceps | Glutes | Hip Adductors | warunkowo: rack z safety bars; bez prób na upadek | 1 | 5-8 | - | zatwierdzone |
| `leg_press` | Prasa nożna 45°<br><sub>45° Leg Press</sub> | Quadriceps | - | Glutes | tak | 0 | 8-12 | udział pośladków zależy od głębokości i ustawienia stóp | zatwierdzone |
| `hack_squat` | Hack squat<br><sub>Hack Squat</sub> | Quadriceps | - | Glutes | warunkowo: zaczepy bezpieczeństwa ustawione | 0 | 8-12 | - | zatwierdzone |
| `smith_split_squat` | Wykroki bułgarskie / split squat na Smithie<br><sub>Smith Split Squat · tylna stopa na podłodze</sub> | Quadriceps | - | Glutes | warunkowo: stopy bezpieczeństwa ustawione | 0 | 8-12 | jednonóż; seria = obie nogi | zatwierdzone |
| `bulgarian_split_squat` | Przysiad bułgarski z hantlami<br><sub>Dumbbell Bulgarian Split Squat · tylna stopa na ławce</sub> | Quadriceps | Glutes | - | warunkowo: możliwość odstawienia hantli; bez prób na upadek | 1 | 8-12 | jednonóż; udział pośladków rośnie z pochyleniem tułowia | zatwierdzone |
| `leg_extension` | Prostowanie nóg na maszynie<br><sub>Leg Extension</sub> | Quadriceps | - | - | tak | 0 | 10-15 | akcent: mięsień prosty uda w skróceniu | zatwierdzone |

## Hamstrings

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `seated_leg_curl` | Uginanie nóg siedząc<br><sub>Seated Leg Curl</sub> | Hamstrings | - | - | tak | 0 | 8-12 | zgięcie kolana przy zgiętym biodrze | zatwierdzone |
| `lying_leg_curl` | Uginanie nóg leżąc<br><sub>Lying Leg Curl</sub> | Hamstrings | - | - | tak | 0 | 8-12 | zgięcie kolana | zatwierdzone |
| `rdl` | Rumuński martwy ciąg<br><sub>Romanian Deadlift</sub> | Hamstrings | Glutes | Back | warunkowo: odłożenie sztangi; bez prób na upadek | 1 | 6-10 | wyprost biodra; zwykle 1-2 RIR (Ch04) | zatwierdzone |

## Glutes

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `deadlift` | Martwy ciąg klasyczny<br><sub>Conventional Deadlift</sub> | - | Glutes, Hamstrings | Quadriceps, Back | warunkowo: bez prób na upadek | 1 | 3-6 | ćwiczenie siłowe; bodziec rozłożony, brak jednego P | zatwierdzone |
| `back_extension` | Wyprosty tułowia na ławce 45°<br><sub>45° Back Extension · ruch z bioder, neutralny kręgosłup</sub> | Glutes | Hamstrings | - | tak | 0 | 8-12 | wyprost biodra; Glutes P zależy od techniki | zatwierdzone |
| `machine_hip_thrust` | Hip thrust na maszynie<br><sub>Machine Hip Thrust</sub> | Glutes | - | - | tak | 0 | 8-12 | - | zatwierdzone |
| `barbell_hip_thrust` | Hip thrust ze sztangą<br><sub>Barbell Hip Thrust</sub> | Glutes | - | - | warunkowo: możliwość opuszczenia sztangi na podłogę | 0 | 8-12 | - | zatwierdzone |

## Hip Adductors

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `hip_adduction` | Przywodzenie nóg na maszynie<br><sub>Hip Adduction Machine</sub> | Hip Adductors | - | - | tak | 0 | 12-15 | - | zatwierdzone |

## Calves

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `standing_calf` | Wspięcia na palce stojąc<br><sub>Standing Calf Raise · proste kolano</sub> | Calves | - | - | tak | 0 | 8-12 | proste kolano: akcent na mięsień brzuchaty | zatwierdzone |
| `seated_calf` | Wspięcia na palce siedząc<br><sub>Seated Calf Raise · zgięte kolano</sub> | Calves | - | - | tak | 0 | 10-15 | zgięte kolano: akcent na płaszczkowaty | zatwierdzone |
| `leg_press_calf` | Wspięcia na palce na prasie<br><sub>Leg Press Calf Raise · proste kolano</sub> | Calves | - | - | tak | 0 | 10-15 | proste kolano | zatwierdzone |

## Trunk Musculature

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `cable_crunch` | Spięcia brzucha na wyciągu<br><sub>Cable Crunch · klęcząc</sub> | Trunk Musculature | - | - | tak | 0 | 10-15 | zgięcie tułowia | zatwierdzone |
| `ab_crunch_machine` | Spięcia brzucha na maszynie<br><sub>Ab Crunch Machine</sub> | Trunk Musculature | - | - | tak | 0 | 10-15 | zgięcie tułowia | zatwierdzone |
| `hanging_knee_raise` | Unoszenie kolan w zwisie<br><sub>Hanging Knee Raise · z podwinięciem miednicy</sub> | Trunk Musculature | - | - | tak | 0 | 8-15 | bez podwinięcia miednicy pracują głównie zginacze biodra | zatwierdzone |
| `pallof_press` | Pallof press<br><sub>Pallof Press</sub> | Trunk Musculature | - | - | tak | 0 | 10-15 | funkcja: antyrotacja (Functional Note) | zatwierdzone |

## Hip Abduction

| ID | Ćwiczenie | P | S | S? | Bezpieczny stop | Min RIR | Zakres | Uwagi | Status |
|---|---|---|---|---|---|---:|---|---|---|
| `hip_abduction` | Odwodzenie nóg na maszynie<br><sub>Hip Abduction Machine</sub> | Hip Abduction | - | - | tak | 0 | 12-20 | Functional Override „Hip Abduction” (Ch02 §7); wymaga aktywacji w planie | zatwierdzone |
