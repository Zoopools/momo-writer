# ⚠️ DashScope 图像生成 API 问题

**时间:** 2026-03-07 13:15  
**状态:** API Key 权限不足  

---

## 🔍 问题分析

**当前 API Key:** `sk-3f4e373a4fbc488898754cf5e57f35e1`

**错误信息:**
```
401 InvalidApiKey: Invalid API-key provided.
```

**可能原因:**
1. ❌ API Key 只有文本生成权限（通义千问）
2. ❌ 图像生成服务（通义万相）需要单独开通
3. ❌ API Key 格式不正确（可能需要不同的前缀）
4. ❌ 服务未在当前区域可用

---

## ✅ 解决方案

### 方案 A：开通通义万相服务（推荐）

**步骤:**
1. 访问 https://dashscope.console.aliyun.com/
2. 登录阿里云账号
3. 在左侧菜单找到"通义万相"
4. 点击"开通服务"
5. 创建新的 API Key（图像生成专用）
6. 更新到 `.env.local`

**预计成本:**
- 通义万相 wanx2.1-turbo: ¥0.02-0.05/张
- 免费额度：新用户可能有赠送

---

### 方案 B：使用其他图像生成服务

| 服务商 | 模型 | 配置难度 | 成本 |
|--------|------|----------|------|
| **OpenAI DALL-E 3** | dall-e-3 | 中（需要代理） | $0.04/张 |
| **Replicate** | nano-banana-pro | 中 | $0.02-0.05/张 |
| **Google Imagen** | imagen-3 | 高（需要代理） | 免费额度 |

---

### 方案 C：使用免费替代方案

**1. Canvas 手绘（墨墨可以画）**
- 优点：免费、快速
- 缺点：质量一般

**2. 在线工具手动生成**
- Canva、稿定设计等
- 优点：可控性强
- 缺点：需要手动操作

**3. 其他免费 API**
- Stable Diffusion WebUI（本地部署）
- LiblibAI（国内免费）

---

## 📝 小媒的建议

**短期方案：**
- 墨墨用 Canvas 绘制简易版信息图
- 或者哥哥手动用 Canva 等工具制作

**长期方案：**
- 开通通义万相服务（推荐）
- 或者配置 DALL-E 3（如果已有 OpenAI Key）

---

## 🎨 墨墨 Canvas 绘图（临时方案）

如果哥哥想立刻看到效果，墨墨可以用 Canvas 绘制简易版：

```html
<!DOCTYPE html>
<canvas width="1080" height="1920"></canvas>
<script>
// 绘制信息图封面
const ctx = canvas.getContext('2d');
// 背景
ctx.fillStyle = '#f0f4f8';
ctx.fillRect(0, 0, 1080, 1920);
// 标题
ctx.fillStyle = '#2d3748';
ctx.font = 'bold 72px sans-serif';
ctx.fillText('杀戮尖塔 2', 140, 300);
ctx.fillText('新手必知的 5 件事', 140, 400);
// 装饰
ctx.fillStyle = '#667eea';
ctx.fillRect(140, 450, 400, 20);
</script>
```

---

*小媒等待 API 配置中...* 📱
