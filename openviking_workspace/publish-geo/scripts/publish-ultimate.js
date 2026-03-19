#!/usr/bin/env node
/**
 * GEO 发布系统 - 终极毁灭方案
 * Gemini 焦土策略 - 清除所有遮罩
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

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

// ===== Gemini 终极毁灭: 物理清场 =====
async function destroyAllMasks(page) {
  console.log('💥 物理清场: 摧毁所有蒙版...');
  await page.evaluate(() => {
    // 1. 移除所有蒙版 ID 引用
    document.querySelectorAll('[mask]').forEach(el => el.removeAttribute('mask'));
    
    // 2. 移除所有包含 "mask" 或 "tour" 类名的节点
    const tourSelectors = [
      '[class*="mask"]', 
      '[class*="tour"]', 
      '.cheetah-tour', 
      'svg:has(defs)',
      '[class*="overlay"]',
      '[class*="backdrop"]'
    ];
    tourSelectors.forEach(s => {
      document.querySelectorAll(s).forEach(el => {
        if (el.tagName === 'svg' || el.className.includes('tour') || el.className.includes('mask')) {
          el.remove();
        }
      });
    });
    
    // 3. 强制恢复 Body 滚动和点击
    document.body.style.overflow = 'auto';
    document.body.style.pointerEvents = 'auto';
    document.body.style.filter = 'none';
    
    console.log('[Matrix] 蒙版防御系统已彻底瓦解');
  });
  await randomDelay(page, 2000, 3000);
  console.log('✅ 清场完成');
}

// ===== Gemini 键盘注入补完 =====
async function keyboardSelectCategory(page) {
  console.log('📂 选择分类: 键盘注入...');
  
  try {
    const categoryTrigger = page.locator('.cheetah-select').first();
    await categoryTrigger.scrollIntoViewIfNeeded();
    
    // 连按三次下箭头，确保穿透 React 异步加载
    console.log('⌨️ 键盘注入: 3x ArrowDown + Enter...');
    await categoryTrigger.click({ force: true, delay: 500 });
    await page.waitForTimeout(1000);
    
    for(let i=0; i<3; i++) {
      await page.keyboard.press('ArrowDown');
      await page.waitForTimeout(300);
    }
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    
    // 再次选择二级分类
    for(let i=0; i<2; i++) {
      await page.keyboard.press('ArrowDown');
      await page.waitForTimeout(300);
    }
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    
    console.log('✅ 键盘注入完成');
    return true;
  } catch (e) {
    console.log('❌ 键盘注入失败:', e.message);
    return false;
  }
}

// ===== Gemini 紧急路径修复: 自动寻找封面 =====
async function findAndUploadCover(page) {
  console.log('🖼️ 寻找封面...');
  
  // 自动寻找可用封面
  const possiblePaths = [
    path.join(BASE_DIR, 'assets', 'cover.jpg'),
    path.join(BASE_DIR, 'assets', 'default-cover.jpg'),
    path.join(process.env.HOME, 'Documents/openclaw/assets/cover.jpg'),
    path.join(LOGS_DIR, 'debug-1-home.png'), // 用调试图占位
  ];
  
  const finalCover = possiblePaths.find(p => fs.existsSync(p));
  
  if (!finalCover) {
    console.log('⚠️ 全局搜寻不到封面图，跳过封面上传');
    return false;
  }
  
  console.log('✅ 找到封面:', finalCover);
  
  try {
    // 切换到单图模式
    await page.click('text=单图', { force: true });
    await page.waitForTimeout(1000);
    
    // 直接设置文件
    const fileInput = page.locator('input[type="file"]').first();
    await fileInput.setInputFiles(finalCover);
    await page.waitForTimeout(3000);
    
    // 处理确认弹窗
    try {
      await page.click('button:has-text("确定"), .cheetah-btn-primary', { force: true });
      await page.waitForTimeout(2000);
    } catch (e) {
      console.log('[Matrix] 无确认弹窗');
    }
    
    console.log('✅ 封面上传完成');
    return true;
  } catch (e) {
    console.log('❌ 封面上传失败:', e.message);
    return false;
  }
}

// ===== 主流程 =====
async function publishArticle(articleFile) {
  console.log('\n🚀 终极毁灭方案 - 焦土策略');
  console.log('📄 文章:', articleFile);
  
  // 读取文章
  const articleContent = fs.readFileSync(path.join(BASE_DIR, articleFile), 'utf-8');
  const lines = articleContent.split('\n');
  const article = {
    title: lines[0].replace('# ', '').trim(),
    content: lines.slice(1).join('\n').trim() // 去掉标题行
  };
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
  
  try {
    // 打开编辑页
    console.log('🌐 打开编辑页面...');
    await page.goto('https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1', {
      waitUntil: 'networkidle',
      timeout: 60000
    });
    await randomDelay(page, 5000, 8000);
    
    // 物理清场
    await destroyAllMasks(page);
    
    // 填写标题
    console.log('✏️ 填写标题...');
    await page.fill('.cheetah-input', article.title);
    await randomDelay(page, 1000, 2000);
    console.log('✅ 标题完成');
    
    // 填写正文
    console.log('✏️ 填写正文...');
    await page.fill('[contenteditable="true"]', article.content);
    await randomDelay(page, 1000, 2000);
    console.log('✅ 正文完成');
    
    // 键盘选择分类
    const categoryOk = await keyboardSelectCategory(page);
    
    // 寻找并上传封面
    const coverOk = await findAndUploadCover(page);
    
    // 点击发布
    console.log('🚀 撞击发布按钮...');
    await page.click('[data-testid="publish-btn"]', { force: true });
    await randomDelay(page, 10000, 15000);
    
    // 处理可能的确认弹窗
    console.log('🔍 检查确认弹窗...');
    try {
      await page.click('button:has-text("确定"), button:has-text("确认"), button:has-text("发布")', { force: true, timeout: 10000 });
      console.log('✅ 确认弹窗已处理');
      await randomDelay(page, 10000, 15000);
    } catch (e) {
      console.log('  无确认弹窗或已处理');
    }
    
    // 监测 URL 变更
    console.log('🔍 监测发布结果...');
    const finalUrl = page.url();
    console.log('📍 最终URL:', finalUrl);
    
    await page.screenshot({ path: path.join(LOGS_DIR, `ultimate-final-${Date.now()}.png`), fullPage: true });
    
    if (finalUrl.includes('preview') || finalUrl.includes('article_id') || finalUrl.includes('content/manage')) {
      console.log('🏆 全自动发布成功！');
      return { success: true, url: finalUrl };
    } else {
      console.log('⚠️ 请检查发布状态');
      return { success: false, url: finalUrl };
    }
    
  } catch (e) {
    console.error('❌ 错误:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `ultimate-error-${Date.now()}.png`), fullPage: true });
    throw e;
  } finally {
    await browser.close();
  }
}

// 主程序
const articleFile = process.argv[2] || 'articles/test-publish.md';

publishArticle(articleFile).then(result => {
  console.log('\n📊 结果:', result);
  process.exit(result.success ? 0 : 1);
}).catch(err => {
  console.error('\n❌ 错误:', err.message);
  process.exit(1);
});
