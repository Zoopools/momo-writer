# 🖤 墨墨的同步配置 - 快速设置指南

## ✅ 已完成的工作

我已经帮哥哥准备好了所有文件：

- ✅ `.gitignore` - 排除敏感信息
- ✅ `.env.example` - 环境变量模板
- ✅ `openclaw.template.json` - 配置模板（不含密钥）
- ✅ `README.md` - 完整同步文档
- ✅ `sync-push.sh` - 推送脚本
- ✅ `sync-pull.sh` - 拉取脚本
- ✅ Git 仓库已初始化
- ✅ 首次提交已完成

---

## 🚀 下一步：推送到 GitHub（需要哥哥手动操作）

### 方法 1：使用 GitHub Desktop（最简单）

1. **下载 GitHub Desktop**: https://desktop.github.com/
2. **打开 GitHub Desktop**
3. **添加本地仓库**: File → Add Local Repository → 选择 `/Users/wh1ko/Documents/openclaw/agents/writer`
4. **发布到 GitHub**: 点击右上角 "Publish repository"
5. **设置为私有**: ✅ 勾选 "Keep this code private"
6. **完成!**

### 方法 2：使用命令行（需要配置认证）

```bash
cd /Users/wh1ko/Documents/openclaw/agents/writer

# 设置 GitHub 认证（二选一）

# 选项 A: 使用 Personal Access Token
git remote set-url origin https://你的 GitHub 用户名:你的 PAT@github.com/Zoopools/momo-config.git

# 选项 B: 使用 SSH（推荐）
# 1. 生成 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 添加公钥到 GitHub
# 访问 https://github.com/settings/keys
# 复制 ~/.ssh/id_ed25519.pub 的内容

# 3. 切换远程仓库为 SSH
git remote set-url origin git@github.com:Zoopools/momo-config.git

# 推送
git push -u origin main
```

---

## 📱 在另一台电脑上设置

### 步骤 1：克隆仓库

```bash
git clone git@github.com:Zoopools/momo-config.git /path/to/agents/writer
cd /path/to/agents/writer
```

### 步骤 2：复制并配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env.local

# 编辑 .env.local，填入你的 API Keys
# 可以从飞书备份文档中复制：
# - openclaw.json 备份文档 (Doc ID: ZL4ydB3R0o6yTHxGxOvc14nGnnb)
```

### 步骤 3：安装 OpenClaw

```bash
npm install -g openclaw
```

### 步骤 4：启动

```bash
# 加载环境变量
source .env.local

# 启动 OpenClaw
openclaw start
```

---

## 🔄 日常同步

### 在这台电脑（修改后）

```bash
cd /Users/wh1ko/Documents/openclaw/agents/writer
./sync-push.sh
```

### 在另一台电脑（接收更新）

```bash
cd /path/to/agents/writer
./sync-pull.sh
```

---

## 🔐 敏感信息处理

**已排除在 Git 之外的文件：**
- `.env.local` - API Keys
- `~/.openclaw/openclaw.json` - 完整配置（含密钥）
- `*.backup.*` - 备份文件（含敏感信息）

**安全存储方式：**
- ✅ 飞书备份文档（已创建）
- ✅ 1Password / Bitwarden
- ✅ 本地 `.env.local`（不提交）

---

## ⚠️ 重要提醒

1. **仓库已经是私有的** - 只有你能访问
2. **敏感信息不会同步** - 需要手动配置 `.env.local`
3. **不要同时运行** - 两台电脑不要同时启动墨墨
4. **推送前先拉取** - 避免冲突

---

## 📞 需要帮助？

如果遇到问题：
1. 检查 GitHub 认证是否配置
2. 确保仓库是私有的
3. 验证 `.env.local` 中的 API Keys 是否正确

哥哥可以随时问我！🖤
