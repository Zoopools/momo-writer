---
agent: hunter
category: tools
status: stable
date: 2026-03-16
tags:
  - hunter
  - tools
  - agent-reach
---

# Agent-Reach 使用指南

## 安装

```bash
git clone https://github.com/Panniantong/Agent-Reach.git \
  ~/.openclaw/tools/agent-reach
```

## 支持平台

- Twitter/X
- Reddit
- YouTube
- GitHub
- Bilibili
- 小红书

## Bilibili 字幕提取（示例）

```bash
# 安装 yt-dlp
pip install yt-dlp

# 配置 Cookie（通过墨墨 key-manager）
key-manager get bilibili cookie

# 提取字幕
yt-dlp --cookies ~/.media/bilibili_cookies.txt \
  --write-subs --sub-langs ai-zh \
  "https://www.bilibili.com/video/BV1fywHzUE9P/"
```

## 状态

| 功能 | 状态 |
|------|------|
| 安装 | ✅ 完成 |
| Bilibili 测试 | ✅ 成功 |
| Cookie 配置 | ✅ 完成 |
| 字幕提取 | ✅ 可用 |
