#!/usr/bin/env python3
"""
生成 Google Drive 上传指南
"""

print("""
# 📤 Google Drive 上传指南

## 方法 1：直接上传 HTML 文件（推荐 ⭐）

### 步骤：

1️⃣ **打开 Google Drive**
   https://drive.google.com

2️⃣ **上传文件**
   把 `B 站评论图片报告 - 在线版.html` 拖到 Google Drive

3️⃣ **获取分享链接**
   - 右键文件 → 分享 → 获取链接
   - 权限改为"任何拥有链接的人"
   - 复制链接

4️⃣ **转换链接格式**
   原始链接:
   https://drive.google.com/file/d/文件 ID/view?usp=sharing
   
   转换为预览链接:
   https://drive.google.com/uc?export=view&id=文件 ID
   
   或者下载链接:
   https://drive.google.com/uc?export=download&id=文件 ID

5️⃣ **分享预览链接**
   别人打开就能看到 HTML 报告了！

---

## 方法 2：GitHub Pages（最稳定 ⭐⭐⭐）

### 30 秒部署：

1️⃣ **打开 GitHub**
   https://github.com/new

2️⃣ **创建仓库**
   - 仓库名：bili-comments（或其他）
   - 勾选"Add a README file"
   - 点击"Create repository"

3️⃣ **上传文件**
   - 点击"Add file" → "Upload files"
   - 把 `B 站评论图片报告 - 在线版.html` 拖进去
   - 点击"Commit changes"

4️⃣ **启用 Pages**
   - Settings → Pages
   - Source 选"main"分支 → Save
   - 等待 1-2 分钟

5️⃣ **获得在线链接**
   https://你的用户名.github.io/bili-comments/B 站评论图片报告 - 在线版.html

---

## 方法 3：Netlify Drop（最快 ⭐⭐⭐）

### 1 分钟部署：

1️⃣ **打开 Netlify Drop**
   https://app.netlify.com/drop

2️⃣ **拖拽文件夹**
   把整个 `bili_images` 文件夹拖到网页

3️⃣ **获得链接**
   立即生成：https://随机名.netlify.app

4️⃣ **（可选）自定义名称**
   Site settings → Change site name

---

## 方法 4：Vercel（专业 ⭐⭐）

### 命令行部署：

```bash
# 安装 Vercel
npm install -g vercel

# 进入目录
cd /Users/wh1ko/Documents/openclaw/agents/hunter/bili_images/

# 部署
vercel --prod
```

获得链接：https://xxx.vercel.app

---

## 💡 我的建议

**最快上手**: Netlify Drop（1 分钟）
**长期稳定**: GitHub Pages（永久免费）
**临时分享**: Google Drive（但体验一般）

---

## 🎯 推荐：GitHub Pages 完整流程

```bash
# 1. 创建仓库后，在本地执行：
cd /Users/wh1ko/Documents/openclaw/agents/hunter/bili_images/

# 2. 初始化 Git
git init

# 3. 添加文件
git add "B 站评论图片报告 - 在线版.html"
git commit -m "B 站评论图片报告"

# 4. 关联远程仓库（替换为你的）
git remote add origin https://github.com/你的用户名/bili-comments.git

# 5. 推送
git push -u origin main

# 6. 启用 GitHub Pages 后访问：
# https://你的用户名.github.io/bili-comments/B 站评论图片报告 - 在线版.html
```

---

*🏹 小猎 · 信息捕手*
""")
