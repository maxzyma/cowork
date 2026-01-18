# AI Agent 上下文工程：术语定义与架构框架

**文档版本：** v1.0
**创建日期：** 2025-01-12
**状态：** 定义规范

---

## 文档说明

本文档明确定义 AI Agent 系统中的核心工程术语，建立清晰的术语体系，以指导系统设计、技术选型和团队协作。

**⚠️ 重要声明：**
本文档中的"记忆工程"、"知识工程"、"上下文工程"等术语是基于 LLM 时代技术实践的现代定义，**不同于** 80年代专家系统时代的传统含义。详见下文"术语演变"章节。

---

## 目录

1. [术语演变与定义原则](#一术语演变与定义原则)
2. [Context Engineering（上下文工程）](#二context-engineering上下文工程)
3. [Memory Engineering（记忆工程）](#三memory-engineering记忆工程)
4. [Knowledge Engineering（知识工程）](#四knowledge-engineering知识工程)
5. [三层架构关系](#五三层架构关系)
6. [实施指导](#六实施指导)
7. [业界对照表](#七业界对照表)

---

## 一、术语演变与定义原则

### 1.1 术语演变历程

```
┌─────────────────────────────────────────────────────────────┐
│  术语演变：从传统到现代                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  【1980s：专家系统时代】                                     │
│  Knowledge Engineering (传统)                                │
│    ├─ 定义：人工构建专家规则系统                            │
│    ├─ 技术：if-then规则、专家系统、知识库                   │
│    ├─ 典型：MYCIN、DENDRAL                                  │
│    └─ 局限：手工维护、难以扩展、缺乏学习能力                 │
│                                                              │
│  【2010s：深度学习时代】                                     │
│  ❌ "Knowledge Engineering" 术语衰落                         │
│    ├─ 原因：深度学习end-to-end范式兴起                      │
│    ├─ 趋势：从知识驱动转向数据驱动                          │
│    └─ 结果：术语几乎消失                                    │
│                                                              │
│  【2020s：LLM + Agent 时代】                                │
│  ✅ "X Engineering" 术语复兴（新定义）                       │
│    ├─ Context Engineering：上下文管理与优化                 │
│    ├─ Memory Engineering：记忆系统的工程化构建              │
│    ├─ Knowledge Engineering：知识图谱的工程化构建           │
│    └─ 本质：从手工规则 → 智能系统设计                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 现代定义的核心原则

**本术语体系遵循以下原则：**

1. **工程化导向**
   - 不是算法研究，而是系统构建
   - 关注可扩展性、可维护性、可靠性
   - 强调设计模式、最佳实践、技术选型

2. **层次化架构**
   - Context Engineering = 总体架构层
   - Memory Engineering = 子系统（记忆）
   - Knowledge Engineering = 子系统（知识）

3. **技术栈明确**
   - 每个领域有清晰的技术边界
   - 有主流工具/框架支撑
   - 可独立实施和迭代

4. **与业界兼容**
   - 尊重现有主流术语（RAG、Knowledge Graph等）
   - 提供清晰的映射关系
   - 便于对外沟通和协作

### 1.3 术语使用规范

| 术语 | 使用场景 | 定义来源 |
|------|---------|---------|
| **Context Engineering** | 本文档 | 现代定义（2025） |
| **Memory Engineering** | 本文档 | 现代定义（2025） |
| **Knowledge Engineering** | 本文档 | 现代定义（2025） |
| **Knowledge Engineering（传统）** | 学术历史引用 | 1980s定义 |
| **RAG** | 业界通用 | 检索增强生成（2023+） |
| **Knowledge Graph** | 业界通用 | 知识图谱（2010+） |
| **Memory Systems** | 业界通用 | 记忆系统（2024+） |

**使用建议：**
- ✅ 内部技术文档：使用本文档术语（明确定义）
- ✅ 技术方案设计：使用本文档术语 + 业界对照
- ⚠️ 对外发布/论文：优先使用业界通用术语，本文档术语作为补充说明

---

## 二、Context Engineering（上下文工程）

### 2.1 定义

**Context Engineering（上下文工程）** 是指在 LLM 应用中，**系统化地管理、优化和传递上下文信息**，以提升模型输出质量和用户体验的工程化实践。

**核心问题：**
- 如何在有限的上下文窗口内传递最有效的信息？
- 如何平衡外部知识、用户记忆、实时信息？
- 如何实现个性化的上下文构建？
- 如何动态调整上下文策略？

### 2.2 职责范畴

```
┌─────────────────────────────────────────────────────────────┐
│  Context Engineering 职责范围                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  【1. 上下文构建】                                           │
│    ├─ 信息源选择：RAG、Memory、KG、实时API                  │
│    ├─ 信息融合：多源信息的整合与排序                         │
│    ├─ 长度控制：Token预算分配                               │
│    └─ 结构化：Prompt模板设计、系统提示词优化                 │
│                                                              │
│  【2. 上下文优化】                                           │
│    ├─ 重排序：Re-rank算法提升相关性                         │
│    ├─ 压缩：信息浓缩、摘要生成                               │
│    ├─ 去重：消除冗余信息                                     │
│    └─ 个性化：基于用户画像调整上下文                        │
│                                                              │
│  【3. 上下文管理】                                           │
│    ├─ 会话管理：多轮对话的上下文延续                         │
│    ├─ 状态跟踪：对话状态的维护                               │
│    ├─ 滑动窗口：长对话的上下文裁剪                           │
│    └─ 优先级：关键信息vs次要信息的区分                       │
│                                                              │
│  【4. 上下文评估】                                           │
│    ├─ 质量度量：上下文相关性、完整性                         │
│    ├─ 效果评估：对模型输出的影响                             │
│    ├─ A/B测试：不同策略的对比                               │
│    └─ 监控指标：Token使用、响应延迟、用户满意度             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 技术栈

#### 上下文构建层

| 技术组件 | 主流工具 | 作用 |
|---------|---------|------|
| **RAG集成** | LangChain RAG, LlamaIndex | 外部知识检索 |
| **Memory集成** | LangGraph Checkpointer, Mem0 | 用户记忆管理 |
| **Knowledge Graph** | GraphRAG, Neo4j | 知识图谱推理 |
| **Prompt模板** | Jinja2, PromptTemplate | 结构化上下文 |
| **Token管理** | Tiktoken, custom utils | 长度控制 |

#### 上下文优化层

| 技术组件 | 主流工具 | 作用 |
|---------|---------|------|
| **重排序** | Cohere Rerank, BGE-Reranker | 结果重排序 |
| **压缩** | LLMLingua, context compression | 信息浓缩 |
| **去重** | MinHash, SimHash | 冗余检测 |
| **个性化** | Custom ranking models | 用户适配 |

### 2.4 设计原则

**1. Token预算意识**
```python
# 示例：分配上下文窗口的Token预算
CONTEXT_WINDOW = 128000  # GPT-4-turbo

budget_allocation = {
    "system_prompt": 500,        # 0.4%
    "user_query": 1000,          # 0.8%
    "external_knowledge": 40000, # 31%
    "user_memory": 20000,        # 16%
    "knowledge_graph": 30000,    # 23%
    "conversation_history": 30000,# 23%
    "buffer": 6500               # 5%
}
```

**2. 信息质量优先**
```
质量评估维度：
• 相关性：与查询的语义关联度
• 准确性：信息的可信度（来源权威性）
• 时效性：信息的新鲜度（时间戳）
• 完整性：信息的完整程度
• 多样性：信息来源的多样性
```

**3. 动态调整策略**
```python
# 根据查询类型动态调整上下文策略
def get_context_strategy(query_type: str) -> dict:
    strategies = {
        "product_inquiry": {
            "external_knowledge": 0.6,  # 产品文档优先
            "user_memory": 0.2,
            "knowledge_graph": 0.2
        },
        "personalized_recommendation": {
            "external_knowledge": 0.2,
            "user_memory": 0.5,        # 用户历史优先
            "knowledge_graph": 0.3
        },
        "technical_support": {
            "external_knowledge": 0.5,
            "user_memory": 0.3,        # 考虑用户技能水平
            "knowledge_graph": 0.2
        }
    }
    return strategies.get(query_type, strategies["product_inquiry"])
```

### 2.5 典型流程

```python
async def context_engineering_pipeline(
    user_query: str,
    user_id: str,
    conversation_history: list
) -> str:
    """
    上下文工程流程
    """

    # ═══════════════════════════════════════════════
    # Phase 1: 并行检索
    # ═══════════════════════════════════════════════
    external_knowledge = await rag_retrieve(user_query)
    user_memories = await memory_retrieve(user_id, user_query)
    graph_insights = await kg_query(user_id, user_query)

    # ═══════════════════════════════════════════════
    # Phase 2: 上下文融合
    # ═══════════════════════════════════════════════

    # 2.1 个性化重排序
    ranked_knowledge = personalize_rerank(
        external_knowledge,
        user_profile={memories, graph_insights}
    )

    # 2.2 去重
    deduplicated = deduplicate_contexts(
        ranked_knowledge,
        user_memories,
        graph_insights
    )

    # 2.3 Token预算分配
    allocated = allocate_token_budget(
        deduplicated,
        budget=get_budget_by_query_type(user_query)
    )

    # 2.4 构建结构化上下文
    context = build_structured_context(
        system_prompt=get_system_prompt(),
        user_query=user_query,
        external_knowledge=allocated["knowledge"],
        user_memories=allocated["memory"],
        knowledge_graph=allocated["graph"],
        conversation_history=conversation_history
    )

    # ═══════════════════════════════════════════════
    # Phase 3: 质量检查
    # ═══════════════════════════════════════════════

    quality_score = evaluate_context_quality(context)
    if quality_score < 0.7:
        # 触发降级策略
        context = apply_fallback_strategy(context)

    return context
```

### 2.6 关键指标

| 指标类别 | 具体指标 | 目标值 |
|---------|---------|--------|
| **效率** | 平均上下文Token数 | < 50K |
| **效率** | 上下文构建延迟 | < 500ms |
| **质量** | 上下文相关性得分 | > 0.8 |
| **质量** | 用户满意度 | > 4.5/5 |
| **效果** | 任务完成率 | > 90% |
| **效果** | 消退率（用户放弃） | < 5% |

---

## 三、Memory Engineering（记忆工程）

### 3.1 定义

**Memory Engineering（记忆工程）** 是指在 AI Agent 系统中，**工程化地设计、实现和管理记忆子系统**，使 Agent 能够持久化、检索、更新和演化记忆信息的工程实践。

**与传统"记忆系统"的区别：**
- 传统"记忆系统" = 存储和检索的技术
- 记忆工程 = 系统化的工程实践（设计、实现、运维、优化）

**核心问题：**
- 如何设计层次化的记忆架构？
- 如何实现记忆的巩固和遗忘？
- 如何平衡记忆的存储成本和检索效率？
- 如何保证记忆的一致性和可靠性？

### 3.2 记忆架构分层

```
┌─────────────────────────────────────────────────────────────┐
│  Memory Engineering：层次化架构                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  【Layer 1: Working Memory / 工作记忆】                      │
│    ├─ 生命周期：当前对话                                     │
│    ├─ 容量：有限（~8K-32K tokens）                          │
│    ├─ 技术：LLM Context Window                              │
│    ├─ 操作：                                                 │
│    │   • 保持对话上下文                                      │
│    │   • 短期信息暂存                                        │
│    │   • 快速读写                                            │
│    └─ 例子：用户刚才问了什么、当前讨论的话题                 │
│                                                              │
│  【Layer 2: Short-term Memory / 短期记忆】                   │
│    ├─ 生命周期：几小时到几天                                 │
│    ├─ 容量：中等（~1M-10M tokens/user）                     │
│    ├─ 技术：Redis, PostgreSQL, LangGraph Checkpointer       │
│    ├─ 操作：                                                 │
│    │   • 对话状态持久化                                      │
│    │   • 近期交互记录                                        │
│    │   • 快速检索                                            │
│    │   • 定期清理/归档                                       │
│    └─ 例子：用户今天早上的对话、本周的学习进度               │
│                                                              │
│  【Layer 3: Long-term Memory / 长期记忆】                    │
│    ├─ 生命周期：永久                                         │
│    ├─ 容量：无限                                             │
│    ├─ 技术：PostgreSQL, Vector DB (Qdrant), Object Storage  │
│    ├─ 操作：                                                 │
│    │   • 重要信息持久化                                      │
│    │   • 语义检索                                            │
│    │   • 记忆巩固                                            │
│    │   • 记忆再巩固                                          │
│    └─ 例子：用户2024年3月购买了Python课程                   │
│                                                              │
│  【转化流程】                                                │
│  Working Memory → Short-term Memory → Long-term Memory      │
│       (实时)          (定期巩固)      (重要信息)            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 记忆类型

#### 3.3.1 按内容分类

```
┌─────────────────────────────────────────────────────────────┐
│  Episodic Memory（情景记忆）                                 │
├─────────────────────────────────────────────────────────────┤
│  定义：对具体事件和经历的记录                                 │
│  形式：结构化/半结构化                                       │
│  例子：                                                     │
│    • "用户在2025-01-10 14:30询问了关于pandas的问题"         │
│    • "用户购买了Python数据科学课程"                         │
│    • "用户偏好视频教程形式"                                  │
│                                                              │
│  存储方案：                                                 │
│    ├─ 结构化存储：PostgreSQL (JSONB)                        │
│    ├─ 语义索引：Vector DB (embedding)                       │
│    └─ 时间索引：时序查询优化                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Semantic Memory（语义记忆）                                 │
├─────────────────────────────────────────────────────────────┤
│  定义：从情景记忆中提取的抽象知识和概念                       │
│  形式：高度结构化                                           │
│  例子：                                                     │
│    • "用户喜欢Python编程"                                    │
│    • "用户每周学习约5小时"                                   │
│    • "用户的数据科学技能水平：中级"                          │
│                                                              │
│  存储方案：                                                 │
│    ├─ KV存储：Redis (user_attributes)                       │
│    ├─ 图数据库：Neo4j (knowledge graph)                     │
│    └─ 特征存储：PostgreSQL (user_profile)                   │
└─────────────────────────────────────────────────────────────┘
```

#### 3.3.2 按时效性分类

| 记忆类型 | 时效性 | 更新频率 | 检索需求 | 存储位置 |
|---------|--------|---------|---------|---------|
| **会话状态** | 秒级 | 每轮对话 | 实时 | Redis |
| **近期交互** | 天级 | 每次交互 | 近期优先 | PostgreSQL + Vector DB |
| **用户偏好** | 周级 | 演化更新 | 精确匹配 | Redis + PostgreSQL |
| **历史行为** | 永久 | 追加 | 语义检索 | Vector DB |
| **关键事件** | 永久 | 不可变 | 时间范围查询 | PostgreSQL |

### 3.4 核心机制

#### 3.4.1 Memory Consolidation（记忆巩固）

```
【记忆巩固：从短期到长期的转化】

触发条件：
├─ 定期任务（每天/每周）
├─ 重要事件检测（用户明确表达）
├─ 重复模式识别（多次提及）
└─ 情感强度（用户强调）

巩固算法：

def consolidate_memory(
    short_term_memories: List[Memory],
    user_profile: Profile
) -> List[LongTermMemory]:

    consolidated = []

    for memory in short_term_memories:
        # 1. 重要性评分
        importance = calculate_importance(
            frequency=memory.occurrence_count,
            recency=memory.timestamp,
            emotional_strength=memory.sentiment_score,
            user_explicitness=memory.is_explicit
        )

        # 2. 阈值过滤
        if importance > CONSOLIDATION_THRESHOLD:
            # 3. 提取语义记忆
            semantic = extract_semantic_memory(memory)

            # 4. 转换为长期记忆格式
            long_term = LongTermMemory(
                content=semantic.summary,
                entities=semantic.entities,
                relations=semantic.relations,
                confidence=importance,
                timestamp=memory.timestamp,
                source="consolidation"
            )

            consolidated.append(long_term)

    return consolidated
```

#### 3.4.2 Memory Reconsolidation（记忆再巩固）

```
【记忆再巩固：记忆的更新与修正】

触发场景：
1. 新信息与旧记忆冲突
   用户："我之前说喜欢Python，但现在想转学R"

2. 用户明确纠正
   用户："不对，我其实是偏好在晚上学习"

3. 长时间未访问
   记忆超过6个月未访问 → 降低置信度

4. 反馈学习
   用户对推荐的负面反馈 → 调整相关记忆权重

处理流程：

def reconsolidate_memory(
    old_memory: Memory,
    new_information: str,
    conflict_type: str
) -> Memory:

    if conflict_type == "direct_contradiction":
        # 直接矛盾：创建新版本，保留历史
        new_memory = Memory(
            content=new_information,
            version=old_memory.version + 1,
            replaces=old_memory.id,
            confidence=0.5,  # 新信息置信度较低
            timestamp=now()
        )

        # 旧记忆降权但保留
        old_memory.confidence *= 0.3
        old_memory.status = "superseded"

        return new_memory

    elif conflict_type == "preference_update":
        # 偏好更新：平滑过渡
        old_memory.content = merge_preference(
            old_content=old_memory.content,
            new_info=new_information,
            old_weight=0.4,
            new_weight=0.6
        )
        old_memory.confidence *= 0.9
        old_memory.last_updated = now()

        return old_memory

    elif conflict_type == "decay":
        # 记忆衰减：降低置信度
        old_memory.confidence *= 0.5
        old_memory.last_accessed = now()

        return old_memory
```

#### 3.4.3 Forgetting Mechanism（遗忘机制）

```
【遗忘机制：自动清理低价值记忆】

遗忘策略：

1. 时间衰减
   def decay(memory):
       age = now() - memory.last_accessed
       decay_factor = exp(-age / HALF_LIFE)
       memory.confidence *= decay_factor

2. 访问频率
   高访问频率 → 提升记忆强度
   低访问频率 → 逐渐衰减

3. 稀疏化存储
   相似记忆合并
   冗余信息删除

4. 分级归档
   低价值记忆 → 冷存储
   过期记忆 → 删除

清理策略：
├─ 每周清理confidence < 0.2的记忆
├─ 每月归档30天未访问的记忆
└─ 每季度删除90天未访问的低价值记忆
```

### 3.5 技术选型

#### 主流技术栈对比

| 技术方案 | 优势 | 劣势 | 适用场景 |
|---------|------|------|---------|
| **LangGraph Checkpointer** | ✅ 与LangGraph深度集成<br>✅ 自动状态管理 | ⚠️ 依赖LangGraph | 对话状态管理 |
| **LangGraph BaseStore** | ✅ 灵活的KV存储<br>✅ 多后端支持 | ⚠️ 需要手动设计schema | 长期记忆存储 |
| **Mem0** | ✅ 开箱即用<br>✅ 自动记忆管理 | ❌ 定制化能力弱<br>❌ RAG能力弱 | 快速原型 |
| **Zep** | ✅ 专注Agent记忆<br>✅ 向量检索内置 | ⚠️ 生态较小 | 生产环境 |
| **自建方案** | ✅ 完全控制<br>✅ 灵活扩展 | ❌ 开发成本高<br>❌ 维护负担 | 定制化需求 |

#### 推荐架构（生产级）

```python
# 三层存储架构
class MemoryArchitecture:
    def __init__(self):
        # Layer 1: 工作记忆
        self.working_memory = ConversationBuffer(
            max_tokens=32000,
            window_size=10
        )

        # Layer 2: 短期记忆
        self.short_term_memory = LangGraphCheckpointer(
            backend=PostgreSQL(),
            namespace="short_term",
            ttl=timedelta(days=7)
        )

        # Layer 3: 长期记忆
        self.long_term_memory = BaseStore(
            backend=PostgreSQL(),  # 结构化数据
            vector_db=Qdrant(),     # 语义检索
            namespace="long_term"
        )

    async def store(self, user_id: str, memory: Memory):
        # 1. 存储到工作记忆
        self.working_memory.add(memory)

        # 2. 异步写入短期记忆
        await self.short_term_memory.put(user_id, memory)

        # 3. 评估是否需要长期存储
        if self._should_consolidate(memory):
            await self.long_term_memory.put(user_id, memory)

    async def retrieve(
        self,
        user_id: str,
        query: str,
        memory_types: List[str]
    ) -> List[Memory]:
        results = []

        # 1. 工作记忆
        if "working" in memory_types:
            results.extend(self.working_memory.get_recent())

        # 2. 短期记忆
        if "short_term" in memory_types:
            results.extend(
                await self.short_term_memory.search(user_id, query)
            )

        # 3. 长期记忆
        if "long_term" in memory_types:
            results.extend(
                await self.long_term_memory.search(user_id, query)
            )

        # 4. 去重和排序
        return self._deduplicate_and_rank(results)
```

### 3.6 设计模式

#### Pattern 1: Sliding Window（滑动窗口）

```python
# 适用场景：长对话的上下文管理
class SlidingWindowMemory:
    def __init__(self, window_size: int = 10):
        self.window = deque(maxlen=window_size)

    def add(self, message: Message):
        self.window.append(message)

    def get_context(self) -> str:
        # 自动保持最近N轮对话
        return "\n".join([m.content for m in self.window])
```

#### Pattern 2: Summary + Retrieval（摘要+检索）

```python
# 适用场景：超长对话历史
class SummaryRetrievalMemory:
    def __init__(self):
        self.summaries = []  # 历史摘要
        self.recent = []     # 近期详细记录

    async def consolidate(self):
        if len(self.recent) > 20:
            # 生成摘要
            summary = await llm_summarize(self.recent)
            self.summaries.append(summary)
            self.recent.clear()

    def get_context(self) -> str:
        return {
            "historical_summary": self.summaries,
            "recent_conversation": self.recent
        }
```

#### Pattern 3: Importance-Based（重要性优先）

```python
# 适用场景：有限容量下的关键信息保留
class ImportanceBasedMemory:
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.memories = []  # 按重要性排序

    async def add(self, memory: Memory):
        # 计算重要性
        memory.importance = await self._calculate_importance(memory)

        # 插入并排序
        self.memories.append(memory)
        self.memories.sort(key=lambda m: m.importance, reverse=True)

        # 保持容量
        if len(self.memories) > self.capacity:
            self.memories = self.memories[:self.capacity]
```

### 3.7 关键指标

| 指标类别 | 具体指标 | 目标值 |
|---------|---------|--------|
| **存储** | 平均每用户记忆大小 | < 100MB |
| **存储** | 记忆保留率（30天） | > 95% |
| **检索** | 检索延迟（P99） | < 200ms |
| **检索** | 检索准确率（Top-10） | > 0.85 |
| **质量** | 记忆一致性 | > 0.9 |
| **质量** | 记忆巩固准确率 | > 0.8 |

---

## 四、Knowledge Engineering（知识工程）

### 4.1 定义

**Knowledge Engineering（知识工程）** 是指在 AI Agent 系统中，**工程化地设计、实现和管理知识图谱子系统**，通过实体、关系、属性的提取、存储、推理和演化，实现结构化知识的自动构建和智能应用。

**与现代技术的关系：**
- Knowledge Engineering ≠ 传统专家系统的规则工程
- Knowledge Engineering = Knowledge Graph + GraphRAG + Automated Extraction

**核心问题：**
- 如何自动化地从非结构化文本中提取知识？
- 如何构建和演化动态知识图谱？
- 如何实现图谱的高效推理？
- 如何融合外部知识和用户记忆？

### 4.2 知识表示

#### 4.2.1 基本元素

```
┌─────────────────────────────────────────────────────────────┐
│  Knowledge Graph：知识图谱表示                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  【Entity / 实体】                                           │
│    ├─ 定义：现实世界中的对象或概念                           │
│    ├─ 类型：Person, Product, Course, Skill, Concept, etc.   │
│    ├─ 属性：                                                │
│    │   • id: 唯一标识                                       │
│    │   • type: 实体类型                                     │
│    │   • name: 显示名称                                     │
│    │   • properties: 自定义属性                             │
│    │   • embedding: 向量表示                                │
│    │   • timestamp: 创建时间                                │
│    └─ 例子：                                                │
│        {                                                     │
│          "id": "user_123",                                  │
│          "type": "Person",                                  │
│          "name": "张三",                                     │
│          "properties": {                                    │
│            "skill_level": "intermediate",                   │
│            "learning_goal": "数据科学"                      │
│          },                                                 │
│          "embedding": [0.1, 0.2, ...],                      │
│          "created_at": "2024-03-01T10:00:00Z"              │
│        }                                                     │
│                                                              │
│  【Relation / 关系】                                         │
│    ├─ 定义：实体之间的语义联系                               │
│    ├─ 类型：购买、学习、偏好、属于、包含、前置、等           │
│    ├─ 属性：                                                │
│    │   • source_entity: 源实体ID                            │
│    │   • target_entity: 目标实体ID                          │
│    │   • relation_type: 关系类型                            │
│    │   • weight: 关系强度（0-1）                            │
│    │   • timestamp: 关系建立时间                            │
│    │   • metadata: 额外信息                                 │
│    └─ 例子：                                                │
│        {                                                     │
│          "source": "user_123",                              │
│          "target": "python_course",                         │
│          "type": "purchased",                               │
│          "weight": 1.0,                                     │
│          "timestamp": "2024-03-01T10:00:00Z",              │
│          "metadata": {                                      │
│            "price": 199,                                    │
│            "platform": "example.com"                        │
│          }                                                  │
│        }                                                     │
│                                                              │
│  【Attribute / 属性】                                        │
│    ├─ 定义：实体的特征信息                                   │
│    ├─ 类型：字符串、数值、日期、列表、嵌套对象               │
│    └─ 例子：                                                │
│        user.skill_level = "intermediate"                    │
│        course.duration = 40                                  │
│        course.prerequisites = ["python_basic"]              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 4.2.2 知识图谱示例

```cypher
// Neo4j Cypher示例：用户知识图谱

// 创建实体
CREATE (u:Person {
  id: "user_123",
  name: "张三",
  skill_level: "intermediate"
})

CREATE (c1:Course {
  id: "python_basic",
  name: "Python基础",
  difficulty: "beginner"
})

CREATE (c2:Course {
  id: "pandas_data_analysis",
  name: "pandas数据分析",
  difficulty: "intermediate"
})

CREATE (s:Skill {
  id: "data_science",
  name: "数据科学"
})

// 创建关系
CREATE (u)-[:PURCHASED {
  timestamp: "2024-03-01",
  price: 199
}]->(c1)

CREATE (u)-[:INQUIRED {
  timestamp: "2024-04-15",
  topic: "pandas基础"
}]->(c2)

CREATE (u)-[:LEARNING]->(s)

CREATE (c1)-[:PREREQUISITE_OF]->(c2)

CREATE (c2)-[:BELONGS_TO]->(s)

// 查询推理：用户应该学什么？
MATCH path = (u:Person {id: "user_123"})-[:PURCHASED|INQUIRED|LEARNING*]->(related)
RETURN related
ORDER BY related.timestamp DESC
```

### 4.3 知识提取

#### 4.3.1 提取流程

```
【知识提取：从非结构化文本到结构化图谱】

原始输入：
  "用户在2024年3月1日购买了Python基础课程，
   他在4月15日询问了pandas库的使用，
   他偏好视频教程形式，每周学习约5小时。"

      ↓

┌─────────────────────────────────────────────────────────┐
│  Phase 1: Entity Extraction（实体提取）                  │
├─────────────────────────────────────────────────────────┤
│  • 使用LLM识别文本中的实体                               │
│  • 实体类型分类                                         │
│  • 实体消歧（合并重复实体）                              │
│                                                          │
│  提取结果：                                              │
│    Entities: [                                           │
│      {id: "user_123", type: "Person", name: "用户"},    │
│      {id: "python_basic", type: "Course",               │
│       name: "Python基础课程"},                           │
│      {id: "pandas_lib", type: "Library",                │
│       name: "pandas库"},                                 │
│      {id: "video_tutorial", type: "Format",             │
│       name: "视频教程"}                                  │
│    ]                                                     │
└─────────────────────────────────────────────────────────┘
      ↓

┌─────────────────────────────────────────────────────────┐
│  Phase 2: Relation Extraction（关系提取）                │
├─────────────────────────────────────────────────────────┤
│  • 识别实体间的关系                                      │
│  • 关系类型分类                                         │
│  • 提取关系属性（时间、权重等）                          │
│                                                          │
│  提取结果：                                              │
│    Relations: [                                          │
│      {source: "user_123", target: "python_basic",       │
│       type: "PURCHASED", timestamp: "2024-03-01"},      │
│      {source: "user_123", target: "pandas_lib",         │
│       type: "INQUIRED", timestamp: "2024-04-15"},       │
│      {source: "user_123", target: "video_tutorial",     │
│       type: "PREFERS", weight: 0.9}                     │
│    ]                                                     │
└─────────────────────────────────────────────────────────┘
      ↓

┌─────────────────────────────────────────────────────────┐
│  Phase 3: Knowledge Graph Construction（图谱构建）      │
├─────────────────────────────────────────────────────────┤
│  • 创建节点和边                                          │
│  • 图数据库存储（Neo4j）                                 │
│  • 建立索引和约束                                        │
│                                                          │
│  图谱结果：                                              │
│    [user_123] --(PURCHASED)--> [python_basic]           │
│    [user_123] --(INQUIRED)--> [pandas_lib]              │
│    [user_123] --(PREFERS)--> [video_tutorial]           │
└─────────────────────────────────────────────────────────┘
```

#### 4.3.2 提取技术

| 技术方案 | 优势 | 劣势 | 适用场景 |
|---------|------|------|---------|
| **LLM-based Extraction** | ✅ 零样本能力<br>✅ 灵活性高 | ❌ 成本高<br>❌ 不稳定 | 通用场景 |
| **GraphRAG** | ✅ 自动化<br>✅ 图感知 | ⚠️ 需要调参 | 大规模文本 |
| **LightRAG** | ✅ 轻量级<br>✅ 快速 | ⚠️ 精度较低 | 快速原型 |
| **Rule-based + NER** | ✅ 快速<br>✅ 可控 | ❌ 需要规则 | 特定领域 |
| **Ensemble（组合）** | ✅ 精度高<br>✅ 鲁棒 | ❌ 复杂 | 生产环境 |

#### 4.3.3 提取示例代码

```python
async def extract_knowledge_from_text(
    text: str,
    user_id: str,
    llm: BaseLLM
) -> KnowledgeGraph:
    """
    使用LLM从文本中提取知识图谱
    """

    # ═══════════════════════════════════════════════
    # Step 1: 实体提取
    # ═══════════════════════════════════════════════

    entity_extraction_prompt = f"""
    从以下文本中提取所有实体，返回JSON格式：

    文本：{text}

    实体类型：
    - Person（人物）
    - Course（课程）
    - Skill（技能）
    - Product（产品）
    - Concept（概念）

    返回格式：
    {{
      "entities": [
        {{"id": "unique_id", "type": "Course", "name": "Python基础"}},
        ...
      ]
    }}
    """

    entities_response = await llm.achat(entity_extraction_prompt)
    entities = parse_entities(entities_response)

    # ═══════════════════════════════════════════════
    # Step 2: 关系提取
    # ═══════════════════════════════════════════════

    relation_extraction_prompt = f"""
    从以下文本中提取实体之间的关系，返回JSON格式：

    文本：{text}

    实体列表：{entities}

    关系类型：
    - PURCHASED（购买）
    - INQUIRED（询问）
    - LEARNING（学习）
    - PREFERS（偏好）
    - BELONGS_TO（属于）
    - PREREQUISITE_OF（前置）

    返回格式：
    {{
      "relations": [
        {{
          "source": "entity_id_1",
          "target": "entity_id_2",
          "type": "PURCHASED",
          "timestamp": "2024-03-01",
          "weight": 1.0
        }},
        ...
      ]
    }}
    """

    relations_response = await llm.achat(relation_extraction_prompt)
    relations = parse_relations(relations_response)

    # ═══════════════════════════════════════════════
    # Step 3: 构建知识图谱
    # ═══════════════════════════════════════════════

    kg = KnowledgeGraph()

    # 添加节点
    for entity in entities:
        kg.add_node(
            node_id=entity["id"],
            node_type=entity["type"],
            properties=entity
        )

    # 添加边
    for relation in relations:
        kg.add_edge(
            source=relation["source"],
            target=relation["target"],
            edge_type=relation["type"],
            properties=relation
        )

    return kg
```

### 4.4 知识推理

#### 4.4.1 推理类型

```
【知识图谱推理：从显性知识到隐性洞察】

┌─────────────────────────────────────────────────────────┐
│  1. Path-based Reasoning（路径推理）                     │
├─────────────────────────────────────────────────────────┤
│  查询：找出用户到"数据科学"的所有路径                     │
│                                                          │
│  Cypher:                                                │
│    MATCH path = (u:Person {{id: "user_123"}})-[*..3]->(s)│
│    WHERE s.name = "数据科学"                             │
│    RETURN path                                          │
│                                                          │
│  结果：                                                  │
│    user_123 → [购买] → python_basic                     │
│            → [属于] → data_science                      │
│                                                          │
│    user_123 → [询问] → pandas_lib                       │
│            → [用于] → data_science                      │
│                                                          │
│  洞察：用户正在学习Python数据科学路径                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  2. Associative Reasoning（关联推理）                    │
├─────────────────────────────────────────────────────────┤
│  规则：如果A喜欢B，B属于C，则A可能喜欢C                 │
│                                                          │
│  示例：                                                  │
│    user_123 -[PREFERS]-> video_tutorial                 │
│    pandas_course -[FORMAT]-> video_tutorial             │
│                                                          │
│    推理：user_123 可能喜欢 pandas_course                │
│                                                          │
│  置信度计算：                                            │
│    confidence = base_score * relation_weight            │
│    confidence = 0.7 * 0.9 = 0.63                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  3. Temporal Reasoning（时序推理）                       │
├─────────────────────────────────────────────────────────┤
│  查询：用户的学习趋势                                    │
│                                                          │
│  Cypher:                                                │
│    MATCH (u:Person {{id: "user_123"}})-[r:INQUIRED]->(c)│
│    RETURN c                                            │
│    ORDER BY r.timestamp DESC                            │
│                                                          │
│  结果：                                                  │
│    2024-01: python_basic                                │
│    2024-03: pandas基础                                   │
│    2024-04: numpy入门                                   │
│    2024-05: matplotlib可视化                            │
│                                                          │
│  洞察：用户正在系统学习Python数据科学栈                 │
│  预测：下一步可能学习机器学习                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  4. Collaborative Reasoning（协同推理）                  │
├─────────────────────────────────────────────────────────┤
│  基于相似用户的行为进行推荐                              │
│                                                          │
│  算法：                                                  │
│    1. 找出与user_123相似的用户（基于图谱结构相似度）    │
│    2. 获取这些用户的学习路径                             │
│    3. 找出user_123尚未学习但被推荐最多的课程            │
│                                                          │
│  示例：                                                  │
│    相似用户：user_456, user_789                          │
│    他们学过：machine_learning, deep_learning             │
│    推荐给user_123：machine_learning                      │
└─────────────────────────────────────────────────────────┘
```

#### 4.4.2 推理示例代码

```python
async def knowledge_graph_reasoning(
    user_id: str,
    query: str,
    kg: KnowledgeGraph
) -> dict:
    """
    知识图谱推理
    """

    results = {
        "inferences": [],
        "recommendations": [],
        "related_entities": []
    }

    # ═══════════════════════════════════════════════
    # Reasoning 1: 学习路径推理
    # ═══════════════════════════════════════════════

    learning_paths = kg.find_paths(
        start_node=user_id,
        max_depth=3,
        edge_types=["PURCHASED", "INQUIRED", "LEARNING"]
    )

    # 提取共同终点
    destinations = Counter([
        path.end_node
        for path in learning_paths
    ])

    for dest, count in destinations.most_common(3):
        results["inferences"].append({
            "type": "learning_interest",
            "content": f"用户对 {dest} 表现出兴趣",
            "confidence": count / len(learning_paths),
            "evidence": [str(p) for p in learning_paths
                        if p.end_node == dest]
        })

    # ═══════════════════════════════════════════════
    # Reasoning 2: 协同推荐
    # ═══════════════════════════════════════════════

    # 找出相似用户
    similar_users = kg.find_similar_users(
        user_id=user_id,
        top_k=5
    )

    # 获取他们的学习路径
    their_courses = kg.get_neighbors(
        nodes=similar_users,
        edge_types=["PURCHASED", "COMPLETED"]
    )

    # 过滤用户已学过的
    user_courses = kg.get_neighbors(
        nodes=[user_id],
        edge_types=["PURCHASED", "COMPLETED"]
    )

    recommended = set(their_courses) - set(user_courses)

    for course in recommended:
        results["recommendations"].append({
            "type": "course",
            "content": course,
            "reason": "相似用户也在学",
            "confidence": 0.7
        })

    # ═══════════════════════════════════════════════
    # Reasoning 3: 时序推理
    # ═══════════════════════════════════════════════

    recent_activities = kg.get_recent_activities(
        user_id=user_id,
        days=30,
        limit=10
    )

    # 识别趋势
    if len(recent_activities) >= 3:
        skills = [a.skill for a in recent_activities]
        trend = infer_learning_trend(skills)

        results["inferences"].append({
            "type": "learning_trend",
            "content": f"用户正在学习 {trend}",
            "confidence": 0.8,
            "timeline": [str(a) for a in recent_activities]
        })

    return results
```

### 4.5 知识演化

```
【知识图谱演化：动态更新机制】

┌─────────────────────────────────────────────────────────┐
│  1. 实体演化                                            │
├─────────────────────────────────────────────────────────┤
│  • 新增实体：从新交互中提取                              │
│  • 实体合并：检测重复实体并合并                          │
│  • 属性更新：更新实体的属性值                            │
│  • 实体分裂：拆分过于泛化的实体                          │
│                                                          │
│  示例：                                                  │
│    新实体：machine_learning                              │
│    重复检测："机器学习" == "machine_learning"           │
│    合并：merge("机器学习", "machine_learning")          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  2. 关系演化                                            │
├─────────────────────────────────────────────────────────┤
│  • 新增关系：发现新的语义关联                            │
│  • 关系权重调整：基于访问频率、时间衰减                  │
│  • 关系类型转换：语义变化                                │
│  • 过期关系清理：长期无效的关系                          │
│                                                          │
│  示例：                                                  │
│    关系权重：user_123 -[PREFERS, 0.9]-> video_tutorial  │
│    衰减：weight *= 0.95（每月）                          │
│    更新：用户最近选择文字教程 → weight = 0.3           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  3. 图谱结构演化                                        │
├─────────────────────────────────────────────────────────┤
│  • 社区发现：识别紧密连接的节点群                        │
│  • 关键节点识别：发现hub节点、桥接节点                   │
│  • 子图提取：提取特定主题的知识子图                      │
│  • 图谱压缩：简化复杂路径                                │
│                                                          │
│  应用：                                                  │
│    社区：{Python, pandas, numpy} → "Python数据科学生态" │
│    关键节点：user_123是学习路径的中心                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  4. 反馈学习                                            │
├─────────────────────────────────────────────────────────┤
│  • 用户反馈：调整图谱权重                                │
│  • 推荐效果：优化推理策略                                │
│  • 提取质量：改进实体/关系提取模型                       │
│                                                          │
│  闭环：                                                  │
│    推荐 → 用户反馈 → 权重调整 → 优化推荐                 │
└─────────────────────────────────────────────────────────┘
```

### 4.6 技术选型

#### 主流技术栈对比

| 技术方案 | 优势 | 劣势 | 适用场景 |
|---------|------|------|---------|
| **GraphRAG** | ✅ 微软出品<br>✅ 图感知检索 | ⚠️ 配置复杂<br>⚠️ 资源消耗大 | 企业级应用 |
| **LightRAG** | ✅ 轻量级<br>✅ 易用 | ⚠️ 功能简化 | 中小规模 |
| **Neo4j** | ✅ 成熟<br>✅ 查询强大 | ❌ 部署复杂 | 图谱推理 |
| **NetworkX** | ✅ Python原生<br>✅ 灵活 | ⚠️ 性能一般 | 原型开发 |
| **ArangoDB** | ✅ 多模型<br>✅ 易用 | ⚠️ 图能力弱Neo4j | 混合存储 |

#### 推荐架构（生产级）

```python
class KnowledgeGraphSystem:
    def __init__(self):
        # 图数据库
        self.graph_db = Neo4j(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="password"
        )

        # 向量数据库（用于实体检索）
        self.vector_db = Qdrant(
            collection_name="entities",
            vector_size=1536
        )

        # LLM（用于提取和推理）
        self.llm = OpenAI(model="gpt-4-turbo")

        # 缓存
        self.cache = Redis()

    async def extract_and_update(
        self,
        text: str,
        user_id: str
    ):
        """提取知识并更新图谱"""

        # 1. 提取实体和关系
        kg = await self.extract_knowledge(text, user_id)

        # 2. 检查缓存
        cache_key = f"kg:{user_id}:{hash(text)}"
        if await self.cache.exists(cache_key):
            return await self.cache.get(cache_key)

        # 3. 更新图谱
        for entity in kg.entities:
            # 实体去重
            existing = await self._find_duplicate(entity)

            if existing:
                # 合并属性
                await self.graph_db.merge_node(existing, entity)
            else:
                # 创建新节点
                await self.graph_db.create_node(entity)

                # 建立向量索引
                embedding = await self.llm.embed(entity.name)
                await self.vector_db.upsert(
                    id=entity.id,
                    vector=embedding,
                    payload=entity
                )

        for relation in kg.relations:
            await self.graph_db.create_edge(relation)

        # 4. 缓存结果
        await self.cache.set(cache_key, kg, ttl=3600)

        return kg

    async def query(
        self,
        user_id: str,
        query: str
    ) -> dict:
        """图谱查询和推理"""

        # 1. 实体检索
        query_embedding = await self.llm.embed(query)
        similar_entities = await self.vector_db.search(
            vector=query_embedding,
            top_k=10,
            filter={"user_id": user_id}
        )

        # 2. 子图扩展
        subgraph = await self.graph_db.expand(
            nodes=[e.id for e in similar_entities],
            max_depth=2
        )

        # 3. 图谱推理
        inferences = await self._reasoning(subgraph, query)

        return {
            "entities": similar_entities,
            "subgraph": subgraph,
            "inferences": inferences
        }
```

### 4.7 关键指标

| 指标类别 | 具体指标 | 目标值 |
|---------|---------|--------|
| **提取质量** | 实体提取F1-score | > 0.85 |
| **提取质量** | 关系提取准确率 | > 0.8 |
| **推理性能** | 推理延迟（P99） | < 500ms |
| **推理性能** | 推理准确率 | > 0.75 |
| **图谱规模** | 平均每用户节点数 | 100-1000 |
| **演化速度** | 增量更新延迟 | < 1s |

---

## 五、三层架构关系

### 5.1 架构层次

```
┌─────────────────────────────────────────────────────────────┐
│                  Context Engineering                        │
│                 （上下文工程 - 总体层）                       │
│                                                              │
│  职责：整合Memory和Knowledge，为LLM提供最优上下文            │
│  ┌─────────────────────┬─────────────────────────────┐      │
│  │                     │                             │      │
│  │   Memory Engineering    Knowledge Engineering      │      │
│  │   （记忆工程）          （知识工程）                │      │
│  │                     │                             │      │
│  │  ┌───────────────┐ │ ┌────────────────────────┐  │      │
│  │  │ Working       │ │ │  Entity Extraction     │  │      │
│  │  │ Short-term    │ │ │  Relation Extraction    │  │      │
│  │  │ Long-term     │ │ │  Knowledge Graph       │  │      │
│  │  └───────────────┘ │ │  Graph Reasoning        │  │      │
│  │                     │ │  Knowledge Evolution    │  │      │
│  │                     │ └────────────────────────┘  │      │
│  │                     │                             │      │
│  └─────────────────────┴─────────────────────────────┘      │
│                                                             │
│  数据流：                                                   │
│    Memory → Knowledge Extraction → Knowledge Graph          │
│           ↓                                                 │
│    Context Fusion (Memory + Knowledge + RAG)                │
│           ↓                                                 │
│    LLM Context Window                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 协作流程

```python
async def three_layer_collaboration(
    user_query: str,
    user_id: str
) -> str:
    """
    三层架构协作示例
    """

    # ═══════════════════════════════════════════════
    # Layer 1: Memory Engineering
    # ═══════════════════════════════════════════════

    # 1.1 检索记忆
    memory_engine = MemoryEngine()
    user_memories = await memory_engine.retrieve(
        user_id=user_id,
        query=user_query,
        memory_types=["short_term", "long_term"]
    )

    # 1.2 记忆巩固（如果需要）
    important_memories = [
        m for m in user_memories
        if m.importance > 0.8
    ]
    if important_memories:
        await memory_engine.consolidate(
            user_id=user_id,
            memories=important_memories
        )

    # ═══════════════════════════════════════════════
    # Layer 2: Knowledge Engineering
    # ═══════════════════════════════════════════════

    # 2.1 从记忆中提取知识
    kg_engine = KnowledgeGraphEngine()

    for memory in user_memories:
        extracted_kg = await kg_engine.extract_from_text(
            text=memory.content,
            user_id=user_id
        )
        await kg_engine.update_graph(extracted_kg)

    # 2.2 图谱推理
    graph_insights = await kg_engine.reasoning(
        user_id=user_id,
        query=user_query
    )

    # ═══════════════════════════════════════════════
    # Layer 3: Context Engineering
    # ═══════════════════════════════════════════════

    # 3.1 外部知识检索（RAG）
    external_knowledge = await rag_retrieve(user_query)

    # 3.2 上下文融合
    context_engine = ContextEngine()

    fused_context = await context_engine.fuse(
        user_query=user_query,
        external_knowledge=external_knowledge,
        user_memories=user_memories,
        knowledge_graph=graph_insights,
        budget={  # Token预算分配
            "external": 0.3,
            "memory": 0.3,
            "graph": 0.2,
            "conversation": 0.2
        }
    )

    # 3.3 质量检查
    quality = await context_engine.evaluate(fused_context)

    if quality.score < 0.7:
        # 触发优化策略
        fused_context = await context_engine.optimize(
            context=fused_context,
            issues=quality.issues
        )

    return fused_context
```

### 5.3 职责边界

| 职责 | Context Engineering | Memory Engineering | Knowledge Engineering |
|------|--------------------|--------------------|----------------------|
| **数据源管理** | ✅ 整合多源数据 | ❌ 不涉及 | ❌ 不涉及 |
| **记忆存储** | ❌ 不涉及 | ✅ 核心职责 | ❌ 不涉及 |
| **记忆检索** | ❌ 不涉及 | ✅ 核心职责 | ❌ 不涉及 |
| **记忆巩固** | ❌ 不涉及 | ✅ 核心职责 | ❌ 不涉及 |
| **实体提取** | ❌ 不涉及 | ⚠️ 可涉及 | ✅ 核心职责 |
| **关系提取** | ❌ 不涉及 | ❌ 不涉及 | ✅ 核心职责 |
| **图谱构建** | ❌ 不涉及 | ❌ 不涉及 | ✅ 核心职责 |
| **图谱推理** | ❌ 不涉及 | ❌ 不涉及 | ✅ 核心职责 |
| **上下文融合** | ✅ 核心职责 | ❌ 不涉及 | ❌ 不涉及 |
| **Token预算管理** | ✅ 核心职责 | ❌ 不涉及 | ❌ 不涉及 |
| **个性化排序** | ✅ 核心职责 | ❌ 不涉及 | ⚠️ 提供特征 |
| **LLM调用** | ✅ 核心职责 | ❌ 不涉及 | ❌ 不涉及 |

### 5.4 数据流向

```
【数据流向：从用户交互到知识演化】

用户输入
  ↓
┌─────────────────────────────────────────────────────────┐
│ Context Engineering                                     │
│  • 解析用户输入                                          │
│  • 并行触发Memory和Knowledge查询                         │
└────┬────────────────────────────────────────┬───────────┘
     │                                        │
     ↓                                        ↓
┌──────────────────┐              ┌──────────────────────┐
│ Memory           │              │ Knowledge            │
│ Engineering      │              │ Engineering          │
├──────────────────┤              ├──────────────────────┤
│ • 检索用户记忆   │              │ • 图谱推理           │
│ • 返回历史记录   │              │ • 返回关联实体       │
└────┬─────────────┘              └────┬─────────────────┘
     │                                  │
     │         Memory → Knowledge      │
     │         知识提取流程             │
     └──────────────┬───────────────────┘
                    ↓
            ┌───────────────┐
            │ 提取实体/关系 │
            └───────┬───────┘
                    ↓
            ┌───────────────┐
            │ 更新知识图谱  │
            └───────────────┘
                    │
                    ↓
     ┌──────────────┴──────────────┐
     │                             │
     ↓                             ↓
┌──────────────────┐      ┌──────────────────┐
│ Memory           │      │ Context          │
│ Engineering      │      │ Engineering      │
│  • 智能记忆巩固  │      │  • 融合所有信息   │
│  • 语义记忆更新  │      │  • 构建上下文     │
└──────────────────┘      └────┬─────────────┘
                                │
                                ↓
                        ┌───────────────┐
                        │ LLM 生成响应  │
                        └───────┬───────┘
                                │
                                ↓
                        ┌───────────────┐
                        │  Memory Store │  ← 存储新交互
                        │  KG Update    │  ← 更新知识图谱
                        └───────────────┘
```

### 5.5 接口设计

```python
# ═══════════════════════════════════════════════
# Memory Engineering Interface
# ═══════════════════════════════════════════════

class MemoryEngine(ABC):
    @abstractmethod
    async def retrieve(
        self,
        user_id: str,
        query: str,
        memory_types: List[str]
    ) -> List[Memory]:
        """检索记忆"""
        pass

    @abstractmethod
    async def store(
        self,
        user_id: str,
        memory: Memory
    ) -> None:
        """存储记忆"""
        pass

    @abstractmethod
    async def consolidate(
        self,
        user_id: str,
        memories: List[Memory]
    ) -> None:
        """记忆巩固"""
        pass

# ═══════════════════════════════════════════════
# Knowledge Engineering Interface
# ═══════════════════════════════════════════════

class KnowledgeGraphEngine(ABC):
    @abstractmethod
    async def extract_from_text(
        self,
        text: str,
        user_id: str
    ) -> KnowledgeGraph:
        """从文本提取知识"""
        pass

    @abstractmethod
    async def reasoning(
        self,
        user_id: str,
        query: str
    ) -> dict:
        """图谱推理"""
        pass

    @abstractmethod
    async def update_graph(
        self,
        kg: KnowledgeGraph
    ) -> None:
        """更新图谱"""
        pass

# ═══════════════════════════════════════════════
# Context Engineering Interface
# ═══════════════════════════════════════════════

class ContextEngine(ABC):
    def __init__(
        self,
        memory_engine: MemoryEngine,
        kg_engine: KnowledgeGraphEngine,
        rag_engine: RAGEngine
    ):
        self.memory = memory_engine
        self.kg = kg_engine
        self.rag = rag_engine

    @abstractmethod
    async def fuse(
        self,
        user_query: str,
        external_knowledge: List[Document],
        user_memories: List[Memory],
        knowledge_graph: dict,
        budget: dict
    ) -> str:
        """融合多源上下文"""
        pass

    @abstractmethod
    async def evaluate(
        self,
        context: str
    ) -> QualityScore:
        """评估上下文质量"""
        pass
```

---

## 六、实施指导

### 6.1 团队组织

#### 推荐的团队结构

```
┌─────────────────────────────────────────────────────────┐
│  AI Agent 团队组织（基于三层架构）                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  【Context Engineering Team】                           │
│    ├─ 负责人：Context Lead                              │
│    ├─ 职责：                                            │
│    │   • 整体架构设计                                   │
│    │   • 上下文融合策略                                 │
│    │   • Token预算优化                                  │
│    │   • 个性化排序                                     │
│    │   • LLM调用优化                                    │
│    └─ 技能要求：                                        │
│       • Prompt Engineering                              │
│       • System Design                                  │
│       • LLM特性理解                                     │
│                                                         │
│  【Memory Engineering Team】                            │
│    ├─ 负责人：Memory Lead                               │
│    ├─ 职责：                                            │
│    │   • 记忆系统设计                                   │
│    │   • 存储架构（Redis/PG/Vector DB）                 │
│    │   • 记忆巩固算法                                   │
│    │   • 遗忘机制                                       │
│    │   • 记忆质量评估                                   │
│    └─ 技能要求：                                        │
│       • Database Design                                │
│       • Data Modeling                                  │
│       • LangGraph/Mem0                                 │
│                                                         │
│  【Knowledge Engineering Team】                         │
│    ├─ 负责人：Knowledge Lead                            │
│    ├─ 职责：                                            │
│    │   • 知识图谱设计                                   │
│    │   • 实体/关系提取                                  │
│    │   • 图谱推理                                       │
│    │   • 知识演化                                       │
│    │   • Neo4j/GraphRAG                                │
│    └─ 技能要求：                                        │
│       • Knowledge Graph                                │
│       • Graph Algorithms                               │
│       • NLP/Information Extraction                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 协作模式

```python
# 协作接口示例

# Context Team调用Memory和Knowledge
class ContextTeam:
    def __init__(
        self,
        memory_system: MemorySystem,  # Memory Team提供
        knowledge_system: KnowledgeSystem  # Knowledge Team提供
    ):
        self.memory = memory_system
        self.knowledge = knowledge_system

    async def build_context(self, query, user_id):
        # 并行调用
        memories, graph_insights = await asyncio.gather(
            self.memory.retrieve(user_id, query),  # 调用Memory Team接口
            self.knowledge.reasoning(user_id, query)  # 调用Knowledge Team接口
        )

        # 融合
        return self._fuse(query, memories, graph_insights)
```

### 6.2 开发阶段

#### Phase 1: MVP（4-6周）

**目标：** 验证三层架构可行性

**Context Engineering:**
- ✅ 基础上下文融合
- ✅ 简单Token预算管理
- ❌ 复杂优化策略

**Memory Engineering:**
- ✅ LangGraph Checkpointer（短期）
- ✅ PostgreSQL存储（长期）
- ❌ 自动记忆巩固

**Knowledge Engineering:**
- ⚠️ 简化版图谱（NetworkX）
- ⚠️ 基于规则推理
- ❌ 自动提取

#### Phase 2: Production（3-4个月）

**目标：** 生产级系统

**Context Engineering:**
- ✅ 智能上下文融合
- ✅ 动态Token预算
- ✅ 个性化重排序
- ✅ A/B测试框架

**Memory Engineering:**
- ✅ 完整记忆管理
- ✅ 自动记忆巩固
- ✅ 遗忘机制
- ✅ 向量检索

**Knowledge Engineering:**
- ✅ GraphRAG/Neo4j
- ✅ LLM自动提取
- ✅ 图谱推理
- ✅ 知识演化

#### Phase 3: Optimization（持续）

**目标：** 性能和效果优化

**优化方向:**
- 上下文质量优化
- 检索延迟降低
- 推理准确率提升
- 用户体验提升

### 6.3 技术选型决策树

```
开始选型
  │
  ├─ 团队规模？
  │   ├─ 小团队（<5人）
  │   │   └─ 推荐方案：
  │   │       • Memory: Mem0
  │   │       • Knowledge: LightRAG
  │   │       • Context: 自建（LangChain）
  │   │
  │   └─ 大团队（>10人）
  │       └─ 推荐方案：
  │           • Memory: LangGraph + PostgreSQL
  │           • Knowledge: GraphRAG + Neo4j
  │           • Context: 自建完整系统
  │
  ├─ 复杂度要求？
  │   ├─ 低（快速验证）
  │   │   └─ 使用现成方案（Mem0 + LightRAG）
  │   │
  │   └─ 高（生产级）
  │       └─ 自建 + 最佳实践组合
  │
  ├─ 延迟要求？
  │   ├─ 低延迟（<500ms）
  │   │   └─ 优化：
  │   │       • Redis缓存
  │   │       • 并行查询
  │   │       • 预计算
  │   │
  │   └─ 可接受（<2s）
  │       └─ 标准实现
  │
  └─ 预算约束？
      ├─ 低预算
      │   └─ 开源方案
      │       • PostgreSQL
      │       • Qdrant
      │       • Neo4j Community
      │
      └─ 充足预算
          └─ 商业方案
              • Managed PostgreSQL
              • Pinecone
              • Neo4j Enterprise
```

### 6.4 最佳实践

#### Practice 1: 接口优先设计

```python
# 先定义接口，再实现

class MemoryEngine(ABC):
    @abstractmethod
    async def retrieve(self, user_id: str, query: str) -> List[Memory]:
        pass

# 可以有多个实现
class PostgresMemoryEngine(MemoryEngine):
    async def retrieve(self, user_id: str, query: str) -> List[Memory]:
        # PostgreSQL实现
        pass

class RedisMemoryEngine(MemoryEngine):
    async def retrieve(self, user_id: str, query: str) -> List[Memory]:
        # Redis实现
        pass

# 便于切换和测试
```

#### Practice 2: 分层测试

```python
# Memory Engineering测试
class TestMemoryEngine:
    async def test_memory_retrieval(self):
        engine = PostgresMemoryEngine()
        memories = await engine.retrieve("user_123", "Python")
        assert len(memories) > 0

# Knowledge Engineering测试
class TestKnowledgeEngine:
    async def test_graph_reasoning(self):
        engine = KnowledgeGraphEngine()
        insights = await engine.reasoning("user_123", "学习")
        assert "inferences" in insights

# Context Engineering测试
class TestContextEngine:
    async def test_context_fusion(self):
        engine = ContextEngine(
            memory_engine=MockMemoryEngine(),
            kg_engine=MockKGEngine()
        )
        context = await engine.fuse("我想学Python", ...)
        assert len(context) < 50000  # Token限制
```

#### Practice 3: 可观测性

```python
# 添加监控和日志

class ContextEngine:
    async def fuse(self, query, memories, graph, budget):
        # 记录输入
        logger.info({
            "event": "context_fusion_start",
            "query_length": len(query),
            "num_memories": len(memories),
            "num_insights": len(graph)
        })

        start = time.time()

        # ... 融合逻辑 ...

        # 记录输出
        logger.info({
            "event": "context_fusion_complete",
            "context_length": len(context),
            "latency_ms": (time.time() - start) * 1000
        })

        return context
```

#### Practice 4: 渐进式增强

```python
# 从简单开始，逐步增加复杂度

class ContextEngine:
    async def fuse(self, query, memories, graph, budget):
        # Phase 1: 简单拼接
        # context = f"{memories}\n{graph}"

        # Phase 2: 去重
        # context = self._deduplicate(memories, graph)

        # Phase 3: 智能融合（当前）
        context = await self._intelligent_fuse(
            query, memories, graph, budget
        )

        # Phase 4: 个性化（未来）
        # context = await self._personalize(context, user_profile)

        return context
```

---

## 七、业界对照表

### 7.1 术语映射

| 本文档术语 | 业界通用术语 | 说明 |
|-----------|------------|------|
| **Context Engineering** | Context Management, RAG Fusion | 本文档强调"工程化" |
| **Memory Engineering** | Memory Systems, Agent Memory | 本文档强调"工程化" |
| **Knowledge Engineering** | Knowledge Graph, GraphRAG | 本文档强调"工程化" |
| **Memory Consolidation** | Memory Consolidation | ✅ 通用 |
| **Memory Reconsolidation** | Memory Update | 本文档更精确 |
| **Knowledge Evolution** | Dynamic Knowledge Graph | ✅ 通用 |

### 7.2 技术栈对照

| 本文推荐 | 业界替代方案 | 说明 |
|---------|------------|------|
| **LangGraph Checkpointer** | Zep, Mem0 | Memory存储 |
| **PostgreSQL + Vector** | Pinecone, Weaviate | 向量检索 |
| **Neo4j** | ArangoDB, Amazon Neptune | 图数据库 |
| **GraphRAG** | LightRAG, LlamaIndex KG | 图谱构建 |
| **Custom Fusion** | LangChain Chain, DSPy | 上下文融合 |

### 7.3 引用规范

**学术论文引用：**

```bibtex
@article{context_engineering_2025,
  title={Context Engineering: A Framework for LLM Context Management},
  author={[Your Name]},
  journal={arXiv preprint},
  year={2025},
  note={Define "Context Engineering" as the systematic management of LLM context}
}
```

**技术文档引用：**

```markdown
Our system uses **Context Engineering** [1], **Memory Engineering** [2], and **Knowledge Engineering** [3] to provide personalized AI agent experiences.

[1] Context Engineering: Systematic context management for LLMs
[2] Memory Engineering: Engineering practices for AI memory systems
[3] Knowledge Engineering: Modern knowledge graph construction for agents
```

**对外沟通建议：**

- ✅ 对技术人员：使用本文档术语 + 解释
- ✅ 对产品/业务：使用"个性化系统"、"智能记忆"等通俗表述
- ✅ 对投资人：使用"AI Memory System"、"Knowledge Graph"等主流术语

---

## 附录

### A. 快速参考

#### 术语定义速查

| 术语 | 定义 | 核心职责 |
|------|------|---------|
| **Context Engineering** | 上下文工程化 | 融合多源信息，构建最优上下文 |
| **Memory Engineering** | 记忆工程化 | 设计实现记忆系统（存储、检索、巩固） |
| **Knowledge Engineering** | 知识工程化 | 设计实现知识图谱（提取、推理、演化） |

#### 技术选型速查

| 场景 | 推荐方案 |
|------|---------|
| 小团队快速原型 | Mem0 + LightRAG |
| 生产级系统 | LangGraph + GraphRAG + Neo4j |
| 低延迟要求 | Redis + 预计算 + 并行查询 |
| 低预算 | PostgreSQL + Qdrant + Neo4j Community |

### B. 相关资源

**论文：**
- MemGPT: Towards LLMs as Operating Systems (2023)
- GraphRAG: From Local to Global (Microsoft, 2024)
- Memory OS of AI Agent (EMNLP 2025)

**工具：**
- LangChain: https://docs.langchain.com/
- LangGraph: https://github.com/langchain-ai/langgraph
- GraphRAG: https://github.com/microsoft/graphrag
- Neo4j: https://neo4j.com/

**社区：**
- LangChain Discord
- Knowledge Graph Slack
- Agent AI Forum

---

**文档版本历史：**

- v1.0 (2025-01-12): 初始版本，定义三个核心工程术语

**维护者：** [Your Name]
**反馈渠道：** [Your Email/GitHub Issues]
