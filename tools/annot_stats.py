#!/usr/bin/env python3
"""Structural statistics from the annotations, written into data/annotation_stats.json.

Everything here comes from the 120-paper annotation table; the style numbers come from
tools/fit_stats.py. Both end up quoted in references/corpus-profile.md.

Usage: python3 tools/annot_stats.py
"""
import json
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FUNC = ["L", "C", "G", "A", "I", "M", "S", "R", "P", "K", "X", "E", "O"]
ABS_FUNC = ["L", "G", "C", "A", "I", "M", "S", "R", "K", "X", "E"]


def main():
    recs_all = [json.loads(l) for l in (ROOT / "data/annot/annotations.jsonl").open(encoding="utf-8")]
    # sequence sanity: an introduction has 4-15 paragraphs, an abstract 4-25 sentences.
    # Records outside that range are kept for type/motivation/moves but dropped from sequence stats.
    def seq_ok(r):
        n = len([c for c in r.get("intro_seq", "") if c in FUNC])
        m = len([c for c in r.get("abstract_seq", "") if c in ABS_FUNC])
        return (4 <= n <= 15 or n == 0) and (4 <= m <= 25 or m == 0)
    recs = [r for r in recs_all if seq_ok(r)]
    corpus = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data/corpus.jsonl").open(encoding="utf-8")}
    n = len(recs)

    out = {"n_papers": n, "n_records_total": len(recs_all),
           "n_sequence_records_used": n}
    out["paper_type"] = Counter(r["type"] for r in recs).most_common()
    out["motivation"] = Counter(r["motivation"] for r in recs).most_common()
    out["threat_model_location"] = Counter(r["threat_model"] for r in recs).most_common()
    out["ethics_location"] = Counter(r.get("ethics") for r in recs).most_common()
    out["openscience_location"] = Counter(r.get("openscience") for r in recs).most_common()
    out["by_venue"] = {}
    for v in sorted({r.get("venue") for r in recs if r.get("venue")}):
        rs = [r for r in recs if r.get("venue") == v]
        out["by_venue"][v] = {
            "n": len(rs),
            "type": Counter(r["type"] for r in rs).most_common(),
            "motivation": Counter(r["motivation"] for r in rs).most_common(),
            "intro_function_presence": {c: sum(1 for r in rs if c in r.get("intro_seq", "")) for c in FUNC},
        }

    presence = Counter()
    first_pos = defaultdict(list)
    lengths = defaultdict(list)
    for r in recs:
        seq = [c for c in r.get("intro_seq", "") if c in FUNC]
        if not seq:
            continue
        lengths[r["type"]].append(len(seq))
        for c in set(seq):
            presence[c] += 1
        for c in FUNC:
            if c in seq:
                first_pos[c].append(seq.index(c) / max(1, len(seq) - 1))
    out["intro_function_presence"] = {c: presence[c] for c in FUNC}
    out["intro_function_first_position_median"] = {
        c: round(st.median(first_pos[c]), 2) for c in FUNC if first_pos[c]}
    out["intro_paragraphs"] = {
        "median": st.median([len([c for c in r["intro_seq"] if c in FUNC]) for r in recs]),
        "by_type": {k: st.median(v) for k, v in lengths.items() if v},
    }

    # abstract arcs: coarse to four slots
    COARSE = {"L": "L", "G": "G", "C": "M", "A": "A", "I": "I", "M": "M", "S": "S", "R": "R", "K": "X", "X": "X", "E": "E", "O": "O"}
    arcs, firsts, lasts = Counter(), Counter(), Counter()
    for r in recs:
        seq = [c for c in r.get("abstract_seq", "") if c in ABS_FUNC]
        if not seq:
            continue
        firsts[seq[0]] += 1
        lasts[seq[-1]] += 1
        coarse = []
        for c in seq:
            g = COARSE.get(c, c)
            if not coarse or coarse[-1] != g:
                coarse.append(g)
        arcs["→".join(coarse)] += 1
    out["abstract_first_sentence"] = firsts.most_common()
    out["abstract_last_sentence"] = lasts.most_common()
    out["abstract_arcs_top"] = arcs.most_common(10)

    # contributions list and section presence, from the extracted structure
    out["contrib_list_in_intro"] = sum(1 for r in recs if "K" in r.get("intro_seq", ""))
    out["has_problem_section"] = sum(1 for r in recs if any(
        s["canon"] == "problem setup" for s in corpus[r["id"]]["sections"]))
    out["has_related_work"] = sum(1 for r in recs if any(
        s["canon"] == "related work" for s in corpus[r["id"]]["sections"]))
    out["has_theory_section"] = sum(1 for r in recs if any(
        s["canon"] == "theory" for s in corpus[r["id"]]["sections"]))

    (ROOT / "data/annotation_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("n_papers", "paper_type", "motivation",
                                          "threat_model_location", "intro_function_presence",
                                          "intro_function_first_position_median", "intro_paragraphs",
                                          "abstract_first_sentence", "abstract_last_sentence",
                                          "abstract_arcs_top", "contrib_list_in_intro")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
