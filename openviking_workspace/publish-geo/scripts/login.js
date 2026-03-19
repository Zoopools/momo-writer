#!/usr/bin/env node
/**
 * GEO 发布系统 - 登录态导出脚本
 * 路径: ~/Documents/openclaw/openviking_workspace/publish-geo/scripts/login.js
 * 
 * 使用方法: node scripts/login.js <platform>
 * 示例: node scripts/login.js bjh-work
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// 路径绝对对齐 - 严格使用同步仓库路径
const BASE_DIR = path.resolve(__dirname, '..');
const AUTH_DIR = path.join(BASE_DIR, 'auth');
const LOGS_DIR = path.join(BASE_DIR, 'logs');

// 确保目录存在
if (!fs.existsSync(AUTH_DIR)) {
  fs.mkdirSync(AUTH_DIR, { recursive: true });
}
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

// 平台配置
const PLATFORMS = {
  'bjh-work': {
    name: '百家号工作号',
    url: 'https://baijiahao.baidu.com',
    description: '百家号创作者平台 - 工作账号'
  },
  'bjh-personal': {
    name: '百家号个人号',
    url: 'https://baijiahao.baidu.com',
    description: '百家号创作者平台 - 个人账号'
  },
  'wechat-mp': {
    name: '微信公众号',
    url: 'https://mp.weixin.qq.com',
    description: '微信公众平台'
  },
  'zhihu': {
    name: '知乎',
    url: 'https://www.zhihu.com',
    description: '知乎创作中心'
  }
};

async function exportAuth(platform) {
  const config = PLATFORMS[platform];
  if (!config) {
    console.error(`❌ 未知平台: ${platform}`);
    console.log(`可用平台: ${Object.keys(PLATFORMS).join(', ')}`);
    process.exit(1);
  }

  const authFile = path.join(AUTH_DIR, `${platform}.json`);
  const logFile = path.join(LOGS_DIR, `login-${platform}-${Date.now()}.log`);

  console.log(`\n🚀 [${config.name}] 登录态导出`);
  console.log(`📍 目标: ${config.url}`);
  console.log(`💾 保存路径: ${authFile}`);
  console.log(`\n⚠️  请确保 Chrome 已启动调试模式:`);
  console.log(`    /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9223`);
  console.log(`\n⏳ 在 Chrome 中完成登录，然后按回车保存...\n`);

  // 连接新的 Chrome 实例（调试模式）
  let browser;
  try {
    browser = await chromium.connectOverCDP('http://127.0.0.1:9223');
    console.log('✅ 已连接到 Chrome (CDP: 9223)');
  } catch (e) {
    console.error('❌ 无法连接到 Chrome，请确保:');
    console.error('   1. 已用上面命令启动新的 Chrome');
    console.error('   2. 端口 9223 未被占用');
    throw e;
  }

  // 使用默认上下文（哥哥的 Chrome）
  const context = browser.contexts()[0] || await browser.newContext();
  
  // 查找或创建页面
  let page = context.pages()[0];
  if (!page) {
    page = await context.newPage();
  }

  // 打开登录页面
  console.log(`🌐 正在打开: ${config.url}`);
  await page.goto(config.url, { waitUntil: 'networkidle' });

  // 记录日志
  const logStream = fs.createWriteStream(logFile, { flags: 'a' });
  logStream.write(`[${new Date().toISOString()}] 打开页面: ${config.url}\n`);

  // 等待用户按回车
  await new Promise(resolve => {
    process.stdin.once('data', () => resolve());
  });

  // 保存登录态
  await context.storageState({ path: authFile });
  logStream.write(`[${new Date().toISOString()}] 登录态已保存\n`);

  // 注意：不关闭 browser，因为是哥哥的 Chrome
  console.log('🔌 断开与 Chrome 的连接（Chrome 继续运行）');

  console.log(`\n✅ [${config.name}] 登录态导出成功!`);
  console.log(`📁 文件: ${authFile}`);
  console.log(`📝 日志: ${logFile}`);
  console.log(`\n💡 提示: 现在可以使用 publish.js 进行自动发布了\n`);
}

// 主程序
const platform = process.argv[2];

if (!platform) {
  console.log('使用方法: node scripts/login.js <platform>');
  console.log('\n可用平台:');
  Object.entries(PLATFORMS).forEach(([key, config]) => {
    console.log(`  ${key.padEnd(15)} - ${config.name}`);
  });
  console.log('\n示例: node scripts/login.js bjh-work');
  process.exit(0);
}

exportAuth(platform).catch(err => {
  console.error('❌ 导出失败:', err.message);
  process.exit(1);
});
