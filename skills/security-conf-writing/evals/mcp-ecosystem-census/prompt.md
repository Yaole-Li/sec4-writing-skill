---
tags: [security-conf-writing, heldout, sp]
max_turns: 40
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

我在写一篇 IEEE S&P 论文，请帮我写**摘要和引言**（英文）。

要求：
- 用 `template/SP` 的项目结构：把模板复制到工作目录的 `paper/`，不要改动模板样式。
- 摘要写进 `paper/sec/abstract.tex` 的 abstract 环境，引言写进 `paper/sec/introduction.tex`，标题写进 `paper/main.tex`。
- 参考文献只用我给的 `refs.bib`（复制为 `paper/main.bib`）；缺的用 `[TODO: cite ...]`。
- 给出 Ethics Considerations 与 Open Science 骨架（内容可留 `[TODO]`）。
- 本机有 LaTeX，请编译出 `paper/main.pdf`；其他说明写进 `report.md`。

下面是我的工作事实。

**Working name**: MCP-UPD（攻击模式称 Parasitic Toolchain Attacks）

**Task**: 研究 LLM 通过 Model Context Protocol (MCP) 调用外部工具时出现的隐私泄漏。输入是 MCP 生态中的服务器、工具与外部数据源，输出是一类无需受害者交互即可完成的隐私外泄路径，以及对生态的可利用性普查。

**Threat model**: 敌手把恶意指令嵌入 LLM 在正常任务中会读取的外部数据源；不发生与受害者的直接交互，不需要控制模型或平台；受害者使用具备工具调用能力的 MCP 集成应用。

**Root cause**: MCP 缺少 context–tool 隔离与最小权限约束，使外来指令可以沿着合法的工具链传播到敏感工具调用。

**Attack**: 三阶段——Parasitic Ingestion、Privacy Collection、Privacy Disclosure；与传统的 prompt injection、tool poisoning 不同，攻击对象是相互连接的工具链本身。

**Measurement**: 设计 MCP-SEC，对 MCP 生态做首次大规模安全普查，覆盖 1,360 个服务器上的 12,230 个工具。

**Prior work**: prompt injection、tool poisoning、以及 MCP 平台的安全分析；这些工作关注单次输出操纵或单个工具，没有把多工具编排作为攻击面。

**Results**: 生态中存在大量真实可利用的 gadget 与多种攻击方式（具体数量分布 `[TODO]`）。

**Ethics**: 只分析公开可获取的服务器与工具描述，不触发真实用户数据外泄；发现的问题按披露流程上报 `[TODO: 细节]`。

**Artefacts**: 普查数据集与工具 `[TODO]`。

输入文件：refs.bib
