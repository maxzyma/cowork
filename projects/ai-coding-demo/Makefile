.PHONY: help install dev test lint format clean db-init db-reset docker-up docker-down

.DEFAULT_GOAL := help

## 彩色输出
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

## 帮助信息
help: ## 显示帮助信息
	@echo "$(BLUE)AI Coding Demo - 可用命令:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

## 开发环境
install: ## 安装依赖
	@echo "$(BLUE)安装依赖...$(NC)"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

dev: ## 启动开发服务器
	@echo "$(BLUE)启动开发服务器...$(NC)"
	python run_dev.py

## 测试
test: ## 运行所有测试
	@echo "$(BLUE)运行测试...$(NC)"
	python scripts/run_tests.py --type all

test-unit: ## 运行单元测试
	@echo "$(BLUE)运行单元测试...$(NC)"
	python scripts/run_tests.py --type unit

test-integration: ## 运行集成测试
	@echo "$(BLUE)运行集成测试...$(NC)"
	python scripts/run_tests.py --type integration

test-e2e: ## 运行 E2E 测试
	@echo "$(BLUE)运行 E2E 测试...$(NC)"
	python scripts/run_tests.py --type e2e

test-coverage: ## 生成测试覆盖率报告
	@echo "$(BLUE)生成测试覆盖率报告...$(NC)"
	pytest --cov=src --cov-report=html --cov-report=term
	@echo "$(GREEN)覆盖率报告: htmlcov/index.html$(NC)"

## 代码质量
lint: ## 运行代码质量检查
	@echo "$(BLUE)运行代码质量检查...$(NC)"
	./scripts/check_quality.sh

format: ## 格式化代码
	@echo "$(BLUE)格式化代码...$(NC)"
	black src/ tests/
	isort src/ tests/
	@echo "$(GREEN)代码格式化完成！$(NC)"

format-check: ## 检查代码格式
	@echo "$(BLUE)检查代码格式...$(NC)"
	black --check src/ tests/
	isort --check-only src/ tests/

type-check: ## 运行类型检查
	@echo "$(BLUE)运行类型检查...$(NC)"
	mypy src/

## 数据库
db-init: ## 初始化数据库
	@echo "$(BLUE)初始化数据库...$(NC)"
	python scripts/init_db.py

db-reset: ## 重置数据库
	@echo "$(YELLOW)重置数据库...$(NC)"
	@echo "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" | psql $(DATABASE_URL)
	python scripts/init_db.py

## Docker
docker-build: ## 构建 Docker 镜像
	@echo "$(BLUE)构建 Docker 镜像...$(NC)"
	docker-compose build

docker-up: ## 启动 Docker 服务
	@echo "$(BLUE)启动 Docker 服务...$(NC)"
	docker-compose up -d

docker-down: ## 停止 Docker 服务
	@echo "$(BLUE)停止 Docker 服务...$(NC)"
	docker-compose down

docker-logs: ## 查看 Docker 日志
	docker-compose logs -f app

## 清理
clean: ## 清理临时文件
	@echo "$(BLUE)清理临时文件...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo "$(GREEN)清理完成！$(NC)"

## CI/CD
ci: lint test ## 运行 CI 检查 (lint + test)
	@echo "$(GREEN)CI 检查通过！$(NC)"

validate-specs: ## 验证规范文档
	@echo "$(BLUE)验证规范文档...$(NC)"
	python scripts/spec-validator.py specs/
