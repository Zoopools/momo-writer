# 飞书多 Agent 配置指南

**创建时间**: 2026-03-19  
**作者**: 墨墨 (Mò)  
**版本**: 1.0  
**标签**: #飞书 #OpenClaw #配置 #多Agent

---

## 📱 飞书配置概览

### 当前配置状态

| 组件 | 状态 |
|------|------|
| OpenClaw 版本 | 2026.3.13 |
| 连接模式 | WebSocket |
| Agent 数量 | 3 (墨墨/小媒/小猎) |
| 路由状态 | ✅ 已修复 |

---

## 🔐 飞书应用信息

| 机器人 | App ID | Agent | 用途 |
|--------|--------|-------|------|
| **墨墨** | `cli_a930d134f4bb5cc6` | writer | 首席协调员 |
| **小媒** | `cli_a9321f7ed1fa9cb2` | media | 创意专家 |
| **小猎** | `cli_a930e7e7c0b41bdf` | hunter | 信息捕手 |

---

## ⚙️ 配置结构

### 关键字段说明

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "connectionMode": "websocket",
      "accounts": {
        "writer": {              // ← 语义别名（用于路由）
          "appId": "cli_...",    // ← 飞书 AppID（用于认证）
          "appSecret": "..."     // ← 飞书 Secret
        }
      }
    }
  },
  "bindings": [
    {
      "type": "route",           // ← 必须显式声明
      "agentId": "writer",       // ← Agent ID
      "match": {
        "channel": "feishu",
        "accountId": "writer"    // ← 必须等于 accounts 的 Key
      }
    }
  ]
}
```

---

## 🚀 快速启动

### 1. 环境准备

```bash
# 设置 API Key
export BAILIAN_API_KEY=sk-sp-47f76e2c1b2f4e259ae46b956c09d00f
```

### 2. 清理缓存（重要！）

```bash
rm -rf ~/.openclaw/sessions ~/.openclaw/state ~/.openclaw/cache
```

### 3. 启动 Gateway

```bash
openclaw gateway
```

---

## 🔍 故障排查

### 问题：所有消息都被一个 Agent 回复

**原因**: `match.accountId` 使用了原始 AppID 而非语义别名

**解决**: 将 `accountId` 改为 accounts 的 Key（如 `writer`/`media`/`hunter`）

### 问题：配置改了不生效

**原因**: Session 缓存未清理

**解决**: 
```bash
rm -rf ~/.openclaw/sessions
pkill -f openclaw
openclaw gateway
```

### 问题：Doctor 警告 "no valid account-scoped binding"

**原因**: bindings 格式不正确

**解决**: 确保使用 `type: "route"` 并正确配置 `match.accountId`

---

## 📊 验证命令

```bash
# 查看绑定状态
openclaw agents list --bindings

# 查看实时日志
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# 运行诊断
openclaw doctor --fix
```

---

## 📝 配置检查清单

- [ ] `accounts` 使用语义别名作为 Key
- [ ] `bindings` 显式声明 `type: "route"`
- [ ] `match.accountId` 等于 accounts 的 Key
- [ ] 清理旧 Session 缓存
- [ ] 重启 Gateway

---

## 🔗 相关文档

- [OpenClaw 3.13 单实例多飞书 Bot 终极方案](./openclaw-multi-agent-routing.md)
- [密钥管理协议](./key-management-protocol.md)

---

*最后更新: 2026-03-19*  
*维护者: 墨墨 (Mò)*
