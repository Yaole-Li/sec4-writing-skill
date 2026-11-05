# SoK papers

Seven of the 241 fit papers are systematisations of knowledge (S&P 5, USENIX 2), all titled `SoK:`
and all written to a different template from an attack or defense paper. A SoK is judged on the
framework it imposes and the evidence it re-examines, not on a new mechanism.

## 1. What a SoK must deliver

1. **A framework.** A taxonomy, a design space, or an evaluation dimension set that prior work did not
   have. The framework is the contribution; it must be stated as an artefact the reader can apply to
   papers published after this one.
2. **A re-evaluation.** At least one claim of the literature tested again under a common protocol:
   baselines re-run on the same data, metrics recomputed, or results reproduced. The S&P SoKs on
   website-fingerprinting defenses and on traffic classifiers both do this.
3. **Coverage with rules.** Inclusion and exclusion criteria, the venues and years covered, and what was
   deliberately left out.
4. **Gaps stated as testable findings.** "No paper in the corpus evaluates X under Y" is a finding;
   "more work is needed" is not.

## 2. Structure that works

```text
1  Introduction          the question the field cannot currently answer
2  Scope and method      corpus construction, inclusion criteria, how claims were normalised
3  Framework             the taxonomy or design space (the deliverable)
4  Mapping               the literature placed in the framework, group by group
5  Re-evaluation         the common-protocol experiment that tests the literature's claims
6  Findings and open problems   numbered, each tied to evidence in §4 or §5
7  Ethics / Open science artefacts used, data released
8  Conclusion
```

## 3. What reviewers attack

- **A list without a framework.** Summaries of forty papers with no organising claim.
- **A framework that fits only the papers cited.** If a new paper cannot be placed in it, it is a
  table, not a design space.
- **Claims about the field that the sample cannot support.** Say which venues, years and search
  strategy; a claim about "the literature" from 30 papers is a claim about those 30.
- **No re-evaluation.** A SoK that never runs anything is a survey and is judged as one.
- **Missing the strongest counter-example.** A paper that contradicts the framework must be discussed.

## 4. Writing notes

- The title carries `SoK:` and then the question, not the topic: `SoK: A Critical Evaluation of ...`.
- The abstract states the framework and the re-evaluation result, in that order.
- Contributions are usually three: the framework, the mapping, the re-evaluation.
- Length runs to the venue's limit; a SoK that stops at eight pages reads as incomplete coverage.

## Checklist

- [ ] A named framework that a future paper can be placed in.
- [ ] Inclusion and exclusion criteria, with venues, years and search method.
- [ ] At least one common-protocol re-evaluation with results.
- [ ] Findings numbered and tied to evidence.
- [ ] Counter-examples to the framework discussed.
- [ ] Artefacts used for the re-evaluation released, or the reason stated.
