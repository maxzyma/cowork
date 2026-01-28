# 功能规范: 用户注册

## 元数据

- **ID**: SPEC-USER-001
- **版本**: 1.0
- **状态**: Approved
- **负责人**: AI Research Team
- **创建日期**: 2026-01-28
- **最后更新**: 2026-01-28
- **相关规范**:
  - SPEC-USER-002 (用户认证)
  - SPEC-API-USER-001 (用户 API)
  - SPEC-DATA-USER-001 (用户数据模型)

## 1. 需求概述

### 1.1 业务背景

用户管理系统需要提供安全、可靠的用户注册功能，允许新用户创建账户并开始使用系统服务。

### 1.2 用户价值

- 快速简便的注册流程
- 安全的账户创建
- 清晰的错误提示和指导
- 邮箱验证确保账户安全

### 1.3 成功标准

- 注册成功率 > 95%
- 平均注册时间 < 2分钟
- 邮箱验证率 > 80%
- 零安全漏洞

## 2. 功能描述

### 2.1 核心功能

用户通过提供以下信息完成注册：
1. 用户名（唯一标识）
2. 邮箱地址（用于验证和通知）
3. 密码（强密码策略）
4. 可选：姓名、电话等补充信息

注册流程：
1. 用户提交注册信息
2. 系统验证信息格式和唯一性
3. 创建用户账户（密码加密存储）
4. 发送邮箱验证邮件
5. 返回注册成功响应（包含临时 token）

### 2.2 用户交互

**注册页面**:
- 清晰的表单布局
- 实时输入验证反馈
- 密码强度指示器
- 用户协议和隐私政策链接

**验证邮件**:
- 包含验证链接（24小时有效）
- 友好的邮件模板
- 重新发送验证邮件选项

### 2.3 边缘情况处理

1. **用户名已存在**
   - 场景: 用户尝试使用已被占用的用户名
   - 预期行为: 返回 409 错误，提示用户名已被使用，建议可用的替代用户名

2. **邮箱已注册**
   - 场景: 用户尝试使用已注册的邮箱
   - 预期行为: 返回 409 错误，提示邮箱已注册，提供找回密码链接

3. **密码强度不足**
   - 场景: 用户提供的密码不符合安全策略
   - 预期行为: 返回 400 错误，明确列出密码要求

4. **邮箱格式无效**
   - 场景: 用户输入的邮箱格式不正确
   - 预期行为: 返回 400 错误，提示正确的邮箱格式

5. **系统过载**
   - 场景: 短时间内大量注册请求
   - 预期行为: 实施速率限制，返回 429 错误

## 3. 技术规范

### 3.1 API 接口

#### 端点1: POST /api/v1/auth/register

**请求格式**:
```json
{
  "username": "string (3-20字符，字母数字下划线)",
  "email": "string (有效邮箱格式)",
  "password": "string (8-128字符)",
  "firstName": "string (可选，1-50字符)",
  "lastName": "string (可选，1-50字符)",
  "phoneNumber": "string (可选，有效手机号格式)"
}
```

**成功响应 (201)**:
```json
{
  "status": "success",
  "message": "注册成功，请检查邮箱完成验证",
  "data": {
    "userId": "usr_abc123xyz",
    "username": "john_doe",
    "email": "john@example.com",
    "emailVerified": false,
    "createdAt": "2026-01-28T10:30:00Z",
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

**错误响应**:

**400 - 请求参数错误**:
```json
{
  "status": "error",
  "code": "INVALID_INPUT",
  "message": "输入验证失败",
  "errors": [
    {
      "field": "password",
      "message": "密码必须至少8字符，包含大小写字母和数字"
    }
  ]
}
```

**409 - 冲突**:
```json
{
  "status": "error",
  "code": "USERNAME_TAKEN",
  "message": "用户名已被使用",
  "suggestions": ["john_doe2", "john_doe_2026"]
}
```

**429 - 速率限制**:
```json
{
  "status": "error",
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "请求过于频繁，请稍后再试",
  "retryAfter": 60
}
```

**500 - 服务器错误**:
```json
{
  "status": "error",
  "code": "INTERNAL_ERROR",
  "message": "服务暂时不可用，请稍后重试"
}
```

#### 端点2: POST /api/v1/auth/verify-email

**请求格式**:
```json
{
  "token": "string (邮箱验证 token)"
}
```

**成功响应 (200)**:
```json
{
  "status": "success",
  "message": "邮箱验证成功",
  "data": {
    "userId": "usr_abc123xyz",
    "emailVerified": true
  }
}
```

#### 端点3: POST /api/v1/auth/resend-verification

**请求格式**:
```json
{
  "email": "string"
}
```

**成功响应 (200)**:
```json
{
  "status": "success",
  "message": "验证邮件已重新发送"
}
```

### 3.2 数据模型

```
Entity: User
Fields:
  - id: UUID, primary key, auto-generated
  - username: string(20), unique, indexed, not null
  - email: string(255), unique, indexed, not null
  - password_hash: string(255), not null
  - first_name: string(50), nullable
  - last_name: string(50), nullable
  - phone_number: string(20), nullable
  - email_verified: boolean, default false
  - email_verification_token: string(255), nullable
  - email_verification_expires: timestamp, nullable
  - created_at: timestamp, default now()
  - updated_at: timestamp, default now()
  - last_login: timestamp, nullable
  - is_active: boolean, default true
  - is_deleted: boolean, default false

Indexes:
  - PRIMARY KEY (id)
  - UNIQUE INDEX (username)
  - UNIQUE INDEX (email)
  - INDEX (email_verified)
  - INDEX (created_at)

Relationships:
  - User has many Profiles
  - User has many Sessions
```

### 3.3 业务规则

1. **用户名规则**:
   - 长度: 3-20 字符
   - 格式: 字母、数字、下划线
   - 必须以字母开头
   - 不区分大小写（存储时统一小写）
   - 保留用户名列表: admin, root, system, etc.

2. **邮箱规则**:
   - 必须符合 RFC 5322 标准
   - 不区分大小写（存储时统一小写）
   - 一个邮箱只能注册一个账户
   - 支持常见邮箱域名验证

3. **密码规则**:
   - 长度: 8-128 字符
   - 必须包含: 至少一个大写字母、一个小写字母、一个数字
   - 可选: 特殊字符
   - 使用 bcrypt 加密，cost factor = 12
   - 不能是常见弱密码（检查常见密码字典）

4. **验证邮件规则**:
   - Token 有效期: 24 小时
   - Token 格式: UUID v4
   - 一次性使用
   - 可以重新发送，但有速率限制（5次/小时）

5. **速率限制**:
   - 注册端点: 5次/小时/IP
   - 验证端点: 10次/小时/用户
   - 重发邮件: 5次/小时/用户

## 4. 非功能需求

### 4.1 性能要求

- 注册请求响应时间: < 500ms (P95)
- 邮箱发送时间: < 2s
- 并发注册能力: 1000 requests/sec
- 数据库查询时间: < 100ms

### 4.2 安全要求

- **认证**: 暂无（注册是公开接口）
- **密码安全**:
  - 使用 bcrypt 加密
  - 密码不在日志中出现
  - 密码复杂度验证
- **数据加密**:
  - 传输层: HTTPS/TLS 1.3
  - 存储层: 密码字段加密
- **防护措施**:
  - CSRF 保护
  - SQL 注入防护
  - XSS 防护
  - 速率限制
  - CAPTCHA（可选，检测到异常时启用）

### 4.3 可观测性要求

- **日志**:
  - 级别: INFO
  - 记录: 注册尝试、成功/失败、验证事件
  - 不记录: 密码、敏感信息

- **指标**:
  - 注册成功率
  - 注册失败率（按原因分类）
  - 邮箱验证率
  - 平均注册时间
  - API 响应时间

- **告警**:
  - 注册成功率 < 90%
  - 注册请求突增（> 正常值 3倍）
  - 邮件发送失败率 > 5%
  - API 响应时间 > 1s

## 5. 验收标准

### 5.1 功能测试用例

- [ ] 成功案例: 使用有效信息注册新用户
- [ ] 验证案例: 用户名格式验证（过短、过长、非法字符）
- [ ] 验证案例: 邮箱格式验证
- [ ] 验证案例: 密码强度验证
- [ ] 冲突案例: 用户名已存在
- [ ] 冲突案例: 邮箱已注册
- [ ] 边界案例: 最小和最大长度输入
- [ ] 邮件案例: 验证邮件发送成功
- [ ] 邮件案例: 邮箱验证 token 有效性
- [ ] 邮件案例: 过期 token 处理
- [ ] 速率限制案例: 超过速率限制返回 429

### 5.2 性能测试基准

- [ ] 负载测试: 1000 concurrent users, 响应时间 < 500ms
- [ ] 压力测试: 持续高负载（30分钟）系统稳定
- [ ] 峰值测试: 突发流量处理能力

### 5.3 安全测试清单

- [ ] SQL 注入测试
- [ ] XSS 攻击测试
- [ ] CSRF 攻击测试
- [ ] 暴力破解防护测试
- [ ] 密码存储安全检查
- [ ] 敏感信息泄露检查
- [ ] 速率限制有效性测试

## 6. 实现注意事项

### 6.1 技术约束

- 必须使用异步处理邮件发送（消息队列）
- 数据库必须支持事务
- 需要实现幂等性（防止重复注册）

### 6.2 依赖关系

- 邮件服务: SMTP 或第三方邮件服务（SendGrid, AWS SES）
- 数据库: PostgreSQL 12+
- 缓存: Redis（用于速率限制和 token 存储）

### 6.3 风险和缓解措施

| 风险 | 影响 | 缓解措施 |
|-----|------|---------|
| 恶意注册攻击 | 高 | 实施速率限制和 CAPTCHA |
| 邮件服务不可用 | 中 | 降级方案，允许手动验证 |
| 数据库性能瓶颈 | 中 | 索引优化，读写分离 |
| 密码泄露 | 高 | 强密码策略，加密存储，监控 |

## 7. 附录

### 7.1 参考文档

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [RFC 5322 - Email Format](https://tools.ietf.org/html/rfc5322)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)

### 7.2 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| 1.0 | 2026-01-28 | 初始版本 | AI Research Team |

### 7.3 讨论记录

- **2026-01-28**: 初始规范设计，确定核心功能和验收标准
- **2026-01-28**: 评审通过，批准实施
