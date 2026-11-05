#!/usr/bin/env python3
"""Deterministic stand-in judge. For self-testing the pipeline ONLY.

  python3 bench/judge_stub.py --case <case> --judge judge-1 [--out judgments/judge-1/<case>.json]

It does not read for meaning. It measures surface proxies of the kind D1-D9 ask about (threat words,
gap markers, numbers with a comparison, prior-work language, ethics language, sentence rhythm, design
vocabulary) and maps them onto 1-5. Three judges differ only by a deterministic tie-break, which
emulates judge variance without pretending to be one.

Every output carries "synthetic": true, and score_judgments.py refuses to publish a leaderboard without
stamping it.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench"
DIMS = [f"D{i}" for i in range(1, 10)]

THREAT = r"\b(attack|attacker|adversar|threat|jailbreak|exploit|leak|victim|defen[cs]e)\b"
GOAL = r"\b(goal|capabilit|knowledge|black-box|white-box|out of scope|assume)\b"
GAP = r"\b(however|despite|although|fail|struggle|limitation|assume[sd]?)\b"
NOVEL = r"\b(we (present|introduce|show|demonstrate|find)|new|first)\b"
EVID = r"\b(%|percent|compared|baseline|versus|vs\.?|outperform|drop|reduc)\b"
POSITION = r"\b(prior|existing|previous|closest|unlike|in contrast|state-of-the-art)\b"
ETHICS = r"\b(ethic|irb|approv|disclos|responsible|consent|dual-use|artefact|artifact|open science|release)\b"
DESIGN = r"\b(design|component|overview|pipeline|module|algorithm|objective|threat model|evaluation|setup|ablation)\b"
SENT = re.compile(r"(?<=[.!?])\s+")


def count(pat, text):
    return len(re.findall(pat, text, re.I))


def band(v, lo, mid, hi):
    if v >= hi:
        return 5
    if v >= mid:
        return 4
    if v >= lo:
        return 3
    if v >= max(1, lo - 1):
        return 2
    return 1


def score_candidate(text, tiebreak):
    n_sent = max(1, len([s for s in SENT.split(text) if s.strip()]))
    words = len(text.split())
    nums = len(re.findall(r"(?<![A-Za-z\d.])\d+(?:[.,]\d+)*", text))
    s = {}
    s["D1"] = band(count(THREAT, text), 2, 5, 9) if count(GOAL, text) else max(1, band(count(THREAT, text), 2, 5, 9) - 1)
    s["D2"] = band(count(GAP, text), 1, 3, 6)
    s["D3"] = band(count(NOVEL, text), 1, 3, 5)
    s["D4"] = band(nums + count(EVID, text), 3, 7, 12)
    s["D5"] = band(nums, 2, 5, 10)
    s["D6"] = band(count(POSITION, text), 1, 3, 6)
    s["D7"] = band(count(ETHICS, text), 1, 3, 5)
    mean_len = words / n_sent
    s["D8"] = 5 if 18 <= mean_len <= 27 else (3 if 14 <= mean_len <= 32 else 2)
    s["D9"] = band(count(DESIGN, text), 3, 6, 10)
    for d in DIMS:
        jitter = int(hashlib.sha256(f"{tiebreak}:{d}".encode()).hexdigest(), 16) % 3 - 1
        s[d] = max(1, min(5, s[d] + jitter))
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--judge", required=True)
    ap.add_argument("--packs", default=str(BENCH / "packs"))
    ap.add_argument("--out")
    args = ap.parse_args()

    cands = json.loads((Path(args.packs) / args.case / "candidates.json").read_text(encoding="utf-8"))
    scores, ranking = {}, []
    for label, rec in sorted(cands.items()):
        text = " ".join([rec.get("abstract", ""), rec.get("intro", ""), rec.get("design_eval", "")])
        sc = score_candidate(text, f"{args.judge}|{args.case}|{label}")
        sc["note"] = "synthetic proxy score; not a judgement"
        scores[label] = sc
        ranking.append((sum(sc[d] for d in DIMS) / len(DIMS), label))
    ranking = [lab for _, lab in sorted(ranking, key=lambda x: (-x[0], x[1]))]
    out = {"case": args.case, "judge": args.judge, "synthetic": True,
           "scores": scores, "ranking": ranking}
    dest = Path(args.out) if args.out else BENCH / "judgments" / args.judge / f"{args.case}.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{args.judge} {args.case}: wrote {dest}  ranking {ranking}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
