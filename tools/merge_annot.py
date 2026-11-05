#!/usr/bin/env python3
"""Merge annotation batches into one table and validate them against the corpus.

Batches are JSONL files under data/annot/batch_*.jsonl with one record per paper:
  {"id": "2024-10262062", "type": "T1", "motivation": "failure",
   "intro_seq": "LCGAMSRK", "abstract_seq": "LGMR",
   "threat_model": "own-section|subsection|intro-paragraph|absent",
   "moves": [{"quote": "...", "section": "introduction", "move": "intro.gap.evasion",
              "why": "..."}]}

Checks: id exists and is in the fit split, no duplicate id, codes come from the frozen taxonomy,
sequences contain only known letters, quotes appear in the source text (verbatim, after
normalisation), and no quote is longer than 60 words or copied from a held-out paper.

Usage: python3 tools/merge_annot.py [--strict]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANNOT = ROOT / "data/annot"
TAXO = json.loads((ANNOT / "taxonomy.json").read_text(encoding="utf-8")) if (ANNOT / "taxonomy.json").exists() else None


def norm(s):
    """Normalise for verbatim comparison: quotes, dashes, and dropped maths symbols (pdftotext loses ε, θ ...)."""
    s = s.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2014", "--").replace("\u2013", "-").replace("\u2212", "-")
    s = re.sub(r"\[\d+(?:\s*[,;–-]\s*\d+)*\]", "", s)   # annotators strip citation brackets
    s = re.sub(r"(?:\s*,\s*)+(?=[.,;:])", "", s)        # ... and the commas they leave behind
    s = re.sub(r"[^\x00-\x7f]", " ", s)
    s = re.sub(r"[^a-z0-9\s.,;:!?'\"()\[\]/%$+\-*=<>]", " ", s.lower())
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,;:!?])", r"\1", s)      # citation removal leaves "LLMs ."
    return s.strip()


def main():
    strict = "--strict" in sys.argv
    recs = {json.loads(l)["id"]: json.loads(l)
            for l in (ROOT / "data/corpus.jsonl").open(encoding="utf-8")}
    split = json.loads((ROOT / "data/split.json").read_text(encoding="utf-8"))
    fit, held = set(split["fit"]), set(split["heldout"])

    type_codes = {t["code"] for t in TAXO["paper_types"]} if TAXO else set()
    intro_codes = set(TAXO["intro_codes"]) if TAXO else set()
    tm_codes = set(TAXO.get("threat_model_locations", []))
    eth_codes = set(TAXO.get("ethics_locations", []))
    ops_codes = set(TAXO.get("openscience_locations", []))

    rows, problems, seen = [], [], set()
    for path in sorted(ANNOT.glob("batch_*.jsonl")):
        for ln, line in enumerate(path.open(encoding="utf-8"), 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as ex:
                problems.append((path.name, ln, f"bad json: {ex}"))
                continue
            pid = r.get("id")
            tag = f"{path.name}:{ln} {pid}"
            if pid not in recs:
                problems.append((tag, "unknown id", ""))
                continue
            if pid in seen:
                problems.append((tag, "duplicate id", ""))
            seen.add(pid)
            if pid in held:
                problems.append((tag, "held-out paper annotated", ""))
            if type_codes and r.get("type") not in type_codes:
                problems.append((tag, "unknown type", r.get("type")))
            for field, codes in (("threat_model", tm_codes), ("ethics", eth_codes), ("openscience", ops_codes)):
                if codes and r.get(field) not in codes:
                    problems.append((tag, f"bad {field}", r.get(field)))
            if intro_codes:
                for k in ("intro_seq", "abstract_seq"):
                    bad = {c for c in str(r.get(k, "")) if c not in intro_codes and c != "-"}
                    if bad:
                        problems.append((tag, f"unknown letters in {k}", "".join(sorted(bad))))
            src = norm(recs[pid].get("abstract", "") + " " +
                       " ".join(s.get("text", "") for s in recs[pid]["sections"]))
            for mv in r.get("moves", []):
                q = mv.get("quote", "")
                mv["verified"] = norm(q) in src
                if len(q.split()) > 60:
                    problems.append((tag, "quote longer than 60 words", q[:60]))
                    mv["verified"] = False
                if not mv["verified"]:
                    problems.append((tag, "quote not found verbatim", q[:80]))
            rows.append(r)

    out = ANNOT / "annotations.jsonl"
    with out.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"merged {len(rows)} records -> {out}")
    print("types:", Counter(r.get("type") for r in rows).most_common())
    print("motivations:", Counter(r.get("motivation") for r in rows).most_common())
    print("threat_model:", Counter(r.get("threat_model") for r in rows).most_common())
    print("ethics:", Counter(r.get("ethics") for r in rows).most_common())
    print("openscience:", Counter(r.get("openscience") for r in rows).most_common())
    moves = [m for r in rows for m in r.get("moves", [])]
    ok = sum(1 for m in moves if m.get("verified"))
    print(f"moves: {len(moves)}  verbatim-verified: {ok} ({100*ok/max(1,len(moves)):.1f}%)")
    print("missing from fit set:", len(fit - seen), sorted(fit - seen)[:10])
    print(f"problems: {len(problems)}")
    for p in problems[:25]:
        print("  ", p)
    return 1 if (strict and problems) else 0


if __name__ == "__main__":
    sys.exit(main())
