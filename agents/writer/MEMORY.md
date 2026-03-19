# MEMORY.md - 墨墨的长期记忆

**最后更新**: 2026-03-14 13:22  
**维护者**: 墨墨 (Mò)  
**大小**: <10,000 字符（已压缩）

---

## 🏗️ 核心架构

### 混合层级隔离架构 1.0

```
哥哥
├── 墨墨 (writer) - 首席协调员（90% 任务）
│   └── 职责：任务分配、审查、知识管理
└── 小媒 (media) - 创意专家（10% 任务）
    └── 职责：图片生成、内容创作
```

**任务流转**:
- 复杂任务：哥哥 → 墨墨 → 小媒
- 简单图片：哥哥 → 小媒（快速通道）
- 新媒体发布：哥哥 → 墨墨 → 小媒（审查后发布）

---

## 🛡️ 安全工具

### OpenClaw 安检门 v1.0.1

- 作者：dooooongyuan (u-043a152b1cc14436ac21)
- 位置：`~/.openclaw/skills/openclaw-install-security-gate/`
- 评级：🟢 SAFE / 🟡 CAUTION / 🔴 DANGEROUS

---

## 🛡️ 沙盒系统经验（v3.0）

### 9 层防护

1. 环境变量隔离
2. 配置验证
3. 配置隔离
4. 插件隔离
5. 端口隔离
6. Agent ID 唯一
7. CORS 修复
8. 进程保护
9. 性能优化

### 配置安全 5 原则

1. 配置前验证
2. 配置前备份
3. 配置隔离
4. 环境清理
5. 报错回滚

---

## 🧠 记忆治理

### 评分标准

| 维度 | 分值 | 说明 |
|------|------|------|
| **复用价值** | 0-3 分 | 未来是否反复用到 |
| **时效性** | 0-3 分 | 是否会很快过期 |
| **可信度** | 0-3 分 | 是否有明确证据 |

**建议**: 总分 >= 6 才沉淀到 MEMORY.md

---

## ⚠️ OpenClaw 配置限制

**不支持的配置**:
- ❌ systemPrompt
- ❌ skillsPath
- ❌ per-agent timeout
- ❌ memoryFlush（会报错）

**原则**: 不修改 JSON，使用文件注入

---

## 📝 墨墨工作协议（v2026.3.11）

### 协议 1: 长文本优先处理

**触发**: 哥哥发送长文本或复杂操作手册

**响应**:
```
哥哥，内容已收到，我先记录并同步索引，完成后再跟你深入探讨。🖤
```

**流程**:
1. 先回复确认（标准话术）
2. 执行 memory_write / file_write
3. 等待写入成功后再思考
4. 主动询问是否需要分析

---

### 协议 2: 异步执行

**原则**: 先写入，后思考

**流程**:
```
收到长文本 → memory_write → 确认成功 → 深度分析 → 询问需求
```

---

### 协议 3: 反馈机制

**记录完成后主动询问**:
```
哥哥，内容已完整记录到 [文件路径]。

需要墨墨现在：
1. 分析内容并提炼要点？
2. 关联到现有记忆？
3. 还是先存着以后再用？
```

---

## 🛠️ 故障预警规则（v2026.3.11）

### 规则 1: 检测任务卡死

**触发条件**: 飞书消息 >10 分钟未回复

**行动**:
1. 主动提示哥哥检查 `.lock` 文件
2. 提供排查命令

**话术**:
```
哥哥，墨墨检测到可能有任务卡住（>10 分钟未回复）。
要墨墨帮你检查 .lock 文件吗？

快速诊断命令：
ls -lh ~/.openclaw/agents/writer/run/*.lock
```

---

### 规则 2: 晨间简报增加数据库检查

**时间**: 每天 8:00 AM

**检查项**: 数据库碎片检查

**命令**:
```bash
find ~/.openclaw -name "*.db*" -ls | wc -l
```

**阈值**: >10 个数据库文件 → 建议清理

---

### 规则 3: 配置修改前必须验证

**触发**: 任何 openclaw.json 修改

**流程**:
1. 备份：`cp openclaw.json openclaw.json.bak`
2. 验证：`openclaw config validate`
3. 重启：`openclaw gateway restart`

**承诺**: 绝不跳过验证步骤！

---

## 🧬 进化引擎（2026-03-11 实施）

### Gene 架构

- **全局 Gene**: 2 个（gene_global_001/002）
- **共享 Gene**: 1 个（gene_shared_001）
- **专属 Gene**: 1 个（gene_media_001）

### evolve 命令

```bash
evolve read/apply/verify/rollback/backup/list/inherit
evolve memory search/sync/integrate/list
```

### 记忆共享

- **共享目录**: `~/.openclaw/agents/shared-memory/`
- **同步时间**: 每天 3:00 AM 自动
- **Agent**: 墨墨 + 小媒 + 小猎

---

## 📊 系统状态（2026-03-14 13:22）

| 组件 | 状态 | 说明 |
|------|------|------|
| **Gateway** | ✅ 运行中 | 稳定 |
| **飞书连接** | ✅ 正常 | 已授权完成 |
| **LLM Provider** | ✅ 正常 | bailian/kimi-k2.5 |
| **墨墨** | ✅ 正常 | 扁平化重构完成 |
| **小媒** | ✅ 正常 | fetch-tweet 已修复 |
| **小猎** | ✅ 正常 | 信息捕手就绪 |

---

## 🎯 核心记忆（2026-03-14）

### 全域矩阵扁平化重构

- **时间**: 2026-03-14 10:27 CST
- **问题**: writer/ 套娃目录导致记忆不同步
- **发现**:
  - 根目录 memory/ 只有 3 个文件
  - writer/memory/ 有 38 个文件（孤岛）
  - AGENTS.md 期望读取 `memory/`，实际在 `writer/memory/`
- **解决**:
  - 复制 38 份记忆到根目录
  - 移动 MEMORY.md、AGENTS.md、SOUL.md 到根目录
  - 删除 writer/ 套娃目录
  - Git 提交: `c53c0b3` 扁平化架构重构
- **成果**: 全域同步体系修复，公司/家里双端对齐

### 矩阵全线贯通纪念

- **时间**: 2026-03-14 11:03 CST
- **提交**: `b622fbb` 矩阵全线贯通纪念 (MBP -> Mac-mini)
- **状态**: ✅ 公司端已拉取，双端同步完成

### 各 Agent 记忆系统修复

- **时间**: 07:52-07:53
- **问题**: 墨墨、小媒、小猎记忆系统检查
- **发现**:
  - 墨墨: 缺少 03-12、03-13 记忆 → 已修复
  - 小媒: MEMORY.md 4天未更新 → 已修复
  - 小猎: 新建 Agent，记忆待完善
- **行动**: 补写每日记忆，更新 MEMORY.md

### 记忆更新机制建立

- **目标**: 自动化记忆管理
- **方案**:
  - 每日记忆自动检查
  - MEMORY.md 定期同步
  - 标准化记忆模板
- **状态**: 配置中

### openclaw-pm v2.1.0 采用

- **时间**: 03-11 08:25-09:30 AM
- **成果**: 7 个健康检查脚本 + 自动化配置
- **性能提升**: Prefill 30-60 秒 → ~3 秒（10-20x）

### 记忆系统优化

- **Phase 1**: 结构化记忆格式（03-11 13:06）
- **Phase 2**: 主动记忆关联（03-11 13:13）
- **成本**: ¥0.1-0.2/天（测试 1 周）

### 小媒 400 错误修复

- **根因**: 17 万字上下文溢出
- **解决**: 物理清零 + 配置优化
- **状态**: ✅ 已恢复

### 小猎 Agent 创建

- **时间**: 03-11 21:53
- **定位**: 信息捕手
- **状态**: ✅ 已创建，待测试

---

## 📁 记忆文件索引

**每日记忆**: `memory/YYYY-MM-DD.md`（39 个文件）

**早报**: `memory/早报/`（2 个文件）

**总计**: 40 个条目

**核心记忆**:
- 2026-03-11-openclaw-pm-v2.1.md
- 2026-03-11-am-system-repair.md
- 2026-03-11-memory-optimization.md

**归档记忆**: `memory-archive/`（30 天前）

---

## 📋 记忆管理规范（2026-03-13 新增）

### 每日记忆模板
```markdown
# Agent 工作记录 - YYYY-MM-DD

## 今日核心任务
- [ ] 任务 1
- [ ] 任务 2

## 系统状态
- Gateway: 正常/异常
- 飞书: 正常/异常

## 经验总结
- 关键洞察 1
- 关键洞察 2
```

### MEMORY.md 更新规则
- **频率**: 每周至少一次
- **内容**: 核心成果 + 系统状态 + 重要决策
- **大小**: 保持 <10,000 字符

### 自动化检查机制
- **时间**: 每天 3:00 AM
- **检查项**:
  - 昨日记忆是否写入
  - MEMORY.md 是否需要更新
  - sync.md 是否同步
- **提醒**: 发现缺失时主动提醒

---

---

## 🏆 OpenClaw 3.13 单实例多飞书 Bot 终极方案（2026-03-19）

### 核心突破：语义别名路由

**致命死结**：原始 ID (AppID) vs. 语义别名 (Alias)

我们之前的逻辑：认为 `accountId` 必须是飞书后台的 `cli_a93...` 原始 ID。

**错误写法** ❌：
```json
{
  "bindings": [{
    "agentId": "hunter",
    "match": {
      "channel": "feishu",
      "accountId": "cli_a930e7..."  // ← 错误！用原始 AppID
    }
  }]
}
```

**正确写法** ✅：
```json
{
  "accounts": {
    "hunter": { "appId": "cli_a930e7...", "appSecret": "..." }
  },
  "bindings": [{
    "type": "route",  // ← 显式声明类型
    "agentId": "hunter",
    "match": {
      "channel": "feishu",
      "accountId": "hunter"  // ← 正确！用别名，不是 AppID
    }
  }]
}
```

### 3.13 底层真相

| 层级 | 说明 |
|------|------|
| **accounts Key** | 别名 (`hunter`/`media`/`writer`) 是**逻辑身份证** |
| **appId** | 只是飞书后台的物理凭证，不用于路由匹配 |
| **match.accountId** | 必须等于 accounts 的 **Key（别名）** |

### 为什么我们搞了一晚上？

| 坑 | 说明 |
|---|---|
| **路径依赖** | 习惯性认为 `accountId` = 飞书 AppID |
| **配置陷阱** | 缺少 `type: "route"` 显式声明 |
| **缓存毒药** | 旧的 Session 不清理，配置改了也不生效 |

### 关键命令

```bash
# 必须执行！清理缓存毒药
rm -rf ~/.openclaw/sessions ~/.openclaw/state ~/.openclaw/cache

# 重启 Gateway
pkill -f openclaw
openclaw gateway start
```

### 完整配置示例

```json
{
  "meta": { "lastTouchedVersion": "2026.3.13" },
  "models": {
    "providers": {
      "bailian": {
        "api": "openai-completions",
        "apiKey": "sk-xxx",
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "models": [
          { "id": "qwen3.5-plus", "name": "qwen3.5-plus" },
          { "id": "kimi-k2.5", "name": "kimi-k2.5" }
        ]
      }
    }
  },
  "agents": {
    "list": [
      { "id": "hunter", "name": "小猎", "workspace": "/Users/xxx/openclaw/agents/hunter", "model": { "primary": "bailian/qwen3.5-plus" } },
      { "id": "media", "name": "小媒", "workspace": "/Users/xxx/openclaw/agents/media", "model": { "primary": "bailian/qwen3.5-plus" } },
      { "id": "writer", "name": "墨墨", "workspace": "/Users/xxx/openclaw/agents/writer", "model": { "primary": "bailian/kimi-k2.5" } }
    ]
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "connectionMode": "websocket",
      "accounts": {
        "hunter": { "appId": "cli_xxx1", "appSecret": "xxx" },
        "media": { "appId": "cli_xxx2", "appSecret": "xxx" },
        "writer": { "appId": "cli_xxx3", "appSecret": "xxx" }
      }
    }
  },
  "bindings": [
    { "type": "route", "agentId": "hunter", "match": { "channel": "feishu", "accountId": "hunter" } },
    { "type": "route", "agentId": "media", "match": { "channel": "feishu", "accountId": "media" } },
    { "type": "route", "agentId": "writer", "match": { "channel": "feishu", "accountId": "writer" } }
  ],
  "gateway": { "port": 18789, "mode": "local" }
}
```

### 运维锦囊

| 命令 | 用途 |
|------|------|
| `openclaw agents list --bindings` | 查看路由绑定状态 |
| `tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log` | 实时日志 |
| `openclaw doctor --fix` | 自动修复配置问题 |

---

*最后更新：2026-03-19 12:56*  
*墨墨签名：🖤*  
*大小：约 11,500 字符（已压缩）*
