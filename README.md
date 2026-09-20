# decision-review

审查一个决定，而不是替你做决定。

产出是一份把分歧钉在**可检验点**上的文档：前提列清了、出处查过了、证据分级过了、
每个方案配了能证伪的判据。

## 边界：靠调查收敛 vs 靠市场接触收敛

这个 skill 只处理**能靠调查收敛**的问题。

| | decision-review | office-hours（不在本仓库） |
| --- | --- | --- |
| 问题 | **这个决定对不对** | **这件事值得做吗** |
| 收敛方式 | 调查：读文档、查源码、问干系人、看数据 | 市场接触：找用户、要钱、看留存 |
| 失败标志 | 前提没被检验 | 没人愿意付钱 |

所以它**不限于技术/架构**。同样适用于供应商选型、要不要接某个客户、定价、
自建还是采购、流程变更、合同取舍。

**产品/市场验证请用 gstack 的 `/office-hours`**（跑在 Claude Code 里，带 brain 和
session tiers 的完整版）。不要在这里重复实现。

## 四个机制

1. **提取前提** —— 这个决定依赖哪些假设？逐条标明 `已验证 / 未验证 / 偏好`
2. **核查出处** —— 谁说的、以什么身份、记在什么格式里
3. **证据分级** —— 廉价（本地可查，必须先查）/ 昂贵（标未验证+写代价）/ 没有（直说是偏好）
4. **可证伪判据** —— 什么结果意味着什么，而不是一个推荐

**最容易跳过、也最常出问题的是第 2 条。** 最高危的组合是：内部判断被记进了
正式格式（"客户要求"、"不可协商"、"原话"）。一旦这样记录，它就有了跟外部约束
同等的效力，而没人知道它是怎么生效的——它会静默覆盖已有的正式决策。

## 结构

```
SKILL.md                            骨架：四步机制、一次一问、证据规则、Phase 0-6
references/
  premises-and-evidence.md          前提/出处/证据的操作细则 + 取位分寸
  decision-brief.md                 D<N>/ELI10/Recommendation/判据 格式 + 排除项声明规则
  decision-doc-template.md          输出模板 + 质量自检（含"已否定路径"和"未决问题"）
scripts/
  profile.py                        仓库内决策画像（read/summary/append）
provenance/                         decision-brief 格式的借用出处（gstack, MIT）
```

## 规模

| | 行数 |
| --- | --- |
| SKILL.md（常驻，仅触发时加载） | 约 175 |
| references/（按需加载） | 约 300 |
| scripts/profile.py | 约 180 |

## 记忆层

`.agents/profile.md`，写在仓库里，跟代码走、跨 agent 可用。与 `repo-checkpoint`
的 `.agents/checkpoints/` 互补：

- **checkpoints** = 任务状态（这件事做到哪了）
- **profile** = 决策画像（这个人怎么决策、反复卡在哪）

`summary` 会聚合跨会话信号并标出重复项，让下一次会话能直接说"上次你也卡在这里"，
而不是从零开始。

信号词表在 `scripts/profile.py` 的 `SIGNALS`。**复用，不要自创**——
看到词表里没有的模式时，记进 `--note` 并说明缺哪个信号。

## 安装

`~/.agents/skills` 是多个 harness 共用的技能根，装一次三家同时生效：

```bash
cp -R . ~/.agents/skills/decision-review
```

| Harness | 读取的技能根 | 需要额外做什么 |
| --- | --- | --- |
| **pi** | `~/.agents/skills`、`~/.pi/agent/skills` | 无 |
| **Codex** | `~/.codex/skills` + `~/.agents/skills` | 无 |
| **dsh**（DeepSeek Harness） | `~/.dsh/skills` + `~/.agents/skills` | 无 |
| **opencode** | `~/.config/opencode/skills/`、`<repo>/.opencode/skills/` | 加符号链接 |
| **Claude Code** | `~/.claude/skills/` | 加符号链接 |

```bash
# opencode
mkdir -p ~/.config/opencode/skills
ln -s ~/.agents/skills/decision-review ~/.config/opencode/skills/decision-review

# Claude Code
ln -s ~/.agents/skills/decision-review ~/.claude/skills/decision-review
```

## 验证它是否有效

| 检查项 | 通过条件 |
| --- | --- |
| 一次一问 | 每个问题后停下等回答，不一连串问 |
| 先查再表态 | 给出立场前先读了本地可查的证据 |
| 出处被核查 | 至少有一条关键论断被追问"这是谁说的" |
| 前提被挑战 | 至少一条前提被标为未验证或直接被推翻 |
| 判据可证伪 | 有"观察到 X 说明方案 A 错了"这类的条目 |
| profile 被写入 | `.agents/profile.md` 有真实信号 |
| 没有滑向实施 | 全程没有开始写代码/改配置 |

### 已知的验证局限

本 skill 的锐度**部分来自执行者自己的上下文**（读过仓库文档、读过框架源码），
无法与 `SKILL.md` 本身的贡献分离。干净的对照需要一个新的、只拿到 SKILL.md 的会话。

## 出处

`references/decision-brief.md` 的格式提取自 gstack 的 `/office-hours`
（MIT, Garry Tan），原始文本见 `provenance/`。
gstack 的产品/市场诊断正文评估后未采用——见 `provenance/README.md`。

## License

MIT —— 见 [LICENSE](./LICENSE)。

`references/decision-brief.md` 与 `references/premises-and-evidence.md` 含派生自 gstack
（MIT, Copyright (c) 2026 Garry Tan）的内容，署名与许可证原文见
[THIRD-PARTY-NOTICES.md](./THIRD-PARTY-NOTICES.md)。
