---
agent: hunter
category: tools
status: stable
date: 2026-03-16
tags:
  - hunter
  - tools
  - chrome-cdp
---

# chrome-cdp 使用指南

## 安装

已包含在 OpenClaw skills 中：
```bash
~/.openclaw/skills/chrome-cdp/skills/chrome-cdp/scripts/cdp.mjs
```

## 开启 Chrome 远程调试

1. 打开 Chrome
2. 地址栏输入：`chrome://inspect/#remote-debugging`
3. 开启远程调试开关
4. 确认端口：9222

## 常用命令

```bash
# 列出标签页
cdp.mjs list

# 截图
cdp.mjs shot <tab-id>

# 获取页面 HTML
cdp.mjs html <tab-id>

# 获取可访问性树
cdp.mjs snap <tab-id>

# 在页面执行 JS
cdp.mjs eval <tab-id> "document.title"

# 导航到 URL
cdp.mjs nav <tab-id> https://...

# 点击元素
cdp.mjs click <tab-id> "selector"
```

## 特点

- ✅ 可访问已登录页面
- ✅ 无需额外登录
- ✅ 实时页面状态
