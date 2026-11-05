#!/usr/bin/env python3
"""Scaffold (and optionally execute) one run: one configuration on one case.

  python3 bench/run_case.py --case vpn-tunnel-leak --config opus-with
  AGENT_CMD='claude -p --max-turns 40' python3 bench/run_case.py --case vpn-tunnel-leak --config opus-with --agent "$AGENT_CMD"

Without --agent the run directory is created and the prompt path is printed; a human can paste the
prompt into any agent. With --agent the command is executed with the prompt on stdin, in the run's
outputs directory, with the case files already placed there.

Layout of a run:

  bench/runs/<case>/<config>/
    prompt.md        the case prompt, plus a line saying whether the skill is enabled
    skill/           a copy of the skill (present only when the skill is enabled)
    outputs/         the agent writes paper/ and report.md here
    run.json         metadata: case, config, model, skill on/off, timestamps, output checks
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench"
EVALS = ROOT / "skills/security-conf-writing/evals"
SKILL = ROOT / "skills/security-conf-writing"
EXPECTED = ["outputs/paper/main.tex", "outputs/paper/sec/0_abstract.tex",
            "outputs/paper/sec/1_intro.tex", "outputs/paper/main.pdf"]


def load_configs():
    return json.loads((BENCH / "configs.json").read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--config", required=True, help="<model>-<with|without>")
    ap.add_argument("--agent", help="agent command; the prompt is piped to its stdin")
    ap.add_argument("--force", action="store_true", help="reuse an existing run directory")
    args = ap.parse_args()

    cfg = load_configs()
    if "-with" in args.config:
        model, skill_on = args.config.replace("-with", ""), True
    elif "-without" in args.config:
        model, skill_on = args.config.replace("-without", ""), False
    else:
        sys.exit("config must be <model>-with or <model>-without")
    if model not in [m["id"] for m in cfg["models"]]:
        sys.exit(f"unknown model '{model}'; known: {[m['id'] for m in cfg['models']]}")
    if args.case not in cfg["cases"]:
        sys.exit(f"unknown case '{args.case}'; known: {cfg['cases']}")

    case_dir = EVALS / args.case
    run = BENCH / "runs" / args.case / args.config
    if run.exists() and not args.force:
        sys.exit(f"{run} exists; pass --force to reuse it")
    (run / "outputs").mkdir(parents=True, exist_ok=True)

    # 1. place the case files the candidate is allowed to read
    scaffold = case_dir / "place-files.sh"
    if scaffold.exists():
        subprocess.run(["bash", str(scaffold)], cwd=run / "outputs", check=True)

    # 2. the prompt, with an explicit statement of whether the skill is available
    prompt = (case_dir / "prompt.md").read_text(encoding="utf-8")
    if skill_on:
        if (run / "skill").exists():
            shutil.rmtree(run / "skill")
        shutil.copytree(SKILL, run / "skill")
        prompt += ("\n\n---\nThe security-conf-writing skill is installed and available in `skill/`. "
                   "Use it. The files it refers to are relative to `skill/`.\n")
    else:
        prompt += ("\n\n---\nNo writing skill is installed for this run. Write the draft directly from "
                   "the facts above, using your own judgement and the venue template.\n")
    (run / "prompt.md").write_text(prompt, encoding="utf-8")

    meta = {
        "case": args.case, "config": args.config, "model": model,
        "skill": skill_on, "started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agent": args.agent, "settings": cfg["settings"],
    }

    if args.agent:
        t0 = time.time()
        try:
            r = subprocess.run(args.agent, shell=True, input=prompt, text=True,
                               cwd=run / "outputs", capture_output=True,
                               timeout=cfg["settings"]["timeout_seconds"])
            meta["returncode"] = r.returncode
            (run / "agent.stdout.log").write_text(r.stdout or "", encoding="utf-8")
            (run / "agent.stderr.log").write_text(r.stderr or "", encoding="utf-8")
        except subprocess.TimeoutExpired:
            meta["returncode"] = "timeout"
        meta["seconds"] = round(time.time() - t0, 1)

    meta["finished"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    meta["outputs_present"] = {p: (run / p).exists() for p in EXPECTED}
    (run / "run.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")

    missing = [p for p, ok in meta["outputs_present"].items() if not ok]
    print(f"run: {run}")
    print(f"prompt: {run / 'prompt.md'}")
    print("outputs:", "complete" if not missing else f"missing {missing}")
    if not args.agent:
        print("\nTo execute it:\n"
              f"  AGENT_CMD='<your agent cli>' python3 bench/run_case.py --case {args.case} "
              f"--config {args.config} --agent \"$AGENT_CMD\" --force")
    return 0


if __name__ == "__main__":
    sys.exit(main())
