# Structured Content - OpenClaw 新手入门指南

## Learning Objectives
学习本指南后，你将能够：
- 理解 OpenClaw 的核心概念和架构
- 完成安装和初始化配置
- 掌握常用命令和操作
- 配置技能系统和移动端节点
- 使用 Web 控制台进行管理

---

## Section 1: 什么是 OpenClaw？

**Key Concept:** 自托管的 AI Agent 网关

**Content:**
OpenClaw 是一个自托管的 AI Agent 网关，将你的聊天应用（WhatsApp、Telegram、Discord、iMessage 等）连接到 AI 编程助手。

**核心特点:**
- 自托管：在你自己的硬件上运行，数据由你控制
- 多通道：一个 Gateway 同时服务多个平台
- Agent 原生：支持工具使用、会话、内存和多 Agent 路由
- 开源：MIT 许可证，社区驱动

**系统要求:**
- Node 22+
- macOS、Linux 或 Windows（推荐 WSL2）
- API 密钥

**Visual Element:**
图示：聊天应用 → Gateway → AI Agent 的数据流架构图

**Text Labels:**
消息传输桥梁、多平台支持、数据自主可控

---

## Section 2: 快速开始 - 安装方法

**Key Concept:** 一键安装，快速上手

**Content:**
两种推荐安装方式：

**方法 1：安装脚本（推荐）**
macOS / Linux / WSL2：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Windows (PowerShell)：
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**方法 2：npm / pnpm**
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

或
```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g
openclaw onboard --install-daemon
```

**Visual Element:**
分步骤图标：1️⃣ 选择安装方式 → 2️⃣ 运行命令 → 3️⃣ 完成安装 → 4️⃣ 运行引导

**Text Labels:**
自动检测 Node、安装并配置、启动引导向导

---

## Section 3: 初始化配置

**Key Concept:** 引导向导，自动配置

**Content:**
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

**Visual Element:**
配置检查清单，每项前面有 ✅ 标记

**Text Labels:**
智能引导、一步到位、自动完成

---

## Section 4: 核心概念

**Key Concept:** 四大支柱，理解架构

**Content:**
1. **Gateway（网关）**
   会话、路由和通道连接的唯一真实来源

2. **Session（会话）**
   独立的对话上下文，包含消息历史、Agent 状态、工具调用、内存

3. **Agent（代理）**
   执行具体任务的 AI 实体，有专用提示词、工具权限、独立内存

4. **Channel（通道）**
   消息传输渠道：WhatsApp、Telegram、Discord、iMessage、飞书等

**Visual Element:**
四象限图，每个概念一个象限，中心是 OpenClaw Logo

**Text Labels:**
网关枢纽、会话上下文、智能代理、多通道支持

---

## Section 5: 常用命令

**Key Concept:** CLI 操作，高效管理

**Content:**

**Gateway 管理**
```bash
openclaw gateway status    # 查看状态
openclaw gateway start     # 启动
openclaw gateway stop      # 停止
openclaw gateway restart   # 重启
```

**Agent 管理**
```bash
openclaw agents list       # 列出所有 Agent
openclaw agents get <name> # 查看 Agent 详情
```

**会话管理**
```bash
openclaw sessions list     # 列出会话
openclaw sessions history  # 查看会话历史
```

**Web 控制台**
```bash
openclaw web               # 启动 Web 控制台
```

**Visual Element:**
命令分组卡片，每组用不同颜色边框区分

**Text Labels:**
进程管理、Agent 管理、会话追踪、Web 界面

---

## Section 6: 技能（Skills）系统

**Key Concept:** 插件扩展，无限可能

**Content:**
通过 ClawHub 安装技能：
```bash
openclaw clawhub search <keyword>
openclaw clawhub install <skill-name>
```

**技能类型:**
- 飞书集成（日历、任务、文档管理）
- GitHub 集成（Issue、PR 管理）
- 媒体创作（图片生成、文档转换）
- 数据分析
- 自动化工具

**Visual Element:**
技能图标网格，每个技能一个图标 + 简短标签

**Text Labels:**
开源生态、社区贡献、即插即用

---

## Section 7: 移动端节点

**Key Concept:** 设备配对，扩展能力

**Content:**
配对移动设备获得：
- Canvas 渲染
- 摄像头/屏幕访问
- 语音输入

**配对流程:**
1. 在移动端安装 OpenClaw Node 应用
2. 生成配对代码
3. 在 Gateway 批准：`openclaw pairing approve <code>`

**Visual Element:**
三步流程图，配对连接动画

**Text Labels:**
iOS & Android、增强交互、实时同步

---

## Section 8: Web 控制台

**Key Concept:** 可视化界面，便捷管理

**Content:**
启动 Web 控制台：
```bash
openclaw web
```

**功能模块:**
- 💬 聊天界面
- ⚙️ 配置管理
- 📊 会话监控
- 📱 节点管理
- 🔧 调试工具

**Visual Element:**
仪表盘预览图，显示各功能模块入口

**Text Labels:**
一站式管理、实时监控、可视化配置

---

## Section 9: 故障排查

**Key Concept:** 快速诊断，解决问题

**Content:**

**Gateway 无法启动**
```bash
openclaw gateway status
openclaw gateway logs
```

**API 配置错误**
检查 `~/.openclaw/config/providers.yaml`

**通道连接失败**
1. 检查网络连接
2. 验证 API 凭据
3. 查看日志：`openclaw gateway logs`

**Visual Element:**
问题诊断流程图，显示常见问题及解决路径

**Text Labels:**
日志分析、配置检查、网络验证

---

## Section 10: 下一步

**Key Concept:** 深入学习，持续探索

**Content:**
- 📚 [完整文档](https://docs.openclaw.ai)
- 🚀 [快速入门](https://docs.openclaw.ai/start/getting-started)
- 💻 [GitHub 仓库](https://github.com/openclaw/openclaw)
- 💬 [社区 Discord](https://discord.com/invite/clawd)

**Visual Element:**
资源卡片，每个资源一个卡片带图标

**Text Labels:**
开源项目、欢迎贡献、社区支持

---

## Design Notes
- 黑板风格：使用粉笔字质感、黑板背景
- 代码块：用白色/浅色背景显示，模拟教学板书
- 图标：简洁的线框图标，配合粉笔手绘感
- 布局：教学风格的信息组织，适合新手学习
- 配色：经典黑板绿/深灰 + 粉笔白/黄/粉/蓝