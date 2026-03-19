# 新媒体 Agent 方案 - 备份与恢复影响分析

**版本:** 1.0  
**创建时间:** 2026-03-06 14:07  
**作者:** 墨墨 (Mò) 🖤  
**状态:** 方案评估中

---

## 📋 问题

> "这一套新的方案（SQLite + n8n + 临时子代理）对于备份和恢复，以及墨墨本身有什么影响吗？"

---

## 🗄️ 新架构组件

### 原有组件（不变）
```
~/Documents/openclaw/agents/
├── writer/          ← 墨墨（受保护）
│   ├── SOUL.md
│   ├── memory/
│   └── ...
└── media/           ← 新媒体 Agent
    ├── SOUL.md
    ├── memory/
    └── ...
```

### 新增组件
```
1. SQLite 数据库
   ~/Documents/openclaw/agents/media/newmedia.db

2. n8n 工作流
   n8n 云端/本地实例
   - 数据监控工作流
   - 内容发布工作流

3. 临时子代理池
   动态创建，任务完成后销毁
```

---

## 📦 备份影响分析

### 1. 备份范围变化

**原有备份（简单）：**
```bash
# 只需备份 MD 文件
cp -r ~/Documents/openclaw/agents/media/ ~/backup/
```

**新增备份（复杂）：**
```bash
# 需要备份：
✅ MD 文件（SOUL.md, memory/等）
✅ SQLite 数据库（newmedia.db）
✅ n8n 工作流（JSON 导出）
✅ 数据库备份策略（每日/每周）
```

### 2. 备份策略

#### SQLite 数据库备份

**方案 A：每日备份（推荐）**
```bash
# 每天凌晨 3 点备份数据库
sqlite3 newmedia.db ".backup 'newmedia-backup-$(date +%Y-%m-%d).db'"

# 保留最近 30 天备份
find ~/backup/ -name "newmedia-backup-*.db" -mtime +30 -delete
```

**方案 B：WAL 模式 + 定期导出**
```bash
# 启用 WAL 模式（Write-Ahead Logging）
sqlite3 newmedia.db "PRAGMA journal_mode=WAL;"

# 每周导出一次
sqlite3 newmedia.db ".dump" | gzip > newmedia-dump-$(date +%Y-%m-%d).sql.gz
```

**方案 C：Git LFS（适合小数据库）**
```bash
# 数据库加入 Git 管理（使用 LFS）
git lfs track "*.db"
git add newmedia.db
git commit -m "备份数据库"
```

#### n8n 工作流备份

**方案 A：n8n 内置备份**
- n8n 云端自动备份
- 工作流版本历史

**方案 B：手动导出**
```bash
# 通过 n8n API 导出工作流
curl -X GET "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-Key: YOUR_KEY" \
  > n8n-workflows-backup-$(date +%Y-%m-%d).json
```

**方案 C：Git 管理**
```bash
# 工作流 JSON 加入 Git
cp n8n-workflows.json ~/Documents/openclaw/agents/media/n8n/
git add n8n/
git commit -m "更新 n8n 工作流"
```

### 3. 备份脚本更新

```bash
#!/bin/bash
# 墨墨的完整备份脚本 - 增强版

BACKUP_DIR=~/Documents/openclaw/backups/墨墨-momo-$(date +%Y-%m-%d_%H%M%S)

# 1. 备份工作区（原有）
cp -r ~/Documents/openclaw/agents/writer/ $BACKUP_DIR/

# 2. 备份新媒体 Agent（原有）
cp -r ~/Documents/openclaw/agents/media/ $BACKUP_DIR/

# 3. 备份 SQLite 数据库（新增）
sqlite3 ~/Documents/openclaw/agents/media/newmedia.db \
  ".backup '$BACKUP_DIR/newmedia.db'"

# 4. 备份 n8n 工作流（新增）
curl -X GET "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-Key: $N8N_API_KEY" \
  > $BACKUP_DIR/n8n-workflows.json

# 5. 生成备份清单
cat > $BACKUP_DIR/BACKUP-MANIFEST.md << EOF
# 备份清单

## 包含内容
- [x] 墨墨工作区
- [x] 新媒体 Agent 工作区
- [x] SQLite 数据库 ($(du -h $BACKUP_DIR/newmedia.db | cut -f1))
- [x] n8n 工作流

## 恢复指南
1. 恢复工作区：cp -r $BACKUP_DIR/writer ~/Documents/openclaw/agents/
2. 恢复数据库：cp $BACKUP_DIR/newmedia.db ~/Documents/openclaw/agents/media/
3. 导入 n8n 工作流：通过 n8n UI 导入 JSON

## 备份时间
$(date)
EOF
```

---

## 🔄 恢复影响分析

### 1. 恢复流程变化

**原有恢复（简单）：**
```bash
# 1. 恢复工作区
cp -r ~/backup/agents/writer ~/Documents/openclaw/agents/

# 2. 重启 OpenClaw
openclaw gateway restart

# 完成！
```

**新增恢复（复杂）：**
```bash
# 1. 恢复工作区（不变）
cp -r ~/backup/agents/writer ~/Documents/openclaw/agents/

# 2. 恢复 SQLite 数据库（新增）
cp ~/backup/newmedia.db ~/Documents/openclaw/agents/media/

# 3. 恢复 n8n 工作流（新增）
# 通过 n8n UI 导入 JSON
# 或 API 批量导入

# 4. 验证数据库
sqlite3 ~/Documents/openclaw/agents/media/newmedia.db \
  "SELECT COUNT(*) FROM tasks;"

# 5. 验证 n8n 工作流
# 测试运行工作流

# 6. 重启 OpenClaw
openclaw gateway restart
```

### 2. 恢复时间对比

| 组件 | 恢复时间 | 复杂度 |
|------|---------|--------|
| MD 文件 | <1 分钟 | ⭐ |
| SQLite 数据库 | <1 分钟 | ⭐⭐ |
| n8n 工作流 | 5-10 分钟 | ⭐⭐⭐ |
| **总计** | **10-15 分钟** | **⭐⭐⭐** |

### 3. 恢复风险

**SQLite 数据库：**
- ✅ 恢复简单（复制文件）
- ⚠️ 数据库损坏风险（需验证完整性）
- ⚠️ 数据一致性问题（备份时的进行中的任务）

**n8n 工作流：**
- ✅ 工作流 JSON 易恢复
- ⚠️ API Key/凭证需重新配置
- ⚠️ Webhook URL 可能变化

**临时子代理：**
- ✅ 无需恢复（按需创建）
- ✅ 无状态设计

---

## 🖤 对墨墨的影响分析

### 1. 墨墨的核心文件

**影响：** ❌ **无影响**

```
墨墨的核心文件：
├── SOUL.md          ← 不变
├── IDENTITY.md      ← 不变
├── USER.md          ← 不变
├── memory/          ← 不变
└── SESSION-STATE.md ← 不变

新媒体 Agent 的 SQLite/n8n 不影响墨墨
```

### 2. 墨墨的技能需求

**新增技能（可选）：**

| 技能 | 必要性 | 说明 |
|------|--------|------|
| SQLite 基础查询 | ⭐⭐⭐ | 检查任务状态、生成报告 |
| n8n API 调用 | ⭐⭐ | 触发工作流、检查状态 |
| 数据库备份 | ⭐⭐ | 定期备份、验证完整性 |
| 成本监控 | ⭐⭐⭐ | API 消耗跟踪、预警 |

**技能实现：**
```markdown
# 墨墨的 TOOLS.md 更新

### SQLite 数据库管理
- 数据库位置：`~/Documents/openclaw/agents/media/newmedia.db`
- 常用查询：
  ```sql
  SELECT COUNT(*) FROM tasks WHERE date(created_at) = date('now');
  SELECT platform, COUNT(*) FROM tasks GROUP BY platform;
  ```

### n8n 工作流管理
- n8n API: `http://localhost:5678/api/v1/`
- API Key: `$N8N_API_KEY`（从环境变量读取）
- 常用操作：
  - 触发工作流
  - 查询执行历史
  - 导出工作流备份

### 成本监控
- 每日检查 API 消耗
- 每周生成报告
- 超额预警（>$3/天 通知，>$5/天 告警）
```

### 3. 墨墨的工作流程变化

**原有流程：**
```
哥哥 → 墨墨 → 新媒体 Agent → 墨墨审查 → 哥哥
```

**新增流程：**
```
哥哥 → 墨墨 → 分配任务
           ↓
    ┌──────┴──────┐
    ↓             ↓
n8n 工作流    临时子代理
    ↓             ↓
    └──────┬──────┘
           ↓
       SQLite 数据库
           ↓
       墨墨审查 → 哥哥
```

**变化：**
- ✅ 墨墨从"执行者"变成"协调者"
- ✅ 墨墨需要监控 n8n 和子代理
- ✅ 墨墨从数据库读取结果（而非文件）
- ⚠️ 墨墨需要新技能（SQLite 查询、n8n API）

### 4. 墨墨的备份独立性

**关键保证：**
```
✅ 墨墨的备份独立于新媒体 Agent
✅ 新媒体 Agent 的 SQLite/n8n 不影响墨墨
✅ 即使新媒体 Agent 完全丢失，墨墨完好无损
```

**备份分离：**
```
~/Documents/openclaw/backups/
├── 墨墨-momo-2026-03-06/    ← 墨墨的备份（独立）
│   └── workspace/
│       ├── SOUL.md
│       ├── memory/
│       └── ...
│
└── 新媒体-media-2026-03-06/ ← 新媒体的备份（独立）
    ├── workspace/
    ├── newmedia.db
    └── n8n-workflows.json
```

---

## 📊 影响总结

### 备份影响

| 维度 | 影响程度 | 说明 |
|------|---------|------|
| 备份复杂度 | ⭐⭐⭐ 增加 | 需备份 SQLite + n8n |
| 备份时间 | ⭐⭐ 略增 | +2-5 分钟 |
| 备份大小 | ⭐⭐ 略增 | +10-50MB（数据库） |
| 墨墨备份 | ❌ 无影响 | 独立备份 |

### 恢复影响

| 维度 | 影响程度 | 说明 |
|------|---------|------|
| 恢复复杂度 | ⭐⭐⭐ 增加 | 需恢复 SQLite + n8n |
| 恢复时间 | ⭐⭐⭐ 增加 | +10-15 分钟 |
| 恢复风险 | ⭐⭐ 中等 | 数据库一致性、n8n 配置 |
| 墨墨恢复 | ❌ 无影响 | 独立恢复 |

### 对墨墨的影响

| 维度 | 影响程度 | 说明 |
|------|---------|------|
| 核心文件 | ❌ 无影响 | 完全独立 |
| 技能需求 | ⭐⭐ 略增 | SQLite 查询、n8n API |
| 工作流程 | ⭐⭐ 变化 | 从执行变协调 |
| 备份独立性 | ✅ 完全独立 | 不受新媒体影响 |

---

## 🎯 建议

### 备份策略优化

1. **分离备份**
   - 墨墨的备份：每日自动
   - 新媒体的备份：每日数据库 + 每周 n8n

2. **数据库备份**
   - 启用 WAL 模式
   - 每日备份，保留 30 天
   - 每周验证完整性

3. **n8n 备份**
   - 使用 n8n 云端（自动备份）
   - 或本地部署 + Git 管理

4. **恢复演练**
   - 每月测试恢复一次
   - 验证数据库完整性
   - 测试 n8n 工作流

### 墨墨技能增强

1. **SQLite 基础**
   - 查询任务状态
   - 生成统计报告
   - 验证数据完整性

2. **n8n API**
   - 触发工作流
   - 查询执行历史
   - 导出备份

3. **成本监控**
   - 每日检查 API 消耗
   - 每周生成报告
   - 超额预警

---

## ✅ 结论

**对备份和恢复的影响：**
- ⚠️ 复杂度增加（需备份 SQLite + n8n）
- ⚠️ 恢复时间增加（+10-15 分钟）
- ✅ 但可管理（有明确流程）

**对墨墨的影响：**
- ✅ 核心文件完全独立
- ✅ 备份完全独立
- ✅ 恢复完全独立
- ⚠️ 需要新技能（SQLite、n8n）
- ⚠️ 工作流程变化（从执行变协调）

**总体评估：**
- ✅ 方案可行
- ✅ 墨墨不受负面影响
- ⚠️ 需要增加备份和监控流程
- ⚠️ 墨墨需要学习新技能

---

*墨墨 (Mò) - 方案影响分析 🖤*
