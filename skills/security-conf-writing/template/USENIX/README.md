# USENIX Security scaffold

This folder uses a local `usenixlike.sty` stand-in because `usenix2019_v3.sty` is not in TeX Live. Replace it with the official `usenix2019_v3.sty` and the conference kit before submission. The corpus target is 13 pages of body text.

- **Class:** local `article` with `[letterpaper,twocolumn,10pt]`; the stand-in sets 1in margins, approximately 0.75in gutter, no page numbers, bold Arabic sections, bold run-in Abstract, and small-caps paragraphs.
- **Review anonymity:** use the official anonymous mode and remove author-identifying text, acknowledgments, and artifact URLs until permitted.
- **Required content:** Ethics Considerations and Open Science are included as required sections; artifact badges are represented as red placeholders.
- **Known gap:** the stand-in cannot reproduce the official fonts, spacing, title block, copyright text, or exact page accounting.

Build exactly with:

```sh
cd skills/security-conf-writing/template/USENIX
pdflatex -interaction=nonstopmode main
pdflatex -interaction=nonstopmode main
```
