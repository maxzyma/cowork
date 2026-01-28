# AI Coding 驱动开发 Demo 项目

## 项目简介

这是一个展示 **AI Coding 驱动开发范式** 的示例项目，实现了一个用户管理服务（User Management Service），完整演示从规范到测试到实现的全生命周期开发流程。

## 核心理念

- **SDD (Specification-Driven Development)**: 规范驱动开发
- **AI-Enhanced TDD**: AI 增强的测试驱动开发
- **CI/CS**: 持续集成与持续规范验证

## 项目结构

```
ai-coding-demo/
├── specs/                          # 规范文档（单一真实来源）
│   ├── features/                   # 功能规范
│   │   ├── SPEC-USER-001-registration.md
│   │   ├── SPEC-USER-002-authentication.md
│   │   └── SPEC-USER-003-profile.md
│   ├── apis/                       # API 接口规范
│   │   └── user-api-spec.md
│   ├── data-models/               # 数据模型规范
│   │   └── user-model-spec.md
│   └── templates/                 # 规范模板
│       ├── feature-spec-template.md
│       ├── api-spec-template.md
│       └── data-model-spec-template.md
│
├── src/                           # 源代码
│   ├── api/                       # API 层
│   │   ├── routes/                # 路由定义
│   │   ├── controllers/           # 控制器
│   │   └── middleware/            # 中间件
│   ├── domain/                    # 领域层
│   │   ├── models/                # 领域模型
│   │   ├── services/              # 领域服务
│   │   └── repositories/          # 仓储接口
│   ├── infrastructure/            # 基础设施层
│   │   ├── database/              # 数据库实现
│   │   ├── cache/                 # 缓存实现
│   │   └── logging/               # 日志实现
│   └── utils/                     # 工具函数
│
├── tests/                         # 测试套件
│   ├── unit/                      # 单元测试（70%）
│   │   ├── domain/
│   │   ├── api/
│   │   └── utils/
│   ├── integration/               # 集成测试（20%）
│   │   ├── api/
│   │   └── database/
│   └── e2e/                       # 端到端测试（10%）
│       └── user-workflows/
│
├── .github/                       # GitHub 配置
│   └── workflows/
│       ├── ci-cs-pipeline.yml     # CI/CS 管道
│       └── spec-validation.yml    # 规范验证
│
├── docs/                          # 文档
│   ├── architecture.md            # 架构文档
│   ├── development-guide.md       # 开发指南
│   └── api-documentation.md       # API 文档（自动生成）
│
├── scripts/                       # 工具脚本
│   ├── spec-validator.py          # 规范验证器
│   ├── test-generator.py          # 测试生成器
│   └── setup-dev.sh              # 开发环境设置
│
├── config/                        # 配置文件
│   ├── development.yml
│   ├── production.yml
│   └── test.yml
│
├── package.json                   # 项目依赖
├── requirements.txt               # Python 依赖
├── docker-compose.yml            # Docker 配置
└── Dockerfile                    # Docker 镜像定义

```

## 开发流程演示

### 阶段 1: 规范编写 (Specification Writing)

1. 从需求出发，编写功能规范
2. 定义 API 接口规范
3. 设计数据模型规范
4. AI 辅助审查和完善规范

示例：`specs/features/SPEC-USER-001-registration.md`

### 阶段 2: 测试生成 (Test Generation)

1. 基于规范自动生成测试用例
2. AI 生成测试代码
3. 覆盖单元测试、集成测试、E2E 测试

示例：`tests/unit/domain/test_user_registration.py`

### 阶段 3: 代码实现 (Implementation)

1. AI 根据规范和测试生成代码
2. 代码审查和优化
3. 确保所有测试通过

示例：`src/domain/services/user_service.py`

### 阶段 4: CI/CS 验证 (Continuous Integration/Specification)

1. 规范变更触发自动验证
2. 代码和规范同步检查
3. 自动化测试执行
4. 部署准备

## 快速开始

### 环境准备

```bash
# 安装依赖
npm install
pip install -r requirements.txt

# 设置开发环境
./scripts/setup-dev.sh

# 启动数据库
docker-compose up -d
```

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 运行 E2E 测试
pytest tests/e2e/
```

### 启动服务

```bash
# 开发模式
npm run dev

# 生产模式
npm run start
```

### 规范验证

```bash
# 验证所有规范
python scripts/spec-validator.py validate specs/

# 检查规范和代码同步
python scripts/spec-validator.py check-sync specs/ src/
```

## 核心功能演示

### 1. 用户注册 (User Registration)

- **规范**: `specs/features/SPEC-USER-001-registration.md`
- **测试**: `tests/unit/domain/test_user_registration.py`
- **实现**: `src/domain/services/user_service.py`

### 2. 用户认证 (User Authentication)

- **规范**: `specs/features/SPEC-USER-002-authentication.md`
- **测试**: `tests/unit/domain/test_user_authentication.py`
- **实现**: `src/domain/services/auth_service.py`

### 3. 用户资料管理 (User Profile Management)

- **规范**: `specs/features/SPEC-USER-003-profile.md`
- **测试**: `tests/unit/domain/test_user_profile.py`
- **实现**: `src/domain/services/profile_service.py`

## 技术栈

- **后端**: Python (FastAPI) / Node.js (Express)
- **数据库**: PostgreSQL
- **缓存**: Redis
- **测试**: pytest / Jest
- **CI/CD**: GitHub Actions
- **容器化**: Docker

## 度量指标

项目跟踪以下关键指标：

- **测试覆盖率**: 目标 95%+
- **规范覆盖率**: 100%（所有代码都有对应规范）
- **CI/CD 成功率**: 目标 98%+
- **平均交付周期**: 从规范到部署的时间

## AI 辅助工具

- **规范生成**: AI 辅助生成结构化规范
- **测试生成**: 根据规范自动生成测试用例
- **代码生成**: 基于规范和测试生成实现代码
- **代码审查**: AI 辅助代码质量和安全检查

## 学习资源

- [AI Coding 驱动开发范式文档](../docs/ai-coding-driven-development-paradigm.md)
- [开发指南](docs/development-guide.md)
- [架构设计](docs/architecture.md)

## 贡献指南

1. 所有功能开发从规范开始
2. 规范变更需要团队评审
3. 代码必须有对应的测试
4. 遵循测试金字塔原则（70% 单元 / 20% 集成 / 10% E2E）
5. 所有 PR 必须通过 CI/CS 管道

## 许可证

MIT License

---

**文档版本**: 1.0
**创建日期**: 2026-01-28
**维护者**: AI Research Team
