# 贡献指南

感谢您对 AI Coding 驱动开发 Demo 项目的关注！

## 如何贡献

我们欢迎各种形式的贡献，包括但不限于：

- 报告 Bug
- 讨论代码状态
- 提交修复
- 提出新功能
- 成为维护者

## 开发流程

### 1. Fork 并克隆仓库

```bash
git clone https://github.com/your-username/ai-coding-demo.git
cd ai-coding-demo
```

### 2. 创建功能分支

```bash
git checkout -b feature/your-feature-name
```

### 3. 编写规范（Specification）

遵循 AI Coding 驱动开发范式，先编写规范：

```bash
# 创建功能规范
cp specs/templates/feature-spec-template.md specs/features/SPEC-XXX-001-your-feature.md
```

### 4. 编写测试（TDD）

```bash
# 编写测试
pytest tests/unit/domain/test_your_feature.py
```

### 5. 实现功能

基于规范和测试实现功能代码。

### 6. 运行测试和验证

```bash
# 运行所有测试
pytest

# 代码格式化
black src/ tests/
isort src/ tests/

# 类型检查
mypy src/

# 代码质量检查
flake8 src/ tests/
```

### 7. 提交更改

```bash
git add .
git commit -m "feat: add your feature description"
```

### 8. 推送到 Fork

```bash
git push origin feature/your-feature-name
```

### 9. 创建 Pull Request

在 GitHub 上创建 Pull Request，并：

- 填写 PR 模板
- 关联相关 Issue
- 确保所有 CI 检查通过
- 请求代码审查

## 代码规范

### Python 风格指南

- 遵循 PEP 8
- 使用 Black 进行代码格式化
- 使用 isort 对导入进行排序
- 类型注解使用 mypy 检查

### 命名约定

- **类名**: PascalCase (如 `UserService`)
- **函数/方法**: snake_case (如 `register_user`)
- **常量**: UPPER_SNAKE_CASE (如 `MAX_LOGIN_ATTEMPTS`)
- **私有方法**: 前缀下划线 (如 `_internal_method`)

### 文档字符串

使用 Google 风格的文档字符串：

```python
def register_user(email: str, password: str) -> User:
    """注册新用户

    Args:
        email: 用户邮箱
        password: 用户密码

    Returns:
        创建的用户对象

    Raises:
        UserAlreadyExistsError: 当用户已存在时
        ValidationError: 当输入验证失败时
    """
    pass
```

## 规范编写规范

### 规范文档结构

每个功能规范应包含：

1. **元数据**: ID、版本、状态、负责人
2. **背景**: 为什么需要这个功能
3. **目标**: 功能要实现什么
4. **需求**: 详细的功能需求
5. **API 设计**: 接口定义
6. **数据模型**: 数据结构
7. **业务规则**: 业务逻辑规则
8. **测试场景**: 测试用例

### 规范状态

- **Draft**: 草稿阶段
- **Review**: 审查中
- **Approved**: 已批准
- **Implemented**: 已实现

## 测试规范

### 测试金字塔

```
        /\
       /  \      E2E Tests (少量)
      /____\
     /      \    Integration Tests (适量)
    /________\
   /          \  Unit Tests (大量)
  /__________  \
```

### 测试命名

使用描述性的测试名称：

```python
def test_register_user_with_valid_credentials_should_succeed():
    """测试使用有效凭据注册用户应该成功"""
    pass

def test_register_user_with_duplicate_email_should_fail():
    """测试使用重复邮箱注册用户应该失败"""
    pass
```

### 测试覆盖

目标测试覆盖率：> 80%

## Pull Request 模板

```markdown
## 描述
简要描述此 PR 的更改。

## 规范
- 规范文档: [链接]
- 规范 ID: SPEC-XXX-001

## 更改类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 重构
- [ ] 性能优化

## 测试
- [ ] 单元测试
- [ ] 集成测试
- [ ] E2E 测试
- [ ] 手动测试

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 测试通过
- [ ] 文档已更新
- [ ] 没有新的警告
- [ ] 已添加适当的注释

## 相关 Issue
Closes #issue-number
```

## 发布流程

### 版本号

遵循语义化版本（Semantic Versioning）：

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的新功能
- **PATCH**: 向后兼容的 Bug 修复

### 发布步骤

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建 Git tag
4. 构建和发布 Docker 镜像
5. 发布 GitHub Release

## 社区准则

- 尊重所有贡献者
- 建设性的反馈
- 欢迎新手
- 专注问题，不针对个人

## 获取帮助

- **文档**: 查看项目 docs/ 目录
- **Issues**: 提交 GitHub Issue
- **Discussions**: 参与 GitHub Discussions

## 许可证

通过贡献，您同意您的贡献将在与项目相同的许可证下发布。
