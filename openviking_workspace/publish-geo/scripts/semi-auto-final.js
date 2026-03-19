#!/usr/bin/env node
/**
 * 半自动发布 - Gemini 终极方案
 * 墨墨自动填写 + 哥哥手动完成分类/封面 + 墨墨监测发布成功
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

// 随机延迟
async function randomDelay(page, min = 500, max = 2000) {
  const delay = Math.floor(Math.random() * (max - min + 1)) + min;
  await page.waitForTimeout(delay);
}

// ===== Gemini 补丁 1: 模拟真实物理点击 =====
async function realPhysicalClick(page, selector) {
  console.log(`🖱️ 物理点击: ${selector}`);
  const element = page.locator(selector).first();
  const box = await element.boundingBox();
  if (box) {
    // 模拟鼠标移动到元素中心并点击
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.mouse.down();
    await page.mouse.up();
    console.log('✅ 物理点击完成');
  }
}

// ===== Gemini 补丁 2: 强制唤醒 Dropdown =====
async function forceOpenDropdown(page, selector) {
  console.log('🎯 强制唤醒下拉框...');
  const element = page.locator(selector).first();
  
  // 1. Focus
  await element.focus();
  await randomDelay(page, 500, 1000);
  
  // 2. Click with delay
  await element.click({ delay: 100, force: true });
  await randomDelay(page, 1000, 2000);
  
  // 3. 按下空格键（Web 辅助功能通用快捷键）
  await page.keyboard.press('Space');
  await randomDelay(page, 2000, 3000);
  
  console.log('✅ 唤醒完成');
}

// ===== 暴力拆除遮罩 =====
async function removeBlockingMasks(page) {
  console.log('🧹 移除遮罩层...');
  await page.evaluate(() => {
    const masks = document.querySelectorAll('svg rect[fill="transparent"], .cheetah-mask, .ant-modal-mask, [class*="overlay"], [class*="backdrop"]');
    masks.forEach(mask => {
      mask.style.pointerEvents = 'none';
      mask.style.display = 'none';
    });
    console.log(`[Matrix] 已移除 ${masks.length} 个干扰层`);
  });
  await randomDelay(page, 1000, 2000);
}

// ===== 记录 DOM 快照 =====
async function saveDOMSnapshot(page, filename) {
  const html = await page.content();
  fs.writeFileSync(path.join(LOGS_DIR, filename), html);
  console.log(`📸 DOM 快照已保存: ${filename}`);
}

// ===== 主流程 =====
async function main() {
  const articleFile = process.argv[2] || 'articles/test-publish.md';
  
  console.log('\n🌐 半自动发布 - Gemini 终极方案\n');
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
  console.log('   2. 墨墨尝试物理点击唤醒分类下拉框');
  console.log('   3. 哥哥手动选择分类和封面');
  console.log('   4. 墨墨监测发布成功\n');

  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 50
  });

  const context = await browser.newContext({
    storageState: path.join(AUTH_DIR, 'bjh-work.json'),
    viewport: { width: 1280, height: 720 }
  });

  const page = await context.newPage();

  try {
    // 打开编辑页
    console.log('🌐 打开编辑页面...');
    await page.goto('https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1', {
      waitUntil: 'networkidle',
      timeout: 60000
    });
    await randomDelay(page, 5000, 8000);
    
    // 移除遮罩
    await removeBlockingMasks(page);
    
    // 填写标题
    console.log('✏️ 填写标题...');
    await page.fill('.cheetah-input', article.title);
    console.log('✅ 标题填写完成');
    
    // 填写正文
    console.log('✏️ 填写正文...');
    await page.fill('[contenteditable="true"]', article.content);
    console.log('✅ 正文填写完成');
    
    // ===== Gemini 补丁: 物理点击唤醒分类 =====
    console.log('\n🎯 尝试物理点击唤醒分类下拉框...');
    try {
      const categorySelector = '.cheetah-select';
      await realPhysicalClick(page, categorySelector);
      await randomDelay(page, 2000, 3000);
      
      // 如果还没出来，强制唤醒
      await forceOpenDropdown(page, categorySelector);
      
      // 记录 DOM 快照
      await saveDOMSnapshot(page, `debug-dropdown-${Date.now()}.html`);
      
      console.log('✅ 唤醒尝试完成');
    } catch (e) {
      console.log('⚠️ 唤醒失败:', e.message);
    }
    
    // ===== 哥哥手动操作阶段 =====
    console.log('\n' + '='.repeat(50));
    console.log('👉 请哥哥现在手动操作:');
    console.log('   1. 选择分类: 游戏 → 游戏资讯');
    console.log('   2. 添加封面');
    console.log('   3. 点击发布按钮');
    console.log('='.repeat(50) + '\n');
    
    // 等待哥哥操作
    await new Promise(resolve => {
      rl.question('哥哥完成后按回车...', resolve);
    });
    
    // ===== 监测发布成功 =====
    console.log('\n🔍 监测发布状态...');
    const finalUrl = page.url();
    console.log('📍 最终URL:', finalUrl);
    
    // 截图
    await page.screenshot({ 
      path: path.join(LOGS_DIR, `semi-auto-final-${Date.now()}.png`),
      fullPage: true 
    });
    
    // 保存最终 DOM
    await saveDOMSnapshot(page, `semi-auto-final-${Date.now()}.html`);
    
    if (finalUrl.includes('preview') || finalUrl.includes('article_id')) {
      console.log('\n✅ 发布成功！');
    } else {
      console.log('\n⚠️ 请检查百家号后台确认发布状态');
    }
    
    console.log('\n👉 按回车关闭浏览器');
    await new Promise(resolve => rl.question('', resolve));
    
  } catch (e) {
    console.error('❌ 错误:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `semi-auto-error-${Date.now()}.png`) });
  } finally {
    await browser.close();
    rl.close();
  }
}

main().catch(console.error);
