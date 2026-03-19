#!/bin/bash

# B 站评论图片报告 - GitHub Pages 一键部署脚本

echo "🚀 开始部署到 GitHub Pages..."
echo ""

# 检查 git 是否安装
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

# 进入目录
cd "/Users/wh1ko/Documents/openclaw/agents/hunter/bili_images" || exit 1

# 检查是否已有 git 仓库
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
fi

# 添加文件
echo "📄 添加文件..."
git add "B 站评论图片报告 - 在线版.html"
git add "B 站评论图片报告.html" 2>/dev/null || true

# 提交
echo "💾 提交更改..."
git commit -m "B 站评论图片报告 - $(date +%Y%m%d-%H%M%S)"

# 获取 GitHub 用户名
echo ""
echo "🔗 请提供你的 GitHub 仓库地址："
echo "   格式：https://github.com/你的用户名/仓库名.git"
echo ""
read -p "输入仓库地址：" REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ 未输入仓库地址"
    exit 1
fi

# 关联远程仓库
echo "🔗 关联远程仓库..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

# 推送
echo "📤 推送到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 下一步操作："
echo "1️⃣ 打开 GitHub 仓库页面"
echo "2️⃣ 进入 Settings → Pages"
echo "3️⃣ Source 选择 'main' 分支 → Save"
echo "4️⃣ 等待 1-2 分钟后访问生成的链接"
echo ""
echo "🌐 访问地址格式："
echo "   https://你的用户名.github.io/仓库名/B 站评论图片报告 - 在线版.html"
echo ""
