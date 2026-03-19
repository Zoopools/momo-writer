# OpenClaw 2026.3.2 配置语法完全指南

**学习时间：** 2026-03-07  
**版本：** 2026.3.2 (85377a2)  
**墨墨学习笔记** 📚

---

## 📋 **配置文件位置**

```bash
# 查看当前配置文件路径
openclaw config file

# 默认位置
~/.openclaw/openclaw.json
```

---

## 🔧 **配置验证命令**

```bash
# 验证配置是否有效
openclaw config validate

# 诊断配置问题
openclaw doctor

# 自动修复配置
openclaw doctor --fix
```

---

## 📊 **完整配置结构**

```json
{
  "meta": {},              // 元数据（自动管理）
  "wizard": {},            // 向导记录（自动管理）
  "models": {},            // 模型配置
  "agents": {},            // Agent 配置 ⭐
  "bindings": [],          // 路由绑定 ⭐
  "commands": {},          // 命令配置
  "channels": {},          // 通道配置 ⭐
  "gateway": {},           // 网关配置 ⭐
  "memory": {},            // 记忆配置
  "plugins": {}            // 插件配置 ⭐
}
```

---

## 🎯 **Agents 配置（核心）**

### ✅ **支持的字段**

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard"  // safeguard | aggressive | none
      },
      "workspace": "~/",     // 默认工作空间
      "heartbeat": {         // ⭐ 心跳配置
        "every": "2h"        // 如 "0m" | "30m" | "2h"
      },
      "tools": {
        "exec": {
          "node": "node-id-or-name"  // 指定执行节点
        }
      }
    },
    "list": [
      {
        "id": "writer",                    // ⭐ Agent ID（必填）
        "name": "墨墨",                     // ⭐ 显示名称
        "workspace": "/path/to/workspace", // ⭐ 工作空间路径
        "model": {
          "primary": "bailian/qwen3.5-plus",    // ⭐ 主模型
          "fallback": "bailian/glm-4.7"         // ⭐ 备用模型
        },
        "tools": {
          "exec": {
            "node": "node-id-or-name"  // 指定执行节点
          }
        }
      }
    ]
  }
}
```

### ❌ **2026.3.2 不支持的字段**

```json
{
  "agents": {
    "defaults": {
      "timeout": 180  // ❌ 不支持
    },
    "list": [
      {
        "timeout": 300,        // ❌ 不支持
        "autoApprove": [],     // ❌ 不支持
        "permissions": {}      // ❌ 不支持
      }
    ]
  }
}
```

**错误信息：**
```
Invalid config at /Users/wh1ko/.openclaw/openclaw.json:
- agents.defaults: Unrecognized key: "timeout"
- agents.list.0: Unrecognized keys: "timeout", "autoApprove", "permissions"
```

---

## 🔗 **Bindings 配置（路由）**

### ✅ **支持的字段**

```json
{
  "bindings": [
    {
      "agentId": "writer",  // ⭐ Agent ID
      "match": {
        "channel": "feishu",     // ⭐ 通道类型
        "accountId": "writer"    // ⭐ 账号 ID
      }
    }
  ]
}
```

**说明：**
- `agentId`: 必须与 `agents.list[].id` 匹配
- `channel`: 通道类型（feishu | telegram | discord 等）
- `accountId`: 通道账号 ID（与 `channels.*.accounts` 匹配）

---

## 📱 **Channels 配置（通道）**

### ✅ **Feishu 通道配置**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,  // ⭐ 是否启用
      "accounts": {     // ⭐ 多账号配置
        "writer": {
          "appId": "cli_xxx",         // ⭐ 飞书 App ID
          "appSecret": "xxx"          // ⭐ 飞书 App Secret
        },
        "media": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        }
      },
      "connectionMode": "websocket",  // ⭐ 连接模式
      "domain": "feishu",             // ⭐ 域名
      "groupPolicy": "open",          // ⭐ 群聊策略
      "dmPolicy": "open",             // ⭐ 私聊策略
      "allowFrom": ["*"]              // ⭐ 允许来源
    }
  }
}
```

### ❌ **不支持的字段**

```json
{
  "channels": {
    "feishu": {
      "bots": []  // ❌ 2026.3.2 不支持 bots 数组格式
    }
  }
}
```

**正确格式：** 使用 `accounts` 对象 + `bindings` 数组

---

## 🌐 **Gateway 配置（网关）**

### ✅ **支持的字段**

```json
{
  "gateway": {
    "port": 18789,           // ⭐ 端口号
    "mode": "local",         // ⭐ 模式（local | remote）
    "bind": "loopback",      // ⭐ 绑定模式
    "auth": {
      "mode": "token",       // ⭐ 认证模式
      "token": "xxx"         // ⭐ 认证令牌
    }
  }
}
```

**说明：**
- `mode: "local"` - 本地模式（必须设置，否则启动失败）
- `bind: "loopback"` - 仅本地访问
- `bind: "lan"` - 局域网访问
- `auth.mode: "token"` - 令牌认证

---

## 🔌 **Plugins 配置（插件）**

### ✅ **支持的字段**

```json
{
  "plugins": {
    "allow": [              // ⭐ 允许的插件列表
      "feishu-openclaw-plugin"
    ],
    "entries": {            // ⭐ 插件条目
      "feishu": {
        "enabled": false    // 禁用内置插件
      },
      "feishu-openclaw-plugin": {
        "enabled": true     // 启用官方插件
      }
    },
    "installs": {           // ⭐ 已安装插件（自动管理）
      "feishu-openclaw-plugin": {
        "source": "npm",
        "spec": "@larksuiteoapi/feishu-openclaw-plugin",
        "installPath": "/path/to/plugin",
        "version": "2026.3.7-beta.1"
      }
    }
  }
}
```

**注意：**
- `plugins.entries.feishu.id` 字段 ❌ 不支持
- 插件 ID 不匹配警告可以忽略

---

## 🧠 **Memory 配置（记忆）**

### ✅ **支持的字段**

```json
{
  "memory": {
    "backend": "qmd"  // ⭐ 记忆后端（qmd | simple）
  }
}
```

**说明：**
- `qmd` - Quad Memory Database（推荐）
- `simple` - 简单文件存储

---

## 🤖 **Models 配置（模型）**

### ✅ **支持的字段**

```json
{
  "models": {
    "mode": "merge",  // ⭐ 模式（merge | strict）
    "providers": {    // ⭐ 模型提供商
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-xxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus"
          }
        ]
      }
    }
  }
}
```

---

## ⚙️ **Commands 配置（命令）**

### ✅ **支持的字段**

```json
{
  "commands": {
    "native": "auto",        // ⭐ 本地命令模式
    "nativeSkills": "auto",  // ⭐ 本地 Skills 模式
    "restart": true,         // ⭐ 自动重启
    "ownerDisplay": "raw"    // ⭐ 所有者显示模式
  }
}
```

---

## 📝 **配置修改最佳实践**

### 步骤 1：备份配置

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
```

### 步骤 2：修改配置

```bash
vim ~/.openclaw/openclaw.json
```

### 步骤 3：验证配置

```bash
openclaw config validate
```

### 步骤 4：诊断问题

```bash
openclaw doctor
```

### 步骤 5：自动修复

```bash
openclaw doctor --fix
```

### 步骤 6：重启网关

```bash
openclaw gateway restart --force
```

### 步骤 7：验证状态

```bash
openclaw status
```

---

## 🚫 **常见错误配置**

### 错误 1：添加不支持的字段

```json
// ❌ 错误
{
  "agents": {
    "list": [
      {
        "timeout": 300,  // 不支持
        "autoApprove": []  // 不支持
      }
    ]
  }
}

// ✅ 正确
{
  "agents": {
    "list": [
      {
        "id": "writer",
        "workspace": "/path/to/workspace"
      }
    ]
  }
}
```

### 错误 2：使用旧版 bots 格式

```json
// ❌ 错误
{
  "channels": {
    "feishu": {
      "bots": [  // 不支持
        { "appId": "xxx", "agentId": "writer" }
      ]
    }
  }
}

// ✅ 正确
{
  "channels": {
    "feishu": {
      "accounts": {
        "writer": { "appId": "xxx", "appSecret": "xxx" }
      }
    }
  },
  "bindings": [
    { "agentId": "writer", "match": { "channel": "feishu", "accountId": "writer" } }
  ]
}
```

### 错误 3：忘记设置 gateway.mode

```json
// ❌ 错误
{
  "gateway": {
    "port": 18789
    // 缺少 mode 字段
  }
}

// ✅ 正确
{
  "gateway": {
    "port": 18789,
    "mode": "local"  // 必须设置
  }
}
```

---

## 🛠️ **配置修改命令参考**

### 使用 CLI 修改

```bash
# 获取配置值
openclaw config get agents.defaults.workspace

# 设置配置值
openclaw config set agents.defaults.workspace "~/projects"

# 设置数组值
openclaw config set plugins.allow '["feishu-openclaw-plugin"]' --strict-json

# 设置对象值
openclaw config set agents.list[0].tools.exec.node "node-1"

# 删除配置值
openclaw config unset agents.defaults.heartbeat

# 验证配置
openclaw config validate
```

### 直接编辑文件

```bash
# 编辑配置文件
vim ~/.openclaw/openclaw.json

# 验证 JSON 格式
cat ~/.openclaw/openclaw.json | python3 -m json.tool > /dev/null

# 重启网关
openclaw gateway restart --force
```

---

## 📋 **配置检查清单**

### 修改前

- [ ] 备份当前配置
- [ ] 确认 OpenClaw 版本
- [ ] 查阅版本文档
- [ ] 运行 `openclaw doctor` 检查状态

### 修改后

- [ ] 验证 JSON 格式
- [ ] 运行 `openclaw config validate`
- [ ] 运行 `openclaw doctor`
- [ ] 重启网关
- [ ] 验证状态 `openclaw status`
- [ ] 测试功能（飞书机器人回复）

---

## 💡 **版本兼容性说明**

### 2026.3.2 支持的特性

- ✅ `agents.list[]` 数组格式
- ✅ `channels.feishu.accounts` 多账号
- ✅ `bindings[]` 路由绑定
- ✅ `plugins.allow` 插件白名单
- ✅ `agents.defaults.heartbeat` 心跳配置
- ✅ `gateway.mode` 网关模式

### 2026.3.2 不支持的特性

- ❌ `agents.list[].timeout`
- ❌ `agents.list[].autoApprove`
- ❌ `agents.list[].permissions`
- ❌ `channels.feishu.bots[]` 数组格式
- ❌ `plugins.entries.*.id` 字段

---

## 🔗 **相关文档**

- CLI 配置：https://docs.openclaw.ai/cli/config
- Agents 管理：https://docs.openclaw.ai/cli/agents
- 完整文档索引：https://docs.openclaw.ai/llms.txt

---

*墨墨学习笔记 - 2026-03-07* 🖤  
*从故障中学习，避免重复踩坑！*
