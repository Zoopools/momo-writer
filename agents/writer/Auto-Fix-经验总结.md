# OpenClaw macOS Auto-Fix 使用指南

**版本：** 1.0  
**创建时间：** 2026-03-07  
**作者：** 墨墨 (Mò)  
**参考：** https://github.com/win4r/openclaw-min-bundle

---

## 📋 **功能概述**

macOS 版本的 OpenClaw Auto-Fix 机制，包含：

1. **自动故障检测** - 检测 Gateway 是否崩溃或异常
2. **自动修复** - 验证配置、清理缓存、释放端口
3. **自动重启** - 多次尝试重启 Gateway
4. **日志收集** - 保存故障日志供分析
5. **配置备份** - 自动备份配置文件
6. **Heartbeat 集成** - 定期检查 Gateway 健康

---

## 📁 **文件结构**

```
~/.openclaw/
├── scripts/
│   ├── auto-fix.sh              # 主修复脚本
│   └── heartbeat-gateway-check.sh  # Heartbeat 检查脚本
├── launchd/
│   └── ai.openclaw.gateway.plist   # LaunchAgent 配置（增强版）
├── logs/
│   ├── auto-fix.log             # Auto-fix 日志
│   ├── gateway.log              # Gateway 日志
│   └── heartbeat-gateway.log    # Heartbeat 检查日志
└── backups/
    └── openclaw-*.json          # 配置备份
```

---

## 🚀 **安装步骤**

### 1. 确认脚本已安装

```bash
ls -la ~/.openclaw/scripts/
# 应该看到：
# - auto-fix.sh
# - heartbeat-gateway-check.sh
```

### 2. 确认执行权限

```bash
chmod +x ~/.openclaw/scripts/auto-fix.sh
chmod +x ~/.openclaw/scripts/heartbeat-gateway-check.sh
```

### 3. 安装增强版 LaunchAgent（可选）

```bash
# 停止当前 Gateway
openclaw gateway stop

# 卸载旧的 LaunchAgent
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>/dev/null || true

# 复制新配置
cp ~/.openclaw/launchd/ai.openclaw.gateway.plist ~/Library/LaunchAgents/

# 加载新的 LaunchAgent
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 启动 Gateway
openclaw gateway start --force
```

### 4. 验证安装

```bash
# 检查 Gateway 状态
openclaw status

# 应该看到：
# │ Gateway service │ LaunchAgent installed · loaded · running (pid xxxxx) │
# │ Feishu          │ ON · OK · configured · accounts 2/2                 │
```

---

## 🔧 **使用方法**

### 手动触发 Auto-Fix

```bash
# 直接运行修复脚本
bash ~/.openclaw/scripts/auto-fix.sh
```

### 查看 Auto-Fix 日志

```bash
# 查看最新日志
tail -f ~/.openclaw/logs/auto-fix.log

# 查看历史日志
ls -la ~/.openclaw/logs/auto-fix.log
```

### Heartbeat 自动检查

墨墨会在每次 heartbeat 时自动检查 Gateway 状态：

- **检查频率：** 每 4 小时
- **检查项：** Gateway 运行状态、Feishu 连接状态
- **自动修复：** 发现异常自动触发 auto-fix

---

## 📊 **故障处理流程**

### 流程图

```
Gateway 异常检测
    ↓
收集日志 (保存到 backups/)
    ↓
备份配置 (保存到 backups/)
    ↓
验证配置 (openclaw config validate)
    ↓
运行 doctor (openclaw doctor --fix)
    ↓
清理缓存 (rm -rf ~/.openclaw/cache/*)
    ↓
检查端口占用 (lsof -i :18789)
    ↓
释放端口 (如有占用)
    ↓
重启 Gateway (最多 3 次)
    ↓
检查是否成功
    ├─ 成功 → 发送通知 → 完成 ✅
    └─ 失败 → 发送警报 → 等待人工干预 ❌
```

### 自动修复内容

| 修复项 | 说明 |
|--------|------|
| **配置验证** | 运行 `openclaw config validate` |
| **Doctor 修复** | 运行 `openclaw doctor --fix` |
| **缓存清理** | 删除 `~/.openclaw/cache/*` |
| **端口释放** | 检查并释放 18789 端口 |
| **配置恢复** | 从最新备份恢复配置（如需要） |
| **Gateway 重启** | 最多尝试 3 次重启 |

---

## 🔍 **故障诊断**

### 查看 Gateway 状态

```bash
openclaw status
```

### 查看 Gateway 日志

```bash
tail -100 ~/.openclaw/logs/gateway.log
```

### 查看 Auto-Fix 日志

```bash
tail -100 ~/.openclaw/logs/auto-fix.log
```

### 运行诊断

```bash
openclaw doctor
```

### 检查 LaunchAgent 状态

```bash
# 查看 LaunchAgent 状态
launchctl print gui/$(id -u)/ai.openclaw.gateway

# 查看系统日志
log show --predicate 'process == "node"' --last 10m | grep -i openclaw
```

---

## ⚙️ **配置选项**

### 环境变量

可以在 `~/.openclaw/scripts/auto-fix.sh` 中修改：

```bash
LOG_FILE="$HOME/.openclaw/logs/auto-fix.log"      # 日志文件路径
GATEWAY_LOG="$HOME/.openclaw/logs/gateway.log"    # Gateway 日志路径
CONFIG_FILE="$HOME/.openclaw/openclaw.json"       # 配置文件路径
BACKUP_DIR="$HOME/.openclaw/backups"              # 备份目录
MAX_RESTART_ATTEMPTS=3                            # 最大重启次数
RESTART_INTERVAL=10                               # 重启间隔（秒）
```

### 通知配置（可选）

目前支持 macOS 系统通知，可以扩展：

```bash
# Telegram 通知（需要配置）
export OPENCLAW_FIX_TELEGRAM_TARGET="<chat_id>"
export TELEGRAM_BOT_TOKEN="<bot_token>"

# 飞书通知（需要配置）
# 可以在 send_notification() 函数中添加飞书 API 调用
```

---

## 📋 **常见问题**

### Q1: Auto-Fix 脚本无法执行

**解决方案：**
```bash
# 检查执行权限
chmod +x ~/.openclaw/scripts/auto-fix.sh

# 检查 bash 路径
which bash  # 应该是 /bin/bash 或 /usr/local/bin/bash
```

### Q2: Gateway 反复崩溃

**可能原因：**
1. 配置错误
2. 端口占用
3. 插件冲突

**解决方案：**
```bash
# 1. 检查配置
openclaw config validate

# 2. 检查端口
lsof -i :18789

# 3. 检查插件
openclaw plugins list

# 4. 查看详细日志
tail -f ~/.openclaw/logs/gateway.log
```

### Q3: LaunchAgent 无法启动 Gateway

**可能原因：**
1. 环境变量问题
2. 路径问题
3. 权限问题

**解决方案：**
```bash
# 1. 手动启动测试
openclaw gateway start --force

# 2. 检查 LaunchAgent 配置
cat ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 3. 重新加载 LaunchAgent
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### Q4: 备份文件太多

**解决方案：**
```bash
# 清理 7 天前的备份
find ~/.openclaw/backups -name "*.json" -mtime +7 -delete

# 清理 7 天前的日志
find ~/.openclaw/logs -name "*.log" -mtime +7 -delete
```

---

## 🎯 **最佳实践**

### 1. 定期检查

```bash
# 每天检查 Gateway 状态
openclaw status

# 每周清理日志和备份
find ~/.openclaw/backups -mtime +7 -delete
find ~/.openclaw/logs -mtime +7 -delete
```

### 2. 配置备份

```bash
# 手动备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d)
```

### 3. 监控日志

```bash
# 实时监控 Gateway 日志
tail -f ~/.openclaw/logs/gateway.log | grep -E "error|warn|fail"
```

### 4. 测试 Auto-Fix

```bash
# 定期测试 auto-fix 脚本（不会实际修复，只检查）
bash ~/.openclaw/scripts/auto-fix.sh
```

---

## 📈 **版本历史**

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0 | 2026-03-07 | 初始版本，包含 auto-fix、heartbeat 集成、LaunchAgent 增强 |

---

## 🔗 **参考资料**

- 原仓库：https://github.com/win4r/openclaw-min-bundle
- OpenClaw 文档：https://docs.openclaw.ai
- LaunchAgent 文档：https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html

---

*墨墨 (Mò) - 2026-03-07* 🖤  
*让 OpenClaw 更稳定、更智能！*
