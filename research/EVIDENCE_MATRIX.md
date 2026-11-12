# HARDSET — Evidence Matrix

Każda pozycja ma jednoznaczną klasę: **SCIENTIFIC_EVIDENCE**, **HARDSET_DESIGN_DECISION**, **IMPLEMENTATION_HEURISTIC**, **PRACTICAL_SAFETY_RULE**, **PRACTICAL_MEASUREMENT**, **NOT_SUPPORTED**.

| ID | Claim / rule | Class | References | Evidence / policy | Critical limit |
|---|---|---|---|---|---|
| E01 | High-effort resistance training produces useful adaptations | SCIENTIFIC_EVIDENCE | R01;R04 | Supported general direction | No unique optimal RIR |
| E02 | Failure is universally required to build muscle | NOT_SUPPORTED | R03;R05;R06 | Not established | Do not tell users that all sets must fail |
| E03 | Closer to failure may favor hypertrophy | SCIENTIFIC_EVIDENCE | R04;R05 | Direction plausible; precision limited | RIR estimates and effort controls heterogeneous |
| E04 | 2 Hard Sets per exercise as default | HARDSET_DESIGN_DECISION | R01;R08 | Organizational standard | Not a proven individual optimum |
| E05 | Lead/Supporting Set effort 1 then 0–1 RIR | HARDSET_DESIGN_DECISION | R03;R04;R05 | Coherent with high-effort approach | Exact pair unvalidated |
| E06 | Failure-conservative RIR in potentially unsafe lifts | PRACTICAL_SAFETY_RULE | R03;R04 | Risk-first decision | Cannot certify individual safety |
| E07 | Fixed Core uses exactly 12 reporting areas | HARDSET_DESIGN_DECISION | - | Taxonomy decision | Not an anatomical claim of completeness |
| E08 | Compound Patterns vs Targeted Functions | HARDSET_DESIGN_DECISION | R12 | Organizational classification | No compound dominance implied |
| E09 | P/S/—/? labels and exposure ledger | HARDSET_DESIGN_DECISION | R02 | Transparency of accounting | Labels require expert/contextual assignment |
| E10 | Secondary series equal 0.5 Primary series | NOT_SUPPORTED | R02 | Fractional value was a statistical model | Must not implement universal conversion |
| E11 | Priority and Standard 2 exposures default | HARDSET_DESIGN_DECISION | R10;R11 | Quality-of-organization preference | Not a biological requirement |
| E12 | Weekly volume often promotes more hypertrophy with diminishing returns | SCIENTIFIC_EVIDENCE | R01;R02;R07;R08 | Supported average tendency | Many uncertainties/heterogeneity |
| E13 | Numeric volume bins Low 2–4 Moderate 5–8 Expanded 9–14 | IMPLEMENTATION_HEURISTIC | R01;R02 | Convenient label only | Not norm in main chapters |
| E14 | Exercise rep templates 5–8 6–10 8–12 12–20 | IMPLEMENTATION_HEURISTIC | R09;R17 | Practical ranges | Not rigid effectiveness zones |
| E15 | Rest 2.5–4 min compounds 1.5–3 targeted | IMPLEMENTATION_HEURISTIC | R16 | Performance-supporting defaults | Not individual optimum |
| E16 | Machine bias if otherwise comparable | HARDSET_DESIGN_DECISION | R12 | Practical failure access and repeatability | Do not claim machines inherently grow more muscle |
| E17 | Progression after lead upper bound + support lower bound | HARDSET_DESIGN_DECISION | R19;R20 | Simple repeatable threshold | Not experimental algorithm |
| E18 | Deload sample 5–7d 40–60% fewer sets 3–4 RIR | IMPLEMENTATION_HEURISTIC | - | Illustrative fatigue strategy | Not a trial-validated law |
| E19 | Frequency may be chosen based on distribution at equal volume | SCIENTIFIC_EVIDENCE | R10;R11;R01 | Supported for hypertrophy broadly | Strength skill may benefit from frequency |
| E20 | Full Body and Split similar at equated volume | SCIENTIFIC_EVIDENCE | R11 | Supported in sampled protocols | Individual adherence differs |
| E21 | Concurrent training does not always impair hypertrophy | SCIENTIFIC_EVIDENCE | R15 | Supported broad trend | Explosive strength and local fatigue possible |
| E22 | Must periodize every N weeks for hypertrophy | NOT_SUPPORTED | R01;R13 | No established necessity | Periodization can serve specific strength goals |
| E23 | Maintenance may require lower volume | SCIENTIFIC_EVIDENCE | R14 | Observed under specific settings | Not a universal min dose |
| E24 | Training Intent Development/Maintenance independent of Priority | HARDSET_DESIGN_DECISION | R14 | Clarifies goals | Not imposed biological category |
| E25 | Training log proves muscle hypertrophy | NOT_SUPPORTED | R21;R22;R23 | Performance is different construct | Progress can be present without measuring size |
| E26 | Circumferences and photos can indicate physique changes | PRACTICAL_MEASUREMENT | R22;R23 | Indirect and noisy | Not muscle-specific estimates |
| E27 | Early apparent growth may include edema | SCIENTIFIC_EVIDENCE | R23 | Observed | Especially early training; context specific |
| E28 | Ultrasound local thickness = exact whole muscle volume | NOT_SUPPORTED | R22 | Not interchangeable | Protocol and sample specific |
| E29 | Program reviews 6–8 weeks size reviews 8–12 weeks | IMPLEMENTATION_HEURISTIC | - | Practical checkpoints | Not outcome deadlines |
| E30 | PASS/CONDITIONAL/FAIL validator statuses | HARDSET_DESIGN_DECISION | - | Decision hygiene | Automated pass cannot medically certify safety |
| E31 | Lead Set RIR estimates are exact | NOT_SUPPORTED | R19;R20 | RIR can be useful but noisy | Treat estimate as estimate |
| E32 | Full ROM always better than shorter ROM | NOT_SUPPORTED | R18 | Cannot generalize unconditionally | Useful repeatable tolerable ROM prioritized |

## Rules for Claude / implementer

1. A scientific paper supports only the **specific limited claim** in its row.
2. NEVER upgrade an internal design decision into a research finding.
3. The absence of evidence in one direction is not always proof of no effect.
4. Numeric heuristics in annexes are removable without changing HARDSET v1.0.
5. Before citing a source, check authors, title, publication year, DOI and intended claim.
6. If evidence conflicts or is outside the studied population, disclose limitations instead of forcing a conclusion.