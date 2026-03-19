# baoyu-skills 研究笔记

**来源：** GitHub - JimLiu/baoyu-skills  
**链接：** https://github.com/JimLiu/baoyu-skills/blob/main/README.zh.md  
**作者：** JimLiu (宝玉)  
**研究日期：** 2026-03-07

---

## 📦 技能包概览

三大技能类别：

| 技能包 | 说明 | 包含技能 |
|--------|------|----------|
| **content-skills** | 内容生成和发布 | xhs-images, infographic, cover-image, slide-deck, comic, article-illustrator, post-to-x, post-to-wechat, post-to-weibo |
| **ai-generation-skills** | AI 生成后端 | image-gen, danger-gemini-web |
| **utility-skills** | 内容处理工具 | url-to-markdown, danger-x-to-markdown, compress-image, format-markdown, translate |

---

## 🎨 核心技能详解

### 1. baoyu-xhs-images ⭐⭐⭐

**功能：** 小红书信息图系列生成器

**特点：**
- 将内容拆解为 1-10 张卡通风格信息图
- 支持 **风格 × 布局** 二维系统

**风格（9 种）：**
- `cute`（默认）、`fresh`、`warm`、`bold`、`minimal`、`retro`、`pop`、`notion`、`chalkboard`

**布局（6 种）：**
| 布局 | 密度 | 适用场景 |
|------|------|----------|
| `sparse` | 1-2 点 | 封面、金句 |
| `balanced` | 3-4 点 | 常规内容 |
| `dense` | 5-8 点 | 知识卡片、干货总结 |
| `list` | 4-7 项 | 清单、排行 |
| `comparison` | 双栏 | 对比、优劣 |
| `flow` | 3-6 步 | 流程、时间线 |

**使用示例：**
```bash
# 自动选择风格和布局
/baoyu-xhs-images posts/ai-future/article.md

# 指定风格
/baoyu-xhs-images posts/ai-future/article.md --style notion

# 指定布局
/baoyu-xhs-images posts/ai-future/article.md --layout dense

# 直接输入内容
/baoyu-xhs-images 今日星座运势
```

**对小媒的启发：** ⭐⭐⭐⭐⭐
- 小媒的游戏内容非常适合用 `dense` 或 `list` 布局
- 杀戮尖塔 2 攻略可以用 `flow` 布局（流程步骤）
- 角色对比可以用 `comparison` 布局

---

### 2. baoyu-infographic ⭐⭐⭐⭐

**功能：** 专业信息图生成器

**特点：**
- 20 种布局 + 17 种视觉风格
- 分析内容后推荐布局×风格组合

**布局（20 种）：**
| 布局 | 适用场景 |
|------|----------|
| `bridge` | 问题→解决方案、跨越鸿沟 |
| `circular-flow` | 循环、周期性流程 |
| `comparison-table` | 多因素对比 |
| `do-dont` | 正确 vs 错误做法 |
| `equation` | 公式分解、输入→输出 |
| `feature-list` | 产品功能、要点列表 |
| `fishbone` | 根因分析、鱼骨图 |
| `funnel` | 转化漏斗、筛选过程 |
| `grid-cards` | 多主题概览、卡片网格 |
| `iceberg` | 表面 vs 隐藏层面 |
| `journey-path` | 用户旅程、里程碑 |
| `layers-stack` | 技术栈、分层结构 |
| `mind-map` | 头脑风暴、思维导图 |
| `nested-circles` | 影响层级、范围圈 |
| `priority-quadrants` | 四象限矩阵、优先级 |
| `pyramid` | 层级金字塔、马斯洛需求 |
| `scale-balance` | 利弊权衡、天平对比 |
| `timeline-horizontal` | 历史、时间线事件 |
| `tree-hierarchy` | 组织架构、分类树 |
| `venn` | 重叠概念、韦恩图 |

**风格（17 种）：**
- `craft-handmade`（默认）、`claymation`、`kawaii`、`storybook-watercolor`、`chalkboard`、`cyberpunk-neon`、`bold-graphic`、`aged-academia`、`corporate-memphis`、`technical-schematic`、`origami`、`pixel-art`、`ui-wireframe`、`subway-map`、`ikea-manual`、`knolling`、`lego-brick`

**使用示例：**
```bash
# 根据内容自动推荐组合
/baoyu-infographic path/to/content.md

# 指定布局
/baoyu-infographic path/to/content.md --layout pyramid

# 指定风格
/baoyu-infographic path/to/content.md --style technical-schematic

# 指定比例
/baoyu-infographic path/to/content.md --aspect portrait
```

**对小媒的启发：** ⭐⭐⭐⭐⭐
- 游戏机制解析 → `fishbone`（根因分析）或 `layers-stack`（技术栈）
- 角色 build 推荐 → `priority-quadrants`（四象限）
- 版本更新对比 → `comparison-table` 或 `scale-balance`
- 杀戮尖塔流程 → `journey-path` 或 `timeline-horizontal`

---

### 3. baoyu-cover-image ⭐⭐⭐

**功能：** 文章封面图生成器

**特点：**
- 五维定制系统：类型 × 配色 × 渲染 × 文字 × 氛围
- 9 种配色方案 × 6 种渲染风格 = 54 种独特效果

**五个维度：**
1. **类型：** `hero`、`conceptual`、`typography`、`metaphor`、`scene`、`minimal`
2. **配色：** `warm`、`elegant`、`cool`、`dark`、`earth`、`vivid`、`pastel`、`mono`、`retro`
3. **渲染：** `flat-vector`、`hand-drawn`、`painterly`、`digital`、`pixel`、`chalk`
4. **文字：** `none`、`title-only`（默认）、`title-subtitle`、`text-rich`
5. **氛围：** `subtle`、`balanced`（默认）、`bold`

**使用示例：**
```bash
# 自动选择所有维度
/baoyu-cover-image path/to/article.md

# 快速模式
/baoyu-cover-image path/to/article.md --quick

# 指定维度
/baoyu-cover-image path/to/article.md --type conceptual --palette cool --rendering digital

# 纯视觉（不含标题文字）
/baoyu-cover-image path/to/article.md --no-title
```

---

### 4. baoyu-slide-deck ⭐⭐⭐

**功能：** 幻灯片生成器

**特点：**
- 从内容生成专业的幻灯片图片
- 先创建包含样式说明的完整大纲，然后逐页生成

**风格系统（4 维度）：**
| 维度 | 选项 |
|------|------|
| 纹理 | `clean`、`grid`、`organic`、`pixel`、`paper` |
| 氛围 | `professional`、`warm`、`cool`、`vibrant`、`dark`、`neutral` |
| 字体 | `geometric`、`humanist`、`handwritten`、`editorial`、`technical` |
| 密度 | `minimal`、`balanced`、`dense` |

**预设（15 种）：**
- `blueprint`（默认）、`chalkboard`、`corporate`、`minimal`、`sketch-notes`、`watercolor`、`dark-atmospheric`、`notion`、`bold-editorial`、`editorial-infographic`、`fantasy-animation`、`intuition-machine`、`pixel-art`、`scientific`、`vector-illustration`、`vintage`

**使用示例：**
```bash
# 从 markdown 生成
/baoyu-slide-deck path/to/article.md

# 指定风格
/baoyu-slide-deck path/to/article.md --style corporate

# 指定受众
/baoyu-slide-deck path/to/article.md --audience executives

# 仅生成大纲
/baoyu-slide-deck path/to/article.md --outline-only
```

---

### 5. baoyu-post-to-x / post-to-wechat / post-to-weibo ⭐⭐⭐⭐

**功能：** 内容发布到各平台

**对小媒的启发：** ⭐⭐⭐⭐⭐
- 这正是咱们需要的自动发布能力！
- 可以借鉴这个架构做 B 站、小红书发布

---

### 6. baoyu-url-to-markdown ⭐⭐⭐

**功能：** 网页转 Markdown

**使用场景：**
- 抓取竞品内容
- 保存参考资料
- 快速提取文章

---

## 🚀 安装方式

### 快速安装（推荐）
```bash
npx skills add jimliu/baoyu-skills
```

### 注册插件市场
```bash
/plugin marketplace add jimliu/baoyu-skills
```

### 安装指定技能
```bash
/plugin install content-skills@baoyu-skills
/plugin install ai-generation-skills@baoyu-skills
/plugin install utility-skills@baoyu-skills
```

### 更新技能
```bash
/plugin → Marketplaces → baoyu-skills → Update marketplace
```

---

## 💡 对小媒 Agent 的启发

### 立即可借鉴的

1. **内容可视化系统** ⭐⭐⭐⭐⭐
   - 小媒的游戏内容非常适合信息图形式
   - 可以借鉴 `xhs-images` 的风格×布局系统
   - 杀戮尖塔 2 攻略 → `flow` 布局 + `pixel-art` 风格

2. **自动发布能力** ⭐⭐⭐⭐⭐
   - `post-to-x` 系列技能的架构值得参考
   - 结合之前研究的 `bili-sunflower-publish`
   - 可以做 `post-to-bilibili`、`post-to-xiaohongshu`

3. **封面图生成** ⭐⭐⭐⭐
   - 小媒的视频/文章需要封面
   - 五维定制系统可以直接借鉴
   - 游戏内容适合 `pixel` 渲染 + `vivid` 配色

4. **网页抓取** ⭐⭐⭐
   - `url-to-markdown` 可以用于竞品分析
   - 抓取 B 站热门游戏视频标题/简介
   - 分析爆款内容的规律

### 中期可以开发的

1. **小媒专属信息图技能**
   - 基于 `baoyu-infographic` 的架构
   - 增加游戏相关的布局（如技能树、装备对比）
   - 风格增加游戏主题（像素风、赛博朋克等）

2. **多平台发布矩阵**
   - B 站（专栏 + 小站）
   - 小红书
   - 抖音
   - 公众号
   - 统一接口，各平台实现差异

3. **内容批量生成**
   - 一篇文章 → 多平台适配版本
   - 自动调整格式、标签、话题
   - 定时发布调度

---

## 📋 行动计划

### Phase 1: 学习（本周）
- [ ] 安装 baoyu-skills 并测试核心功能
- [ ] 重点研究 `xhs-images` 和 `infographic` 的实现
- [ ] 分析 `post-to-x` 系列的发布逻辑

### Phase 2: 设计（下周）
- [ ] 设计小媒的内容可视化方案
- [ ] 确定 B 站/小红书发布的接口设计
- [ ] 规划风格×布局的游戏主题扩展

### Phase 3: 实现（2 周）
- [ ] 开发小媒专属信息图技能
- [ ] 实现 B 站自动发布（参考 bili-sunflower-publish）
- [ ] 实现小红书自动发布

### Phase 4: 整合（1 周）
- [ ] 整合到小媒 Agent 工作流
- [ ] 测试完整的内容生成→发布流程
- [ ] 优化用户体验

---

## 🔗 相关资源

- **GitHub:** https://github.com/JimLiu/baoyu-skills
- **作者：** JimLiu (宝玉)
- **安装命令：** `npx skills add jimliu/baoyu-skills`
- **技能分类：** content-skills, ai-generation-skills, utility-skills

---

*最后更新：2026-03-07*
