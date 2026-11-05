# ACM CCS scaffold

This folder is a compile-tested scaffold for ACM CCS. Replace local metadata and the current ACM CCS author instructions as needed before submission. The corpus target is 12 pages of body text.

- **Class:** local `acmart` with `[sigconf,anonymous,review]`, two columns, and the local `ACM-Reference-Format.bst`.
- **Review anonymity:** the anonymous/review options suppress author-identifying material; do not add acknowledgments or identifying artifact links during review.
- **Style facts represented:** Arabic section numbering, CCS Concepts metadata, `\keywords{}`, and ACM reference-format selection.
- **Known gap:** exact ACM metadata, rights block, fonts, and current page-count interpretation must follow the CCS call and author kit.

Build exactly with:

```sh
cd skills/security-conf-writing/template/CCS
pdflatex -interaction=nonstopmode main
pdflatex -interaction=nonstopmode main
```
