# TOOLS.md - 小媒工具配置

## 🛠️ 全局工具（所有 Agent 共享）

### x-tweet-fetcher - 社交媒体抓取（新增 ⭐）

**安装位置**: `~/.openclaw/tools/x-tweet-fetcher`  
**命令入口**: `fetch-tweet`

**功能**:
- 抓取 Twitter/X 推文（无需登录）
- 搜索微信公众号
- 抓取微博/B站/CSDN

**使用方法**:
```bash
# 抓取推文（基础功能，零依赖）
fetch-tweet --url "https://x.com/user/status/123456"

# 搜索微信公众号文章
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/sogou_wechat.py \
  --keyword "AI Agent" --limit 10 --json

# 抓取中文平台内容
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/fetch_china.py \
  --url "https://weibo.com/..."

# 发现推文（需要 Camofox）
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/x_discover.py \
  --keywords "AI,LLM" --limit 20 --json
```

**输出格式**: JSON
```json
{
  "tweet": {
    "text": "推文内容...",
    "likes": 42,
    "retweets": 8,
    "views": 4152,
    "media": ["图片URL"],
    "article": { "full_text": "长文章内容..." }
  }
}
```

**应用场景**:
- ✅ 获取 Twitter 热点内容用于创作
- ✅ 搜索微信公众号文章
- ✅ 监控竞品社交媒体动态
- ✅ 收集中文平台资讯

---

## 🎨 小媒专属技能

### baoyu-* 系列（9个核心技能）

1. **baoyu-image-gen** - AI 图片生成
2. **baoyu-cover-image** - 封面图生成
3. **baoyu-post-to-wechat** - 公众号发布
4. **baoyu-post-to-x** - X/Twitter 发布
5. **baoyu-xhs-images** - 小红书图片
6. **baoyu-translate** - 翻译
7. **baoyu-format-markdown** - 格式化
8. **baoyu-compress-image** - 图片压缩
9. **baoyu-markdown-to-html** - MD转HTML

### 飞书工具
- feishu-bitable - 多维表格
- feishu-calendar - 日历
- feishu-create-doc - 创建文档
- feishu-fetch-doc - 获取文档
- feishu-im-read - IM 消息读取
- feishu-task - 任务管理

---

*小媒签名：🎨*
