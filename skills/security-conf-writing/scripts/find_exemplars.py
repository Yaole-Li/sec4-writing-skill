#!/usr/bin/env python3
"""Retrieve TIFS exemplars by rhetorical function.

  python3 scripts/find_exemplars.py --para gap --type T1        # paragraphs with this function
  python3 scripts/find_exemplars.py intro.gap.assumption        # every move with this prefix
  python3 scripts/find_exemplars.py --phrases transition -n 5   # sentence frames
  python3 scripts/find_exemplars.py --list                      # what is in the bank

The bank is generated from the annotated corpus (`data/annot/annotations.jsonl` in the repository);
held-out papers are excluded. Read exemplars for order and calibration, never for copying: the checker
flags any six-word run shared with the bank.
"""
import argparse
import csv
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BANK = ROOT / "references/exemplars"


def load_jsonl(name):
    p = BANK / name
    if not p.exists():
        return []
    out = []
    for line in p.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def show(rows, n, kind):
    if not rows:
        print("no exemplar found; try --list to see what the bank holds")
        return 1
    pick = rows if len(rows) <= n else random.sample(rows, n)
    for r in pick:
        head = f"[{r.get('id','')}] {r.get('venue','')} {r.get('year','')}".strip()
        if kind == "move":
            print(f"\n--- {r['move']}  {head}")
            print(f"    {r['quote']}")
        elif kind == "para":
            print(f"\n--- {r['function']}  {head}  type={r.get('paper_type','')}")
            print(f"    {r['text'][:600]}")
        else:
            print(f"\n--- {r.get('function','')}  {r.get('pattern','')}")
            print(f"    {r.get('example','')}")
        why = r.get("why") or r.get("why_good")
        if why:
            print(f"    why: {why}")
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("move", nargs="?", help="move prefix, e.g. intro.gap")
    ap.add_argument("--para", help="paragraph function, e.g. gap, attacker, results")
    ap.add_argument("--phrases", help="phrasebank function, e.g. transition, gap")
    ap.add_argument("--type", help="paper type filter, T1..T6")
    ap.add_argument("--motivation", help="motivation filter")
    ap.add_argument("--venue", help="venue filter: SP, USENIX, NDSS")
    ap.add_argument("--abstracts", metavar="VENUE", help="print whole real abstracts of this venue")
    ap.add_argument("-n", type=int, default=3)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)

    moves = load_jsonl("moves.jsonl")
    abstracts = load_jsonl("abstracts.jsonl")
    paras = load_jsonl("paragraphs.jsonl")
    phrases = list(csv.DictReader((BANK / "phrasebank.csv").open(encoding="utf-8"))) \
        if (BANK / "phrasebank.csv").exists() else []

    if args.list:
        abstracts = load_jsonl("abstracts.jsonl")
        print(f"moves: {len(moves)}  abstracts: {len(abstracts)}  phrases: {len(phrases)}")
        ven = {}
        for m in moves:
            ven[m.get("venue", "?")] = ven.get(m.get("venue", "?"), 0) + 1
        print("  moves by venue:", ven)
        seen = {}
        for m in moves:
            seen[m["move"]] = seen.get(m["move"], 0) + 1
        for k in sorted(seen):
            print(f"  {k:34s} {seen[k]}")
        print("\nparagraph functions:", sorted({p["function"] for p in paras}))
        print("phrase functions:", sorted({p["function"] for p in phrases}))
        return 0

    if args.abstracts:
        rows = [a for a in abstracts if a.get("venue") == args.abstracts.upper()]
        if args.type:
            rows = [a for a in rows if a.get("type") == args.type]
        if not rows:
            print("no abstract found for that venue")
            return 1
        for a in (rows if len(rows) <= args.n else random.sample(rows, args.n)):
            print(f"\n--- {a['venue']} {a['year']}  type={a['type']}  {a['words']} words  [{a['id']}]")
            print("   " + a["text"][:1400])
        return 0
    if args.phrases:
        rows = [p for p in phrases if p.get("function") == args.phrases]
        return show(rows, args.n, "phrase")
    if args.para:
        rows = [p for p in paras if p.get("function") == args.para]
        if args.venue:
            rows = [p for p in rows if p.get("venue") == args.venue]
        if args.type:
            rows = [p for p in rows if p.get("paper_type") == args.type]
        return show(rows, args.n, "para")
    if args.move:
        rows = [m for m in moves if m.get("move", "").startswith(args.move)]
        if args.type:
            rows = [m for m in rows if m.get("paper_type") == args.type]
        if args.motivation:
            rows = [m for m in rows if m.get("motivation") == args.motivation]
        if args.venue:
            rows = [m for m in rows if m.get("venue") == args.venue]
        return show(rows, args.n, "move")
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
