#!/usr/bin/env node
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🔍 调试发布页面\n');

  const browser = await chromium.launch({ 
    headless: false,  // 有界面
    slowMo: 100
  });

  const context = await browser.newContext({
    storageState: path.join(__dirname, '..', 'auth', 'bjh-work.json'),
    viewport: { width: 1280, height: 720 }
  });

  const page = await context.newPage();

  // 打开首页
  await page.goto('https://baijiahao.baidu.com');
  console.log('✅ 首页已打开');
  await page.waitForTimeout(3000);

  // 截图
  await page.screenshot({ path: path.join(__dirname, '..', 'debug-1-home.png') });

  // 点击发布图文
  console.log('🖱️ 点击"发布图文"...');
  await page.click('text=发布图文', { force: true });
  await page.waitForTimeout(5000);

  // 截图发布页面
  await page.screenshot({ path: path.join(__dirname, '..', 'debug-2-publish.png') });
  console.log('📸 截图已保存');

  // 获取页面源码
  const html = await page.content();
  require('fs').writeFileSync(
    path.join(__dirname, '..', 'debug-publish.html'), 
    html
  );

  console.log('✅ 调试完成，请查看截图和 HTML');
  console.log('👉 按回车关闭浏览器');

  await new Promise(resolve => process.stdin.once('data', resolve));
  await browser.close();
})();
