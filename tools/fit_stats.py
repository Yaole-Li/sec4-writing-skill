#!/usr/bin/env python3
"""Fit corpus statistics on the fit split and write data/corpus_stats.json.

Pooled over the three covered venues, and again per venue, because the venues differ: S&P abstracts
run ~275 words, USENIX ~212.

Usage: python3 tools/fit_stats.py
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills/security-conf-writing/scripts"))
import style_metrics as sm  # noqa: E402

PCT = [10, 25, 50, 75, 90]
CANON_SECS = ["related work", "threat model", "method", "experiments", "discussion", "conclusion",
              "ethics", "open science"]


def pct(values, p):
    v = sorted(values)
    if not v:
        return 0.0
    k = (len(v) - 1) * p / 100
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return round(v[lo] + (v[hi] - v[lo]) * (k - lo), 3)


def dist(values):
    d = {f"p{p}": pct(values, p) for p in PCT}
    d["n"] = len(values)
    return d


def title_pattern(t):
    if ":" in t:
        return "name-colon-desc"
    if t.strip().endswith("?"):
        return "question"
    if re.match(r"^(sok|sok:)", t, re.I):
        return "sok"
    return "descriptive"


def fit(recs, label, out_style, out_struct):
    style = {"abstract": defaultdict(list), "intro": defaultdict(list)}
    for c in CANON_SECS:
        style[c] = defaultdict(list)
    struct = defaultdict(list)
    for r in recs:
        secs = sm.corpus_sections(r)
        for name in ("abstract", "intro"):
            txt = secs[name]
            # degenerate extractions (missing abstract, an intro that swallowed a page break) would
            # poison the percentiles, so they are dropped from that section's distribution only
            floor = 80 if name == "abstract" else 300
            if len(txt.split()) < floor:
                continue
            m, _ = sm.metric(txt)
            for k, v in m.items():
                style[name][k].append(v)
        for c in CANON_SECS:
            txt = "\n\n".join(s.get("text", "") for s in r["sections"] if s.get("canon") == c)
            if len(txt.split()) > 80:
                mc, _ = sm.metric(txt)
                for k, v in mc.items():
                    style[c][k].append(v)
        caps = [f["caption"] for f in r["figures"] if f.get("caption")]
        struct["caption_words"].extend(len(c.split()) for c in caps)
        if caps:
            struct["fig1_caption_words"].append(len(caps[0].split()))
        struct["tab_caption_words"].extend(len(t["caption"].split()) for t in r["tables"] if t.get("caption"))
        struct["pages"].append(r["pages"])
        struct["figures"].append(r["n_figures"])
        struct["tables"].append(r["n_tables"])
        struct["abstract_words"].append(r["abstract_words"])
        struct["sections"].append(len(r["sections"]))
        struct["title_words"].append(len(r["title"].split()))
        struct["floats_per_page"].append(round((r["n_figures"] + r["n_tables"]) / max(1, r["pages"]), 2))
        for k, v in r["has"].items():
            struct["has_" + k].append(1 if v else 0)
    out_style[label] = {sec: {k: dist(v) for k, v in metrics.items() if v}
                        for sec, metrics in style.items()}
    s = {}
    for k in ("pages", "figures", "tables", "abstract_words", "sections", "title_words",
              "caption_words", "fig1_caption_words", "tab_caption_words", "floats_per_page"):
        if struct[k]:
            s[k] = dist(struct[k])
    for k in [x for x in struct if x.startswith("has_")]:
        s[k] = {"count": int(sum(struct[k])), "n": len(struct[k])}
    out_struct[label] = s
    return style


def main():
    recs = sm.load_corpus(str(ROOT / "data/corpus.jsonl"), str(ROOT / "data/split.json"), "fit")
    byv = defaultdict(list)
    for r in recs:
        byv[r["venue"]].append(r)

    style_pool, struct_pool = {}, {}
    fit(recs, "pooled", style_pool, struct_pool)
    style_venue, struct_venue = {}, {}
    for v, rs in sorted(byv.items()):
        fit(rs, v, style_venue, struct_venue)

    out = {
        "source": f"{len(recs)} security-conference papers (S&P, USENIX Security, NDSS) used for fitting; "
                  f"{len(json.loads((ROOT / 'data/split.json').read_text())['heldout'])} held out. "
                  f"Corpus contains no CCS papers.",
        "metric_definitions": "skills/security-conf-writing/scripts/style_metrics.py",
        "style": style_pool["pooled"],
        "style_by_venue": {v: style_venue[v] for v in style_venue},
        "structure": struct_pool["pooled"],
        "structure_by_venue": {v: struct_venue[v] for v in struct_venue},
        "counts": {v: len(rs) for v, rs in byv.items()},
    }
    (ROOT / "data/corpus_stats.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                 encoding="utf-8")
    print("wrote data/corpus_stats.json")
    for v in ["pooled"] + sorted(style_venue):
        a = out["style_by_venue"][v]["abstract"] if v != "pooled" else out["style"]["abstract"]
        i = out["style_by_venue"][v]["intro"] if v != "pooled" else out["style"]["intro"]
        st = out["structure_by_venue"][v] if v != "pooled" else out["structure"]
        print(f"{v:8s} n={a['words']['n']:3d} abs words p50={a['words']['p50']:6.1f} sent={a['sentences']['p50']:5.1f} "
              f"num={a['numbers']['p50']:4.1f} | intro words p50={i['words']['p50']:6.1f} sent={i['sentences']['p50']:5.1f} "
              f"num={i['numbers']['p50']:5.1f} | pages={st['pages']['p50']:4.1f} figs={st['figures']['p50']:4.1f}")


if __name__ == "__main__":
    main()
