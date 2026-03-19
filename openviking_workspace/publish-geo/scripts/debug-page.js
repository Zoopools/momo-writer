#!/usr/bin/env node
/**
 * 调试页面结构
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const AUTH_DIR = path.join(__dirname, '..', 'auth');

async function debug() {
  console.log('🔍 调试百家号页面结构\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    storageState: path.join(AUTH_DIR, 'bjh-work.json')
  });
  const page = await context.newPage();

  // 打开发布页面
  await page.goto('https://baijiahao.baidu.com/builder/preview/s?id=', {
    waitUntil: 'networkidle'
  });

  console.log('✅ 页面已加载');
  console.log('📸 截图保存到: debug-screenshot.png');

  // 截图
  await page.screenshot({ path: path.join(__dirname, '..', 'debug-screenshot.png') });

  // 获取页面 HTML
  const html = await page.content();
  fs.writeFileSync(path.join(__dirname, '..', 'debug-page.html'), html);
  console.log('📄 HTML 保存到: debug-page.html');

  console.log('\n👉 请查看截图和 HTML，分析页面结构');
  console.log('👉 完成后关闭浏览器\n');

  // 等待用户关闭
  await new Promise(() => {});
}

debug().catch(console.error);
