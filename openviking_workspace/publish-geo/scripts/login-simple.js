#!/usr/bin/env node
/**
 * GEO 发布系统 - 登录态导出脚本（简单版）
 * 使用 Playwright 自带浏览器
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_DIR = path.resolve(__dirname, '..');
const AUTH_DIR = path.join(BASE_DIR, 'auth');
const LOGS_DIR = path.join(BASE_DIR, 'logs');

if (!fs.existsSync(AUTH_DIR)) fs.mkdirSync(AUTH_DIR, { recursive: true });
if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });

const PLATFORMS = {
  'bjh-work': {
    name: '百家号工作号',
    url: 'https://baijiahao.baidu.com'
  },
  'bjh-personal': {
    name: '百家号个人号',
    url: 'https://baijiahao.baidu.com'
  },
  'wechat-mp': {
    name: '微信公众号',
    url: 'https://mp.weixin.qq.com'
  },
  'zhihu': {
    name: '知乎',
    url: 'https://www.zhihu.com'
  }
};

async function exportAuth(platform) {
  const config = PLATFORMS[platform];
  if (!config) {
    console.error(`❌ 未知平台: ${platform}`);
    process.exit(1);
  }

  const authFile = path.join(AUTH_DIR, `${platform}.json`);

  console.log(`\n🚀 [${config.name}] 登录态导出`);
  console.log(`📍 目标: ${config.url}`);
  console.log(`💾 保存路径: ${authFile}`);
  console.log(`\n⏳ 请在弹出的浏览器中完成登录，然后回到这里按回车保存...\n`);

  // 启动 Playwright 自带浏览器
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai'
  });

  const page = await context.newPage();

  // 打开登录页面
  await page.goto(config.url, { waitUntil: 'networkidle' });

  // 等待用户按回车
  await new Promise(resolve => {
    process.stdin.once('data', () => resolve());
  });

  // 保存登录态
  await context.storageState({ path: authFile });

  await browser.close();

  console.log(`\n✅ [${config.name}] 登录态导出成功!`);
  console.log(`📁 文件: ${authFile}`);
  console.log(`\n💡 现在可以使用 publish.js 进行自动发布了\n`);
}

const platform = process.argv[2] || 'bjh-work';
exportAuth(platform).catch(err => {
  console.error('❌ 导出失败:', err.message);
  process.exit(1);
});
