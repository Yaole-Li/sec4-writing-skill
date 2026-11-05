#!/usr/bin/env python3
"""Build the paper table and the fit / held-out split, stratified by venue x year.

Writes data/papers.csv and data/split.json. Deterministic (sha1 of the id), so it can be reviewed.
"""
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path

OUT = Path("data")
HELDOUT = 27  # 10% of 268


def main():
    recs = [json.loads(l) for l in (OUT / "corpus.jsonl").open(encoding="utf-8")]
    strata = defaultdict(list)
    for r in recs:
        strata[(r["venue"], r["year"])].append(r)
    for k in strata:
        strata[k].sort(key=lambda r: hashlib.sha1(r["id"].encode()).hexdigest())

    total = len(recs)
    quota = {k: round(HELDOUT * len(v) / total) for k, v in strata.items()}
    while sum(quota.values()) < HELDOUT:
        k = max(strata, key=lambda k: len(strata[k]) - quota[k])
        if quota[k] < len(strata[k]):
            quota[k] += 1
        else:
            break
    while sum(quota.values()) > HELDOUT:
        k = max((k for k in quota if quota[k] > 0), key=lambda k: quota[k])
        quota[k] -= 1

    heldout = set()
    for k, q in quota.items():
        for r in strata[k][:q]:
            heldout.add(r["id"])

    rows = []
    for r in sorted(recs, key=lambda r: (r["venue"], r["year"], r["id"])):
        rows.append({
            "id": r["id"], "venue": r["venue"], "year": r["year"],
            "title": r["title"][:180], "pages": r["pages"],
            "figures": r["n_figures"], "tables": r["n_tables"],
            "abstract_words": r["abstract_words"],
            "abstract_ok": "yes" if r["abstract_words"] >= 80 else "no",
            "role": "held-out" if r["id"] in heldout else "fit",
        })
    with (OUT / "papers.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    (OUT / "split.json").write_text(json.dumps({
        "fit": [r["id"] for r in rows if r["role"] == "fit"],
        "heldout": [r["id"] for r in rows if r["role"] == "held-out"],
    }, indent=1), encoding="utf-8")
    import collections
    print("papers:", len(rows), "fit:", sum(1 for r in rows if r['role'] == 'fit'), "heldout:", len(heldout))
    print("held-out by venue:", dict(collections.Counter(
        r['venue'] for r in rows if r['role'] == 'held-out')))
    print("abstract unusable:", sum(1 for r in rows if r['abstract_ok'] == 'no'))


if __name__ == "__main__":
    main()
