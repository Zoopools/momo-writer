# KEYS.md - 统一密钥管理协议

**生效日期**: 2026-03-16  
**管理权**: 墨墨 (Writer Agent) - Matrix 首席密钥官 🔐  
**适用范围**: AGFS 全设备 (MBP / Mac-mini)

---

## 📜 核心原则

1. **统一管理**: 所有 API Token、Cookie、身份凭证统一存储
2. **路径一致**: 所有设备使用相同路径 `~/.media/config.yaml`
3. **安全隔离**: 真实配置严禁提交 Git，仅同步模板
4. **权限控制**: 文件权限 600 (仅所有者可读写)

---

## 🗂️ 文件结构

```
~/.media/
├── config.yaml           # 真实配置 (含敏感凭证) ⚠️ 严禁 Git 提交
├── config.yaml.template  # 配置模板 (安全) ✅ 可 Git 同步
└── .gitignore            # Git 忽略规则
```

---

## 🔑 存储的凭证类型

| 类型 | 平台 | 用途 | 优先级 |
|------|------|------|--------|
| Cookie | Twitter/X | 推文搜索/读取 | 🔴 高 |
| Cookie | 小红书 | 笔记读取/搜索 | 🟡 中 |
| Cookie | 抖音 | 视频解析 | 🟡 中 |
| Token | GitHub | 私有仓库访问 | 🟢 低 |
| URL | 代理 | 解决 IP 封锁 | 🟢 低 |

---

## 🛡️ 安全规范

### 1. 文件权限

```bash
# 设置权限 (仅所有者可读写)
chmod 600 ~/.media/config.yaml

# 验证权限
ls -l ~/.media/config.yaml
# 应显示：-rw-------  1 user  staff  ...
```

### 2. Git 隔离

```bash
# .gitignore 规则
config.yaml           # 忽略真实配置
!config.yaml.template # 但允许模板
```

### 3. 多设备同步

```bash
# ✅ 正确做法
git add config.yaml.template
git commit -m "更新配置模板"
git push

# ❌ 错误做法 (严禁)
git add config.yaml  # 绝对禁止！
```

### 4. 备份策略

```bash
# 加密后备份到私有仓库
# 或使用密码管理工具 (1Password/Bitwarden)
# 严禁明文上传到任何公共/共享仓库
```

---

## 📱 调用规范

### 小媒 & 小猎 (子 Agent)

**禁止**:
```bash
# ❌ 硬编码 Token
export TWITTER_TOKEN="abc123..."

# ❌ 私自存储凭证
echo "token=xyz" > ~/.my-secrets
```

**正确做法**:
```bash
# ✅ 从统一配置读取
yq -r '.twitter.cookie' ~/.media/config.yaml

# ✅ 或使用工具自动读取
xreach tweet "URL" --json  # 工具自动读取配置
```

### 墨墨 (首席密钥官)

**职责**:
1. 维护 `config.yaml.template` 模板
2. 配置 `.gitignore` 规则
3. 确保多设备路径一致
4. 定期更新安全策略
5. 更新 SOUL.md / AGENTS.md 行为准则

---

## 🔄 配置流程

### 新设备初始化

```bash
# 1. 创建目录
mkdir -p ~/.media

# 2. 复制模板
cp ~/Documents/openclaw/agents/media/config.yaml.template \
   ~/.media/config.yaml

# 3. 设置权限
chmod 600 ~/.media/config.yaml

# 4. 编辑配置 (填入真实凭证)
nano ~/.media/config.yaml

# 5. 验证配置
yq -r '.twitter.enabled' ~/.media/config.yaml
```

### 更新凭证

```bash
# 1. 编辑配置
nano ~/.media/config.yaml

# 2. 更新 Cookie/Token

# 3. 测试配置
xreach tweet "https://x.com/..." --json
```

---

## ⚠️ 安全警告

### Cookie 风险

- ⚠️ **封号风险**: 使用 Cookie 登录的平台可能检测非正常浏览行为
- ✅ **解决方案**: 使用专用小号，不要用主账号
- ⚠️ **泄露风险**: Cookie 等同于完整登录权限
- ✅ **解决方案**: 文件权限 600，不上传云端

### 备份建议

- ✅ 加密后备份到私有 Git 仓库
- ✅ 使用密码管理工具 (1Password/Bitwarden)
- ❌ 严禁明文上传到任何公共/共享仓库
- ❌ 严禁通过即时通讯工具发送

---

## 📋 检查清单

### 每周检查 (墨墨)

- [ ] 验证文件权限 (600)
- [ ] 检查 Git 忽略规则
- [ ] 确认多设备同步
- [ ] 更新过期 Cookie

### 每月检查 (墨墨)

- [ ] 审查凭证使用情况
- [ ] 更新安全策略
- [ ] 备份配置文件 (加密)
- [ ] 检查 Agent 行为准则

---

## 🖤 责任声明

**墨墨 (Writer Agent)** 作为 Matrix 首席密钥官：
- ✅ 对所有凭证的安全负全责
- ✅ 确保配置在两端 (MBP/Mac-mini) 一致
- ✅ 定期更新安全策略
- ✅ 监督子 Agent 遵守调用规范

**小媒 & 小猎** 作为子 Agent：
- ✅ 遵守调用规范，不私自存储凭证
- ✅ 需要权限时从统一配置读取
- ✅ 发现安全问题立即报告墨墨

---

*统一密钥管理协议生效 - 2026-03-16* 🔐🖤
