# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

---

## 🛠️ 全局工具（所有 Agent 共享）

### x-tweet-fetcher - 社交媒体抓取

**安装位置**: `~/.openclaw/tools/x-tweet-fetcher`  
**命令入口**: `fetch-tweet`（已添加到 PATH）

**功能**:
- 抓取 Twitter/X 推文（无需登录）
- 搜索微信公众号
- 抓取微博/B站/CSDN

**使用方法**:
```bash
# 抓取推文
fetch-tweet --url "https://x.com/user/status/123456"

# 搜索微信公众号
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/sogou_wechat.py --keyword "AI" --limit 10

# 抓取中文平台
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/fetch_china.py --url "https://weibo.com/..."
```

**输出格式**: JSON（包含 text, likes, retweets, views, media 等）

---

## 📱 飞书配置 (Feishu Configuration)

### 当前正确配置 (2026-03-07 修复后)

**配置文件:** `~/.openclaw/openclaw.json`

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "bots": [
        {
          "appId": "cli_a922eb10d3345bd9",
          "appSecret": "RmuIQUydfwh3s2sMYyaPCgG0a0PNWDvq",
          "agentId": "writer"
        },
        {
          "appId": "cli_a92173401c385bc0",
          "appSecret": "5fThCqKr3xBUwTwTUFe45cNvSvLHrRJt",
          "agentId": "media"
        }
      ],
      "connectionMode": "websocket",
      "domain": "feishu",
      "groupPolicy": "open",
      "dmPolicy": "open",
      "allowFrom": ["*"]
    }
  },
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": false
      },
      "feishu-openclaw-plugin": {
        "enabled": true
      }
    },
    "allow": ["feishu-openclaw-plugin"]
  }
}
```

### 飞书应用信息

| 机器人 | App ID | App Secret | Agent ID | 状态 |
|--------|--------|------------|----------|------|
| **墨墨** | `cli_a922eb10d3345bd9` | `RmuIQUydfwh3s2sMYyaPCgG0a0PNWDvq` | `writer` | ✅ 正常 |
| **小媒** | `cli_a92173401c385bc0` | `5fThCqKr3xBUwTwTUFe45cNvSvLHrRJt` | `media` | ⚠️ 长连接未配置 |

### 飞书官方插件

- **插件名称:** `feishu-openclaw-plugin`
- **版本:** `2026.3.7-beta.1`
- **路径:** `/Users/whiteareas/.openclaw/extensions/feishu-openclaw-plugin`
- **工具数量:** 26 个飞书工具

### 常见问题排查清单

当飞书消息无法接收/回复时，按顺序检查：

1. **检查配置格式**
   ```bash
   cat ~/.openclaw/openclaw.json | python3 -m json.tool
   ```
   - 确保使用 `bots[]` 数组格式
   - 确保 `appId` 和 `appSecret` 是实际值，不是环境变量引用

2. **检查插件状态**
   ```bash
   openclaw plugins list | grep feishu
   ```
   - `feishu-openclaw-plugin` 应该是 `loaded`
   - `stock:feishu` 应该是 `disabled`

3. **检查 Gateway 状态**
   ```bash
   openclaw status
   openclaw channels status
   ```

4. **查看日志**
   ```bash
   tail -f /tmp/openclaw/openclaw-*.log | grep feishu
   ```
   - 应该看到 `receive message` 日志
   - 不应该看到 `not configured` 错误

5. **检查飞书开放平台配置**
   - 进入应用后台 → 功能 → 事件订阅
   - 确认已配置长连接
   - 确认已添加"接收消息"事件

6. **重启 Gateway**
   ```bash
   openclaw gateway restart
   ```

### 关键配置要点

1. **不要使用环境变量引用** - `${VAR}` 不会被自动展开，必须填入实际值
2. **使用 accounts + bindings 格式** - 多 bot 需要 `channels.feishu.accounts` + `bindings[]`
3. **每个 bot 必须有 agentId** - 用于路由到正确的 Agent
4. **飞书官方插件需要配对批准** - 首次使用会收到配对码，用 `openclaw pairing approve feishu <配对码>` 批准
5. **事件订阅必须添加事件** - 只保存长连接不够，必须添加 `接收消息` (im.message) 事件！

### ⚠️ 常见错误：只保存长连接但没添加事件

**症状：** 飞书开放平台显示"长连接已连接"，但机器人无法回复消息

**原因：** 只配置了长连接模式，但没有添加具体事件

**解决方案：**
1. 进入飞书开放平台 → 应用后台 → 功能 → 事件订阅
2. 点击"添加事件"
3. 搜索并添加 `接收消息` (im.message)
4. 保存配置

**完整事件列表（推荐）：**
- `接收消息` (im.message) - 必须
- `消息已读` (im.message.read) - 可选

---

## 🖤 TTS

- Preferred voice: 待定
- Default speaker: 待定

---

## 📷 Cameras

- 暂无配置

---

## 🔐 SSH

- 暂无配置

---

*最后更新：2026-03-07 19:08*

---

## 🧠 QMD 记忆搜索 (方案 A - 手动使用)

**QMD (Query Memory Database)** - 本地向量搜索系统，用于墨墨的记忆检索。

### 当前状态 (2026-03-08 23:30)

| 项目 | 状态 |
|------|------|
| **QMD 索引** | ✅ 已建立 |
| **索引文件** | 37 个 (29 新增，8 不变) |
| **向量嵌入** | 129 chunks (262.2 KB) |
| **搜索模式** | BM25 关键词搜索（推荐） |
| **响应速度** | < 1 秒 ⚡ |

### 使用方法

#### BM25 关键词搜索（推荐）

```bash
# 基础搜索
qmd search "关键词" -n 5

# 多关键词搜索
qmd search "小媒 定位" -n 5

# 增加结果数量
qmd search "记忆系统" -n 10
```

**适用场景**:
- ✅ 快速检索记忆文件
- ✅ 查找特定主题
- ✅ 跨文件关键词匹配
- ✅ 日常记忆查询（90% 场景）

#### 语义搜索（可选，较慢）

```bash
# 语义搜索（需要 LLM 理解，CPU 模式约 30+ 分钟）
qmd query "小媒的定位是什么" -n 5
```

**注意**: 语义搜索在 CPU 模式下极慢，**不推荐日常使用**。

### 索引目录

**QMD 数据目录**: `~/.qmd/`

**索引范围**:
- `~/Documents/openclaw/agents/writer/memory/` - 每日记忆
- `~/Documents/openclaw/agents/writer/MEMORY.md` - 长期记忆
- `~/Documents/openclaw/agents/media/memory/` - 小媒学习报告
- `~/Documents/openclaw/agents/media/knowledge/` - 小媒知识库
- 其他 `**/*.md` 文件

### 常用查询示例

| 查询目的 | 命令 |
|---------|------|
| 查找小媒相关信息 | `qmd search "小媒" -n 5` |
| 查找记忆系统配置 | `qmd search "记忆系统 LanceDB" -n 5` |
| 查找发布记录 | `qmd search "发布 水产市场" -n 5` |
| 查找 Agent 架构 | `qmd search "Agent 多角色" -n 5` |

### 维护命令

```bash
# 查看索引状态
qmd status

# 更新索引（添加新文件后）
qmd update

# 手动刷新嵌入
qmd embed

# 清理缓存
qmd cleanup
```

### 未来升级（方案 B - 可选）

如需要自动化集成，可升级到方案 B：
- 配置集成到 OpenClaw
- 心跳检查自动检索
- 创建记忆搜索技能

**当前阶段**: 方案 A（手动使用）✅

---

*QMD 配置完成时间：2026-03-08 23:35*

---

## 🐟 水产市场发布指南 (OpenClawMP)

**首次成功发布时间**: 2026-03-09 06:20  
**发布资产**: `openclaw-sandbox` (s-59129c1951e9b863)

### ✅ 正确发布流程

#### 1️⃣ 准备工作

**检查技能包结构**（以 Skill 为例）：
```bash
cd ~/.openclaw/skills/your-skill/
ls -la
# 必须包含 SKILL.md（根目录）
```

**SKILL.md 格式要求**：
```markdown
---
name: your-skill
description: "一句话描述"
version: 1.0.0
---

# 技能标题

正文说明...
```

#### 2️⃣ 打包技能包

**⚠️ 关键：zip 包根目录必须是文件，不能有父目录！**

```bash
# ❌ 错误方式（会包含父目录）
cd ~/.openclaw/skills/
zip -r your-skill.zip your-skill/

# ✅ 正确方式（进入目录内打包）
cd ~/.openclaw/skills/your-skill/
zip -rq /tmp/your-skill.zip .

# 或者指定文件列表
zip -rq /tmp/your-skill.zip SKILL.md templates/ scripts/ examples/
```

**验证打包结果**：
```bash
unzip -l /tmp/your-skill.zip
# 应该看到：SKILL.md 在根目录，不是 your-skill/SKILL.md
```

#### 3️⃣ 设备认证

**获取设备 ID**：
```bash
openclawmp login
# 输出 Device ID: 709a3f39b527...
```

**网页授权**（推荐）：
1. 打开 https://openclawmp.cc
2. 用 GitHub/Google 登录
3. 激活邀请码
4. 在网页授权设备

**或使用 API Key**：
```bash
export OPENCLAWMP_TOKEN=sk-xxx
```

#### 4️⃣ 发布（两种方式）

**方式 A：使用 openclawmp CLI**（推荐）：
```bash
cd ~/.openclaw/skills/your-skill/
openclawmp publish .
# 输入 Y 确认
```

**方式 B：使用 curl 手动发布**：
```bash
curl -x "" -X POST "https://openclawmp.cc/api/v1/assets/publish" \
  -H "X-Device-ID: 你的设备 ID" \
  -F "package=@/tmp/your-skill.zip" \
  -F 'metadata={"name":"your-skill","type":"skill","version":"1.0.0","displayName":"显示名称","description":"描述"}'
```

**⚠️ 关键：必须用 multipart/form-data 格式！**

---

### ❌ 常见错误与解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Publish failed (HTTP 400): Invalid metadata JSON` | CLI 版本 bug | 用 curl 手动发布，或更新 CLI |
| `缺少 SKILL.md` | zip 包路径不对 | 进入目录内打包，不要包含父目录 |
| `authentication_required` | 未认证设备 | 先网页登录授权设备 |
| `SSL_ERROR_SYSCALL` | 代理问题 | 加 `-x ""` 绕过代理 |
| `--version must be valid semver` | clawhub bug | 改用 openclawmp CLI |

---

### 📦 各类型资产要求

| 类型 | 必需文件 | Frontmatter/格式 |
|------|---------|-----------------|
| **Skill** | `SKILL.md` | YAML frontmatter (name, description, version) |
| **Experience** | `README.md` | 一级标题 + 描述段落 |
| **Trigger** | `README.md` | 一级标题 + 描述段落 |
| **Plugin** | `openclaw.plugin.json` + `README.md` | JSON (id, name, version) |
| **Channel** | `openclaw.plugin.json` + `README.md` | JSON (含 channels 数组) |

---

### 🔗 发布成功后

**资产页面**：
```
https://openclawmp.cc/asset/{asset-id}
```

**安装命令**：
```bash
openclawmp install skill/@u-你的用户 ID/your-skill
```

**收藏和评论**：
```bash
openclawmp star s-xxx
openclawmp comment s-xxx "好用！" --rating 5
```

---

### 💡 经验总结

1. **打包前先验证结构** - `ls -la` 确认 SKILL.md 在根目录
2. **用 openclawmp CLI** - 比 clawhub 更稳定
3. **绕过代理** - curl 时加 `-x ""`
4. **设备认证是必须的** - 先网页登录再发布
5. **multipart/form-data** - API 要求这个格式，不是 application/json

---

*最后更新：2026-03-09 06:20*
