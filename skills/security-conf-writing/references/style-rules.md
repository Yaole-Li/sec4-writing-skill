# Style rules

Every range below is the p10–p90 band of the fit set, per venue where the venues differ
(`references/corpus/corpus_stats.json`). A draft outside a band is not wrong, it is unrepresentative:
the checker reports it so that the author can decide.

## 1. The register

Security-conference prose is concrete, adversarial and numeric. The median abstract is 230 words with
three numbers; the median introduction is 1,121 words with 18 numbers, because the introduction carries
the evaluation's headline results. Only 9 % of introduction sentences open with "We" or "Our": the
system, the attacker and the data are the subjects. Hedging is rare (0–2 per abstract) and so is
boosting; both are conspicuous when they appear.

| Metric | Abstract (p10–p90) | Introduction (p10–p90) |
|---|---|---|
| Words | 230 (158–529) | 1121 (695–2438) |
| Sentences | 10 (7–23) | 48 (23–107) |
| Mean sentence length | 22.9 (18.5–28.4) | 23.1 (18.9–27.1) |
| Short sentences (≤12 words) | 9 % (0–27 %) | 17 % (8–33 %) |
| Numbers | 3 (0–8) | 18 (4–48) |
| Hedges | 0 (0–2) | 2 (0–10) |
| Boosters | 0 (0–2) | 1 (0–4) |
| Evaluative words | 3 (0–7) | 9 (1–21) |
| Connectors per 100 words | 0.93 (0–1.90) | 0.91 (0.36–1.38) |
| Sentences opening with We/Our | 17 % (0–40 %) | 9 % (0–21 %) |
| Participial tails | 14 % (0–35 %) | 13 % (3–22 %) |
| Passive constructions | 12 % (0–33 %) | 15 % (6–29 %) |

## 2. Per-venue adjustments

| | S&P | USENIX | NDSS |
|---|---|---|---|
| Abstract words | 271 (178–578) | 211 (134–285) | 226 (169–333) |
| Abstract sentences | 12 (8–26) | 9 (5–13) | 9 (7–14) |
| Abstract numbers | 3 (0–8) | 2 (0–7) | 2 (0–10) |
| Introduction words | 993 (644–2038) | 1162 (704–3218) | 1168 (811–1846) |
| Introduction numbers | 18 (5–55) | 18 (0–55) | 20 (9–37) |
| Threat vocabulary in the intro | 2 (0–10) | 3 (0–17) | 5 (1–19) |

S&P rewards a longer, more comparative abstract. USENIX rewards compression and a front-loaded
result. NDSS sits between the two and tolerates the densest introduction.

## 3. Sentences

- Pivots are short: the assumption, the failure, the observation. The rest carry a relation.
- A run of three short sentences is normal in an introduction (median 2, p90 5); six in a row reads
  like slides.
- Participial tails (", enabling ...", ", making ...") appear in 13 % of sentences. Use them for a real
  consequence, not as a way to append significance.

## 4. Numbers

- The abstract carries two or three numbers, each with its setting: dataset, metric, baseline.
- The introduction carries the headline results with their conditions, and the scale of the study
  (accounts, hosts, models, samples). A number without a comparison is decoration.
- Every abstract number must appear in a table or figure.

## 5. Hedging and boosting

- Zero hedges in the abstract is normal; two is the p90. A hedge that undercuts a measured result is
  worse than no hedge.
- Boosters (significantly, remarkably) need a test result or a large margin behind them.
- "State-of-the-art" is common; a claim of it without naming the baselines in the same sentence is not.

## 6. Phrases measured in this corpus

| Phrase | Abstract | Introduction | Verdict |
|---|---|---|---|
| "our attack", "our system" | common | common | normal |
| "to the best of our knowledge" | occasional | common | acceptable with a scoped claim |
| "we propose" / "we present" | common | common | normal |
| "in this paper" | common | common | normal, once |
| "with the rapid development" | rare | rare | rewrite |
| "has attracted increasing attention" | rare | rare | rewrite |
| "plays an important role" | rare | rare | delete |
| "novel" | common | common | say what is new in the same sentence |
| "extensive experiments" | common | common | make it earn itself with a count |

The exact counts live in `references/corpus-profile.md`; the checker encodes the severities.

## 7. Before submitting

- Abstract within the venue's band, numbers attached to their setting.
- No claim the tables cannot support.
- Terms fixed after first definition: an artefact name, an attacker name, a metric name.
- No figure or table reference in the abstract; conference abstracts stand alone.
- Section titles follow the venue's numbering style (all four use arabic numerals).
