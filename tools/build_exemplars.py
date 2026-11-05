#!/usr/bin/env python3
"""Build the shipped exemplar bank from the merged annotations.

  data/annot/annotations.jsonl  ->  skills/tifs-paper-writing/references/exemplars/
      moves.jsonl       sentence-level: {id, move, quote, section, why, year, paper_type, motivation}
      paragraphs.jsonl  paragraph-level: {id, function, text, paper_type, motivation}
      phrasebank.csv    function, pattern, example, id, year   (patterns tagged by shape, not abstracted)

Held-out papers never enter the bank: the annotation set is the fit split only, and this script
re-checks it.

Usage: python3 tools/build_exemplars.py
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANNOT = ROOT / "data" / "annot" / "annotations.jsonl"
OUT = ROOT / "skills" / "security-conf-writing" / "references" / "exemplars"
CORPUS = ROOT / "data" / "corpus.jsonl"

FUNC = {"L": "landscape", "C": "credit", "G": "gap", "A": "attacker", "I": "insight",
        "M": "method", "S": "security", "R": "results", "P": "positioning",
        "K": "contributions", "X": "stance", "E": "ethics", "O": "open science"}

# phrase frames are tagged by the shape of the sentence, not by an abstracted template:
# the example stays verbatim and the tag says what to imitate.
SHAPES = [
    ("contrast", r"\b(However|Although|While|Whereas|Despite|Nonetheless)\b"),
    ("colon-expansion", r":\s"),
    ("rather-than", r"\b(rather than|instead of|in contrast)\b"),
    ("assumption", r"\b(assume|assumes|assumption|presuppose)\b"),
    ("capability", r"\b(can|cannot|is able to|capable of)\b"),
    ("quantified-gap", r"\b(\d+(\.\d+)?\s*(%|percent))\b"),
    ("purpose", r"\b(in order to|to this end|motivated by)\b"),
    ("consequence", r",\s+(thereby|which|enabling|making)\b"),
    ("enumeration", r"\b(First|Second|Third|Finally)\b"),
    ("definition", r"\b(we define|is defined as|denote)\b"),
]


def main():
    split = json.loads((ROOT / "data/split.json").read_text(encoding="utf-8"))
    fit, held = set(split["fit"]), set(split["heldout"])
    recs = {json.loads(l)["id"]: json.loads(l) for l in CORPUS.open(encoding="utf-8")}
    rows = [json.loads(l) for l in ANNOT.open(encoding="utf-8") if l.strip()]
    rows = [r for r in rows if r["id"] in fit]
    OUT.mkdir(parents=True, exist_ok=True)

    moves = []
    for r in rows:
        for m in r.get("moves", []):
            q = m.get("quote", "").strip()
            if not q or m.get("verified") is False:
                continue
            moves.append({
                "id": r["id"], "venue": r.get("venue", ""), "move": m["move"], "quote": q,
                "section": "abstract" if m["move"].startswith("abstract") else "introduction",
                "why": m.get("why", ""), "year": recs[r["id"]]["year"],
                "paper_type": r["type"], "motivation": r["motivation"],
                "venue": recs[r["id"]]["venue"],
            })
    with (OUT / "moves.jsonl").open("w", encoding="utf-8") as fh:
        for m in moves:
            fh.write(json.dumps(m, ensure_ascii=False) + "\n")

    # Abstract bank: the abstract is a single paragraph, so it is the one block that extracts reliably.
    abstracts = []
    for r in rows:
        a = recs[r["id"]].get("abstract", "")
        if len(a.split()) >= 80:
            abstracts.append({"id": r["id"], "venue": recs[r["id"]]["venue"],
                              "year": recs[r["id"]]["year"], "type": r["type"],
                              "motivation": r["motivation"], "words": len(a.split()),
                              "text": a})
    with (OUT / "abstracts.jsonl").open("w", encoding="utf-8") as fh:
        for a in abstracts:
            fh.write(json.dumps(a, ensure_ascii=False) + "\n")

    seen, bank = set(), []
    for m in moves:
        q = m["quote"]
        for tag, pat in SHAPES:
            if re.search(pat, q):
                key = (m["move"], q)
                if key in seen:
                    continue
                seen.add(key)
                bank.append({"function": m["move"].split(".")[1] if "." in m["move"] else m["move"],
                             "pattern": tag, "example": q, "id": m["id"], "year": m["year"]})
                break
    with (OUT / "phrasebank.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["function", "pattern", "example", "id", "year"])
        w.writeheader()
        w.writerows(bank)

    skipped = sum(1 for r in rows for m in r.get("moves", []) if m.get("verified") is False)
    print(f"unverified moves excluded: {skipped}")
    print(f"papers annotated: {len(rows)}  moves: {len(moves)}  abstracts: {len(abstracts)}  phrases: {len(bank)}")
    print("move tags:", len(Counter(m['move'] for m in moves)))
    print("by venue:", dict(Counter(a['venue'] for a in abstracts)))
    print("phrase shapes:", dict(Counter(b['pattern'] for b in bank)))
    leaked = [r["id"] for r in rows if r["id"] in held]
    if leaked:
        print("ERROR held-out papers present:", leaked)


if __name__ == "__main__":
    main()
