# 小媒技能加载指南

## ⚠️ 重要：不要一次性读取所有技能！

**baoyu-skills 总计**: 203,610 字符（超过 169,984 限制）

---

## ✅ 正确的技能加载方式

### 方式 1: 按需加载（推荐）

```
接到任务 → 识别需要的技能 → 只读取该技能的 SKILL.md
```

**示例**:
- 任务："生成小红书封面图" → 读取 `baoyu-cover-image/SKILL.md`
- 任务："写微博文案" → 读取 `baoyu-post-to-weibo/SKILL.md`
- 任务："翻译文章" → 读取 `baoyu-translate/SKILL.md`

---

### 方式 2: 技能索引（快速查找）

**17 个 baoyu-skills 列表**:

| 技能 | 大小 | 用途 |
|------|------|------|
| baoyu-image-gen | ~8 KB | 通用图片生成 |
| baoyu-xhs-images | ~22 KB | 小红书信息图 |
| baoyu-cover-image | ~9 KB | 封面图生成 |
| baoyu-infographic | ~12 KB | 信息图 |
| baoyu-slide-deck | ~23 KB | 幻灯片 |
| baoyu-comic | ~13 KB | 知识漫画 |
| baoyu-article-illustrator | ~16 KB | 文章配图 |
| baoyu-compress-image | ~5 KB | 图片压缩 |
| baoyu-format-markdown | ~16 KB | Markdown 排版 |
| baoyu-markdown-to-html | ~11 KB | HTML 转换 |
| baoyu-post-to-wechat | ~16 KB | 公众号发布 |
| baoyu-post-to-weibo | ~8 KB | 微博发布 |
| baoyu-post-to-x | ~8 KB | X/Twitter 发布 |
| baoyu-translate | ~16 KB | 翻译 |
| baoyu-url-to-markdown | ~11 KB | 网页转 Markdown |
| baoyu-danger-gemini-web | ~12 KB | Gemini 生成 |
| baoyu-danger-x-to-markdown | ~7 KB | X 转 Markdown |

**总计**: 203 KB（不能一次性读取！）

---

## 🛡️ 防护机制

### 每次会话读取上限

**建议读取**:
- SOUL.md (4.5 KB)
- USER.md (0.5 KB)
- AGENTS.md (8.6 KB)
- memory/*.md (24.7 KB)
- **单个技能 SKILL.md** (最多 23 KB)

**总计**: 约 61 KB（安全范围内）

---

## 🚨 错误示例

```bash
# ❌ 错误：一次性读取所有技能
cat skills/baoyu-skills/skills/*/SKILL.md

# 结果：203,610 字符 → 超长报错！
```

## ✅ 正确示例

```bash
# ✅ 正确：按需读取
cat skills/baoyu-skills/skills/baoyu-cover-image/SKILL.md

# 结果：9,572 字符 → 安全！
```

---

*创建时间：2026-03-10 | 目的：防止技能文件超长报错*
