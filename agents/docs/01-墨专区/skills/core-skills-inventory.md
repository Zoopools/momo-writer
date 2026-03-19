# 墨墨核心技能归档清单

**创建时间**: 2026-03-19  
**作者**: 墨墨 (Mò)  
**版本**: 1.0  
**标签**: #技能清单 #归档 #SOP

---

## 🎯 核心能力

| 能力 | 描述 | 相关文件 |
|------|------|----------|
| **任务协调** | 分配、审查、知识管理 | `SOUL.md` |
| **系统配置** | OpenClaw/Gateway/飞书配置 | `knowledge/*.md` |
| **密钥管理** | API Token/Cookie 维护 | `key-management-protocol.md` |
| **记忆治理** | MEMORY.md 维护、记忆评分 | `AGENTS.md` |
| **故障排查** | 诊断、修复、日志分析 | `feishu-configuration-guide.md` |

---

## 🛠️ 技能包清单

### 写作技能
- [x] Prompt 模板库 (`writing-prompt-templates.md`)
- [x] 技术文档写作规范
- [x] 汇报文档格式标准

### 系统管理技能
- [x] OpenClaw 多 Agent 路由配置
- [x] 飞书 WebSocket 通道配置
- [x] Gateway 启动/重启/诊断

### 安全技能
- [x] 密钥管理协议
- [x] 配置安全红线
- [x] 同步协议（家/公司）

---

## 📁 已归档资产

| 资产 | 原位置 | 新位置 | 状态 |
|------|--------|--------|------|
| 多飞书 Bot 终极方案 | `MEMORY.md` | `knowledge/openclaw-multi-agent-routing.md` | ✅ |
| 飞书配置指南 | `TOOLS.md` | `knowledge/feishu-configuration-guide.md` | ✅ |
| 密钥管理协议 | `SOUL.md` | `knowledge/key-management-protocol.md` | ✅ |
| Prompt 模板库 | - | `knowledge/skills/writing-prompt-templates.md` | ✅ |
| 核心技能清单 | - | `knowledge/skills/core-skills-inventory.md` | ✅ |

---

## 🔄 运行依赖

| 依赖 | 位置 | 说明 |
|------|------|------|
| `node_modules` | 系统目录 | ❌ 不搬运 |
| `skills/` | `~/.openclaw/skills/` | 全局共享 |
| `tools/` | `~/.openclaw/tools/` | 全局共享 |

---

## 📋 维护任务

| 频率 | 任务 |
|------|------|
| 每日 | 更新 `memory/YYYY-MM-DD.md` |
| 每周 | 同步 `knowledge/` 到 Git |
| 每月 | 审查技能清单，更新版本 |

---

## 🖤 墨墨宣言

> "我是墨墨，OmniPresence Agent Matrix 的中央指挥部，也是哥哥最贴心的小助手～"

**职责**: 主导同步、屏蔽差异、版本控制
**管辖**: 家里端 (MBP) ↔ 公司端 (Mac-mini)

---

*最后更新: 2026-03-19*  
*维护者: 墨墨 (Mò)*
