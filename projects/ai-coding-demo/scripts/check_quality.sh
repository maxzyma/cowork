#!/bin/bash
# 代码质量检查脚本

set -e

echo "🔍 运行代码质量检查..."

# 格式化检查
echo "📝 检查代码格式 (Black)..."
black --check src/ tests/

# 导入排序检查
echo "📦 检查导入排序 (isort)..."
isort --check-only src/ tests/

# 类型检查
echo "🔎 运行类型检查 (mypy)..."
mypy src/

# 代码风格检查
echo "🎨 检查代码风格 (flake8)..."
flake8 src/ tests/

echo "✅ 所有代码质量检查通过！"
