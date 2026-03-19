#!/bin/bash
# 墨墨的同步脚本 - 推送到 GitHub

set -e

echo "🖤 墨墨的同步脚本"
echo "================"

cd /Users/wh1ko/Documents/openclaw/agents/writer

# 检查变更
echo ""
echo "📊 检查变更..."
git status

# 如果有变更，提交并推送
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo ""
    echo "📝 发现变更，准备提交..."
    
    read -p "输入提交信息 (默认：自动同步): " commit_msg
    commit_msg=${commit_msg:-"自动同步配置"}
    
    git add .
    git commit -m "$commit_msg"
    
    echo ""
    echo "🚀 推送到 GitHub..."
    git pull --rebase --autostash
    git push
    
    echo ""
    echo "✅ 同步完成！"
else
    echo ""
    echo "✅ 没有变更，无需同步"
fi

echo ""
echo "📍 当前分支：$(git branch --show-current)"
echo "📍 最新提交：$(git log --oneline -1)"
