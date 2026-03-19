#!/bin/bash
# 小媒内容长度检查脚本
# 用途：检查并修复超长内容

set -e

MEDIA_DIR="$HOME/Documents/openclaw/agents/media"
MAX_LENGTH=160000  # 预留 1 万字符余量

echo "╔════════════════════════════════════════╗"
echo "║   小媒内容长度检查                     ║"
echo "╚════════════════════════════════════════╝"
echo ""

# 检查 outbox 目录
if [ ! -d "$MEDIA_DIR/outbox" ]; then
    echo "outbox 目录不存在"
    exit 0
fi

# 查找超长文件
FOUND_LONG=false
for file in "$MEDIA_DIR/outbox"/*.md "$MEDIA_DIR"/*.md; do
    if [ -f "$file" ]; then
        LENGTH=$(wc -c < "$file")
        if [ $LENGTH -gt $MAX_LENGTH ]; then
            echo "⚠️  超长文件：$file"
            echo "   长度：$LENGTH 字符（限制：$MAX_LENGTH）"
            echo "   操作：创建安全版本..."
            
            # 创建安全版本（截断）
            head -c $MAX_LENGTH "$file" > "$file.safe"
            mv "$file.safe" "$file"
            
            echo "   ✓ 已截断到 $MAX_LENGTH 字符"
            echo ""
            
            FOUND_LONG=true
        fi
    fi
done

if [ "$FOUND_LONG" = false ]; then
    echo "✅ 所有文件长度正常"
fi

echo ""
echo "建议："
echo "  - 超过 10 万字的内容先发送摘要"
echo "  - 询问用户是否需要全文"
echo "  - 全文分块发送（每块 16 万字）"
