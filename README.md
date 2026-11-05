<div align="center">

# Security Conference Writing Skill

**按安全四大顶会的写法，生成摘要、引言、威胁模型、设计、评测、伦理与开源声明**

写作规律提炼自 268 篇 IEEE S&P / USENIX Security / NDSS 论文（2023–2026），按会议分层校准

![corpus](https://img.shields.io/badge/corpus-268%20papers-orange) ![fit](https://img.shields.io/badge/fit-241%20%7C%20held--out-27-blue) ![venues](https://img.shields.io/badge/venues-S%26P%20%C2%B7%20USENIX%20%C2%B7%20NDSS-informational) ![license](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey)

[论文清单](PAPER_LIST.md) · [更新日志](CHANGELOG.md) · [Skill 入口](skills/security-conf-writing/SKILL.md)

</div>

---

## 先读这一条：语料里没有 CCS

`<corpus-dir>` 的 268 篇里只有三个会议：**S&P 95、USENIX Security 116、NDSS 57**，CCS 为 0 篇。

因此这个 skill 的分层是诚实的：

- **S&P / USENIX / NDSS**——每一条风格区间、摘要预算、图表数量都由该会议的拟合集算出。
- **CCS**——模板、CCS Concepts、12 页限制、artifact 徽章按 ACM 与会议政策给出，并在文档里逐处标为「约定，未经语料校准」。

要把 CCS 也变成实测，把 CCS PDF 放进同一个文件夹（命名 `年_CCS_标题.pdf`），重跑 `tools/extract_corpus.py` 起的流水线即可；分类与统计脚本不用改。

## 它能做什么

- **按会议分层的摘要预算**：S&P 271 词、USENIX 211 词、NDSS 226 词（中位），句数与数字个数各不相同。写错会议的长度，审稿人一眼能看出来。
- **引言结构**：中位 1121 词、48 句、18 个数字；只有 9% 的句子以 We/Our 开头。文档给出十段时间骨架与四段决定生死的段落（真实部署、被打破的假设、攻击者、设计）。
- **威胁模型**：目标、知识、能力、可观测量、设定、范围外，六件套逐条给模板；241 篇里 157 篇提到威胁模型，只有 47 篇给它独立章节。
- **伦理与开源**：USENIX 强制要求 Ethics Considerations 与 Open Science 两节（104 篇里 89 篇谈伦理、78 篇声明工件）；文档给出按工作类型（人、真实流量、线上系统、漏洞、LLM、恶意样本）的清单与真实句式。
- **评测章**：设定 → 主张先行的结果 → 鲁棒性与自适应攻击 → 消融 → 开销 → 局限；两个错误方向必须在同一工作点上报。
- **自带检查器**：`check_draft.py --venue` 按该会议的分位数检查摘要与引言，并检查伦理/开源/威胁模型/CCS 元数据是否齐全；`check_figures.py` 检查图注、标签与浮动体。
- **不编造**：没给的数字、基线、攻击者能力、伦理审批，一律 `[TODO]`。

## 与会话语料对齐的判定（节选）

同一句话在不同会议、不同语料里的判定会反转。这个 skill 的判定来自本语料 241 篇的实测出现率：

| 短语 | 摘要出现 | 引言出现 | 判定 |
|---|---|---|---|
| `with the rapid development` | 1 / 241 | 0 / 241 | ERROR |
| `plays an important role` | 0 / 241 | 0 / 241 | ERROR |
| `our key insight is` | 0 / 241 | 0 / 241 | ERROR |
| `has attracted increasing attention` | 1 / 241 | 1 / 241 | ERROR |
| `delve` | 3 / 241 | 5 / 241 | WARN |
| `in recent years` | 4 / 241 | 17 / 241 | WARN |
| `novel` | 72 / 241 | 107 / 241 | 正常写法 |
| `state-of-the-art` | 52 / 241 | 76 / 241 | 正常写法，但要求同句点名基线 |
| `extensive experiments` | 28 / 241 | 28 / 241 | 正常写法 |

## 语料

| 项 | 值 |
|---|---|
| 论文数 | 268（S&P 95 · USENIX 116 · NDSS 57），2023–2026 |
| 拟合 / 留出 | 241 / 27 |
| 页数 | 中位 19（17–21，含参考文献与附录） |
| 图 / 表 | 中位 9 / 8；浮动体密度 0.95 / 页 |
| 摘要 | 中位 230 词（S&P 271 · USENIX 211 · NDSS 226） |
| 引言 | 中位 1121 词、48 句、18 个数字 |
| 标注 | 120 篇逐句标注：类型、缺口类型、移动标签、威胁模型/伦理/开源落位 |

主题偏斜需要说清：索引把 116/268 标为 LLM、61 为流量分析、18 为 agent。这是一份偏网络与 LLM 安全的样本，不是四个会议的均匀抽样。

## 怎么做出来的（八步，与 TIFS 那套一致）

1. **抽取**：三种版式（IEEE 双栏、USENIX 双栏含封面页、NDSS 双栏）分别处理噪声、标题编号与页脚（`tools/extract_corpus.py`）。
2. **划分**：按会议 × 年份分层哈希，27 篇留出（`tools/make_split.py`）。
3. **标注**：120 篇，4 个批次并行，逐句标注移动与类型（`data/annot/`）。
4. **统计**：按会议分别拟合分位数（`tools/fit_stats.py`）+ 结构普查（`tools/census.py`）。
5. **规则文档**：15 篇 references，数字带分母；会议政策与语料实测分开标注。
6. **脚本**：检查器读统计文件，按 `--venue` 切分位数。
7. **输入契约**：`sec4-intake/v1` 表单，必填 5 项，含伦理与开源两栏。
8. **留出评测**：2 个用例 × 13 条判据 + 盲评量表 + 确定性信号。

标注质量由脚本把关：每条引用必须逐字命中源文本，未命中的不进范例库（392/395 通过）。

## 安装

```bash
cd sec4-writing-skill
./install.sh codex     # DeepSeek Harness / Codex -> ~/.agents/skills/
./install.sh claude    # Claude Code -> ~/.claude/skills/
./install.sh all       # 两个都装；加 --project 装到当前项目
```

## 两种使用方式

**填表**：浏览器打开 `skills/security-conf-writing/assets/intake_form.html`，导出 JSON。

> 用 security-conf-writing，目标 USENIX Security，根据这份信息表 JSON 写出 Title、Abstract、Introduction、Threat Model、Design、Evaluation、Ethics 和 Open Science。

**贴草稿**：把摘要或整段引言贴进来，skill 先反推成信息表字段、给出「已有/模糊/缺失」对照表，再写底稿并附逐句修改对照表。

## 目录结构

```
sec4-writing-skill/
├── README.md / PAPER_LIST.md / CHANGELOG.md / NOTICE.md / LICENSE / install.sh
├── data/                       # papers.csv · split.json · corpus_stats.json · annotation_stats.json · census.json · annot/
├── tools/                      # 抽取、划分、统计、普查、范例库、标注合并（构建用）
├── bench/                      # 第 ④ 层评测：run → blind pack → judge → score → leaderboard
└── skills/security-conf-writing/
    ├── SKILL.md                # 入口：工作流与硬性规则
    ├── references/             # 15 篇规则文档 + corpus_stats.json + 范例库
    ├── scripts/                # check_draft · check_figures · style_metrics · find_exemplars · intake_to_brief
    ├── assets/intake_form.html
    ├── template/{SP,NDSS,USENIX,CCS}/   # 四套模板，均编译验证
    ├── evals/                  # 2 个留出用例 × 13 判据 + rubric + score_outputs
    └── agents/openai.yaml
```

## Benchmark（第 ④ 层：模型 × 有/无技能）

`bench/` 复刻了参考项目只在网页上发布的那层评测，三件它没开源的东西都补上了：盲评包生成器、评委提示词与打分聚合。

```bash
python3 bench/selftest.py                 # 端到端自检（无需调用任何模型）
python3 bench/run_case.py --case vpn-tunnel-leak --config opus-with   # 铺一次运行
AGENT_CMD='<你的 agent CLI>' python3 bench/run_case.py --case vpn-tunnel-leak --config opus-with --agent "$AGENT_CMD"
python3 bench/pack.py --case vpn-tunnel-leak --reference refs/original.txt   # 匿名成 A/B/C/D
python3 bench/judge_stub.py --case vpn-tunnel-leak --judge judge-1           # 换成真实评委时替换这一步
python3 bench/score_judgments.py && python3 bench/leaderboard.py
```

口径与参考项目一致：候选池包含**原始论文**作为上限，3 位评委盲评 D1–D9，配置得分是九个维度的均值再对评委与用例求平均，头条数字是**同一模型的配对差**（有技能 − 无技能）。产物：[`bench/leaderboard.html`](bench/leaderboard.html)、[`bench/scores.json`](bench/scores.json)，自检样例在 [`bench/demo/`](bench/demo/)。

自检产出全部带 `SYNTHETIC` 标记，因为 `judge_stub.py` 只做确定性代理打分，用来证明流水线跑得通，不构成任何模型结论。

## 已知限制

- **CCS 无语料**：CCS 全部分层是约定。
- **段落级标注未做成**：三种版式的段落边界无法从纯文本可靠恢复，引言的功能分层因此是定性的，已写在 `introduction.md` 里。
- **主题偏斜**：LLM 与流量分析占比高，硬件、密码学、取证方向样本少。
- **模板是骨架**：S&P/NDSS 用本地 IEEEtran，USENIX 用本地 stand-in，提交前必须换成官方 kit。
- **产物徽章检测不到**：proceedings 里是图片，文本普查为 0，这属于抽取假象，已写明。

## 版权与许可

- 原创内容（文档、脚本、模板骨架、统计量）采用 [CC BY 4.0](LICENSE)。
- 范例库中的论文短句与 117 篇摘要仅作教学评论引用并注明出处，版权归原作者，请勿复制进新论文。
- 本仓库不含论文 PDF 或全文。详见 [`NOTICE.md`](NOTICE.md)。
