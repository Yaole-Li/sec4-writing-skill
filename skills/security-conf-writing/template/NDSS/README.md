# NDSS scaffold

This folder is a compile-tested scaffold for the Network and Distributed System Security Symposium (NDSS). Replace the local IEEE skeleton with the official NDSS author kit before submission; `ndss.sty` is absent from this TeX Live installation. The corpus target is 13--15 pages including references.

- **Class:** local `IEEEtran` with `[conference]`, 10pt, two columns, IEEE-like layout.
- **Review anonymity:** omit author names, affiliations, acknowledgments, and identifying links in review submissions.
- **Style facts represented:** Arabic section numbering, Abstract run-in, and a visible placeholder for the NDSS symposium/DOI footnote block.
- **Known gap:** exact NDSS typography, footer block, margins, and page-count rules require the official kit.

Build exactly with:

```sh
cd skills/security-conf-writing/template/NDSS
pdflatex -interaction=nonstopmode main
pdflatex -interaction=nonstopmode main
```
