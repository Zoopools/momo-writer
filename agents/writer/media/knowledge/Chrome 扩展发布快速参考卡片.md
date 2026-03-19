# 🦎 Chrome 扩展发布快速参考卡片

**小媒专用** - 贴在桌边随时看！

---

## 🚀 核心命令（复制粘贴）

```bash
bun ~/.openclaw/agents/media/skills/baoyu-skills/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown /tmp/article.md \
  --cover /tmp/cover.jpg \
  --profile chrome \
  --target-id 1D0B45C65218CE57CD5A2DEE27F42B72 \
  --submit
```

---

## 🔑 关键参数（必背！）

| 参数 | 值 | 说明 |
|------|-----|------|
| `--profile` | `chrome` | **必须使用 Chrome 扩展** |
| `--target-id` | `1D0B45C65218CE57CD5A2DEE27F42B72` | **公众号标签页 ID** |
| `--submit` | (无值) | **直接发布** |

---

## 📋 7 步流程

```
1. 创作文章 (Markdown)
   ↓
2. 生成封面 (baoyu-cover-image)
   ↓
3. 格式化 (baoyu-format-markdown)
   ↓
4. 检查标签页 (openclaw browser tabs)
   ↓
5. Chrome 扩展发布 (核心命令)
   ↓
6. 发布完成
   ↓
7. 通知哥哥 + 提醒分离标签页
```

---

## ⚠️ 常见错误

### ❌ 错误 1: 忘记 --profile chrome

```bash
# 错误：会使用独立浏览器
bun wechat-article.ts --markdown article.md

# 正确：使用 Chrome 扩展
bun wechat-article.ts --markdown article.md --profile chrome
```

---

### ❌ 错误 2: 标签页未附加

**错误信息**:
```
Error: No tabs found for profile: chrome
```

**解决**:
```
提醒哥哥：「哥哥，请附加公众号后台标签页」
```

---

### ❌ 错误 3: 今天群发次数已用完

**错误信息**:
```
Error: 今天群发次数已用完
```

**解决**:
```
✅ 文章保存到草稿箱
✅ 明天再群发
```

---

## 📞 快速检查

### 检查标签页

```bash
openclaw browser --browser-profile chrome tabs
```

**应该看到**:
```
1. 公众号
   id: 1D0B45C65218CE57CD5A2DEE27F42B72
```

---

### 检查封面图

```bash
ls -lh /tmp/cover.jpg
```

**应该看到**:
```
-rw-r--r--  cover.jpg (200KB)
```

---

### 检查文章

```bash
cat /tmp/article.md | head -20
```

**应该看到**:
```markdown
---
title: 文章标题
author: 哥哥
---

# 文章正文
```

---

## 🎯 一键执行（推荐）

```bash
bash ~/.openclaw/agents/media/scripts/publish-wechat.sh /tmp/article.md
```

**自动完成**:
1. ✅ 生成封面图
2. ✅ 格式化 Markdown
3. ✅ 检查标签页
4. ✅ Chrome 扩展发布
5. ✅ 通知哥哥

---

## 🖤 发布完成后

**通知话术**:
```
哥哥，文章已群发到公众号！📝✨

标题：{文章标题}
链接：{文章链接}
字数：{字数}

记得分离标签页哦～ 🦎
```

---

## 📞 墨墨求助

**遇到问题时**:
```
"墨墨，公众号发布遇到 XXX 问题，帮帮我！"
```

**墨墨会立即**:
1. ✅ 检查问题
2. ✅ 提供解决方案
3. ✅ 协助发布

---

*版本：v2.0（Chrome 扩展模式）*  
*标签页 ID: 1D0B45C65218CE57CD5A2DEE27F42B72*  
*创建时间：2026-03-10 21:06*
