#!/usr/bin/env node
/**
 * 手动辅助工具 - 哥哥点击后墨墨分析
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

async function main() {
  console.log('\n🌐 启动辅助浏览器\n');
  console.log('👉 请哥哥手动操作：');
  console.log('   1. 在浏览器中点击"发布图文"');
  console.log('   2. 进入编辑页面后，回到这里按回车');
  console.log('   3. 墨墨会分析页面结构\n');

  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 100
  });

  const context = await browser.newContext({
    storageState: path.join(AUTH_DIR, 'bjh-work.json'),
    viewport: { width: 1280, height: 720 }
  });

  const page = await context.newPage();

  // 打开发布页
  await page.goto('https://baijiahao.baidu.com/builder/article/edit?type=imgtxt');
  console.log('✅ 浏览器已打开\n');

  // 等待哥哥操作
  await new Promise(resolve => {
    rl.question('哥哥进入编辑页后按回车...', resolve);
  });

  console.log('\n🔍 分析页面结构...');

  // 获取所有 iframe
  const frames = page.frames();
  console.log(`\n发现 ${frames.length} 个 frame:`);
  for (let i = 0; i < frames.length; i++) {
    console.log(`  [${i}] ${frames[i].url().substring(0, 60)}`);
  }

  // 查找所有 input
  console.log('\n📝 查找所有 input 元素:');
  const inputs = await page.$$('input, [contenteditable="true"]');
  console.log(`  找到 ${inputs.length} 个可输入元素`);
  
  for (let i = 0; i < Math.min(inputs.length, 10); i++) {
    try {
      const tag = await inputs[i].evaluate(el => el.tagName);
      const placeholder = await inputs[i].getAttribute('placeholder');
      const className = await inputs[i].getAttribute('class');
      const id = await inputs[i].getAttribute('id');
      console.log(`\n  [${i}] ${tag}`);
      console.log(`      placeholder: ${placeholder}`);
      console.log(`      class: ${className?.substring(0, 50)}`);
      console.log(`      id: ${id}`);
    } catch (e) {}
  }

  // 截图
  await page.screenshot({ 
    path: path.join(BASE_DIR, 'logs', `manual-edit-page-${Date.now()}.png`),
    fullPage: true 
  });
  console.log('\n📸 截图已保存');

  console.log('\n✅ 分析完成！请把上面的信息发给 Gemini\n');
  console.log('👉 按回车关闭浏览器');
  
  await new Promise(resolve => rl.question('', resolve));
  await browser.close();
  rl.close();
}

main().catch(console.error);
