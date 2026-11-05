#!/usr/bin/env python3
"""Blind pack generator: turn a case's runs (plus the published paper) into anonymised candidates.

  python3 bench/pack.py --case vpn-tunnel-leak --reference refs/vpn_original.txt

Writes
  packs/<case>/pack.md          what the judges read (A/B/C/D, no mapping)
  packs/<case>/candidates.json  structured text per candidate
  packs/<case>/key.json         the mapping, for score_judgments.py only

Anonymisation: the case's working name, any "we call it X" artefact name, author blocks and the title
are masked. Numbers are kept, because D4 judges claim calibration on them.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench"
EVALS = ROOT / "skills/security-conf-writing/evals"
WS = re.compile(r"\s+")


def strip_latex(t):
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\(cite[tp]?|ref|eqref|label)\*?(\[[^\]]*\])?\{[^}]*\}", " [c] ", t)
    t = re.sub(r"\\(section|subsection|paragraph)\*?\{([^}]*)\}", r"\n\n\2\n\n", t)
    t = re.sub(r"\\begin\{(abstract|center|itemize|enumerate|small|quote)\}", " ", t)
    t = re.sub(r"\\end\{(abstract|center|itemize|enumerate|small|quote)\}", " ", t)
    t = re.sub(r"\\item\s*", "\n- ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^{}]*)\}", r"\2", t)
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    return re.sub(r"\n{3,}", "\n\n", t.replace("~", " ")).strip()


def read_first(base, names):
    for n in names:
        p = base / n
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace")
    return ""


def working_name(case):
    p = EVALS / case / "prompt.md"
    t = p.read_text(encoding="utf-8")
    m = re.search(r"\*\*Working name\*\*:\s*(.+)", t)
    if not m:
        return []
    raw = m.group(1).strip()
    names = {raw}
    names |= {w for w in re.findall(r"[A-Z][A-Za-z0-9\-]{2,}", raw) if w not in
              {"Working", "Target", "CVPR", "TIFS", "USENIX", "NDSS", "CCS"}}
    return sorted({n for n in names if len(n) >= 3}, key=len, reverse=True)


def anonymise(text, masks):
    out = text
    for n in masks:
        out = re.sub(rf"\b{re.escape(n)}\b", "[SYSTEM]", out)
    out = re.sub(r"\bwe (?:call|name|term) (?:it|this) ([A-Z][A-Za-z0-9\-]+)", r"we call it [SYSTEM]", out)
    out = re.sub(r"\[SYSTEM\](?:\s*\[SYSTEM\])+", "[SYSTEM]", out)
    return WS.sub(" ", out).strip()


def extract(run_dir):
    paper = run_dir / "outputs" / "paper"
    main = read_first(paper, ["main.tex"])
    title = ""
    m = re.search(r"\\title\{((?:[^{}]|\{[^{}]*\})*)\}", main, re.S)
    if m:
        title = WS.sub(" ", strip_latex(m.group(1)))
    abstract = strip_latex(read_first(paper, ["sec/abstract.tex", "sec/0_abstract.tex"]))
    intro = strip_latex(read_first(paper, ["sec/introduction.tex", "sec/1_intro.tex",
                                           "sec/1_introduction.tex"]))
    method = strip_latex(read_first(paper, ["sec/design.tex", "sec/4_method.tex", "sec/method.tex"]))
    evaln = strip_latex(read_first(paper, ["sec/evaluation.tex", "sec/5_experiments.tex",
                                          "sec/experiments.tex"]))
    return {"title": title, "abstract": abstract, "intro": intro,
            "design_eval": (method + "\n\n" + evaln)[:4000]}


def label_order(items, salt):
    """Deterministic shuffle: same salt gives the same labels, so a run can be audited."""
    keyed = sorted(items, key=lambda kv: hashlib.sha256(f"{salt}:{kv[0]}".encode()).hexdigest())
    return {f"ABCDEFGH"[i]: kv for i, kv in enumerate(keyed)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--reference", help="text file with the published abstract and introduction")
    ap.add_argument("--salt", default="sec4-bench-v1")
    ap.add_argument("--allow-no-reference", action="store_true")
    ap.add_argument("--min-candidates", type=int, default=3)
    args = ap.parse_args()

    case_dir = EVALS / args.case
    runs = sorted(p for p in (BENCH / "runs" / args.case).glob("*")
                  if (p / "run.json").exists() and (p / "outputs" / "paper").exists())
    if not runs:
        sys.exit(f"no runs under bench/runs/{args.case}; scaffold them with bench/run_case.py")
    masks = working_name(args.case)

    items = []
    for r in runs:
        rec = extract(r)
        if not rec["abstract"] and not rec["intro"]:
            print(f"skip {r.name}: no abstract or introduction")
            continue
        items.append((r.name, {**rec, "kind": "config"}))
    if args.reference:
        ref = Path(args.reference).read_text(encoding="utf-8", errors="replace")
        items.append(("reference", {"title": "", "abstract": "", "intro": ref,
                                    "design_eval": "", "kind": "reference"}))
    elif not args.allow_no_reference:
        sys.exit("no --reference given: the published paper belongs in the pack as the ceiling; "
                 "pass --allow-no-reference to score relative to the runs only")

    if len(items) < args.min_candidates:
        sys.exit(f"{len(items)} candidates; need at least {args.min_candidates} "
                 f"(runs + reference). Scaffold more runs.")

    labelled = label_order(items, args.salt)
    out = BENCH / "packs" / args.case
    out.mkdir(parents=True, exist_ok=True)

    pack_md, cands, key = [], {}, {"case": args.case, "salt": args.salt,
                                   "reference_included": bool(args.reference), "map": {}}
    for label, (name, rec) in labelled.items():
        pack_md.append(f"## Candidate {label}\n")
        if rec["abstract"]:
            pack_md.append("**Abstract**\n\n" + anonymise(rec["abstract"], masks) + "\n")
        if rec["intro"]:
            pack_md.append("**Introduction**\n\n" + anonymise(rec["intro"], masks) + "\n")
        if rec["design_eval"]:
            pack_md.append("**Excerpt from the design and evaluation sections**\n\n"
                           + anonymise(rec["design_eval"], masks) + "\n")
        pack_md.append("")
        cands[label] = {"abstract": anonymise(rec["abstract"], masks),
                        "intro": anonymise(rec["intro"], masks),
                        "design_eval": anonymise(rec["design_eval"], masks)}
        key["map"][label] = name

    (out / "pack.md").write_text("\n".join(pack_md), encoding="utf-8")
    (out / "candidates.json").write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"pack: {out/'pack.md'}")
    print(f"candidates: {len(labelled)}  labels: {''.join(sorted(labelled))}")
    print(f"reference included: {bool(args.reference)}  salt: {args.salt}")
    print("key (do not give this to judges):", json.dumps(key["map"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
