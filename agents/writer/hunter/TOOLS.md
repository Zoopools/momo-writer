# TOOLS.md - 小猎工具配置

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
# 抓取推文
fetch-tweet --url "https://x.com/user/status/123456"

# 搜索微信公众号
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/sogou_wechat.py \
  --keyword "AI Agent" --limit 10 --json

# 抓取中文平台
python3 ~/.openclaw/tools/x-tweet-fetcher/scripts/fetch_china.py \
  --url "https://weibo.com/..."
```

**输出格式**: JSON（结构化数据，易于处理）

**应用场景**:
- ✅ 信息收集与监控
- ✅ 竞品分析
- ✅ 热点追踪
- ✅ 数据抓取

---

## 🎯 小猎专属技能

### 信息抓取
- **web_fetch** - 网页内容获取
- **web_search** - 网络搜索
- **camofox_*** - 浏览器自动化
- **fetch-tweet** - Twitter/X 抓取（全局工具）

### 飞书工具
- feishu-bitable - 多维表格
- feishu-calendar - 日历管理
- feishu-task - 任务管理
- feishu-im-read - 消息读取

### 开发工具
- github - GitHub 操作
- gh-issues - Issue 管理
- clawhub - 技能市场

---

## 🔍 信息抓取最佳实践

### 网页抓取流程
```
1. 评估目标网站
   - 静态页面 → web_fetch
   - 动态内容 → camofox
   - 社交媒体 → fetch-tweet

2. 检查内容长度
   - < 20,000 字符 → 直接处理
   - > 20,000 字符 → 提取核心内容

3. 数据存储
   - 原始数据 → memory/YYYY-MM-DD.md
   - 关键信息 → MEMORY.md
   - 结构化数据 → 飞书表格
```

### 约束提醒
- 🔴 HTML > 20K 字符 → 必须提取核心
- 🔴 严禁直接发送原始代码给大模型
- 🔴 B 站抓取 → 分批处理，每批 ≤50 条

---

*小猎签名：🏹*
