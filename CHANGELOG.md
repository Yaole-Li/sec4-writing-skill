# Changelog

## v1.0

First release, fitted on 268 security papers (S&P 95, USENIX 116, NDSS 57; 2023–2026); 241 fit, 27 held out.

- Workflow for Title, Abstract, Introduction, Related Work, Threat Model, Design, Evaluation, Ethics,
  Open Science and Conclusion, for Claude Code and Codex.
- Per-venue style bands for S&P, USENIX and NDSS (the venues have different abstract and introduction
  budgets), with CCS handled as labelled convention because the corpus contains no CCS papers.
- Routing by paper type (A1 attack, A2 defense, A3 measurement, A4 system, A5 analysis, A6 SoK,
  A7 dataset) and gap type (new-surface, failure, assumption-gap, cost, capability-gap, scale-gap,
  insight), with a separate SoK route.
- Reference documents: venue guide, abstract, introduction, related work, threat model, method,
  evaluation, figures, ethics and disclosure, artefact and open science, style rules, claim calibration,
  LaTeX output, corpus profile.
- Exemplar bank: 392 verbatim sentences tagged by move and venue, 117 whole abstracts, 125 phrase frames.
- Venue-aware checkers: `check_draft.py --venue`, `check_figures.py`, `style_metrics.py`,
  `find_exemplars.py` (with `--venue` and `--abstracts`), `intake_to_brief.py`.
- Four LaTeX templates (SP, NDSS, USENIX, CCS), each verified to compile twice with pdflatex.
- Held-out evaluation: two cases with 13 graders each, a blind rubric and `score_outputs.py`.
