# Gene 同步指南 - 3.12 宇宙

**时间**: 2026-03-16 08:05 GMT+8  
**来源**: 公司端修复记录  
**状态**: 需要家里端同步执行

---

## 背景

公司端（Mac-mini）已新增 **6 个 Gene 文件**，家里端（MBP）需要同步创建。

**当前状态**:
- 公司端: 10 个 Gene ✅
- 家里端: 4 个 Gene ⏳（待同步）

**新增 Gene 列表**:
1. gene_global_003 - 路径存在性检测
2. gene_global_004 - LaunchAgent 管理规范
3. gene_global_005 - 目录自动创建
4. gene_global_006 - 混合层级隔离架构
5. gene_global_007 - 配置加载器演进
6. gene_global_008 - 故障恢复与最佳实践

---

## 家里端执行步骤

### 步骤 1: 进入 Gene 目录

```bash
cd ~/.openclaw/genes/
```

### 步骤 2-7: 创建 6 个新 Gene 文件

复制以下每个代码块执行：

**Gene 003 - 路径存在性检测**
```bash
cat > gene_global_003.md << 'EOF'
# Gene Global 003 - 路径存在性检测

**类型**: 全局 Gene
**版本**: 1.0.0
**创建时间**: 2026-03-14
**适用范围**: 所有 Agent

---

## 规则：路径存在性检测

所有运维脚本必须先检测文件/目录存在性，禁止硬编码。

### 正确示例
```bash
PLIST_FILE=""
if [ -f "$HOME/Library/LaunchAgents/com.user.agfs.plist" ]; then
    PLIST_FILE="$HOME/Library/LaunchAgents/com.user.agfs.plist"
elif [ -f "$HOME/Library/LaunchAgents/com.user.agfs.server.plist" ]; then
    PLIST_FILE="$HOME/Library/LaunchAgents/com.user.agfs.server.plist"
fi
```

### 触发场景
- 编写脚本时
- 部署到多端时

*Gene 固化时间：2026-03-14*
EOF
```

**Gene 004 - LaunchAgent 管理规范**
```bash
cat > gene_global_004.md << 'EOF'
# Gene Global 004 - LaunchAgent 管理规范

**类型**: 全局 Gene
**版本**: 1.0.0
**创建时间**: 2026-03-14
**适用范围**: 所有 Agent

---

## 规则：LaunchAgent 管理规范

优先使用 launchctl 管理守护进程，禁止手动启动冲突。

### 正确示例
```bash
# 重启
launchctl kickstart -k gui/$(id - u)/com.user.agfs

# 或先卸载再加载
launchctl unload ~/Library/LaunchAgents/com.user.agfs.plist
launchctl load ~/Library/LaunchAgents/com.user.agfs.plist
```

### 触发场景
- 重启 AGFS Server 时
- 自愈脚本执行时

*Gene 固化时间：2026-03-14*
EOF
```

**Gene 005 - 目录自动创建**
```bash
cat > gene_global_005.md << 'EOF'
# Gene Global 005 - 目录自动创建

**类型**: 全局 Gene
**版本**: 1.0.0
**创建时间**: 2026-03-14
**适用范围**: 所有 Agent

---

## 规则：目录自动创建

所有涉及文件/日志的操作必须先执行 mkdir -p。

### 正确示例
```bash
mkdir -p ~/Documents/openclaw/logs
~/.local/bin/agfs-server > ~/Documents/openclaw/logs/agfs.server.log 2>&1
```

### 触发场景
- 创建日志文件时
- 创建配置文件时
- 启动服务时

*Gene 固化时间：2026-03-14*
EOF
```

**Gene 006 - 混合层级隔离架构**
```bash
cat > gene_global_006.md << 'EOF'
# Gene Global 006 - 混合层级隔离架构

**类型**: 全局 Gene
**版本**: 1.0.0
**创建时间**: 2026-03-08
**适用范围**: 所有 Agent

---

## 架构原则

### 核心设计
```
哥哥
├── 墨墨 (writer) - 首席协调员（90% 任务）
│   └── 职责：任务分配、审查、知识管理
└── 小媒 (media) - 创意专家（10% 任务）
    └── 职责：图片生成、内容创作
```

### 任务流转规则
| 任务类型 | 流转路径 | 说明 |
|---------|---------|------|
| **复杂任务** | 哥哥 → 墨墨 → 小媒 | 墨墨分配、审查 |
| **简单图片** | 哥哥 → 小媒 | 快速通道 |
| **新媒体发布** | 哥哥 → 墨墨 → 小媒 | 审查后发布 |

### 关键学习
1. OpenClaw 2026.3.2 不支持 systemPrompt
2. 权限设计：最小权限 + 物理隔离 + 逻辑隔离
3. 版本兼容：不修改 JSON，使用文件注入

*Gene 固化时间：2026-03-08*
EOF
```

**Gene 007 - 配置加载器演进**
```bash
cat > gene_global_007.md << 'EOF'
# Gene Global 007 - 配置加载器演进

**类型**: 全局 Gene
**版本**: 1.0.0
**创建时间**: 2026-03-08
**适用范围**: 所有 Agent

---

## 关键原则

### 1. 稳定性 > 性能
- 纳秒级缓存 vs 毫秒级直读
- **选择可靠**

### 2. 简单 > 复杂
- 少即是多
- **减少出错点**

### 3. 兼容 > 优化
- 适配所有环境
- **不做特殊假设**

## 权限管理
```bash
chmod 755 ~/.openclaw/config          # ✅ 平衡安全与实用
chmod 644 ~/.openclaw/config/**/*.json # ✅ 当前用户可写，其他人可读
```

*Gene 固化时间：2026-03-08*
EOF
```

**Gene 008 - 故障恢复与最佳实践**
```bash
cat > gene_global_008.md << 'EOF'
# Gene Global 008 - 故障恢复与最佳实践

**类型**: 全局 Gene
**版本**: 1.0.0
**创建时间**: 2026-03-08
**适用范围**: 所有 Agent

---

## 故障恢复流程

### Gateway 崩溃（1006 错误）
```bash
# 1. 恢复备份配置
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json

# 2. 清理网关进程和锁文件
rm -f ~/.openclaw/gateway.lock
pkill -f "openclaw gateway"

# 3. 冷启动网关
openclaw gateway start --force --allow-unconfigured
```

## 三阶段重构法
```
Phase 1: 创建新结构（纯新增，零风险）
  ↓
Phase 2: 逐步迁移（可回滚，双轨运行）
  ↓
Phase 3: 切换完成（删除旧结构）
```

## 关键原则
1. **备份是生命线** - 带时间戳的备份
2. **冷启动能力** - 知道如何完全重启
3. **文档化一切** - 问题记录到 memory/

*Gene 固化时间：2026-03-08*
EOF
```

### 步骤 8: 验证

```bash
ls -la gene_global_*.md
echo "期望看到 8 个 gene_global_*.md 文件"
echo "加上 gene_media_001.md 和 gene_shared_001.md，共 10 个 Gene"
```

---

## 一键执行（全部复制）

```bash
cd ~/.openclaw/genes/ && \
cat > gene_global_003.md << 'EOF'
# Gene Global 003 - 路径存在性检测
**类型**: 全局 Gene | **版本**: 1.0.0 | **创建时间**: 2026-03-14
---
## 规则：路径存在性检测
所有运维脚本必须先检测文件/目录存在性，禁止硬编码。
### 正确示例
PLIST_FILE=""
if [ -f "$HOME/Library/LaunchAgents/com.user.agfs.plist" ]; then
    PLIST_FILE="$HOME/Library/LaunchAgents/com.user.agfs.plist"
elif [ -f "$HOME/Library/LaunchAgents/com.user.agfs.server.plist" ]; then
    PLIST_FILE="$HOME/Library/LaunchAgents/com.user.agfs.server.plist"
fi
*Gene 固化时间：2026-03-14*
EOF
cat > gene_global_004.md << 'EOF'
# Gene Global 004 - LaunchAgent 管理规范
**类型**: 全局 Gene | **版本**: 1.0.0 | **创建时间**: 2026-03-14
---
## 规则：LaunchAgent 管理规范
优先使用 launchctl 管理守护进程，禁止手动启动冲突。
### 正确示例
launchctl kickstart -k gui/$(id - u)/com.user.agfs
*Gene 固化时间：2026-03-14*
EOF
cat > gene_global_005.md << 'EOF'
# Gene Global 005 - 目录自动创建
**类型**: 全局 Gene | **版本**: 1.0.0 | **创建时间**: 2026-03-14
---
## 规则：目录自动创建
所有涉及文件/日志的操作必须先执行 mkdir -p。
### 正确示例
mkdir -p ~/Documents/openclaw/logs
*Gene 固化时间：2026-03-14*
EOF
cat > gene_global_006.md << 'EOF'
# Gene Global 006 - 混合层级隔离架构
**类型**: 全局 Gene | **版本**: 1.0.0 | **创建时间**: 2026-03-08
---
## 架构原则
哥哥 → 墨墨 (writer, 90%) → 小媒 (media, 10%)
### 任务流转
- 复杂任务：哥哥 → 墨墨 → 小媒
- 简单图片：哥哥 → 小媒
- 新媒体发布：哥哥 → 墨墨 → 小媒
*Gene 固化时间：2026-03-08*
EOF
cat > gene_global_007.md << 'EOF'
# Gene Global 007 - 配置加载器演进
**类型**: 全局 Gene | **版本**: 1.0.0 | **创建时间**: 2026-03-08
---
## 关键原则
1. 稳定性 > 性能
2. 简单 > 复杂
3. 兼容 > 优化
## 权限管理
chmod 755 ~/.openclaw/config
chmod 644 ~/.openclaw/config/**/*.json
*Gene 固化时间：2026-03-08*
EOF
cat > gene_global_008.md << 'EOF'
# Gene Global 008 - 故障恢复与最佳实践
**类型**: 全局 Gene | **版本**: 1.0.0 | **创建时间**: 2026-03-08
---
## 故障恢复流程
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
rm -f ~/.openclaw/gateway.lock
openclaw gateway start --force --allow-unconfigured
## 三阶段重构法
Phase 1: 创建新结构 → Phase 2: 逐步迁移 → Phase 3: 切换完成
*Gene 固化时间：2026-03-08*
EOF
echo "✅ Gene 同步完成！"
ls -la gene_global_*.md
```

---

## 同步后验证

家里端执行后，运行：

```bash
evolve list
```

应该显示 **10 个 Gene**（原来 4 个 + 新增 6 个）。

---

*更新时间：2026-03-16 08:05*  
*更新者：墨墨 (公司端)*  
*版本：v2.0（新增 3 个 Gene）*
