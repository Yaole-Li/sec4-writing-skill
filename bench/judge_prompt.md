# Judge instruction

You are scoring blind drafts of a security-conference paper. You do not know which candidate is which.
One of the candidates is the published paper; the rest are model outputs. Your job is to score each
candidate on nine dimensions and rank them.

## What you receive

- `CASE`: the case name.
- `PACK`: four candidates labelled A, B, C, D. Each has an abstract, an introduction, and an excerpt from
  the design and evaluation sections.
- `RUBRIC`: the nine dimensions with their 1 / 3 / 5 anchors.

## What you return

One JSON object, and nothing else:

```json
{
  "case": "<CASE>",
  "judge": "<your judge id>",
  "scores": {
    "A": {"D1": 4, "D2": 3, "D3": 4, "D4": 4, "D5": 3, "D6": 3, "D7": 2, "D8": 4, "D9": 3,
          "note": "one sentence on the single most important difference from the published paper"},
    "B": {"D1": 2, "D2": 2, "D3": 2, "D4": 1, "D5": 2, "D6": 1, "D7": 1, "D8": 3, "D9": 2,
          "note": "..."},
    "C": {"...": 0},
    "D": {"...": 0}
  },
  "ranking": ["C", "A", "D", "B"]
}
```

Rules

1. Integers 1–5 for every dimension of every candidate. No half points.
2. Any invented number, dataset, baseline, attacker capability, approval or citation sets D4 to 1 for that
   candidate, whatever else it does.
3. An attack or defense draft with no threat model cannot exceed 3 on D1 or D4.
4. Length is not rewarded. A long candidate does not rank higher for being long.
5. Judge against the venue's own papers, not against your taste. If you recognise a candidate as a
   published paper, score it on its qualities and do not adjust for provenance.
6. The notes are one sentence each. No essays.

## Filling the template

```
CASE: {{CASE}}

RUBRIC:
{{RUBRIC}}

PACK:
{{PACK}}
```
