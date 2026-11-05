# Corpus profile

Two sources feed every number in this skill.

- **Style and structure** are computed by `scripts/style_metrics.py` over the 241 fit papers' abstracts
  and sections; the machinery is `data/corpus_stats.json`, shipped as
  `references/corpus/corpus_stats.json`. Per-venue distributions sit under `style_by_venue`.
- **Rhetorical structure** comes from 120 annotated papers (S&P 42, USENIX 52, NDSS 26): paper type, gap
  type, threat-model / ethics / open-science placement, and 392 verbatim sentences tagged with a
  rhetorical move. The sentences are in `references/exemplars/`; the counts here.

Thirteen per cent of the corpus is held out: 27 papers (S&P 9, USENIX 12, NDSS 6) never enter a rule or an
exemplar and are used only in `evals/`.

## 1. What the corpus is, and what it is not

| Item | Value |
|---|---|
| PDFs extracted | 268 |
| Fit / held out | 241 / 27 |
| Venues | S&P 95, USENIX 116, NDSS 57 (all PDFs) — **no CCS papers** |
| Years | 2023–2026 |
| Pages | 19 (17–21), including references and appendices |

Topic skew matters for interpreting the rules. The index tags 116 of 268 papers as large-language-model
work, 61 as traffic analysis and 18 as agent work. This is not a uniform sample of the four venues: it is
a sample weighted toward network security, LLM security and privacy measurement. Rules that hold across
all of it are safe; venue-level claims about, say, hardware side channels rest on a handful of papers.

Eight USENIX abstracts could not be extracted (the abstract sits outside the text layer) and are excluded
from abstract statistics only. Four USENIX introductions were similarly degenerate and are excluded from
introduction statistics only.

## 2. Structure

| Observation | S&P | USENIX | NDSS |
|---|---|---|---|
| Pages, median (min–max) | 19 (15–20) | 21 (18–21) | 18 (14–20) |
| Figures / tables, median | 9 / 8 | 8 / 8 | 11 / 9 |
| Floats per page | 1.05 | 0.81 | 1.17 |
| Sections, median | 6 | 6 | 7 |
| Related-work section | 74 / 86 | 71 / 104 | 40 / 51 |
| Explicit threat-model section | 15 / 86 | 22 / 104 | 10 / 51 |
| Threat model anywhere in the text | 47 / 86 | 73 / 104 | 37 / 51 |
| Ethics heading | 5 / 86 | 15 / 104 | 7 / 51 |
| Ethics mentioned anywhere | 57 / 86 | 89 / 104 | 32 / 51 |
| Open-science statement | 3 / 86 | 9 / 104 | 8 / 51 |
| Limitations mentioned | 75 / 86 | 96 / 104 | 43 / 51 |
| Ablation mentioned | 39 / 86 | 46 / 104 | 25 / 51 |
| Title contains a colon | 74 % | 76 % | 69 % |

Pooled over the fit set: related-work section 185 / 241, threat model mentioned 157 / 241, ethics
mentioned 178 / 241, open science 86 / 241, limitations 214 / 241, ablation 110 / 241, proofs 87 / 241.

## 3. Section lengths

Median words, over the papers that have the section:

| Section | Median (p10–p90) | Papers |
|---|---|---|
| Related Work | 1017 (352–4414) | 183 |
| Threat Model | 1066 (420–3912) | 47 |
| Method / Design | 2569 (463–5351) | 137 |
| Evaluation / Experiments | 3187 (1116–5747) | 171 |
| Discussion | 589 (190–1361) | 103 |
| Conclusion | 478 (152–2087) | 144 |
| Ethics | 484 (92–2727) | 18 |
| Open Science | 175 (124–2173) | 9 |

Mean sentence length inside these sections runs 19.4 to 22.5 words, slightly shorter than in the abstract.

## 4. Abstract and introduction

| | S&P | USENIX | NDSS | Pooled |
|---|---|---|---|---|
| Abstract words | 271 (178–578) | 211 (134–285) | 226 (169–333) | 230 (158–547) |
| Abstract sentences | 12 | 9 | 9 | 10 |
| Abstract numbers | 3 (0–8) | 2 (0–7) | 2 (0–10) | 3 (0–8) |
| Introduction words | 993 (644–2038) | 1162 (704–3218) | 1168 (811–1846) | 1121 (695–2438) |
| Introduction sentences | 45 | 48 | 51 | 48 |
| Introduction numbers | 18 (5–55) | 18 (0–55) | 20 (9–37) | 18 (4–48) |

## 5. Paper types and gaps (120 annotated papers)

| Type | Papers |
|---|---|
| A1 attack | 35 |
| A4 system | 28 |
| A3 measurement | 25 |
| A2 defense | 14 |
| A5 analysis or construction | 8 |
| A6 SoK | 5 |
| A7 dataset or benchmark | 5 |

| Gap type | Papers |
|---|---|
| capability-gap | 28 |
| new-surface | 25 |
| assumption-gap | 15 |
| failure | 15 |
| insight | 14 |
| cost | 13 |
| scale-gap | 10 |

`new-surface` is the second most common gap in this corpus and would be rare in a corpus drawn from
before 2022: it is the LLM wave showing up as an argumentative pattern.

## 6. Threat model, ethics and open science, as annotated

| Field | Distribution (120 papers) |
|---|---|
| Threat model | implicit 47, own section 31, introduction paragraph 23, absent 15 |
| Ethics statement | absent 105, introduction paragraph 8, own section 6, appendix 1 |
| Open-science statement | absent 77, introduction sentence 41, own section 2 |

The threat model is usually implicit in prose rather than a sectional one, and the ethics statement is
usually absent even where the subject matter calls for one. That is the corpus, not the ideal: the
venue-guide and ethics documents state what the venues require, and the checker warns when a draft is
missing them.

## 7. Style bands the checker uses

| Metric | Abstract | Introduction |
|---|---|---|
| Mean sentence length | 22.9 (18.5–28.4) | 23.1 (18.9–27.1) |
| Short sentences (≤12 words) | 9 % (0–27 %) | 17 % (8–33 %) |
| Run of short sentences | 1 (0–2) | 2 (1–5) |
| Participial tails | 14 % (0–35 %) | 13 % (3–22 %) |
| Connectors per 100 words | 0.93 (0–1.90) | 0.91 (0.36–1.38) |
| Hedges | 0 (0–2) | 2 (0–10) |
| Boosters | 0 (0–2) | 1 (0–4) |
| Sentences opening with We/Our | 17 % (0–40 %) | 9 % (0–21 %) |
| Passive constructions | 12 % (0–33 %) | 15 % (6–29 %) |

## 8. Phrase frequencies (papers containing the phrase, out of 241)

| Phrase | Abstract | Introduction |
|---|---|---|
| novel | 72 | 107 |
| state-of-the-art | 52 | 76 |
| significantly | 55 | 103 |
| extensive experiments | 28 | 28 |
| in this paper, we propose | 19 | 19 |
| our contributions | 4 | 57 |
| to the best of our knowledge | 2 | 21 |
| in recent years | 4 | 17 |
| delve | 3 | 5 |
| pivotal | 2 | 4 |
| with the rapid development | 1 | 0 |
| has attracted increasing attention | 1 | 1 |
| plays an important role | 0 | 0 |

## 9. Figures and tables

| Observation | Value |
|---|---|
| Caption words, median (p10–p90) | 28.5 (6–94) |
| Figure 1 caption words | 53.5 |
| Table caption words | 20 (6–88) |
| Figures / tables per paper | 9 / 8 |
| Floats per page | 0.95 (0.52–1.39) |

Captions in security papers are longer than in the TIFS corpus (median 28.5 words against 14): they
carry the setting as well as the takeaway, because a security figure usually needs its threat setting
named.

## 10. What was measured and what was not

Measured: style bands, section lengths and presence, venue differences, paper and gap types, threat-model
and ethics placement, 392 verbatim exemplar sentences, phrase frequencies, figure and table counts.

Not measured, and stated as convention instead: page limits, anonymity rules, the CCS class and its
metadata, artefact badge processes. CCS has no papers in the corpus at all, so every CCS statement in
this skill is a convention borrowed from the ACM class and from the other three venues.

Paragraph-level rhetorical sequences were attempted and abandoned: the three layouts do not yield
reliable paragraph boundaries from extracted text. The consequence is documented in
`references/introduction.md` §3.
