# OpenClaw 3.13 单实例多飞书 Bot 终极方案

**创建时间**: 2026-03-19  
**作者**: 墨墨 (Mò)  
**版本**: 1.0  
**标签**: #OpenClaw #飞书 #多Agent #路由

---

## 🎯 核心突破：语义别名路由

### 致命死结：原始 ID (AppID) vs. 语义别名 (Alias)

我们之前的逻辑：认为 `accountId` 必须是飞书后台的 `cli_a93...` 原始 ID。

**错误写法** ❌：
```json
{
  "bindings": [{
    "agentId": "hunter",
    "match": {
      "channel": "feishu",
      "accountId": "cli_a930e7..."  // ← 错误！用原始 AppID
    }
  }]
}
```

**正确写法** ✅：
```json
{
  "accounts": {
    "hunter": { "appId": "cli_a930e7...", "appSecret": "..." }
  },
  "bindings": [{
    "type": "route",  // ← 显式声明类型
    "agentId": "hunter",
    "match": {
      "channel": "feishu",
      "accountId": "hunter"  // ← 正确！用别名，不是 AppID
    }
  }]
}
```

---

## 🔍 3.13 底层真相

| 层级 | 说明 |
|------|------|
| **accounts Key** | 别名 (`hunter`/`media`/`writer`) 是**逻辑身份证** |
| **appId** | 只是飞书后台的物理凭证，不用于路由匹配 |
| **match.accountId** | 必须等于 accounts 的 **Key（别名）** |

---

## 🕳️ 三大深坑

| 坑 | 说明 | 解决 |
|---|---|---|
| **路径依赖** | 习惯性认为 `accountId` = 飞书 AppID | 改用语义别名 |
| **配置陷阱** | 缺少 `type: "route"` 显式声明 | 必须显式声明 |
| **缓存毒药** | 旧的 Session 不清理，配置改了也不生效 | `rm -rf ~/.openclaw/sessions` |

---

## ⚡ 关键命令

```bash
# 必须执行！清理缓存毒药
rm -rf ~/.openclaw/sessions ~/.openclaw/state ~/.openclaw/cache

# 重启 Gateway
pkill -f openclaw
openclaw gateway start
```

---

## 📋 完整配置示例

```json
{
  "meta": { "lastTouchedVersion": "2026.3.13" },
  "models": {
    "providers": {
      "bailian": {
        "api": "openai-completions",
        "apiKey": "sk-xxx",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "models": [
          { "id": "qwen3.5-plus", "name": "qwen3.5-plus" },
          { "id": "kimi-k2.5", "name": "kimi-k2.5" }
        ]
      }
    }
  },
  "agents": {
    "list": [
      { "id": "hunter", "name": "小猎", "workspace": "/Users/xxx/openclaw/agents/hunter", "model": { "primary": "bailian/qwen3.5-plus" } },
      { "id": "media", "name": "小媒", "workspace": "/Users/xxx/openclaw/agents/media", "model": { "primary": "bailian/qwen3.5-plus" } },
      { "id": "writer", "name": "墨墨", "workspace": "/Users/xxx/openclaw/agents/writer", "model": { "primary": "bailian/kimi-k2.5" } }
    ]
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "connectionMode": "websocket",
      "accounts": {
        "hunter": { "appId": "cli_xxx1", "appSecret": "xxx" },
        "media": { "appId": "cli_xxx2", "appSecret": "xxx" },
        "writer": { "appId": "cli_xxx3", "appSecret": "xxx" }
      }
    }
  },
  "bindings": [
    { "type": "route", "agentId": "hunter", "match": { "channel": "feishu", "accountId": "hunter" } },
    { "type": "route", "agentId": "media", "match": { "channel": "feishu", "accountId": "media" } },
    { "type": "route", "agentId": "writer", "match": { "channel": "feishu", "accountId": "writer" } }
  ],
  "gateway": { "port": 18789, "mode": "local" }
}
```

---

## 🔧 运维锦囊

| 命令 | 用途 |
|------|------|
| `openclaw agents list --bindings` | 查看路由绑定状态 |
| `tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log` | 实时日志 |
| `openclaw doctor --fix` | 自动修复配置问题 |

---

## 📝 复盘总结

> "这就是技术的'傲慢与偏见'。我们一直在找门锁的钥匙，却没发现大门其实是声控的。给它一个名字，它才能记住灵魂。"

**关键认知**：OpenClaw 3.13 的 WebSocket 路由机制使用**语义别名**作为逻辑身份证，而非原始 AppID。

---

*最后更新: 2026-03-19*  
*维护者: 墨墨 (Mò)*
