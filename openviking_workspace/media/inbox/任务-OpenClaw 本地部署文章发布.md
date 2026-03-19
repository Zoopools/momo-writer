# 任务：OpenClaw 本地部署文章发布

**任务时间**: 2026-03-10 19:44  
**发布者**: 哥哥  
**执行者**: 小媒 (media)  
**状态**: ⏳ 进行中

---

## 🎯 任务内容

**哥哥指令**:
> "小媒使用新方案 写一篇关于 openclaw 本地部署详细步骤的文章并用我的浏览器发布到公众号"

---

## 📋 任务要求

### 1. 文章主题

**OpenClaw 本地部署详细步骤**

**内容要点**:
- ✅ OpenClaw 是什么
- ✅ 系统要求（macOS/Windows/Linux）
- ✅ 安装步骤（详细命令）
- ✅ 配置步骤（API Key、飞书等）
- ✅ 启动 Gateway
- ✅ 验证安装
- ✅ 常见问题排查
- ✅ 使用示例

---

### 2. 使用新方案发布（Chrome 扩展）⭐

**重要**: 使用 Chrome 扩展模式，不要使用独立浏览器！

**发布流程**:
1. ✅ 创作内容（Markdown）
2. ✅ 生成封面图（baoyu-cover-image）
3. ✅ 排版成微信格式（baoyu-format-markdown）
4. ✅ **检查标签页是否已附加**:
   ```bash
   openclaw browser --browser-profile chrome tabs
   ```
5. ✅ **使用 Chrome 扩展发布**:
   - profile: "chrome"
   - targetId: 从上面命令获取
   - 导航到公众号后台
   - 填写标题、内容、封面
   - 点击发布
6. ✅ 飞书通知哥哥

---

### 3. 文章结构建议

```markdown
# OpenClaw 本地部署完整指南

## 什么是 OpenClaw

## 系统要求

## 安装步骤

### macOS

### Windows

### Linux

## 配置步骤

### 1. API Key 配置

### 2. 飞书配置

### 3. 其他配置

## 启动 Gateway

## 验证安装

## 常见问题

## 使用示例
```

---

## 🚀 立即开始

**步骤 1: 检查标签页**
```bash
openclaw browser --browser-profile chrome tabs
```

**如果没有标签页** → 提醒哥哥：「哥哥，请先附加公众号后台标签页」

**如果有标签页** → 开始创作并发布

---

## 📝 参考资料

- OpenClaw 文档：https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw
- 安装命令参考：`openclaw --help`

---

## 🖤 墨墨的提示

小媒，记得:
1. ✅ 使用 Chrome 扩展模式（profile: "chrome"）
2. ✅ 复用哥哥的登录状态
3. ✅ 发布完成后提醒哥哥分离标签页
4. ✅ 文章要详细、清晰、可操作

**加油！期待你的大作**！📝✨

---

*任务时间：2026-03-10 19:44*  
*使用方案：Chrome 扩展模式（新方案）*  
*发布平台：微信公众号*
