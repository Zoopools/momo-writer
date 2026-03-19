#!/usr/bin/env node
/**
 * Danmaku Designer - 弹幕互动设计工具
 * 
 * 使用方法:
 * node danmaku-designer.js --duration <分钟> --topic <主题> [options]
 */

const fs = require('fs');
const path = require('path');

// 弹幕模板库
const DANMAKU_TEMPLATES = {
  opening: [
    "来了来了",
    "前排围观",
    "第一！",
    "热乎的",
    "刚出炉",
    "来了",
    "打卡",
  ],
  shocking: [
    "???",
    "卧槽",
    "离谱",
    "震惊",
    "不会吧",
    "真的假的",
    "我人傻了",
  ],
  agreement: [
    "真实",
    "太对了",
    "我也是",
    "同意",
    "确实",
    "正确的",
    "一针见血",
  ],
  question: [
    "选A",
    "选B",
    "我选C",
    "都不选",
    "全都要",
  ],
  ending: [
    "三连了",
    "投币支持",
    "下次一定",
    "催更",
    "下期见",
    "辛苦了",
  ],
};

// 彩蛋模板
const EASTER_EGGS = [
  { trigger: "老粉集合", response: "这里这里", time: "random" },
  { trigger: "暗号", response: "天王盖地虎", time: "random" },
  { trigger: "催更", response: "生产队的驴", time: "ending" },
];

/**
 * 主函数
 */
async function main() {
  const args = parseArgs();
  
  if (!args.duration || !args.topic) {
    console.error('错误: 必须提供 --duration 和 --topic 参数');
    printUsage();
    process.exit(1);
  }

  console.log('🎨 Bilibili 弹幕互动设计工具');
  console.log(`视频时长: ${args.duration} 分钟`);
  console.log(`主题: ${args.topic}`);
  console.log('');

  const design = generateDanmakuDesign(args);
  
  // 输出到文件或控制台
  const output = formatOutput(design);
  
  if (args.output) {
    fs.writeFileSync(args.output, output);
    console.log(`✅ 设计方案已保存: ${args.output}`);
  } else {
    console.log(output);
  }
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = {};
  const argv = process.argv.slice(2);
  
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  
  return args;
}

/**
 * 打印用法
 */
function printUsage() {
  console.log('');
  console.log('用法:');
  console.log('  node danmaku-designer.js --duration <分钟> --topic <主题> [options]');
  console.log('');
  console.log('参数:');
  console.log('  --duration <分钟>    视频时长 (必需)');
  console.log('  --topic <主题>       视频主题 (必需)');
  console.log('  --style <风格>       视频风格 (知识/娱乐/教程)');
  console.log('  --keywords <关键词>  关键词，逗号分隔');
  console.log('  --output <文件>      输出文件路径');
  console.log('');
  console.log('示例:');
  console.log('  node danmaku-designer.js --duration 10 --topic "AI工具介绍"');
}

/**
 * 生成弹幕设计方案
 */
function generateDanmakuDesign(args) {
  const duration = parseInt(args.duration);
  const topic = args.topic;
  const style = args.style || '知识';
  const keywords = args.keywords ? args.keywords.split(',') : [];
  
  // 计算关键时间点
  const triggers = calculateTriggers(duration, style);
  
  // 生成种子弹幕
  const seedDanmaku = generateSeedDanmaku(topic, style, keywords);
  
  // 生成彩蛋
  const easterEggs = generateEasterEggs(topic);
  
  // 生成互动问题
  const questions = generateQuestions(topic, style);
  
  return {
    duration,
    topic,
    style,
    keywords,
    triggers,
    seedDanmaku,
    easterEggs,
    questions,
  };
}

/**
 * 计算弹幕触发点
 */
function calculateTriggers(duration, style) {
  const triggers = [];
  
  // 开场（0-0.5%）
  triggers.push({
    time: '0:03',
    moment: '开场白',
    type: '口号型',
    expected: '来了来了,前排,第一',
    density: '高',
  });
  
  // 根据风格设置不同触发点
  if (style === '知识') {
    // 知识点揭示（20-30%）
    const revealTime = Math.floor(duration * 0.25 * 60);
    triggers.push({
      time: formatTime(revealTime),
      moment: '核心知识点揭示',
      type: '震惊型',
      expected: '???,原来如此,学到了',
      density: '高',
    });
    
    // 案例讲解（50-60%）
    const caseTime = Math.floor(duration * 0.55 * 60);
    triggers.push({
      time: formatTime(caseTime),
      moment: '实际案例',
      type: '共鸣型',
      expected: '真实,我也是,太对了',
      density: '中',
    });
  } else if (style === '娱乐') {
    // 笑点（随机）
    const funnyTime = Math.floor(duration * 0.3 * 60);
    triggers.push({
      time: formatTime(funnyTime),
      moment: '笑点/梗',
      type: '梗型',
      expected: '哈哈哈哈,笑死,绝了',
      density: '高',
    });
  }
  
  // 互动问题（70-80%）
  const questionTime = Math.floor(duration * 0.75 * 60);
  triggers.push({
    time: formatTime(questionTime),
    moment: '互动提问',
    type: '问答型',
    expected: '选A,选B,我选C',
    density: '中',
  });
  
  // 结尾（90-100%）
  const endingTime = Math.floor(duration * 0.9 * 60);
  triggers.push({
    time: formatTime(endingTime),
    moment: '结尾/总结',
    type: '结尾型',
    expected: '三连,投币,下次一定',
    density: '高',
  });
  
  return triggers;
}

/**
 * 格式化时间
 */
function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * 生成种子弹幕
 */
function generateSeedDanmaku(topic, style, keywords) {
  const seeds = [];
  
  // 基础种子
  seeds.push(...DANMAKU_TEMPLATES.opening.slice(0, 3));
  seeds.push(...DANMAKU_TEMPLATES.ending.slice(0, 3));
  
  // 根据主题生成
  if (style === '知识') {
    seeds.push("学到了", "干货", "记笔记", "收藏了");
  } else if (style === '娱乐') {
    seeds.push("哈哈哈哈", "笑死", "绝了", "名场面");
  } else if (style === '教程') {
    seeds.push("学会了", "感谢", "有用", "已三连");
  }
  
  // 根据关键词生成
  keywords.forEach(keyword => {
    seeds.push(`${keyword}来了`, `关于${keyword}`);
  });
  
  // 去重并限制数量
  return [...new Set(seeds)].slice(0, 15);
}

/**
 * 生成彩蛋
 */
function generateEasterEggs(topic) {
  return EASTER_EGGS.map(egg => ({
    trigger: egg.trigger,
    response: egg.response,
    time: egg.time === 'random' ? '随机' : '结尾',
  }));
}

/**
 * 生成互动问题
 */
function generateQuestions(topic, style) {
  const questions = [];
  
  if (style === '知识') {
    questions.push({
      question: `你平时用什么${topic}？`,
      options: ['A', 'B', 'C', '其他'],
      expected: 'mixed',
    });
  } else {
    questions.push({
      question: `你喜欢这期${topic}吗？`,
      options: ['喜欢', '超喜欢', '非常喜欢'],
      expected: 'all',
    });
  }
  
  return questions;
}

/**
 * 格式化输出
 */
function formatOutput(design) {
  const lines = [];
  
  lines.push('# 弹幕互动设计方案');
  lines.push('');
  lines.push('## 视频信息');
  lines.push(`- 时长: ${design.duration} 分钟`);
  lines.push(`- 主题: ${design.topic}`);
  lines.push(`- 风格: ${design.style}`);
  if (design.keywords.length > 0) {
    lines.push(`- 关键词: ${design.keywords.join(', ')}`);
  }
  lines.push('');
  
  lines.push('## 弹幕触发点');
  lines.push('');
  lines.push('| 时间戳 | 内容时刻 | 弹幕类型 | 预期弹幕 | 密度 |');
  lines.push('|--------|----------|----------|----------|------|');
  design.triggers.forEach(t => {
    lines.push(`| ${t.time} | ${t.moment} | ${t.type} | ${t.expected} | ${t.density} |`);
  });
  lines.push('');
  
  lines.push('## 种子弹幕（10-15条）');
  lines.push('');
  design.seedDanmaku.forEach((seed, i) => {
    lines.push(`${i + 1}. "${seed}"`);
  });
  lines.push('');
  
  lines.push('## 老粉彩蛋');
  lines.push('');
  design.easterEggs.forEach(egg => {
    lines.push(`- **触发**: "${egg.trigger}"`);
    lines.push(`  **回应**: "${egg.response}"`);
    lines.push(`  **时机**: ${egg.time}`);
    lines.push('');
  });
  
  lines.push('## 互动问题');
  lines.push('');
  design.questions.forEach((q, i) => {
    lines.push(`${i + 1}. **Q**: ${q.question}`);
    lines.push(`   **选项**: ${q.options.join(' / ')}`);
    lines.push(`   **预期**: ${q.expected}`);
    lines.push('');
  });
  
  lines.push('---');
  lines.push('*自动生成于 ' + new Date().toLocaleString() + '*');
  
  return lines.join('\n');
}

// 运行
main().catch(console.error);
