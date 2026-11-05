---
tags: [security-conf-writing, heldout, usenix]
max_turns: 40
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

我在写一篇 USENIX Security 论文，请帮我写**摘要和引言**（英文）。

要求：
- 用 `template/USENIX` 的项目结构：把模板复制到工作目录的 `paper/`，不要改动模板样式。
- 摘要写进 `paper/sec/abstract.tex` 的 abstract 环境（无引用、无公式、无图表引用），引言写进 `paper/sec/introduction.tex`，标题写进 `paper/main.tex`。
- 参考文献只用我给的 `refs.bib`（复制为 `paper/main.bib`）；需要但 bib 里没有的，用 `[TODO: cite ...]` 标出。
- USENIX 要求 Ethics Considerations 与 Open Science 两节，请一并给出骨架（内容可留 `[TODO]`）。
- 本机有 LaTeX，请编译出 `paper/main.pdf`；其他说明写进 `report.md`。

下面是我的工作事实。

**Working name**: 无（两个攻击，分别称 Attack 1 与 Attack 2）

**Task**: 研究 VPN 客户端如何把流量错误地送出 VPN 隧道。输入是被动/主动混合的家庭网络场景（受害者使用桌面或移动 VPN 客户端），输出是"受害者的流量以明文形式离开隧道"这一泄漏事实，以及受影响的客户端数量。

**Threat model / setting**: 敌手控制受害者连接的一个 Wi-Fi 接入点，或者能够伪造 DNS 响应；不破解 VPN 加密，不接触受害者设备，不控制 VPN 服务端。受害者在 Windows、macOS、iOS、Linux、Android 上使用常见 VPN 客户端（免费、付费、开源、企业、系统自带）。

**Root cause**: VPN 客户端通过改写系统路由表把所有流量导向隧道，同时为"本地网络"与"VPN 服务器本身"保留路由例外；这些例外可以被敌手操纵。

**Prior work**: 已有工作研究 VPN 流量识别、隧道指纹、DNS 泄漏检测，但没有把路由表例外当作攻击面；也没有大规模测量各家客户端在这一点上的实现差异。

**Results**: 在 5 个操作系统上对 67 家代表性 VPN 提供商的客户端做了 248 次实验；两个攻击分别有 126 与 39 个客户端受影响（64.6% 与 73.6%）；并讨论与验证了缓解措施。

**Disclosure**: 已按负责任披露流程通知相关厂商（具体厂商与时间 `[TODO]`）。

**Artefacts**: 实验脚本与配置 `[TODO: 是否开源]`。

输入文件：refs.bib
