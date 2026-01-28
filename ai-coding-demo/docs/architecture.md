# 项目架构文档

## 系统架构概述

本项目采用**领域驱动设计（DDD）**和**六边形架构（端口和适配器）**原则，实现清晰关注点分离和高度可测试性。

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│                     (FastAPI + Pydantic)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Routes     │  │ Controllers  │  │ Middleware   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                      Domain Layer                           │
│                   (Business Logic)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Models     │  │  Services    │  │ Repositories │     │
│  │  (Entities)  │  │  (Business)  │  │  (Interfaces)│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Infrastructure Layer                       │
│              (External Dependencies)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Database    │  │    Cache     │  │    Email     │     │
│  │  (PostgreSQL)│  │   (Redis)    │  │  (SMTP/SendGrid)│   │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 层次结构

### 1. API Layer (接口层)

**职责**:
- 处理 HTTP 请求和响应
- 请求验证和序列化
- 路由定义
- 中间件处理（认证、日志、错误处理）

**关键组件**:
```python
src/api/
├── main.py              # FastAPI 应用入口
├── routes/              # 路由定义
│   ├── __init__.py
│   ├── auth.py         # 认证相关路由
│   └── users.py        # 用户管理路由
├── controllers/         # 控制器（协调领域服务）
├── middleware/          # 中间件
│   ├── auth.py         # 认证中间件
│   ├── logging.py      # 日志中间件
│   └── error_handler.py # 错误处理
└── schemas/            # Pydantic 模型（请求/响应）
```

**示例**:
```python
# src/api/routes/users.py
from fastapi import APIRouter, Depends
from src.api.schemas.user import UserCreate, UserResponse
from src.domain.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    user_service: Depends(get_user_service)
):
    """创建新用户"""
    result = user_service.register_user(**user_data.dict())
    return UserResponse.from_domain(result)
```

### 2. Domain Layer (领域层)

**职责**:
- 封装核心业务逻辑
- 定义领域模型和实体
- 定义业务规则和约束
- 定义仓储接口

**关键组件**:
```python
src/domain/
├── models/              # 领域模型
│   └── user.py         # 用户实体
├── services/            # 领域服务
│   └── user_service.py # 用户服务
├── repositories/        # 仓储接口
│   └── user_repository.py
├── exceptions.py        # 领域异常
└── value_objects/       # 值对象（可选）
```

**设计原则**:
- **纯净的领域层**: 不依赖任何外部框架
- **业务规则集中**: 所有业务逻辑在领域层
- **接口隔离**: 通过接口定义依赖，便于测试

**示例**:
```python
# src/domain/services/user_service.py
class UserService:
    def __init__(
        self,
        user_repository: UserRepository,  # 接口
        email_service: EmailService,
        rate_limiter: RateLimiter
    ):
        self.user_repository = user_repository
        self.email_service = email_service
        self.rate_limiter = rate_limiter

    def register_user(self, username: str, email: str, password: str):
        # 业务逻辑
        self._validate_username(username)
        self._check_username_availability(username)
        # ...
```

### 3. Infrastructure Layer (基础设施层)

**职责**:
- 实现领域层定义的接口
- 与外部系统集成
- 数据持久化
- 技术实现细节

**关键组件**:
```python
src/infrastructure/
├── database/            # 数据库实现
│   ├── postgresql.py   # PostgreSQL 实现
│   ├── models.py       # SQLAlchemy ORM 模型
│   └── repositories/   # 仓储实现
│       └── user_repository_impl.py
├── cache/              # 缓存实现
│   └── redis.py        # Redis 实现
├── email/              # 邮件服务
│   └── smtp.py         # SMTP 实现
├── logging/            # 日志实现
│   └── structlog.py    # Structlog 实现
└── rate_limiter/       # 速率限制
    └── redis.py        # Redis 实现
```

**示例**:
```python
# src/infrastructure/database/repositories/user_repository_impl.py
from src.domain.repositories.user_repository import UserRepository

class PostgresUserRepository(UserRepository):
    def __init__(self, db_session):
        self.db = db_session

    def create(self, user: User) -> User:
        # 具体的数据库操作
        db_user = UserModel.from_domain(user)
        self.db.add(db_user)
        self.db.commit()
        return db_user.to_domain()
```

## 数据流

### 请求处理流程

```
1. HTTP Request
   ↓
2. API Layer (FastAPI Router)
   ↓
3. Request Validation (Pydantic Schema)
   ↓
4. Controller (调用领域服务)
   ↓
5. Domain Service (业务逻辑)
   ↓
6. Repository Interface
   ↓
7. Infrastructure Implementation
   ↓
8. Database/External Service
   ↓
9. Response (反向流回)
```

### 示例：用户注册流程

```
POST /api/v1/auth/register
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}

↓ FastAPI Router 接收请求

↓ Pydantic 验证请求数据

↓ AuthController.register()

↓ UserService.register_user()
   ├─ 验证用户名 (领域规则)
   ├─ 检查用户名可用性 (Repository)
   ├─ 验证邮箱格式 (领域规则)
   ├─ 检查邮箱可用性 (Repository)
   ├─ 密码加密 (基础设施)
   ├─ 创建用户实体 (领域模型)
   ├─ 保存到数据库 (Repository)
   └─ 发送验证邮件 (基础设施)

↓ 返回 UserRegistrationResult

↓ 转换为响应模型

↓ HTTP Response (201 Created)
{
  "user_id": "usr_abc123",
  "username": "john_doe",
  "email": "john@example.com",
  "token": "eyJhbG..."
}
```

## 测试架构

### 测试金字塔

```
           /\
          / E2E \        10% - 关键用户路径
         /--------\
        /Integration\    20% - API和数据库集成
       /--------------\
      /    Unit Tests \  70% - 业务逻辑测试
     /------------------\
```

### 单元测试（70%）

**测试范围**:
- 领域服务业务逻辑
- 值对象验证规则
- 实体行为

**特点**:
- 快速执行
- 无外部依赖（全部 Mock）
- 高覆盖率

**示例**:
```python
# tests/unit/domain/test_user_service.py
class TestUserService:
    def test_register_user_with_duplicate_username_raises_error(self):
        # Given
        mock_repo = Mock()
        mock_repo.find_by_username.return_value = User(...)
        service = UserService(mock_repo, ...)

        # When/Then
        with pytest.raises(ConflictError):
            service.register_user(username="existing", ...)
```

### 集成测试（20%）

**测试范围**:
- API 端点
- 数据库集成
- 缓存集成

**特点**:
- 使用真实数据库（测试环境）
- 测试容器化（TestContainers）

**示例**:
```python
# tests/integration/api/test_user_api.py
@pytest.mark.integration
class TestUserAPI:
    def test_register_user_endpoint(self, client, db_session):
        response = client.post("/api/v1/auth/register", json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "TestPass123"
        })
        assert response.status_code == 201
```

### E2E 测试（10%）

**测试范围**:
- 完整用户流程
- 多服务交互

**特点**:
- 完整环境
- 真实服务（或高度仿真）

## 部署架构

### 生产环境

```
┌─────────────┐
│   Nginx     │  ← 反向代理 + SSL终止
└──────┬──────┘
       │
┌──────▼──────┐
│  Gunicorn   │  ← 应用服务器（多Worker）
│  FastAPI    │
└──────┬──────┘
       │
┌──────▼──────┐    ┌──────────┐
│ PostgreSQL  │◄──►│ Redis    │
│  (Primary)  │    │  Cache   │
└─────────────┘    └──────────┘
       │
┌──────▼──────┐
│ PostgreSQL  │  ← 只读副本
│ (Replica)   │
└─────────────┘
```

### 容器化部署

```yaml
# docker-compose.prod.yml
services:
  app:
    image: myapp:${VERSION}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
    environment:
      - DATABASE_URL=${PROD_DB_URL}

  postgres:
    image: postgres:15
    volumes:
      - pg_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data
```

## 安全架构

### 认证和授权

```
┌────────────┐
│  Client    │
└─────┬──────┘
      │ 1. POST /auth/login
      │    {username, password}
      ↓
┌─────▼──────┐
│ API Layer  │
│ - 验证凭证  │
│ - 生成 JWT  │
└─────┬──────┘
      │ 2. JWT Token
      ↓
┌─────▼──────────┐
│ Subsequent     │
│ Requests       │
│ - Header:      │
│   Authorization│
│   : Bearer <JWT>│
└─────┬──────────┘
      │
┌─────▼──────┐
│ Middleware │
│ - 验证 JWT  │
│ - 提取用户  │
└─────┬──────┘
      │
┌─────▼──────┐
│ Controller │
│ - 授权检查  │
└────────────┘
```

### 数据安全

- **传输加密**: HTTPS/TLS 1.3
- **密码存储**: bcrypt (cost factor 12)
- **敏感数据**: 数据库字段加密
- **审计日志**: 所有关键操作记录

## 可观测性

### 监控指标

```
┌─────────────────────────────────────┐
│         Prometheus                  │
│  - 收集应用指标                      │
│  - 收集基础设施指标                  │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────┐
│     Grafana         │
│  - 可视化仪表板      │
│  - 告警规则         │
└─────────────────────┘
```

**关键指标**:
- 请求速率和延迟
- 错误率
- 数据库连接池
- 缓存命中率
- 业务指标（注册数、活跃用户等）

### 日志

```
结构化日志 (JSON格式)
{
  "timestamp": "2026-01-28T10:30:00Z",
  "level": "INFO",
  "logger": "src.domain.services.user_service",
  "message": "User registration successful",
  "context": {
    "user_id": "usr_abc123",
    "username": "john_doe",
    "ip_address": "1.2.3.4"
  }
}
```

### 分布式追踪

```
OpenTelemetry ← 分布式追踪
├─ Trace ID: 追踪整个请求链路
├─ Span ID: 标识单个操作
└─ Context: 传递上下文信息
```

## 扩展性

### 水平扩展

- **无状态应用**: 可以任意增减实例
- **负载均衡**: Nginx + Gunicorn Workers
- **数据库分片**: 按用户ID哈希
- **缓存集群**: Redis Cluster

### 垂直扩展

- **资源限制**: CPU/Memory 限制
- **连接池**: 数据库连接池优化
- **缓存策略**: 多级缓存

## 技术选型

| 组件 | 技术选择 | 理由 |
|-----|---------|------|
| Web框架 | FastAPI | 高性能、异步、类型安全 |
| 数据库 | PostgreSQL | 可靠、功能丰富、ACID |
| 缓存 | Redis | 高性能、丰富数据结构 |
| ORM | SQLAlchemy | 成熟、灵活 |
| 测试 | pytest | 强大、易用 |
| 容器 | Docker | 标准化、可移植 |

## 最佳实践

1. **依赖倒置**: 高层模块不依赖低层模块，都依赖抽象
2. **单一职责**: 每个类只负责一件事
3. **接口隔离**: 定义细粒度接口
4. **开闭原则**: 对扩展开放，对修改关闭
5. **测试驱动**: 保持高测试覆盖率

## 参考资源

- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design by Eric Evans](https://www.domainlanguage.com/ddd/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
