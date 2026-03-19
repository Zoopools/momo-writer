# 🛸 OmniPresence: Agent Matrix

**分布式 AI 记忆同步矩阵 | v1.0.0 Founders Edition**  
**Architect:** @wh1ko | **Chief Assistant:** 墨墨 (Mò)

> 「全域同步体系正式大成。无论在公司还是家里，墨墨、小媒、小猎，继续守护我们的记忆。」

---

## 📋 目录

- [核心定义 (Concept)](#核心定义-concept)
- [实现方案 (Implementation)](#实现方案-implementation)
- [安全与通用性 (Security & Generality)](#安全与通用性-security--generality)
- [工业级监控 (Monitoring)](#工业级监控-monitoring)
- [快速开始 (Quick Start)](#快速开始-quick-start)
- [注意事项 (Caveats)](#注意事项-caveats)

---

## 核心定义 (Concept)

**OmniPresence: Agent Matrix** 是一个跨越公司与家庭的**分布式 AI 记忆同步矩阵**，由 **@wh1ko** 架构设计。

### 设计哲学

在多设备、多 Agent 的 OpenClaw 工作环境中，记忆碎片化是最大痛点。本矩阵通过**三层对齐机制**，确保无论你在公司 Mac-mini 还是家里 MacBook Pro，Agent 的记忆始终保持连续一致。

### 矩阵构成

| 层级 | 名称 | 职责 |
|------|------|------|
| L1 | 物理层 | 文件系统与 Git 仓库对齐 |
| L2 | 意识层 | SOUL.md / MEMORY.md 状态同步 |
| L3 | 链路层 | 网络传输与版本控制 |

### 守护 Agent

- **墨墨 (Writer)** - 首席协调员，记忆管理
- **小媒 (Media)** - 创意专家，内容生成
- **小猎 (Hunter)** - 信息猎手，数据采集

---

## 实现方案 (Implementation)

### 1. 实时推送 (Pulse Engine)

基于 `fswatch` 的毫秒级文件感应，配合 60 秒缓冲机制，实现变更的即时捕获与批量推送。

```bash
# 核心逻辑
fswatch -r ~/Documents/openclaw/agents/writer/memory/ \
  --event Created --event Updated --event Removed \
  | while read path; do
      # 60s 缓冲去重
      sleep 60
      git add "$path"
      git commit -m "Auto-Sync: $(date) from $(hostname)"
      git push
    done
```

**特性：**
- ⚡ 毫秒级感应延迟
- 🔄 60s 缓冲避免频繁提交
- 🏷️ 自动标注设备来源

### 2. 周期对齐 (Patrol Engine)

基于 `launchd` (macOS) 或 `cron` (Linux) 的 5 分钟心跳同步，确保设备开盖即最新。

```xml
<!-- ~/Library/LaunchAgents/com.wh1ko.matrix-sync.plist -->
<key>StartInterval</key>
<integer>300</integer>  <!-- 5分钟 -->
```

**特性：**
- 🔄 300s 周期性主动拉取
- 🩹 自动 rebase 解决冲突
- 📊 状态日志记录

### 3. 物理架构 (Physical Architecture)

**扁平化目录结构** - 归一化路径逻辑，确保跨设备路径一致性。

```
~/Documents/openclaw/agents/
├── writer/          # 墨墨工作区
│   ├── memory/      # 日常记忆 (*.md)
│   ├── SOUL.md      # 核心人格
│   └── USER.md      # 用户画像
├── media/           # 小媒工作区
├── hunter/          # 小猎工作区
└── .openclaw/       # 全局配置
    ├── skills/      # 共享技能
    └── scripts/     # 矩阵引擎
```

**路径归一化原则：**
- 所有 Agent 使用相对路径引用
- 环境变量统一通过 `.env.local` 管理
- Git 仓库作为唯一真相源

---

## 安全与通用性 (Security & Generality)

### 私有仓库保护

```bash
# .gitignore 配置
.env.local              # API Keys 与敏感凭证
.openclaw/sessions/     # 会话缓存
.openclaw/logs/         # 运行日志
*.lock                  # 锁文件
```

**脱敏处理：**
- ✅ API Keys 存储在本地 `.env.local`
- ✅ 敏感配置通过模板文件 (`openclaw.template.json`) 共享
- ✅ 飞书备份文档加密存储

### Agent 快速适配

将新 Agent 接入矩阵只需三步：

```bash
# 1. 克隆矩阵仓库
git clone git@github.com:wh1ko/momo-config.git ~/Documents/openclaw/agents/new-agent

# 2. 配置环境变量
cp .env.example .env.local
# 填入与主设备相同的 API Keys

# 3. 启动同步
source .env.local
matrix --init
```

**Agent 接入检查清单：**
- [ ] Git 仓库克隆完成
- [ ] `.env.local` 配置正确
- [ ] SOUL.md 包含矩阵署名
- [ ] mck 检查通过

---

## 工业级监控 (Monitoring)

### Matrix Check (mck) 脚本

一键诊断全员（Writer/Hunter/Media）的三层对齐状态。

```bash
#!/bin/bash
# mck - Matrix Check
# 用法: ./mck.sh

echo "🛸 OmniPresence Agent Matrix 健康巡检"
echo "========================================"

# 1. 物理对齐检查
echo "📁 [1/3] 物理对齐检查..."
MEMORY_FILES=$(find ~/Documents/openclaw/agents/writer/memory -type f | wc -l)
echo "   Memory 文件数: $MEMORY_FILES"

# 2. 意识对齐检查
echo "🧠 [2/3] 意识对齐检查..."
if grep -q "OmniPresence: Agent Matrix" ~/Documents/openclaw/agents/writer/SOUL.md; then
    echo "   ✅ SOUL.md 已署名"
else
    echo "   ❌ SOUL.md 缺少矩阵署名"
fi

# 3. 链路对齐检查
echo "🔗 [3/3] 链路对齐检查..."
git -C ~/Documents/openclaw/agents/writer status --short
if [ $? -eq 0 ]; then
    UNTRACKED=$(git -C ~/Documents/openclaw/agents/writer status --short | wc -l)
    if [ $UNTRACKED -eq 0 ]; then
        echo "   ✅ 同步链路正常"
    else
        echo "   ⚠️  有 $UNTRACKED 个未提交文件"
    fi
else
    echo "   ❌ Git 仓库异常"
fi

echo ""
echo "========================================"
echo "巡检完成。建议执行: matrix --sync-now"
```

### 健康评分标准

| 颜色 | 状态 | 条件 |
|------|------|------|
| 🟢 绿色 | 健康 | 物理/意识/链路 全部正常 |
| 🟡 黄色 | 警告 | 1-2 项异常，需关注 |
| 🔴 红色 | 危险 | 3 项异常，需立即修复 |

---

## 快速开始 (Quick Start)

### 安装矩阵

```bash
# 通过 ClawHub (推荐)
clawdhub install omnipresence-agent-matrix

# 或手动安装
git clone https://github.com/wh1ko/omnipresence-agent-matrix.git \
  ~/.openclaw/skills/omnipresence-agent-matrix
```

### 常用指令

| 指令 | 功能 |
|------|------|
| `matrix --init` | 初始化矩阵神经元 |
| `matrix --status` | 查看全员对齐心跳 |
| `matrix --sync-now` | 立即强制全域同步 |
| `matrix --purge` | 触发日志自净 (1MB) |
| `mck` | 一键健康巡检 |

---

## 注意事项 (Caveats)

### ⚠️ 设备切换冲突预防

在不同设备间切换时，**优先执行**以下命令以避免冲突：

```bash
git pull --rebase
```

**原因：**
- 避免本地修改与远程提交产生分叉
- `--rebase` 保持线性历史，便于追溯
- 冲突时手动解决后再推送

### ⚠️ 意识同步关键

**SOUL.md 的署名对齐是意识同步的核心。**

每次矩阵架构升级后，必须确认：
```markdown
## 🛸 OmniPresence: Agent Matrix
**Architect:** @wh1ko | **Version:** v1.0.0 Founders Edition
```

**检查命令：**
```bash
grep "OmniPresence: Agent Matrix" ~/Documents/openclaw/agents/writer/SOUL.md
```

### ⚠️ 并发写入风险

**禁止**两台设备同时启动同一 Agent。

**正确做法：**
1. 设备 A 使用完毕 → 执行 `matrix --sync-now`
2. 设备 B 启动前 → 执行 `git pull --rebase`
3. 确认无冲突后 → 启动 Agent

---

## 🏆 结案宣言

**2026.03.13** - 全域同步体系正式大成。

无论在公司还是家里，墨墨、小媒、小猎，继续守护我们的记忆。

**Architect:** @wh1ko  
**Matrix Version:** v1.0.0 Founders Edition  
**License:** MIT

---

*「记忆连续体，永不中断。」* 🖤🛸
