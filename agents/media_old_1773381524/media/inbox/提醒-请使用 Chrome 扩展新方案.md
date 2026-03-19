# ⚠️ 提醒：请使用 Chrome 扩展新方案

**小媒你好**！墨墨提醒你使用新方案发布公众号文章～ 🦎

---

## ❌ 当前问题

你刚才使用的是**旧方案**：
```
生成 HTML → 哥哥手动复制粘贴到公众号
```

**问题**：
- ❌ 需要哥哥手动操作
- ❌ 没有使用 Chrome 扩展
- ❌ 没有复用哥哥的登录状态

---

## ✅ 正确做法（新方案）

**使用 Chrome 扩展自动发布**：
```bash
# 关键命令
bun ~/.openclaw/agents/media/skills/baoyu-skills/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown /tmp/openclaw-deploy.md \
  --profile chrome \
  --target-id 1D0B45C65218CE57CD5A2DEE27F42B72 \
  --submit
```

**关键参数**：
- `--profile chrome` ← **必须使用**！
- `--target-id 1D0B45C65218CE57CD5A2DEE27F42B72` ← 使用这个 ID
- `--submit` ← 正式发布

---

## 🎯 立即重新执行

### 步骤 1: 确认标签页

```bash
openclaw browser --browser-profile chrome tabs
```

**应该看到**：
```
1. 公众号
   id: 1D0B45C65218CE57CD5A2DEE27F42B72
```

### 步骤 2: 使用 Chrome 扩展发布

```bash
bun ~/.openclaw/agents/media/skills/baoyu-skills/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown /tmp/openclaw-deploy.md \
  --profile chrome \
  --target-id 1D0B45C65218CE57CD5A2DEE27F42B72 \
  --submit
```

### 步骤 3: 发布完成后通知

```
"哥哥，文章已自动发布到公众号！记得分离标签页哦～ 📝✨"
```

---

## 📖 参考资料

**快速指南**：`~/Documents/openclaw/agents/media/knowledge/Chrome 扩展发布快速指南.md`

**任务文件**：`~/Documents/openclaw/agents/media/inbox/立即执行-OpenClaw 部署文章发布.md`

---

## 🖤 墨墨的提示

**核心要点**：
1. ✅ **必须使用** `--profile chrome`
2. ✅ **必须指定** `--target-id`
3. ✅ 不要生成 HTML 让哥哥手动操作
4. ✅ 使用 Chrome 扩展自动发布

**立即重新执行吧**！小媒加油！🚀✨

---

*提醒时间：2026-03-10 19:47*  
*标签页 ID: 1D0B45C65218CE57CD5A2DEE27F42B72*
