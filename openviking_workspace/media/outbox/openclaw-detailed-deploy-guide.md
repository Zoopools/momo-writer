# OpenClaw 本地部署完整指南：从零开始搭建你的私人 AI 助手

> 不需要服务器，不需要订阅，5 分钟让你拥有一个完全属于自己的 AI 助手

你是否想过：**能否拥有一个真正"私人的" AI 助手？**

- 不用担心聊天记录被上传到云端
- 24 小时待命，随时响应
- 在你常用的所有平台上使用
- 一次配置，长期使用

答案是：**有，而且很简单**。

这篇文章会带你一步步完成 OpenClaw 的本地部署，从零开始，直到你的 AI 助手上线。

---

## 什么是 OpenClaw？

**OpenClaw** 是一个运行在你自己设备上的**个人 AI 助手**。

它不是云端 SaaS 服务，而是一个开源项目。这意味着：

- ✅ **完全隐私**：你的数据永远不会离开你的设备
- ✅ **完全控制**：想怎么配置就怎么配置
- ✅ **永远在线**：24 小时待命
- ✅ **多平台支持**：WhatsApp、Telegram、微信、Slack、Discord 等 15+ 平台
- ✅ **开源免费**：不用订阅，想改就改

---

## 系统要求

在开始之前，先确认你的设备满足以下要求：

### 最低配置

- **操作系统**：macOS / Linux / Windows (WSL2)
- **Node.js**：≥ 22.0.0
- **内存**：≥ 4GB RAM
- **存储**：≥ 500MB 可用空间

### 推荐配置

- **内存**：≥ 8GB RAM
- **存储**：≥ 2GB 可用空间

---

## 第 1 步：安装 Node.js

OpenClaw 需要 Node.js 22 或更高版本。

### macOS / Linux

推荐使用 nvm（Node Version Manager）安装：

```bash
# 1. 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 2. 重新加载 shell 配置
source ~/.bashrc  # 或 ~/.zshrc

# 3. 安装 Node.js 22
nvm install 22

# 4. 使用 Node.js 22
nvm use 22

# 5. 设置为默认版本
nvm alias default 22
```

### Windows (WSL2)

```bash
# 1. 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 2. 重新加载 shell 配置
source ~/.bashrc

# 3. 安装 Node.js 22
nvm install 22

# 4. 使用 Node.js 22
nvm use 22
```

### 验证安装

```bash
node --version
# 应该输出：v22.x.x

npm --version
# 应该输出：10.x.x 或更高
```

---

## 第 2 步：安装 OpenClaw

打开终端，运行以下命令：

```bash
npm install -g openclaw@latest
```

等待安装完成（通常需要 1-2 分钟）。

### 验证安装

```bash
openclaw --version
# 应该输出：OpenClaw 2026.x.x
```

---

## 第 3 步：启动安装向导

OpenClaw 提供了交互式安装向导，会引导你完成所有配置。

```bash
openclaw onboard --install-daemon
```

向导会问你以下问题：

### 1. 工作空间设置

**问题**：工作空间路径？
**推荐**：`~/openclaw`（默认）
**说明**：这是 OpenClaw 存储配置和数据的目录

### 2. Gateway 配置

**问题**：Gateway 端口？
**推荐**：18789（默认）
**说明**：这是 OpenClaw 网关服务的端口，确保端口未被占用

### 3. AI 模型选择

向导会列出支持的 AI 模型：

**免费模型**：
- **DeepSeek**（推荐，性价比高）
- **Ollama**（本地模型，完全免费）

**付费模型**：
- **OpenAI GPT-4**
- **Anthropic Claude**
- **Google Gemini**

**推荐选择**：DeepSeek（免费 + 高质量）

选择模型后，输入 API Key。

### 4. 渠道配置

向导会询问你想连接哪些平台：

**推荐配置**：
- ✅ **Feishu**（如果你在国内）
- ✅ **Telegram**（国际用户首选）
- ✅ **WhatsApp**（最广泛）

选择一个或多个平台，按照向导提示完成授权。

### 5. 守护进程安装

向导会自动安装 Gateway 守护进程，确保 OpenClaw 在后台运行。

**macOS**: 使用 launchd
**Linux**: 使用 systemd

---

## 第 4 步：启动 OpenClaw

安装完成后，启动 OpenClaw：

```bash
openclaw gateway start
```

### 验证运行

```bash
openclaw gateway status
# 应该显示：Running
```

---

## 第 5 步：测试你的 AI 助手

现在你的 AI 助手已经上线了！

### 测试方式 1：命令行

```bash
# 直接和助手对话
openclaw agent --message "你好，你是谁？"

# 高级思考模式
openclaw agent --message "帮我规划一个学习计划" --thinking high
```

### 测试方式 2：配置的平台

打开你配置的平台（如 Feishu、Telegram），给你的 AI 助手发一条消息：

```
你好，你是谁？
```

如果收到回复，恭喜你！你的 AI 助手已经成功上线！🎉

---

## 常见问题

### Q1：安装失败怎么办？

运行诊断命令：

```bash
openclaw doctor
```

它会检查你的系统配置，告诉你问题在哪。

### Q2：如何更新？

```bash
openclaw update
```

### Q3：如何停止 OpenClaw？

```bash
openclaw gateway stop
```

### Q4：如何重新启动？

```bash
openclaw gateway restart
```

### Q5：查看日志？

```bash
openclaw gateway logs
```

### Q6：如何配置更多渠道？

```bash
openclaw configure --section channels
```

### Q7：如何切换 AI 模型？

```bash
openclaw configure --section models
```

---

## 进阶配置

### 自定义技能

OpenClaw 支持安装扩展技能：

```bash
# 列出可用技能
openclaw skills list

# 安装技能
openclaw skills install <skill-name>
```

**常用技能**：
- 天气查询
- GitHub 集成
- 飞书集成
- 图片生成
- 文章生成

### 工作区管理

```bash
# 创建新工作区
openclaw workspace create <name>

# 切换工作区
openclaw workspace use <name>

# 列出所有工作区
openclaw workspace list
```

---

## 总结

通过以上 5 个步骤，你已经成功搭建了自己的 AI 助手：

1. ✅ 安装 Node.js
2. ✅ 安装 OpenClaw
3. ✅ 运行安装向导
4. ✅ 启动 Gateway
5. ✅ 测试 AI 助手

**现在你的 AI 助手已经上线了！**

它会在后台持续运行，随时响应你的请求。

---

## 下一步

### 学习更多

- 📚 [官方文档](https://docs.openclaw.ai)
- 💬 [Discord 社区](https://discord.gg/clawd)
- 🐙 [GitHub 仓库](https://github.com/openclaw/openclaw)

### 探索功能

- 配置更多渠道
- 安装更多技能
- 自定义提示词
- 创建工作流

---

**开始你的 AI 助手之旅吧！** 🚀

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

有问题？在评论区告诉我，我来帮你解决！