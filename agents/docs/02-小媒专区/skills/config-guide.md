# 小媒技能配置指南

## 🔑 API 密钥配置

**⚠️ 重要：密钥文件不在 skills/ 目录下，避免 Git 同步泄露！**

### 配置位置

| 配置类型 | 文件路径 | 说明 |
|---------|---------|------|
| **项目级配置** | `/.baoyu-skills/.env` | 仅当前项目使用 |
| **用户级配置** | `~/.baoyu-skills/.env` | 所有项目共享 |

### 当前生效配置

**项目级配置路径**：
```
/Users/whiteareas/Documents/openclaw/agents/media/.baoyu-skills/.env
```

### 配置项说明

```env
# OpenAI API 配置（用于图片生成等）
OPENAI_API_KEY=sk-xxx
OPENAI_IMAGE_MODEL=gpt-4o-image
OPENAI_IMAGE_USE_CHAT=true
OPENAI_BASE_URL=https://sg.uiuiapi.com/v1

# 微信公众号 API 配置（如使用 API 方式发布）
WECHAT_APP_ID=你的 AppID
WECHAT_APP_SECRET=你的 AppSecret

# 其他服务配置（按需添加）
```

### 修改步骤

1. 打开配置文件：
   ```bash
   # 项目级
   code /Users/whiteareas/Documents/openclaw/agents/media/.baoyu-skills/.env
   
   # 或用户级
   code ~/.baoyu-skills/.env
   ```

2. 修改对应的 API 密钥

3. 保存即可生效（无需重启）

### 优先级

```
环境变量 > 项目级 .env > 用户级 .env > 技能默认值
```

---

## 📁 技能目录结构

```
02-小媒专区/skills/
├── config-guide.md          # 本文件 - 配置指南
├── baoyu-post-to-wechat/    # 微信公众号发布
├── baoyu-image-gen/         # AI 图片生成
├── baoyu-cover-image/       # 封面图生成
├── baoyu-xhs-images/        # 小红书图片
├── baoyu-compress-image/    # 图片压缩
├── baoyu-post-to-x/         # X/Twitter 发布
├── baoyu-post-to-weibo/     # 微博发布
├── baoyu-infographic/       # 信息图生成
├── baoyu-comic/             # 漫画生成
├── baoyu-format-markdown/   # Markdown 格式化
├── baoyu-translate/         # 翻译
├── baoyu-markdown-to-html/  # Markdown 转 HTML
├── baoyu-url-to-markdown/   # URL 转 Markdown
├── baoyu-danger-x-to-markdown/  # X/Twitter 内容抓取
└── baoyu-danger-gemini-web/     # Gemini Web 工具
```

---

**最后更新**: 2026-03-19  
**维护者**: 小媒
