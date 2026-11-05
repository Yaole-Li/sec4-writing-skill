#!/usr/bin/env python3
"""Checks for the figures and tables of a TIFS draft (LaTeX).

Ranges come from data/corpus_stats.json of the 120-paper fit set; if that file is not present the
script falls back to the same numbers written inline, so the skill folder stays self-contained.

Levels: ERROR (must fix), WARN (outside the range of 90% of this corpus or a known habit), NOTE.

Usage: python3 scripts/check_figures.py main.tex
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATS_CANDIDATES = [HERE.parent.parent.parent / "data/corpus_stats.json",
                    HERE.parent / "references/corpus/corpus_stats.json"]

FALLBACK = {"caption_words": (6, 94), "fig1_caption_words": (6, 94),
            "figures": (4, 16), "tables": (2, 16), "floats_per_page": (0.52, 1.39)}

# TIFS captions open with a noun phrase naming the thing (79% of 1239 captions in the corpus);
# a clause opener ("We show that ...") appears in 1%.
CLAUSE_OPEN = re.compile(r"^\s*(we|our|this paper|here|in this)\b", re.I)
NOUN_OPEN = re.compile(r"^\s*(the|a|an|overview|illustration|architecture|framework|structure|"
                       r"pipeline|workflow|diagram|schematic|comparison|performance|result|effect|"
                       r"impact|visuali[sz]ation|example|accuracy|detection|robustness|sensitivity|"
                       r"ablation|analysis|threat|two|three|four)\b", re.I)
RASTER = re.compile(r"\.(png|jpg|jpeg|bmp|gif|tif|tiff)\b", re.I)
ABS_WIDTH = re.compile(r"\\includegraphics\s*\[[^\]]*width\s*=\s*[0-9.]+\s*(cm|mm|in|pt)\b")
VERB = re.compile(r"\b(is|are|was|were|shows?|illustrates?|compares?|demonstrates?|depicts?|"
                  r"reports?|presents?|gives|summari[sz]es)\b", re.I)


def load_ranges():
    for p in STATS_CANDIDATES:
        if p.exists():
            try:
                st = json.loads(p.read_text(encoding="utf-8"))["structure"]

                def rng(key, fb):
                    d = st.get(key, {})
                    return (d.get("p10", fb[0]), d.get("p90", fb[1])) if d else fb

                return {k: rng(k, v) for k, v in FALLBACK.items()}
            except Exception:  # noqa: BLE001
                break
    return dict(FALLBACK)


def strip_comments(t):
    return re.sub(r"(?<!\\)%.*", "", t)


def blocks(tex, env):
    e = re.escape(env)
    return re.findall(rf"\\begin\{{{e}\}}(.*?)\\end\{{{e}\}}", tex, re.S)


def caption_of(block):
    m = re.search(r"\\caption(?:\[[^\]]*\])?\{(.*?)\}\s*(?:\\label|\\end|$)", block, re.S)
    if not m:
        return None
    cap = m.group(1)
    depth, out = 1, ""
    for ch in cap:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                break
        out += ch
    return re.sub(r"\s+", " ", out).strip()


def expand_inputs(path, depth=0):
    """Inline \\input and \\include so that figures living in sec/ or fig/ are checked."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if depth > 4:
        return text

    def rep(m):
        name = m.group(1).strip()
        if not name.endswith(".tex"):
            name += ".tex"
        for cand in (path.parent / name, path.parent / "sec" / name, path.parent / "fig" / name):
            if cand.exists():
                return expand_inputs(cand, depth + 1)
        return m.group(0)

    return re.sub(r"\\(?:input|include)\{([^}]+)\}", rep, text)


def main(path):
    raw = expand_inputs(path)
    tex = strip_comments(raw)
    R = load_ranges()
    issues = []

    figs = blocks(tex, "figure") + blocks(tex, "figure*")
    tabs = blocks(tex, "table") + blocks(tex, "table*")
    labels = set(re.findall(r"\\label\{([^}]+)\}", tex))
    refs = set(re.findall(r"\\(?:ref|cref|Cref|autoref)\{([^}]+)\}", tex))
    pages = None
    m = re.search(r"\\documentclass\[([^\]]*)\]\{IEEEtran\}", tex) or re.search(r"\\documentclass\{IEEEtran\}", tex)
    has_journal = bool(m)

    for i, b in enumerate(figs, 1):
        cap = caption_of(b)
        lab = re.search(r"\\label\{([^}]+)\}", b)
        if cap is None:
            issues.append(("ERROR", f"figure {i}: no \\caption", ""))
            continue
        if not lab:
            issues.append(("WARN", f"figure {i}: no \\label, cannot be referenced", ""))
        elif lab.group(1) not in refs:
            issues.append(("WARN", f"figure {i}: label '{lab.group(1)}' is never referenced", ""))
        words = len(cap.split())
        lo, hi = R["fig1_caption_words"] if i == 1 else R["caption_words"]
        if words > hi:
            issues.append(("WARN", f"figure {i}: caption is {words} words (90% of this corpus' captions <= {hi})", cap[:70]))
        if words < 4:
            issues.append(("WARN", f"figure {i}: caption is a bare label ({words} words); add what the reader should take away", cap))
        if CLAUSE_OPEN.match(cap):
            issues.append(("WARN", f"figure {i}: caption opens with a clause; TIFS captions open with a noun phrase naming the figure", cap[:70]))
        elif not NOUN_OPEN.match(cap):
            head = re.split(r"[.:;]", cap)[0]
            if VERB.search(head):
                issues.append(("NOTE", f"figure {i}: caption opens with a clause rather than a noun phrase", cap[:70]))
        if not cap.rstrip().endswith((".", "?", "!")):
            issues.append(("WARN", f"figure {i}: caption does not end with a period", cap[-60:]))
        if words > 20 and not VERB.search(cap):
            issues.append(("NOTE", f"figure {i}: long caption with no finite verb; the second sentence should say what changes", cap[:70]))
        inc = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", b)
        for f in inc:
            if RASTER.search(f):
                issues.append(("WARN", f"figure {i}: raster image '{f}'; submit vector (PDF/EPS/TikZ) where possible", ""))
        if ABS_WIDTH.search(b):
            issues.append(("WARN", f"figure {i}: absolute width; use a fraction of \\columnwidth or \\textwidth", ""))
        if "\\TODO" in b or "\\figplan" in b:
            issues.append(("NOTE", f"figure {i}: still a placeholder", ""))

    for i, b in enumerate(tabs, 1):
        cap = caption_of(b)
        if cap is None:
            issues.append(("ERROR", f"table {i}: no \\caption", ""))
            continue
        lab = re.search(r"\\label\{([^}]+)\}", b)
        if not lab:
            issues.append(("WARN", f"table {i}: no \\label", ""))
        elif lab.group(1) not in refs:
            issues.append(("WARN", f"table {i}: label '{lab.group(1)}' is never referenced", ""))
        if re.search(r"\\begin\{tabular\}\{[^}]*\|", b):
            issues.append(("WARN", f"table {i}: vertical rules in tabular; IEEE tables use booktabs rules only", ""))
        if "\\hline" in b and "\\toprule" not in b:
            issues.append(("NOTE", f"table {i}: \\hline instead of booktabs (\\toprule/\\midrule/\\bottomrule)", ""))
        if cap and CLAUSE_OPEN.match(cap):
            issues.append(("WARN", f"table {i}: caption opens with a clause; name the table first", cap[:70]))

    lo = R["figures"][1]
    if len(figs) > lo:
        issues.append(("WARN", f"{len(figs)} figures (90% of this corpus have <= {lo}); move some to the supplement", ""))
    lo_t = R["tables"][1]
    if len(tabs) > lo_t:
        issues.append(("WARN", f"{len(tabs)} tables (90% of this corpus have <= {lo_t})", ""))
    if not figs:
        issues.append(("NOTE", "no figure found; a TIFS paper normally has 5 to 14", ""))
    intro = re.search(r"\\section\{Introduction\}(.*?)\\section\{", tex, re.S)
    if figs and intro and not re.search(r"\\(?:ref|cref)\{(fig:[^}]+)\}", intro.group(1)):
        issues.append(("NOTE", "Figure 1 is not referenced in the Introduction; papers in this corpus usually place the anchor figure there", ""))
    if not figs and not tabs:
        issues.append(("NOTE", "no float found; a security paper normally has 9 figures and 8 tables", ""))

    order = {"ERROR": 0, "WARN": 1, "NOTE": 2}
    issues.sort(key=lambda x: order[x[0]])
    for lvl, msg, ctx in issues:
        print(f"{lvl:5s} {msg}" + (f"\n      {ctx}" if ctx else ""))
    errs = sum(1 for i in issues if i[0] == "ERROR")
    print(f"\n{len(figs)} figures, {len(tabs)} tables, {len(issues)} issues "
          f"({errs} ERROR, {sum(1 for i in issues if i[0]=='WARN')} WARN, "
          f"{sum(1 for i in issues if i[0]=='NOTE')} NOTE)")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
