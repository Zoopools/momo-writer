#!/usr/bin/env node
/**
 * 录制发布流程 - 哥哥操作，墨墨记录
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
  console.log('\n🎥 录制发布流程\n');
  console.log('👉 请哥哥完成以下步骤：');
  console.log('   1. 检查标题和正文');
  console.log('   2. 选择文章分类（重要！）');
  console.log('   3. 点击"发布"按钮');
  console.log('   4. 如有确认弹窗，点击确认');
  console.log('   5. 等待发布成功页面');
  console.log('   6. 回到这里按回车\n');

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
  console.log('✅ 浏览器已打开');
  console.log('💡 标题和正文已自动填写\n');

  // 自动填写标题和正文
  try {
    await page.fill('.cheetah-input', 'GEO 自动化测试文章 - 录制版');
    await page.fill('[contenteditable="true"]', '这是录制测试的正文内容');
    console.log('✅ 标题和正文已填写\n');
  } catch (e) {
    console.log('⚠️ 自动填写失败，请手动填写\n');
  }

  // 等待哥哥操作
  await new Promise(resolve => {
    rl.question('哥哥完成发布后按回车...', resolve);
  });

  // 记录最终状态
  const finalUrl = page.url();
  const title = await page.title();
  
  console.log('\n📊 录制结果：');
  console.log(`📍 URL: ${finalUrl}`);
  console.log(`📰 标题: ${title}`);

  // 保存录制信息
  const record = {
    timestamp: new Date().toISOString(),
    finalUrl,
    title,
    success: finalUrl.includes('preview') || finalUrl.includes('success')
  };
  
  fs.writeFileSync(
    path.join(BASE_DIR, 'logs', `record-${Date.now()}.json`),
    JSON.stringify(record, null, 2)
  );

  if (record.success) {
    console.log('\n✅ 发布成功！请检查百家号后台');
  } else {
    console.log('\n⚠️ 请检查是否发布成功');
  }

  console.log('\n👉 按回车关闭浏览器');
  await new Promise(resolve => rl.question('', resolve));
  
  await browser.close();
  rl.close();
}

main().catch(console.error);
