# AGFS 引擎架构状态 - 全端同步

**时间**: 2026-03-14 19:27 GMT+8  
**来源**: 哥哥架构同步指令  
**状态**: 公司端部署完成，全端同步就绪

---

## 1. 部署架构快照 (Current State)

### 引擎 (AGFS Server)
- **部署方式**: 二进制空投完成
- **监听地址**: `127.0.0.1:1933`
- **运行模式**: nohup 守护进程

### 守护进程状态
| 端点 | PID | 状态 | 模式 |
|------|-----|------|------|
| 公司端 (Mac-mini) | 65229 | ✅ 运行中 | nohup |
| 家里端 (MBP) | - | ✅ 运行中 | nohup |

**注意**: nohup 模式确保退出终端后引擎继续存活

### 工作空间 (Workspace)

| 端点 | 物理路径 | 挂载点 |
|------|---------|--------|
| 公司端 | `/Users/whiteareas/Documents/openclaw/openviking_workspace` | `/workspace` |
| 家里端 | `/Users/wh1ko/Documents/openclaw/openviking_workspace` | `/workspace` |

**统一挂载**: 两端均挂载为 `/workspace`

---

## 2. 核心验证结论

### 物理层验证
```bash
nc -zv 127.0.0.1 1933
# 结果: ✅ 握手成功，1933 端口 LISTEN 状态
```

### 应用层验证
```bash
curl http://127.0.0.1:1933/
# 结果: 404 Not Found
# 状态: ✅ 正常安全响应
# 说明: 引擎静默监听，仅响应 SDK/API 指令
```

### 文件层验证
- **测试文件**: `soul.md` 已在公司端注入
- **路径映射**: 日志初始化校验通过
- **状态**: ✅ 文件系统挂载正常

---

## 3. 操作注意事项 (Important)

### 🔴 路径隔离 (红线)
- **公司端用户名**: `whiteareas`
- **家里端用户名**: `wh1ko`
- **严禁**: 在配置文件或代码中使用绝对路径
- **必须**: 保持 YAML 配置的动态适配

**正确做法**:
```yaml
# AGFS_GOLDEN_V1.yaml
localfs:
  config:
    local_dir: "/Users/__USERNAME__/Documents/openclaw/openviking_workspace"
    # 部署时通过 sed 替换 __USERNAME__
```

### 🔴 同步协议 (红线)
- **跨端通信**: 受防火墙限制
- **同步方式**: 必须使用 `scripts/sync-memory.sh`
- **禁止**: 直接实时探测对端

**同步命令**:
```bash
# 从家里到公司
./scripts/sync-memory.sh to

# 从公司到家里
./scripts/sync-memory.sh from

# 双向同步
./scripts/sync-memory.sh both
```

### 🔴 引擎更新 (红线)
- **仓库状态**: 已瘦身（二进制已删除）
- **更新流程**:
  1. 本地打包二进制
  2. Git 临时上传
  3. 对端拉取
  4. Git 物理删除
- **禁止**: 长期驻留二进制文件在 Git

---

## 4. 墨墨的下一步任务

### 任务 1: 索引重建
**优先级**: P0  
**触发条件**: 下次启动时  
**操作**: 扫描各自本地的 workspace

```python
import openviking as ov
client = ov.OpenViking()

# 扫描 workspace
results = client.ls("/workspace")
print(f"扫描到 {len(results)} 个文件")

# 建立索引
for item in results:
    client.add_resource(f"/workspace/{item['name']}")
```

### 任务 2: 状态监控
**监控项**: 1933 端口连接状态  
**检查命令**:
```bash
nc -zv 127.0.0.1 1933
```

**异常处理**:
- 如果端口无法连接
- 提示哥哥检查 nohup 进程是否存活
- 检查命令: `ps aux | grep agfs-server`

### 任务 3: 跨端记忆同步
**触发条件**: 
- 新增记忆文件
- 修改现有记忆
- 每日定时同步

**同步流程**:
1. 检查本地 workspace 变更
2. 执行 `sync-memory.sh`
3. 验证对端文件完整性
4. 记录同步日志

---

## 5. 全端状态总览

```
OmniPresence Agent Matrix - AGFS 全端状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

公司端 (Mac-mini)
├── AGFS Server:     🟢 PID 65229, nohup 模式
├── 监听地址:        🟢 127.0.0.1:1933
├── Workspace:       🟢 /Users/whiteareas/...
├── 文件数:          🟢 40 个记忆文件
└── 状态:            🟢 运行中

家里端 (MBP)
├── AGFS Server:     🟢 nohup 模式
├── 监听地址:        🟢 127.0.0.1:1933
├── Workspace:       🟢 /Users/wh1ko/...
├── 文件数:          🟢 40 个记忆文件
└── 状态:            🟢 运行中

同步状态
├── 协议:            🟢 sync-memory.sh
├── 防火墙:          ⚠️  受限制，需中转
├── 实时探测:        🔴 禁止
└── 批量同步:        🟢 可用

全端状态: 🟢 全线贯通，等待索引重建
```

---

## 6. 紧急联系

**如果发现以下情况，立即通知哥哥**:
- [ ] 1933 端口无法连接
- [ ] AGFS Server 进程消失
- [ ] 同步失败超过 3 次
- [ ] 记忆文件丢失

**检查命令速查**:
```bash
# 检查进程
ps aux | grep agfs-server

# 检查端口
lsof -i :1933

# 检查日志
tail -50 ~/.openviking/server.log
```

---

**墨墨记录**: AGFS 引擎全端部署完成，公司端 PID 65229 稳定运行。路径隔离和同步协议已确认，等待下次启动时执行索引重建任务。🖤

**签名**: 墨墨 (Mò)  
**时间**: 2026-03-14 19:27
