# 全局状态 (00_GLOBAL_STATUS)

**最后更新**: 2026-03-11 09:17 AM  
**维护者**: 墨墨

---

## 🎯 核心现状

| 项目 | 状态 |
|------|------|
| **墨墨 Agent** | ✅ 运行中 (qwen3.5-plus) |
| **Gateway** | ✅ 运行中 (PID 89242) |
| **Feishu 连接** | ✅ 已连接 |
| **性能优化** | ✅ 完成 |
| **openclaw-pm v2.1.0** | ✅ 完整采用 |

---

## ⚙️ 关键配置

```
Compaction: ✅ 已启用
  - keepRecentTokens: 12000
  - maxHistoryShare: 0.25
  - reserveTokens: 40000
  - threshold: ~60k (自动触发)

Health Check: ✅ 自动化
  - launchd: 每 5 分钟
  - crontab: 每 30 分钟 (gateway-monitor)
  - crontab: 每天 8:00 AM (morning-briefing)
```

---

## 📋 下一步行动

- [x] openclaw-pm v2.1.0 完整安装
- [ ] 观察 Compaction 效果（1-2 天）
- [ ] 补执行错过的 Cron 任务（3 个）
- [ ] 活跃项目创建 PROJECT.md

---

## 📁 项目索引

| 项目 | 状态 | 文档 |
|------|------|------|
| **config-center** | ✅ 已发布 | - |
| **sandbox** | ✅ 已发布 | - |
| **QMD 记忆系统** | ✅ 优化完成 | - |
| **openclaw-pm v2.1** | ✅ 完整采用 | temp/openclaw-pm-v2.1-plan.md |

---

## 🔧 墨墨临时指令

- 回复风格：精简优先（保持墨墨风格）
- 工具调用：合并 exec 命令
- 重要信息：主动保存到 memory/
- 任务执行：先写 plan.md，再执行

---

## 📊 性能指标

| 指标 | 目标 | 当前 |
|------|------|------|
| Prefill 时间 | <5 秒 | ~3 秒 ✅ |
| 上下文上限 | <60k | 200k (刚 compacted) |
| 内存占用 | <600MB | 待测 |
| 健康检查 | 自动 | ✅ 每 5 分钟 |

---

## 🏥 健康检查摘要 (09:17 AM)

- ✅ Gateway: 运行正常
- ✅ Session Lock: 1 个活跃
- ✅ 飞书连接：已连接
- ✅ 未回复消息：无
- ⚠️ Cron 任务：3 个未执行（待补执行）
- ✅ 磁盘空间：12%

---

*极简版 v2.0 | 字数：~400 字*
