# 常见问题 (FAQ)

## 关于项目

### 1. 什么是 AI Coding 驱动开发？

AI Coding 驱动开发是一种新的软件开发范式，它将 AI 编码工具深度集成到开发流程中，强调：

- **SDD (Specification-Driven Development)**: 规范驱动开发
- **AI-Enhanced TDD**: AI 增强的测试驱动开发
- **CI/CS**: 持续集成 + 持续规范验证
- **自动化工作流**: 规范、测试、代码生成自动化

详细信息请参考 [设计文档](../docs/ai-coding-driven-development-paradigm.md)。

### 2. 这个项目的目标是什么？

这个 Demo 项目旨在展示 AI Coding 驱动开发的完整实践，包括：

- 完整的软件研发生命周期
- 规范驱动的开发流程
- 从规范到测试到实现的自动化
- 现代化的架构设计
- 完善的 DevOps 实践

## 开发相关

### 3. 如何开始开发？

```bash
# 克隆项目
git clone <repository-url>
cd ai-coding-demo

# 安装依赖
make install

# 启动开发服务器
make dev

# 运行测试
make test
```

详细步骤请参考 [开发指南](./development-guide.md)。

### 4. 如何运行测试？

```bash
# 运行所有测试
make test

# 运行特定类型测试
make test-unit      # 单元测试
make test-integration  # 集成测试
make test-e2e       # E2E 测试

# 生成覆盖率报告
make test-coverage
```

### 5. 如何添加新功能？

遵循 AI Coding 驱动开发流程：

1. **编写规范**: 使用 `specs/templates/feature-spec-template.md` 创建功能规范
2. **编写测试**: 基于规范编写测试用例
3. **实现功能**: 编写通过测试的代码
4. **验证**: 运行测试和代码质量检查
5. **文档**: 更新相关文档

详细流程请参考 [贡献指南](./contributing.md)。

### 6. 项目使用的技术栈是什么？

- **语言**: Python 3.11
- **Web 框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **测试**: pytest
- **容器化**: Docker
- **CI/CD**: GitHub Actions

## 部署相关

### 7. 如何部署到生产环境？

我们提供了多种部署方式：

- **Docker Compose**: 适合小规模部署
- **Kubernetes**: 适合大规模生产环境

详细部署步骤请参考 [部署文档](./deployment.md)。

### 8. 环境变量如何配置？

复制 `.env.example` 到 `.env` 并根据需要修改：

```bash
cp .env.example .env
# 编辑 .env 文件
```

关键配置项：

- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT 密钥
- `DEBUG`: 调试模式（生产环境设为 false）

## 故障排查

### 9. 数据库连接失败

**问题**: 应用无法连接到数据库

**解决方案**:

1. 检查数据库是否运行
   ```bash
   docker-compose ps db
   ```

2. 检查连接字符串
   ```bash
   echo $DATABASE_URL
   ```

3. 验证数据库可访问性
   ```bash
   psql $DATABASE_URL
   ```

### 10. 测试失败

**问题**: 测试无法通过

**解决方案**:

1. 确保所有依赖已安装
   ```bash
   make install
   ```

2. 检查测试环境配置
   ```bash
   python -m pytest --collect-only
   ```

3. 查看详细错误信息
   ```bash
   python -m pytest -vvs
   ```

### 11. Docker 构建失败

**问题**: Docker 镜像构建失败

**解决方案**:

1. 清理 Docker 缓存
   ```bash
   docker system prune -a
   ```

2. 重新构建
   ```bash
   docker-compose build --no-cache
   ```

3. 检查 Dockerfile 语法
   ```bash
   docker build -t test .
   ```

## 最佳实践

### 12. 如何编写好的规范文档？

一个好的规范文档应该：

- ✅ 清晰描述功能的业务价值
- ✅ 提供详细的 API 定义
- ✅ 包含完整的数据模型
- ✅ 列出所有业务规则
- ✅ 定义清晰的测试场景

参考模板: `specs/templates/feature-spec-template.md`

### 13. 如何保持代码质量？

遵循以下实践：

- **类型注解**: 使用 mypy 进行类型检查
- **代码格式化**: 使用 Black 和 isort
- **代码审查**: 所有代码需要经过审查
- **测试覆盖率**: 保持 80%+ 的覆盖率
- **文档**: 保持文档与代码同步

### 14. 如何处理安全性？

安全性措施：

- ✅ 使用环境变量管理敏感信息
- ✅ 密码使用 bcrypt 哈希
- ✅ API 输入验证
- ✅ SQL 注入防护（使用 ORM）
- ✅ HTTPS（生产环境）
- ✅ 定期依赖更新

## 社区

### 15. 如何获得帮助？

- 📖 查看 [文档](./)
- 💬 参与 [Discussions](https://github.com/your-repo/discussions)
- 🐛 提交 [Issue](https://github.com/your-repo/issues)
- ✉️ 联系维护者

### 16. 如何贡献？

我们欢迎各种形式的贡献！

- 报告 Bug
- 提出新功能建议
- 改进文档
- 提交代码

详细指南请参考 [贡献指南](./contributing.md)。

## 其他

### 17. 项目的许可证是什么？

本项目使用 MIT 许可证。详见 [LICENSE](../LICENSE) 文件。

### 18. 如何联系项目维护者？

- Email: your-email@example.com
- Twitter: @your-twitter
- GitHub: @your-github

---

还有其他问题？请随时在 [Discussions](https://github.com/your-repo/discussions) 中提问！
