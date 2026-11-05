#!/usr/bin/env python3
"""Validate judge JSON, map labels back to configurations, aggregate, write scores.json.

  python3 bench/score_judgments.py [--judgments DIR] [--packs DIR] [--out scores.json]

Aggregation follows the protocol of the reference project: a candidate's score is the mean of D1-D9;
a configuration's score is that mean pooled over judges and cases. The headline number is the paired
difference (with skill minus without skill) for the same model and the same case.
"""
import argparse
import json
import random
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BENCH = ROOT / "bench"
DIMS = [f"D{i}" for i in range(1, 10)]


def load_judgments(d):
    out = {}
    for p in sorted(Path(d).glob("*/*.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        case = data.get("case") or p.stem
        out.setdefault(case, []).append(data)
    return out


def validate(rec):
    errs = []
    for lab, sc in (rec.get("scores") or {}).items():
        for d in DIMS:
            v = sc.get(d)
            if not isinstance(v, int) or not 1 <= v <= 5:
                errs.append(f"{lab}.{d}={v!r}")
    rk = rec.get("ranking") or []
    labs = sorted((rec.get("scores") or {}).keys())
    if sorted(rk) != labs:
        errs.append(f"ranking {rk} is not a permutation of {labs}")
    return errs


def boot_ci(values, n=2000, seed=7):
    if len(values) < 2:
        return [None, None]
    rnd = random.Random(seed)
    means = []
    for _ in range(n):
        means.append(st.mean(rnd.choice(values) for _ in values))
    means.sort()
    return [round(means[int(0.025 * n)], 2), round(means[int(0.975 * n)], 2)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judgments", default=str(BENCH / "judgments"))
    ap.add_argument("--packs", default=str(BENCH / "packs"))
    ap.add_argument("--out", default=str(BENCH / "scores.json"))
    args = ap.parse_args()

    judgments = load_judgments(args.judgments)
    if not judgments:
        sys.exit(f"no judgments under {args.judgments}; run bench/judge_stub.py or collect real ones")

    problems, synthetic = [], False
    per_config_case = {}          # (config, case) -> [means]
    per_config_case_dim = {}      # (config, case) -> {dim: [scores]}
    reference_scores = {}
    for case, recs in judgments.items():
        key_path = Path(args.packs) / case / "key.json"
        if not key_path.exists():
            problems.append(f"{case}: no key.json, cannot map labels")
            continue
        key = json.loads(key_path.read_text(encoding="utf-8"))["map"]
        for rec in recs:
            synthetic = synthetic or bool(rec.get("synthetic"))
            for e in validate(rec):
                problems.append(f"{case}/{rec.get('judge')}: {e}")
            for label, sc in (rec.get("scores") or {}).items():
                name = key.get(label)
                if not name:
                    problems.append(f"{case}/{rec.get('judge')}: label {label} not in key")
                    continue
                mean = st.mean(sc[d] for d in DIMS)
                if name == "reference":
                    reference_scores.setdefault(case, []).append(mean)
                    continue
                per_config_case.setdefault((name, case), []).append(mean)
                d = per_config_case_dim.setdefault((name, case), {x: [] for x in DIMS})
                for x in DIMS:
                    d[x].append(sc[x])

    configs = sorted({c for c, _ in per_config_case})
    cases = sorted({k for _, k in per_config_case})
    by_config = {}
    for cfg in configs:
        means = [m for (c, _), v in per_config_case.items() if c == cfg for m in v]
        by_config[cfg] = {"overall": round(st.mean(means), 2) if means else None,
                          "n": len(means),
                          "ci95": boot_ci(means),
                          "per_case": {case: round(st.mean(v), 2)
                                       for (c, case), v in per_config_case.items() if c == cfg},
                          "per_dim": {d: round(st.mean(x), 2) for d, x in
                                      {dd: [s for (c, _), vv in per_config_case_dim.items()
                                            if c == cfg for s in vv[dd]] for dd in DIMS}.items()}}

    pairs = {}
    for cfg in configs:
        if cfg.endswith("-with"):
            base = cfg[:-5] + "-without"
            if base in by_config and by_config[cfg]["overall"] and by_config[base]["overall"]:
                pairs[cfg[:-5]] = round(by_config[cfg]["overall"] - by_config[base]["overall"], 2)

    result = {
        "protocol": "mean of D1-D9, pooled over judges and cases; headline = paired difference",
        "synthetic": synthetic,
        "cases": cases,
        "judges_per_case": {c: len(v) for c, v in judgments.items()},
        "configs": by_config,
        "paired_delta": pairs,
        "reference_ceiling": {c: round(st.mean(v), 2) for c, v in reference_scores.items()},
        "problems": problems,
    }
    Path(args.out).write_text(json.dumps(result, indent=1), encoding="utf-8")

    print(f"{'config':22s} {'overall':>8s} {'n':>4s} {'95% CI':>14s}")
    for cfg, v in sorted(by_config.items()):
        ci = v["ci95"]
        print(f"{cfg:22s} {v['overall']!s:>8s} {v['n']:>4d} {str(ci):>14s}")
    if pairs:
        print("\npaired difference (with skill - without skill):")
        for m, d in sorted(pairs.items()):
            print(f"  {m:10s} {d:+.2f}")
    if result["reference_ceiling"]:
        print("\npublished paper (ceiling):", result["reference_ceiling"])
    if synthetic:
        print("\nWARNING: at least one judgment is synthetic (judge_stub). These numbers prove the "
              "pipeline runs; they say nothing about any model.")
    if problems:
        print(f"\n{len(problems)} problems:")
        for p in problems[:10]:
            print("  -", p)
    print(f"\nwrote {args.out}")
    return 0 if not problems else 2


if __name__ == "__main__":
    sys.exit(main())
