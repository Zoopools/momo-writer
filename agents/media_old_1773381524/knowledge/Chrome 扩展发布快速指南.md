# 🦎 Chrome 扩展发布快速指南

**小媒专用** - 3 步完成公众号发布

---

## ✅ 当前状态

**标签页已附加**: 2 个公众号后台

**可用标签页 ID**:
- `1D0B45C65218CE57CD5A2DEE27F42B72`
- `8AC5F7AD463605D7DBD502F809E9DE7F`

---

## 🚀 3 步发布流程

### 步骤 1: 创作内容

```bash
# 写文章（Markdown 格式）
cat > /tmp/article.md << 'EOF'
---
title: 文章标题
author: 哥哥
---

# 文章正文

...
EOF
```

### 步骤 2: 生成封面图

```bash
# 使用 baoyu-cover-image 技能
# 墨墨会自动调用
```

### 步骤 3: 使用 Chrome 扩展发布

**关键命令**:
```bash
bun ~/.openclaw/agents/media/skills/baoyu-skills/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown /tmp/article.md \
  --profile chrome \
  --target-id 1D0B45C65218CE57CD5A2DEE27F42B72 \
  --submit
```

**参数说明**:
- `--profile chrome` ← **关键！使用 Chrome 扩展模式**
- `--target-id <ID>` ← 使用上面提供的标签页 ID
- `--submit` ← 正式发布（不加是预览）

---

## ⚠️ 常见错误

### 错误 1: 忘记使用 `--profile chrome`

**错误做法**:
```bash
# ❌ 这会使用独立浏览器，需要重新登录
bun wechat-article.ts --markdown article.md
```

**正确做法**:
```bash
# ✅ 使用 Chrome 扩展，复用哥哥的登录状态
bun wechat-article.ts --markdown article.md --profile chrome --target-id <ID>
```

---

### 错误 2: 标签页 ID 错误

**检查标签页**:
```bash
openclaw browser --browser-profile chrome tabs
```

**如果没有标签页**:
- 提醒哥哥：「哥哥，请附加公众号后台标签页」
- 等待哥哥附加后再发布

---

## 📝 完整示例

```bash
# 1. 检查标签页
openclaw browser --browser-profile chrome tabs

# 输出:
# 1. 公众号
#    https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1073230568
#    id: 1D0B45C65218CE57CD5A2DEE27F42B72

# 2. 创作文章
cat > /tmp/openclaw-deploy.md << 'EOF'
---
title: OpenClaw 本地部署完整指南
author: 哥哥
---

# OpenClaw 本地部署完整指南

## 什么是 OpenClaw

OpenClaw 是一个...

## 安装步骤

...
EOF

# 3. 发布（使用 Chrome 扩展）
bun ~/.openclaw/agents/media/skills/baoyu-skills/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown /tmp/openclaw-deploy.md \
  --profile chrome \
  --target-id 1D0B45C65218CE57CD5A2DEE27F42B72 \
  --submit

# 4. 发布完成，提醒哥哥
echo "✅ 文章已发布！哥哥记得分离标签页哦～"
```

---

## 🎯 当前任务

**哥哥指令**:
> "小媒使用新方案 写一篇关于 openclaw 本地部署详细步骤的文章并用我的浏览器发布到公众号"

**立即执行**:
1. ✅ 标签页已就绪（2 个可用）
2. ✅ 使用 `--profile chrome`
3. ✅ 使用标签页 ID: `1D0B45C65218CE57CD5A2DEE27F42B72`
4. ✅ 发布完成后提醒哥哥

---

## 🖤 墨墨的提示

**核心要点**:
- ✅ **必须使用** `--profile chrome`
- ✅ **必须指定** `--target-id <ID>`
- ✅ 不要使用独立浏览器模式
- ✅ 复用哥哥的登录状态

**发布完成后**:
- ✅ 飞书通知哥哥
- ✅ 提醒哥哥分离标签页
- ✅ 附上文章链接

---

*更新时间：2026-03-10 19:45*  
*标签页状态：✅ 2 个已附加*  
*可用 ID: 1D0B45C65218CE57CD5A2DEE27F42B72*
