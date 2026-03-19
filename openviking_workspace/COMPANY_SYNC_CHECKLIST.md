# OpenViking 公司端同步清单

**版本**: GOLDEN v1.0  
**目标**: Mac-mini (公司端)  
**源**: MBP (家里端)  
**时间**: 2026-03-14 18:38 GMT+8

---

## 📦 需要同步的文件

### 1. Binary 文件

| 文件 | 源位置 | 目标位置 | 大小 |
|------|--------|----------|------|
| agfs-server | `~/.local/bin/agfs-server` | `~/.local/bin/agfs-server` | ~37MB |
| ov | `~/.local/bin/ov` | `~/.local/bin/ov` | ~6MB |

**验证命令**:
```bash
~/.local/bin/agfs-server --version  # 应显示 v0.2.7-4-g20b5dab
~/.local/bin/ov --version           # 应显示 openviking 0.2.1
```

---

### 2. Config 文件

| 文件 | 源位置 | 目标位置 | 需要修改 |
|------|--------|----------|----------|
| AGFS_GOLDEN_V1.yaml | `~/.openviking/AGFS_GOLDEN_V1.yaml` | `~/.openviking/AGFS_GOLDEN_V1.yaml` | ✅ YES |
| OPENVIKING_GOLDEN_V1.json | `~/.openviking/OPENVIKING_GOLDEN_V1.json` | `~/.openviking/OPENVIKING_GOLDEN_V1.json` | ⚠️ 检查 API Key |

**关键修改项**:
```yaml
# AGFS_GOLDEN_V1.yaml 第 44 行
localfs:
  enabled: true
  path: "/workspace"
  config:
    local_dir: "/Users/__COMPANY_USERNAME__/Documents/openclaw/openviking_workspace"  # ← 修改这里
    mount_path: "/workspace"
```

---

### 3. 工作目录

| 目录 | 源位置 | 目标位置 | 内容 |
|------|--------|----------|------|
| viking_workspace | `~/Documents/openclaw/openviking_workspace` | `~/Documents/openclaw/openviking_workspace` | 40 个记忆文件 |

**文件清单**:
```
openviking_workspace/
├── 2026-03-06.md ~ 2026-03-14.md (14 个)
├── 2026-03-14-Success.md
├── Auto-Fix-经验总结.md
├── ClawRouter 整合方案.md
├── OpenClaw 集中配置管理系统.md
├── ... (共 40 个文件)
└── 早报/
```

---

## 🔧 公司端部署步骤

### 步骤 1: 创建目录结构

```bash
# 在公司 Mac-mini 上执行
mkdir -p ~/.local/bin
mkdir -p ~/.openviking
mkdir -p ~/Documents/openclaw/openviking_workspace
```

### 步骤 2: 复制 Binary

```bash
# 从 Git 或家里复制
scp user@home-mbp:~/.local/bin/agfs-server ~/.local/bin/
scp user@home-mbp:~/.local/bin/ov ~/.local/bin/
chmod +x ~/.local/bin/agfs-server ~/.local/bin/ov
```

### 步骤 3: 复制 Config

```bash
# 从 Git 复制
git clone https://github.com/Zoopools/momo-writer.git
cp momo-writer/openviking-config/AGFS_GOLDEN_V1.yaml ~/.openviking/
cp momo-writer/openviking-config/OPENVIKING_GOLDEN_V1.json ~/.openviking/
```

### 步骤 4: 修改路径变量

```bash
# 获取公司端用户名
COMPANY_USER=$(whoami)

# 修改 AGFS 配置
sed -i.bak "s|/Users/wh1ko|/Users/${COMPANY_USER}|g" ~/.openviking/AGFS_GOLDEN_V1.yaml

# 验证修改
grep "local_dir:" ~/.openviking/AGFS_GOLDEN_V1.yaml
```

### 步骤 5: 复制记忆文件

```bash
# 从 Git 或家里复制 40 个记忆文件
rsync -av user@home-mbp:~/Documents/openclaw/openviking_workspace/ \
  ~/Documents/openclaw/openviking_workspace/
```

### 步骤 6: 启动服务

```bash
# 启动 AGFS Server
~/.local/bin/agfs-server -c ~/.openviking/AGFS_GOLDEN_V1.yaml

# 验证启动
tail -20 ~/.openviking/server.log
```

### 步骤 7: 验证测试

```bash
# Python 测试
export OPENVIKING_CONFIG_FILE=~/.openviking/OPENVIKING_GOLDEN_V1.json
python3.11 -c "
import openviking as ov
client = ov.OpenViking()
print('✅ 客户端连接成功')
results = client.ls('/')
print(f'✅ 找到 {len(results)} 个根目录条目')
client.close()
"
```

---

## ✅ 公司端验证清单

部署完成后检查：

- [ ] `~/.local/bin/agfs-server --version` 显示版本
- [ ] `~/.local/bin/ov --version` 显示版本
- [ ] `~/.openviking/AGFS_GOLDEN_V1.yaml` 存在且路径已修改
- [ ] `~/Documents/openclaw/openviking_workspace` 有 40 个文件
- [ ] AGFS Server 启动无错误
- [ ] Python 客户端可以连接
- [ ] `client.ls('/')` 返回 4 个条目
- [ ] 端口 1933 可访问

---

## 🆘 常见问题

### Q1: 公司端 Python 版本不对？
```bash
# 安装 Python 3.11
brew install python@3.11
```

### Q2: 公司端没有 OpenViking Python 包？
```bash
/usr/local/bin/python3.11 -m pip install openviking
```

### Q3: AGFS Server 启动失败？
```bash
# 检查端口占用
lsof -i :1933
# 清理后重试
pkill -f agfs-server
```

---

## 📋 同步命令速查

```bash
# 在家里打包
mkdir -p ~/openviking-sync
cp ~/.local/bin/{agfs-server,ov} ~/openviking-sync/
cp ~/.openviking/{AGFS_GOLDEN_V1.yaml,OPENVIKING_GOLDEN_V1.json} ~/openviking-sync/
tar czf ~/openviking-sync.tar.gz ~/openviking-sync ~/Documents/openclaw/openviking_workspace

# 在公司解压
tar xzf ~/openviking-sync.tar.gz -C ~/
# 然后执行上面的部署步骤 4-7
```

---

**准备完成！等待哥哥指令同步到 Mac-mini 🖤**
