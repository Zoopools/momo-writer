# 🖤 墨墨的同步配置

这是墨墨（Mò）的 OpenClaw 配置同步仓库。

## 📦 仓库内容

- ✅ **工作区配置** - `SESSION-STATE.md`, `SOUL.md`, `USER.md` 等
- ✅ **日常记忆** - `memory/` 目录
- ✅ **配置模板** - `openclaw.template.json`（不含敏感信息）
- ✅ **技能列表** - 已安装的技能清单

## 🔐 敏感信息处理

**本仓库不包含：**
- ❌ API Keys
- ❌ App Secrets
- ❌ 个人凭证

**敏感信息存储在：**
- 📁 `.env.local`（本地文件，已在 .gitignore 中排除）
- 🔒 飞书备份文档（加密）

---

## 🚀 第一次设置（电脑 A - 主机）

```bash
# 1. 克隆仓库（如果还没克隆）
git clone git@github.com:wh1ko/momo-config.git /Users/wh1ko/Documents/openclaw/agents/writer

# 2. 复制环境变量模板
cp .env.example .env.local

# 3. 编辑 .env.local，填入你的 API Keys
# OPENCLAW_DASHSCOPE_API_KEY="sk-xxx"
# OPENCLAW_FEISHU_APP_SECRET="xxx"

# 4. 加载环境变量
source .env.local

# 5. 复制配置模板到 ~/.openclaw/
cp openclaw.template.json ~/.openclaw/openclaw.json

# 6. 启动 OpenClaw
openclaw start
```

---

## 🔄 同步到另一台电脑（电脑 B）

### 步骤 1：克隆仓库

```bash
# 在新电脑上克隆仓库
git clone git@github.com:wh1ko/momo-config.git /path/to/agents/writer
cd /path/to/agents/writer
```

### 步骤 2：安装 OpenClaw

```bash
# 安装 OpenClaw（如果还没安装）
npm install -g openclaw
```

### 步骤 3：配置环境变量

```bash
# 复制环境变量文件
cp .env.example .env.local

# 编辑 .env.local，填入与电脑 A 相同的 API Keys
# 可以从飞书备份文档中复制
```

### 步骤 4：链接配置

```bash
# 方法 1：直接复制配置
cp openclaw.template.json ~/.openclaw/openclaw.json

# 方法 2：符号链接（推荐，保持同步）
ln -s /path/to/agents/writer/openclaw.template.json ~/.openclaw/openclaw.json
```

### 步骤 5：加载环境变量

```bash
# 临时加载（当前终端）
source .env.local

# 永久加载（添加到 ~/.zshrc）
echo 'source /path/to/agents/writer/.env.local' >> ~/.zshrc
source ~/.zshrc
```

### 步骤 6：验证

```bash
# 检查环境变量
echo $OPENCLAW_DASHSCOPE_API_KEY
echo $OPENCLAW_FEISHU_APP_SECRET

# 启动 OpenClaw
openclaw start
```

---

## 📝 日常同步流程

### 在电脑 A（修改后）

```bash
cd /Users/wh1ko/Documents/openclaw/agents/writer

# 查看变更
git status

# 添加变更
git add .

# 提交
git commit -m "描述你的变更"

# 推送
git push
```

### 在电脑 B（接收更新）

```bash
cd /path/to/agents/writer

# 拉取最新配置
git pull

# 加载环境变量（如果没在 ~/.zshrc 中）
source .env.local
```

---

## ⚠️ 注意事项

1. **不要同时运行** - 两台电脑不要同时启动墨墨，避免记忆冲突
2. **推送前 pull** - 每次推送前先 `git pull`，避免冲突
3. **敏感信息** - 永远不要提交 `.env.local` 或含 API Key 的文件
4. **冲突解决** - 如果 `SESSION-STATE.md` 冲突，保留最新的，合并待办事项

---

## 🛠️ 故障排除

### 问题：环境变量未加载

```bash
# 检查是否设置
printenv | grep OPENCLAW

# 手动加载
source .env.local
```

### 问题：Git 推送失败

```bash
# 先拉取最新代码
git pull --rebase

# 解决冲突后
git add .
git commit -m "解决冲突"
git push
```

### 问题：技能不同步

```bash
# 在电脑 A 导出技能列表
ls ~/.openclaw/skills/ > skills-list.txt
git add skills-list.txt
git commit -m "更新技能列表"
git push

# 在电脑 B 安装缺失的技能
# （根据 skills-list.txt 手动安装）
```

---

## 📚 已安装技能列表

- `skill-creator` - 创造新技能
- `find-skills` - 发现和安装技能
- `social-media-marketing` - 自媒体营销
- `gh-issues` - GitHub issues 管理
- `healthcheck` - 系统安全审计
- `elite-longterm-memory` - 长期记忆
- `self-improving-agent` - 自我进化

---

## 🔒 安全提示

- ✅ 本仓库是**私有的**，只有你能访问
- ✅ 敏感信息已排除在 Git 之外
- ✅ API Keys 存储在本地 `.env.local`
- ✅ 建议开启 GitHub 双重验证

---

**仓库创建时间**: 2026-03-05  
**墨墨版本**: 2026.3.2  
**配置状态**: ✅ 3 层记忆系统已激活
