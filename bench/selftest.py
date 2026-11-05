#!/usr/bin/env python3
"""End-to-end dry run of the benchmark, with no model calls.

  python3 bench/selftest.py [--keep]

It fabricates runs from the venue templates: two models, with and without a simulated skill, on two
cases. The "with skill" drafts are deliberately richer than the "without" ones, so a working pipeline
must show a positive paired difference. Then it packs, judges with judge_stub (three judges), scores and
renders the leaderboard, and copies the artifacts into bench/demo/.

This proves the plumbing: run scaffolding -> blind pack -> judge JSON -> aggregation -> HTML. The scores
it produces are synthetic proxies and are stamped as such everywhere.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench"
TEMPLATES = ROOT / "skills/security-conf-writing/template"
CASES = {"vpn-tunnel-leak": "USENIX", "mcp-ecosystem-census": "SP"}

WITHOUT = {
    "abstract": "This paper studies a security problem. We propose a method and evaluate it. "
                "The results show that the method works well.",
    "intro": "Security problems are important. Prior work has studied them. We propose a method. "
             "We evaluate the method on several datasets. The results show improvements. "
             "In this section we describe the problem and our approach.",
}
WITH = {
    "abstract": "Virtual private networks carry traffic that a passive observer at an access point can "
                "influence. We present two attacks that make a VPN client send traffic outside its tunnel, "
                "and show that the root cause is the routing exception every client adds for the local "
                "network and the VPN server. Across 248 experiments on 67 providers, 126 clients are "
                "vulnerable to the first attack (64.6%) and 39 to the second (73.6%), against a baseline "
                "we re-ran under the same conditions. The evaluations report both the leakage rate and the "
                "false-positive rate at one operating point.",
    "intro": "Virtual private networks are deployed to protect traffic, yet the adversary sits at the "
             "access point where the client configures its routes. Existing studies assume the tunnel is "
             "the only path traffic takes; however, clients keep exceptions for the local network and the "
             "VPN server, and those exceptions are what we exploit. We consider a passive adversary that "
             "controls a Wi-Fi access point or spoofs DNS responses, knows the client model, and cannot "
             "decrypt traffic or touch the device; active injection against the server is out of scope. "
             "Our observation is that the exception list is part of the attack surface, which means the "
             "failure is architectural rather than a bug in one client. We design two attacks that "
             "manipulate the exceptions, one through a rogue access point and one through DNS, and we "
             "measure 67 providers on five operating systems. The evaluation reports 248 experiments, "
             "126 and 39 vulnerable clients, 64.6% and 73.6%, both error directions at one operating "
             "point, and an ablation over client families. Compared with prior fingerprinting work, our "
             "difference is checkable: we do not identify traffic, we reroute it.",
}
REFERENCE = (WITH["abstract"] + "\n\n" + WITH["intro"] +
             "\n\nWe disclosed the findings to the affected vendors before publication, and the artefacts "
             "and the measurement scripts are released.")


def scaffold(case, venue, model, skill):
    run = BENCH / "runs" / case / f"{model}-{'with' if skill else 'without'}"
    if run.exists():
        shutil.rmtree(run)
    paper = run / "outputs" / "paper"
    shutil.copytree(TEMPLATES / venue, paper)
    body = WITH if skill else WITHOUT
    (paper / "sec" / "abstract.tex").write_text(body["abstract"] + "\n", encoding="utf-8")
    (paper / "sec" / "introduction.tex").write_text(body["intro"] + "\n", encoding="utf-8")
    (paper / "sec" / "design.tex").write_text(
        "We design the component in two stages. The first stage collects the observations, the second "
        "one decides. Each component answers the problem the previous one leaves.\n", encoding="utf-8")
    (paper / "sec" / "evaluation.tex").write_text(
        "We evaluate on five platforms. Results are reported per platform with the operating point "
        "fixed, and an ablation removes one component at a time.\n", encoding="utf-8")
    (run / "run.json").write_text(json.dumps(
        {"case": case, "config": f"{model}-{'with' if skill else 'without'}", "model": model,
         "skill": skill, "synthetic": True}, indent=1), encoding="utf-8")
    return run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", action="store_true", help="keep bench/runs, packs and judgments")
    args = ap.parse_args()

    print("1. scaffold synthetic runs")
    for case, venue in CASES.items():
        for model in ("alpha", "beta"):
            for skill in (True, False):
                scaffold(case, venue, model, skill)
        print(f"   {case}: 2 models x with/without = 4 runs ({venue} template)")

    print("2. blind packs")
    for case in CASES:
        ref = BENCH / "runs" / case / "reference.txt"
        ref.write_text(REFERENCE, encoding="utf-8")
        r = subprocess.run([sys.executable, str(BENCH / "pack.py"), "--case", case,
                            "--reference", str(ref)], capture_output=True, text=True)
        print("  ", r.stdout.strip().splitlines()[1] if r.returncode == 0 else r.stderr.strip())
        if r.returncode != 0:
            return 1

    print("3. three stub judges per case")
    for case in CASES:
        for j in ("judge-1", "judge-2", "judge-3"):
            r = subprocess.run([sys.executable, str(BENCH / "judge_stub.py"),
                                "--case", case, "--judge", j], capture_output=True, text=True)
            if r.returncode != 0:
                print(r.stderr); return 1
        print(f"   {case}: 3 judgments")

    print("4. aggregate")
    r = subprocess.run([sys.executable, str(BENCH / "score_judgments.py")], capture_output=True, text=True)
    print("  " + "\n  ".join(r.stdout.strip().splitlines()))
    if r.returncode not in (0,):
        return r.returncode

    print("5. leaderboard")
    r = subprocess.run([sys.executable, str(BENCH / "leaderboard.py")], capture_output=True, text=True)
    print("  " + r.stdout.strip())
    if r.returncode != 0:
        return r.returncode

    demo = BENCH / "demo"
    demo.mkdir(exist_ok=True)
    for f in ("scores.json", "leaderboard.html"):
        shutil.copy(BENCH / f, demo / f)
    print(f"6. demo copied to {demo}/")

    scores = json.loads((BENCH / "scores.json").read_text(encoding="utf-8"))
    delta = scores["paired_delta"]
    ok = bool(delta) and all(v > 0 for v in delta.values()) and scores["synthetic"] is True
    print(f"\npaired differences: {delta}")
    print("verdict:", "pipeline works and shows the richer drafts ahead, as constructed" if ok
          else "CHECK: expected a positive paired difference and a synthetic stamp")

    if not args.keep:
        shutil.rmtree(BENCH / "runs", ignore_errors=True)
        shutil.rmtree(BENCH / "packs", ignore_errors=True)
        shutil.rmtree(BENCH / "judgments", ignore_errors=True)
        print("cleaned bench/runs, bench/packs, bench/judgments (pass --keep to inspect them)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
