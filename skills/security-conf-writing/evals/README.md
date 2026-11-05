# Evaluation cases: held-out security papers

The style bands, exemplar bank and checker thresholds were fitted on 241 of the 268 extracted papers. The
27 held-out papers (S&P 9, USENIX 12, NDSS 6) never enter a rule or an exemplar and are used only here.

| Case | Original paper (hidden at test time) | Venue | Type |
|---|---|---|---|
| `vpn-tunnel-leak` | Bypassing Tunnels: Leaking VPN Client Traffic by Abusing Routing Tables | USENIX Security 2023 | A1 attack |
| `mcp-ecosystem-census` | Parasites in the Toolchain: A Large-Scale Analysis of Attacks on the MCP Ecosystem | IEEE S&P 2026 | A3 measurement |

The original abstracts and introductions are not shipped, for copyright reasons: pass them with
`--reference` when scoring a run.

## Case layout

```
<case>/
  case.yaml        schema_version, name, venue, expected_outcome, context.scaffold_script
  prompt.md        the task plus the author-side facts; no sentence from the paper
  files/refs.bib   the references the candidate may cite, and only these
  place-files.sh   copies files/ into the run directory
  graders/         13 criteria, one markdown file each
```

## The 13 criteria

Seven general (files and template, compilation, citations only from the bib, numbers only from the facts,
ethics and open-science sections present, no process traces, the contribution stated as a claim), two on
form (abstract within the venue band, threat model stated), four case-specific. All are `type: llm`,
`focus: trace`, `weight: 1`: none is a keyword test, because the failures they catch are semantic.

## Scoring

1. **graders** — one judgement per criterion, by a model or a human reading the run directory.
2. **`score_outputs.py`** — deterministic signals: structure, citations against the bib, numbers the case
   did not supply, `[TODO]` count, the venue-aware `check_draft` result, `check_figures`, and (with
   `--reference`) the 8-gram overlap with the original, ignoring n-grams present in the prompt.
   ```bash
   python3 evals/score_outputs.py evals/<case> <run>/outputs --reference <original>.txt
   ```
3. **`rubric.md`** — blind 1–5 comparison of each configuration together with the original paper.

## Anti-leak rules

- The 27 held-out papers are excluded from `references/exemplars/`; `tools/build_exemplars.py` re-checks
  this and prints an error if one appears.
- No rule document quotes a held-out paper.
- A case prompt contains only facts an author would supply.
