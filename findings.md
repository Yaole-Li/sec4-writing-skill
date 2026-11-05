# 发现记录

只记从数据里量出来的事实，供规则文档引用。数字以 `data/corpus_stats.json` 与 `data/census.json` 为准。

## 语料体检

- 268 篇 PDF：S&P 95、USENIX 116、NDSS 57，2023–2026，共 739 MB；没有 CCS。
- 抽取 268/268 成功；8 篇 USENIX 摘要不可用（不在文本层）。
- 页数中位 19（17–21，含参考文献）；图 9、表 8；浮动体密度 0.95/页。
- 摘要中位：S&P 271、USENIX 211、NDSS 226 词。
- 引言中位：S&P 993、USENIX 1162、NDSS 1168 词，18–20 个数字。

## 结构惯例

- 相关工作中位 1017 词（n=183）；方法 2569（n=137）；实验 3187（n=171）；结论 478（n=144）。
- 威胁模型：提到 157/241，独立章节 47/241。
- 伦理：提到 178/241，独立章节 21/241；USENIX 89/104 提到。
- 开源声明：86/241；USENIX 78/104。
- 局限：214/241 提到。
- 标题含冒号 178/241；SoK 7 篇（S&P 5、USENIX 2）。

## 标注结论（120 篇）

- 类型：A1 攻击 35、A4 系统 28、A3 测量 25、A2 防护 14、A5 分析 8、A6 SoK 5、A7 数据集 5。
- 缺口：capability-gap 28、new-surface 25、assumption-gap 15、failure 15、insight 14、cost 13、scale-gap 10。
- 威胁模型落位：implicit 47、独立章节 31、引言段 23、缺失 15。
- 伦理：缺失 105、引言段 8、独立章节 6。
- 开源：缺失 77、引言句 41、独立章节 2。

## 判定校准

- `with the rapid development` 1/241、`plays an important role` 0/241、`our key insight is` 0/241 → ERROR。
- `novel` 72/241 摘要、`state-of-the-art` 52/241、`we propose` 89/241 → 正常写法。
- `delve` 3/241、`in recent years` 4/241 摘要 → WARN。
