# Security conference LaTeX templates

These four local, compile-tested scaffolds are derived from the supplied corpus measurements. Each folder is self-contained: its `main.tex` inputs only files in that folder and uses only TeX Live classes/packages or the local USENIX stand-in.

| Venue | Class/style used locally | Columns | Section numbering | Page target | Required/important sections | Review anonymity | Artwork constraints |
|---|---|---:|---|---|---|---|---|
| SP | `IEEEtran` `[conference]` (official SP kit is IEEE-based) | 2 | Arabic | 13 body + unlimited references | Ethics is strongly recommended; Open Science optional | Anonymous author block; remove identifying material | Figures/tables in body; exact IEEE/SP artwork rules come from kit |
| NDSS | `IEEEtran` `[conference]` stand-in | 2 | Arabic | 13--15 including references | Ethics and Open Science optional stubs | Anonymous review | Figures/tables in body; official NDSS kit controls final rules |
| USENIX | `article` + local `usenixlike.sty` stand-in | 2 | Arabic, bold | 13 body | Ethics Considerations and Open Science required; artifact badges | Anonymous review | Body figures/tables and official artifact-badge treatment; replace stand-in |
| CCS | `acmart` `[sigconf,anonymous,review]` | 2 | Arabic | 12 body | CCS Concepts and keywords; Ethics/Open Science optional | ACM anonymous/review mode | Body figures/tables under ACM rules; use official CCS instructions |

All unsupplied paper-specific values and artifacts are rendered with the red `\TODO{...}` macro. The local builds use manual `thebibliography` blocks so two `pdflatex` passes resolve citations without requiring BibTeX; each folder also contains `refs.bib` with the same two sample entries for a later official-kit bibliography workflow.

Build a venue with the exact commands in its folder README.
