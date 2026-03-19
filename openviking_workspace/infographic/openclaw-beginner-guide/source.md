# OpenClaw 新手入门指南

## 什么是 OpenClaw？

OpenClaw 是一个自托管的 AI Agent 网关，将你的聊天应用（WhatsApp、Telegram、Discord、iMessage 等）连接到 AI 编程助手（如 Pi）。在你的机器上运行单个 Gateway 进程，它就成为消息应用和随时可用的 AI 助手之间的桥梁。

**核心特点：**
- 自托管：在你自己的硬件上运行，数据由你控制
- 多通道：一个 Gateway 同时服务 WhatsApp、Telegram、Discord 等多个平台
- Agent 原生：为编程 Agent 构建，支持工具使用、会话、内存和多 Agent 路由
- 开源：MIT 许可证，社区驱动

**系统要求：**
- Node 22+
- macOS、Linux 或 Windows（推荐 WSL2）
- API 密钥（OpenAI、Anthropic 等）

## 快速开始

### 方法 1：安装脚本（推荐）

macOS / Linux / WSL2：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Windows (PowerShell)：
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

脚本会自动处理 Node 检测、安装和引导向导。

### 方法 2：npm / pnpm

如果你已有 Node 22+：

npm：
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

pnpm：
```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g
openclaw onboard --install-daemon
```

## 初始化配置

运行引导向导：
```bash
openclaw onboard
```

向导会帮你：
1. 选择 AI 提供商（OpenAI、Anthropic 等）
2. 配置 API 密钥
3. 选择聊天通道（WhatsApp、Telegram 等）
4. 设置 Agent 和工作区
5. 启动 Gateway 守护进程

## 核心概念

### Gateway（网关）

Gateway 是会话、路由和通道连接的唯一真实来源。它管理所有消息路由和 AI Agent 的交互。

### Session（会话）

每个会话是独立的对话上下文，包含：
- 消息历史
- Agent 状态
- 工具调用记录
- 内存数据

### Agent（代理）

Agent 是执行具体任务的 AI 实体。每个 Agent 可以有：
- 专用的提示词（system prompt）
- 特定的工具权限
- 独立的内存空间

### Channel（通道）

Channel 是消息传输渠道，支持：
- WhatsApp
- Telegram
- Discord
- iMessage
- 飞书（通过插件）
- 等

## 常用命令

### Gateway 管理
```bash
openclaw gateway status    # 查看状态
openclaw gateway start     # 启动
openclaw gateway stop      # 停止
openclaw gateway restart   # 重启
```

### Agent 管理
```bash
openclaw agents list       # 列出所有 Agent
openclaw agents get <name> # 查看 Agent 详情
```

### 会话管理
```bash
openclaw sessions list     # 列出会话
openclaw sessions history  # 查看会话历史
```

### Web 控制台
```bash
openclaw web               # 启动 Web 控制台
```

## 技能（Skills）

OpenClaw 支持扩展技能，增强 Agent 能力：

技能可以通过 ClawHub 安装：
```bash
openclaw clawhub search <keyword>
openclaw clawhub install <skill-name>
```

### 技能类型

- 飞书集成（日历、任务、文档管理）
- GitHub 集成（Issue、PR 管理）
- 媒体创作（图片生成、文档转换）
- 数据分析
- 自动化工具

## 移动端节点

你可以将 iOS 和 Android 设备配对为 OpenClaw 节点，获得：
- Canvas 渲染
- 摄像头/屏幕访问
- 语音输入

配对流程：
1. 在移动端安装 OpenClaw Node 应用
2. 生成配对代码
3. 在 Gateway 批准：`openclaw pairing approve <code>`

## Web 控制台

启动 Web 控制台：
```bash
openclaw web
```

控制台提供：
- 💬 聊天界面
- ⚙️ 配置管理
- 📊 会话监控
- 📱 节点管理
- 🔧 调试工具

## 故障排查

### Gateway 无法启动
```bash
openclaw gateway status
openclaw gateway logs
```

### API 配置错误
检查 `~/.openclaw/config/providers.yaml`

### 通道连接失败
1. 检查网络连接
2. 验证 API 凭据
3. 查看日志：`openclaw gateway logs`

## 下一步

- 📚 [完整文档](https://docs.openclaw.ai)
- 🚀 [获取指南](https://docs.openclaw.ai/start/getting-started)
- 💻 [GitHub 仓库](https://github.com/openclaw/openclaw)
- 💬 [社区 Discord](https://discord.com/invite/clawd)

---

**提示：OpenClaw 是开源项目，欢迎贡献！**