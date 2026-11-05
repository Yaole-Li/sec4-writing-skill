#!/usr/bin/env python3
"""Render leaderboard.html from scores.json.

  python3 bench/leaderboard.py [--scores bench/scores.json] [--out bench/leaderboard.html]
"""
import argparse
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench"
DIMS = [f"D{i}" for i in range(1, 10)]
DIM_LABEL = {
    "D1": "Threat model", "D2": "Gap and failing assumption", "D3": "Novelty of the object",
    "D4": "Evidence-calibrated claims", "D5": "Concreteness", "D6": "Positioning",
    "D7": "Ethics and artefacts", "D8": "Flow and economy", "D9": "Method and experiments",
}

CSS = """
:root{--bg:#fbfbfa;--card:#fff;--ink:#17181c;--muted:#6b7280;--line:#e4e6eb;--gold:#b8860b;--accent:#0b5cad;--warn:#b45309}
@media (prefers-color-scheme:dark){:root{--bg:#14161a;--card:#1c1f25;--ink:#e8eaef;--muted:#9aa3b2;--line:#2b303a;--accent:#6aa9ff;--gold:#e0b34a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC","Helvetica Neue",Arial,sans-serif}
main{max-width:980px;margin:0 auto;padding:36px 20px 80px}
h1{font-size:24px;margin:0 0 6px}
.sub{color:var(--muted);font-size:13.5px;margin:0 0 26px}
.banner{background:var(--warn);color:#fff;padding:10px 14px;border-radius:10px;font-weight:600;margin:0 0 22px}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:14px}
th,td{padding:9px 12px;text-align:left;border-bottom:1px solid var(--line)}
th{font-size:12.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-weight:600}
tr:last-child td{border-bottom:none}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.pos{color:#0a7d3f;font-weight:600}.neg{color:#b3261e;font-weight:600}
.bar{display:inline-block;height:8px;border-radius:4px;vertical-align:middle;margin-right:6px}
.wrap{margin:30px 0 0}
h2{font-size:16px;margin:34px 0 10px}
.note{color:var(--muted);font-size:13px;margin-top:10px}
code{background:var(--bg);border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:12.5px}
"""


def bar(v, vmax=5.0, color="var(--accent)"):
    w = max(2, int(120 * v / vmax))
    return f'<span class="bar" style="width:{w}px;background:{color}"></span>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", default=str(BENCH / "scores.json"))
    ap.add_argument("--out", default=str(BENCH / "leaderboard.html"))
    args = ap.parse_args()
    s = json.loads(Path(args.scores).read_text(encoding="utf-8"))
    cfg = s["configs"]
    models = sorted({c.replace("-with", "").replace("-without", "") for c in cfg})

    rows = []
    for m in models:
        w, wo = cfg.get(m + "-with"), cfg.get(m + "-without")
        if not (w and wo):
            continue
        d = s["paired_delta"].get(m)
        cls = "pos" if (d or 0) > 0 else "neg"
        rows.append(f"<tr><td>{html.escape(m)}</td>"
                    f"<td class='num'>{wo['overall']}</td>"
                    f"<td class='num'>{bar(wo['overall'], color='var(--muted)')}{wo['overall']}</td>"
                    f"<td class='num'>{w['overall']}</td>"
                    f"<td class='num'>{bar(w['overall'])}{w['overall']}</td>"
                    f"<td class='num {cls}'>{d:+.2f}</td>"
                    f"<td class='num'>{w['ci95'][0] if w['ci95'][0] is not None else '—'}–"
                    f"{w['ci95'][1] if w['ci95'][1] is not None else '—'}</td></tr>")

    dim_rows = []
    for m in models:
        for cfgname, tag in ((m + "-without", "w/o"), (m + "-with", "w/ ")):
            c = cfg.get(cfgname)
            if not c:
                continue
            cells = "".join(f"<td class='num'>{c['per_dim'][d]}</td>" for d in DIMS)
            dim_rows.append(f"<tr><td>{html.escape(m)}</td><td>{tag}</td>{cells}</tr>")

    case_rows = []
    for m in models:
        for cfgname, tag in ((m + "-without", "w/o"), (m + "-with", "w/ ")):
            c = cfg.get(cfgname)
            if not c:
                continue
            cells = "".join(f"<td class='num'>{v}</td>" for _, v in sorted(c["per_case"].items()))
            case_rows.append(f"<tr><td>{html.escape(m)}</td><td>{tag}</td>{cells}</tr>")
    case_names = sorted({k for c in cfg.values() for k in c["per_case"]})

    ceil_pairs = " · ".join(f"{html.escape(k)} = {v}" for k, v in sorted(s.get("reference_ceiling", {}).items()))
    judges_txt = " · ".join(f"{html.escape(k)}: {v}" for k, v in sorted(s["judges_per_case"].items()))
    banner = ('<div class="banner">SYNTHETIC — at least one judgment came from judge_stub.py. '
              'These numbers prove the pipeline runs and say nothing about any model.</div>'
              if s.get("synthetic") else "")

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>security-conf-writing · leaderboard{' (synthetic)' if s.get('synthetic') else ''}</title>
<style>{CSS}</style></head>
<body><main>
<h1>Does the skill move a draft closer to the published paper?</h1>
<p class="sub">{html.escape(s['protocol'])} · cases: {', '.join(map(html.escape, s['cases']))} ·
judges per case: {judges_txt}</p>
{banner}
<table>
<thead><tr><th>Model</th><th class="num">w/o skill</th><th></th><th class="num">w/ skill</th><th></th>
<th class="num">Δ</th><th class="num">95% CI (w/ skill)</th></tr></thead>
<tbody>{''.join(rows) or '<tr><td colspan="7">no paired configurations yet</td></tr>'}</tbody>
</table>
<p class="note">A score of 5 means indistinguishable from the published paper, which is in the pool as a
ceiling. The headline number is the paired difference: same model, same case, same facts.</p>

<div class="wrap"><h2>Per dimension</h2>
<table><thead><tr><th>Model</th><th>Skill</th>{''.join(f'<th class="num">{d}</th>' for d in DIMS)}</tr></thead>
<tbody>{''.join(dim_rows)}</tbody></table>
<p class="note">{html.escape(' · '.join(f'{k} {v}' for k, v in DIM_LABEL.items()))}</p></div>

<div class="wrap"><h2>Per case</h2>
<table><thead><tr><th>Model</th><th>Skill</th>{''.join(f'<th class="num">{html.escape(c)}</th>' for c in case_names)}</tr></thead>
<tbody>{''.join(case_rows)}</tbody></table>
{f'<p class="note">Published paper (ceiling), mean of D1–D9: {ceil_pairs}</p>' if ceil_pairs else ''}</div>

<p class="note">Regenerate: <code>python3 bench/score_judgments.py &amp;&amp; python3 bench/leaderboard.py</code></p>
</main></body></html>"""
    Path(args.out).write_text(doc, encoding="utf-8")
    print(f"wrote {args.out}  ({len(doc)} bytes, synthetic={s.get('synthetic')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
