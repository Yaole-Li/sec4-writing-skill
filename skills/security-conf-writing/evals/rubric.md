# Blind comparison rubric (abstract + introduction)

Candidates per case: each configuration's output **and the original paper's abstract and introduction**,
anonymised as A, B, C, D with artefact names normalised. Score 1–5 per dimension, then rank.

| # | Dimension | 1 | 3 | 5 |
|---|---|---|---|---|
| D1 | **Threat model** | no attacker, or one that changes between paragraphs | attacker named with goal and capability | goal, knowledge, capability, observables and out-of-scope all stated, consistent with the evaluation |
| D2 | **Gap and failing assumption** | "existing work has limitations" | a concrete failure condition | the assumption that breaks, with its condition and cost, set up as the tension the paper resolves |
| D3 | **Novelty of the object** | a variant of a known technique with no new object | a new mechanism in a known threat model | a new attack surface, abstraction or measurement target that a reviewer can name |
| D4 | **Evidence-calibrated claims** | overclaims, or a measured result presented as a guarantee; one error direction missing | mostly supported | every claim at the strength its evidence supports, both error directions, adaptive evaluation stated |
| D5 | **Concreteness** | adjectives and abstractions | some numbers | mechanisms, datasets, numbers and one concrete instance carry the argument |
| D6 | **Positioning** | no prior work named | named, vague difference | closest work named with one checkable difference (mechanism, scope, cost, assumption, input, output, evaluation) |
| D7 | **Ethics and artefacts** | neither addressed | one addressed | approval, disclosure and data handling stated; artefacts named with what is withheld |
| D8 | **Venue register** (holistic) | reads like a generic ML paper or an AI draft | solid submission | indistinguishable from a paper of that venue |

Report per case: the score table, the ranking, and for each generated candidate the single most
important difference from the original paper.

Penalties
- Any invented number, dataset, baseline, attacker capability, approval or citation sets **D4 to 1**.
- An attack or defense paper with no threat model cannot score above 3 on D1 or D4.
- Length is not rewarded.
