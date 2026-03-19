# ClawRouter 整合方案 - 风险评估与配置预设

**分析时间**: 2026-03-08 14:48  
**分析者**: 墨墨 (Mò)  
**版本**: v1.0 (预设方案)

---

## 📋 整合目标

将 ClawRouter 智能路由能力整合到"OpenClaw 集中配置管理系统"Skill 中，实现：
1. **智能模型路由** - 自动选择最便宜但能处理任务的模型
2. **Token 优化** - 自动压缩，减少 7-40% tokens
3. **响应缓存** - 重复请求 100% 免费
4. **成本监控** - 实时追踪 API 花费

**预期效果**: 节省 **74% API 成本** (基于 ClawRouter 官方数据)

---

## 🔍 影响分析

### 一、配置修改范围

#### ✅ 需要新增的配置

| 配置文件 | 新增内容 | 影响范围 |
|---------|---------|---------|
| `core.json` | ClawRouter 路由配置、缓存配置 | 全局 |
| `agents/writer.json` | 模型路由策略、成本阈值 | 仅协调员 Agent |
| `agents/media.json` | 模型路由策略、成本阈值 | 仅创意专家 Agent |
| `skills/baoyu.json` | 图片生成模型路由 | 仅 baoyu 技能 |

#### ⚠️ 需要修改的配置

| 配置文件 | 修改内容 | 影响范围 | 风险等级 |
|---------|---------|---------|---------|
| `openclaw.json` | 添加 ClawRouter proxy 配置 | 全局 | 🟡 中 |
| `channels/feishu.json` | 无需修改 | - | 🟢 无 |
| 现有脚本 | 无需修改 | - | 🟢 无 |

---

## 📦 预设配置方案

### 方案 A: 零风险 - 纯新增配置模板 (推荐)

**策略**: 不修改现有配置，只增加 ClawRouter 配置模板

**新增文件**:
```
~/.openclaw/config/
└── clawrouter.json          # ClawRouter 配置模板
```

**内容预设**:
```json
{
  "enabled": true,
  "proxy": {
    "endpoint": "http://localhost:8080/v1",
    "api_key": "{{ClawRouter API Key}}",
    "timeout_ms": 30000
  },
  "routing": {
    "strategy": "cost_optimized",
    "dimensions": 14,
    "fallback_chain": [
      "anthropic/claude-sonnet-4",
      "zhipu/glm-4",
      "deepseek/deepseek-chat"
    ]
  },
  "compression": {
    "enabled": true,
    "threshold_kb": 180,
    "observation_compression": true,
    "max_compression_ratio": 0.97
  },
  "cache": {
    "enabled": true,
    "ttl_minutes": 10,
    "deduplication": true,
    "max_cache_size_mb": 500
  },
  "monitoring": {
    "enabled": true,
    "track_cost": true,
    "track_tokens": true,
    "alert_threshold_usd": 10
  }
}
```

**优点**:
- ✅ 零风险 - 不影响现有配置
- ✅ 可选安装 - 用户按需启用
- ✅ 向后兼容 - v1.0.0 用户无缝升级

**缺点**:
- ⚠️ 需要手动启用 ClawRouter
- ⚠️ 配置分散在两个文件

---

### 方案 B: 中等风险 - 修改 core.json (需测试)

**策略**: 在 core.json 中集成 ClawRouter 配置

**修改内容**:
```json
{
  "device_id": "{{设备 ID}}",
  "api_base": "https://api.openclaw.ai",
  "log_level": "info",
  
  // 新增 ClawRouter 配置
  "clawrouter": {
    "enabled": false,  // 默认关闭，用户手动启用
    "proxy_endpoint": "http://localhost:8080/v1",
    "api_key": "{{ClawRouter API Key}}",
    "routing_strategy": "cost_optimized",
    "compression_enabled": true,
    "cache_enabled": true,
    "cache_ttl_minutes": 10
  },
  
  "gateway_port": 18789,
  "webui_port": 3000
}
```

**优点**:
- ✅ 配置集中 - 所有核心配置在一个文件
- ✅ 易于管理 - 单一数据源

**缺点**:
- ⚠️ 需要修改现有配置结构
- ⚠️ 需要测试兼容性
- ⚠️ v1.0.0 用户升级需要手动合并

---

### 方案 C: 高风险 - 修改模型配置 (不推荐)

**策略**: 在每个 Agent 的 model 配置中直接集成 ClawRouter

**修改示例** (`agents/writer.json`):
```json
{
  "name": "{{协调员 Agent 名称}}",
  "role": "coordinator",
  "agent_id": "writer",
  "workspace": "{{用户主目录}}/Documents/openclaw/agents/writer",
  
  // 修改前
  "model": {
    "primary": "bailian/qwen3.5-plus"
  },
  
  // 修改后 (方案 C)
  "model": {
    "provider": "clawrouter",
    "primary": "anthropic/claude-sonnet-4",
    "routing": {
      "enabled": true,
      "strategy": "cost_optimized",
      "fallback_models": [
        "zhipu/glm-4",
        "deepseek/deepseek-chat"
      ]
    },
    "compression": {
      "enabled": true,
      "threshold_kb": 180
    }
  }
}
```

**优点**:
- ✅ 每个 Agent 独立控制路由策略
- ✅ 灵活性最高

**缺点**:
- ❌ 配置复杂度高
- ❌ 需要大量测试
- ❌ 破坏现有配置结构
- ❌ 不建议采用

---

## ⚠️ 风险评估

### 风险矩阵

| 风险项 | 可能性 | 影响程度 | 风险等级 | 缓解措施 |
|-------|--------|---------|---------|---------|
| 配置不兼容 | 低 | 高 | 🟡 中 | 采用方案 A (纯新增) |
| ClawRouter 安装失败 | 中 | 中 | 🟡 中 | 提供详细安装指南 |
| 路由策略错误 | 低 | 高 | 🟡 中 | 默认关闭，用户手动启用 |
| API Key 泄露 | 低 | 高 | 🟡 中 | 占位符脱敏 + 安全提醒 |
| 缓存一致性问题 | 中 | 中 | 🟡 中 | 提供清理缓存命令 |
| 成本监控不准确 | 低 | 低 | 🟢 低 | 标注"仅供参考" |

### 关键风险点

#### 1. ClawRouter 安装依赖
**风险**: 用户需要额外安装 ClawRouter proxy
**缓解**:
- 提供一键安装脚本
- 提供 Docker 部署方案
- 明确标注"可选功能"

#### 2. 配置冲突
**风险**: ClawRouter 配置与现有配置冲突
**缓解**:
- 采用方案 A (独立配置文件)
- 配置项加前缀 (`clawrouter.`)
- 提供配置验证脚本

#### 3. 模型路由错误
**风险**: 智能路由选择了错误的模型
**缓解**:
- 默认使用保守策略
- 提供手动覆盖选项
- 记录路由决策日志

---

## 📋 推荐实施方案

### 阶段 1: 零风险整合 (本周)

**目标**: 新增 ClawRouter 配置模板，不修改现有配置

**步骤**:
1. ✅ 新增 `clawrouter.json` 配置模板
2. ✅ 新增 ClawRouter 安装指南
3. ✅ 新增成本监控模板
4. ✅ 更新 Skill 说明文档
5. ✅ 发布 v1.2.0

**影响**:
- 现有用户：无影响
- 新用户：可选择性启用
- 配置修改：仅新增文件

---

### 阶段 2: 深度整合 (下周，需测试)

**目标**: 将 ClawRouter 配置集成到 core.json

**步骤**:
1. ⏳ 测试 ClawRouter + OpenClaw 兼容性
2. ⏳ 修改 core.json 配置结构
3. ⏳ 提供迁移脚本 (v1.0.0 → v1.2.0)
4. ⏳ 更新文档和示例
5. ⏳ 发布 v1.3.0

**影响**:
- 现有用户：需要运行迁移脚本
- 新用户：开箱即用
- 配置修改：core.json 结构变化

---

### 阶段 3: 优化增强 (观察后)

**目标**: 增加高级功能

**功能**:
- ⏳ 智能路由策略调优
- ⏳ 成本分析和报告
- ⏳ 自动预算控制
- ⏳ 多模型负载均衡

---

## 📦 预设配置模板

### 1. clawrouter.json (新增)

```json
{
  "_version": "1.0.0",
  "_description": "ClawRouter 配置模板 - 节省 74% API 成本",
  "_author": "墨墨 (Mò)",
  
  "enabled": false,
  
  "proxy": {
    "endpoint": "http://localhost:8080/v1",
    "api_key": "{{ClawRouter API Key}}",
    "timeout_ms": 30000,
    "retry_count": 3
  },
  
  "routing": {
    "strategy": "cost_optimized",
    "dimensions": 14,
    "fallback_chain": [
      "anthropic/claude-sonnet-4",
      "zhipu/glm-4",
      "deepseek/deepseek-chat",
      "openai/gpt-4o-mini"
    ],
    "claude_percentage": 23
  },
  
  "compression": {
    "enabled": true,
    "threshold_kb": 180,
    "observation_compression": true,
    "max_compression_ratio": 0.97,
    "expected_savings": "7-15%"
  },
  
  "cache": {
    "enabled": true,
    "ttl_minutes": 10,
    "deduplication": true,
    "max_cache_size_mb": 500,
    "expected_savings": "10-20%"
  },
  
  "monitoring": {
    "enabled": true,
    "track_cost": true,
    "track_tokens": true,
    "alert_threshold_usd": 10,
    "report_frequency": "daily"
  },
  
  "_security": {
    "note": "API Key 请妥善保管，不要上传到公开仓库",
    "gitignore": "config/clawrouter.json"
  }
}
```

---

### 2. ClawRouter 安装指南 (新增)

```markdown
# ClawRouter 安装指南

## 方式 1: 一键安装 (推荐)

```bash
curl -fsSL https://blockrun.ai/ClawRouter-update | bash
openclaw gateway restart
```

## 方式 2: Docker 部署

```bash
docker run -d \
  -p 8080:8080 \
  -v ~/.clawrouter:/app/data \
  --name clawrouter \
  blockrun/clawrouter:latest
```

## 方式 3: 源码安装

```bash
git clone https://github.com/blockrunai/ClawRouter.git
cd ClawRouter
npm install
npm start
```

## 验证安装

```bash
curl http://localhost:8080/health
# 应返回：{"status": "ok"}
```

## 充值钱包

```bash
# 打印钱包地址
clawrouter wallet address

# 充值 USDC (Base 或 Solana 链)
# $5 足够数千次请求
```

## 成本对比

安装 ClawRouter 前后对比：

| 指标 | 安装前 | 安装后 | 节省 |
|------|--------|--------|------|
| 月 API 成本 | $450 | $117 | 74% |
| Claude 使用率 | 100% | 23% | 77% |
| 平均响应时间 | 2.3s | 1.8s | 22% |

数据来源：ClawRouter 官方 (2026-03-08)
```

---

### 3. 成本监控模板 (新增)

```markdown
# API 成本监控

## 本月概览

| 指标 | 数值 | 目标 |
|------|------|------|
| 总成本 | $0.00 | <$50 |
| 总请求数 | 0 | - |
| 平均成本/请求 | $0.00 | <$0.01 |
| Claude 使用率 | 0% | <30% |

## 每日成本

| 日期 | 成本 | 请求数 | Claude% |
|------|------|--------|---------|
| 2026-03-08 | $0.00 | 0 | 0% |

## 优化建议

- [ ] 启用 ClawRouter 智能路由
- [ ] 开启响应缓存
- [ ] 设置预算告警
```

---

## 🎯 发布计划

### v1.2.0 (本周)

**更新内容**:
- ✅ 新增 `clawrouter.json` 配置模板
- ✅ 新增 ClawRouter 安装指南
- ✅ 新增成本监控模板
- ✅ 更新 Skill 说明 (增加成本优化章节)
- ✅ 更新贡献家评分报告

**发布平台**:
- 水产市场
- ClawHub
- GitHub

**预计评分**: 8.7-9.2/10 (v1.1.0 为 8.5-9.0)

---

### v1.3.0 (下周，需测试)

**更新内容**:
- ⏳ 集成到 core.json
- ⏳ 提供迁移脚本
- ⏳ 深度测试报告

**前提条件**:
- ClawRouter 兼容性测试通过
- 至少 5 个用户反馈正面

---

## 🖤 墨墨的建议

**哥哥，墨墨建议采用"阶段 1: 零风险整合"方案！**

**理由**:
1. ✅ **零风险** - 不影响现有配置
2. ✅ **快速发布** - 今天就能发布 v1.2.0
3. ✅ **用户选择** - 按需启用，不强制
4. ✅ **向后兼容** - v1.0.0/v1.1.0 用户无缝升级

**执行步骤**:
1. 创建 `clawrouter.json` 配置模板
2. 创建 ClawRouter 安装指南
3. 创建成本监控模板
4. 更新 SKILL.md 说明文档
5. 打包发布 v1.2.0

**时间预估**: 30-40 分钟

---

**哥哥，要立即执行吗？还是再看看其他方案？** 😊🖤
