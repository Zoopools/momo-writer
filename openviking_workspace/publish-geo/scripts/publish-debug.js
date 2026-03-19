#!/usr/bin/env node
/**
 * GEO 发布系统 - 调试版本
 * 在关键位置暂停，供哥哥检查
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

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

// 暂停函数
async function pause(message) {
  console.log(`\n⏸️  ${message}`);
  console.log('👉 按回车继续...\n');
  await new Promise(resolve => rl.question('', resolve));
}

// 随机延迟
async function randomDelay(page, min = 500, max = 2000) {
  const delay = Math.floor(Math.random() * (max - min + 1)) + min;
  await page.waitForTimeout(delay);
}

// ===== 物理清场 =====
async function destroyAllMasks(page) {
  console.log('💥 物理清场: 摧毁所有蒙版...');
  await page.evaluate(() => {
    document.querySelectorAll('[mask]').forEach(el => el.removeAttribute('mask'));
    const tourSelectors = ['[class*="mask"]', '[class*="tour"]', '.cheetah-tour', 'svg:has(defs)', '[class*="overlay"]'];
    tourSelectors.forEach(s => {
      document.querySelectorAll(s).forEach(el => {
        if (el.tagName === 'svg' || el.className.includes('tour') || el.className.includes('mask')) {
          el.remove();
        }
      });
    });
    document.body.style.overflow = 'auto';
    document.body.style.pointerEvents = 'auto';
    document.body.style.filter = 'none';
  });
  await randomDelay(page, 2000, 3000);
  console.log('✅ 清场完成');
}

// ===== 主流程 =====
async function main() {
  const articleFile = process.argv[2] || 'articles/test-publish.md';
  
  console.log('\n🐛 调试模式 - 关键位置会暂停\n');
  console.log('📄 文章:', articleFile);
  
  // 读取文章
  const articleContent = fs.readFileSync(path.join(BASE_DIR, articleFile), 'utf-8');
  const lines = articleContent.split('\n');
  
  // 提取标题（第一行，去掉#，只保留10个字）
  let title = lines[0].replace('# ', '').trim().substring(0, 10);
  console.log('📰 标题(10字):', title);
  
  // 不提取正文（测试是否标题问题）
  const article = { title, content: '' };
  console.log('📰 标题:', article.title);
  
  // 启动浏览器
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
    args: ['--disable-blink-features=AutomationControlled']
  });
  
  const context = await browser.newContext({
    storageState: path.join(AUTH_DIR, 'bjh-work.json'),
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  // 打开编辑页
  console.log('🌐 打开编辑页面...');
  await page.goto('https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1', {
    waitUntil: 'networkidle',
    timeout: 60000
  });
  await randomDelay(page, 5000, 8000);
  
  // 暂停 1: 检查页面加载
  await pause('【图一位置】页面已加载，请检查是否有报错或异常');
  
  // 物理清场
  await destroyAllMasks(page);
  
  // 填写标题
  console.log('✏️ 填写标题...');
  await page.fill('.cheetah-input', article.title);
  console.log('✅ 标题完成');
  
  // 填写正文
  console.log('✏️ 填写正文...');
  await page.fill('[contenteditable="true"]', article.content);
  console.log('✅ 正文完成');
  
  // 跳过分类选择和封面上传，直接测试发布
  console.log('⏭️  跳过分类和封面，直接测试发布按钮...');
  
  // 直接点击发布按钮
  console.log('🚀 点击发布按钮...');
  await page.click('[data-testid="publish-btn"]', { force: true });
  await page.waitForTimeout(10000);
  
  // 检查是否有报错弹窗
  console.log('🔍 检查报错...');
  await page.screenshot({ path: path.join(LOGS_DIR, `debug-publish-attempt-${Date.now()}.png`), fullPage: true });
  
  // 暂停查看结果
  await pause('【检查点】已点击发布，请查看是否有报错弹窗');
  
  // 关闭浏览器
  console.log('\n✅ 调试完成');
  await browser.close();
  rl.close();
}

main().catch(console.error);
