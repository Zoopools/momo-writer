#!/usr/bin/env node
/**
 * 手动发布辅助工具 - 哥哥操作，墨墨记录
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const BASE_DIR = path.resolve(__dirname, '..');
const AUTH_DIR = path.join(BASE_DIR, 'auth');
const LOGS_DIR = path.join(BASE_DIR, 'logs');

async function main() {
  console.log('\n🌐 手动发布辅助工具\n');
  console.log('👉 请哥哥在浏览器中完成以下操作：');
  console.log('   1. 确认标题和正文已填写');
  console.log('   2. 选择文章分类（必填）');
  console.log('   3. 点击"发布"按钮');
  console.log('   4. 如有弹窗，点击确认');
  console.log('   5. 发布后，回到这里按回车\n');

  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 100
  });

  const context = await browser.newContext({
    storageState: path.join(AUTH_DIR, 'bjh-work.json'),
    viewport: { width: 1280, height: 720 }
  });

  const page = await context.newPage();

  // 打开编辑页
  await page.goto('https://baijiahao.baidu.com/builder/rc/edit?type=news');
  console.log('✅ 浏览器已打开\n');

  // 等待哥哥操作
  await new Promise(resolve => {
    rl.question('哥哥完成发布后按回车...', resolve);
  });

  // 获取最终状态
  const finalUrl = page.url();
  console.log(`\n📍 最终URL: ${finalUrl}`);

  // 截图
  await page.screenshot({ 
    path: path.join(LOGS_DIR, `manual-final-${Date.now()}.png`),
    fullPage: true 
  });
  console.log('📸 最终截图已保存');

  // 检查是否发布成功
  if (finalUrl.includes('preview') || finalUrl.includes('success')) {
    console.log('\n✅ 看起来发布成功了！');
  } else {
    console.log('\n⚠️ 请检查百家号后台确认是否发布成功');
  }

  console.log('\n👉 按回车关闭浏览器');
  await new Promise(resolve => rl.question('', resolve));
  
  await browser.close();
  rl.close();
}

main().catch(console.error);
