# SteamDB 监控系统 - 技术方案 v1.0

**创建时间**: 2026-03-18  
**创建者**: 小猎 (Hunter)  
**状态**: ✅ 核心流程已验证通过  
**最后更新**: 2026-03-18 15:43

---

## 📋 项目概述

**目标**: 监控 SteamDB 首页 Trending Games 板块的 14 款游戏，计算过去 7 天在线人数增长率，筛选增长 >30% 的游戏并告警。

**核心突破**: 通过 Browser 工具接管 Chrome 浏览器，绕过 Cloudflare 防护，直接提取 Highcharts 图表中的原始数据（每 10 分钟采样，共 3,465 个数据点）。

---

## 🎯 技术架构

```
┌─────────────────────────────────────────────────────────┐
│  浏览器接管层                                          │
│  - OpenClaw browser 工具 (profile="chrome")            │
│  - Chrome 扩展继电器 (Cloudflare 绕过)                  │
├─────────────────────────────────────────────────────────┤
│  数据提取层                                            │
│  - JavaScript 注入 (Highcharts.charts[0].series[0])    │
│  - 原始数据点提取 (x: 时间戳，y: 在线人数)              │
├─────────────────────────────────────────────────────────┤
│  数据处理层                                            │
│  - 7 天数据切片 (最近 1,008 个点 = 7×24×6)              │
│  - 增长率计算 (平均值/峰值/综合评分)                    │
├─────────────────────────────────────────────────────────┤
│  输出层                                                │
│  - 飞书表格存储                                        │
│  - 告警消息推送                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ 核心实现

### 1. 浏览器接管与页面加载

```javascript
// 打开 SteamDB Charts 页面
browser.open(
  profile="chrome",
  url="https://steamdb.info/app/{APP_ID}/charts/"
)

// 等待 Cloudflare 验证 + 页面加载 (8 秒)
// 点击 Charts 标签页触发数据加载
// 滚动到图表容器触发懒加载
```

### 2. Highcharts 数据提取

```javascript
// 提取图表原始数据
const result = { charts: [] };
if (typeof Highcharts === 'undefined') return { error: 'Highcharts not loaded' };

for (let i = 0; i < Highcharts.charts.length; i++) {
  const chart = Highcharts.charts[i];
  if (!chart || !chart.series) continue;
  
  const chartData = { index: i, seriesCount: chart.series.length, series: [] };
  
  for (let j = 0; j < chart.series.length; j++) {
    const series = chart.series[j];
    if (!series.data || series.data.length === 0) continue;
    
    const dataPoints = series.data.map(p => ({ x: p.x, y: p.y }));
    chartData.series.push({
      name: series.name || 'unnamed',
      dataPoints: dataPoints.length,
      firstPoint: dataPoints[0],
      lastPoint: dataPoints[dataPoints.length - 1],
      sample7days: dataPoints.slice(-1008)  // 最近 7 天数据
    });
  }
  
  if (chartData.series.length > 0) result.charts.push(chartData);
}

return JSON.stringify(result, null, 2);
```

### 3. 数据验证结果（赛博朋克 2077 测试）

| 指标 | 值 |
|------|-----|
| **图表数量** | 2 个 (Players + Average Players) |
| **数据点总数** | 3,465 个 (实时在线) |
| **数据频率** | 每 10 分钟采样一次 |
| **7 天数据量** | 1,008 个点 (7×24×6) |
| **当前在线** | 15,504 人 |
| **7 天前在线** | 15,643 人 |
| **简单增长率** | -0.89% |
| **平均增长率** | +1.50% (推荐指标) |

---

## 📊 增长率计算方案

### 推荐方案：平均增长率

```python
def calculate_avg_growth(data_7days, data_prev_7days):
    """
    计算 7 天平均增长率（推荐作为主要告警指标）
    
    Args:
        data_7days: 最近 7 天的数据点列表
        data_prev_7days: 前 7 天的数据点列表
    
    Returns:
        增长率百分比 (%)
    """
    avg_current = sum(data_7days) / len(data_7days)
    avg_prev = sum(data_prev_7days) / len(data_prev_7days)
    
    if avg_prev == 0:
        return None
    
    growth = ((avg_current - avg_prev) / avg_prev) * 100
    return growth
```

### 辅助指标（可选）

| 指标 | 计算公式 | 用途 |
|------|---------|------|
| **峰值增长率** | (最近 7 天峰值 - 前 7 天峰值) / 前 7 天峰值 | 捕捉爆发式增长 |
| **中位数增长率** | (最近 7 天中位数 - 前 7 天中位数) / 前 7 天中位数 | 抗异常值干扰 |
| **趋势斜率** | 线性回归斜率 / 平均值 | 反映增长方向 |
| **综合评分** | 平均 (50%) + 峰值 (30%) + 斜率 (20%) | 全面评估 |

---

## 📋 执行流程

```
1. 从 SteamDB 首页获取 14 款 trending 游戏
   └─ URL: https://steamdb.info/
   └─ 提取：游戏名称、App ID、当前在线人数

2. 对每款游戏访问 Charts 页面
   └─ URL: https://steamdb.info/app/{APP_ID}/charts/
   └─ 等待：8 秒 (Cloudflare + 懒加载)

3. 提取 Highcharts 数据
   └─ JavaScript 注入
   └─ 获取：3,465 个数据点 (每 10 分钟)

4. 计算增长率
   └─ 切片：最近 7 天 (1,008 点) vs 前 7 天 (1,008 点)
   └─ 计算：平均增长率 %

5. 筛选告警
   └─ 阈值：>30% 或 <-30%
   └─ 输出：告警游戏列表

6. 写入飞书表格 + 发送消息
```

---

## 🗂️ 飞书表格设计

### 表 1: 监控游戏列表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| App ID | 数字 | Steam 游戏唯一标识 |
| 游戏名称 | 文本 | |
| 监控状态 | 单选 | 启用/暂停 |
| 添加日期 | 日期 | |

### 表 2: 每日数据记录

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日期 | 日期 | |
| App ID | 数字 | |
| 游戏名称 | 文本 | |
| 当前在线 | 数字 | 实时数据 |
| 7 天平均 | 数字 | 最近 7 天平均值 |
| 前 7 天平均 | 数字 | 前 7 天平均值 |
| 平均增长率 | 百分比 | **主要告警指标** |
| 峰值增长率 | 百分比 | 辅助指标 |
| 趋势 | 单选 | 📈上升/📉下降/📊平稳 |
| 是否告警 | 复选框 | >30% 或 <-30% |

### 表 3: 告警记录

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 告警日期 | 日期 | |
| 游戏名称 | 文本 | |
| App ID | 数字 | |
| 增长率 | 百分比 | |
| 当前值 | 数字 | |
| 已通知 | 复选框 | 避免重复推送 |

---

## ⚠️ 注意事项

### 技术限制

| 限制 | 解决方案 |
|------|---------|
| **Cloudflare 防护** | 使用 Browser 工具 (真实浏览器环境) |
| **图表懒加载** | 点击 Charts tab + 滚动到图表容器 |
| **数据量大** | 只提取最近 14 天数据 (2,016 点) |
| **浏览器占用** | 执行前通知哥哥，避免冲突 |

### 速率控制

- **请求间隔**: 每款游戏间隔 2-3 秒
- **执行频率**: 每天 1-2 次 (建议凌晨 2 点 + 早上 9 点)
- **同时请求**: 单次执行，避免并发

---

## 🚀 待办事项

### 已完成 ✅

- [x] Browser 工具接管 Chrome 浏览器
- [x] 绕过 Cloudflare 验证
- [x] 触发 Highcharts 图表加载
- [x] 提取原始数据点 (3,465 个)
- [x] 计算 7 天增长率
- [x] 验证数据准确性 (赛博朋克 2077 测试)

### 待完成 ⏳

- [ ] 批量抓取首页 14 款游戏
- [ ] 创建飞书表格模板
- [ ] 编写完整 Python 脚本
- [ ] 配置定时任务 (cron)
- [ ] 设置告警推送 (飞书消息)
- [ ] 异常处理与日志记录

---

## 📞 关键联系人

- **项目负责人**: 哥哥 (Zoopools)
- **执行 Agent**: 小猎 (Hunter)
- **技术文档**: 本文件

---

## 🔗 相关链接

- **SteamDB 首页**: https://steamdb.info/
- **SteamDB Charts**: https://steamdb.info/app/1091500/charts/ (示例)
- **Highcharts 文档**: https://api.highcharts.com/
- **飞书多维表格**: 待创建

---

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-03-18 | v1.0 | 初始版本，核心流程验证通过 |

---

*🏹 小猎签名：技术存档完成，随时可以重启项目！*
