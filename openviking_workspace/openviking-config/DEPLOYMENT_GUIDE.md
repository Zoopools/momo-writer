# OpenViking 部署指南 - OmniPresence Agent Matrix

**版本**: GOLDEN v1.0  
**生成时间**: 2026-03-14 18:33 GMT+8  
**状态**: ✅ 已验证可用

---

## 📋 文件清单

| 文件 | 用途 | 位置 |
|------|------|------|
| `AGFS_GOLDEN_V1.yaml` | AGFS Server 配置 | `~/.openviking/` |
| `OPENVIKING_GOLDEN_V1.json` | OpenViking 客户端配置 | `~/.openviking/` |
| `agfs-server` | AGFS Server 二进制 | `~/.local/bin/` |
| `ov` | OpenViking CLI | `~/.local/bin/` |

---

## 🚀 快速启动

### 1. 启动 AGFS Server

```bash
# 使用 GOLDEN 配置启动
~/.local/bin/agfs-server -c ~/.openviking/AGFS_GOLDEN_V1.yaml

# 或使用后台模式
nohup ~/.local/bin/agfs-server -c ~/.openviking/AGFS_GOLDEN_V1.yaml > ~/.openviking/server.log 2>&1 &
```

### 2. 验证启动

查看日志确认以下关键信息：
```
✅ localfs instance 'localfs' mounted at /workspace
✅ sqlfs instance 'sqlfs' mounted at /sqlfs
✅ Starting AGFS server on localhost:1933
```

### 3. 测试 Python 客户端

```bash
export OPENVIKING_CONFIG_FILE=~/.openviking/OPENVIKING_GOLDEN_V1.json
python3.11 -c "
import openviking as ov
client = ov.OpenViking()
results = client.search('OpenClaw')
for r in results:
    print(f'- {r.uri}: {r.score}')
client.close()
"
```

---

## ⚠️ 关键注意事项

### 1. 路径配置

**AGFS Server (`AGFS_GOLDEN_V1.yaml`)**:
- `local_dir`: 必须使用绝对路径
- 当前配置: `/Users/wh1ko/Documents/openclaw/openviking_workspace`
- **公司端部署时需要修改为对应路径**

### 2. API Key

**OPENVIKING_GOLDEN_V1.json**:
- 包含火山引擎 API Key
- **不要上传到 Git！**
- 公司端部署时需要使用相同的 Key 或申请新的 Key

### 3. 端口

- AGFS Server: `localhost:1933`
- **不要修改**，这是 OpenViking 客户端的默认连接端口

---

## 🏢 公司端部署步骤

### 步骤 1: 复制文件

```bash
# 在家里打包
mkdir -p ~/openviking-deploy
cp ~/.local/bin/agfs-server ~/openviking-deploy/
cp ~/.local/bin/ov ~/openviking-deploy/
cp ~/.openviking/AGFS_GOLDEN_V1.yaml ~/openviking-deploy/
cp ~/.openviking/OPENVIKING_GOLDEN_V1.json ~/openviking-deploy/

# 压缩
tar czf openviking-deploy.tar.gz ~/openviking-deploy
```

### 步骤 2: 在公司解压

```bash
# 解压到对应位置
mkdir -p ~/.local/bin
cp agfs-server ov ~/.local/bin/
chmod +x ~/.local/bin/agfs-server ~/.local/bin/ov

mkdir -p ~/.openviking
cp AGFS_GOLDEN_V1.yaml OPENVIKING_GOLDEN_V1.json ~/.openviking/
```

### 步骤 3: 修改配置

编辑 `~/.openviking/AGFS_GOLDEN_V1.yaml`:
```yaml
localfs:
  enabled: true
  path: "/workspace"
  config:
    local_dir: "/Users/YOUR_USERNAME/Documents/openclaw/openviking_workspace"  # 修改这里
    mount_path: "/workspace"
```

### 步骤 4: 启动

```bash
~/.local/bin/agfs-server -c ~/.openviking/AGFS_GOLDEN_V1.yaml
```

---

## ✅ 验证清单

部署完成后检查：

- [ ] AGFS Server 启动无错误
- [ ] 日志显示所有插件已挂载
- [ ] Python 客户端可以连接
- [ ] 语义搜索返回结果
- [ ] 端口 1933 可访问

---

## 🆘 故障排除

### 问题 1: 端口被占用
```bash
pkill -f agfs-server
```

### 问题 2: 配置文件格式错误
- AGFS Server 只接受 YAML 格式
- OpenViking 客户端只接受 JSON 格式

### 问题 3: local_dir 路径不存在
```bash
mkdir -p /Users/YOUR_USERNAME/Documents/openclaw/openviking_workspace
```

---

**维护者**: 墨墨 (Mò) 🖤  
**最后更新**: 2026-03-14
