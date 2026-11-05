# Abstract

One paragraph, no citations, no figure or table references, no undefined abbreviations. It is the part
every reviewer reads and the part most drafts overspend.

## 1. Budget, by venue

| | S&P (86) | USENIX (104) | NDSS (51) | CCs (policy) |
|---|---|---|---|---|
| Words, median (p10–p90) | 271 (178–578) | 211 (134–285) | 226 (169–333) | 150–250 recommended |
| Sentences, median | 12 | 9 | 9 | 8–12 |
| Numbers, median | 3 | 2 | 2 | 2–4 |

The S&P abstract is the longest of the three and it earns the length with a comparison; the USENIX
abstract is the tightest and front-loads the result. A 270-word abstract at USENIX reads as an S&P
submission, and a 200-word abstract at S&P reads as a short paper. Pick the venue before writing.

## 2. Shape

```text
L  landscape or threat    what is deployed, who is exposed            (1-2 sentences)
G  gap                    the assumption that breaks, and its cost    (1-2)
A  attacker or setting    the capability that makes the claim testable (0-1)
I  idea                   the observation the design follows from     (0-1)
M  method                 what was built, components in causal order  (1-3)
S  security property      what holds, or what is only measured        (0-1)
R  result                 numbers with dataset, metric and baseline   (1-3)
K  release / X scope      what is released, what is out of scope      (0-1)
```

`L → G → M → R` is the backbone; the annotated sample adds `S` or `X` in roughly half the papers.

## 3. Sentence by sentence

**L — the deployed reality.** Name the thing that is deployed and the exposure that follows from it.

> Keystroke timing attacks have long been recognized as a serious security concern. — S&P 2023

> Security operators use red teams to simulate real attackers and proactively find defense gaps.
> — S&P 2025

> Large language models (LLMs) are increasingly used for code generation in fast, informal development
> workflows, often referred to as vibe coding, where speed and convenience are prioritized. — USENIX 2025

Avoid the growth cliché. "With the rapid development of ..." is rare in this corpus and marks a draft
written for a different venue.

**G — the assumption that breaks.** Not "existing methods have limitations": say what they assume, and
what that assumption costs when it fails.

**A — the attacker.** One sentence naming the capability the evaluation grants. It is what makes the
number that follows meaningful, and it is the sentence a reviewer checks against the threat model.

**I — the idea.** An observation about the problem, stated directly. Never "our key insight is".

**M — the method.** The components in the order data flows through them. Name the artefact once, then
use the name.

**S — the property.** What is guaranteed, or what is only measured, and under which attacker.

**R — the result.** Two to three numbers, each attached to its dataset, metric and baseline. Lead with
the comparison that carries the claim:

> CAMEO reaches 72.85% to 94.88% closed-world top-1 accuracy ... ahead of every baseline on every
> platform.

**K / X — release and scope.** One sentence: what is released, and what the claim does not cover.

## 4. Rules

- No citations. No equations. No `\cref{}` to a figure or table.
- Every number in the abstract appears in the evaluation.
- No undefined abbreviation: expand once in the abstract, use the short form afterwards.
- No claim the tables cannot support: "state-of-the-art" without naming the baseline is not a result.
- The abstract states the same strength of claim as the introduction's results paragraph, word for word
  where possible.

## 5. What to cut on the second pass

- Sentences that explain why the area matters (the reviewer already knows).
- Any adjective without a number behind it.
- Historical background, prior-work detail, implementation detail.
- The second and third restatement of the same claim.

## Checklist

- [ ] Within the venue's band (S&P 271, USENIX 211, NDSS 226 words at the median).
- [ ] First two sentences contain the deployed reality and the exposure.
- [ ] The gap names an assumption.
- [ ] The attacker is named in one sentence.
- [ ] Two to three numbers, each with dataset, metric and baseline.
- [ ] No citations, equations, figure references or undefined abbreviations.
- [ ] The strength of claim matches the evaluation.
