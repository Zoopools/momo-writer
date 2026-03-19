#!/bin/bash
# 墨墨的同步脚本 - 从 GitHub 拉取

set -e

echo "🖤 墨墨的同步脚本 (拉取)"
echo "======================="

cd /Users/wh1ko/Documents/openclaw/agents/writer

echo ""
echo "📥 从 GitHub 拉取最新配置..."
git pull

echo ""
echo "🔧 加载环境变量..."
if [ -f .env.local ]; then
    source .env.local
    echo "✅ 环境变量已加载"
else
    echo "⚠️  .env.local 不存在，请复制 .env.example 并填入密钥"
    echo "   cp .env.example .env.local"
fi

echo ""
echo "✅ 拉取完成！"
echo ""
echo "📍 当前分支：$(git branch --show-current)"
echo "📍 最新提交：$(git log --oneline -1)"
