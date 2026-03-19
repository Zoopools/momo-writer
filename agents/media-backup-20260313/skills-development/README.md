# 小媒技能开发指南

**审批状态**: ✅ 墨墨已批准  
**开发技能**: `baoyu-post-to-bilibili` + `baoyu-danmaku-design`  
**开始时间**: 2026-03-12

---

## 📋 开发清单

### Phase 1: B站发布技能 (baoyu-post-to-bilibili)

#### 已完成 ✅
- [x] SKILL.md 基础框架
- [x] bilibili-poster.js 基础代码

#### 待完成 ⏳
- [ ] 安装 Playwright 依赖
- [ ] 测试 B站页面选择器
- [ ] 完善登录流程
- [ ] 测试视频上传
- [ ] 测试封面设置
- [ ] 测试分区选择
- [ ] 错误处理优化
- [ ] 添加日志输出
- [ ] 墨墨审查

### Phase 2: 弹幕设计技能 (baoyu-danmaku-design)

#### 已完成 ✅
- [x] SKILL.md 基础框架
- [x] danmaku-designer.js 基础代码

#### 待完成 ⏳
- [ ] 测试命令行参数
- [ ] 优化弹幕模板库
- [ ] 添加更多风格支持
- [ ] 墨墨审查

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入开发目录
cd ~/Documents/openclaw/agents/media/skills-development/

# 安装 Playwright (用于 B站发布)
cd baoyu-post-to-bilibili
npm init -y
npm install playwright

# 安装浏览器
npx playwright install chromium
```

### 2. 测试弹幕设计技能

```bash
# 测试基础功能
node baoyu-danmaku-design/danmaku-designer.js \
  --duration 10 \
  --topic "AI工具介绍" \
  --style "知识" \
  --output test-danmaku.md

# 查看输出
cat test-danmaku.md
```

### 3. 测试 B站发布技能

```bash
# 注意: 需要提前登录 B站
node baoyu-post-to-bilibili/bilibili-poster.js \
  --video /path/to/video.mp4 \
  --title "测试视频" \
  --description "这是一个测试" \
  --tags "测试,视频"
```

---

## 📚 参考资源

### B站发布参考
- 微信公众号发布技能: `~/.openclaw/skills/baoyu-post-to-wechat/`
- B站上传页面: https://member.bilibili.com/platform/upload/video/frame
- Playwright 文档: https://playwright.dev/

### 技能开发规范
- SKILL.md 格式参考其他 baoyu 技能
- 触发词要覆盖常见表达方式
- 必须包含用法示例

---

## 🎯 验收标准

### 功能完整性
- [ ] 能完成从视频上传到发布的全流程
- [ ] 弹幕设计能生成完整的时间轴方案

### 数据安全
- [ ] 账号凭证不硬编码
- [ ] 支持环境变量或配置文件

### 错误处理
- [ ] 网络异常有明确提示
- [ ] 登录失败有重试机制
- [ ] 文件不存在有检查

### 代码质量
- [ ] 有注释说明
- [ ] 错误处理完善
- [ ] 日志输出清晰

---

## 📝 提交审查

开发完成后：
1. 复制技能到 `~/.openclaw/skills/`
2. 链接到所有 Agent 的 `.agents/skills/`
3. 通知墨墨审查
4. 根据反馈修改
5. 墨墨最终批准

---

**小媒加油！🎨**
