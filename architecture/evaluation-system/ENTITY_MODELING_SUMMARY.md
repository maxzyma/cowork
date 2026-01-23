# 评估系统实体建模（更落地：Definition + Run 两层模型）

本文档在不大改你现有字段的前提下，把“可配置对象（Definition）”与“一次执行/产物（Run）”拆开，避免 UI/存储层面混淆，并强化可追溯与可复现。

## 0. 实体总览（7个实体）

本系统包含 **7 个核心实体**，每个实体按“两层模型”拆分为 **Definition（配置模板）** 和 **Run（执行记录）**：

| 实体 | Definition 层 | Run 层 | 说明 |
|------|--------------|--------|------|
| **1. Benchmark** | `BenchmarkDefinition` | - | 顶层入口，定义维度/权重，并固定绑定评估任务 |
| **2. Agent** | `AgentDefinition` | `AgentSnapshot`（可选） | 智能体配置 |
| **3. Simulator** | `SimulatorDefinition` | `SimulatorRun` | 仿真器配置 + 一次执行 |
| **4. Dataset Builder** | `DatasetBuilderDefinition` | `DatasetBuildRun` | 数据集构建器 + 一次构建 |
| **5. Evaluation Task** | `EvaluationTaskDefinition` | - | 评估任务/Prompt |
| **6. Evaluation Run** | `EvaluationRunRequest`（参数） | `EvaluationRun` | 评估执行 |
| **7. Result Entry** | - | `results_summary` | Leaderboard 消费的结果条目 |

> **说明**：不是所有实体都需要 Run 层。例如 Benchmark、Agent、Evaluation Task 主要是配置，Run 层用于“有执行过程”的实体（Simulator、Dataset Builder、Evaluation Run）。

---

## 0.1 约定（核心思想）

- **Definition**：用户在页面保存/复用的“配置模板”（可版本化）。
- **Run**：某次实际执行或产出记录（有状态机、时间、错误信息、产物引用）。
- **结果条目**：Leaderboard 消费的 `results_summary`，本质是一个 **Result Entry（结果条目）**，可视为某个 Benchmark 下的一次完整链路 Run 汇总。

> 术语：文中尽量保留你现有字段，例如 `benchmark_name`、`agent_id`、`dataset_id`、`task_id`、`run_id` 等；仅在“Run 层”补充必要的 `*_run_id` 来消除歧义。

---

## 1. Benchmark（顶层入口）

### 1.1 BenchmarkDefinition（配置）

```python
benchmark_definition = {
  "benchmark_id": str,                 # 建议新增：稳定ID（name 可变）
  "benchmark_name": str,
  "benchmark_version": str,            # 建议新增：版本号/快照hash（用于可复现）
  "dimensions": [
    {"dimension": str, "weight": float}
  ],
  "evaluation_task_id": str,           # ✅ 固定绑定：该 benchmark version 对应的评估任务
}
```

### 1.2 BenchmarkView（UI 视图，不是实体）

- Benchmark 页面通常展示：
  - 选择 Agent（运行时参数）
  - Task 为 BenchmarkVersion 固定绑定（不在此处选择）
  - 最近 Runs / 结果列表（来自 ResultEntry/Leaderboard 查询）

---

## 2. Agent

### 2.1 AgentDefinition（配置）

> `password` 不建议明文存储；若必须配置，建议只在前端临时使用，或用 `credential_id` 引用密钥系统。

```python
agent_definition = {
  "agent_id": str,
  "agent_name": str,
  "url": str,
  "account": str,
  "password": str,                     # ⚠️ 建议替换为 credential_id，或明确“不落库”
  "agent_card": dict | None
}
```

### 2.2 AgentSnapshot（Run 层快照，建议）

```python
agent_snapshot = {
  "agent_id": str,
  "agent_name": str,
  "url": str,
  "account": str,
  "agent_card": dict | None,
  "agent_version": str | None          # 可选：配置hash/版本号
}
```

---

## 3. Simulator（UI 自动化/仿真）

### 3.1 SimulatorDefinition（配置）

> “角色库”在实际场景里是 **Langfuse Prompt 上存放的一批角色画像 markdown 内容**。因此建模为对 Langfuse prompt 的引用，并在 Run/结果里记录版本以保证可复现。

```python
simulator_definition = {
  "simulator_id": str,
  "environment": str,                  # windows_runner_pool（远端预装evalkit的Windows机器池） | local
  "config": {
    "agent_id": str,
    "automation_script_git_url": str,
    "role_library": {
      "provider": str,                 # e.g. "langfuse"
      "prompt_id": str,                # Langfuse prompt id/name（角色画像集合）
      "prompt_version": str | None,    # 建议：固定版本/commit（用于可复现）
      "labels": list[str] | None       # 可选：Langfuse labels / tags
    },
    "runner_pool_id": str | None,      # 可选：指定使用哪一组Windows runner（environment=windows_runner_pool 时）
    "output_language": str
  }
}
```

### 3.2 SimulatorRun（一次执行）

```python
simulator_run = {
  "simulator_run_id": str,             # 建议新增：Run 的稳定ID
  "simulator_id": str,
  "environment": str,                  # windows_runner_pool | local（记录实际执行环境，便于排障/统计）
  "runner_id": str | None,             # 可选：若在远端机器池执行，记录实际分配到的Windows机器
  "status": str,                       # queued | running | success | failed | canceled
  "created_at": str,                   # ISO8601，如 2026-01-21T13:45:30Z（UTC 时间，Z 表示零时区）
  "started_at": str | None,
  "finished_at": str | None,
  "error": {
    "error_code": str | None,
    "error_message": str | None
  } | None,
  "outputs": {
    "session_ids": list[str]
  }
}
```

---

## 4. Dataset Builder（结构化数据集构建）

### 4.1 DatasetBuilderDefinition（配置）

```python
dataset_builder_definition = {
  "builder_id": str,
  "builder_name": str,
  "provider": str,                     # benchmark_owner / third_party（可选：标识提供方）
  "api": {
    "base_url": str,                   # e.g. https://builder.example.com
    "build_endpoint": str,             # e.g. /v1/build_dataset
    "timeout_ms": int | None,
    "auth_ref": str | None             # ✅ 不在文档里放 token；引用 credential_id / secret key
  },
  "contract": {
    "input_spec_version": str | None,  # 输入schema版本（便于升级兼容）
    "output_spec_version": str | None  # 输出schema版本（对应 evaluation_task 期望）
  } | None
}
```

### 4.2 DatasetBuildRun（一次构建）

> 你原文把 `inputs/outputs` 放在 builder 实体里；更落地的做法是把它们放到 Run 里。

```python
dataset_build_run = {
  "dataset_build_run_id": str,         
  "builder_id": str,
  "status": str,                       # queued | running | success | failed | canceled
  "created_at": str,
  "inputs": {
    "session_ids": list[str],
    "simulator_run_id": str | None     # 可选：追溯这批 session 来自哪次仿真
  },
  "outputs": {
    "dataset_id": str,                 # 结构化数据集ID（供 EvaluationRun 引用）
    "langfuse_dataset": {
      "dataset_id": str,               # Langfuse dataset id/name
      "item_count": int | None,        # 可选：写入条数
    }
  },
  "artifacts": {
    "raw_ref": str | None              # 可选：对象存储引用
  } | None
}
```

---

## 5. Evaluation Task（评估任务/Prompt）

### 5.1 EvaluationTaskDefinition（配置）

```python
evaluation_task_definition = {
  "task_id": str,
  "task_name": str,
  "evaluation_prompt": str,
  "prompt_ref": {
    "provider": str,                   # "langfuse"
    "prompt_label": str                # ✅ 用 label 获取 prompt（目前的实际方式）
  }
}
```

---

## 6. Evaluation Run（对结构化数据集执行评估）

### 6.1 EvaluationRunDefinition（“请求”/参数）

> 你原文的 `evaluation_run` 更像“发起一次评估的参数”；在两层模型里它归为 Run 的输入（Definition 层可选做模板）。

```python
evaluation_run_request = {
  "dataset_id": str,
  "task_id": str
}
```

### 6.2 EvaluationRun（一次评估）

```python
evaluation_run = {
  "evaluator_run_id": str,             # 用这个做真正的评估run id（避免与结果 run_id 冲突）
  "status": str,                       # queued | running | success | failed | canceled
  "created_at": str,
  "inputs": {
    "dataset_id": str,
    "task_id": str
  },
  "outputs": {
    "raw_results_ref": str | None      # 原始评估结果引用
  },
  "error": {
    "error_code": str | None,
    "error_message": str | None
  } | None
}
```

---

## 7. Result Entry（Leaderboard 消费的结果条目 = `results_summary`）

### 7.1 设计要点（把语义拆清楚）

- **`run_id`**：建议作为 **ResultEntry 的主键**（也就是“上榜条目ID”），不再模糊表示“评估run”。
- `inputs.evaluation_run.evaluator_run_id`：指向真正的 `evaluation_run.evaluator_run_id`。
- `scores.dimensions[].weight`：建议写入 **当次 Benchmark 的权重快照**（即使后续 benchmark 改了，也不影响历史可复现）。

### 7.2 `results_summary`（保持原结构，补充少量可复现字段）

```python
results_summary = {
  "run_id": str,                        # ✅ 结果条目ID（Leaderboard Entry ID）
  "benchmark_name": str,
  "benchmark_version": str | None,      # 本次使用的benchmark快照/版本
  "agent": {
    "agent_name": str,
    "agent_id": str | None,
    "agent_card": dict | None,
    "agent_version": str | None         # 本次使用的agent快照/版本
  },
  "status": str,                        # running | success | failed
  "created_at": str,                    # ISO8601
  "inputs": {
    "simulator": {
      "simulator_id": str | None,
      "simulator_run_id": str | None,   # 指向 SimulatorRun
      "session_ids": list[str]
    },
    "dataset": {
      "dataset_id": str | None,
      "dataset_build_run_id": str | None  # 指向 DatasetBuildRun
    },
    "evaluation_task": {
      "task_id": str | None,
      "task_name": str,
      "prompt_label": str | None        # ✅ 用 label 获取 prompt（与 EvaluationTaskDefinition 对齐）
    },
    "evaluation_run": {
      "evaluator_run_id": str | None    # 指向 EvaluationRun
    }
  },
  "scores": {
    "overall_score": float,
    "dimensions": [
      {
        "dimension": str,
        "weight": float,
        "score": float
      }
    ]
  },
  "breakdown": {
    "per_session": [
      {
        "session_id": str,
        "score": float | None,
        "dimension_scores": dict[str, float] | None
      }
    ]
  },
  "artifacts": {
    "report_url": str | None,  # 面向人的评测报告入口（比如一页汇总报告、可视化页面、标注页面
  }
}
```

---

## 8. UI 落地建议（最小闭环）

- **Benchmark 页面（顶层）**：
  - 选择 `BenchmarkDefinition`（其 `evaluation_task_id` 固定绑定到 `EvaluationTaskDefinition`）
  - 运行时选择 `AgentDefinition`、`SimulatorDefinition`、`DatasetBuilderDefinition`
  - 依次发起 `SimulatorRun` → `DatasetBuildRun` → `EvaluationRun`
  - 生成/写入 `results_summary`（ResultEntry），供 Leaderboard 查询展示
- **Leaderboard 页面**：
  - 只消费 `results_summary`（ResultEntry）列表；Leaderboard 本身不必作为“存储实体”


