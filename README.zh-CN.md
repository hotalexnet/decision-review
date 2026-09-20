# decision-review

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Runtime: Python 3](https://img.shields.io/badge/runtime-python3-blue.svg)](https://www.python.org/)
[![Standard: Agent Skills](https://img.shields.io/badge/standard-agent--skills-2ea44f.svg)](https://agentskills.io/specification)
[![Scope: Investigation](https://img.shields.io/badge/scope-investigation-8957e5.svg)](#适用范围)

[**English**](./README.md) | **中文**

**审查一个决定，而不是替你做决定。**

给编码 agent 装的一个技能。凡是能靠查资料查清楚的决定，它都会逼你把前提、出处、
证据摆到台面上，最后给一份可证伪的判据，而不是一个听着挺有道理的结论。

## 它治什么毛病

你问 agent"该不该换平台"，它一定会给答案。答案通常很自信，通常也自洽。
**问题是它的前提，没有人验过。**

毛病不在推理，在于 agent 从没说出口的假设出发论证，而你看不出结论到底压在哪个假设上。

更难防的是假设记错了地方。交接笔记里随手一句"数据库另建 PostgreSQL"，被归档在客户原话
旁边；过了一周，它就有了跟签字需求同等的分量，把一份没人记得的正式决策文档悄悄废掉了。

这个技能就是治这个：让 agent 停下来，把前提摆出来，查清谁说了什么，证据不够就直说不够。

## 适用范围

分界线是**问题靠什么解决**，不是它属于哪个领域。

| | `decision-review` | 产品/市场验证 |
| --- | --- | --- |
| 问题 | 这个决定对不对 | 这件事值得做吗 |
| 怎么解决 | **查**：读文档、翻源码、问干系人、看数据 | **找人**：找用户、收钱、看留存 |
| 什么时候算失败 | 前提一直没被检验 | 没人愿意付钱 |

因为分界线是解决方式，所以它**不局限于技术**。这些都能用：

- 平台、供应商、框架选型
- 架构改造、系统迁移
- 接不接这个客户，要不要拒
- 自建、买、还是自托管
- 流程改动
- 定价和合同的取舍
- 招人还是外包

**产品/市场验证用不了**，那得靠找人，不是靠查。

## 四个机制

1. **把前提挖出来**：这个决定要成立，必须有哪些事是真的？逐条标"已验证""未验证""只是偏好"。
2. **查出处**：这话谁说的？以什么身份？记在哪儿？
3. **给证据分级**：能查的必须先查；查不了的不许猜；纯偏好就直说是偏好。
4. **给可证伪的判据**：什么结果说明什么，而不是给一个推荐。

### 一次只问一个

问完就停，等回答。

一口气问三个，会拿到三个敷衍的答案；问一个，闭嘴等着，第二遍或第三遍回答才是真的。
**这条规矩值一半的分**，也正是它让一次审查比一个推荐慢，但结论落在完全不同的地方。

### 证据分三级

| 级别 | 例子 | 怎么办 |
| --- | --- | --- |
| **能查的** | 仓库文档、配置、源码、日志、数据、提交历史 | **表态之前必须查完** |
| **查不了的** | 问干系人、要数据、做实验、试竞品 | 不许猜。标"未验证"，并写明查清它要花多少代价 |
| **压根没有** | 口味、偏好 | 直说是偏好，别包装成"架构" |

### 查出处：最容易漏的一步

查出处不需要任何技术能力，所以所有人都不做。最危险的情况是**把内部判断记进了正式格式**：
"客户要求"、"不可协商"、"原话"。

这么一记，它就有了外部约束的分量，而且没人看得出来它是怎么生效的。

标准动作：找出**已有的正式决策文档**，跟当前结论逐条对。对不上就**报告矛盾，
别替用户裁决**，而是说清哪两份文件打架、该谁定。

## 安装

`~/.agents/skills` 是几个 harness 共用的技能根，装一次全都认：

```bash
git clone https://github.com/hotalexnet/decision-review.git ~/.agents/skills/decision-review
```

| Harness | 认哪个目录 | 还要做什么 |
| --- | --- | --- |
| **pi** | `~/.agents/skills`、`~/.pi/agent/skills` | 不用 |
| **Codex** | `~/.codex/skills` + `~/.agents/skills` | 不用 |
| **dsh**（DeepSeek Harness） | `~/.dsh/skills` + `~/.agents/skills` | 不用 |
| **opencode** | `~/.config/opencode/skills/`、`<repo>/.opencode/skills/` | 建个软链 |
| **Claude Code** | `~/.claude/skills/` | 建个软链 |

```bash
# opencode
mkdir -p ~/.config/opencode/skills
ln -s ~/.agents/skills/decision-review ~/.config/opencode/skills/decision-review

# Claude Code
ln -s ~/.agents/skills/decision-review ~/.claude/skills/decision-review
```

依赖只有 Python 3（只用标准库）和 `git`（记忆层要用）。

## 怎么用

只要是在问"这个决定成不成立"，都会触发：

```
"我们是不是该换掉 X？"
"帮我看看这个决定对不对"
"这个判断有依据吗"
"Should we switch off X?"
```

一次审查走下来是这样：

```
Phase 0  到底要拍的是什么决定？
Phase 1  把能查的证据先查了。这之前不表态。
Phase 2  查出处。把前提挖出来。
Phase 3  逐条确认前提，一次一条。          <- 价值最高的一关
Phase 4  给 2-3 个真不一样的方案 + 可证伪判据表
Phase 5  写决策文档
Phase 6  信号反思、一个具体动作、写 profile
```

每个决策点都以**决策简报**的形式发出，是一段紧凑的 markdown：把权衡用大白话讲清楚，
给出明确推荐，每个选项都要写出诚实的缺点。

```
D2 — 用什么最少的代价，验证这个交界是不是真问题？

ELI10: ...

Stakes if wrong: ...

Recommendation: B because ...

Completeness: A=4/10, B=9/10

A) 先评估竞品平台  (recommended)
   ✅ ...
   ❌ ...
B) 先写平台中立的领域模型，再做原型
   ✅ ...
   ❌ ...

Net: ...
```

如果 harness 有结构化提问工具（dsh 的 `ask_user_question`、Claude Code 的
`AskUserQuestion`），简报就通过它发；没有就发一条普通 markdown 消息，用户打字回答，
那个回答就是决定。

**排除一个选项从来不会悄悄进行**，一定点名，并写明为什么排除。

## 目录结构

```
SKILL.md                            骨架：四机制、证据规则、Phase 0-6
references/
  premises-and-evidence.md          前提怎么挖、出处怎么查、证据怎么分级、立场怎么取
  decision-brief.md                 D<N> 简报格式、4 选项上限、排除项要声明
  decision-doc-template.md          输出模板 + 质量自检
scripts/
  profile.py                        仓库内的决策画像（read / summary / append）
provenance/                         借来的简报格式，留档可查
```

常驻加载的只有 `SKILL.md`（约 175 行），references 用到才读。

## 记忆层

写在目标仓库的 `.agents/profile.md`，跟着代码走，换 harness 也还在。
它和任务检查点是两回事，互补：

- **任务检查点**（比如 [`repo-checkpoint`](https://github.com/hotalexnet/agent-checkpoint)）：*这个任务做到哪了*
- **决策画像**：*这个人怎么决策，老卡在哪*

```bash
python3 scripts/profile.py read      # Phase 1 读
python3 scripts/profile.py append --kind technical --signal unvalidated_premise --note "..."
python3 scripts/profile.py summary   # 跨会话汇总，重复的会标出来
```

```console
$ python3 scripts/profile.py summary
sessions recorded: 3

recurring signals (push here first):
  unvalidated_premise        2   <-- repeating
  action_over_analysis       2   <-- repeating
  domain_expertise           1
```

**重点是那些重复的**。有了它，下次会话一开口就能说"上次你也卡在这儿"，
不用从零开始。

信号词表在 `scripts/profile.py` 里。**照着用，别自己造**。真碰到词表里没有的模式，
写进 `--note` 里并说明缺哪个信号。

## 怎么算跑对了

| 检查 | 什么样才算过 |
| --- | --- |
| 一次只问一个 | 每个问题后面停下来等回答 |
| 先有证据再表态 | 表态之前读过本地能查的东西 |
| 查了出处 | 至少有一条关键说法被追问过"这是谁说的" |
| 挑战了前提 | 至少有一条前提被标成未验证，或者被推翻 |
| 判据可证伪 | 有"看到 X 就说明方案 A 错了"这类条目 |
| 写了 profile | `.agents/profile.md` 里有真信号 |
| 没滑去做实现 | 全程没开始写代码或改配置 |

### 有一件事我验不了

一次审查到底有多管用，很大程度上取决于**执行它的 agent 手上已经有多少上下文**：
它读了多少仓库、有没有真去翻框架源码。**这一部分没法跟 `SKILL.md` 本身的贡献分开算。**
要干净地比，得开一个全新的会话，只给它一个 `SKILL.md`。

这个技能是从一次真实会话里拆出来的，完整跑通过一次：在一个平台选型决策上，
它翻了框架源码，推翻了一条被当成事实的技术障碍。

**上面那张表才是可信的门槛，这句话不是承诺。**

## 出处

决策简报的格式，以及一部分表态分寸和反谄媚的规则，来自 Garry Tan 的
[gstack](https://github.com/garrytan/gstack)（MIT）。哪个文件派生自哪里、完整的许可证原文，
都在 [THIRD-PARTY-NOTICES.md](./THIRD-PARTY-NOTICES.md)。

gstack 里那个原版是产品/市场技能，评估之后**有意没有搬过来**，它靠找人解决，
是另一套机制。见 [`provenance/`](./provenance/README.md)。

## 许可证

MIT，见 [LICENSE](./LICENSE)。
