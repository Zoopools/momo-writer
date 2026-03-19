#!/usr/bin/env node
/**
 * GEO 发布系统 - 终极全自动方案 v2.0
 * Gemini 键盘注入 + Input 探测
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

// ===== Gemini 补丁 1: 键盘导航大法 =====
async function forceSelectCategory(page) {
  console.log('📂 选择分类: 键盘导航大法...');
  
  try {
    const categoryTrigger = page.locator('.cheetah-select').filter({ hasText: /选择分类|分类/ }).first();
    await categoryTrigger.scrollIntoViewIfNeeded();
    
    // 1. 真实物理点击
    console.log('🎯 点击分类框...');
    await categoryTrigger.click({ delay: 200 });
    await page.waitForTimeout(1000); // 等待 React 反应
    
    // 2. 暴力键盘导航
    console.log('⌨️ 键盘导航: ArrowDown + Enter...');
    await page.keyboard.press('ArrowDown');
    await page.waitForTimeout(500);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1000);
    
    // 3. 再次选择二级分类
    await page.keyboard.press('ArrowDown');
    await page.waitForTimeout(500);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1000);
    
    console.log('✅ 键盘导航完成');
    return true;
  } catch (e) {
    console.log('❌ 键盘导航失败:', e.message);
    return false;
  }
}

// ===== Gemini 补丁 2: 全局 Input 探测 =====
async function forceUploadCover(page, filePath) {
  console.log('🖼️ 封面上传: 全局 Input 探测...');
  
  try {
    // 1. 切换到单图模式
    console.log('🎯 点击"单图"...');
    await page.click('text=单图', { force: true });
    await page.waitForTimeout(1000);
    
    // 2. 寻找页面中隐藏的上传 input
    console.log('🔍 探测 file input...');
    const fileInput = page.locator('input[type="file"]').first();
    
    // 3. 直接设置文件，不经过点击过程
    const finalPath = filePath || path.join(BASE_DIR, 'assets', 'default-cover.jpg');
    if (fs.existsSync(finalPath)) {
      await fileInput.setInputFiles(finalPath);
      console.log('✅ 文件已注入');
    } else {
      console.log('⚠️ 封面文件不存在:', finalPath);
      return false;
    }
    
    // 4. 处理可能出现的裁剪弹窗
    await page.waitForTimeout(3000);
    try {
      const confirmBtn = page.locator('button:has-text("确定"), .cheetah-btn-primary').last();
      await confirmBtn.waitFor({ state: 'visible', timeout: 5000 });
      await confirmBtn.click();
      console.log('✅ 确认弹窗已处理');
    } catch (e) {
      console.log('[Matrix] 未探测到确认弹窗，可能已直接上传成功');
    }
    
    await page.waitForTimeout(2000);
    console.log('✅ 封面设置完成');
    return true;
  } catch (e) {
    console.log('❌ 封面上传失败:', e.message);
    return false;
  }
}

// ===== 移除遮罩 =====
async function removeBlockingMasks(page) {
  console.log('🧹 移除遮罩层...');
  await page.evaluate(() => {
    const masks = document.querySelectorAll('svg rect[fill="transparent"], .cheetah-mask, .ant-modal-mask, [class*="overlay"]');
    masks.forEach(mask => {
      mask.style.pointerEvents = 'none';
      mask.style.display = 'none';
    });
  });
  await randomDelay(page, 1000, 2000);
}

// ===== 主流程 =====
async function publishArticle(articleFile, coverPath) {
  console.log('\n🚀 终极全自动发布 v2.0');
  console.log('📄 文章:', articleFile);
  
  // 读取文章
  const articleContent = fs.readFileSync(path.join(BASE_DIR, articleFile), 'utf-8');
  const article = {
    title: articleContent.split('\n')[0].replace('# ', '').trim(),
    content: articleContent
  };
  console.log('📰 标题:', article.title);
  
  // 启动浏览器
  const browser = await chromium.launch({
    headless: false,
    slowMo: 150,
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
    
    // 移除遮罩
    await removeBlockingMasks(page);
    
    // 填写标题
    console.log('✏️ 填写标题...');
    await page.fill('.cheetah-input', article.title);
    await randomDelay(page, 1000, 2000);
    console.log('✅ 标题填写完成');
    
    // 填写正文
    console.log('✏️ 填写正文...');
    await page.fill('[contenteditable="true"]', article.content);
    await randomDelay(page, 1000, 2000);
    console.log('✅ 正文填写完成');
    
    // 选择分类（键盘导航）
    const categoryOk = await forceSelectCategory(page);
    
    // 上传封面（全局 Input 探测）
    const coverOk = await forceUploadCover(page, coverPath);
    
    // 点击发布
    console.log('🚀 点击发布...');
    await page.click('[data-testid="publish-btn"]', { force: true });
    await randomDelay(page, 5000, 8000);
    
    // ===== Gemini 补丁 3: 终极自检 =====
    console.log('🔍 监测 URL 变更...');
    try {
      await page.waitForURL('**/builder/rc/content/manage**', { timeout: 15000 });
      console.log('🏆 全自动发布圆满成功！');
      return { success: true, url: page.url() };
    } catch (e) {
      console.log('❌ 发布可能卡在表单校验');
      await page.screenshot({ path: path.join(LOGS_DIR, `final-check-error-${Date.now()}.png`), fullPage: true });
      
      // 检查是否有错误提示
      const finalUrl = page.url();
      console.log('📍 最终URL:', finalUrl);
      
      return { success: false, url: finalUrl };
    }
    
  } catch (e) {
    console.error('❌ 错误:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `final-error-${Date.now()}.png`) });
    throw e;
  } finally {
    await browser.close();
  }
}

// 主程序
const articleFile = process.argv[2] || 'articles/test-publish.md';
const coverPath = process.argv[3];

publishArticle(articleFile, coverPath).then(result => {
  console.log('\n📊 结果:', result);
  process.exit(result.success ? 0 : 1);
}).catch(err => {
  console.error('\n❌ 错误:', err.message);
  process.exit(1);
});
