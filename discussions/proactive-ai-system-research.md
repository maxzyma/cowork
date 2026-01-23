# 主动型 AI 系统（Proactive AI）- 业界深度调研报告

**核心差异**：
- ❌ **传统 Agent**：用户问 → AI 答（被动响应 / Reactive）
- ✅ **主动型 AI**：AI 后台自动执行 → 主动推送消息给用户（主动驱动 / Proactive）

**应用场景**：企业培训业务

**调研目标**：针对"主动型 AI 系统"进行业界调研，重点关注**自主触发机制、推送模式、后台持续运行**

**调研日期**：2025-01-23

---

## 核心产品概念回顾

PRD 描述的产品核心特征：
1. **主动型 AI（核心）**：AI 后台自动执行任务，主动推送 proposal 给用户，而非被动等待指令
2. **长周期自驱动**：持续思考"接下来做什么"，日拱一卒
3. **Proposal-driven**：主动提出建议，获取授权，执行行动
4. **记忆驱动架构**：通过记忆的抽取和重组来驱动新的行动

### 与传统 Agent 的本质区别

| 维度 | 传统 Agent（被动 Reactive） | 主动型 AI 系统（Proactive） |
|------|------------------|----------------|
| **交互模式** | 用户问 → AI 答 | AI 主动推送 → 用户确认 |
| **触发方式** | 用户发起请求 | AI 自主判断时机 |
| **运行位置** | 前台等待 | 后台持续运行 |
| **任务来源** | 用户指令 | AI 自主规划 |
| **消息流向** | 用户 → AI | AI → 用户 |
| **执行模式** | On-demand（按需） | Continuous/Scheduled（持续/定时） |
| **典型例子** | ChatGPT, GitHub Copilot | 本系统（每日推送 proposal）、智能提醒助手 |

---

## 一、主动型 AI 触发机制调研

主动型 AI 的核心技术在于**"何时主动行动"**的判断机制。

### 1.1 触发机制类型

| 触发类型 | 核心逻辑 | 典型应用 | 技术实现 |
|---------|---------|---------|---------|
| **定时触发** | 按固定时间间隔执行 | 每日报告、定期检查 | Cron、Celery Beat |
| **事件触发** | 监测到特定事件时执行 | 监控告警、实时响应 | Event Queue、Webhooks |
| **条件触发** | 满足特定条件时执行 | 阈值告警、目标达成 | Rule Engine、状态机 |
| **推理触发** | AI 推断需要行动时执行 | 主动建议、预测性服务 | LLM + 决策逻辑 |
| **混合触发** | 结合多种触发条件 | 复杂业务场景 | 组合上述机制 |

### 1.2 PRD 需求的触发机制分析

**PRD 描述的场景**：
> "以稳定的频率（如每日一次），持续思考'接下来应该做什么'，向企业对接人递交新的 proposal"

这是 **定时触发 + 推理触发** 的混合模式：

```
定时触发（每日一次）
    ↓
AI 评估当前状态（检索记忆）
    ↓
推理判断是否需要行动（LLM 决策）
    ↓
生成 proposal（如果需要）
    ↓
推送消息给用户
```

### 1.3 关键技术挑战

**1. 时机判断**
- 问题：如何判断"现在是行动的好时机"？
- 方向：
  - 基于历史数据预测最佳时机
  - 避免打扰用户（工作时间、时区）
  - 考虑用户的活跃模式

**2. 触发频率控制**
- 问题：如何避免过于频繁或稀疏的推送？
- 方向：
  - 自适应频率调整
  - 用户反馈机制（太频繁/太少）
  - 重要性评分阈值

**3. 上下文保持**
- 问题：定时触发时如何保持连续性？
- 方向：
  - 分层记忆系统（MemGPT）
  - 状态持久化
  - 任务上下文恢复

---

## 二、推送型 AI 产品调研（Push-based AI）

虽然企业培训领域没有主动型 AI，但其他领域已有推送型产品的探索。

### 2.1 消费级产品

| 产品 | 推送模式 | 触发机制 | 学习点 |
|------|---------|---------|-------|
| **Google Assistant** | 主动建议 | 基于用户行为、日历、位置 | ✅ 时机判断成熟 |
| **Apple Siri** | 智能建议 | 系统事件、习惯学习 | ✅ 隐私保护模式 |
| **Amazon Alexa** | 日常提醒 | 定时 + 事件触发 | ✅ 语音交互 |
| **Notion AI** | 写作建议 | 用户输入时触发 | ⚠️ 仍是被动触发 |
| **Crystal (knows who you are)** | 性格分析建议 | 邮件/日历事件 | ✅ 主动推送洞察 |

### 2.2 企业级产品

| 产品 | 推送模式 | 触发机制 | 学习点 |
|------|---------|---------|-------|
| **Salesforce Einstein** | 销售机会提醒 | 数据变化触发 | ✅ 企业数据集成 |
| **Microsoft Copilot** | 代码建议 | 编码时触发 | ❌ 被动响应 |
| **Slackbot** | 工作提醒 | 定时 + 事件 | ✅ 企业消息推送 |
| **Datadog** | 监控告警 | 阈值触发 | ✅ 实时事件处理 |
| **PagerDuty** | 事件响应 | 告警触发 | ✅ 值班调度 |
| **Zoom AI Companion** | 会议总结 | 会议结束触发 | ⚠️ 事件触发，非主动规划 |

### 2.3 关键发现

✅ **技术可行性已被验证**
- 推送机制成熟（Web、Mobile、Email）
- 触发逻辑有成熟框架
- 企业级消息推送有标准方案

❌ **主动型 Agent 仍是空白**
- 大部分产品是"响应式"的
- 真正"自主规划并推送"的 AI 很少
- **"Proposal → 授权 → 执行"的完整闭环在消费/企业产品中都很少见**

---

## 三、事件驱动型 Agent 调研

### 3.1 事件驱动架构

**核心思想**：Agent 不是被动等待，而是监听事件流，在关键时刻主动行动。

**技术栈**：
- **消息队列**：Kafka、RabbitMQ、Redis Pub/Sub
- **事件总线**：AWS EventBridge、Google Cloud Events
- **Workflow**：Temporal、AWS Step Functions

### 3.2 事件驱动 Agent 框架

| 框架 | 事件处理能力 | 持续运行 | 适用场景 |
|------|------------|---------|---------|
| **LangChain Event Handlers** | ✅ 基础事件钩子 | ⚠️ 需自建 | 工具调用型 |
| **AutoGPT** | ✅ 任务完成事件 | ✅ 循环运行 | 复杂任务 |
| **BabyAGI** | ✅ 任务列表更新 | ✅ 持续循环 | 增量任务 |
| **CrewAI** | ✅ 多Agent事件 | ✅ 团队协作 | 协作场景 |
| **Microsoft Semantic Kernel** | ✅ 事件 Planner | ⚠️ 需自建 | 企业应用 |

### 3.3 最接近 PRD 的实现

**AutoGPT 的自主循环机制**：

```python
while not task_completed:
    # 1. 思考下一步
    thought = llm.decide_next_action(current_state, memory)

    # 2. 执行行动
    result = execute(thought.action)

    # 3. 存储记忆
    memory.store(result)

    # 4. 判断是否完成
    task_completed = llm.evaluate_completion(memory)
```

**与 PRD 的差异**：
- ✅ 共同点：持续循环、记忆驱动
- ⚠️ 差异点：AutoGPT 是"完成任务导向"，PRD 是"长期运营导向"
- ⚠️ 差异点：AutoGPT 无人类授权环节

---

## 四、定时任务与自主规划调研

### 4.1 定时任务系统

| 技术 | 适用场景 | 优势 | 劣势 |
|------|---------|------|------|
| **Linux Cron** | 简单定时任务 | 成熟稳定 | 无分布式、无状态管理 |
| **Celery Beat** | Python 异步任务 | 与 Celery 集成 | 需额外 Beat 进程 |
| **AWS EventBridge Scheduler** | 云端定时 | 高可用、托管 | AWS 绑定 |
| **Airflow** | 复杂工作流 | DAG 可视化 | 重型系统 |
| **Temporal** | 长期运行流程 | 状态持久化、可重试 | 学习曲线陡 |

### 4.2 自主规划系统（Autonomous Planning）

**学术界研究**：

| 论文/项目 | 年份 | 核心贡献 | 与 PRD 相关性 |
|----------|------|---------|--------------|
| **ReAct** | 2022 | 推理+行动交替 | ⭐⭐⭐⭐ 基础范式 |
| **Reflexion** | 2023 | 自我反思学习 | ⭐⭐⭐⭐ 记忆机制 |
| **Tree of Thoughts (ToT)** | 2023 | 树状搜索规划 | ⭐⭐⭐ 规划方法 |
| **Voyager (Minecraft Agent)** | 2023 | 长期自主探索 | ⭐⭐⭐⭐⭐ 最接近 |
| **AutoGPT** | 2023 | 自主任务分解 | ⭐⭐⭐⭐ 实现参考 |
| **BabyAGI** | 2023 | 增量任务管理 | ⭐⭐⭐⭐ 实现参考 |

### 4.3 最相关的案例：Voyager

**Voyager (2023)** - Minecraft 中的长期自主 Agent

核心特性：
1. **长期目标**：持续探索 Minecraft 世界
2. **自主学习**：积累技能库
3. **自主规划**：不断设定新子目标
4. **情景记忆**：记住所有探索经历

**与 PRD 的相似度**：⭐⭐⭐⭐⭐
- ✅ 都是长期运营
- ✅ 都需要自主规划"下一步做什么"
- ✅ 都依赖记忆积累

**差异**：
- Voyager 是游戏环境，PRD 是企业业务环境
- Voyager 无需人类授权，PRD 需要 HITL

---

## 五、Agent 框架的主动能力对比

### 5.1 对比表格（聚焦主动性）

| 框架 | 被动/主动 | 触发机制 | 推送能力 | 记忆系统 | 长期运行 | HITL 支持 |
|------|----------|---------|---------|---------|---------|-----------|
| **LangChain Agent** | 被动 | 用户请求 | ❌ | Memory Class | ⚠️ 需自建 | ✅ |
| **AutoGPT** | ✅ 主动 | 循环触发 | ⚠️ 仅日志 | ✅ 向量存储 | ✅ | ❌ |
| **BabyAGI** | ✅ 主动 | 任务列表驱动 | ⚠️ 仅日志 | ✅ 任务记忆 | ✅ | ❌ |
| **MemGPT** | ⚠️ 半主动 | 对话+记忆检索 | ❌ | ✅ 分层记忆 | ✅ | ✅ |
| **CrewAI** | ⚠️ 半主动 | 任务分配 | ❌ | ✅ 角色记忆 | ✅ | ✅ |
| **Microsoft AutoGen** | ⚠️ 半主动 | 对话触发 | ❌ | ⚠️ 对话历史 | ✅ | ✅ |
| **Clio** | ✅ 主动 | 任务启动时 | ✅ Proposal | ⚠️ 单次任务 | ❌ | ✅ |

### 5.2 核心发现

**现有框架的局限**：
1. ❌ 大多没有"主动推送消息给用户"的能力
2. ❌ 长期运行框架通常忽略 HITL（人类授权）
3. ❌ 没有框架实现"定时评估 + 推送 proposal"的模式

**PRD 需要自行构建的部分**：
- ✅ 推送系统（Web/Mobile/Email 通知）
- ✅ 定时调度器（Cron/Temporal）
- ✅ Proposal 展示与授权界面
- ✅ 结合 MemGPT 的记忆机制

---

## 六、通知系统技术调研

主动型 AI 系统需要可靠的消息推送能力。

### 6.1 推送渠道

| 渠道 | 适用场景 | 技术栈 | 实时性 |
|------|---------|--------|-------|
| **Web Push** | 桌面/移动浏览器 | Firebase Cloud Messaging, OneSignal | 高 |
| **移动推送** | 移动 App | APNs (iOS), FCM (Android) | 高 |
| **Email** | 正式通知 | SendGrid, AWS SES | 低 |
| **即时通讯** | 企业协作 | Slack Webhook, Teams Bot | 高 |
| **短信** | 紧急通知 | Twilio, AWS SNS | 高 |

### 6.2 企业级通知最佳实践

**时机控制**：
- 避免非工作时间打扰
- 智能聚合相似通知
- 用户可配置推送偏好

**内容设计**：
- 清晰的行动号召（CTA）
- 简洁的 proposal 描述
- 一键接受/拒绝/修改

**状态管理**：
- 通知送达确认
- 用户响应跟踪
- 失败重试机制

---

## 七、记忆驱动架构深度调研

### 7.1 MemGPT 的分层记忆设计

**核心论文**：《MemGPT: Towards LLMs as Operating Systems》(2023)

**架构图示**：
```
┌─────────────────────────────────────┐
│         LLM (Context Window)         │ ← 主内存 (RAM)
│    - Limited capacity (e.g., 128K)   │
│    - Fast access                     │
└─────────────────────────────────────┘
              ↕
    ┌─────────────────────┐
    │  Memory Controller  │ ← 自动管理读写
    └─────────────────────┘
              ↕
┌─────────────────────────────────────┐
│      Vector Database (外存/HDD)       │ ← 外存
│    - Unlimited capacity              │
│    - Semantic search                 │
│    - Episodic + Semantic memory      │
└─────────────────────────────────────┘
```

**关键机制**：
1. **虚拟上下文**：让 LLM 感知上下文无限大
2. **内存控制器**：智能决定读什么、写什么、何时刷新
3. **中断机制**：当重要信息超出容量时，暂停并请求加载

**与 PRD 的关联**：
- ✅ 解决了"长周期运行的上下文管理"问题
- ✅ 提供了"记忆驱动行动"的技术基础
- ⚠️ 需要结合定时触发机制

### 7.2 记忆触发机制

**关键问题**：如何让记忆"主动"驱动新的行动？

**方案 A：定期记忆反思（Reflexion 模式）**
```python
def daily_reflection():
    # 1. 检索最近的记忆
    recent_memories = memory.retrieve(last_24_hours)

    # 2. 反思总结
    insights = llm.reflect(recent_memories)

    # 3. 生成新的 proposal
    proposals = llm.generate_proposals(insights, goals)

    return proposals
```

**方案 B：重要性驱动触发**
```python
def on_memory_store(event):
    # 1. 评估事件重要性
    importance = llm.evaluate_importance(event)

    # 2. 如果重要，触发 proposal 生成
    if importance > threshold:
        proposal = generate_proposal_based_on(event)
        notify_user(proposal)
```

**方案 C：混合模式（推荐）**
- 定时触发（每日）+ 事件触发（重要事件时）
- 日常：定期反思生成 proposal
- 紧急：重要事件立即触发

---

## 八、技术实现路径

### 8.1 系统架构设计

```
┌─────────────────────────────────────────────────┐
│                 前端界面                         │
│   - Proposal 展示                               │
│   - 用户授权交互                                 │
└─────────────────────────────────────────────────┘
                      ↕ (WebSocket/Web Polling)
┌─────────────────────────────────────────────────┐
│              API 服务层                          │
│   - REST / GraphQL API                          │
│   - WebSocket 推送                              │
└─────────────────────────────────────────────────┘
                      ↕
┌─────────────────────────────────────────────────┐
│            主动型 AI Engine                     │
│   ┌─────────────────────────────────────────┐  │
│   │   调度器 (Scheduler)                    │  │
│   │   - 定时任务触发                         │  │
│   │   - 事件监听                             │  │
│   └─────────────────────────────────────────┘  │
│                      ↓                          │
│   ┌─────────────────────────────────────────┐  │
│   │   Proposal Generator                    │  │
│   │   - 记忆检索                             │  │
│   │   - LLM 推理                             │  │
│   │   - 生成建议                             │  │
│   └─────────────────────────────────────────┘  │
│                      ↓                          │
│   ┌─────────────────────────────────────────┐  │
│   │   记忆系统 (Memory System)              │  │
│   │   - MemGPT 架构                         │  │
│   │   - 向量数据库                           │  │
│   │   - 记忆控制器                           │  │
│   └─────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                      ↕
┌─────────────────────────────────────────────────┐
│              基础设施层                          │
│   - 向量数据库 (Pinecone/Weaviate)              │
│   - 消息队列 (Redis/RabbitMQ)                   │
│   - 任务队列 (Celery/Temporal)                  │
└─────────────────────────────────────────────────┘
```

### 8.2 核心流程实现

**每日提案流程**：
```python
class ProactiveAISystem:
    def __init__(self):
        self.memory = MemGPTMemorySystem()
        self.llm = OpenAI()  # or Claude
        self.scheduler = TemporalScheduler()
        self.notification = NotificationService()

    def start(self):
        # 注册每日任务
        self.scheduler.schedule_daily(
            func=self.daily_proposal_cycle,
            time="09:00",  # 上午 9 点
            timezone=user.timezone
        )

    def daily_proposal_cycle(self, user_id):
        # 1. 检索记忆
        context = self.memory.construct_context(
            user_id=user_id,
            include_recent=True,
            include_goals=True,
            include_history=True
        )

        # 2. 生成提案
        proposals = self.llm.generate_proposals(
            system_prompt=SYSTEM_PROMPT,
            context=context,
            num_proposals=3
        )

        # 3. 推送消息
        self.notification.send_proposals(
            user_id=user_id,
            proposals=proposals,
            channels=["web", "email"]
        )

        # 4. 等待用户响应
        # (通过 API 异步处理)
```

**Proposal 生成 Prompt 示例**：
```
你是一位主动型的企业培训顾问 AI。

【当前状态】
{current_state}

【企业目标】
{goals}

【历史行动与结果】
{history}

【最近的重要事件】
{recent_events}

【任务】
基于以上信息，思考接下来应该做什么来推动企业培训体系的建立。

请生成 3-5 个具体的 proposal，每个包含：
1. 标题
2. 理由（为什么现在要做）
3. 具体行动步骤
4. 预期结果

要求：
- 考虑当前业务阶段
- 避免重复已完成的行动
- 优先考虑高价值、低门槛的行动
```

### 8.3 技术栈推荐

| 组件 | 推荐技术 | 理由 |
|------|---------|------|
| **LLM** | Claude 3.5 Sonnet / GPT-4o | 强推理能力，长上下文 |
| **记忆架构** | MemGPT (开源) | 最接近 PRD，分层记忆 |
| **向量数据库** | Pinecone / Weaviate | 成熟稳定，性能好 |
| **任务调度** | Temporal | 长期运行流程，状态持久化 |
| **消息推送** | OneSignal / Firebase | 多渠道推送 |
| **API 框架** | FastAPI | 高性能，易用 |
| **前端** | React / shadcn/ui | 快速构建 UI |

---

## 九、竞品分析（聚焦主动性）

### 9.1 AI Agent 产品主动性评估

| 产品 | 主动性等级 | 推送机制 | 触发方式 | 缺失能力 |
|------|-----------|---------|---------|---------|
| **ChatGPT** | ❌ 完全被动 | 无 | 用户输入 | 无主动性 |
| **GitHub Copilot** | ❌ 完全被动 | 无 | 用户编码 | 无主动性 |
| **Perplexity AI** | ❌ 完全被动 | 无 | 用户搜索 | 无主动性 |
| **Claude** | ❌ 完全被动 | 无 | 用户输入 | 无主动性 |
| **AutoGPT** | ✅ 强主动 | ⚠️ 仅日志 | 循环触发 | 无用户交互 |
| **Devin (软件工程)** | ⚠️ 半主动 | ✅ 任务更新 | 人类分配 | 非自主规划 |
| **Crystal** | ✅ 主动 | ✅ 邮件推送 | 邮件事件 | 单一触发源 |
| **Google Assistant** | ✅ 主动 | ✅ 通知推送 | 行为/位置/时间 | 非长周期运营 |

### 9.2 关键空白点

**❌ 未发现竞品实现**：
1. **长周期运营 + 主动推送 + HITL** 的三合一
2. **记忆驱动的定时提案生成**
3. **企业服务场景的主动型 AI**
4. **"AI 即 COE" 的自主服务模式**

---

## 十、潜在风险与挑战

### 10.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| **记忆不一致** | 长期运行中记忆冲突 | 实现记忆冲突检测 |
| **目标漂移** | 偏离初始业务目标 | 定期目标对齐检查 |
| **推送疲劳** | 用户反感过度推送 | 自适应频率 + 用户反馈 |
| **误触发** | 不合时宜的推送 | 时机预测 + 用户习惯学习 |
| **上下文丢失** | 任务状态丢失 | 状态持久化 |

### 10.2 用户接受度风险

| 挑战 | 建议 |
|------|------|
| **对 AI 不信任** | 每个 proposal 附带理由和预期结果 |
| **担心失控** | 提供清晰的授权机制和撤销能力 |
| **打扰工作** | 智能时机选择 + 用户偏好配置 |
| **黑盒焦虑** | 可解释性：展示 AI 的思考过程 |

---

## 十一、关键论文与资源

### 11.1 必读论文（聚焦主动性）

| 论文 | 年份 | 核心贡献 | 相关性 |
|------|------|---------|-------|
| **MemGPT: Towards LLMs as Operating Systems** | 2023 | 分层记忆、虚拟上下文 | ⭐⭐⭐⭐⭐ |
| **Voyager: An Open-Ended Embodied Agent** | 2023 | 长期自主探索、技能积累 | ⭐⭐⭐⭐⭐ |
| **Reflexion: Language Agents with Verbal Reinforcement Learning** | 2023 | 自我反思、记忆学习 | ⭐⭐⭐⭐ |
| **Clio: A Proposal-Driven Assistant** | 2023 | Proposal-driven 交互 | ⭐⭐⭐⭐ |
| **ReAct: Synergizing Reasoning and Acting** | 2022 | 推理-行动循环 | ⭐⭐⭐⭐ |
| **Tree of Thoughts** | 2023 | 规划与搜索 | ⭐⭐⭐ |

### 11.2 开源项目

| 项目 | GitHub | 学习点 |
|------|--------|-------|
| **MemGPT** | https://github.com/cpacker/MemGPT | 分层记忆实现 |
| **AutoGPT** | https://github.com/Significant-Gravitas/AutoGPT | 自主循环机制 |
| **BabyAGI** | https://github.com/yoheinakajima/babyagi | 任务列表管理 |
| **Voyager** | https://github.com/MineDojo/Voyager | 长期探索 Agent |
| **Temporal** | https://github.com/temporalio/sdk-python | 长期运行工作流 |

### 11.3 技术博客

- **Lilian Weng - AI Agent**: https://lilianweng.github.io/posts/2023-06-23-agent/
- **Andrew Ng - Agentic Workflows**: DeepLearning.AI
- **MemGPT Blog**: https://memgpt.ai/blog

---

## 十二、结论与建议

### 12.1 调研结论

**✅ 技术可行性高**
- MemGPT 证明分层记忆架构可行
- AutoGPT/Voyager 证明长期自主 Agent 可行
- 推送系统技术成熟

**✅ 市场空白明显**
- 企业服务领域无主动型 AI 产品
- "记忆驱动 + 定时提案 + HITL" 组合无先例
- 从 Copilot 到 Autopilot 的演进处于早期

**✅ 创新空间大**
- 范式创新：从被动响应到主动推送
- 架构创新：记忆驱动的自运行系统
- 模式创新：AI 即 COE

### 12.2 建议的下一步

**Phase 1: 技术验证（4 周）**
1. 搭建 MemGPT 原型
2. 实现定时触发机制
3. 构建 Proposal 生成流程
4. 集成推送系统

**Phase 2: 用户研究（6 周）**
1. 访谈 10-20 家企业
2. 验证"主动型 AI"接受度
3. 测试推送频率偏好
4. 收集 Proposal 质量反馈

**Phase 3: MVP 开发（8 周）**
1. 实现 L0 使命规划层
2. 完成授权交互界面
3. 部署监控与日志系统
4. 邀请种子用户试用

### 12.3 核心差异化主张

**"从 Copilot 到 Autopilot 的范式转变"**

传统 AI 助手：
- 你问，我答
- 你需要时，我出现

主动型 AI 系统：
- 我思考，我提案
- 我持续为你创造价值

---

**报告生成时间**：2025-01-23
**核心聚焦**：主动型 AI 系统（Proactive AI System）
**关键维度**：自主触发、推送机制、记忆驱动、长周期运行
**调研局限**：网络工具限额，基于 2025-01 前知识库
