# GEO 发布系统

**路径**: `~/Documents/openclaw/openviking_workspace/publish-geo/`

**功能**: 多平台自媒体文章自动发布系统

---

## ✅ 已完成

### 1. 登录态导出
- 支持 Cookie-Editor 扩展导出
- 自动转换为 Playwright storageState 格式
- 保存到 `auth/` 目录

### 2. 百家号登录态
- 文件: `auth/bjh-work.json`
- 包含: BDUSS, bjhStoken, PHPSESSID 等关键 Cookie
- 状态: ✅ 有效

### 3. 防封策略
- 随机延迟 (500-2000ms)
- 模拟人类打字
- 差异化 User-Agent
- 无头模式运行

### 4. 飞书回填
- 发布成功/失败自动报告
- 支持状态: 已发布、发布失败、需重新授权

---

## 🔄 进行中

### 自动发布功能
**问题**: 百家号发布页面有 4 步引导流程，需要处理后才能进入编辑页

**尝试过的方案**:
1. 直接打开发布 URL - 进入引导页
2. 点击"发布图文" - 弹窗拦截
3. 等待新页面 - 未触发

**下一步**:
- 使用有界面模式手动进入编辑页
- 或使用 Playwright codegen 录制完整流程

---

## 🚀 使用方法

### 导出登录态
```bash
# 使用 Cookie-Editor 导出 Cookie
# 然后运行转换脚本
node scripts/login-final.js
```

### 发布文章（开发中）
```bash
node scripts/publish.js bjh-work articles/article.md
```

---

## 📋 多平台支持计划

| 平台 | 登录态 | 发布脚本 | 状态 |
|------|--------|----------|------|
| 百家号 | ✅ | 🔄 | 开发中 |
| 微信公众号 | ⬜ | ⬜ | 待开发 |
| 知乎 | ⬜ | ⬜ | 待开发 |
| 小红书 | ⬜ | ⬜ | 待开发 |

---

## 🛠️ 技术栈

- Playwright - 浏览器自动化
- Node.js - 运行时
- OpenClaw - 调度执行

---

**最后更新**: 2024-03-17 13:09
