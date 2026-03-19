#!/usr/bin/env node
/**
 * GEO 发布系统 - 交互式登录态导出
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const BASE_DIR = path.resolve(__dirname, '..');
const AUTH_DIR = path.join(BASE_DIR, 'auth');

if (!fs.existsSync(AUTH_DIR)) fs.mkdirSync(AUTH_DIR, { recursive: true });

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function exportAuth() {
  console.log('\n🚀 百家号登录态导出');
  console.log('💾 保存路径: ~/Documents/openclaw/openviking_workspace/publish-geo/auth/bjh-work.json\n');

  // 启动浏览器
  console.log('🌐 正在启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    slowMo: 50
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai'
  });

  const page = await context.newPage();

  // 打开百家号
  console.log('📍 正在打开 https://baijiahao.baidu.com');
  await page.goto('https://baijiahao.baidu.com', { waitUntil: 'networkidle' });

  console.log('\n✅ 浏览器已打开！');
  console.log('👉 请在浏览器中完成登录');
  console.log('👉 登录成功后，回到这里输入 "ok" 并按回车\n');

  // 等待用户输入
  const answer = await new Promise(resolve => {
    rl.question('登录完成后请输入 "ok": ', resolve);
  });

  if (answer.trim().toLowerCase() !== 'ok') {
    console.log('❌ 取消导出');
    await browser.close();
    rl.close();
    process.exit(0);
  }

  // 保存登录态
  const authFile = path.join(AUTH_DIR, 'bjh-work.json');
  await context.storageState({ path: authFile });

  await browser.close();
  rl.close();

  // 验证文件
  if (fs.existsSync(authFile)) {
    const stats = fs.statSync(authFile);
    console.log(`\n✅ 登录态导出成功!`);
    console.log(`📁 文件: ${authFile}`);
    console.log(`📊 大小: ${stats.size} bytes`);
    console.log(`\n💡 现在可以运行: node scripts/publish.js bjh-work <article.md>\n`);
  } else {
    console.log('❌ 导出失败，文件未创建');
    process.exit(1);
  }
}

exportAuth().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
