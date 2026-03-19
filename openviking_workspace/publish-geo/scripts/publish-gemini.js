#!/usr/bin/env node
/**
 * GEO 发布系统 - Gemini 终极方案
 * 百家号全自动发布脚本（完整版）
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

// ===== 第一步：暴力拆除"透明墙" =====
async function removeBlockingMasks(page) {
  console.log('🧹 移除遮罩层...');
  await page.evaluate(() => {
    // 移除所有可能拦截点击的透明 SVG 或遮罩层
    const masks = document.querySelectorAll('svg rect[fill="transparent"], .cheetah-mask, .ant-modal-mask, [class*="overlay"], [class*="backdrop"]');
    masks.forEach(mask => {
      mask.style.pointerEvents = 'none';
      mask.style.display = 'none';
    });
    console.log(`[Matrix] 已物理移除 ${masks.length} 个潜在干扰层`);
  });
  await randomDelay(page, 1000, 2000);
}

// ===== 第二步：分类选择器·深度重构 =====
async function selectCategory(page) {
  console.log('📂 选择文章分类: 游戏-游戏资讯...');
  
  try {
    // 1. 确保遮罩已清空
    await removeBlockingMasks(page);
    
    // 2. 定位分类触发器
    console.log('🎯 点击分类下拉框...');
    const categoryTrigger = page.locator('.cheetah-select').filter({ hasText: /选择分类|分类/ }).first();
    await categoryTrigger.scrollIntoViewIfNeeded();
    await categoryTrigger.click({ force: true });
    await randomDelay(page, 3000, 5000);
    
    // 3. 等待 Body 级别的 Dropdown 挂载
    console.log('⏳ 等待下拉菜单...');
    const dropdown = page.locator('.cheetah-select-dropdown:not([style*="display: none"])');
    await dropdown.waitFor({ state: 'visible', timeout: 10000 });
    
    // 4. 选择"游戏"
    console.log('🎯 选择"游戏"...');
    await dropdown.locator('.cheetah-select-item').filter({ hasText: /^游戏$/ }).click({ force: true });
    await randomDelay(page, 2000, 3000);
    
    // 5. 选择"游戏资讯"
    console.log('🎯 选择"游戏资讯"...');
    const subOption = page.locator('.cheetah-select-item').filter({ hasText: /^游戏资讯$/ });
    await subOption.click({ force: true });
    await randomDelay(page, 2000, 3000);
    
    console.log('✅ 分类选择完成');
    return true;
  } catch (e) {
    console.log('❌ 分类选择失败:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-category-fail-${Date.now()}.png`) });
    return false;
  }
}

// ===== 第三步：封面上传·穿透方案 =====
async function uploadCover(page, coverPath) {
  console.log('🖼️ 添加封面...');
  
  try {
    // 1. 点击"单图"选项
    console.log('🎯 点击"单图"...');
    await page.click('text=单图', { force: true });
    await randomDelay(page, 2000, 3000);
    
    // 2. 监听文件选择事件
    console.log('🎯 触发文件选择...');
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser', { timeout: 10000 }),
      page.locator('.cheetah-upload, [class*="upload"]').first().click({ force: true })
    ]);
    
    // 3. 选择本地文件
    const finalCoverPath = coverPath || path.join(BASE_DIR, 'assets', 'default-cover.jpg');
    if (fs.existsSync(finalCoverPath)) {
      await fileChooser.setFiles(finalCoverPath);
      console.log('✅ 封面上传完成');
    } else {
      console.log('⚠️ 封面文件不存在:', finalCoverPath);
      await fileChooser.cancel();
      return false;
    }
    
    // 4. 等待上传预览并保存
    await page.waitForSelector('.cheetah-modal-content, [class*="preview"]', { timeout: 10000 });
    await page.click('button:has-text("确定"), button:has-text("确认")', { force: true });
    await randomDelay(page, 2000, 3000);
    
    console.log('✅ 封面设置完成');
    return true;
  } catch (e) {
    console.log('❌ 封面上传失败:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-cover-fail-${Date.now()}.png`) });
    return false;
  }
}

// ===== 第四步：发布前置校验 =====
async function prePublishCheck(page) {
  console.log('🔍 发布前校验...');
  
  const titleValue = await page.inputValue('.cheetah-input');
  const contentValue = await page.locator('[contenteditable="true"]').innerText();
  const categoryVisible = await page.locator('.cheetah-select-selection-item').isVisible().catch(() => false);
  
  const isTitleOk = titleValue !== '';
  const isContentOk = contentValue !== '';
  const isCategoryOk = categoryVisible;
  
  console.log(`  标题: ${isTitleOk ? '✅' : '❌'}`);
  console.log(`  内容: ${isContentOk ? '✅' : '❌'}`);
  console.log(`  分类: ${isCategoryOk ? '✅' : '❌'}`);
  
  if (!isTitleOk || !isContentOk || !isCategoryOk) {
    throw new Error(`[发布拦截] 必填项缺失: 标题(${isTitleOk}), 内容(${isContentOk}), 分类(${isCategoryOk})`);
  }
  
  console.log('✅ 校验通过');
}

// ===== 主发布流程 =====
async function publishArticle(articleFile, coverPath) {
  console.log('\n🚀 开始发布');
  console.log('📄 文章:', articleFile);
  
  // 读取文章
  const articleContent = fs.readFileSync(path.join(BASE_DIR, articleFile), 'utf-8');
  const article = {
    title: articleContent.split('\n')[0].replace('# ', '').trim(),
    content: articleContent
  };
  console.log('📰 标题:', article.title);
  
  // 启动浏览器
  const browser = await chromium.launch({ headless: false });
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
    
    // 填写标题
    console.log('✏️ 填写标题...');
    await page.fill('.cheetah-input', article.title);
    console.log('✅ 标题填写完成');
    
    // 填写正文
    console.log('✏️ 填写正文...');
    await page.fill('[contenteditable="true"]', article.content);
    console.log('✅ 正文填写完成');
    
    // 选择分类
    const categoryOk = await selectCategory(page);
    
    // 上传封面
    const coverOk = await uploadCover(page, coverPath);
    
    // 发布前校验
    await prePublishCheck(page);
    
    // 点击发布
    console.log('🚀 点击发布...');
    await page.click('[data-testid="publish-btn"]', { force: true });
    await randomDelay(page, 5000, 8000);
    
    // 检查确认弹窗
    try {
      await page.click('button:has-text("确定"), button:has-text("确认")', { force: true, timeout: 5000 });
      await randomDelay(page, 3000, 5000);
    } catch (e) {
      console.log('  无确认弹窗');
    }
    
    // 获取结果
    const finalUrl = page.url();
    console.log('📍 最终URL:', finalUrl);
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-final-${Date.now()}.png`) });
    
    if (finalUrl.includes('preview') || finalUrl.includes('article_id')) {
      console.log('✅ 发布成功！');
      return { success: true, url: finalUrl };
    } else {
      console.log('⚠️ 请手动检查是否发布成功');
      return { success: false, url: finalUrl };
    }
    
  } catch (e) {
    console.error('❌ 发布失败:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-error-${Date.now()}.png`) });
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
