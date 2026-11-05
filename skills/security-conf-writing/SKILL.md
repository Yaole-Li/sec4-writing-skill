---
name: security-conf-writing
description: Draft or rewrite the Title, Abstract, Introduction, Related Work, Threat Model, Design, Evaluation, Ethics, Open Science and Conclusion of a paper for IEEE S&P, USENIX Security, NDSS or ACM CCS, in the register of the 268 security papers in this skill's corpus (S&P, USENIX and NDSS; CCS content is convention-based). Use when the user (A) fills in the intake form (assets/intake_form.html JSON) or describes a threat, an attack, a defense, a measurement or a system and its results, or (B) pastes an existing abstract or draft to make it venue-ready. Writes into the four LaTeX templates in template/. Not for journal submissions to TIFS (use tifs-paper-writing), for rebuttals, or for plain proofreading.
---

# Security Conference Writing: the four top venues

Turn a description of a security project, or a draft, into a submission-shaped paper for IEEE S&P,
USENIX Security, NDSS or ACM CCS. The guidance is fitted on **241 papers** (S&P 86, USENIX 104, NDSS 51;
2023–2026) extracted from 268 PDFs, of which 27 are held out for testing. **The corpus contains no CCS
papers**, so every CCS statement here is convention, and it says so where it appears.

## What the corpus shows

1. **The abstract budget is venue-specific.** S&P 271 words, USENIX 211, NDSS 226 (`abstract.md`).
2. **The introduction carries the evaluation.** 1,121 words and 18 numbers at the median; only 9 % of
   sentences open with "We" (`introduction.md`).
3. **The attacker is the organising device.** 157 of 241 papers state a threat model somewhere, and 39 of
   120 annotated papers give the attacker its own introduction paragraph (`threat-model.md`).
4. **Ethics and open science are venue requirements, not decoration.** USENIX requires an Ethics
   Considerations section and an Open Science statement; 89 of 104 USENIX papers discuss ethics and 78
   state artefact availability (`ethics-and-disclosure.md`, `artifact-and-open-science.md`).
5. **The evaluation is judged on adaptivity and honesty.** A static baseline only, or one error
   direction only, is the most common substantive weakness (`evaluation.md`).

What is normal in this corpus: "novel" (72 of 241 abstracts), "state-of-the-art" (52), "extensive
experiments" (28). What is not: "with the rapid development" (1), "plays an important role" (0), "our key
insight is" (0). The checker encodes exactly these severities.

## Workflow

Do not write prose before Step 4.

### Step 0 — Intake

**Mode A: intake JSON** from `assets/intake_form.html` (schema `sec4-intake/v1`). Run
`python3 scripts/intake_to_brief.py <file.json> --out brief.md --bib refs.bib`, then work from
`brief.md`; exit code 2 means a required field is missing.

**Mode B: an existing draft.** Reverse-engineer it into the intake fields (task, threat, the assumption
that breaks, prior work, insight, method, results with numbers, ethics, artefacts) and show a table:
field, what the draft says, status (present / vague / missing). Keep the author's facts, numbers and
terminology verbatim. Add a **change table** to `report.md` (original sentence → revised sentence → the
pattern it follows).

In both modes:
- Required: `one_line`, `task`, `threat`, `failure`, `results`. Recommended: `method`, `prior_best`,
  `failure_reason`, `insight`, `closest`, plus the memorability fields. Ask once, in one compact list.
- Never invent numbers, datasets, baselines, attacker capabilities, ethics approvals or citations.
- Record the target venue at intake; every range in Step 7 depends on it.

### Step 1 — Claim, attacker, assumption, numbers

Write for yourself, into `report.md`:

- **Claim**: `We show that [mechanism] [achieves what] against [which attacker] under [which setting].`
- **Attacker in one line**: goal, knowledge, capability, out of scope.
- **The assumption that breaks** in prior work, and its cost.
- **Paper type** (A1–A7) and **gap type** (new-surface / failure / assumption-gap / cost /
  capability-gap / scale-gap / insight) per `routing.md`.
- **Closest work** and the one checkable difference.
- **Headline numbers**: one or two, each with dataset, metric and baseline.

### Step 2 — Route

Load `references/routing.md`. Fix the type and the gap, then follow the route's introduction order and
its reviewer question. Type decides what counts as evidence: an A1 attack on generality, an A2 defense
on adaptivity, an A3 measurement on sampling and ethics, an A6 SoK on the framework and a re-evaluation
(`sok.md`).

### Step 3 — Claim map and evidence map

Load `references/claim-calibration.md` if present, otherwise apply its three rungs: measured, guaranteed,
assumed. For every claim, name the strongest wording the evidence supports and the table that carries
it. A claim without evidence is softened in the introduction or gets a `[TODO]` experiment.

### Step 4 — Skeleton

Load `references/abstract.md` and `references/introduction.md`. One line per paragraph, one line per
abstract sentence. Check against the tiers: always (deployed reality, gap with its assumption, attacker,
design, numbers), usual (contributions, ethics sentence, closest-work comparison), optional (roadmap,
stance). Mark the pivot sentences: the assumption, the failure, the observation.

### Step 5 — Draft with exemplars

For each function read two or three real sentences of the same move and the same venue:
`python3 scripts/find_exemplars.py intro.gap.failure --venue USENIX -n 3`,
`python3 scripts/find_exemplars.py --venue SP --list`, or read whole abstracts with
`--abstracts SP -n 5`. Learn the order of information and the rhythm; never copy a sentence or a run of
six words, which the checker tests against the bank.

### Step 5b — Threat model, related work, design, evaluation

1. **Threat model** (`threat-model.md`): six items — goal, knowledge, capability, observables, setting,
   out of scope. The same attacker appears in the introduction and in the evaluation.
2. **Related work** (`related-work.md`): group by the assumption each family makes.
3. **Design** (`method.md`): overview + anchor figure, then one subsection per component in the order
   need → mechanism → property, then the security and complexity argument.
4. **Evaluation** (`evaluation.md`): setup, claim-first results, robustness and adaptive evaluation,
   ablation, overhead, limitations.
5. **Ethics** (`ethics-and-disclosure.md`) and **open science** (`artifact-and-open-science.md`): one
   short section each, before the conclusion. Missing numbers stay `\TODO{}`.

### Step 5c — Figures

Load `references/figures.md`. Figure 1 is the system overview or the threat scenario, not a result.
Captions name the figure in a noun phrase and then give the takeaway (median 28.5 words here, 53.5 for
Figure 1). Draw only mechanisms the authors have described; every result figure stays a framed
placeholder whose caption carries the plan.

### Step 6 — Output

Use the venue template: `template/SP`, `template/NDSS`, `template/USENIX` or `template/CCS`
(`references/latex-output.md`). Without LaTeX, write Markdown with `## Abstract`, `## 1 Introduction`,
and so on. The paper text carries no move labels and no notes other than `[TODO]` / `\TODO{}`.

### Step 7 — Check

1. `python3 scripts/check_draft.py main.tex --venue <SP|USENIX|NDSS|CCS>` — fix every ERROR. WARN means
   outside the band of 90 % of that venue's papers, or a missing venue requirement (ethics, open science,
   CCS metadata, threat model); revise it or justify it in `report.md`. NOTEs are information.
   `python3 scripts/style_metrics.py main.tex` prints every metric with the venue's percentiles.
2. `python3 scripts/check_figures.py main.tex` — fix every ERROR; WARNs (caption length, clause
   openers, raster plots, absolute widths, float counts) are fixed or justified.
3. Semantic checks:
   - The threat model has all six items and matches the introduction's attacker.
   - An adaptive or knowledgeable attacker is evaluated, or its absence is explained.
   - Both error directions at one operating point; overhead or usability cost reported.
   - Robustness claims name the attack family they survive.
   - Ethics names approval, disclosure and data handling where the work involves people or live systems.
   - Artefacts: what is released, where, under which licence, what is withheld.
   - The abstract, introduction and contributions say the same thing at the same strength.
   - Read the draft aloud: if several consecutive sentences carry one bare fact each, merge them.

### Step 8 — Deliver

1. The paper, in the venue template.
2. `report.md`: claim, attacker, failing assumption, insight, closest work, type and gap, route, claim
   map, checker summaries, `[TODO]` list, open questions, limitations kept out of the abstract, the
   ethics and artefact statements, and the figure plan.

## Hard rules

- Never fabricate numbers, datasets, baselines, attacker capabilities, citations, approvals or artefacts.
- Never cite a key that is not in the author's bibliography; write `[TODO: cite ...]`.
- The abstract carries no citations, no equations, no figure references and no undefined abbreviations.
- An attack or defense paper states a threat model. No threat model, no security claim.
- Adaptive evaluation reported when it exists; its absence stated when it does not.
- Human subjects, real traffic, live systems, malware: ethics statement with approval, disclosure and
  data handling.
- Both error directions at one operating point. A bare detection rate is not a security result.
- USENIX: Ethics Considerations and Open Science sections. CCS: CCS Concepts block and keywords.
- Anonymity: no author names, acknowledgements or self-identifying links in the review version.
- Name mechanisms, not abstractions; when the input does not say how something works, write `[TODO]` and ask.
- Describe components by their relation, not as a parallel list.
- Keep what makes the draft memorable: the pivot sentences, the attacker sentence, the handle in the title.

## Files

| File | Load at |
|---|---|
| `references/intake-form.md`, `assets/intake_form.html`, `scripts/intake_to_brief.py` | Step 0 |
| `references/routing.md`, `references/sok.md` | Step 2 |
| `references/abstract.md`, `references/introduction.md` | Steps 4–5 |
| `references/venue-guide.md`, `references/corpus-profile.md` | when a venue-specific number is needed |
| `references/exemplars/` (`moves.jsonl`, `abstracts.jsonl`, `phrasebank.csv`), `scripts/find_exemplars.py` | Step 5 |
| `references/style-rules.md` | Steps 5, 7 |
| `references/threat-model.md`, `references/related-work.md`, `references/method.md`, `references/evaluation.md` | Step 5b |
| `references/ethics-and-disclosure.md`, `references/artifact-and-open-science.md` | Step 5b |
| `references/figures.md`, `template/<VENUE>/` | Steps 5c, 6 |
| `references/latex-output.md` | Step 6 |
| `scripts/check_draft.py`, `scripts/style_metrics.py`, `scripts/check_figures.py`, `references/corpus/corpus_stats.json` | Step 7 |

Use `python3`. Attribution and licences: `NOTICE.md`.
