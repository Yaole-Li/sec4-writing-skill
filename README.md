<div align="center">

# Security Conference Writing Skill

**按安全四大顶会的写法，生成摘要、引言、威胁模型、设计、评测、伦理与开源声明**

🏆 写作规律提炼自 268 篇 IEEE S&P / USENIX Security / NDSS 论文（2023–2026），一个 Skill 同时支持 Claude 与 Codex

[![corpus](https://img.shields.io/badge/corpus-268%20papers-orange)](PAPER_LIST.md) [![fit](https://img.shields.io/badge/fit-241%20of%20268-green)](skills/security-conf-writing/references/corpus-profile.md) [![venues](https://img.shields.io/badge/venues-S%26P%20%C2%B7%20USENIX%20%C2%B7%20NDSS-informational)](#-语料268-篇安全顶会论文) [![version](https://img.shields.io/badge/version-v1.0-blue)](CHANGELOG.md) [![license](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey)](LICENSE)

[📚 论文清单](PAPER_LIST.md) · [📝 更新日志](CHANGELOG.md) · [🧩 Skill 入口](skills/security-conf-writing/SKILL.md) · [📊 评测排行榜](bench/leaderboard.html)

</div>

---

## ✨ 它能做什么

输入一篇安全研究的事实，输出一份符合顶会审稿人期待的底稿：

- 📝 **摘要与引言**：先给部署现实，再给被打破的假设、攻击者与带设置的结果。摘要预算按会议分层：S&P 271 词、USENIX 211 词、NDSS 226 词
- 🛡️ **威胁模型**：目标、知识、能力、可观测量、设定、范围外，六件套逐条给模板。语料里 157/241 篇提到威胁模型，其中 47 篇给它独立章节
- 🧩 **设计与评测**：组件按「需要 → 机制 → 性质」串起来；评测按「设定 → 主张先行的结果 → 鲁棒性与自适应攻击 → 消融 → 开销 → 局限」展开
- ⚖️ **伦理与开源**：USENIX 强制要求 Ethics Considerations 与 Open Science 两节；语料里 89/104 篇谈伦理、78/104 篇声明工件，文档按工作类型给出清单与真实句式
- 🧭 **按论文类型路由**：七类论文（攻击、防护、测量、系统、分析、SoK、数据集）各有论证路线与审稿人关注点
- 🔍 **自带检查器**：`check_draft.py --venue` 按该会议的分位数检查摘要与引言，并检查伦理、开源、威胁模型、CCS 元数据是否齐全
- 📋 **附带作者报告 `report.md`**：核心主张、攻击者一句话、被打破的假设、主张-证据表、待补清单、留给 Limitations 的要点
- 🔒 **不编造**：没给的数字、基线、攻击者能力、伦理审批，一律保留为 `[TODO]`

## 为什么不直接用通用提示词？

通用模型的稿子彼此相似，而安全顶会的稿子有自己的形状。下面每一条都来自语料实测，不是个人偏好：

| 写法 | 通用 AI 草稿 | 安全顶会论文 |
|---|---|---|
| 摘要长度 | 一段 150–200 词的通用背景 | S&P 271 词、USENIX 211 词、NDSS 226 词（中位） |
| 开场 | 「随着……的快速发展」 | 部署现实：什么技术在用、谁暴露在风险中 |
| 缺口 | 「现有方法存在局限」 | 前人的哪条假设被打破、在什么条件下、代价是什么 |
| 攻击者 | 常缺失 | 目标、知识、能力、范围外，四件事写清 |
| 组件 | A 做……B 做……C 做……（并排） | 第二个组件解决第一个留下的问题（因果串联） |
| 伦理与披露 | 常缺失 | USENIX 27/104 篇有独立伦理小节，89/104 篇正文讨论 |
| 词表 | 一律避免「novel」「SOTA」 | `novel` 72/241、`state-of-the-art` 52/241 属正常写法 |

规则来自对语料的逐句标注与统计，每条规则都带分母，而不是一味向「平均值」靠拢。

## 🚀 两种使用方式

**📝 填表 / 📄 贴草稿** → **🔍 补全缺项** → **🧭 选论证路线** → **✍️ 对照范例起草** → **✅ 自检** → **📦 论文稿 + `report.md`**

### 📝 方式一：填写信息表

用浏览器打开 [`skills/security-conf-writing/assets/intake_form.html`](skills/security-conf-writing/assets/intake_form.html)（离线可用，自动保存，可导出与再次导入 JSON）。必填 5 项，推荐 8 项，其余折叠在补充信息与方法实验里：

| 档位 | 内容 |
|---|---|
| ⚙️ 基本设置 | 目标会议（S&P / USENIX / NDSS / CCS）、论文类型（A1–A7）、要写哪些部分 |
| 🔴 必填（5） | 一句话说清工作、任务与受影响方、威胁模型、失效现象、头条结果 |
| ⭐ 推荐（8） | 方法组成、现有最强工作、失败的技术原因、核心观察、最相近工作与差异、具体画面、代价、反直觉之处、团队内部叫法 |
| 🟢 补充（折叠） | 伦理与披露、开源与工件、次要结果、局限、其他材料、refs.bib |
| 🔵 方法与实验（折叠） | 设定与符号、组件、数据集、指标、对比方法、自适应攻击、开销 |

把导出的 JSON 发给 agent：

> 用 security-conf-writing，目标 USENIX Security，根据这份信息表 JSON 写出 Title、Abstract、Introduction、Threat Model、Design、Evaluation、Ethics 和 Open Science。

### 📄 方式二：直接给草稿

skill 不会盲目重写。它先把草稿拆回信息表字段，给出「已有 / 模糊 / 缺失」对照表，一次性追问缺项，再写完整底稿，并附摘要的**修改对照表**（原句 → 改后句 → 依据哪条语料规律），你可以逐条接受或拒绝。你的数字与术语原样保留，草稿里没有的数字、基线与引用一律留作 `[TODO]`。

> 用 security-conf-writing，目标 IEEE S&P，根据这段草稿把它改成投稿形态。

## 📦 安装

```bash
git clone https://github.com/Yaole-Li/sec4-writing-skill.git
cd sec4-writing-skill

./install.sh codex      # DeepSeek Harness / Codex -> ~/.agents/skills/
./install.sh claude     # Claude Code -> ~/.claude/skills/
./install.sh all        # 两个都装；加 --project 则装到当前项目
```

| 平台 | 方式 |
|---|---|
| 🟢 **Codex / DeepSeek Harness** | `./install.sh codex`，或手动复制 `skills/security-conf-writing/` 到 `~/.agents/skills/`；用 `$security-conf-writing` 显式调用 |
| 🟣 **Claude Code** | `./install.sh claude`，或手动复制到 `~/.claude/skills/` |
| 🟣 **Claude.ai / Cowork** | 把 `security-conf-writing` 文件夹打成 zip，在 Skills 页面上传 |

辅助脚本需要 Python 3；模板需要 LaTeX（S&P/NDSS 用 `IEEEtran`，CCS 用 `acmart`，都随 TeX Live 发布；USENIX 需换成官方 `usenix2019_v3.sty`）。装好后若看不到，重启 agent。

## 🗂️ 目录结构

```
sec4-writing-skill/
├── README.md / PAPER_LIST.md / CHANGELOG.md / NOTICE.md / LICENSE
├── data/                      # papers.csv · split.json · corpus_stats.json · census.json · annot/
├── tools/                     # 抽取、划分、统计、普查、范例库生成、标注合并（构建用）
├── bench/                     # 第 ④ 层评测：run → blind pack → judge → score → leaderboard
└── skills/security-conf-writing/
    ├── SKILL.md               # 入口：工作流与硬性规则
    ├── references/            # 18 篇规则文档 + corpus_stats.json + 范例库
    │   └── exemplars/         # 392 条移动句 · 117 篇摘要 · 125 条句式框架
    ├── scripts/               # check_draft · check_figures · style_metrics · find_exemplars · intake_to_brief
    ├── assets/                # intake_form.html
    ├── template/              # SP · NDSS · USENIX · CCS 四套模板，均编译验证
    ├── evals/                 # 2 个留出用例 × 13 判据 + 盲评量表 + score_outputs
    └── agents/openai.yaml
```

## 📚 语料：268 篇安全顶会论文

2023 至 2026 年 IEEE S&P、USENIX Security 与 NDSS 的论文，来自各会议公开 proceedings。

| 会议 | 篇数 | 摘要中位 | 引言中位 | 页数中位 |
|---|---|---|---|---|
| IEEE S&P | 95 | 271 词 | 993 词 | 19 |
| USENIX Security | 116 | 211 词 | 1162 词 | 21 |
| NDSS | 57 | 226 词 | 1168 词 | 18 |

类型分布（120 篇标注）：攻击 35 · 系统 28 · 测量 25 · 防护 14 · 分析 8 · SoK 5 · 数据集 5。缺口类型：能力缺失 28 · 新威胁面 25 · 假设过时 15 · 特定条件下失效 15 · 洞察 14 · 代价过高 13 · 规模不足 10。

> 🔬 **关于留出测试**：规则由其中 241 篇拟合，另外 27 篇（S&P 9 · USENIX 12 · NDSS 6）从范例库中移除，只用来测试。`data/split.json` 与 `data/papers.csv` 的 `role` 列记录了这条划分，`tools/build_exemplars.py` 每次重建范例库都会重新核对。

## 🔍 检查器对照什么

阈值全部来自对应会议的分位数，句式严重性按短语在 241 篇拟合集中的出现率来定：

| 短语 | 摘要出现 | 引言出现 | 判定 |
|---|---|---|---|
| `with the rapid development` | 1 / 241 | 0 / 241 | ERROR |
| `plays an important role` | 0 / 241 | 0 / 241 | ERROR |
| `our key insight is` | 0 / 241 | 0 / 241 | ERROR |
| `has attracted increasing attention` | 1 / 241 | 1 / 241 | ERROR |
| `delve` | 3 / 241 | 5 / 241 | WARN |
| `in recent years` | 4 / 241 | 17 / 241 | WARN |
| `to the best of our knowledge` | 2 / 241 | 21 / 241 | 正常写法 |
| `novel` | 72 / 241 | 107 / 241 | 正常写法 |
| `state-of-the-art` | 52 / 241 | 76 / 241 | 正常写法，但要求同句点名基线 |
| `extensive experiments` | 28 / 241 | 28 / 241 | 正常写法 |

除句式外，检查器还核对会议硬性要求：USENIX 的 Ethics 与 Open Science 两节、CCS 的 CCS Concepts 与 keywords、攻击与防护论文的威胁模型、摘要中的引用与公式、与范例库重合的六词片段。

## 🧪 第 ④ 层评测：装上技能前后

`bench/` 复刻了参考项目只在网页上发布的那一层，并补齐了它没开源的三个部件：盲评包生成器、评委提示词与打分聚合。

口径与参考项目一致：候选池包含**原始论文**作为上限，3 位评委盲评 D1–D9，配置得分是九维均值再对评委与用例求平均，头条数字是**同一模型的配对差**（有技能 − 无技能）。

```bash
python3 bench/selftest.py            # 端到端自检，不调用任何模型
python3 bench/run_case.py --case vpn-tunnel-leak --config opus-with
python3 bench/pack.py --case vpn-tunnel-leak --reference refs/original.txt
python3 bench/score_judgments.py && python3 bench/leaderboard.py
```

自检样例见 [`bench/demo/leaderboard.html`](bench/demo/leaderboard.html)。该页带 `SYNTHETIC` 标记：`judge_stub.py` 只做确定性代理打分，用来证明流水线可跑，不构成任何模型结论。

## 🧭 已知限制

- **段落级功能序列未做成**：三种版式的段落边界无法从纯文本可靠恢复，引言的功能分层因此是定性的，已写在 `references/introduction.md`
- **主题偏斜**：索引把 116/268 标为 LLM、61 为流量分析，硬件、密码学、数字取证方向样本少
- **模板是骨架**：S&P/NDSS 用本地 IEEEtran，USENIX 用本地 stand-in，提交前必须换成官方 kit
- **工件徽章检测不到**：proceedings 里是图片，文本普查为 0，属抽取假象，已在 `corpus-profile.md` 写明
- **评测规模**：留出用例 2 个，够跑通流程，不足以支撑统计显著结论

## 📄 版权与许可

- 原创内容（说明、脚本、模板骨架、统计量）采用 [CC BY 4.0](LICENSE)
- `references/exemplars/` 中的论文短句与摘要仅作教学评论引用并注明出处，版权归原作者，请勿复制进新论文
- 本仓库不含任何论文 PDF 或全文

## 🙏 致谢

构造方法沿用 [Best-Paper-Writing-Skill](https://github.com/gulucaptain/Best-Paper-Writing-Skill)（CC BY 4.0）的八阶段流程，并按期刊与会议体裁重做：语料、统计、标注、文档与脚本均为本项目自带。LaTeX 模板基于 IEEE 的 `IEEEtran` 与 ACM 的 `acmart`。

## 🤝 参与

欢迎通过 Issue 反馈规则在真实投稿中的表现、补充语料缺少的领域（硬件安全、密码学、数字取证），或分享你用这个 skill 写出的稿子。如果它对你有帮助，欢迎点一个 ⭐ Star。

## 📎 语料范围说明

四大顶会里，本语料覆盖 IEEE S&P（95 篇）、USENIX Security（116 篇）与 NDSS（57 篇），**暂不含 ACM CCS**。因此：

| 部分 | 依据 |
|---|---|
| 风格区间、摘要与引言预算、图表数量 | 由该会议自己的拟合集算出 |
| 论文类型、缺口类型、范例库 | 120 篇标注，覆盖三个会议 |
| 伦理、开源与工件指引 | 三个会议的语料，加上各会议公开政策 |
| **CCS 全部分层** | **ACM 类文件与会议政策，属于约定，未经语料校准** |

要把 CCS 也变成实测，把 PDF 放进同一素材目录（命名 `2026_CCS_标题.pdf`），从 `tools/extract_corpus.py` 起重跑一遍流水线即可，分类与统计脚本无需改动。
