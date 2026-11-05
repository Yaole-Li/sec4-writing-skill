# Benchmark: does the skill move a draft closer to a published paper?

This is the fourth layer of the evaluation protocol, the one the reference project published only as a
web page. It answers one question: **given the same facts, is a draft written with the skill closer to
the published paper than the same model's draft written without it?**

The protocol is deliberately the same as the reference project's, so the numbers are comparable:

- candidates per case = every configuration's output **plus the published paper's own abstract and
  introduction**, anonymised as A/B/C/D;
- three judges score every candidate 1–5 on nine dimensions (D1–D9, §3);
- a configuration's score is the mean of D1–D9, pooled over judges and cases.

## 1. Layout

```
bench/
  configs.json          the grid: models × with/without skill × cases
  rubric.md             D1–D9 with 1/3/5 anchors (security-venue version)
  judge_prompt.md       the judge instruction, with the JSON schema the scorer expects
  run_case.py           scaffolds one run and (optionally) invokes an agent CLI
  pack.py               blind pack generator: anonymise candidates into A/B/C/D
  judge_stub.py         deterministic stand-in judge, for self-testing the pipeline only
  score_judgments.py    validates judge JSON, aggregates, writes scores.json
  leaderboard.py        renders leaderboard.html from scores.json
  selftest.py           end-to-end dry run on the venue templates, no model calls
  runs/                 (gitignored) one directory per configuration × case
  packs/                (gitignored) the blind packs handed to judges
  judgments/            (gitignored) one JSON per judge per case
  scores.json           aggregated result of the last scoring run
  leaderboard.html      rendered leaderboard of the last scoring run
```

## 2. Running it for real

```bash
# 1. produce outputs: one run per config per case
export AGENT_CMD='claude -p --max-turns 40'        # or any CLI that takes a prompt on stdin
python3 bench/run_case.py --case vpn-tunnel-leak --config opus-with --agent "$AGENT_CMD"
python3 bench/run_case.py --case vpn-tunnel-leak --config opus-without --agent "$AGENT_CMD"

# 2. blind the candidates (A/B/C/D), plus the published paper as one candidate
python3 bench/pack.py --case vpn-tunnel-leak --reference path/to/original_abstract_intro.txt

# 3. hand each pack to three judges with judge_prompt.md; collect their JSON
#    judgments/<judge>/<case>.json

# 4. aggregate and render
python3 bench/score_judgments.py
python3 bench/leaderboard.py
```

`run_case.py` never invents a run: without `--agent` it only scaffolds the directory and prints the
prompt path, so a human can paste the prompt into any agent.

## 3. The nine dimensions

D1 threat model · D2 gap and failing assumption · D3 novelty of the object · D4 evidence-calibrated
claims · D5 concreteness · D6 positioning · D7 ethics and artefacts · D8 flow and economy · D9
method and experiments.

D1–D8 score the abstract and introduction; D9 scores the method and experiments section, which is why
the reference leaderboard reports it separately. Anchors are in `rubric.md`.

## 4. What the numbers mean

- A **paired** comparison: the same model, the same case, the same facts, the only difference is the
  skill. That is why the headline number is a difference, not a score.
- The published paper is in the pool as a ceiling. A score of 5 means indistinguishable from it, not
  better than it.
- Judge variance is large. Three judges and bootstrap intervals are the minimum; one judge is an anecdote.

## 5. Honesty rules

- `judge_stub.py` exists to prove the pipeline runs. Its scores are deterministic proxies, not opinions,
  and the leaderboard it produces is stamped **SYNTHETIC** in the title and in every row.
- A leaderboard is only published when each case has at least three judges and the pack contains the
  published paper.
- The blind pack is keyed: `packs/<case>/key.json` holds the mapping. Judges must not see it until the
  scoring run is closed.
