#!/usr/bin/env python3
"""Structural census of the fit set: one table per venue, plus the facts the rule documents quote.

Writes data/census.json and prints a markdown summary.
Usage: python3 tools/census.py
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def p50(values):
    v = sorted(values)
    return v[len(v) // 2] if v else 0


def main():
    recs = [json.loads(l) for l in (ROOT / "data/corpus.jsonl").open(encoding="utf-8")]
    split = json.loads((ROOT / "data/split.json").read_text(encoding="utf-8"))
    fit = [r for r in recs if r["id"] in set(split["fit"])]
    byv = defaultdict(list)
    for r in fit:
        byv[r["venue"]].append(r)

    out = {"n_fit": len(fit), "venues": {}}
    for v, rs in sorted(byv.items()):
        n = len(rs)
        f = lambda k: sum(1 for r in rs if r["has"].get(k))
        abs_ok = [r["abstract_words"] for r in rs if r["abstract_words"] >= 80]
        canon = Counter()
        for r in rs:
            canon.update({c for c in r["section_canons"] if c != "other"})
        titles = Counter("colon" if ":" in r["title"] else ("question" if r["title"].strip().endswith("?") else "plain")
                         for r in rs)
        sok = [r for r in rs if re.match(r"^(sok|sok:)", r["title"], re.I)]
        out["venues"][v] = {
            "n": n,
            "pages": {"p50": p50([r["pages"] for r in rs]), "min": min(r["pages"] for r in rs),
                      "max": max(r["pages"] for r in rs)},
            "abstract_words": {"p50": p50(abs_ok), "usable": len(abs_ok), "unusable": n - len(abs_ok)},
            "figures_p50": p50([r["n_figures"] for r in rs]),
            "tables_p50": p50([r["n_tables"] for r in rs]),
            "floats_per_page_p50": round(p50([round((r["n_figures"] + r["n_tables"]) / max(1, r["pages"]), 2)
                                              for r in rs]), 2),
            "section_presence": dict(canon.most_common()),
            "ethics_section": f("ethics_section"),
            "ethics_mention": f("ethics_mention"),
            "open_science": f("open_science"),
            "artifact_badge_in_text": f("artifact_badge"),
            "threat_model_section": f("threat_model_section"),
            "threat_model_any": f("threat_model"),
            "related_work_section": f("related_work"),
            "ablation_mention": f("ablation"),
            "limitations_mention": f("limitations"),
            "title_pattern": dict(titles),
            "sok": len(sok),
        }
    (ROOT / "data/census.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"fit papers: {len(fit)}\n")
    for v, d in out["venues"].items():
        print(f"## {v} (n={d['n']})")
        print(f"- pages {d['pages']['p50']} ({d['pages']['min']}–{d['pages']['max']}), "
              f"abstract {d['abstract_words']['p50']} words ({d['abstract_words']['unusable']} unusable)")
        print(f"- figures {d['figures_p50']}, tables {d['tables_p50']}, floats/page {d['floats_per_page_p50']}")
        print(f"- threat model: section {d['threat_model_section']}, any {d['threat_model_any']}/{d['n']}")
        print(f"- ethics: section {d['ethics_section']}, mention {d['ethics_mention']}/{d['n']}")
        print(f"- open science: {d['open_science']}/{d['n']}; artefact badge detected in text: {d['artifact_badge_in_text']}")
        print(f"- related work section {d['related_work_section']}/{d['n']}, ablation mention {d['ablation_mention']}, "
              f"limitations mention {d['limitations_mention']}")
        print(f"- titles {d['title_pattern']}, SoK {d['sok']}")
        print(f"- sections: {d['section_presence']}\n")


if __name__ == "__main__":
    main()
