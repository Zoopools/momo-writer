#!/usr/bin/env node
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  console.log('🔍 获取百家号页面源码\n');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: path.join(__dirname, '..', 'auth', 'bjh-work.json')
  });
  const page = await context.newPage();

  // 先打开首页
  console.log('📍 打开百家号首页...');
  await page.goto('https://baijiahao.baidu.com', {
    waitUntil: 'networkidle',
    timeout: 60000
  });

  await page.waitForTimeout(3000);

  // 获取首页源码
  const html = await page.content();
  const outputFile = path.join(__dirname, '..', 'page-home.html');
  fs.writeFileSync(outputFile, html);

  console.log('✅ 首页源码已保存');
  console.log(`📄 ${outputFile}`);

  // 查找"发布图文"按钮
  const publishBtn = await page.$('text=发布图文, button:has-text("发布图文")');
  if (publishBtn) {
    console.log('\n🎯 找到发布图文按钮，点击...');
    await publishBtn.click();
    await page.waitForTimeout(5000);

    // 获取新页面源码
    const publishHtml = await page.content();
    const publishFile = path.join(__dirname, '..', 'page-publish.html');
    fs.writeFileSync(publishFile, publishHtml);

    console.log('✅ 发布页面源码已保存');
    console.log(`📄 ${publishFile}`);

    // 查找标题输入框
    const inputs = await page.$$('input');
    console.log(`\n📝 找到 ${inputs.length} 个 input 元素`);

    for (let i = 0; i < Math.min(inputs.length, 5); i++) {
      const placeholder = await inputs[i].getAttribute('placeholder');
      const type = await inputs[i].getAttribute('type');
      const outerHTML = await inputs[i].evaluate(el => el.outerHTML.substring(0, 200));
      console.log(`\n[${i}] type=${type}, placeholder=${placeholder}`);
      console.log(outerHTML);
    }
  } else {
    console.log('\n⚠️ 未找到发布图文按钮');
  }

  await browser.close();
})();
