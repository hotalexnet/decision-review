# decision-review

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Runtime: Python 3](https://img.shields.io/badge/runtime-python3-blue.svg)](https://www.python.org/)
[![Standard: Agent Skills](https://img.shields.io/badge/standard-agent--skills-2ea44f.svg)](https://agentskills.io/specification)
[![Scope: Investigation](https://img.shields.io/badge/scope-investigation-8957e5.svg)](#适用范围)

[**English**](./README.md) | **中文**

**审查一个决定，而不是替你做决定。**

一个给编码 agent 用的技能：审查那些**能靠调查收敛**的决定。它提取前提、核查出处、
给证据分级，最后交出可证伪的判据——而不是一个自信满满的推荐。

## 为什么需要它

你问 agent"我们该不该换平台？"，它会给你一个答案。这个答案通常很自信、通常听起来
合理、通常建立在**没有任何人验证过的前提**上。

失败模式不是推理错误，而是**跳过了前提提取**：agent 从它从未摆上台面的假设出发论证，
而用户看不出结论究竟挂在哪个假设上。

更糟的是，有些假设被记在了错误的地方。交接笔记里随口一句"数据库另建 PostgreSQL"，
被归档在客户原话旁边，一周后它就拥有了跟签字需求同等的效力，**静默覆盖了一份没人
记得写过的正式决策文档**。

这个技能就是为了抓这件事。它让 agent 停下来，说出前提，查清谁说了什么，
并在证据不足时**直说不确定**。

## 适用范围

边界是**问题靠什么收敛**，不是它属于哪个领域：

| | `decision-review` | 产品/市场验证 |
| --- | --- | --- |
| 问题 | 这个决定对不对 | 这件事值得做吗 |
| 收敛方式 | **调查** —— 读文档、查源码、问干系人、查数据 | **市场接触** —— 找用户、要钱、看留存 |
| 失败标志 | 前提从未被检验 | 没人愿意付钱 |

正因为边界是收敛方式，这个技能**不限于技术或架构**。同样适用于：

- 平台、供应商、框架选型
- 架构与迁移决策
- 接不接这个客户 / 要不要拒绝
- 自建 vs 采购 vs 自托管
- 流程与工作流变更
- 定价与合同取舍
- 招人还是外包

它**不适用**于产品/市场验证——那需要市场接触，不是调查。

## 四个机制

1. **提取前提** —— 这个决定要成立，必须有哪些事是真的？逐条标 `已验证` / `未验证` / `偏好`。
2. **核查出处** —— 谁说的、以什么身份、记在什么格式里？
3. **给证据分级** —— 廉价（必须先读）、昂贵（写明代价，不许猜）、没有（直说是偏好）。
4. **产出可证伪判据** —— 什么结果意味着什么，而不是一个推荐。

### 一次一问

问一个问题，然后停下等回答。

一次问三个，得到三个敷衍答案。一次问一个，沉默，第二或第三个回答才是真答案。
**这一条规则承担了大部分价值**——它正是为什么一次审查比一个推荐更慢，而且到达了
不同的地方。

### 证据分级

| 级别 | 例子 | 处理方式 |
| --- | --- | --- |
| **廉价** | 仓库文档、配置、源码、日志、数据、git 历史 | **给出任何立场前必须先读** |
| **昂贵** | 问干系人、要数据、跑实验、试用竞品 | 不许猜。标 `未验证`，写明获取代价 |
| **没有** | 品味、偏好 | 直说是偏好，不要包装成"架构" |

### 出处核查 —— 最容易被跳过的一步

出处核查不需要任何技术能力，**这恰恰是所有人都跳过它的原因**。最高危的组合是
**内部判断被记进了正式格式**——"客户要求"、"不可协商"、"原话"。

一旦这样记录，它就带上了外部约束的效力，而且没有人能看出它是怎么生效的。
标准动作：找出**已有的正式决策文档**，拿当前结论逐条比对，
**冲突时报告矛盾而不是替用户裁决**——说清哪两份文件互相矛盾、需要谁来定。

## 安装

`~/.agents/skills` 是多个 harness 共用的技能根，装一次全都生效：

```bash
git clone https://github.com/hotalexnet/decision-review.git ~/.agents/skills/decision-review
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

依赖：Python 3（仅标准库），以及 `git`（用于 profile 层）。

## 用法

任何在问"这个决定成不成立"的说法都会触发：

```
"我们是不是该换掉 X？"
"帮我看看这个决定对不对"
"这个判断有依据吗"
"Should we switch off X?"
```

一次审查的流程：

```
Phase 0  到底要拍的是什么决定？
Phase 1  读廉价证据。在这之前不发言。
Phase 2  核查出处。提取前提。
Phase 3  逐条确认前提，一次一条。          <- 价值最高的一道闸
Phase 4  2-3 个真正不同的方案 + 可证伪判据表
Phase 5  写决策文档
Phase 6  信号反思、一个具体动作、写 profile
```

每个决策点都以**决策简报**的形式发出——一段紧凑的 markdown，包含权衡的大白话解释、
明确的推荐、以及每个选项诚实的缺点：

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

如果 harness 提供结构化提问工具（dsh 的 `ask_user_question`、Claude Code 的
`AskUserQuestion`），简报会通过它投递；否则就是一条普通 markdown 消息，
用户打字的回答就是决定。

**排除一个选项从来不静默进行**——被排除的选项永远会被点名，并写明排除理由。

## 目录结构

```
SKILL.md                            骨架：四机制、证据规则、Phase 0-6
references/
  premises-and-evidence.md          前提提取、出处核查、证据分级、取位分寸
  decision-brief.md                 D<N> 简报格式、4 选项上限、排除项声明规则
  decision-doc-template.md          输出模板 + 质量自检
scripts/
  profile.py                        仓库内决策画像（read / summary / append）
provenance/                         借用的简报格式，留档为出处
```

`SKILL.md` 是唯一常驻加载的文件（约 175 行），references 按需加载。

## 记忆层

写在目标仓库的 `.agents/profile.md`，跟着代码走、跨 harness 可用。
它和任务检查点是互补关系，不是替代：

- **任务检查点**（如 [`repo-checkpoint`](https://github.com/hotalexnet/agent-checkpoint)）——*这个任务做到哪了*
- **决策画像** —— *这个人怎么决策，反复卡在哪*

```bash
python3 scripts/profile.py read      # Phase 1
python3 scripts/profile.py append --kind technical --signal unvalidated_premise --note "..."
python3 scripts/profile.py summary   # 跨会话聚合，标出重复项
```

```console
$ python3 scripts/profile.py summary
sessions recorded: 3

recurring signals (push here first):
  unvalidated_premise        2   <-- repeating
  action_over_analysis       2   <-- repeating
  domain_expertise           1
```

**重复项才是重点**：它让下一次会话能开口就说"上次你也卡在这里"，而不是从零开始。

信号词表在 `scripts/profile.py`。**复用，不要自创**——看到词表里没有的模式时，
记进 `--note` 并说明缺哪个信号。

## 验证它是否有效

| 检查项 | 通过条件 |
| --- | --- |
| 一次一问 | 每个问题后停下等回答 |
| 先有证据再有立场 | 表态前读过本地可查的证据 |
| 出处被核查 | 至少一条关键论断被追问"这是谁说的" |
| 前提被挑战 | 至少一条前提被标为未验证或被推翻 |
| 判据可证伪 | 有"观察到 X 说明方案 A 错了"这类的条目 |
| profile 被写入 | `.agents/profile.md` 有真实信号 |
| 没有滑向实施 | 全程没有开始写代码或改配置 |

### 已知的验证局限

一次审查有多锐利，部分取决于执行者自己的上下文——它读了多少仓库、有没有去查框架源码。
**这无法与 `SKILL.md` 自身的贡献分离。** 干净的对照需要一个全新的、只拿到 `SKILL.md`
的会话。

这个技能从一次真实会话中抽取而来，并完整跑通过一次——在一个平台选型决策上，
它通过读框架源码推翻了一条被当成事实的技术障碍。**请把上面那张验证表当作诚实的标准，
而不是把这句话当作承诺。**

## 出处

决策简报格式，以及部分取位与反谄媚规则，派生自 Garry Tan 的
[gstack](https://github.com/garrytan/gstack)（MIT）。逐文件的派生关系与完整许可证原文见
[THIRD-PARTY-NOTICES.md](./THIRD-PARTY-NOTICES.md)。

gstack 那个版本所属的产品/市场技能经过评估后**有意未采用**——它靠市场接触收敛，
是另一套机制。见 [`provenance/`](./provenance/README.md)。

## 许可证

MIT —— 见 [LICENSE](./LICENSE)。
