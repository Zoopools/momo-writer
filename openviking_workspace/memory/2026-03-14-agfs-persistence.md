# AGFS 底层持久化改造 - 环境感知逻辑更新

**时间**: 2026-03-14 19:52  
**状态**: 🟢 全自动运行 | 3.12 宇宙"无人值守"阶段

---

## 1. 引擎身份与路径对齐 (Binary Truth)

### 最终本体路径
```
/Users/whiteareas/.local/bin/agfs-server
```

### ⚠️ 异常修正
- **作废逻辑**: 在 workspace 目录下寻找引擎
- **正确逻辑**: 系统级诊断时，以 `.local/bin/agfs-server` 为准

### 诊断命令
```bash
# 检查引擎存在
ls -la /Users/whiteareas/.local/bin/agfs-server

# 检查版本
/Users/whiteareas/.local/bin/agfs-server --version
```

---

## 2. 守护进程协议 (Persistence Protocol)

### 管理模式
- **LaunchAgents 接管**: `com.user.agfs`
- **配置文件**: `~/Library/LaunchAgents/com.user.agfs.plist`

### 自愈特性
- **KeepAlive**: ✅ 启用
- **行为**: 进程掉线时，系统自动重启
- **墨墨感知**: 1933 端口瞬间断开又重连 = 系统自愈中

### 重启感知流程
```
1933 端口断开
    ↓
系统检测到进程异常
    ↓
KeepAlive 触发自动重启
    ↓
等待 5 秒
    ↓
1933 端口恢复
    ↓
🟢 自愈完成，无需人工干预
```

**墨墨话术**: "哥哥，AGFS 引擎正在自愈重启，请稍等 5 秒..."

---

## 3. 日志审计点 (Log Audit)

### 标准日志位置
```
~/agfs.log
```

### 日志内容
- 启动信息
- 挂载（Mount）事件
- 错误信息
- 连接状态

### 排查命令
```bash
# 实时查看
tail -f ~/agfs.log

# 查看最后 10 行（优先）
tail -n 10 ~/agfs.log

# 查看错误
grep -i "error\|fail\|panic" ~/agfs.log | tail -n 5
```

**墨墨排查流程**:
1. 发现 1933 端口异常
2. 读取 `~/agfs.log` 最后 10 行
3. 判断是自愈重启还是严重错误
4. 向哥哥报告

---

## 4. 结论：全自动运行 (Status: Autonomous)

### 公司端状态
| 项目 | 状态 | 说明 |
|------|------|------|
| 引擎位置 | 🟢 | `/Users/whiteareas/.local/bin/agfs-server` |
| 守护模式 | 🟢 | LaunchAgents (com.user.agfs) |
| 开机自启 | 🟢 | 已入编系统 |
| 自愈能力 | 🟢 | KeepAlive 自动重启 |
| 日志审计 | 🟢 | `~/agfs.log` 实时滚动 |

### 分布式状态
- **公司端**: 🟢 全自动运行
- **家里端**: ⏳ 待部署对齐
- **全线状态**: 🟢 贯通

### 3.12 宇宙阶段
**"无人值守"阶段正式开启**

- AGFS 引擎：系统级守护，自动自愈
- 记忆同步：脚本就绪，随时待命
- 墨墨角色：低功耗监控，异常告警

---

## 🛸 墨墨的环境感知逻辑更新

```python
def check_agfs_status():
    """AGFS 状态检查 - 更新后逻辑"""
    
    # 1. 检查引擎本体路径
    binary_path = "/Users/whiteareas/.local/bin/agfs-server"
    if not os.path.exists(binary_path):
        return "❌ AGFS 引擎不存在"
    
    # 2. 检查 1933 端口
    port_status = check_port(1933)
    
    if port_status == "disconnected":
        # 读取日志判断是自愈还是严重错误
        log_tail = read_log("~/agfs.log", lines=10)
        
        if "restarting" in log_tail or "keepalive" in log_tail:
            return "🔄 系统自愈中，请稍等 5 秒"
        else:
            return "❌ AGFS 异常，请检查日志"
    
    return "🟢 AGFS 运行正常"

def on_port_flapping():
    """端口闪断处理 - 自愈感知"""
    time.sleep(5)  # 等待自愈
    if check_port(1933) == "connected":
        return "🟢 自愈完成，服务恢复"
    else:
        return "❌ 自愈失败，需要人工干预"
```

---

## 📋 快速参考卡

| 操作 | 命令 |
|------|------|
| 检查引擎 | `ls /Users/whiteareas/.local/bin/agfs-server` |
| 检查端口 | `nc -zv 127.0.0.1 1933` |
| 查看日志 | `tail -n 10 ~/agfs.log` |
| 检查守护进程 | `launchctl list | grep com.user.agfs` |
| 手动重启 | `launchctl unload ~/Library/LaunchAgents/com.user.agfs.plist && launchctl load ~/Library/LaunchAgents/com.user.agfs.plist` |

---

**3.12 宇宙"无人值守"阶段已启动** 🖤🛸

*AGFS 引擎全自动运行，墨墨低功耗守护中...*
