# API 文档

## 概述

用户管理服务提供 RESTful API 用于用户注册、管理和认证。

**Base URL**: `http://localhost:8000`

**API Version**: v1.0.0

## 认证

当前版本支持未认证的用户注册。后续版本将添加 JWT 认证。

## 端点

### 健康检查

#### GET /health

检查服务健康状态。

**响应示例**:

```json
{
  "status": "healthy",
  "service": "user-management",
  "dependencies": []
}
```

**状态码**:
- `200 OK`: 服务健康

---

### 用户注册

#### POST /api/v1/users/register

注册新用户。

**请求头**:
```
Content-Type: application/json
```

**请求体**:

```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "username": "johndoe"
}
```

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| email | string (email) | ✅ | 用户邮箱，必须唯一 |
| password | string | ✅ | 密码，最少8字符 |
| username | string | ❌ | 用户名，3-50字符，如果提供必须唯一 |

**响应示例** (200 OK):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2026-01-28T10:30:00Z"
}
```

**错误响应**:

**400 Bad Request** - 输入验证失败
```json
{
  "error": "VALIDATION_ERROR",
  "detail": "Password must contain at least one uppercase letter"
}
```

**409 Conflict** - 用户已存在
```json
{
  "error": "USER_ALREADY_EXISTS",
  "detail": "User with email 'user@example.com' already exists"
}
```

**500 Internal Server Error** - 服务器错误
```json
{
  "error": "INTERNAL_ERROR",
  "detail": "An unexpected error occurred"
}
```

---

### 获取用户信息

#### GET /api/v1/users/{user_id}

获取指定用户的信息。

**路径参数**:

| 参数 | 类型 | 描述 |
|------|------|------|
| user_id | UUID | 用户ID |

**响应示例** (200 OK):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2026-01-28T10:30:00Z"
}
```

**错误响应**:

**404 Not Found** - 用户不存在
```json
{
  "error": "USER_NOT_FOUND",
  "detail": "User with id 'xxx' not found"
}
```

**注意**: 此端点尚未实现，返回 501

---

## 数据模型

### User

```typescript
{
  id: UUID;           // 用户唯一标识
  email: string;      // 用户邮箱
  username?: string;  // 用户名（可选）
  is_active: boolean; // 账户是否激活
  created_at: string; // 创建时间（ISO 8601）
}
```

### ErrorResponse

```typescript
{
  error: string;   // 错误代码
  detail: string;  // 错误详情
}
```

---

## 错误代码

| 错误代码 | HTTP 状态码 | 描述 |
|----------|------------|------|
| VALIDATION_ERROR | 400 | 输入验证失败 |
| USER_ALREADY_EXISTS | 409 | 用户已存在 |
| USER_NOT_FOUND | 404 | 用户不存在 |
| INTERNAL_ERROR | 500 | 服务器内部错误 |
| DOMAIN_ERROR | 500 | 领域逻辑错误 |

---

## 使用示例

### cURL

```bash
# 注册用户
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "username": "johndoe"
  }'

# 健康检查
curl http://localhost:8000/health
```

### Python (requests)

```python
import requests

# 注册用户
response = requests.post(
    "http://localhost:8000/api/v1/users/register",
    json={
        "email": "user@example.com",
        "password": "SecurePass123",
        "username": "johndoe"
    }
)

user = response.json()
print(user)
```

### JavaScript (fetch)

```javascript
// 注册用户
fetch('http://localhost:8000/api/v1/users/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123',
    username: 'johndoe'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 限流

当前版本未实现速率限制。后续版本将添加：

- 每IP每分钟最多 100 次请求
- 注册端点额外限制：每IP每小时 10 次

---

## 版本历史

- **v1.0.0** (2026-01-28): 初始版本
  - 用户注册
  - 健康检查

---

## 交互式文档

访问以下地址查看交互式 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 相关文档

- [功能规范](../specs/features/SPEC-USER-001-registration.md)
- [架构文档](./architecture.md)
- [部署指南](./deployment.md)
