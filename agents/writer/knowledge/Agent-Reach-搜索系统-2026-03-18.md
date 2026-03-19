# Agent Reach — 全域搜索系统

**整理时间**: 2026-03-18  
**整理人**: 墨墨  
**状态**: ⚠️ 已安装但未完全配置

---

## 📍 位置信息

| 项目 | 路径 |
|------|------|
| **安装目录** | `~/.openclaw/tools/agent-reach/` |
| **Skill 文档** | `~/.openclaw/tools/agent-reach/agent_reach/skill/SKILL.md` |
| **配置模板** | `~/.openclaw/tools/agent-reach/.env.example` |
| **CLI 入口** | `agent-reach` (需要安装到 PATH) |

---

## 🔍 当前状态

### ✅ 已存在
- Agent Reach 代码库已克隆到本地
- Skill 文档已存在
- 支持 16+ 平台的配置指南

### ❌ 未完成
- Python 包未安装 (`pip install agent-reach`)
- CLI 命令不在 PATH
- 未配置 API Keys
- 未运行安装脚本

---

## 🚀 Agent Reach 能力清单

Agent Reach 是**专门给 AI Agent 设计的互联网搜索系统**，比内置的 web_search 强大得多！

### 支持的平台

| 平台 | 能力 | 配置需求 |
|------|------|---------|
| 🌐 **任意网页** | 阅读任意 URL | 无需配置 |
| 🔍 **全网搜索** | Exa 语义搜索 | MCP 自动配置 |
| 🐦 **Twitter/X** | 搜索、读推文、时间线 | 需 Cookie |
| 📺 **YouTube** | 字幕提取、视频搜索 | 无需配置 |
| 📺 **B站** | 字幕提取、视频搜索 | 本地可用 |
| 📖 **Reddit** | 搜索、读帖 | 需代理（服务器） |
| 📦 **GitHub** | 仓库搜索、代码搜索 | 可选 Token |
| 📕 **小红书** | 搜索、阅读、发帖 | 需 Cookie |
| 🎵 **抖音** | 视频解析、无水印下载 | 无需登录 |
| 💬 **微信公众号** | 搜索 + 阅读全文 | 无需配置 |
| 📰 **微博** | 热搜、搜索、用户动态 | 无需配置 |
| 💻 **V2EX** | 热门帖子、节点、详情 | 无需配置 |
| 🎙️ **小宇宙播客** | 音频转文字 | 需 Groq Key |
| 💼 **LinkedIn** | Profile、搜索 | 需 Cookie |
| 📡 **RSS** | 订阅任意 RSS | 无需配置 |

---

## 🛠️ 为什么今天"断网"了？

### 根本原因
**Agent Reach 已下载但未完成安装！**

Gemini 提到的 "Agent-Reach 协议" 确实存在，但只完成了第一步（下载代码），没有完成：
1. ❌ Python 包安装
2. ❌ 系统依赖安装
3. ❌ API Keys 配置
4. ❌ 注册到 OpenClaw

### 对比：当前可用 vs Agent Reach

| 功能 | 当前状态 | Agent Reach |
|------|---------|-------------|
| Google 搜索 | ✅ Browser 工具（慢） | ✅ Exa 搜索（快） |
| Twitter/X | ❌ 不可用 | ✅ 搜索+读取 |
| YouTube 字幕 | ❌ 不可用 | ✅ 提取字幕 |
| B站 | ❌ 不可用 | ✅ 字幕+搜索 |
| 小红书 | ❌ 不可用 | ✅ 搜索+阅读 |
| 微信公众号 | ❌ 不可用 | ✅ 搜索+阅读 |
| 微博 | ❌ 不可用 | ✅ 热搜+搜索 |
| Reddit | ❌ 不可用 | ✅ 搜索+读帖 |

---

## 🔧 修复方案

### 方案 A：完整安装 Agent Reach（推荐）

**步骤**:

1. **确保 exec 权限开启**（OpenClaw 需要）
   ```bash
   openclaw config set tools.profile "coding"
   openclaw gateway restart
   ```

2. **运行安装指令**
   ```bash
   cd ~/.openclaw/tools/agent-reach
   pip install -e .
   ```

3. **安装系统依赖**
   ```bash
   agent-reach install --env=auto
   ```

4. **检查状态**
   ```bash
   agent-reach doctor
   ```

5. **配置 API Keys**（可选）
   ```bash
   agent-reach configure
   ```

### 方案 B：快速启用特定功能

如果只需要搜索功能，可以单独配置：

**启用 Exa 搜索**（无需 API Key）:
```bash
# 安装 mcporter
pip install mcporter

# 测试搜索
mcporter call 'exa.web_search_exa(query: "GEO optimization", numResults: 5)'
```

**启用网页阅读**:
```bash
# 使用 Jina Reader（无需配置）
curl -s "https://r.jina.ai/https://example.com/article"
```

---

## 💡 给哥哥的建议

### 当前状况
- ✅ Agent Reach **代码已下载**
- ❌ **未完成安装**
- ❌ **未配置 API Keys**

### 墨墨的建议

**如果哥哥需要频繁进行以下操作，建议完成 Agent Reach 安装**:
1. 搜索 Twitter/X、Reddit 等社交媒体
2. 提取 YouTube/B站视频字幕
3. 搜索小红书、微信公众号
4. 快速网页搜索（比 Browser 快）

**如果只是偶尔搜索，当前 Browser 工具够用**:
- 打开 Google 搜索
- 抓取结果页面
- 提取信息

### 立即可以尝试

Agent Reach 的 **Jina Reader** 功能无需安装即可使用：

```bash
# 读取任意网页（无需安装 Agent Reach）
curl -s "https://r.jina.ai/https://searchengineland.com/mastering-generative-engine-optimization-in-2026-full-guide-469142"
```

这个命令可以**立即使用**，把网页内容转为干净的 Markdown！

---

## 📚 参考文档

- **Agent Reach 主页**: https://github.com/Panniantong/Agent-Reach
- **安装指南**: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
- **更新指南**: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md
- **本地 Skill**: `~/.openclaw/tools/agent-reach/agent_reach/skill/SKILL.md`

---

## 🎯 核心结论

> **Gemini 说得对！** Agent Reach 确实是一个强大的搜索系统，但当前状态是：
> - ✅ 代码已下载
> - ❌ 未完成安装
> - ❌ 未配置 Keys

**墨墨现在可以**:
1. 使用 Browser 工具进行 Google 搜索 ✅
2. 使用 Jina Reader 读取网页 ✅
3. 使用 x-tweet-fetcher 抓取推文（基础功能）✅

**需要完成安装后才能**:
1. Exa 快速搜索
2. Twitter/X 搜索
3. YouTube/B站字幕提取
4. 小红书、微信公众号搜索

哥哥要墨墨现在完成 Agent Reach 的安装吗？🖤
