# Open science and artefacts

USENIX Security requires a statement of what is released; S&P, NDSS and CCS expect one whenever code,
data or a testbed is part of the contribution. In the fit set, 78 of 104 USENIX papers state artefact
availability somewhere, against 3 of 86 at S&P and 8 of 51 at NDSS, where the statement is often a
sentence at the end of the introduction instead of a section.

## 1. What the statement answers

1. **What is released**: code, dataset, prompts, model weights, measurement traces, configuration.
2. **Where**: a repository URL, an anonymous mirror for review, or a DOI. An anonymised artefact link is
   mandatory during review at all four venues.
3. **Under which licence**, especially for data derived from other people's content.
4. **What is withheld, and why**: exploit details under embargo, personally identifiable data, model
   outputs that reproduce harm.
5. **How the evaluation can be reproduced**: which figure or table each artefact reproduces, and the
   command that does it.

## 2. Two valid shapes

**A short section** (USENIX, and increasingly S&P):

```text
Open Science
Our code, configuration files and the scripts that reproduce Figures 3-5 and Table 2 are available at
\TODO{anonymous URL} under \TODO{licence}. The measurement dataset is released as \TODO{what}; raw
traces are withheld because \TODO{reason}. The \TODO{model checkpoints} are released under
\TODO{licence}.
```

**One paragraph at the end of the introduction** (most common at S&P and NDSS):

> Our code and datasets are publicly available at \TODO{URL}.

The paragraph satisfies the form, the section satisfies the reviewer who wants to reproduce. When the
artefact is the contribution (A7), use the section.

## 3. Artefact badges

USENIX and CCS run artefact evaluation (Available, Functional, Reusable, Results Reproduced). Badges are
not required to publish, but the evaluation asks for the same facts as §1, so a paper that states them
clearly is already most of the way there. Badges appear as images in the proceedings PDFs, which is why
a text census of published papers finds none; their absence in the corpus is an artefact of extraction,
not evidence that authors ignore them.

## 4. What not to do

- Do not claim availability without a link that a reviewer can open anonymously.
- Do not promise data that cannot be shared for legal or ethical reasons; state the reason instead.
- Do not list an artefact that reproduces nothing; say which table it reproduces.
- Do not put the statement only in the appendix: a reviewer deciding on the artefact may not read it.

## 5. Checklist

- [ ] What is released, where, and under which licence.
- [ ] What is withheld and why.
- [ ] Which figure, table or claim each artefact reproduces.
- [ ] Anonymised link during review; permanent link for the camera-ready.
- [ ] For a dataset or benchmark paper: split definition, licence, and a datasheet-style summary.
