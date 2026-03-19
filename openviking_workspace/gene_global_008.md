# Gene Global 008 - 故障恢复与最佳实践
**类型**: 全局 Gene | **版本**: 1.0.0 | **创建时间**: 2026-03-08
---
## 故障恢复流程
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
rm -f ~/.openclaw/gateway.lock
openclaw gateway start --force --allow-unconfigured
*Gene 固化时间：2026-03-08*
