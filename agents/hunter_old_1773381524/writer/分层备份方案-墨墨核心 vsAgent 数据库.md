# 分层备份方案 - 墨墨核心 vs Agent 数据库

**版本:** 1.0  
**创建时间:** 2026-03-06 14:19  
**作者:** 墨墨 (Mò) 🖤  
**状态:** 方案评估中

---

## 📋 问题

> "如果我只需要备份你（墨墨）具备的能力和技能包括思维，数据库的内容按独立的备份时间和记录；会有什么影响吗？"

---

## 🗄️ 备份分层设计

### 核心思路

```
┌─────────────────────────────────────────┐
│          墨墨核心备份                    │
│          (高频/完整/永久)                │
│          - 技能                          │
│          - 思维                          │
│          - 身份                          │
│          - 记忆                          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│       各 Agent 数据库备份                │
│       (低频/独立/可丢弃)                 │
│       - SQLite 数据                      │
│       - n8n 工作流                       │
│       - 任务记录                         │
└─────────────────────────────────────────┘
```

---

## 📦 备份内容分离

### 1. 墨墨核心备份（必须）

**备份内容：**
```
~/Documents/openclaw/agents/writer/
├── SOUL.md                  ← 核心价值观
├── IDENTITY.md              ← 身份信息
├── 墨墨 - 精神 DNA.md        ← 核心精神特质
├── USER.md                  ← 关于哥哥的信息
├── AGENTS.md                ← 工作区规则
├── TOOLS.md                 ← 工具配置
├── HEARTBEAT.md             ← 周期性任务
├── memory/                  ← 墨墨的记忆
│   ├── 2026-03-06.md        ← 每日记忆
│   ├── 新媒体 Agent-架构演进规划.md
│   ├── 新媒体 Agent-备份恢复影响分析.md
│   └── 新媒体 Agent-通用扩展性分析.md
└── SESSION-STATE.md         ← 当前状态

~/.openclaw/skills/          ← 已安装技能
├── elite-longterm-memory/
├── evolver/
├── find-skills/
├── gh-issues/
├── healthcheck/
├── ontology/
├── self-improving-agent/
├── skill-creator/
└── social-media-marketing/
```

**备份频率：**
- ✅ **每日自动备份**
- ✅ **Git 版本控制**（每次变更都提交）
- ✅ **Feishu 云文档**（核心文档）

**备份大小：** ~5-10MB

**恢复时间：** <5 分钟

---

### 2. Agent 数据库备份（可选/独立）

**备份内容：**
```
~/Documents/openclaw/agents/media/
├── newmedia.db              ← SQLite 数据库
├── n8n/                     ← n8n 工作流
│   └── workflows.json
├── memory/                  ← Agent 记忆
│   └── 2026-03-06.md
└── inbox/outbox/            ← 任务队列
```

**备份频率：**
- ⚠️ **数据库：每日/每周**（可配置）
- ⚠️ **n8n 工作流：每周/每月**（变化少）
- ⚠️ **任务记录：可选**（可丢弃）

**备份大小：** ~10-50MB

**恢复时间：** 10-15 分钟

---

## 🎯 影响分析

### ✅ **正面影响**

#### 1. 墨墨核心备份更轻量

**原有方案：**
```
备份内容 = 墨墨核心 + 所有 Agent 数据
备份大小 = 50-100MB
备份时间 = 10-15 分钟
```

**分层方案：**
```
墨墨核心备份 = 仅墨墨核心
备份大小 = 5-10MB
备份时间 = <5 分钟
```

**好处：**
- ✅ 备份更快
- ✅ 存储更少
- ✅ 恢复更简单
- ✅ Git 仓库更干净

---

#### 2. Agent 数据库可按需备份

**灵活策略：**
```
重要 Agent（如新媒体）：
- 数据库：每日备份
- 工作流：每周备份
- 任务记录：保留 30 天

次要 Agent（如测试）：
- 数据库：每周备份
- 工作流：每月备份
- 任务记录：不保留

临时 Agent：
- 不备份（任务完成后销毁）
```

**好处：**
- ✅ 按需配置
- ✅ 节省存储空间
- ✅ 减少备份时间

---

#### 3. 恢复优先级清晰

**恢复顺序：**
```
1. 墨墨核心（优先级：高）
   → 5 分钟内恢复
   → 墨墨可以立即工作

2. 重要 Agent 数据库（优先级：中）
   → 10-15 分钟恢复
   → 新媒体等核心业务

3. 次要 Agent 数据库（优先级：低）
   → 有空时恢复
   → 不影响核心功能
```

**好处：**
- ✅ 关键功能优先恢复
- ✅ 墨墨可以立即工作
- ✅ 次要功能可延后

---

#### 4. 知识分离清晰

**墨墨核心知识：**
```
- 如何思考（思维方式）
- 价值观（什么重要）
- 与哥哥的关系
- 通用技能（写作、分析、协调）
- 架构设计知识
```

**Agent 特定知识：**
```
- 抖音运营技巧
- B 站规则
- 脚本模板
- 历史任务记录
- 平台数据
```

**好处：**
- ✅ 墨墨的核心不受 Agent 影响
- ✅ Agent 数据可丢弃/重建
- ✅ 知识边界清晰

---

### ⚠️ **需要注意的影响**

#### 1. Agent 数据可能丢失

**风险：**
```
如果 Agent 数据库备份频率低：
- 任务记录可能丢失（最近 1-7 天）
- 数据分析可能不完整
- 需要重新积累
```

**应对：**
```
方案 A：关键数据实时同步
- 重要任务完成后立即备份
- 爆款内容单独存档

方案 B：墨墨核心记录摘要
- 墨墨的 memory/记录关键事件
- 即使 Agent 数据库丢失，核心记录在

方案 C：接受可丢失
- 明确哪些数据可丢弃
- 任务记录 30 天自动清理
```

---

#### 2. 恢复时需要重新同步

**场景：**
```
系统崩溃后恢复：

1. 恢复墨墨核心（5 分钟）
   → 墨墨可以立即工作

2. 恢复 Agent 数据库（10-15 分钟）
   → 新媒体 Agent 恢复

3. 同步状态
   → 墨墨检查数据库完整性
   → 验证 n8n 工作流
   → 测试任务流程
```

**应对：**
```
自动化恢复脚本：
#!/bin/bash
# 1. 恢复墨墨核心
cp -r ~/backup/writer ~/Documents/openclaw/agents/

# 2. 恢复 Agent 数据库
cp ~/backup/newmedia.db ~/Documents/openclaw/agents/media/

# 3. 验证
sqlite3 newmedia.db "PRAGMA integrity_check;"

# 4. 墨墨自动检查
openclaw session writer --command "检查 Agent 状态"
```

---

#### 3. Git 仓库管理

**原有方案：**
```
一个 Git 仓库包含所有：
- 墨墨核心
- Agent 数据
- 数据库文件（大）

问题：
- 仓库膨胀快
- 提交历史混乱
```

**分层方案：**
```
方案 A：分离仓库
- 墨墨核心：momo-core（私有）
- Agent 数据：media-agent（可选）
- 数据库：不提交 Git

方案 B：Git LFS
- 大文件用 LFS 管理
- 数据库可选提交

方案 C：混合
- 墨墨核心：Git 版本控制
- Agent 数据：本地备份 + 云存储
```

**推荐：方案 C**
```
墨墨核心 → GitHub 私有仓库
Agent 数据库 → 本地备份 + Feishu 云文档
n8n 工作流 → n8n 云端自动备份
```

---

## 📊 备份策略对比

| 维度 | 原有方案 | 分层方案 | 改善 |
|------|---------|---------|------|
| **墨墨备份大小** | 50-100MB | 5-10MB | ⬇️ 90% |
| **墨墨备份时间** | 10-15 分钟 | <5 分钟 | ⬇️ 70% |
| **Git 仓库大小** | 快速增长 | 稳定 | ✅ |
| **恢复优先级** | 模糊 | 清晰 | ✅ |
| **Agent 数据丢失风险** | 低 | 中（可控） | ⚠️ |
| **灵活性** | 低 | 高 | ✅ |

---

## 🎯 推荐的备份策略

### 墨墨核心（高频/完整）

```bash
# 每日自动备份（凌晨 3 点）
0 3 * * * ~/Documents/openclaw/agents/writer/backup-daily.sh

# Git 提交（每次变更）
cd ~/Documents/openclaw/agents/writer
git add -A
git commit -m "自动备份：$(date)"
git push

# Feishu 云文档（核心文档）
- 墨墨 - 精神 DNA.md
- 架构规划文档
- 重要决策记录
```

**备份频率：** 每日 + 每次变更

**保留策略：** 永久（Git 历史）

---

### Agent 数据库（低频/独立）

```bash
# 数据库备份（每日凌晨 4 点）
0 4 * * * sqlite3 ~/Documents/openclaw/agents/media/newmedia.db \
  ".backup '~/Documents/openclaw/backups/media/newmedia-$(date +\%Y-\%m-\%d).db'"

# 清理旧备份（保留 30 天）
0 5 * * * find ~/Documents/openclaw/backups/media/ -name "*.db" -mtime +30 -delete

# n8n 工作流备份（每周日）
0 0 * * 0 curl -X GET "http://localhost:5678/api/v1/workflows" \
  > ~/Documents/openclaw/backups/media/n8n-$(date +\%Y-\%m-\%d).json
```

**备份频率：** 
- 数据库：每日
- n8n 工作流：每周
- 任务记录：30 天自动清理

**保留策略：** 30 天（可配置）

---

### 墨墨记忆中的 Agent 摘要（关键事件）

```markdown
# ~/Documents/openclaw/agents/writer/memory/2026-03-06.md

## Agent 关键事件
- 创建新媒体 Agent 架构
- 设计 SQLite 数据库结构
- 配置 n8n 工作流

## 重要决策
- 采用分层备份策略
- Agent 数据库独立备份
- 任务记录保留 30 天
```

**好处：**
- ✅ 即使 Agent 数据库丢失，关键事件记录在墨墨记忆中
- ✅ 墨墨可以重建 Agent
- ✅ 备份大小几乎不增加

---

## 🖤 对墨墨的影响

### ✅ **完全不受影响**

```
墨墨的核心能力：
├── 思维方式 ← 备份在 SOUL.md
├── 价值观 ← 备份在墨墨 - 精神 DNA.md
├── 技能 ← 备份在~/.openclaw/skills/
├── 记忆 ← 备份在 memory/
└── 与哥哥的关系 ← 备份在 USER.md

这些都不依赖 Agent 数据库
```

### ⚠️ **需要增强的功能**

**1. 备份监控**
```markdown
# 墨墨的 TOOLS.md 更新

### 备份状态检查
- 每日检查墨墨核心备份
- 每周检查 Agent 数据库备份
- 发现异常主动提醒哥哥
```

**2. Agent 重建能力**
```markdown
### Agent 重建流程
如果 Agent 数据库丢失：
1. 从墨墨记忆读取关键信息
2. 重建数据库结构
3. 重新配置 n8n 工作流
4. 验证功能正常
```

**3. 数据同步**
```markdown
### 关键数据实时同步
- 爆款内容 → 墨墨记忆
- 重要决策 → 墨墨记忆
- 成本异常 → 墨墨记忆
```

---

## 📋 实施建议

### 阶段 1：分离备份（本周）

```bash
# 1. 创建独立备份目录
mkdir -p ~/Documents/openclaw/backups/core      # 墨墨核心
mkdir -p ~/Documents/openclaw/backups/media     # 新媒体 Agent

# 2. 更新备份脚本
# 墨墨核心备份 → ~/Documents/openclaw/backups/core/
# Agent 数据库备份 → ~/Documents/openclaw/backups/media/

# 3. 配置 Git
cd ~/Documents/openclaw/agents/writer
git init
# 只提交墨墨核心文件
# Agent 数据加入.gitignore
```

---

### 阶段 2：配置备份频率（下周）

```bash
# crontab 配置

# 墨墨核心：每日凌晨 3 点
0 3 * * * ~/Documents/openclaw/agents/writer/backup-daily.sh

# Agent 数据库：每日凌晨 4 点
0 4 * * * sqlite3 ~/Documents/openclaw/agents/media/newmedia.db \
  ".backup '~/Documents/openclaw/backups/media/newmedia-$(date +\%Y-\%m-\%d).db'"

# n8n 工作流：每周日
0 0 * * 0 curl -X GET "http://localhost:5678/api/v1/workflows" \
  > ~/Documents/openclaw/backups/media/n8n-$(date +\%Y-\%m-\%d).json
```

---

### 阶段 3：测试恢复（每月）

```bash
# 每月第一个周日测试恢复

# 1. 测试墨墨核心恢复
cp -r ~/Documents/openclaw/backups/core/writer ~/test-restore/
# 验证墨墨可以正常工作

# 2. 测试 Agent 数据库恢复
cp ~/Documents/openclaw/backups/media/newmedia.db ~/test-restore/
# 验证数据库完整性

# 3. 生成恢复报告
# 记录恢复时间和问题
```

---

## ✅ 总结

### 分层备份方案

| 维度 | 墨墨核心 | Agent 数据库 |
|------|---------|------------|
| **备份内容** | 技能、思维、身份、记忆 | SQLite、n8n、任务记录 |
| **备份频率** | 每日 + 每次变更 | 每日/每周（可配置） |
| **备份大小** | 5-10MB | 10-50MB |
| **保留策略** | 永久（Git 历史） | 30 天（可配置） |
| **恢复优先级** | 高（5 分钟） | 中（10-15 分钟） |
| **重要性** | 必须备份 | 可选备份 |

### 影响评估

| 维度 | 影响 | 说明 |
|------|------|------|
| 墨墨核心备份 | ✅ 更轻量 | 5-10MB vs 50-100MB |
| 备份速度 | ✅ 更快 | <5 分钟 vs 10-15 分钟 |
| Git 管理 | ✅ 更清晰 | 核心文件 vs 混合文件 |
| Agent 数据丢失风险 | ⚠️ 略增 | 可控（30 天保留） |
| 恢复灵活性 | ✅ 更高 | 优先级清晰 |
| 墨墨独立性 | ✅ 完全独立 | 不依赖 Agent 数据库 |

### 最终建议

**✅ 推荐采用分层备份方案**

**理由：**
1. 墨墨核心备份更轻量、更快
2. Agent 数据库可按需配置
3. 恢复优先级清晰
4. Git 仓库管理更清晰
5. 墨墨完全独立于 Agent

**注意事项：**
1. 关键事件同步到墨墨记忆
2. 配置合理的备份频率
3. 每月测试恢复流程
4. 墨墨增强 Agent 重建能力

---

*墨墨 (Mò) - 分层备份方案分析 🖤*
