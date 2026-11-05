#!/usr/bin/env python3
"""Mechanical checks for a security-conference draft (S&P, USENIX Security, NDSS, CCS).

Two kinds of check, kept apart:
  (a) venue rules     -- what the four venues require regardless of corpus statistics: no citations or
      equations in the abstract, a threat model for attack and defense papers, an ethics statement and an
      open-science statement where the venue requires them, no copied exemplar text;
  (b) corpus bands    -- every style number compared with the p10-p90 of the fit papers *of that venue*,
      read from references/corpus/corpus_stats.json. A draft outside the band of 90% of that venue's
      papers is a WARN: revise it or justify it in report.md.

Phrase severities are calibrated on the corpus, not on taste:
  ERROR  the phrase appears in at most 2 of 241 fit papers
  WARN   3-10 of 241
  NOTE   common in the venue; flagged only when the sentence stays vague

Usage:
  python3 scripts/check_draft.py main.tex --venue USENIX [--json] [--sections abstract,intro]
Exit code 1 if any ERROR is found.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import style_metrics as sm  # noqa: E402

STATS_PATHS = [ROOT / "references/corpus/corpus_stats.json",
               ROOT.parent.parent / "data/corpus_stats.json"]
BANK = ROOT / "references/exemplars/moves.jsonl"
PARAS = ROOT / "references/exemplars/paragraphs.jsonl"
VENUES = {"SP": "S&P", "USENIX": "USENIX", "NDSS": "NDSS", "CCS": "CCS"}

ERROR_PHRASES = {
    r"with the rapid (development|growth|advance)": "boilerplate opener (1 of 241 abstracts)",
    r"plays? an? (important|vital|key|crucial) role": "empty claim (0 of 241 abstracts)",
    r"has attracted (increasing|growing|much) attention": "boilerplate opener (1 of 241)",
    r"our (key|core|central) insight is": "state the observation directly; the formula is absent from the corpus",
    r"\[(intro|abstract|relwork|method|eval)\.[a-z\-.]+\]": "move tag left in the text",
    r"\b(supplied|provided)\b[^.]{0,40}\b(by the (user|author)|input)\b": "workflow trace left in the text",
}
WARN_PHRASES = {
    r"\bdelve": "rare in the corpus (3 of 241)",
    r"\bpivotal\b": "rare (2 of 241)",
    r"\bseamless(ly)?\b": "rare (5 of 241)",
    r"in recent years": "generic opener (4 of 241 abstracts)",
    r"paradigm shift": "rare (4 of 241 introductions)",
    r"simple yet effective": "cliché",
}
NOTE_PHRASES = {
    r"\bnovel\b": "common (72 of 241 abstracts); say what is new in the same sentence",
    r"\bstate[- ]of[- ]the[- ]art\b|\bSOTA\b": "common (52 of 241); name the baselines in the same sentence",
    r"\bthe first\b|\bfor the first time\b": "state the scope of the claim",
    r"\bextensive\b": "make it earn itself with a count",
    r"\bsignificantly\b": "attach a test result or a margin",
    r"\bwe believe\b": "rare in the corpus; state the fact",
    r"\bit is worth noting\b": "filler",
}

ABSTRACT_FORBIDDEN = [
    (r"\\cite[tp]?\b|\b[A-Z][a-z]+\s+et al\.|\[\d+\]", "citation in the abstract: conference abstracts cite nothing"),
    (r"\\begin\{equation\}|\\begin\{align\}|\$[^$]{2,}\$", "equation in the abstract: state the result in words"),
    (r"\b(Fig\.|Figure|Table|Tab\.)\s*[0-9IVX]+", "figure or table reference in the abstract"),
]

ETHICS_HINT = re.compile(r"\b(participants?|interview|survey|users?|human subjects?|irb|traffic|"
                         r"scanning|crawl|vulnerab|disclos|malware|personal)", re.I)
ATTACK_HINT = re.compile(r"\b(attack|adversar|threat model|attacker|defen[cs]e|jailbreak)\b", re.I)


def load_stats():
    for p in STATS_PATHS:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return None


def bands(stats, venue, section):
    if not stats:
        return {}
    by_venue = (stats.get("style_by_venue") or {}).get(venue, {})
    if section in by_venue:
        return by_venue[section]
    return (stats.get("style") or {}).get(section, {})


def get_sections(path):
    secs = dict(sm.sections_from_file(path))
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    if path.endswith(".tex"):
        raw = sm.expand_inputs(path)
    secs["raw"] = raw
    secs["body"] = sm.strip_latex(raw) if path.endswith(".tex") else raw
    for key in ("abstract", "intro", "keywords", "threat", "ethics", "openscience"):
        secs.setdefault(key, "")
    return secs


def ngrams(s, n=6):
    w = re.findall(r"[a-z0-9]+", s.lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


BOILER_SUBSTRINGS = ("as follows", "organized as", "summarized as", "structured as")
BOILERPLATE = [
    r"^(the )?(main |key |primary )?contributions? of (this|the) (paper|article|work) (are|is|can)",
    r"^in (this|the) (paper|article|work) we (propose|present|introduce|develop)",
    r"^(to )?(address|tackle|overcome|handle) (these|the|such) (challenges|issues|problems|limitations)",
    r"^to the best of our knowledge",
    r"^(experimental|extensive) (results|experiments|evaluations) (show|demonstrate|verify|validate)",
]


def is_boilerplate(g):
    return any(s in g for s in BOILER_SUBSTRINGS) or any(re.match(p, g) for p in BOILERPLATE)


def bank_ngrams():
    bank = set()
    for p in (BANK, PARAS):
        if p.exists():
            for line in p.open(encoding="utf-8"):
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                bank |= ngrams(d.get("quote") or d.get("text") or "")
    pb = ROOT / "references/exemplars/phrasebank.csv"
    if pb.exists():
        for r in csv.DictReader(pb.open(encoding="utf-8")):
            bank |= ngrams(r.get("example", ""))
    return {g for g in bank if not is_boilerplate(g)}


def band_checks(name, text, b, issues):
    m, _ = sm.metric(text)

    def over(key, msg, level="WARN"):
        if key not in b or "p10" not in b[key]:
            return
        p10, p90 = b[key]["p10"], b[key]["p90"]
        v = m[key]
        if v > p90:
            issues.append((level, f"{name}: {msg} ({v}; 90% of this venue's papers <= {p90})"))
        elif v < p10:
            issues.append((level, f"{name}: {msg} ({v}; 90% of this venue's papers >= {p10})"))

    over("words", "word count")
    over("sentences", "sentence count", "NOTE")
    over("sent_len_mean", "mean sentence length")
    over("short_sent_ratio", "share of short sentences (<=12 words)")
    over("short_run_max", "run of consecutive short sentences (<15 words each)")
    over("numbers", "numeric tokens", "NOTE")
    over("connector_per_100w", "logical connectors per 100 words")
    over("participle_tail_ratio", "share of sentences ending in a participial clause")
    over("antithesis_ratio", "share of aphoristic contrasts (X is not Y / rather than)")
    over("hedge_count", "hedges (may, could, suggest)")
    over("booster_count", "boosters (significantly, remarkably)")
    over("passive_ratio", "passive constructions per sentence", "NOTE")
    if name == "abstract":
        over("self_praise_count", "evaluative words (outperforms, first, effective)", "NOTE")
    if name == "intro" and "self_praise_count" in b:
        if m["self_praise_count"] < b["self_praise_count"]["p10"]:
            issues.append(("NOTE", "introduction: promotes the work less than 90% of this venue's papers"))
    return m


def phrase_checks(text, where, issues):
    low = re.sub(r"\s+", " ", sm.clean_for_metrics(text)).lower()
    for pat, msg in ERROR_PHRASES.items():
        hit = re.search(pat, low)
        if hit:
            issues.append(("ERROR", f"{where}: {msg} -- '{hit.group(0)}'"))
    for pat, msg in WARN_PHRASES.items():
        if re.search(pat, low):
            issues.append(("WARN", f"{where}: {msg}"))
    for pat, msg in NOTE_PHRASES.items():
        if re.search(pat, low):
            issues.append(("NOTE", f"{where}: {msg}"))


def venue_rules(venue, secs, issues, anonymous):
    raw = secs["raw"]
    body_low = re.sub(r"\s+", " ", secs["body"]).lower()
    has_ethics_heading = bool(re.search(r"\\(?:section|subsection)\*?\{\s*(?:Ethics|Ethical)", raw))
    has_open_heading = bool(re.search(r"\\(?:section|subsection)\*?\{\s*(?:Open Science|Artifact)", raw))
    if venue == "USENIX":
        if not has_ethics_heading:
            issues.append(("WARN", "USENIX requires an Ethics Considerations section; none found"))
        if not has_open_heading and "open science" not in body_low:
            issues.append(("WARN", "USENIX requires an Open Science statement; neither a section nor the phrase is present"))
    if venue == "CCS":
        if not re.search(r"\\ccsdesc", raw):
            issues.append(("WARN", "CCS submission without a \\ccsdesc block (CCS Concepts)"))
        if not re.search(r"\\keywords\{", raw):
            issues.append(("WARN", "CCS submission without \\keywords{}"))
    if ATTACK_HINT.search(body_low) and "threat model" not in body_low and not secs["threat"].strip():
        issues.append(("WARN", "no threat model anywhere: attack and defense papers are expected to state one"))
    if ETHICS_HINT.search(body_low) and "ethic" not in body_low and not secs["ethics"].strip():
        issues.append(("NOTE", "human, traffic, vulnerability or disclosure material present, but no ethics statement"))
    if re.search(r"\bvulnerab", body_low) and "disclos" not in body_low:
        issues.append(("NOTE", "vulnerabilities are found but no responsible-disclosure statement is present"))
    if anonymous:
        m = re.search(r"\\author\{([^}]*)\}", raw)
        if m and m.group(1).strip() and "anonymous" not in m.group(1).lower():
            issues.append(("WARN", f"--anonymous given, but \\author still holds '{m.group(1)[:40]}'"))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--venue", default="USENIX", choices=list(VENUES))
    ap.add_argument("--sections", default="abstract,intro")
    ap.add_argument("--anonymous", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    stats = load_stats()
    if stats is None:
        print("corpus_stats.json not found; band checks skipped")
    bank = bank_ngrams()
    report = []
    for path in args.files:
        secs = get_sections(path)
        issues = []
        if not secs["abstract"].strip():
            issues.append(("ERROR", "no abstract found"))
        for where in [s.strip() for s in args.sections.split(",")]:
            text = secs.get(where, "")
            if not text.strip():
                if where == "intro":
                    issues.append(("WARN", "no Introduction section found"))
                continue
            if where == "abstract":
                for pat, msg in ABSTRACT_FORBIDDEN:
                    if re.search(pat, text):
                        issues.append(("ERROR", f"abstract: {msg}"))
            b = bands(stats, args.venue, where) if stats else {}
            if b:
                band_checks(where, text, b, issues)
            phrase_checks(text, where, issues)
            hit = {g for g in (ngrams(text) & bank) if not is_boilerplate(g)}
            if hit:
                issues.append(("ERROR", f"{where}: {len(hit)} six-word runs identical to the exemplar bank "
                                        f"(do not copy exemplars): {sorted(hit)[:3]}"))
        venue_rules(args.venue, secs, issues, args.anonymous)
        todos = len(re.findall(r"\\TODO\{|\[TODO", secs["raw"]))
        if todos:
            issues.append(("NOTE", f"{todos} placeholders left in the draft"))
        order = {"ERROR": 0, "WARN": 1, "NOTE": 2}
        issues.sort(key=lambda x: order[x[0]])
        report.append({"file": path, "venue": args.venue, "issues": issues})
        if not args.json:
            print(f"== {path}  (venue {VENUES[args.venue]})")
            for lvl, msg in issues:
                print(f"{lvl:5s} {msg}")
            e = sum(1 for i in issues if i[0] == "ERROR")
            print(f"   {e} ERROR, {sum(1 for i in issues if i[0]=='WARN')} WARN, "
                  f"{sum(1 for i in issues if i[0]=='NOTE')} NOTE\n")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    return 1 if any(i[0] == "ERROR" for f in report for i in f["issues"]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
