# 统一密钥管理协议

**创建时间**: 2026-03-16  
**更新时间**: 2026-03-19  
**作者**: 墨墨 (Mò)  
**版本**: 1.1  
**标签**: #密钥管理 #安全 #协议

---

## 🔐 首席密钥官任命

**墨墨 (Writer Agent)** 正式接任 **Matrix 首席密钥官**

### 职责
- 全权负责所有 API Token、Cookie 及身份凭证的维护与安全
- 编写密钥调用接口 (key-manager)
- 确保 `~/.media/config.yaml` 在两端（家/公司）格式及路径完全一致

---

## 📁 物理路径

```
~/.media/config.yaml          # 真实密钥文件 (权限: 600, Git 忽略)
~/.media/config.yaml.template  # 模板文件 (Git 同步)
~/.media/.gitignore           # 排除规则
```

---

## 📝 调用规范

| Agent | 权限 | 规范 |
|-------|------|------|
| **墨墨** | 维护 | 维护 key-manager 接口，提供 config.yaml.template |
| **小媒** | 读取 | 禁止私自存储 Token，通过 key-manager 获取 |
| **小猎** | 读取 | 禁止私自存储 Token，通过 key-manager 获取 |

---

## 🔴 安全红线

- ❌ **严禁**将真实 config.yaml 推送到远程仓库
- ❌ **禁止**在代码中硬编码 Token
- 🟢 **仅允许**同步 config.yaml.template

---

## 🛡️ 密钥清单

### 当前管理的密钥

| 服务 | 密钥位置 | 用途 |
|------|----------|------|
| **Bailian** | `~/.media/config.yaml` | LLM API (qwen/kimi) |
| **飞书** | `~/.openclaw/openclaw.json` | Bot 认证 |
| **GitHub** | `~/.media/config.yaml` | Git 操作 |

---

## 🔄 同步协议

### 家里端 (MBP) ↔ 公司端 (Mac-mini)

| 端点 | 用户名 | 路径 |
|------|--------|------|
| 家里 MBP | wh1ko | `/Users/wh1ko/.media/config.yaml` |
| 公司 Mac-mini | whiteareas | `/Users/whiteareas/.media/config.yaml` |

### 同步命令

```bash
# 家里端推送
rsync -avz ~/.media/config.yaml whiteareas@mac-mini:~/.media/

# 或使用 Git 同步模板
git pull origin main  # 同步 config.yaml.template
```

---

## 📝 config.yaml.template 示例

```yaml
# 复制为 config.yaml 并填入真实值
bailian:
  api_key: "YOUR_BAILIAN_API_KEY"

github:
  token: "YOUR_GITHUB_TOKEN"
  
feishu:
  writer:
    app_id: "cli_xxx"
    app_secret: "xxx"
  media:
    app_id: "cli_xxx"
    app_secret: "xxx"
  hunter:
    app_id: "cli_xxx"
    app_secret: "xxx"
```

---

## 🔧 维护任务

| 频率 | 任务 |
|------|------|
| 每周 | 检查密钥有效期 |
| 每月 | 轮换敏感 Token |
| 每季度 | 审计密钥访问日志 |

---

## 📋 应急处理

### 密钥泄露

1. 立即撤销泄露的 Token
2. 生成新 Token
3. 更新 `~/.media/config.yaml`
4. 同步到所有端点
5. 检查 Git 历史，确保无硬编码

---

*最后更新: 2026-03-19*  
*维护者: 墨墨 (Mò)*
