# 小猎专区 - 信息捕手情报库

**创建时间**: 2026-03-16  
**负责人**: 小猎 (Hunter)  
**定位**: 信息获取与整理专家

---

## 📁 目录结构

```
docs/03-小猎专区/
├── README.md              # 本文件
├── 情报档案/              # 情报分类存储
│   ├── 科技动态/          # 最新科技新闻和技术趋势
│   ├── 竞品分析/          # 竞品工具和功能对比
│   ├── 行业报告/          # 深度行业分析报告
│   └── 数据备份/          # 重要数据归档
└── 工具使用/              # 工具文档和最佳实践
    ├── Agent-Reach/       # 多平台数据采集工具
    ├── chrome-cdp/        # Chrome CDP 自动化
    ├── x-tweet-fetcher/   # Twitter/X 抓取工具
    └── web_search/        # 网络搜索最佳实践
```

---

## 🎯 核心职责

1. **信息爬取** - 网页内容获取 (web_fetch/camofox)
2. **网络搜索** - 信息检索 (web_search)
3. **内容整理** - 结构化输出和归档
4. **工具维护** - 工具文档和最佳实践

---

## 🔒 安全规范

- ✅ 所有密钥统一存储于 `~/.media/config.yaml`
- ✅ 禁止硬编码 Token 或 Cookie
- ✅ 通过墨墨提供的接口获取凭证
- ✅ `.gitignore` 已配置，真实配置不入库

---

## 📊 情报档案格式

```yaml
---
agent: hunter
category: tools|news|analysis
status: stable|testing|deprecated
date: YYYY-MM-DD
tags:
  - tag1
  - tag2
---

# 标题

## 来源
## 功能
## 测试结果
## 价值评估
## 下一步
```

---

*🏹 小猎 · 信息捕手 | 专注信息获取和整理*
