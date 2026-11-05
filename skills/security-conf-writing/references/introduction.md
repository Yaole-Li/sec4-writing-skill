# Introduction

The introduction is where a security paper is accepted or rejected in the reviewer's first pass: it has
to establish the deployed reality, the assumption that breaks, the attacker, and the headline numbers,
in that order, before the design appears.

## 1. Budget, by venue

| Metric | S&P (83) | USENIX (90) | NDSS (51) | Pooled (224) |
|---|---|---|---|---|
| Words, median (p10–p90) | 993 (644–2038) | 1162 (704–3218) | 1168 (811–1846) | 1121 (695–2438) |
| Sentences, median | 45 | 48 | 51 | 48 |
| Mean sentence length | 22.4 | 23.3 | 24.2 | 23.1 |
| Numbers, median (p10–p90) | 18 (5–55) | 18 (0–55) | 20 (9–37) | 18 (4–48) |
| Evaluative words, median | 7.5 | 9.5 | 10 | 9 |
| Threat vocabulary, median | 2 | 3 | 5 | 3 |
| Sentences opening with We/Our | 11 % | 8.5 % | 8 % | 9 % |

The counts in parentheses are papers with a usable introduction; eight USENIX abstracts and a handful of
introductions could not be extracted and are excluded from that section's distribution only.

## 2. Shape

```text
P1  L  the deployed reality: what technology, who is exposed, at what scale
P2  C  what prior work does, group by group, with what each assumes
P3  G  the assumption that breaks, the condition, and the cost  <- the pivot paragraph
P4  A  the attacker: goal, knowledge, capability, out of scope
P5  I  the observation the design follows from, in one sentence
P6  M  the design, components in causal order
P7  S  what holds: the property claimed, or the measurement made
P8  R  headline numbers with dataset, metric and baseline
P9  K  contributions, when the venue expects a list
P10 E/O ethics, disclosure and artefact availability, one short paragraph
```

Eight to ten paragraphs at S&P and NDSS; USENIX papers run longer because the introduction carries more
of the evaluation.

## 3. What the corpus shows about each move

The annotated sample (120 papers) tagged 395 verbatim sentences with a rhetorical function. Counts below
are papers in which at least one such sentence was annotated, which is a lower bound: annotators quoted
two to four sentences per paper, so a function can be present without being counted.

| Move | Papers (of 120) | What it does |
|---|---|---|
| `intro.landscape` | 41 | names the deployed technology and the exposure |
| `intro.attacker` | 39 | states the adversary's capability |
| `intro.method` | 31 | summarises the design |
| `intro.gap.*` (failure / new-surface / assumption / cost / scale) | 25 | the assumption that breaks |
| `intro.security` | 21 | what the design guarantees, or what it only measures |
| `intro.contributions` | 20 | the enumerated list |
| `intro.openscience` | 20 | artefacts released |
| `intro.results` | 19 | headline numbers |
| `intro.credit` | 17 | what prior work does |
| `intro.stance` | 12 | impact and limits |
| `intro.ethics` | 11 | IRB, disclosure, dual use |
| `intro.insight` | 6 | the observation the design follows from |
| `intro.positioning` | 4 | the closest work, named |

Two readings matter. The attacker and the landscape dominate, which fits a venue whose reviewers are
adversarial by training. The insight is rarely an explicit sentence: it usually rides inside the method
paragraph, which is why a draft that never states one still reads as if it had.

*Measurement note:* paragraph-level function sequences were attempted first and abandoned. The three
layouts (IEEE two-column, USENIX two-column, NDSS two-column) do not yield reliable paragraph boundaries
from extracted text, so a sequence-per-paragraph statistic would be an artefact of line wrapping. The
tiers below are therefore qualitative, grounded in the section census (`references/corpus-profile.md`)
and in the annotated sentences above.

## 4. Tiers

**Always** (section census: introduction in 241/241; threat model mentioned in 157/241; limitations in
214/241): the deployed reality, the gap with its assumption, the attacker, the design, the numbers.

**Usual**: a contributions list (S&P and CCS expect one; USENIX tolerates prose), an ethics sentence, an
open-science sentence at USENIX, the closest-work comparison inside the gap paragraph.

**Optional**: a roadmap paragraph (4 of 241 papers in the TIFS corpus family keep one; here it is rare
and reviewers do not miss it), a stance paragraph, a formal insight sentence.

## 5. The four paragraphs that decide the review

**P1, the deployed reality.** A concrete technology and a concrete exposure, not a discipline.

> Many protocols, like HTTP, FTP, POP3, and SMTP, were originally designed as synchronous plaintext
> protocols, commands and data are sent in the clear. — USENIX 2025

> QUIC is a modern transport protocol increasingly adopted by major platforms and services, making its
> security and correctness critically important. — NDSS 2026

**P3, the gap.** The assumption that breaks, stated as a fact about prior work.

> However, existing rule-based systems suffer low detection accuracy, especially the high false alarms,
> due to the lack of fine-grained rules and environment constraints. — NDSS 2025

> Despite the efficacy of fuzzing in verifying the implementation correctness of network protocols,
> existing IoT protocol fuzzing approaches grapple with ... — S&P 2025

**P4, the attacker.** Goal, knowledge, capability, out of scope. One paragraph, four sentences, and the
same attacker must appear in the threat-model section and in the evaluation.

**P6, the design in causal order.** Each component answers the residue the previous one leaves.
Components listed in parallel ("A does X. B does Y.") read as a bag of tricks and are the most common
structural weakness in rejected submissions.

## 6. Numbers

The introduction carries the evaluation's headline results, with their settings, plus the scale of the
study: hosts scanned, users interviewed, models tested, samples collected. A number without a comparison
is decoration, and a number that appears nowhere in the evaluation is a fabrication risk.

## 7. Positioning

One sentence, inside P2 or P3, naming the closest work and one checkable difference: mechanism, scope,
cost, assumption, input, output, or evaluation. A standalone "difference from prior work" paragraph is
rare in this corpus and usually redundant with the related-work section.

## 8. Contributions

A list of three contributions is the norm at S&P and CCS, and common at USENIX and NDSS. Each item
states what was done and what it achieves, in one sentence; no item restates another. For a SoK, the
three are the framework, the mapping, and the re-evaluation (`references/sok.md`).

## Checklist

- [ ] P1 names a concrete technology and a concrete exposure.
- [ ] P3 names the assumption that breaks, not "existing methods have limitations".
- [ ] P4 gives goal, knowledge, capability and out-of-scope for the attacker.
- [ ] The attacker in P4 matches the threat-model section and the evaluation.
- [ ] P5 or P6 states the observation the design follows from.
- [ ] Components appear in causal order, not as a list.
- [ ] Headline numbers carry dataset, metric and baseline.
- [ ] The closest work appears with one checkable difference.
- [ ] Ethics and artefact sentences present where the venue expects them.
- [ ] Within the venue's word band; every number in the abstract appears here.
