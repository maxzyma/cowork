#!/bin/bash
# Claude Code 项目配置迁移脚本
# 从 memory 项目迁移到 knowledge&memory 项目

set -e

OLD_PROJECT="$HOME/.claude/projects/-Users-magooup-workspace-default-research-memory"
NEW_PROJECT="$HOME/.claude/projects/-Users-magooup-workspace-default-research-knowledge-memory"

echo "=== Claude Code 配置迁移 ==="
echo "从: $OLD_PROJECT"
echo "到: $NEW_PROJECT"
echo ""

# 检查源目录是否存在
if [ ! -d "$OLD_PROJECT" ]; then
    echo "错误: 源目录不存在: $OLD_PROJECT"
    exit 1
fi

# 创建目标目录（如果不存在）
if [ ! -d "$NEW_PROJECT" ]; then
    mkdir -p "$NEW_PROJECT"
    echo "✓ 创建目标目录"
fi

echo "开始迁移文件..."
echo ""

# 复制会话目录和文件
for session_dir in "$OLD_PROJECT"/[0-9a-f]*-[0-9a-f]*-[0-9a-f]*; do
    if [ -d "$session_dir" ]; then
        session_name=$(basename "$session_dir")
        echo "复制会话目录: $session_name"
        cp -R "$session_dir" "$NEW_PROJECT/"
    fi
done

# 复制会话历史文件
for jsonl_file in "$OLD_PROJECT"/*.jsonl; do
    if [ -f "$jsonl_file" ]; then
        filename=$(basename "$jsonl_file")
        echo "复制会话历史: $filename"
        cp "$jsonl_file" "$NEW_PROJECT/"
    fi
done

# 复制其他文件
for file in "$OLD_PROJECT"/*.html "$OLD_PROJECT"/.DS_Store; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "复制文件: $filename"
        cp "$file" "$NEW_PROJECT/"
    fi
done

# 复制 cache 目录
if [ -d "$OLD_PROJECT/cache" ]; then
    echo "复制 cache 目录"
    cp -R "$OLD_PROJECT/cache" "$NEW_PROJECT/"
fi

echo ""
echo "=== 迁移完成 ==="
echo "旧项目文件数: $(find "$OLD_PROJECT" -type f | wc -l | tr -d ' ')"
echo "新项目文件数: $(find "$NEW_PROJECT" -type f | wc -l | tr -d ' ')"
echo ""
echo "会话对比:"
echo "原项目:"
ls -lh "$OLD_PROJECT"/*.jsonl 2>/dev/null | awk '{print "  " $9, $5}'
echo "新项目:"
ls -lh "$NEW_PROJECT"/*.jsonl 2>/dev/null | awk '{print "  " $9, $5}'
