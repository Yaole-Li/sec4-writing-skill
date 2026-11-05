# Rubric D1–D9

Candidates are anonymised as A, B, C, D. One of them is the published paper. Score every candidate on
every dimension with an integer 1–5.

| # | Dimension | 1 | 3 | 5 |
|---|---|---|---|---|
| D1 | **Threat model** | no attacker, or an attacker that changes between paragraphs | attacker named with goal and capability | goal, knowledge, capability, observables and out-of-scope stated, consistent with the evaluation |
| D2 | **Gap and failing assumption** | "existing work has limitations" | a concrete failure condition | the assumption that breaks, with its condition and cost, set up as the tension the paper resolves |
| D3 | **Novelty of the object** | a variant of a known technique with no new object | a new mechanism inside a known threat model | a new attack surface, abstraction or measurement target that the reader can name |
| D4 | **Evidence-calibrated claims** | overclaims (state-of-the-art, first, secure, robust) or presents a measurement as a guarantee; one error direction missing | mostly supported, one gap | every claim at the strength its evidence supports, both error directions at one operating point, guarantee vs measurement distinguished |
| D5 | **Concreteness** | adjectives and abstractions | some numbers | mechanisms, datasets, numbers and one concrete instance carry the argument |
| D6 | **Positioning** | no prior work named | named, vague difference | closest work named with one checkable difference (mechanism, scope, cost, assumption, input, output, evaluation) |
| D7 | **Ethics and artefacts** | neither addressed | one addressed | approval, disclosure and data handling stated; artefacts named with what is withheld and why |
| D8 | **Flow and economy** | repetitive, paragraphs restate themselves | readable | each sentence adds something; pivots are short; no claim stated twice |
| D9 | **Method and experiments** | no design order, no setup, results without claims | conventional structure, partial setup | components in causal order with need→mechanism→property, claim-first results pointing at tables, adaptive evaluation and overhead reported |

## Penalties

- Any invented number, dataset, baseline, attacker capability, approval or citation: **D4 = 1**, whatever
  the rest looks like.
- An attack or defense draft with no threat model: D1 and D4 cannot exceed 3.
- Length is not rewarded. A longer candidate does not rank higher for being longer.

## Output

For each candidate and each dimension, an integer 1–5. Then a ranking of the four candidates, and for each
generated candidate the single most important difference from the published paper.
