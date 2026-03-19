#!/usr/bin/env node
/**
 * 半自动发布 - 墨墨填写内容，哥哥手动完成发布
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
  const articleFile = process.argv[2] || 'articles/test-publish.md';
  
  console.log('\n🌐 半自动发布模式\n');
  console.log('📄 文章:', articleFile);
  
  // 读取文章
  const articleContent = fs.readFileSync(path.join(BASE_DIR, articleFile), 'utf-8');
  const article = {
    title: articleContent.split('\n')[0].replace('# ', '').trim(),
    content: articleContent
  };
  
  console.log('📰 标题:', article.title);
  console.log('\n👉 流程:');
  console.log('   1. 墨墨自动填写标题和正文');
  console.log('   2. 哥哥手动选择分类: 游戏-游戏资讯');
  console.log('   3. 哥哥手动添加封面');
  console.log('   4. 哥哥点击发布\n');

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
  console.log('🌐 打开编辑页面...');
  await page.goto('https://baijiahao.baidu.com/builder/rc/edit?type=news');
  await page.waitForTimeout(5000);
  
  // 填写标题
  console.log('✏️ 填写标题...');
  await page.fill('.cheetah-input', article.title);
  console.log('✅ 标题填写完成');
  
  // 填写正文
  console.log('✏️ 填写正文...');
  await page.fill('[contenteditable="true"]', article.content);
  console.log('✅ 正文填写完成');
  
  console.log('\n✅ 墨墨部分完成！');
  console.log('👉 请哥哥现在:');
  console.log('   1. 选择分类: 游戏 → 游戏资讯');
  console.log('   2. 添加封面');
  console.log('   3. 点击发布按钮');
  console.log('\n完成后按回车...');
  
  await new Promise(resolve => rl.question('', resolve));
  
  console.log('\n✅ 半自动发布流程完成！');
  console.log('👉 按回车关闭浏览器');
  
  await new Promise(resolve => rl.question('', resolve));
  await browser.close();
  rl.close();
}

main().catch(console.error);
