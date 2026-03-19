---
agent: media
category: media
status: stable
date: 2026-03-16
tags:
  - media
  - account
  - config
---

# 平台账号管理

## 账号清单

| 平台 | 账号 | 状态 | Cookie/Token |
|------|------|------|-------------|
| Twitter/X | @xxx | 🟡 待配置 | 需 Cookie |
| 小红书 | @xxx | 🟡 待配置 | 需 Cookie |
| 抖音 | @xxx | 🟡 待配置 | 需 MCP |
| Bilibili | @xxx | 🟡 待配置 | 需 Cookie |
| 微信公众号 | xxx | 🟡 待配置 | 需 Token |

## 配置方式

所有 Token 通过墨墨的 `key-manager` 获取：

```bash
key-manager get twitter cookie
key-manager get xiaohongshu cookie
```

## 安全提醒

⚠️ 所有账号使用专用小号，避免主号风险
