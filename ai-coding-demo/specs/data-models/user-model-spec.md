# 数据模型规范: 用户模型 (User Model)

## 元数据

- **ID**: SPEC-DATA-USER-001
- **版本**: 1.0
- **状态**: Approved
- **负责人**: AI Research Team
- **创建日期**: 2026-01-28
- **最后更新**: 2026-01-28

## 1. 概述

用户模型是系统的核心实体，表示系统中的注册用户及其基本信息。

## 2. 数据模型定义

### 2.1 实体关系图 (ERD)

```
┌─────────────────────────────────────┐
│            User                      │
├─────────────────────────────────────┤
│ PK  id: UUID                        │
│ UK  username: VARCHAR(20)           │
│ UK  email: VARCHAR(255)             │
│     password_hash: VARCHAR(255)     │
│     first_name: VARCHAR(50)         │
│     last_name: VARCHAR(50)          │
│     phone_number: VARCHAR(20)       │
│     email_verified: BOOLEAN         │
│     email_verification_token: UUID  │
│     email_verification_expires: TS  │
│     created_at: TIMESTAMP           │
│     updated_at: TIMESTAMP           │
│     last_login: TIMESTAMP           │
│     is_active: BOOLEAN              │
│     is_deleted: BOOLEAN             │
└─────────────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────────┐
│          UserSession                 │
├─────────────────────────────────────┤
│ PK  id: UUID                        │
│ FK  user_id: UUID                   │
│     token: VARCHAR(500)             │
│     expires_at: TIMESTAMP           │
│     created_at: TIMESTAMP           │
└─────────────────────────────────────┘
```

### 2.2 字段定义

#### User 表

| 字段名 | 数据类型 | 约束 | 默认值 | 描述 |
|-------|---------|------|--------|------|
| id | UUID | PRIMARY KEY, NOT NULL | uuid_generate_v4() | 用户唯一标识 |
| username | VARCHAR(20) | UNIQUE, NOT NULL, INDEX | - | 用户名（唯一） |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | - | 邮箱地址（唯一） |
| password_hash | VARCHAR(255) | NOT NULL | - | bcrypt 加密的密码哈希 |
| first_name | VARCHAR(50) | NULL | - | 名字 |
| last_name | VARCHAR(50) | NULL | - | 姓氏 |
| phone_number | VARCHAR(20) | NULL | - | 电话号码 |
| email_verified | BOOLEAN | NOT NULL, INDEX | false | 邮箱是否已验证 |
| email_verification_token | UUID | NULL | - | 邮箱验证 token |
| email_verification_expires | TIMESTAMP | NULL | - | 验证 token 过期时间 |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | 更新时间 |
| last_login | TIMESTAMP | NULL | - | 最后登录时间 |
| is_active | BOOLEAN | NOT NULL | true | 账户是否激活 |
| is_deleted | BOOLEAN | NOT NULL | false | 软删除标记 |

### 2.3 索引定义

```sql
-- 主键索引
PRIMARY KEY (id)

-- 唯一索引
UNIQUE INDEX idx_user_username ON users(LOWER(username))
UNIQUE INDEX idx_user_email ON users(LOWER(email))

-- 普通索引
INDEX idx_user_email_verified ON users(email_verified)
INDEX idx_user_created_at ON users(created_at)
INDEX idx_user_is_active ON users(is_active)
INDEX idx_user_is_deleted ON users(is_deleted)

-- 组合索引
INDEX idx_user_active_not_deleted ON users(is_active, is_deleted)
```

### 2.4 约束条件

```sql
-- 检查约束
CHECK (LENGTH(username) >= 3 AND LENGTH(username) <= 20)
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
CHECK (LENGTH(password_hash) > 0)
CHECK (email_verification_expires IS NULL OR email_verification_expires > created_at)

-- 触发器：自动更新 updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## 3. 数据完整性规则

### 3.1 必填字段

- id (自动生成)
- username
- email
- password_hash
- email_verified
- created_at
- updated_at
- is_active
- is_deleted

### 3.2 唯一性约束

- username: 必须唯一（不区分大小写）
- email: 必须唯一（不区分大小写）

### 3.3 格式验证

**username**:
- 长度: 3-20 字符
- 格式: `^[a-z][a-z0-9_]*$` (小写字母、数字、下划线，必须以字母开头)

**email**:
- 格式: 符合 RFC 5322 标准
- 示例: `user@example.com`

**password_hash**:
- 格式: bcrypt 哈希
- 示例: `$2b$12$KIXxLVDpFwQx...`

**phone_number**:
- 格式: E.164 国际格式
- 示例: `+1234567890`

## 4. 业务规则

### 4.1 创建规则

1. 创建用户时自动生成 UUID
2. username 和 email 自动转为小写存储
3. password 必须先通过 bcrypt 加密
4. 默认 email_verified = false
5. 默认 is_active = true
6. 默认 is_deleted = false

### 4.2 更新规则

1. updated_at 自动更新为当前时间
2. username 创建后不可修改
3. email 修改需要重新验证
4. password_hash 不能直接修改（通过专门接口）

### 4.3 删除规则

1. 使用软删除（设置 is_deleted = true）
2. 物理删除需要管理员权限
3. 删除后保留 90 天可恢复期

## 5. 数据迁移

### 5.1 创建表 SQL

```sql
-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建用户表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(20),
    email_verified BOOLEAN NOT NULL DEFAULT false,
    email_verification_token UUID,
    email_verification_expires TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_deleted BOOLEAN NOT NULL DEFAULT false,

    -- 约束
    CONSTRAINT username_length CHECK (LENGTH(username) >= 3 AND LENGTH(username) <= 20),
    CONSTRAINT username_format CHECK (username ~ '^[a-z][a-z0-9_]*$'),
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- 创建索引
CREATE UNIQUE INDEX idx_user_username ON users(LOWER(username));
CREATE UNIQUE INDEX idx_user_email ON users(LOWER(email));
CREATE INDEX idx_user_email_verified ON users(email_verified);
CREATE INDEX idx_user_created_at ON users(created_at);
CREATE INDEX idx_user_active_not_deleted ON users(is_active, is_deleted);

-- 创建触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 创建触发器
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 创建备注
COMMENT ON TABLE users IS '用户表，存储系统注册用户信息';
COMMENT ON COLUMN users.id IS '用户唯一标识（UUID）';
COMMENT ON COLUMN users.username IS '用户名（唯一，小写）';
COMMENT ON COLUMN users.email IS '邮箱地址（唯一，小写）';
COMMENT ON COLUMN users.password_hash IS 'bcrypt 加密的密码哈希';
```

## 6. 示例数据

```sql
-- 示例用户数据
INSERT INTO users (
    username,
    email,
    password_hash,
    first_name,
    last_name,
    email_verified
) VALUES (
    'john_doe',
    'john@example.com',
    '$2b$12$KIXxLVDpFwQx.s.PcjGqWOmgC3K8sxXVcMp5O2BhR4m0QxK/kXtYe',
    'John',
    'Doe',
    true
);
```

## 7. 性能考虑

### 7.1 查询优化

- username 和 email 查询使用索引
- 分页查询使用 created_at 索引
- 避免全表扫描

### 7.2 存储优化

- 使用 UUID 作为主键（分布式友好）
- 字段长度合理设置
- 使用 BOOLEAN 而非 TINYINT

### 7.3 扩展性

- 支持分库分表（按 user_id 哈希）
- 支持读写分离
- 支持缓存层（Redis）

## 8. 安全考虑

### 8.1 敏感字段

- password_hash: 永不在 API 响应中返回
- email_verification_token: 仅在特定场景返回

### 8.2 访问控制

- 用户只能查看和修改自己的数据
- 管理员可以查看所有用户（脱敏）

### 8.3 审计日志

- 记录所有数据修改操作
- 包括操作人、操作时间、修改内容

## 附录

### A. 相关规范

- SPEC-USER-001: 用户注册功能规范
- SPEC-USER-002: 用户认证功能规范

### B. 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
|-----|------|---------|--------|
| 1.0 | 2026-01-28 | 初始版本 | AI Research Team |
