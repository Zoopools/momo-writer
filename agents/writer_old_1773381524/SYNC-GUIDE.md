# 双机同步指南

**创建时间**: 2026-03-12  
**用途**: 公司 ↔ 家里 环境同步

---

## 📋 Git 同步部分（自动）

### writer Agent 配置
```bash
# 公司 → 家里
cd ~/Documents/openclaw/agents/writer
git add .
git commit -m "Update: $(date '+%Y-%m-%d %H:%M')"
git push

# 家里 → 公司
cd ~/Documents/openclaw/agents/writer
git pull
```

**已跟踪内容**:
- ✅ MEMORY.md
- ✅ SOUL.md
- ✅ AGENTS.md
- ✅ knowledge/
- ✅ memory/
- ✅ .agents/skills/ (软链接)

---

## ⚠️ 需手动同步部分

### 1. 系统级配置 (~/.openclaw/)

**需要同步的目录**:
```
~/.openclaw/
├── genes/              # 进化引擎 Gene 文件
├── scripts/            # 脚本（evolve.sh 等）
├── skills/             # 技能软链接
├── bin/                # 命令（evolve, qmd 等）
└── openclaw.json       # 核心配置（注意：包含 API Key）
```

**同步方法**:
```bash
# 方法 1: 压缩后传输
# 公司电脑
cd ~
tar czf openclaw-config.tar.gz .openclaw/genes .openclaw/scripts .openclaw/skills .openclaw/bin

# 方法 2: 使用 iCloud/坚果云
# 将 ~/.openclaw/ 同步到云盘
```

### 2. Agent 工作目录

**公司特有**（家里需要初始化）:
```
~/Documents/openclaw/agents/
├── media/              # 小媒
└── hunter/             # 小猎
```

**初始化方法**:
```bash
# 家里执行
mkdir -p ~/Documents/openclaw/agents/media/{memory,knowledge,scripts}
mkdir -p ~/Documents/openclaw/agents/hunter/{memory,knowledge,scripts}

# 复制基础文件
cp ~/Documents/openclaw/agents/writer/.agents/skills/find-skills \
   ~/Documents/openclaw/agents/media/.agents/skills/
cp ~/Documents/openclaw/agents/writer/.agents/skills/find-skills \
   ~/Documents/openclaw/agents/hunter/.agents/skills/
```

---

## 🔄 推荐同步流程

### 日常同步（Git）

**公司工作完成后**:
```bash
cd ~/Documents/openclaw/agents/writer
git add .
git commit -m "Update: $(date '+%Y-%m-%d %H:%M')"
git push
```

**家里开始工作前**:
```bash
cd ~/Documents/openclaw/agents/writer
git pull
```

### 系统配置同步（按需）

**当系统配置变更时**:
1. 记录变更: `ls -la ~/.openclaw/`
2. 压缩传输或使用云盘
3. 家里解压覆盖

---

## ⚠️ 注意事项

### 1. API Key 安全
- `~/.openclaw/openclaw.json` 包含 API Key
- 不要上传到公共仓库
- 如需同步，使用加密传输

### 2. 飞书 Bot
- 同一时间只能连接一个 Gateway
- 切换设备时需要停止/启动 Gateway

### 3. 路径差异
- 公司: `/Users/whiteareas/`
- 家里: `/Users/wh1ko/` (可能不同)
- 使用 `$HOME` 环境变量避免硬编码

---

## 🎯 今天需要同步的内容

### Git 提交
- ✅ TOOLS.md 修改
- ✅ find-skills 技能
- ✅ 知识库文件

### 手动同步（可选）
- ⚠️ `~/.openclaw/genes/` - 进化引擎
- ⚠️ `~/.openclaw/scripts/` - 脚本
- ⚠️ `~/.openclaw/bin/` - 命令
- ⚠️ `~/.openclaw/skills/` - 技能链接
- ⚠️ `~/Documents/openclaw/agents/media/` - 小媒
- ⚠️ `~/Documents/openclaw/agents/hunter/` - 小猎

---

*最后更新: 2026-03-12*
