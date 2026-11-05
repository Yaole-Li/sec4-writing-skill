#!/usr/bin/env python3
"""Repair truncated annotations.

Some annotated quotes stop in the middle of a sentence (the annotator hit a word limit). This script
finds the sentence the quote came from in the extracted paper text, extends the quote to the sentence
end, and rewrites the batch file in place. It never invents text: the repaired quote is a substring of
the source, and it is re-verified before writing.

Usage: python3 tools/repair_quotes.py            # dry run, prints what it would fix
       python3 tools/repair_quotes.py --write    # rewrite the batch files
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from merge_annot import norm  # noqa: E402


def raw_source(rec):
    intro = " ".join(s.get("text", "") for s in rec["sections"])
    return rec.get("abstract", "") + "\n" + intro


def find_sentence(raw, quote):
    words = norm(quote).split()
    if len(words) < 4:
        return None
    head = words[:6]
    pat = r"\b" + r"\W+".join(re.escape(w) for w in head) + r"\b"
    m = re.search(pat, norm(raw))  # normalised search for the anchor
    if not m:
        return None
    # map the anchor back onto the raw text by walking it
    anchor_words = words[:6]
    it = re.finditer(r"[^\s]+", raw)
    spans = [(x.start(), x.end(), re.sub(r"[^a-z0-9]", "", x.group(0).lower())) for x in it]
    idx = None
    for i in range(len(spans) - len(anchor_words) + 1):
        window = [spans[i + k][2] for k in range(len(anchor_words))]
        if window == [re.sub(r"[^a-z0-9]", "", w) for w in anchor_words]:
            idx = i
            break
    if idx is None:
        return None
    start = spans[idx][0]
    tail = raw[start:]
    end = re.search(r"[.!?](\s|$)", tail)
    if not end:
        return None
    cand = re.sub(r"\s+", " ", tail[: end.end()]).strip()
    BAD = ("manuscript received", "digital object", "1556-6013", "©", "received ", "revised ",
           "authorized licensed", "ieee transactions on information forensics")
    if any(b in cand.lower() for b in BAD):
        return None
    if len(cand.split()) > 60:
        return None
    if not norm(cand).startswith(norm(quote)[:60]):
        return None
    return cand


def main():
    write = "--write" in sys.argv
    only = None
    for a in sys.argv:
        if a.startswith("--only="):
            only = a.split("=", 1)[1]
    recs = {json.loads(l)["id"]: json.loads(l)
            for l in (ROOT / "data/corpus.jsonl").open(encoding="utf-8")}
    fixed = failed = 0
    for path in sorted((ROOT / "data/annot").glob("batch_*.jsonl")):
        if only and only not in path.name:
            continue
        rows = [json.loads(l) for l in path.open(encoding="utf-8") if l.strip()]
        changed = False
        for r in rows:
            src = raw_source(recs[r["id"]])
            nsrc = norm(src)
            for m in r.get("moves", []):
                if norm(m["quote"]) in nsrc:
                    continue
                cand = find_sentence(src, m["quote"])
                if cand and norm(cand) in nsrc:
                    print(f"{path.name} {r['id']}: {m['quote'][:60]}...")
                    print(f"    -> {cand[:110]}...")
                    if write:
                        m["quote"] = cand
                        changed = True
                    fixed += 1
                else:
                    failed += 1
        if write and changed:
            path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                            encoding="utf-8")
    print(f"\nrepairable: {fixed}  unrepairable: {failed}  (write={write})")


if __name__ == "__main__":
    main()
