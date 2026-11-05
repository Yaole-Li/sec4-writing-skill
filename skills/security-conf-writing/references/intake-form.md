# Intake: what the skill needs from the authors

`assets/intake_form.html` exports JSON with schema `sec4-intake/v1`; `scripts/intake_to_brief.py`
validates it and writes `brief.md`. Five fields are required; the rest decide whether the draft reads
like a top-venue security paper.

## meta

| Key | Meaning |
|---|---|
| `venue` | `SP`, `USENIX`, `NDSS` or `CCS`, with the year. Every style band depends on it. |
| `paper_type` | `A1`–`A7` (`routing.md`), or `auto` to let the skill decide |
| `working_name` | the artefact name, if there is one |
| `sections` | which parts to write: Title, Abstract, Introduction, Related Work, Threat Model, Design, Evaluation, Ethics, Open Science, Conclusion |

## required (5)

| Key | What to write | Why the skill needs it |
|---|---|---|
| `one_line` | one sentence: what was built or found, what it achieves, why it works | seeds the title, the claim sentence and the thesis |
| `task` | input → output, who is exposed, what is protected | without it the draft opens with generic background |
| `threat` | attacker goal, knowledge, capability, observables, out of scope | the organising device of the whole paper |
| `failure` | the observable failure of current practice: which condition, which assumption, what goes wrong | the gap paragraph is built from this |
| `results` | per result: dataset, metric, direction, baseline and its number, our number, table | headline numbers anchor abstract and introduction |

## recommended

| Key | What to write |
|---|---|
| `method` | the 2–4 components, each with what problem it answers |
| `prior_best` | how the strongest prior work actually works, mechanically |
| `failure_reason` | the assumption it rests on and why that assumption breaks |
| `insight` | the observation the design follows from, as a plain statement |
| `closest` | 1–3 closest works with a difference type and the concrete difference |
| `example` | one concrete instance: a vulnerable target, a trace, a screenshot, a number |
| `overhead` | latency, memory, bandwidth, query count, cost to the user |
| `surprising` | the counter-intuitive finding |
| `handle` | the team's internal name for the idea |

## enhancers and support

`ethics` (approval, disclosure, data handling, dual use), `openscience` (what is released, where, under
which licence, what is withheld), `release`, `limitations`, `materials` (notes, tables, related-work
list to paste), `bib` (BibTeX).

## methodexp

`paste` (anything: design notes, equations, result tables), `setting`, `components` (need → mechanism →
property), `datasets` (name, scale, split, provenance), `metrics` (direction), `baselines` (name, bibkey,
how it was run), `main_tables`, `ablation`, `adaptive_attacks`, `overhead`, `limitations`.

## Missing fields

- A missing required field stops the brief with exit code 2 and lists what is missing.
- A missing recommended field is listed under "Missing"; the skill asks once, then writes `[TODO: ...]`.
- Missing numbers are never invented: `\TODO{}` in the draft, listed in `report.md`.
