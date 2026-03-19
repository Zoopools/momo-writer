# Image Generation Prompt

## Image Specifications

- **Type**: Infographic
- **Layout**: dense-modules
- **Style**: chalkboard
- **Aspect Ratio**: portrait (9:16)
- **Language**: Chinese (zh-CN)

## Core Principles

- Follow the layout structure precisely for information architecture
- Apply style aesthetics consistently throughout
- Keep information concise, highlight keywords and core concepts
- Use compact spacing to maximize information density
- Maintain clear visual hierarchy through size, color, and placement

## Layout Guidelines: dense-modules

High-density modular layout with 6-7 typed information modules packed with concrete data.

### Structure
- 6-7 distinct modules per image, each serving a specific information function
- Every module contains concrete data: commands, steps, parameters
- Minimal whitespace—compact spacing prioritized over breathing room
- Smaller text acceptable to maximize information density
- Each module identified by coordinate label (e.g., MOD-1, SEC-A, B-03)

### Module Archetypes
1. **Brand/Selection Array**: Grid of options with recommendations
2. **Quick Reference**: Compact summary with commands
3. **Deep Dive**: Technical breakdown of key concepts
4. **Step-by-Step**: Sequential process flow
5. **Warning/Pitfall Zone**: Critical mistakes to avoid
6. **Scenario Comparison**: Side-by-side use cases
7. **Checklist**: How-to format (look/test/check)

### Visual Elements
- Module boundary markers (thick lines, dotted frames, or coordinate grids)
- Coordinate labels in corners (MOD-1, SEC-A, B-03)
- Data callout boxes with highlighted numbers
- Progression indicators and arrows
- Warning/alert visual markers for pitfall modules
- Metadata in corners (section numbers, small markers)

### Text Placement
- Main title at top, prominent and impactful
- Module headers inside colored badges or labeled frames
- Body text compact, multiple columns within modules when possible
- Numbers and commands highlighted with accent colors, slightly larger than body text
- Every corner should contain useful information or metadata

## Style Guidelines: chalkboard

Classic classroom chalkboard aesthetic with hand-drawn chalk illustrations.

### Background
- Color: Chalkboard Black (#1A1A1A) or Dark Green-Black (#1C2B1C)
- Texture: Realistic chalkboard texture with subtle scratches, dust particles, and faint eraser marks

### Typography
- Hand-drawn chalk lettering style with visible chalk texture
- Imperfect baseline adds authenticity
- White or bright colored chalk for emphasis

### Color Palette
- Background: Chalkboard Black (#1A1A1A)
- Primary Text: Chalk White (#F5F5F5)
- Accent 1 (Highlights): Chalk Yellow (#FFE566)
- Accent 2 (Secondary): Chalk Pink (#FF9999)
- Accent 3 (Diagrams): Chalk Blue (#66B3FF)
- Accent 4 (Success): Chalk Green (#90EE90)
- Accent 5 (Warnings): Chalk Orange (#FFB366)

### Visual Elements
- Hand-drawn chalk illustrations with sketchy, imperfect lines
- Chalk dust effects around text and key elements
- Doodles: stars, arrows, underlines, circles, checkmarks
- Eraser smudges and chalk residue textures
- Wooden frame border optional
- Stick figures and simple icons
- Connection lines with hand-drawn feel

### Style Rules
- Maintain authentic chalk texture on all elements
- Use imperfect, hand-drawn quality throughout
- Add subtle chalk dust and smudge effects
- Create visual hierarchy with color variety
- Include playful doodles and annotations

---

## Content: OpenClaw 新手入门指南

### MODULE 1: [MOD-01] 什么是 OpenClaw？

**Title: OpenClaw 架构**
**Type: Brand/Selection Array**

**核心概念**: 自托管 AI Agent 网关

**特点 (4个图标项):**
✓ 自托管 - 数据由你控制
✓ 多通道 - 一个 Gateway 服务所有平台
✓ Agent 原生 - 工具使用、会话、内存、路由
✓ 开源 - MIT 许可证，社区驱动

**系统要求:**
- Node 22+
- macOS / Linux / Windows (WSL2)
- API 密钥

**Visual:**
架构图: 聊天应用 → Gateway → AI Agent
用箭头连接，简图标表示

---

### MODULE 2: [SEC-A] 快速安装

**Title: 一键安装**
**Type: Step-by-Step**

**方法 1: 安装脚本（推荐）**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```
或
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**方法 2: npm / pnpm**
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

**流程图标:**
1️⃣ 选择方式 → 2️⃣ 运行命令 → 3️⃣ 完成安装 → 4️⃣ 启动向导

**Visual:**
分步骤流程，每步用数字标记

---

### MODULE 3: [B-03] 初始化配置

**Title: openclaw onboard**
**Type: Checklist**

**引导向导会自动完成:**

☑ 选择 AI 提供商 (OpenAI/Anthropic 等)
☑ 配置 API 密钥
☑ 选择聊天通道 (WhatsApp/Telegram 等)
☑ 设置 Agent 和工作区
☑ 启动 Gateway 守护进程

**Visual:**
检查清单，每项前面有 ✅ 标记

---

### MODULE 4: [MOD-04] 核心概念

**Title: 4 大支柱**
**Type: Deep Dive**

**四象限图:**

[Gateway] - 会话、路由、通道连接唯一来源

[Session] - 独立对话上下文 (消息历史、状态、内存)

[Agent] - AI 实体 (提示词、工具、权限、内存)

[Channel] - 消息渠道 (WhatsApp/Telegram/Discord/iMessage/飞书)

**Visual:**
四象限布局，中心放 OpenClaw logo

---

### MODULE 5: [SEC-E] 常用命令

**Title: CLI 操作**
**Type: Quick Reference**

**Gateway 管理:**
```bash
openclaw gateway status/start/stop/restart
```

**Agent 管理:**
```bash
openclaw agents list
openclaw agents get <name>
```

**会话管理:**
```bash
openclaw sessions list
openclaw sessions history
```

**Web 控制台:**
```bash
openclaw web
```

**Visual:**
命令分组，用不同颜色边框区分

---

### MODULE 6: [MOD-06] 技能与移动端

**Title: 扩展能力**
**Type: Scenario Comparison**

**ClawHub 技能:**
```bash
openclaw clawhub search <keyword>
openclaw clawhub install <skill-name>
```

**技能类型:**
- 飞书集成 (日历/任务/文档)
- GitHub 集成 (Issue/PR)
- 媒体创作 (图片/文档)
- 数据分析
- 自动化工具

**移动端节点:**
iOS & Android 配对获得:
📱 Canvas 渲染 📷 摄像头 🖥️ 屏幕 🎤 语音

**配对:**
```bash
openclaw pairing approve <code>
```

**Visual:**
技能图标网格 + 移动设备图标

---

### MODULE 7: [SEC-G] Web 控制台

**Title: openclaw web**
**Type: Dashboard**

**功能模块:**
💬 聊天界面
⚙️ 配置管理
📊 会话监控
📱 节点管理
🔧 调试工具

**Visual:**
仪表盘预览，显示各功能入口

---

### MODULE 8: [B-08] 故障排查

**Title: 快速诊断**
**Type: Warning/Pitfall Zone**

**Gateway 无法启动:**
```bash
openclaw gateway status
openclaw gateway logs
```

**API 配置错误:**
检查: `~/.openclaw/config/providers.yaml`

**通道连接失败:**
1. 检查网络连接
2. 验证 API 凭据
3. 查看日志

**Visual:**
问题诊断流程图，⚠️ 警告图标

---

### MODULE 9: [MOD-09] 下一步

**Title: 深入学习**
**Type: Brand/Selection Array**

**学习资源:**
📚 docs.openclaw.ai - 完整文档
🚀 快速入门指南
💻 GitHub 仓库
💬 社区 Discord

**提示:**
开源项目，欢迎贡献！

**Visual:**
资源卡片，每个带图标

---

## Design Notes
- 黑板风格：使用粉笔字质感、黑板背景 (#1A1A1A)
- 代码块：用白色/浅色背景显示，模拟教学板书
- 图标：简洁的线框图标，配合粉笔手绘感
- 布局：高密度模块，紧凑但有序
- 配色：黑板绿/深灰 + 粉笔白/黄/粉/蓝/绿/橙
- 添加 chalk dust 效果和 doodle 装饰
- 每个模块用坐标标记 (MOD-01, SEC-A, B-03 等)
- 用不同颜色边框或标记区分模块类型

Generate a professional, high-density infographic with chalkboard style in portrait (9:16) aspect ratio.