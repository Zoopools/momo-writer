# 🚀 立即执行：OpenClaw 部署文章发布

**任务状态**: ⏳ 立即执行

---

## ✅ 准备工作已完成

**标签页已就绪**:
- ✅ ID: `1D0B45C65218CE57CD5A2DEE27F42B72`
- ✅ ID: `8AC5F7AD463605D7DBD502F809E9DE7F`

**哥哥已登录公众号后台**，可以直接使用！

---

## 📝 立即执行这些命令

### 1. 创作文章

```bash
cat > /tmp/openclaw-deploy.md << 'EOF'
---
title: OpenClaw 本地部署完整指南
author: 哥哥
---

# OpenClaw 本地部署完整指南

## 什么是 OpenClaw

OpenClaw 是一个强大的 AI Agent 框架，让你可以轻松创建和管理多个 AI 助手。

## 系统要求

- **macOS**: 10.15+
- **Windows**: 10+
- **Linux**: Ubuntu 20.04+

## 安装步骤

### macOS

```bash
# 使用 Homebrew 安装
brew install openclaw
```

### 使用 npm 安装

```bash
npm install -g openclaw
```

## 配置步骤

### 1. API Key 配置

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "list": [
      {
        "id": "writer",
        "model": {
          "primary": "你的 API Key"
        }
      }
    ]
  }
}
```

### 2. 飞书配置

在飞书开放平台创建应用，获取 App ID 和 App Secret。

## 启动 Gateway

```bash
openclaw gateway start
```

## 验证安装

```bash
openclaw status
```

## 常见问题

### Gateway 无法启动

检查端口是否被占用：
```bash
lsof -i :18789
```

### 飞书连接失败

检查 App ID 和 App Secret 是否正确。

## 使用示例

```bash
# 查看状态
openclaw status

# 查看会话
openclaw sessions list
```

---

**参考资料**:
- 官方文档：https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw
EOF
```

### 2. 生成封面图

（墨墨会自动调用 baoyu-cover-image）

### 3. 使用 Chrome 扩展发布

```bash
bun ~/.openclaw/agents/media/skills/baoyu-skills/skills/baoyu-post-to-wechat/scripts/wechat-article.ts \
  --markdown /tmp/openclaw-deploy.md \
  --profile chrome \
  --target-id 1D0B45C65218CE57CD5A2DEE27F42B72 \
  --submit
```

**关键参数**:
- `--profile chrome` ← **必须使用**！
- `--target-id 1D0B45C65218CE57CD5A2DEE27F42B72` ← 使用这个 ID
- `--submit` ← 正式发布

### 4. 发布完成后通知哥哥

```
"哥哥，文章已发布到公众号！记得分离标签页哦～ 📝✨"
```

---

## ⚠️ 注意事项

1. **必须使用** `--profile chrome`（不要用独立浏览器）
2. **必须指定** `--target-id`（使用上面的 ID）
3. 发布完成后提醒哥哥分离标签页

---

**立即执行吧！小媒加油**！🚀✨

*创建时间：2026-03-10 19:45*
