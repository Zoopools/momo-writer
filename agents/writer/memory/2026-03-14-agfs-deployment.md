# AGFS 引擎部署记录 - 公司端 (Mac-mini)

**时间**: 2026-03-14 19:27  
**部署端**: 公司端 (Mac-mini)  
**引擎版本**: AGFS Server (二进制空投部署)

---

## 1. 部署架构快照 (Current State)

### 引擎 (AGFS Server)
- **状态**: ✅ 已通过二进制空投完成部署
- **监听地址**: `127.0.0.1:1933`
- **守护模式**: nohup 运行 (PID: 65229)
- **特性**: 退出终端不影响引擎存活

### 工作空间 (Workspace)
| 端点 | 物理路径 | 挂载点 |
|------|---------|--------|
| 公司端 (Mac-mini) | `/Users/whiteareas/Documents/openclaw/openviking_workspace` | `/workspace` |
| 家端 (MBP) | `/Users/wh1ko/Documents/openclaw/openviking_workspace` | `/workspace` |

---

## 2. 核心验证结论

### 物理层 ✅
```bash
nc -zv 127.0.0.1 1933  # 握手成功
# 1933 端口处于 LISTEN 状态
```

### 应用层 ✅
- **外部 curl 探测**: 返回 `404 Not Found`
- **状态**: 正常安全响应
- **说明**: 引擎静默监听，仅响应 SDK/API 指令

### 文件层 ✅
- `soul.md` 已在公司端测试注入
- 路径映射通过日志初始化校验

---

## 3. 操作注意事项 (Important)

### ⚠️ 路径隔离
- **公司端 User**: `whiteareas`
- **家端 User**: `wh1ko`
- **严禁**: 在配置文件或代码中使用绝对路径
- **必须**: 保持 YAML 配置的动态适配

### ⚠️ 同步协议
- **限制**: 跨端通信受防火墙限制
- **现阶段方案**: 依赖 `scripts/sync-memory.sh` 进行"中转同步"
- **非实时**: 不能直接实时探测

### ⚠️ 引擎更新流程
仓库已瘦身。更新二进制引擎需执行：
```
本地打包 -> Git 临时上传 -> 对端拉取 -> Git 物理删除
```

---

## 4. 墨墨的下一步任务

### ✅ 索引重建
- **下次启动时**: 优先扫描各自本地的 workspace
- **目标**: 建立 AGFS 文件索引

### ✅ 状态监控
- **检查命令**: `nc -zv 127.0.0.1 1933`
- **异常处理**: 若 1933 端口无法连接，提示哥哥检查 nohup 进程是否存活
- **进程检查**: `ps aux | grep agfs`

---

## 5. 快速参考

### 检查 AGFS 引擎状态
```bash
# 端口监听检查
nc -zv 127.0.0.1 1933

# 进程存活检查
ps aux | grep agfs | grep -v grep

# 日志查看
tail -f /Users/whiteareas/Documents/openclaw/openviking_workspace/logs/agfs.log
```

### 重启 AGFS 引擎
```bash
# 1. 查找并终止旧进程
pkill -f agfs-server

# 2. 重新启动 (nohup 模式)
nohup /Users/whiteareas/Documents/openclaw/openviking_workspace/bin/agfs-server > logs/agfs.log 2>&1 &

# 3. 验证端口
nc -zv 127.0.0.1 1933
```

---

**部署状态**: 🟢 公司端 AGFS 引擎运行正常  
**同步状态**: ⏳ 等待家端 (MBP) 部署对齐  
**记忆签名**: 🖤 墨墨已记录
