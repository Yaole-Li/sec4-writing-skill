# 安全四大顶会写作 skill 构建计划

目标：基于 `<corpus-dir>`（268 篇，S&P/USENIX/NDSS，无语料级 CCS），复用
`tifs-paper-writing` 的八阶段方法，产出 `skills/security-conf-writing/`。

| 阶段 | 内容 | 状态 |
|---|---|---|
| S0 | 抽取 268 篇（三种版式，含 USENIX 封面页、编号差异） | complete |
| S1 | 划分 241 拟合 / 27 留出（会议 × 年分层哈希） | complete |
| S2 | 120 篇逐句标注（4 批并行） | complete |
| S3 | 按会议分位数统计 + 结构普查 | complete |
| S4 | 15 篇规则文档（会议政策与语料实测分开标注） | complete |
| S5 | 5 个脚本（venue-aware check_draft） | complete |
| S6 | 信息表 + 四套 LaTeX 模板（均编译验证） | complete |
| S7 | 2 个留出用例 × 13 判据 + rubric + score_outputs | complete |
| S8 | 打包、安装到 DSH、验收 | in progress |

## 关键决策

| 决策 | 选择 | 理由 |
|---|---|---|
| CCS 处理 | 模板与政策给全，规则标为「约定」 | 语料 0 篇 CCS，不能假装拟合 |
| 段落级功能序列 | 放弃，改为句级移动 + 定性分层 | 三种版式段落边界不可靠恢复 |
| 模板 | SP/NDSS 用 IEEEtran，USENIX 用本地 stand-in，CCS 用 acmart | 官方 kit 不在 TeX Live |
| 标注规模 | 120 篇（拟合集的 50%） | 类型/缺口分布稳定，边际收益递减 |

## 遇到的错误

| 错误 | 处理 |
|---|---|
| S&P/USENIX 章节编号混用（arabic/roman/无编号） | 双正则 + 已知无编号标题（Ethics/Open Science/Acknowledgments）合并 |
| `SEC_ARABIC` 写成 `{{2,90}}` 导致 NDSS/S&P 零章节 | 修正为 `{2,90}` |
| USENIX 标题编号独占一行 | 预先把「数字 + 换行 + 标题」合并 |
| USENIX 有 proceedings 封面页 | 检测 "is included in the Proceedings of" 后截断 |
| 8 篇 USENIX 摘要落在文本层之外 | 标记为不可用，只从摘要统计中排除 |
| 标题里的冒号被文件名吃掉 | 用 index.csv 的真实标题回填 268 篇 |
| 标注的引言功能序列长度失真（一句一个字母） | 加长度过滤（4–15），只用于定性结论 |
| 范例库写入路径沿用了 TIFS 的目录 | 修正 OUT 路径并删除误建的目录 |
