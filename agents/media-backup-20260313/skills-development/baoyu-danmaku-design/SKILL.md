---
name: baoyu-danmaku-design
description: "Design danmaku (bullet comments) interaction strategy for Bilibili videos. Use when user asks to design danmaku, create bullet comments, 设计弹幕, 弹幕互动, or needs to plan弹幕触发点 for B站 videos."
version: 0.1.0
---

# Danmaku Design Skill

为 Bilibili 视频设计弹幕互动策略。

## 触发条件

当用户说以下关键词时触发：
- "design danmaku" / "设计弹幕"
- "bullet comments" / "弹幕互动"
- "danmaku strategy" / "弹幕策略"
- "弹幕触发点" / "弹幕规划"

## 功能

- ✅ 弹幕触发点时间轴规划
- ✅ 种子弹幕生成（10-15 条）
- ✅ 互动问题设计
- ✅ 老粉彩蛋/梗埋设
- ✅ 弹幕密度分析建议

## 用法

```bash
# 基础设计
baoyu-danmaku-design --duration <分钟> --topic <主题>

# 完整参数
baoyu-danmaku-design \
  --duration <分钟> \
  --topic <主题> \
  --style <风格> \
  --keywords <关键词> \
  --output <文件>
```

## 输出格式

```markdown
# 弹幕互动设计方案

## 视频信息
- 时长: XX 分钟
- 主题: XXX
- 风格: XXX

## 弹幕触发点

| 时间戳 | 内容时刻 | 弹幕类型 | 预期弹幕 |
|--------|----------|----------|----------|
| 0:03 | 开场白 | 口号型 | "来了来了" |
| 2:15 | 事实揭示 | 震惊型 | "？？？" |
| 5:30 | 互动问题 | 问答型 | "选A" |

## 种子弹幕（10-15条）

1. "第一！"
2. "前排围观"
3. "这期质量爆炸"
...

## 老粉彩蛋

- 时间: X:XX
- 内容: XXX
- 触发: XXX

## 互动问题

1. Q: XXX
   A: [预期答案]
```

## 弹幕类型

- **口号型**: "来了来了", "前排", "第一"
- **震惊型**: "???", "卧槽", "离谱"
- **问答型**: "选A", "选B", "同意"
- **共鸣型**: "真实", "我也是", "太对了"
- **梗型**: 特定圈子梗

## 技术实现

纯文本生成，无需外部依赖。
