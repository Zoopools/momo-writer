# Hunter-B 站评论 + 图片获取及在线访问 1.0

**创建时间**: 2026-03-13  
**版本**: v1.0  
**状态**: ✅ 已验证可用  
**简称**: Hunter-B 站评论方案

---

## 📋 方案概述

从视频链接出发，抓取评论区带图片的评论，生成美观的 HTML 报告，并部署到 GitHub Pages 实现永久在线访问。

**核心流程**：
```
视频链接 → 评论抓取 → 图片下载 → HTML 生成 → GitHub 部署 → 在线访问
```

**代表作品**：
- B 站评论图片抓取：https://zoopools.github.io/bili-comments/

---

## 🎯 适用场景

1. **社交媒体评论抓取**
   - B 站视频评论
   - 微博评论
   - 知乎回答
   - 小红书笔记

2. **信息报告生成**
   - 数据整理报告
   - 竞品分析报告
   - 舆情监控报告

3. **在线展示需求**
   - 需要永久链接
   - 需要团队共享
   - 需要美观展示

---

## 🛠️ 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| 编程语言 | Python 3.9+ | 脚本开发 |
| HTTP 请求 | requests | API 调用 |
| 版本控制 | Git | 代码管理 |
| 部署平台 | GitHub Pages | 静态网站托管 |
| 前端 | HTML/CSS | 报告样式 |
| CLI 工具 | GitHub CLI (gh) | 仓库管理 |

---

## 📝 实施步骤

### 阶段 1：数据抓取

**目标**：从目标平台获取评论数据

**关键代码**：
```python
# B 站移动端 API（无需登录）
https://api.bilibili.com/x/web-interface/view?bvid={BV_ID}
https://api.bilibili.com/x/v2/reply/main?oid={aid}&type=1&mode=3

# 提取图片 URL
for reply in replies:
    pictures = reply["content"]["pictures"]
    img_url = pic["img_src"]
```

**注意事项**：
- 优先使用官方 API
- 设置合理的 User-Agent
- 处理图片防盗链（`referrerpolicy="no-referrer"`）

---

### 阶段 2：图片下载

**目标**：下载评论中的原图

**关键处理**：
```python
# 去除压缩参数
clean_url = re.sub(r'\.\d+x\d+\.jpg$', '.jpg', img_url)
clean_url = re.sub(r'@\d+w_\d+h\.[a-z]+$', '', clean_url)

# 确保 HTTPS
if clean_url.startswith("http://"):
    clean_url = clean_url.replace("http://", "https://")

# 下载保存
img_resp = session.get(clean_url, timeout=15)
with open(filepath, "wb") as f:
    f.write(img_resp.content)
```

---

### 阶段 3：HTML 报告生成

**目标**：生成美观的 HTML 报告

**核心样式**：
```css
/* 紫色渐变背景 */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 卡片样式 */
.card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

/* 图片防盗链 */
img {
    referrerpolicy="no-referrer";
    loading="lazy";
}
```

**设计要点**：
- 响应式布局
- 卡片式信息分组
- 悬停动画效果
- 图片懒加载

---

### 阶段 4：GitHub Pages 部署

**目标**：部署到 GitHub 实现永久在线

**命令流程**：
```bash
# 1. 创建仓库
gh repo create bili-comments --public --source=./bili_images --push

# 2. 初始化 Git
cd bili_images
git init
git add .
git commit -m "B 站评论图片报告"

# 3. 推送代码
git remote add origin https://github.com/Zoopools/bili-comments.git
git push -u origin main

# 4. 启用 Pages（手动）
# GitHub → Settings → Pages → Save
```

**访问链接**：
```
https://<用户名>.github.io/<仓库名>/
```

---

## ⚠️ 常见问题与解决

### 问题 1：图片防盗链

**现象**：图片显示裂开（403 Forbidden）

**解决**：
```html
<img referrerpolicy="no-referrer" src="...">
```

---

### 问题 2：中文文件名 404

**现象**：中文文件名的 HTML 访问 404

**解决**：
- 使用英文文件名（`index.html`）
- 或 URL 编码访问

---

### 问题 3：图片加载失败

**现象**：部分图片不显示

**解决**：
```html
<img onerror="显示备用提示" src="...">
```

---

## 📁 文件结构

```
项目目录/
├── bili_images/              # 输出目录
│   ├── index.html           # 在线版 HTML
│   ├── bili_视频 ID_1.jpg   # 评论图片
│   └── ...
├── bili_mobile_api.py       # 抓取脚本
├── bili_export_table.py     # 导出脚本
├── generate_index.py        # HTML 生成
└── README.md                # 项目说明
```

---

## 🔄 复用流程

### 抓取新视频评论

```bash
cd /Users/wh1ko/Documents/openclaw/agents/hunter

# 1. 修改脚本中的 BV_ID
# 2. 运行抓取
python3 bili_export_table.py

# 3. 生成报告
python3 generate_index.py

# 4. 推送到 GitHub
cd bili_images
git add . && git commit -m "更新报告" && git push

# 5. 等待 1 分钟自动部署
```

---

## 💡 最佳实践

### 1. 代码组织
- 模块化设计（抓取、处理、输出分离）
- 配置文件独立（便于修改）
- 注释清晰（方便后续维护）

### 2. 错误处理
- 网络请求超时设置
- API 失败重试机制
- 数据验证（检查关键字段）

### 3. 性能优化
- 图片懒加载
- 批量请求控制
- CDN 加速（可选）

### 4. 安全注意
- 不上传敏感数据
- 使用 HTTPS
- 定期检查依赖安全

---

## 📊 项目指标

| 指标 | 数值 |
|------|------|
| 抓取速度 | ~5 秒/视频 |
| 图片画质 | 100% 原图 |
| 部署时间 | ~1 分钟 |
| 托管成本 | 免费 |
| 访问速度 | 全球 CDN |

---

## 🔮 扩展方向

### 功能扩展
- [ ] 批量抓取多个视频
- [ ] 定时自动更新
- [ ] 评论情感分析
- [ ] 图片 OCR 文字提取
- [ ] 导出 PDF/Excel 格式

### 平台扩展
- [ ] 微博评论抓取
- [ ] 知乎回答抓取
- [ ] 小红书笔记抓取
- [ ] 抖音评论抓取

### 部署优化
- [ ] 自定义域名
- [ ] CDN 加速
- [ ] 多环境部署

---

## 📚 相关资源

### 文档链接
- GitHub Pages 官方文档：https://pages.github.com/
- GitHub CLI 文档：https://cli.github.com/
- B 站开放平台：https://open.bilibili.com/

### 代码仓库
- 示例项目：https://github.com/Zoopools/bili-comments

### 在线演示
- B 站评论报告：https://zoopools.github.io/bili-comments/

---

## 🏹 小猎签名

**方案命名**: Hunter 在线报告部署方案 v1.0  
**创建者**: 小猎（Hunter）  
**最后更新**: 2026-03-13  
**状态**: ✅ 生产环境可用

---

*🏹 小猎 · 信息捕手 | 专注信息获取和整理*
