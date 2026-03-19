#!/usr/bin/env node
/**
 * Bilibili Page Tester - 测试 B站上传页面元素
 * 
 * 用于探测页面选择器，帮助完善 bilibili-poster.js
 */

const { chromium } = require('playwright');

const CONFIG = {
  bilibiliUploadUrl: 'https://member.bilibili.com/platform/upload/video/frame',
  headless: false,
  slowMo: 100,
};

async function main() {
  console.log('🔍 Bilibili 页面上元素探测工具');
  console.log('================================');
  console.log('');

  const browser = await chromium.launch({
    headless: CONFIG.headless,
    slowMo: CONFIG.slowMo,
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
  });

  const page = await context.newPage();

  try {
    // 打开 B站上传页面
    console.log('1. 打开 B站上传页面...');
    await page.goto(CONFIG.bilibiliUploadUrl);
    await page.waitForTimeout(3000);

    // 探测登录状态
    console.log('');
    console.log('2. 探测登录状态...');
    const loginSelectors = [
      '.header-login-entry',
      '.login-btn',
      '[class*="login"]',
      'a[href*="login"]',
    ];

    for (const selector of loginSelectors) {
      const element = await page.$(selector);
      if (element) {
        console.log(`  ✓ 找到登录按钮: ${selector}`);
        const text = await element.textContent();
        console.log(`    文本: ${text?.trim()}`);
      }
    }

    // 探测文件上传输入框
    console.log('');
    console.log('3. 探测文件上传元素...');
    const fileInputSelectors = [
      'input[type="file"]',
      'input[accept*="video"]',
      '[class*="upload"] input[type="file"]',
    ];

    for (const selector of fileInputSelectors) {
      const element = await page.$(selector);
      if (element) {
        console.log(`  ✓ 找到文件输入框: ${selector}`);
        const accept = await element.getAttribute('accept');
        console.log(`    accept: ${accept}`);
      }
    }

    // 探测标题输入框
    console.log('');
    console.log('4. 探测标题输入框...');
    const titleSelectors = [
      'input[placeholder*="标题"]',
      'input[name*="title"]',
      'input[id*="title"]',
      '[class*="title"] input',
    ];

    for (const selector of titleSelectors) {
      const element = await page.$(selector);
      if (element) {
        console.log(`  ✓ 找到标题输入框: ${selector}`);
        const placeholder = await element.getAttribute('placeholder');
        console.log(`    placeholder: ${placeholder}`);
      }
    }

    // 探测描述输入框
    console.log('');
    console.log('5. 探测描述输入框...');
    const descSelectors = [
      'textarea[placeholder*="简介"]',
      'textarea[placeholder*="描述"]',
      'textarea[name*="desc"]',
      '[class*="desc"] textarea',
    ];

    for (const selector of descSelectors) {
      const element = await page.$(selector);
      if (element) {
        console.log(`  ✓ 找到描述输入框: ${selector}`);
        const placeholder = await element.getAttribute('placeholder');
        console.log(`    placeholder: ${placeholder}`);
      }
    }

    // 探测标签输入框
    console.log('');
    console.log('6. 探测标签输入框...');
    const tagSelectors = [
      'input[placeholder*="标签"]',
      'input[placeholder*="tag"]',
      '[class*="tag"] input',
    ];

    for (const selector of tagSelectors) {
      const element = await page.$(selector);
      if (element) {
        console.log(`  ✓ 找到标签输入框: ${selector}`);
        const placeholder = await element.getAttribute('placeholder');
        console.log(`    placeholder: ${placeholder}`);
      }
    }

    // 探测封面上传
    console.log('');
    console.log('7. 探测封面上传...');
    const coverSelectors = [
      '[class*="cover"]',
      '[class*="cover"] button',
      '[class*="cover"] input[type="file"]',
    ];

    for (const selector of coverSelectors) {
      const element = await page.$(selector);
      if (element) {
        console.log(`  ✓ 找到封面元素: ${selector}`);
      }
    }

    // 探测分区选择
    console.log('');
    console.log('8. 探测分区选择...');
    const partitionSelectors = [
      '[class*="partition"]',
      '[class*="category"]',
      '[class*="type"]',
    ];

    for (const selector of partitionSelectors) {
      const element = await page.$(selector);
      if (element) {
        console.log(`  ✓ 找到分区选择器: ${selector}`);
        const text = await element.textContent();
        console.log(`    文本: ${text?.substring(0, 50)}...`);
      }
    }

    // 探测提交按钮
    console.log('');
    console.log('9. 探测提交按钮...');
    const submitSelectors = [
      'button[type="submit"]',
      'button:has-text("提交")',
      'button:has-text("投稿")',
      'button:has-text("发布")',
      '[class*="submit"]',
    ];

    for (const selector of submitSelectors) {
      try {
        const element = await page.$(selector);
        if (element) {
          console.log(`  ✓ 找到提交按钮: ${selector}`);
          const text = await element.textContent();
          console.log(`    文本: ${text?.trim()}`);
        }
      } catch (e) {
        // 忽略错误
      }
    }

    console.log('');
    console.log('================================');
    console.log('✅ 页面探测完成！');
    console.log('');
    console.log('提示:');
    console.log('- 如果未登录，请先手动登录');
    console.log('- 根据探测结果更新 bilibili-poster.js 中的选择器');
    console.log('- 按 Ctrl+C 关闭浏览器');

    // 保持浏览器打开
    await new Promise(() => {});

  } catch (error) {
    console.error('❌ 错误:', error.message);
  }
}

main().catch(console.error);
