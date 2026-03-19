#!/usr/bin/env node
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🌐 启动调试浏览器...');
  console.log('👉 请手动导航到百家号发布页面');
  console.log('👉 然后查看页面结构\n');

  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 100
  });

  const context = await browser.newContext({
    storageState: path.join(__dirname, '..', 'auth', 'bjh-work.json'),
    viewport: { width: 1280, height: 720 }
  });

  const page = await context.newPage();

  // 打开百家号首页
  await page.goto('https://baijiahao.baidu.com');

  console.log('✅ 浏览器已打开，请：');
  console.log('   1. 点击"发布图文"');
  console.log('   2. 右键点击标题输入框 → 检查');
  console.log('   3. 把 input 元素的 HTML 发给我\n');

  // 保持运行
  await new Promise(() => {});
})();
