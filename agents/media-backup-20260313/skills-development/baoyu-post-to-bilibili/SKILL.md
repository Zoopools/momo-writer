---
name: baoyu-post-to-bilibili
description: "Post videos and content to Bilibili (哔哩哔哩) platform. Use when user asks to post to Bilibili, upload video to B站, 发布到B站, or needs to publish content on bilibili.com. Supports video upload, cover image, title optimization, tags, and scheduling."
version: 0.1.0
---

# Bilibili Post Skill

发布内容到哔哩哔哩 (Bilibili) 平台。

## 触发条件

当用户说以下关键词时触发：
- "post to bilibili" / "发布到B站"
- "upload to bilibili" / "上传到B站"
- "bilibili upload" / "B站发布"
- "发B站" / "投稿B站"

## 功能

### 核心功能
- ✅ 视频上传（支持分 P）
- ✅ 封面图设置
- ✅ 标题/标签/描述优化
- ✅ 分区选择
- ✅ 定时发布

### 待开发
- ⏳ 投稿后数据追踪
- ⏳ 弹幕预设

## 用法

```bash
# 基础发布
baoyu-post-to-bilibili --video <path> --title <title>

# 完整参数
baoyu-post-to-bilibili \
  --video <path> \
  --title <title> \
  --description <desc> \
  --tags <tag1,tag2> \
  --cover <image_path> \
  --partition <分区> \
  --schedule <时间>
```

## 分区列表

- 动画 (anime)
- 游戏 (game)
- 知识 (knowledge)
- 科技 (tech)
- 生活 (life)
- 美食 (food)
- 影视 (movie)

## 技术实现

采用 Chrome CDP 方案，参考 `baoyu-post-to-wechat` 实现。

## 依赖

- Chrome 浏览器
- Playwright 或 Selenium
- B站账号登录状态
