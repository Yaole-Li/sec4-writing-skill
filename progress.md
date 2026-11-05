# 构建日志

## 2026-11-05

### 产出

| 阶段 | 产出 | 验证 |
|---|---|---|
| S0 | `tools/extract_corpus.py`、`data/corpus.jsonl`、`data/text/*.json` | 268/268 抽取成功 |
| S1 | `tools/make_split.py`、`data/papers.csv`、`data/split.json` | 241 / 27，按会议×年分层 |
| S2 | 4 批标注 → `data/annot/batch_1..4.jsonl` | 120 篇、395 条引用中 392 条逐字命中（99.2%） |
| S3 | `tools/fit_stats.py`、`tools/census.py`、`data/corpus_stats.json`、`data/census.json` | 按会议分别拟合 |
| S4 | `references/` 15 篇 | 数字带分母，政策与实测分开 |
| S5 | `scripts/` 5 个 | 四个模板各跑一遍，0 ERROR |
| S6 | `assets/intake_form.html`、`template/{SP,NDSS,USENIX,CCS}` | 表单浏览器实测；四套模板各编译两遍 |
| S7 | `evals/` 2 用例 × 13 判据 + rubric + score_outputs | score_outputs 在模拟目录跑通 |
| S8 | README/CHANGELOG/NOTICE/PAPER_LIST/install.sh、安装到 DSH | install.sh 装到临时 HOME 后脚本可用 |

### 已知限制

- CCS 无语料，全部为约定。
- 段落级功能序列不可靠，引言分层为定性。
- USENIX 模板是本地 stand-in，提交前须换官方 kit。
- 8 篇 USENIX 摘要不可用，仅从摘要统计排除。
