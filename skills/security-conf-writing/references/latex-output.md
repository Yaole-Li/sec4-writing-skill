# LaTeX Output

## Template tree

The local template tree has one folder per venue: `SP/`, `NDSS/`, `USENIX/`, and `CCS/`.

Each venue folder contains `main.tex`, `refs.bib`, `README.md`, and a `sec/` directory with section stubs such as title, abstract, introduction, background, threat model, design, evaluation, discussion, conclusion, ethics, open science, and appendix.

The requested conceptual preamble is currently in `main.tex`; the tree has no separate file named `preamble`. Keep shared package and macro definitions in the preamble area of `main.tex` unless the official kit supplies a separate file.

The local README files describe compile-tested scaffolds, official-kit gaps, review anonymity, and exact local build commands. The local PDFs and build logs are generated artifacts and are not source inputs for a submission.

## Classes and official kits

S&P uses `IEEEtran` with the conference option in the local scaffold. Replace the local skeleton with the official IEEE S&P author kit before submission.

NDSS uses `IEEEtran` as a local stand-in. Replace it with the official NDSS kit; the local README records that the NDSS style file is absent from the installed TeX Live environment.

USENIX uses `usenix2019_v3.sty` under the official kit. That style is not in TeX Live. The local tree uses `article` plus `usenixlike.sty` as a compile-tested stand-in, so copy the official style into the venue folder and update the main file before submission.

CCS uses `acmart` with the `sigconf` option. The local scaffold also enables `anonymous` and `review` for review output and uses ACM reference formatting.

These class and kit statements are venue policy or template facts, not measurements from the 241-paper corpus.

## Anonymization mechanics

All four venues require anonymized review submissions under the stated venue conventions. Remove author names, affiliations, acknowledgments, self-identifying artifact URLs, repository names, and identifying metadata from the review PDF.

For S&P, use the anonymous author block required by the official IEEE S&P kit and remove identifying material from text, figures, and artifact references.

For NDSS, omit author-identifying text, acknowledgments, and identifying links in the review version, then follow the official NDSS kit's anonymous mode.

For USENIX, use the official anonymous submission mode and hold author-identifying text, acknowledgments, and artifact URLs until the venue permits disclosure.

For CCS, use `acmart` with `anonymous` and `review` during review. The local CCS README records that these options suppress author-identifying material; verify current ACM instructions before submission.

Do not use a self-citation formulation that reveals identity. Cite the prior work in the same neutral style required for anonymous review.

## Required metadata and sections

CCS requires a CCS Concepts block and `\keywords{...}` in the paper metadata. Keep both in the `acmart` metadata area and replace placeholders with the official taxonomy terms.

USENIX requires an Ethics Considerations section and an Open Science statement. The local USENIX scaffold includes both section stubs; fill them with paper-specific content rather than deleting them.

The corpus reports ethics mentioned anywhere in 178 of 241 papers, an ethics section in 21 of 241 papers, and an open-science statement in 86 of 241 papers. Those are corpus observations; the USENIX requirements above are venue policy.

Use Arabic section numbering for all four venues under the stated conventions. Confirm the official kit if a current call changes a formatting detail.

## Page limits and build

The stated venue body limits are policy facts: S&P allows 13 pages plus unlimited references, USENIX allows 13 pages including everything, NDSS allows 13 pages plus references, and CCS allows 12 pages plus references.

Build each local scaffold from its folder with two `pdflatex` passes:

```sh
cd skills/security-conf-writing/template/SP
pdflatex -interaction=nonstopmode main
pdflatex -interaction=nonstopmode main
```

Use the same command pair after replacing `SP` with `NDSS`, `USENIX`, or `CCS`. Use the official kit and its prescribed bibliography command when the submission tree changes.

## Verification before submission

Search all source files for `\\TODO` and resolve every occurrence. Confirm that every `\\cite` key resolves in `refs.bib` or the official bibliography database.

Build from a clean directory and inspect the log for undefined references, missing citations, overfull boxes, missing files, and class or package errors.

Count PDF pages and compare the result with the applicable venue limit. Check whether references are included under that venue's rule.

Open the PDF and inspect anonymization, figure and table placement, caption readability, CCS metadata, USENIX mandatory sections, and the final bibliography.

## Checklist

- [ ] Are `SP/`, `NDSS/`, `USENIX/`, and `CCS/` mapped to the correct `main.tex`, preamble area, `sec/` stubs, `refs.bib`, and `README.md`?
- [ ] Was the absence of a separate `preamble` file recorded instead of assuming one exists?
- [ ] Was the local IEEEtran scaffold replaced or checked against the official S&P and NDSS kits?
- [ ] Was the USENIX stand-in replaced with official `usenix2019_v3.sty` before submission?
- [ ] Does CCS use `acmart` with `sigconf`, a CCS Concepts block, and `\keywords{}`?
- [ ] Are all four review outputs anonymized, including links, acknowledgments, and metadata?
- [ ] Does USENIX contain Ethics Considerations and an Open Science statement?
- [ ] Are section numbers Arabic under the venue convention?
- [ ] Were two local `pdflatex` passes or the official kit build completed cleanly?
- [ ] Are no `\\TODO` markers left?
- [ ] Does every `\\cite` resolve?
- [ ] Is the PDF page count checked against the applicable policy and reference rule?
