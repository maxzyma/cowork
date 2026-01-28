# 部署文档

## 生产环境部署指南

本文档描述如何将用户管理服务部署到生产环境。

## 部署架构

```
                        ┌─────────────────┐
                        │   Load Balancer │
                        └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
              ┌─────▼─────┐ ┌───▼────┐ ┌───▼────┐
              │  App Pod  │ │ App... │ │ App... │
              └─────┬─────┘ └───┬────┘ └───┬────┘
                    │            │            │
                    └────────────┼────────────┘
                                 │
                        ┌────────▼────────┐
                        │  PostgreSQL DB  │
                        │   (Primary)     │
                        └─────────────────┘
```

## 部署步骤

### 1. 准备工作

```bash
# 克隆代码仓库
git clone <repository-url>
cd ai-coding-demo

# 创建环境配置
cp .env.example .env
# 编辑 .env 文件，设置生产环境变量

# 构建镜像
docker build -t user-management-service:latest .
```

### 2. 数据库迁移

```bash
# 运行数据库迁移
docker-compose run --rm alembic upgrade head
```

### 3. 启动服务

```bash
# 使用 Docker Compose
docker-compose up -d

# 检查服务状态
docker-compose ps
docker-compose logs -f app
```

### 4. 健康检查

```bash
# 检查服务健康状态
curl http://localhost:8000/health

# 检查 API 文档
curl http://localhost:8000/docs
```

## Kubernetes 部署

### Namespace 配置

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: user-management
```

### Deployment 配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-management-app
  namespace: user-management
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-management
  template:
    metadata:
      labels:
        app: user-management
    spec:
      containers:
      - name: app
        image: user-management-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Service 配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-management-service
  namespace: user-management
spec:
  selector:
    app: user-management
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

## 监控和日志

### Prometheus 指标

应用暴露以下指标：

- `http_requests_total`: HTTP 请求总数
- `http_request_duration_seconds`: 请求处理时间
- `user_registrations_total`: 用户注册总数

### 日志收集

使用 Fluentd/Fluent Bit 收集应用日志：

```json
{
  "log_level": "info",
  "service": "user-management",
  "timestamp": "2026-01-28T10:00:00Z",
  "message": "User registered successfully",
  "user_id": "uuid"
}
```

## 安全考虑

1. **环境变量管理**: 使用 Kubernetes Secrets 或 AWS Secrets Manager
2. **HTTPS**: 在负载均衡器层配置 SSL/TLS
3. **网络策略**: 配置 Kubernetes Network Policies
4. **镜像扫描**: 定期扫描 Docker 镜像漏洞
5. **速率限制**: 实现API速率限制防止滥用

## 故障排查

### 常见问题

**服务无法启动**
```bash
# 检查日志
docker-compose logs app
# 或
kubectl logs -f deployment/user-management-app
```

**数据库连接失败**
```bash
# 检查数据库连接
docker-compose exec app pg_isready -h db -p 5432
```

**健康检查失败**
```bash
# 手动执行健康检查
curl http://localhost:8000/health
```

## 回滚策略

```bash
# Docker Compose 回滚
docker-compose down
docker-compose up -d --scale app=0
# 切换到之前的镜像版本
docker-compose up -d

# Kubernetes 回滚
kubectl rollout undo deployment/user-management-app
```

## 性能优化

1. **数据库连接池**: 调整 SQLAlchemy pool_size
2. **缓存**: 添加 Redis 缓存层
3. **CDN**: 静态资源使用 CDN
4. **压缩**: 启用 gzip 压缩
5. **索引**: 确保数据库字段有适当索引
