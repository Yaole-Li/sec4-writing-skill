# Evaluation

## Setup paragraph

Open Evaluation with one setup paragraph that makes the experiment reproducible in principle.

Name every dataset, its scale, and its provenance. Give counts, units, collection source, filtering, and the train-test or calibration split when those choices affect the claim.

Name every baseline and say whether its code was released or the system was reimplemented. State the version, configuration, and any adaptation required for a fair comparison.

Define each metric, its direction, and its operating point. State whether larger or smaller values are favorable and identify the threshold, budget, false-positive rate, latency target, or other fixed condition.

Report hardware, software versions, concurrency, and random seeds. Give the number of repetitions when a result is averaged or has an error bar.

Put provenance and scale next to the dataset name. A bare dataset label leaves selection and coverage unclear.

## Claim-first paragraphs

Open every evaluation paragraph with the claim that the paragraph tests. The first sentence should tell the reader what the table or figure will establish.

End every claim paragraph by pointing to the table that carries the claim. Use a precise pointer such as "Table 2 reports the comparison at the stated operating point."

Use the middle sentences for setup, observation, and interpretation. Keep observation separate from explanation when the data do not identify a cause.

Order paragraphs by the claims in the introduction. A result that does not answer a stated claim belongs in an appendix or a later analysis.

## Robustness and adaptive evaluation

State the perturbation axis and its range. Examples include input corruption, attacker budget, deployment scale, timing noise, model drift, or resource pressure.

Report static and adaptive numbers separately. Define the adaptive attacker\'s information and interaction budget before giving the result.

If an adaptive attacker was not run, say why in one sentence and identify the remaining evidence. Keep the reason concrete, such as unavailable interface access, a defined scope restriction, or an experiment deferred to future work.

Use the same metric direction and operating point across static and adaptive comparisons. Mark changes in the attacker or data distribution in the table caption.

## Ablations as an argument

Treat an ablation as evidence for a design claim. Give one row or one controlled comparison per design decision.

Map each row to the claim it tests: removing component A tests whether A supplies property P; changing parameter B tests the stated cost or operating tradeoff.

Keep all unrelated settings fixed. State the changed factor, expected direction, observed direction, and interpretation.

Avoid a component dump with no hypothesis. A row earns space when it distinguishes two explanations for the main result.

## Overhead and usability costs

Report overhead as a resource and a denominator: added milliseconds per request, bytes per message, CPU time per input, storage per item, or operator actions per deployment.

State the baseline and operating point for every overhead number. Separate one-time setup cost from per-use cost.

Measure usability costs that affect deployment, such as enrollment steps, required privileges, false alarms, manual review, or compatibility constraints. State who pays each cost.

Include security and performance tradeoffs in the same comparison when the method changes both. Avoid presenting a security gain without the cost that produces it.

## Limitations and corpus evidence

Place limitations in the last Evaluation subsection or in Discussion. The limitation should name the tested range, the untested case, and the consequence for interpreting the claim.

Limitations are mentioned in 214 of 241 corpus papers. Use that prevalence as a completeness check, not as a reason to list generic caveats.

| Practice | Corpus occurrence |
|---|---:|
| Limitations mentioned | 214 of 241 papers |
| Ablation mentioned | 110 of 241 papers |
| Proofs mentioned | 87 of 241 papers |
| Explicit threat-model section | 47 of 241 papers |
| Threat model mentioned anywhere | 157 of 241 papers |

The table reports only supplied corpus counts. It does not imply that every occurrence uses the practice rigorously.

## Checklist

- [ ] Does the setup name datasets with scale and provenance?
- [ ] Does every baseline identify released code or reimplementation, version, and configuration?
- [ ] Does every metric state direction and operating point?
- [ ] Are hardware, software versions, concurrency, seeds, and repetitions reported?
- [ ] Does every paragraph open with a claim and end at the table or figure that carries it?
- [ ] Does every robustness result state the perturbation axis and range?
- [ ] Are static and adaptive attacker results separated and defined?
- [ ] If no adaptive attacker was run, is the concrete reason stated in one sentence?
- [ ] Does each ablation row map to one design decision and one claim?
- [ ] Are overhead and usability costs reported with denominators, baselines, and operating points?
- [ ] Are limitations in the last Evaluation subsection or Discussion, with tested and untested ranges?
- [ ] Does the final draft address the supplied corpus practices without inventing counts?
