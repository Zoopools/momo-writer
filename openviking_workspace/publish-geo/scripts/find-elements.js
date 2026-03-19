#!/usr/bin/env node
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  console.log('🔍 查找页面元素\n');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    storageState: path.join(__dirname, '..', 'auth', 'bjh-work.json')
  });
  const page = await context.newPage();

  await page.goto('https://baijiahao.baidu.com', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);

  // 查找所有包含"发布"的元素
  const elements = await page.$$('*');
  console.log(`找到 ${elements.length} 个元素\n`);

  let count = 0;
  for (const el of elements) {
    try {
      const text = await el.textContent();
      if (text && text.includes('发布')) {
        const tag = await el.evaluate(e => e.tagName);
        const className = await el.getAttribute('class');
        console.log(`[${count}] ${tag} class="${className}" text="${text.substring(0, 50)}"`);
        count++;
        if (count >= 10) break;
      }
    } catch (e) {}
  }

  // 查找所有 input
  console.log('\n📝 所有 input 元素:');
  const inputs = await page.$$('input');
  for (let i = 0; i < Math.min(inputs.length, 10); i++) {
    try {
      const type = await inputs[i].getAttribute('type');
      const placeholder = await inputs[i].getAttribute('placeholder');
      const className = await inputs[i].getAttribute('class');
      console.log(`[${i}] type=${type}, placeholder="${placeholder}", class="${className}"`);
    } catch (e) {}
  }

  await browser.close();
})();
