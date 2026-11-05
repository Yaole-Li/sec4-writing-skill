#!/usr/bin/env python3
"""Style metrics for IEEE TIFS drafts and for the corpus fit set.

The metric set is shared by three consumers, which is why it lives here:
  tools/fit_stats.py          computes corpus percentiles with it
  scripts/style_metrics.py    (shipped) prints a draft's metrics with the percentiles
  scripts/check_draft.py      (shipped) raises ERROR / WARN / NOTE against the percentiles

Differences from a vision-conference style checker, on purpose:
  * "In this paper, we propose ..." is the normal IEEE formula and is not an error.
  * Index Terms, threat model, security analysis and complexity are part of the genre.
  * Passive voice and long sentences are common in TIFS; the checks use ranges, not taste.
"""
import json
import re
from pathlib import Path

PUNCT = r"[.,;:!?]"

CONNECTORS = ["however", "therefore", "thus", "hence", "consequently", "moreover",
              "furthermore", "additionally", "in addition", "yet", "nevertheless",
              "nonetheless", "whereas", "while", "in contrast", "instead", "rather",
              "unlike", "accordingly", "as a result", "to this end", "on the other hand",
              "specifically", "in particular", "as such", "importantly", "finally",
              "in summary", "overall", "meanwhile", "besides"]

HEDGES = ["may", "might", "could", "likely", "possibly", "suggest", "suggests",
          "appear to", "appears to", "seem to", "seems to", "potentially", "presumably",
          "to some extent", "arguably"]

BOOSTERS = ["significantly", "substantially", "dramatically", "remarkably", "notably",
            "surprisingly", "strikingly", "drastically", "considerably", "greatly",
            "extremely", "highly"]

PRAISE = ["novel", "effective", "efficient", "powerful", "superior",
          "state-of-the-art", "sota", "outperform", "outperforms", "outperforming",
          "first", "best", "robust", "lightweight", "practical"]

# IEEE / TIFS formulaic openings and claims (counted, then judged by the corpus range,
# not hard-coded as errors: most TIFS papers use them).
FORMULAS = ["in this paper, we propose", "in this paper, we present", "in this work, we",
            "in this article, we", "this paper proposes", "we propose a", "we propose an",
            "experiments show that", "experimental results show", "extensive experiments",
            "to the best of our knowledge", "the main contributions", "contributions of this"]

INSIGHT_FORMULAS = ["key insight", "core insight", "central insight", "key idea",
                    "key observation", "main insight", "our insight", "the insight is"]

THREAT_WORDS = ["threat model", "adversar", "attacker", "assume that the attacker",
                "capabilit", "background knowledge", "security goal", "privacy goal"]

SECURITY_EVAL = ["attack success rate", "asr", "detection rate", "false positive rate",
                 "fpr", "tpr", "auc", "adaptive attack", "transferab", "robustness"]

PARTICIPLE_TAIL = re.compile(r",\s+(?:thereby\s+|which\s+)?\w+ing\b[^.]*\.$")
ANTITHESIS = re.compile(r"\b(?:is|are|does|do|was|were|can|cannot)\s+not\b|\bnot\s+yet\b"
                        r"|\brather than\b|\binstead of\b|\bneed not\b|\bisn't\b|\baren't\b")
LATEFIG = re.compile(r"\b(?:Figure|Fig\.|Table|Tab\.)\s*(?:[2-9]|\d{2,})\b")
NUMBER = re.compile(r"(?<![A-Za-z\d.])\d+(?:[.,]\d+)*(?![A-Za-z\d])")
PERCENT = re.compile(r"\d+(?:\.\d+)?\s*%")
WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(\[])", text)
    return [p.strip() for p in parts if len(p.strip()) > 2]


def words(text):
    return WORD.findall(text)


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _count_phrases(low, phrases):
    n = 0
    for p in phrases:
        if " " in p:
            n += low.count(p)
        else:
            n += len(re.findall(rf"\b{re.escape(p)}", low))   # prefix match: 'adversar' hits 'adversaries' 
    return n


CITATION = re.compile(r"\[\d+(?:\s*[,;–-]\s*\d+)*\]|\(\d{1,3}\)")


def clean_for_metrics(text):
    """Drop citation markers so that [12] is not counted as a number."""
    text = CITATION.sub(" ", text)
    text = re.sub(r"https?://\S+|doi:\s*\S+|10\.\d{4,}/\S+", " ", text, flags=re.I)
    return text


def metric(text):
    """Return (metrics dict, sentences list). One definition for corpus and drafts."""
    text = clean_for_metrics(text)
    sents = sentences(text)
    w = words(text)
    n_w = len(w)
    low = " ".join(sents).lower()
    lens = [len(s.split()) for s in sents] or [0]
    short = sum(1 for x in lens if x <= 12)
    run = best = 0
    for x in lens:
        run = run + 1 if x < 15 else 0
        best = max(best, run)
    colon_or_dash = sum(1 for s in sents if re.search(r"[:;]|—|–", s))
    starts = sum(1 for s in sents if re.match(r"^(However|Therefore|Thus|Hence|Moreover|"
                                             r"Furthermore|Additionally|Yet|Nevertheless|"
                                             r"Nonetheless|Meanwhile|Besides|Overall|Finally)\b", s))
    m = {
        "words": n_w,
        "sentences": len(sents),
        "prose_paragraphs": max(1, len(paragraphs(text))),
        "sent_len_mean": round(sum(lens) / len(lens), 2),
        "short_sent_ratio": round(short / max(1, len(sents)), 3),
        "short_run_max": best,
        "numbers": len(NUMBER.findall(text)),
        "percent_claims": len(PERCENT.findall(text)),
        "connector_per_100w": round(100 * _count_phrases(low, CONNECTORS) / max(1, n_w), 3),
        "connector_sentence_start_ratio": round(starts / max(1, len(sents)), 3),
        "colon_or_dash_sentences": round(colon_or_dash / max(1, len(sents)), 3),
        "hedge_count": _count_phrases(low, HEDGES),
        "booster_count": _count_phrases(low, BOOSTERS),
        "self_praise_count": _count_phrases(low, PRAISE),
        "formula_count": _count_phrases(low, FORMULAS),
        "insight_formula_count": _count_phrases(low, INSIGHT_FORMULAS),
        "threat_words": _count_phrases(low, THREAT_WORDS),
        "security_eval_terms": _count_phrases(low, SECURITY_EVAL),
        "we_sentence_ratio": round(sum(1 for s in sents if re.match(r"^(We|Our|we|our)\b", s))
                                   / max(1, len(sents)), 3),
        "question_sentences": sum(1 for s in sents if s.rstrip().endswith("?")),
        "participle_tail_ratio": round(sum(1 for s in sents if PARTICIPLE_TAIL.search(s))
                                       / max(1, len(sents)), 3),
        "antithesis_ratio": round(sum(1 for s in sents if ANTITHESIS.search(s))
                                  / max(1, len(sents)), 3),
        "late_figure_refs": len(LATEFIG.findall(text)),
        "passive_ratio": round(len(re.findall(r"\b(?:is|are|was|were|be|been|being)\s+"
                                              r"(?:\w+ly\s+)?\w+(?:ed|en)\b", text))
                               / max(1, len(sents)), 3),
    }
    return m, sents


# ---------------------------------------------------------------- corpus side
def corpus_sections(rec):
    """Abstract and introduction text of one extracted paper record."""
    out = {"abstract": rec.get("abstract", "")}
    intro = ""
    for s in rec.get("sections", []):
        if s.get("canon") == "introduction":
            intro = s.get("text", "")
            break
    out["intro"] = intro
    return out


def load_corpus(corpus_path="data/corpus.jsonl", split_path="data/split.json", role="fit"):
    split = json.loads(Path(split_path).read_text(encoding="utf-8"))
    keep = set(split[role])
    recs = [json.loads(l) for l in Path(corpus_path).open(encoding="utf-8")]
    return [r for r in recs if r["id"] in keep]


# ---------------------------------------------------------------- draft side
def expand_inputs(path, depth=0):
    """Inline \\input / \\include so a multi-file LaTeX project is measured as one draft."""
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


def sections_from_file(path):
    """Return {abstract, intro, keywords, related, method, experiments, conclusion} text."""
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    tex = path.endswith(".tex")
    if tex:
        raw = expand_inputs(path)
    out = {}
    if tex:
        m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", raw, re.S)
        out["abstract"] = strip_latex(m.group(1)) if m else ""
        m = re.search(r"\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}", raw, re.S)
        out["keywords"] = strip_latex(m.group(1)) if m else ""
        for name, pat in (("intro", r"Introduction"), ("related", r"Related Work|Background"),
                          ("method", r"Proposed Method|Method|Approach"),
                          ("experiments", r"Experiments|Evaluation"),
                          ("conclusion", r"Conclusion")):
            m = re.search(r"\\section\*?\{\s*(?:" + pat + r")\s*\}(.*?)(?=\\section\*?\{|\\appendix|\\end\{document\}|\Z)",
                          raw, re.S)
            out[name] = strip_latex(m.group(1)) if m else ""
    else:
        m = re.search(r"^#+\s*Abstract\s*$(.*?)(?=^#+\s|\Z)", raw, re.S | re.M)
        out["abstract"] = m.group(1) if m else ""
        out["keywords"] = ""
        for name, pat in (("intro", "Introduction"), ("related", "Related Work|Background"),
                          ("threat", "Threat Model|Problem Formulation"),
                          ("method", "Design|Method|Approach|System Design"),
                          ("experiments", "Evaluation|Experiments"),
                          ("ethics", "Ethics|Ethical"),
                          ("openscience", "Open Science|Artifact"),
                          ("discussion", "Discussion|Limitations"),
                          ("conclusion", "Conclusion")):
            m = re.search(r"^#+\s*(?:\d+\.?\s*)?(?:" + pat + r")\s*$(.*?)(?=^#+\s|\Z)", raw, re.S | re.M)
            out[name] = m.group(1) if m else ""
    return out


def strip_latex(t):
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\(cite[tp]?|ref|eqref|label)\*?(\[[^\]]*\])?\{[^}]*\}", " [c] ", t)
    t = re.sub(r"\\(section|subsection|paragraph)\*?\{([^}]*)\}", r"\n\n\2\n\n", t)
    t = re.sub(r"\\item\s*", "\n- ", t)
    t = t.replace("\\times", "×").replace("~", " ")
    t = t.replace("---", "—").replace("--", "–")
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^{}]*)\}", r"\2", t)
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    return t.replace("$", "").replace("{", "").replace("}", "")


# ---------------------------------------------------------------- CLI
SHOW = ["words", "sentences", "sent_len_mean", "short_sent_ratio", "short_run_max", "numbers",
        "percent_claims", "connector_per_100w", "hedge_count", "booster_count",
        "self_praise_count", "formula_count", "we_sentence_ratio", "passive_ratio",
        "participle_tail_ratio", "antithesis_ratio", "threat_words"]


def _stats_paths():
    here = Path(__file__).resolve().parent
    return [here.parent / "references/corpus/corpus_stats.json",
            here.parent.parent.parent / "data/corpus_stats.json"]


def load_stats():
    for p in _stats_paths():
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return None


def _pct(value, d):
    """Which band of the corpus distribution a value falls into."""
    if not d:
        return ""
    if value < d.get("p10", 0):
        return "below p10"
    if value > d.get("p90", 0):
        return "above p90"
    return "in range"


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Print style metrics with their corpus percentiles.")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sections", default="abstract,intro")
    args = ap.parse_args(argv)

    stats = load_stats() or {}
    out = []
    for path in args.files:
        secs = sections_from_file(path)
        row = {"file": path, "sections": {}}
        for name in [s.strip() for s in args.sections.split(",")]:
            text = secs.get(name, "")
            if not text.strip():
                continue
            m, _ = metric(text)
            row["sections"][name] = m
        out.append(row)

    if args.json:
        print(json.dumps({"corpus": bool(stats), "results": out}, ensure_ascii=False, indent=1))
        return 0

    for row in out:
        print(f"== {row['file']}")
        for name, m in row["sections"].items():
            d = (stats.get("style") or {}).get(name, {})
            print(f"  {name}")
            for k in SHOW:
                if k not in m:
                    continue
                if d and k in d:
                    band = _pct(m[k], d[k])
                    ref = f"p10 {d[k].get('p10')} | p50 {d[k].get('p50')} | p90 {d[k].get('p90')}"
                    print(f"    {k:24s} {m[k]:>8}   {ref:42s} {band}")
                else:
                    print(f"    {k:24s} {m[k]:>8}")
        if not stats:
            print("  (corpus_stats.json not found: percentiles unavailable)")
    return 0


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main(_sys.argv[1:]))
