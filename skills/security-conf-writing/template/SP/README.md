# IEEE S&P scaffold

This folder is a compile-tested scaffold for IEEE Symposium on Security and Privacy (SP). The official submission kit is the IEEE S&P author kit; replace this local `IEEEtran` skeleton with the current conference style files before submission. The corpus target is 13 pages of body text plus unlimited references, with figures and tables in the body.

- **Class:** local `IEEEtran` with `[conference]`, 10pt, two columns, US letter. The official kit is IEEE-based; this local build proves the skeleton, not the exact house style.
- **Review anonymity:** remove author names, affiliations, acknowledgments, and identifying artifact URLs in the review version.
- **Style facts represented:** Arabic section numbering, bold-italic run-in Abstract, no Index Terms, and an IEEE-style footer note.
- **Known gap:** the exact SP copyright footer, fonts, spacing, and current page accounting come from the official kit.

Build exactly with:

```sh
cd skills/security-conf-writing/template/SP
pdflatex -interaction=nonstopmode main
pdflatex -interaction=nonstopmode main
```
