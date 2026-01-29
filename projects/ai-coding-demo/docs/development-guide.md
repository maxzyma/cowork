# 开发指南

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd ai-coding-demo

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动数据库
docker-compose up -d postgres redis

# 运行数据库迁移
python scripts/migrate.py
```

### 2. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单元测试
pytest tests/unit/ -v

# 运行集成测试
pytest tests/integration/ -v

# 生成覆盖率报告
pytest tests/ --cov=src/ --cov-report=html
```

### 3. 启动开发服务器

```bash
# 开发模式（自动重载）
uvicorn src.api.main:app --reload --port 8000

# 或使用 Docker
docker-compose up app
```

## 开发流程

### SDD（规范驱动开发）流程

1. **编写规范**
   ```bash
   # 复制规范模板
   cp specs/templates/feature-spec-template.md specs/features/SPEC-XXX-001-new-feature.md

   # 填写规范内容
   # ...
   ```

2. **验证规范**
   ```bash
   python scripts/spec-validator.py validate specs/
   ```

3. **生成测试**（基于规范）
   ```bash
   # 测试文件命名: tests/unit/domain/test_<feature>.py
   # 参考: tests/unit/domain/test_user_registration.py
   ```

4. **实现功能**
   ```bash
   # 实现文件命名: src/domain/services/<feature>_service.py
   # 参考: src/domain/services/user_service.py
   ```

5. **验证同步**
   ```bash
   python scripts/spec-validator.py check-sync specs/ src/
   ```

### TDD（测试驱动开发）流程

```bash
# 1. 编写测试（红）
pytest tests/unit/domain/test_user_registration.py -v  # 失败

# 2. 实现功能（绿）
# 编辑 src/domain/services/user_service.py
pytest tests/unit/domain/test_user_registration.py -v  # 通过

# 3. 重构（重构）
# 优化代码结构
pytest tests/unit/domain/test_user_registration.py -v  # 仍然通过
```

## 项目结构说明

```
ai-coding-demo/
├── specs/              # 规范文档（单一真实来源）
│   ├── features/       # 功能规范
│   ├── apis/          # API 规范
│   └── data-models/   # 数据模型规范
├── src/               # 源代码
│   ├── api/           # API 层（FastAPI 路由、控制器）
│   ├── domain/        # 领域层（业务逻辑）
│   ├── infrastructure/ # 基础设施层（数据库、缓存等）
│   └── utils/         # 工具函数
└── tests/             # 测试
    ├── unit/          # 单元测试（70%）
    ├── integration/   # 集成测试（20%）
    └── e2e/           # E2E 测试（10%）
```

## 代码规范

### Python 代码风格

- 使用 Black 格式化代码
- 使用 Flake8 检查代码风格
- 使用 Pylint 检查代码质量
- 使用 MyPy 进行类型检查

```bash
# 格式化代码
black src/ tests/

# 检查风格
flake8 src/ tests/

# 类型检查
mypy src/
```

### 命名约定

- **类名**: PascalCase (例: UserService)
- **函数/方法**: snake_case (例: register_user)
- **常量**: UPPER_SNAKE_CASE (例: RESERVED_USERNAMES)
- **私有方法**: _leading_underscore (例: _validate_username)

### 文档字符串

使用 Google 风格的文档字符串：

```python
def register_user(self, username: str, email: str, password: str) -> User:
    """
    注册新用户

    实现规范: SPEC-USER-001, 2.1 核心功能

    Args:
        username: 用户名（3-20字符）
        email: 邮箱地址
        password: 密码（8-128字符）

    Returns:
        User: 注册的用户对象

    Raises:
        ValidationError: 输入验证失败
        ConflictError: 用户名或邮箱已存在
    """
```

## 测试编写指南

### 单元测试结构

```python
class TestFeature:
    """功能测试套件"""

    def setup_method(self):
        """每个测试方法前的设置"""
        pass

    def teardown_method(self):
        """每个测试方法后的清理"""
        pass

    def test_success_case(self):
        """测试成功场景"""
        # Given: 准备测试数据
        # When: 执行被测试功能
        # Then: 验证结果
        pass

    def test_error_case(self):
        """测试错误场景"""
        pass
```

### 测试命名规范

使用描述性的测试名称：

```python
# ✅ 好
def test_user_registration_with_duplicate_email_raises_conflict_error(self):
    pass

# ❌ 不好
def test_conflict(self):
    pass
```

## 规范编写指南

### 规范文档结构

每个规范文档应包含：

1. **元数据**: ID、版本、状态、负责人
2. **需求概述**: 业务背景、用户价值、成功标准
3. **功能描述**: 核心功能、用户交互、边缘情况
4. **技术规范**: API接口、数据模型、业务规则
5. **非功能需求**: 性能、安全、可观测性
6. **验收标准**: 功能测试、性能测试、安全测试

### 规范状态管理

- **Draft**: 草稿，正在编写中
- **Review**: 评审中，等待团队反馈
- **Approved**: 已批准，可以开始实现
- **Implemented**: 已实现，等待验收

## Git 工作流

### 分支策略

- `main`: 生产分支，始终保持稳定
- `develop`: 开发分支，集成最新功能
- `feature/SPEC-XXX`: 功能分支，基于规范开发
- `bugfix/XXX`: 修复分支

### 提交消息规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 重构
- `chore`: 构建/工具相关

示例：
```
feat(user): add user registration feature

Implement SPEC-USER-001 user registration functionality
including email verification and rate limiting.

Closes #123
```

### Pull Request 流程

1. 创建功能分支
2. 完成开发并通过所有测试
3. 创建 PR，关联到规范文档
4. 代码审查
5. CI/CD 通过后合并

## 调试技巧

### 使用 IPDB 调试

```python
import ipdb; ipdb.set_trace()  # 设置断点
```

### 查看日志

```bash
# 查看应用日志
docker-compose logs -f app

# 查看数据库日志
docker-compose logs -f postgres
```

### 数据库调试

```bash
# 连接到数据库
docker-compose exec postgres psql -U user -d ai_coding_demo

# 查询用户表
SELECT * FROM users WHERE username = 'test_user';
```

## 常见问题

### Q: 如何添加新的功能规范？

A:
1. 复制模板 `specs/templates/feature-spec-template.md`
2. 创建新规范文件 `specs/features/SPEC-XXX-001-feature-name.md`
3. 填写规范内容
4. 运行 `python scripts/spec-validator.py validate specs/` 验证

### Q: 如何确保测试覆盖率？

A:
```bash
# 查看覆盖率报告
pytest tests/ --cov=src/ --cov-report=term-missing

# 生成HTML报告
pytest tests/ --cov=src/ --cov-report=html
open htmlcov/index.html
```

### Q: 如何处理数据库迁移？

A:
```bash
# 创建迁移
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 相关资源

- [AI Coding 驱动开发范式](../docs/ai-coding-driven-development-paradigm.md)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [pytest 文档](https://docs.pytest.org/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
