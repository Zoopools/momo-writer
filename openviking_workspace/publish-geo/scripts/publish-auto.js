#!/usr/bin/env node
/**
 * GEO 发布系统 - 协议级全自动方案
 * Gemini 终极降维打击版
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

// ===== Gemini 方案 A: 协议级模拟 =====
async function protocolLevelClick(page, selector) {
  console.log(`🎯 协议级点击: ${selector}`);
  const element = page.locator(selector).first();
  
  await element.evaluate(el => {
    el.focus();
    // 模拟完整的鼠标事件链
    ['mousedown', 'mouseup', 'click'].forEach(evt => {
      el.dispatchEvent(new MouseEvent(evt, { 
        bubbles: true, 
        cancelable: true, 
        view: window
      }));
    });
  });
  
  await randomDelay(page, 1000, 2000);
  console.log('✅ 协议级点击完成');
}

// ===== Gemini 方案 A: Portal 穿透 =====
async function selectCategoryPortal(page) {
  console.log('📂 选择分类: Portal 穿透方案...');
  
  try {
    // 1. 触发下拉框显示（协议级）
    console.log('🎯 触发下拉框...');
    const categoryTrigger = page.locator('.cheetah-select').filter({ hasText: /选择分类|分类/ }).first();
    
    await categoryTrigger.evaluate(el => {
      el.focus();
      ['mousedown', 'mouseup', 'click'].forEach(evt => {
        el.dispatchEvent(new MouseEvent(evt, { bubbles: true, cancelable: true, view: window }));
      });
    });
    
    await randomDelay(page, 1500, 2500);
    
    // 2. 暴力扫描 Body 下的所有 Portal 容器
    console.log('🔍 扫描 Portal 容器...');
    await page.waitForTimeout(1000); // 给 React 渲染时间
    
    // 尝试从 body 最后一个 div 查找
    const dropdownItem = page.locator('body > div').last().locator('.cheetah-select-item').filter({ hasText: /^游戏$/ });
    
    if (await dropdownItem.isVisible().catch(() => false)) {
      console.log('✅ 找到 Portal 下拉选项');
      await dropdownItem.evaluate(el => el.click());
      await randomDelay(page, 1500, 2500);
      
      // 选择二级分类
      const subItem = page.locator('body > div').last().locator('.cheetah-select-item').filter({ hasText: /^游戏资讯$/ });
      if (await subItem.isVisible().catch(() => false)) {
        await subItem.evaluate(el => el.click());
        console.log('✅ 分类选择完成');
        return true;
      }
    } else {
      console.log('⚠️ Portal 未找到，尝试坐标点击');
      // 备选：通过坐标暴力点击
      const box = await categoryTrigger.boundingBox();
      if (box) {
        await page.mouse.click(box.x + 10, box.y + 50); // 向下偏移
        await randomDelay(page, 1500, 2500);
        
        // 再次扫描
        const retryItem = page.locator('body > div').last().locator('.cheetah-select-item').filter({ hasText: /^游戏$/ });
        if (await retryItem.isVisible().catch(() => false)) {
          await retryItem.evaluate(el => el.click());
          await randomDelay(page, 1500, 2500);
          
          const retrySub = page.locator('body > div').last().locator('.cheetah-select-item').filter({ hasText: /^游戏资讯$/ });
          if (await retrySub.isVisible().catch(() => false)) {
            await retrySub.evaluate(el => el.click());
            console.log('✅ 分类选择完成（坐标方案）');
            return true;
          }
        }
      }
    }
    
    return false;
  } catch (e) {
    console.log('❌ 分类选择失败:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-category-fail-${Date.now()}.png`) });
    return false;
  }
}

// ===== Gemini 方案 B: 封面无感注入 =====
async function uploadCoverStealth(page, coverPath) {
  console.log('🖼️ 封面上传: 无感注入方案...');
  
  try {
    // 直接监听并注入文件
    console.log('🎯 触发文件选择...');
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser', { timeout: 15000 }),
      // 通过点击包含"封面"或"单图"字样的容器
      page.locator('div:has-text("单图"), .cheetah-upload, [class*="cover"]').first().click({ force: true })
    ]);
    
    // 选择本地文件
    const finalCoverPath = coverPath || path.join(BASE_DIR, 'assets', 'default-cover.jpg');
    if (fs.existsSync(finalCoverPath)) {
      await fileChooser.setFiles(finalCoverPath);
      console.log('✅ 文件已注入');
    } else {
      console.log('⚠️ 封面文件不存在');
      await fileChooser.cancel();
      return false;
    }
    
    // 等待上传完成并确认
    await page.waitForTimeout(3000);
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

// ===== 移除遮罩 =====
async function removeBlockingMasks(page) {
  console.log('🧹 移除遮罩层...');
  await page.evaluate(() => {
    const masks = document.querySelectorAll('svg rect[fill="transparent"], .cheetah-mask, .ant-modal-mask, [class*="overlay"], [class*="backdrop"]');
    masks.forEach(mask => {
      mask.style.pointerEvents = 'none';
      mask.style.display = 'none';
    });
  });
  await randomDelay(page, 1000, 2000);
}

// ===== 主流程 =====
async function publishArticle(articleFile, coverPath) {
  console.log('\n🚀 协议级全自动发布');
  console.log('📄 文章:', articleFile);
  
  // 读取文章
  const articleContent = fs.readFileSync(path.join(BASE_DIR, articleFile), 'utf-8');
  const article = {
    title: articleContent.split('\n')[0].replace('# ', '').trim(),
    content: articleContent
  };
  console.log('📰 标题:', article.title);
  
  // ===== Gemini 方案 C: 启动浏览器（隐藏自动化特征）=====
  console.log('🌐 启动浏览器（slowMo: 150ms）...');
  const browser = await chromium.launch({
    headless: false, // 必须有头
    slowMo: 150, // 模拟人类反应
    args: [
      '--disable-blink-features=AutomationControlled', // 隐藏自动化特征
    ]
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
    
    // 选择分类（协议级）
    const categoryOk = await selectCategoryPortal(page);
    
    // 上传封面（无感注入）
    const coverOk = await uploadCoverStealth(page, coverPath);
    
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
    await page.screenshot({ path: path.join(LOGS_DIR, `auto-final-${Date.now()}.png`) });
    
    if (finalUrl.includes('preview') || finalUrl.includes('article_id')) {
      console.log('✅ 发布成功！');
      return { success: true, url: finalUrl };
    } else {
      console.log('⚠️ 请检查发布状态');
      return { success: false, url: finalUrl };
    }
    
  } catch (e) {
    console.error('❌ 错误:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `auto-error-${Date.now()}.png`) });
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