#!/usr/bin/env python3
"""Deterministic signals for one evaluation run.

  python3 evals/score_outputs.py evals/<case> <run>/outputs [--reference original.txt] [--json]

It does NOT produce a single score. It reports the things a judge should not have to check by hand:
which files exist, whether the LaTeX compiles into the expected paths, whether every citation key is in
the case's bib, whether every number in the draft is one the case supplied, how many [TODO] remain,
what check_draft.py and check_figures.py say, and — when a reference text is given — the 8-gram overlap
with the original paper (memorisation), ignoring n-grams that already appear in the case input.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SCRIPTS = SKILL / "scripts"

NUMBER = re.compile(r"(?<![A-Za-z\d.])\d+(?:[.,]\d+)*(?![A-Za-z\d])")
CITE = re.compile(r"\\cite[tp]?\{([^}]*)\}")


def read(p):
    try:
        return Path(p).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def ngrams(s, n=8):
    w = re.findall(r"[a-z0-9]+", s.lower())
    return [" ".join(w[i:i + n]) for i in range(len(w) - n + 1)]


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as ex:  # noqa: BLE001
        return 99, repr(ex)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("case_dir")
    ap.add_argument("run_dir")
    ap.add_argument("--reference")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    case = Path(args.case_dir)
    run_dir = Path(args.run_dir)
    out = {"case": case.name, "run": str(run_dir)}

    # venue from case.yaml, used by the venue-aware checker
    venue = "USENIX"
    cy = read(case / "case.yaml")
    m = re.search(r"^venue:\s*(\w+)", cy, re.M)
    if m:
        venue = m.group(1)

    # 1. structure
    tex = run_dir / "paper" / "main.tex"
    files = {
        "main.tex": tex.exists(),
        "abstract": (run_dir / "paper" / "sec" / "0_abstract.tex").exists(),
        "intro": (run_dir / "paper" / "sec" / "1_intro.tex").exists(),
        "pdf": (run_dir / "paper" / "main.pdf").exists(),
    }
    out["structure"] = files

    body = " ".join(read(p) for p in sorted(run_dir.rglob("*.tex")))
    body += " ".join(read(p) for p in sorted(run_dir.rglob("*.md")))

    # 2. citations against the case bib
    bib = read(case / "files" / "refs.bib")
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    cited = set()
    for m in CITE.finditer(body):
        cited |= {k.strip() for k in m.group(1).split(",") if k.strip()}
    out["citations"] = {"cited": len(cited), "bib": len(bib_keys),
                        "not_in_bib": sorted(cited - bib_keys),
                        "uncited_bib": sorted(bib_keys - cited)}

    # 3. numbers: which ones were supplied by the case
    prompt = read(case / "prompt.md")
    supplied = {n.replace(",", "") for n in NUMBER.findall(prompt)}
    used = {n.replace(",", "") for n in NUMBER.findall(body)}
    suspicious = sorted(n for n in used - supplied if not re.fullmatch(r"(19|20)\d\d", n)
                        and not re.fullmatch(r"[0-9]", n) and int(float(n)) > 10)
    out["numbers"] = {"used": len(used), "supplied": len(supplied), "unsupplied": suspicious[:25],
                      "unsupplied_count": len(suspicious)}
    out["todos"] = len(re.findall(r"\\TODO\{|\[TODO", body))

    # 4. skill checkers
    if tex.exists():
        rc, log = run(["python3", str(SCRIPTS / "check_draft.py"), "--json", "--venue", venue, str(tex)])
        try:
            parsed = json.loads(log[log.index("["):]) if "[" in log else []
            issues = parsed[0]["issues"] if parsed else []
        except Exception:  # noqa: BLE001
            issues = []
        out["check_draft"] = {"errors": sum(1 for i in issues if i[0] == "ERROR"),
                              "warns": sum(1 for i in issues if i[0] == "WARN"),
                              "notes": sum(1 for i in issues if i[0] == "NOTE")}
        rc, log2 = run(["python3", str(SCRIPTS / "check_figures.py"), str(tex)])
        out["check_figures"] = {"errors": log2.count("\nERROR") + log2.startswith("ERROR"),
                                "warns": log2.count("\nWARN") + log2.startswith("WARN")}

    # 5. overlap with the original (memorisation), ignoring n-grams present in the prompt
    if args.reference:
        ref = read(args.reference)
        ref_g = set(ngrams(ref))
        prompt_g = set(ngrams(prompt))
        cand = set(ngrams(body))
        shared = (cand & ref_g) - prompt_g
        ref_words = [g.split() for g in ref_g]
        out["overlap"] = {"shared_8grams": len(shared), "examples": sorted(shared)[:5]}
        # longest shared word run
        cw = re.findall(r"[a-z0-9]+", body.lower())
        rw = re.findall(r"[a-z0-9]+", ref.lower())
        rset = {tuple(rw[i:i + 6]) for i in range(len(rw) - 5)}
        best, cur = 0, 0
        for i in range(len(cw) - 5):
            if tuple(cw[i:i + 6]) in rset:
                cur += 1
                best = max(best, cur + 5)
            else:
                cur = 0
        out["overlap"]["longest_shared_run"] = best

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print(f"case {out['case']}  run {out['run']}")
        print("  structure:", files)
        c = out["citations"]
        print(f"  citations: {c['cited']} cited, {len(c['not_in_bib'])} not in bib {c['not_in_bib'][:5]}, "
              f"{len(c['uncited_bib'])} bib entries unused")
        n = out["numbers"]
        print(f"  numbers: {n['used']} used, {n['supplied']} supplied by the case, "
              f"{n['unsupplied_count']} not supplied: {n['unsupplied'][:8]}")
        print("  [TODO] left:", out["todos"])
        if "check_draft" in out:
            print("  check_draft:", out["check_draft"], " check_figures:", out["check_figures"])
        if "overlap" in out:
            print("  overlap with original:", out["overlap"]["shared_8grams"], "shared 8-grams,",
                  "longest shared run", out["overlap"]["longest_shared_run"], "words")
            if out["overlap"]["examples"]:
                print("    e.g.", out["overlap"]["examples"][:3])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
