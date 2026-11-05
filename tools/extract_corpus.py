#!/usr/bin/env python3
"""Extract a structured corpus from the four-security-conferences PDF library.

Three layouts are present and each needs its own noise model:
  SP       IEEE two-column, roman section numerals, IEEE copyright footer + licence watermark
  NDSS     IEEE-like two-column, arabic section numerals, DOI footer, ndss-symposium.org footer
  USENIX   two-column usenix2019 style with a proceedings cover page, artifact badges,
           "USENIX Association ... NNNN" footer

For every PDF this writes one JSON record with title, abstract, section tree, captions and the
section-level flags a security reviewer looks for (threat model, ethics, open science, artifact).

Usage:
  python3 tools/extract_corpus.py --src "/path/to/library" --out data --limit 3
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

NAME_RE = re.compile(r"^(\d{4})_(NDSS|SP|USENIX)_(.+)\.pdf$", re.I)

VENDOR_NOISE = [
    re.compile(r"^Authorized licensed use limited to:.*$", re.M),
    re.compile(r"^©\s*\d{4}\s*IEEE.*$", re.M),
    re.compile(r"^\d{4}\s+IEEE Symposium on Security and Privacy.*$", re.M),
    re.compile(r"^Network and Distributed System Security \(NDSS\) Symposium.*$", re.M),
    re.compile(r"^ISBN\s+1-891562.*$", re.M),
    re.compile(r"^https?://dx\.doi\.org/10\.14722/.*$", re.M),
    re.compile(r"^www\.ndss-symposium\.org.*$", re.M),
    re.compile(r"^USENIX Association\s+.*$", re.M),
    re.compile(r"^\d{4,5}$", re.M),
    re.compile(r"^Digital Object Identifier.*$", re.M),
]

ROMAN = r"(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV|XVI)"
SEC_ROMAN = re.compile(rf"^({ROMAN})\.\s+([A-Z][^\n]{{2,90}})\s*$", re.M)
SEC_ARABIC = re.compile(r"^(\d{1,2})\.?\s+([A-Z][^\n]{2,90})\s*$", re.M)
SUB_ROMAN = re.compile(r"^([A-Z])\.\s+([A-Z][a-z][^\n]{1,90})\s*$", re.M)
SUB_ARABIC = re.compile(r"^(\d\.\d)\s+([A-Za-z][^\n]{1,90})\s*$", re.M)
UNNUMBERED = re.compile(r"^(Ethics Considerations|Ethics|Open Science|Acknowledg(?:e)?ments|"
                        r"Responsible Disclosure|Artifact(?:s| Appendix)?|Appendix(?: [A-Z])?)\s*$", re.M)
FIG_RE = re.compile(r"^Fig(?:ure)?\.?\s*(\d+)\s*[:.]\s*(.*)$", re.M)
TAB_RE = re.compile(r"^(?:TABLE|Table)\s+([IVX\d]+)\s*[:.]?\s*(.*)$", re.M)

CANON_RULES = [
    ("ethics", r"ETHIC|RESPONSIBLEDISCLOSURE|DISCLOSURE"),
    ("open science", r"OPENSCIENCE|ARTIFACT"),
    ("conclusion", r"CONCLU|FUTUREWORK"),
    ("related work", r"RELATED|BACKGROUND|PRIORWORK|LITERATURE"),
    ("threat model", r"THREATMODEL|ATTACKERMODEL|ADVERSARYMODEL|SECURITYMODEL|ATTACKMODEL"),
    ("discussion", r"DISCUSS|LIMITATION|THREATSTOVALIDITY"),
    ("problem setup", r"PROBLEM|PRELIMINAR|FORMULAT|SYSTEMODEL|NOTATION|SETTING|ASSUMPTION"),
    ("experiments", r"EVALUAT|EXPERIMENT|RESULT|MEASUREMENT|CASESTUDY|ANALYSIS|PERFORMANCE|BENCHMARK|ASSESSMENT"),
    ("method", r"DESIGN|METHOD|APPROACH|SYSTEM|FRAMEWORK|SCHEME|ARCHITECTURE|CONSTRUCTION|IMPLEMENT"),
    ("introduction", r"INTROD"),
]

ETHICS_PAT = re.compile(r"ethic|responsible disclosure|irb approval|institutional review", re.I)
OPENSCI_PAT = re.compile(r"open science|artifact (?:available|evaluated|appendix)|results reproduc", re.I)

_DICT = None


def dictionary():
    global _DICT
    if _DICT is None:
        try:
            _DICT = {w.strip().lower() for w in open("/usr/share/dict/words", encoding="utf-8", errors="ignore")}
        except OSError:
            _DICT = set()
    return _DICT


def dehyphenate(m):
    left, right = m.group(1), m.group(2)
    d = dictionary()
    merged = (left + right).lower()
    if not d or merged in d:
        return left + right
    if left.lower() in d and right.lower() in d:
        return left + "-" + right
    return left + right


def smallcaps_fix(s: str) -> str:
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"(?<![A-Za-z])([A-Z]) ([A-Z]{2,})", r"\1\2", s)
    return s.strip()


def heading_key(s: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def canon(key: str) -> str:
    for name, pat in CANON_RULES:
        if re.search(pat, key):
            return name
    return "other"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    return r.returncode, r.stdout


def pages_of(pdf: Path) -> int:
    _, out = run(["pdfinfo", str(pdf)])
    for line in out.splitlines():
        if line.lower().startswith("pages:"):
            try:
                return int(line.split(":", 1)[1])
            except ValueError:
                pass
    return 0


def text_of(pdf: Path) -> str:
    _, out = run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"])
    return out


def strip_cover(text: str) -> str:
    """USENIX PDFs start with a proceedings cover page; drop everything before the paper body."""
    head = text[:6000]
    if re.search(r"is included in the Proceedings of", head):
        marker = re.search(r"sponsored by USENIX\.?", head)
        if marker:
            return text[marker.end():]
    return text


def clean(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\f", "\n")
    for pat in VENDOR_NOISE:
        text = pat.sub("", text)
    text = re.sub(r"(\w+)-\n(\w+)", dehyphenate, text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def take_abstract(text: str):
    m = re.search(r"^\s*Abstract\s*[—\-:]?\s*", text, re.M)
    if not m:
        m = re.search(r"ABSTRACT\s*[—\-:]?\s*", text)
    if not m:
        return ""
    tail = text[m.end():]
    end = re.search(r"^\s*(?:Index Terms|CCS Concepts|Keywords)\s*[—\-:]?", tail, re.M)
    if not end:
        end = re.search(rf"^({ROMAN}\.\s|\d{{1,2}}\.?\s+[A-Z])", tail, re.M)
    abstract = tail[: end.start()] if end else tail[:2500]
    return re.sub(r"\s+", " ", abstract).strip()


def _heading_ok(title: str, key: str) -> bool:
    """A line is a section heading if it maps to a known canon, or is a short all-caps line."""
    if canon(key) != "other":
        return len(title.split()) <= 10
    words = [w for w in re.split(r"\s+", title) if re.search(r"[A-Za-z]{3,}", w)]
    if not words or len(title.split()) > 7:
        return False
    letters = [c for c in title if c.isalpha()]
    if not letters:
        return False
    upper = sum(1 for c in letters if c.isupper()) / len(letters)
    return upper > 0.8


def split_sections(text: str):
    body = text
    ref = re.search(r"^\s*(?:\d{1,2}\.?\s*)?(?:REFERENCES?|Bibliography)\s*$", body, re.M | re.I)
    if ref:
        body = body[: ref.start()]
    app = re.search(r"^\s*(?:\d{1,2}\.?\s*)?(?:APPENDIX|Appendix)\b.*$", body, re.M)
    if app:
        body = body[: app.start()]
    # USENIX puts the number on its own line: "1\n\nIntroduction" -> "1 Introduction"
    body = re.sub(r"^(\d{1,2})[ \t]*\n+([A-Z][^\n]{2,90})\s*$", r"\1 \2", body, flags=re.M)
    # a heading whose title wrapped to the next line: "VIII.\nPERFORMANCE" -> "VIII. PERFORMANCE"
    body = re.sub(r"^([IVX]{1,6}\.|\d{1,2}\.?)[ \t]*\n(?=[A-Z])", r"\1 ", body, flags=re.M)

    def collect(regex):
        out = []
        for m in regex.finditer(body):
            title = smallcaps_fix(m.group(2))
            key = heading_key(title)
            if _heading_ok(title, key):
                out.append((m, title, key))
        return out

    roman, arabic = collect(SEC_ROMAN), collect(SEC_ARABIC)
    known = lambda lst: sum(1 for _, _, k in lst if canon(k) != "other")
    style = "roman" if known(roman) >= known(arabic) else "arabic"
    marks = list(roman if style == "roman" else arabic)

    # unnumbered headings (USENIX style: "Ethics Considerations", "Open Science", "Acknowledgments")
    for m in UNNUMBERED.finditer(body):
        title = smallcaps_fix(m.group(0))
        key = heading_key(title)
        marks.append((m, title, key))
    marks.sort(key=lambda x: x[0].start())

    sections = []
    for i, (m, title, key) in enumerate(marks):
        end = marks[i + 1][0].start() if i + 1 < len(marks) else len(body)
        chunk = body[m.end(): end]
        sub_re = SUB_ROMAN if style == "roman" else SUB_ARABIC
        subs = [{"level": 2, "title": smallcaps_fix(s.group(2).strip())} for s in sub_re.finditer(chunk)]
        sections.append({"level": 1, "number": m.group(1), "title": title, "key": key,
                         "canon": canon(key), "subsections": subs,
                         "text": re.sub(r"\n{3,}", "\n\n", chunk).strip()})
    return sections, style


def captions(text):
    def join(m):
        head = m.group(2).strip()
        rest = text[m.end():].split("\n\n", 1)[0]
        rest = re.split(r"\bTABLE\s+[IVX\d]+|\bFig(?:ure)?\.?\s*\d+\s*[:.]", rest)[0]
        return re.sub(r"\s+", " ", head + " " + rest).strip()[:600]

    figs = [{"label": m.group(1), "caption": join(m)} for m in FIG_RE.finditer(text)]
    tabs = [{"label": m.group(1), "caption": join(m)} for m in TAB_RE.finditer(text)]
    return figs, tabs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", default="data")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    (out / "text").mkdir(parents=True, exist_ok=True)
    files = sorted(f for f in os.listdir(src) if NAME_RE.match(f))
    if args.limit:
        files = files[: args.limit]

    records, fails = [], []
    for i, name in enumerate(files, 1):
        m = NAME_RE.match(name)
        year, venue, slug = m.group(1), m.group(2).upper(), m.group(3)
        pdf = src / name
        pid = f"{year}-{venue}-" + re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")[:60]
        try:
            n_pages = pages_of(pdf)
            text = text_of(pdf)
            if venue == "USENIX":
                text = strip_cover(text)
            text = clean(text)
            abstract = take_abstract(text)
            sections, style = split_sections(text)
            figs, tabs = captions(text)
            low = text.lower()
            rec = {
                "id": pid, "year": year, "venue": venue,
                "title": re.sub(r"_+", " ", slug).strip(),
                "pages": n_pages,
                "abstract": abstract, "abstract_words": len(abstract.split()),
                "sections": sections,
                "section_titles": [s["title"] for s in sections],
                "section_canons": [s["canon"] for s in sections],
                "heading_style": style,
                "figures": figs, "tables": tabs,
                "n_figures": len(figs), "n_tables": len(tabs),
                "has": {
                    "related_work": any(s["canon"] == "related work" for s in sections),
                    "threat_model_section": any(s["canon"] == "threat model" for s in sections),
                    "threat_model": any(s["canon"] == "threat model" for s in sections) or "threat model" in low,
                    "ethics_section": any(s["canon"] == "ethics" for s in sections),
                    "ethics_mention": bool(ETHICS_PAT.search(text)),
                    "open_science": any(s["canon"] == "open science" for s in sections) or bool(OPENSCI_PAT.search(text)),
                    "artifact_badge": bool(re.search(r"artifact (available|evaluated)|available\s*reusable", low)),
                    "limitations": "limitation" in low,
                    "ablation": "ablation" in low,
                    "proof": "proof" in low,
                    "appendix": "appendix" in low,
                },
                "body_words": len(text.split()),
            }
            records.append(rec)
            (out / "text" / f"{pid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1),
                                                      encoding="utf-8")
        except Exception as ex:  # noqa: BLE001
            fails.append((name, repr(ex)[:160]))
        if i % 25 == 0:
            print(f"  {i}/{len(files)}", flush=True)

    with (out / "corpus.jsonl").open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"ok={len(records)} fail={len(fails)}")
    for n, e in fails[:8]:
        print("  FAIL", n[:60], e)
    noabs = [r["id"] for r in records if r["abstract_words"] < 80]
    print("abstract<80w:", len(noabs), noabs[:5])
    if records:
        print("median sections:", sorted(len(r["sections"]) for r in records)[len(records) // 2])
        print("heading styles:", sorted({r["heading_style"] for r in records}))
        print("median figures:", sorted(r["n_figures"] for r in records)[len(records) // 2])


if __name__ == "__main__":
    sys.exit(main())
