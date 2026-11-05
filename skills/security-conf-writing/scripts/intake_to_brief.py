#!/usr/bin/env python3
"""Turn the intake JSON (schema tifs-intake/v1) into brief.md for writing.

  python3 scripts/intake_to_brief.py intake.json --out brief.md --bib refs.bib

Exit codes: 0 ok, 2 missing required field, 3 unreadable or wrong schema.
Missing recommended fields do not fail: they are listed under "Missing" and the skill asks once,
then leaves [TODO] in the draft.
"""
import argparse
import json
import sys
from pathlib import Path

SCHEMA = "sec4-intake/v1"
REQUIRED = [("required", "one_line"), ("required", "task"), ("required", "threat"),
            ("required", "failure"), ("required", "results")]
RECOMMENDED = [("required", "method"), ("required", "prior_best"), ("required", "failure_reason"),
               ("required", "insight"), ("required", "closest"), ("enhancers", "example"),
               ("enhancers", "overhead"), ("enhancers", "surprising"), ("enhancers", "handle")]
LABEL = {
    "working_name": "Working name", "venue": "Venue", "paper_type": "Paper type",
    "sections": "Sections to write",
    "one_line": "One line", "task": "Task (input -> output, who is exposed)",
    "failure": "Where current methods fail (observable)",
    "threat": "Threat model (goal, knowledge, capability, out of scope)",
    "method": "Method components", "results": "Headline results",
    "prior_best": "Strongest current defense, mechanically",
    "failure_reason": "Technical reason it fails (the assumption that breaks)",
    "insight": "Observation the design follows from",
    "closest": "Closest work and the checkable difference",
    "example": "One concrete picture", "overhead": "Cost (latency, memory, bandwidth)",
    "surprising": "Counter-intuitive finding", "handle": "Internal name for the idea",
    "applications": "What it plugs into", "paper_type": "Paper type",
    "motivation": "Motivation type", "secondary": "Secondary results and ablations",
    "release": "Released artefacts", "limitations": "Limitations (kept out of abstract)",
    "ethics": "Ethics, data handling, disclosure", "openscience": "Artefacts and release",
    "materials": "Other material",
    "bib": "BibTeX",
}


def get(d, sec, key):
    v = (d.get(sec) or {}).get(key)
    if isinstance(v, list):
        v = [x for x in v if x]
    return v


def render_value(v, indent="  "):
    if v in (None, "", [], {}):
        return ""
    if isinstance(v, list):
        lines = []
        for item in v:
            if isinstance(item, dict):
                parts = "; ".join(f"{k}: {x}" for k, x in item.items() if x)
                lines.append(f"{indent}- {parts}")
            else:
                lines.append(f"{indent}- {item}")
        return "\n".join(lines)
    if isinstance(v, dict):
        return "\n".join(f"{indent}- {k}: {x}" for k, x in v.items() if x)
    return f"{indent}{v}"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("intake")
    ap.add_argument("--out", default="brief.md")
    ap.add_argument("--bib", help="write this BibTeX block to a file as well")
    args = ap.parse_args(argv)

    try:
        data = json.loads(Path(args.intake).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as ex:
        print(f"cannot read intake JSON: {ex}", file=sys.stderr)
        return 3
    schema = data.get("schema") or data.get("schema_version")
    if schema and str(schema).startswith("sec4-intake"):
        pass
    elif schema and not str(schema).startswith("sec4-intake"):
        print(f"unexpected schema '{schema}', expected {SCHEMA}", file=sys.stderr)
        return 3

    missing_req = [f"{sec}.{key}" for sec, key in REQUIRED if not get(data, sec, key)]
    if missing_req:
        print("missing required fields:", ", ".join(missing_req), file=sys.stderr)
        print("ask for these once, then rerun; do not invent them.", file=sys.stderr)
        return 2

    missing_rec = [f"{sec}.{key}" for sec, key in RECOMMENDED if not get(data, sec, key)]

    out = ["# Writing brief", "",
           "Generated from the intake JSON. Numbers and mechanisms in this file are the authors' facts;",
           "anything absent stays [TODO] in the draft and is listed in report.md.", ""]

    meta = data.get("meta") or {}
    out += ["## Meta", ""]
    for k in ("working_name", "venue", "paper_type", "sections"):
        if meta.get(k):
            out.append(f"- **{LABEL.get(k, k)}**: {meta[k]}")
    out.append("")

    out += ["## Required", ""]
    for sec, key in REQUIRED:
        v = get(data, sec, key)
        out.append(f"### {LABEL.get(key, key)}")
        out.append(render_value(v))
        out.append("")

    out += ["## Recommended", ""]
    for sec, key in RECOMMENDED:
        v = get(data, sec, key)
        if v:
            out.append(f"### {LABEL.get(key, key)}")
            out.append(render_value(v))
            out.append("")

    enh = data.get("enhancers") or {}
    extra = [(k, v) for k, v in enh.items() if v and k not in [x[1] for x in RECOMMENDED]]
    sup = data.get("support") or {}
    extra += [(k, v) for k, v in sup.items() if v]
    if extra:
        out += ["## Supplementary", ""]
        for k, v in extra:
            out.append(f"### {LABEL.get(k, k)}")
            out.append(render_value(v))
            out.append("")

    me = data.get("methodexp") or {}
    if any(me.values()):
        out += ["## Method and experiments material", ""]
        for k, v in me.items():
            if v:
                out.append(f"### {LABEL.get(k, k.replace('_', ' '))}")
                out.append(render_value(v))
                out.append("")

    out += ["## Missing (ask once, then use [TODO])", ""]
    if missing_rec:
        for m in missing_rec:
            out.append(f"- {LABEL.get(m.split('.')[1], m)}")
    else:
        out.append("- nothing; all recommended fields were supplied")
    out.append("")

    out += ["## Writer notes", "",
            "- Do not add a number, dataset, baseline, attacker capability or citation that is absent here.",
            "- The threat model above must be reproduced in the threat-model section and used by the evaluation.",
            "- Ethics and open-science statements are required by USENIX and expected elsewhere; if they are",
            "  absent here, ask once and otherwise write [TODO].",
            "- Any result without a table label still needs its table; keep [TODO] until the authors supply it.",
            ""]

    Path(args.out).write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {args.out} ({len(out)} lines); missing recommended: {len(missing_rec)}")

    bib = sup.get("bib") or enh.get("bib")
    if args.bib and bib:
        head = bib if bib.strip().startswith("@") else bib
        Path(args.bib).write_text(head + "\n", encoding="utf-8")
        keys = [ln.split("{", 1)[1].split(",", 1)[0] for ln in head.splitlines() if ln.strip().startswith("@")]
        print(f"wrote {args.bib} with {len(keys)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
