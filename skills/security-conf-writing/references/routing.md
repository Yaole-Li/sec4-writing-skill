# Routing: paper type × gap type → the route to write

Two decisions, made in Step 2 and recorded in `report.md`. The type fixes the section order, the
evidence the reviewer will demand, and the exemplars to read.

## 1. Paper type (first yes wins)

Counts are from the 120-paper annotated sample.

| # | Type | Decide when | Papers | Route |
|---|---|---|---|---|
| 1 | **A6 SoK** | the paper systematises or re-evaluates existing work; the framework is the deliverable | 5 | `sok` |
| 2 | **A7 Dataset / benchmark** | a dataset, benchmark or testbed is released as the contribution | 5 | `resource` |
| 3 | **A1 Attack** | a new attacker capability is the deliverable | 35 | `attack` |
| 4 | **A3 Measurement** | a characterisation of a threat, ecosystem or deployment is the deliverable | 25 | `measurement` |
| 5 | **A4 System** | an implemented artefact carries the claim, judged on overhead and deployment | 28 | `system` |
| 6 | **A5 Analysis / construction** | a proof, bound, construction or formal analysis carries the claim | 8 | `theory` |
| 7 | **A2 Defense** | a detection, prevention or mitigation mechanism is the deliverable | 14 | `defense` |

The order matters: a paper that re-evaluates prior defenses is a SoK even though it also proposes a
classifier, and a paper that releases a benchmark with a baseline model on top is A7.

Per venue, from the same sample: S&P is attack-heavy (A1 15 of 42), USENIX is measurement-heavy
(A3 15 of 52, A1 14), NDSS is the most balanced (A2 6, A1 6, A4 5, A5 4 of 26).

## 2. Gap type

| Type | Papers | Choose when | Diagnostic question |
|---|---|---|---|
| `capability-gap` | 28 | nothing can answer the question at all | is there really no baseline for the full task? |
| `new-surface` | 25 | a newly deployed technology creates an unexamined surface | what is new in deployment, and what does it newly expose? |
| `assumption-gap` | 15 | prior work rests on an assumption that no longer holds | which attacker capability invalidates it? |
| `failure` | 15 | a strong defense breaks under a specific, reproducible condition | can you show the input where it breaks? |
| `insight` | 14 | one observation collapses the pipeline | is there one sentence the design follows from? |
| `cost` | 13 | existing defenses work but cost too much: latency, bandwidth, usability | can you quantify the cost you remove? |
| `scale-gap` | 10 | lab-only evidence, real deployments behave differently | what changes at deployment scale? |

`new-surface` is the reason this corpus looks the way it does: 116 of the 268 papers are tagged LLM and
61 traffic analysis, so a large share of the sample argues about a technology that did not exist five
years ago. If your paper is in that situation, the gap is not that prior work is weak; it is that the
surface is new and the threat model has not been written yet.

## 3. Route table

| Route | Introduction order | Abstract | Read these exemplars |
|---|---|---|---|
| `attack` | L → C (defenses) → A → G → I → M → R → K → E | L-G-A-M-R | `intro.attacker`, `intro.gap.failure`, `abstract.result` |
| `defense` | L → C (attacks) → G → A → I → M → S → R → K | L-G-M-S-R | `intro.method`, `intro.security` |
| `measurement` | L → C (what is known) → G (what nobody measured) → M (campaign) → R (what the data shows) → E | L-G-M-R-E | `eval.setup`, `eval.claim-first` |
| `system` | L → C → G (cost or deployment gap) → M (architecture) → R (deployment result incl. overhead) → X | L-G-M-R-X | `eval.overhead`, `method.opener` |
| `theory` | L → C (known results) → G (what is unproven) → S (the result in words) → M (proof route) → R → X | L-G-S-R | `abstract.security`, `method.property` |
| `resource` | L → C (what is missing) → G → M (collection principle) → R (scale + what it enables) → O | L-G-M-R-K | `openscience.data-release` |
| `sok` | L → G (the question the field cannot answer) → M (framework + corpus) → R (re-evaluation) → K | L-G-M-R-K | `references/sok.md` |

## 4. What each type must prove

| Type | The reviewer's first question |
|---|---|
| A1 attack | does the capability generalise beyond one model or dataset, and is the threat model honest about what the attacker cannot do? |
| A2 defense | does it survive an adaptive attacker, and what does it cost? |
| A3 measurement | is the sample representative, is the scale real, and is the ethics section adequate? |
| A4 system | what is the overhead in deployment units, and does it hold outside the testbed? |
| A5 analysis | are the assumptions minimal and stated, and does the bound say something about practice? |
| A6 SoK | is there a framework a future paper can be placed in, and was anything re-run? |
| A7 dataset | is the split leak-free, does it solve a real gap, and are baselines re-run on it? |

## 5. Output

```text
Type: A1 attack        Gap: new-surface (LLM agents)
Route: L -> C -> A -> G -> I -> M -> R -> K -> E
Reviewer will ask: generality across models, adaptive evaluation, disclosure of harmful artefacts
```
