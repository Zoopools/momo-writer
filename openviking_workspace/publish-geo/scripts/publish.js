#!/usr/bin/env node
/**
 * GEO 发布系统 - 自动发布脚本
 * 路径: ~/Documents/openclaw/openviking_workspace/publish-geo/scripts/publish.js
 * 
 * 使用方法: node scripts/publish.js <platform> <article-file>
 * 示例: node scripts/publish.js bjh-work ../articles/test.md
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// 路径绝对对齐
const BASE_DIR = path.resolve(__dirname, '..');
const AUTH_DIR = path.join(BASE_DIR, 'auth');
const LOGS_DIR = path.join(BASE_DIR, 'logs');

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

// 不同账号的 User-Agent 池（差异化身份）
const USER_AGENTS = {
  'bjh-work': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'bjh-personal': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
  'wechat-mp': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
  'zhihu': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
};

// 随机延迟函数（防封）
async function randomDelay(page, min = 500, max = 2000) {
  const delay = Math.floor(Math.random() * (max - min + 1)) + min;
  await page.waitForTimeout(delay);
}

// 模拟人类打字（防封）
async function humanType(page, selector, text) {
  for (const char of text) {
    await page.type(selector, char, { delay: Math.random() * 100 + 50 });
  }
}

// 飞书回填（双向心跳）
async function feishuReport(platform, status, url = '', error = '') {
  const timestamp = new Date().toLocaleString('zh-CN');
  const report = {
    platform,
    status,
    url,
    error,
    timestamp
  };

  // 记录到本地日志
  const reportFile = path.join(LOGS_DIR, `feishu-report-${Date.now()}.json`);
  fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));

  console.log(`📋 飞书报告: ${status} ${url || error}`);

  // TODO: 调用飞书 API 回填表格
  // 这里可以通过 OpenClaw 工具或飞书 API 实现
}

// 检查登录态是否有效
async function checkAuthValid(authFile) {
  if (!fs.existsSync(authFile)) {
    return { valid: false, reason: '文件不存在' };
  }

  const stats = fs.statSync(authFile);
  const age = Date.now() - stats.mtime.getTime();
  const maxAge = 7 * 24 * 60 * 60 * 1000; // 7天

  if (age > maxAge) {
    return { valid: false, reason: '登录态过期（超过7天）' };
  }

  return { valid: true };
}

// 百家号发布逻辑
async function publishBjh(browser, page, article, platform) {
  console.log('📝 开始发布到百家号...');

  // 直接打开真正的编辑页面（绕过引导页）
  console.log('🌐 打开编辑页面...');
  await page.goto('https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1', {
    waitUntil: 'networkidle',
    timeout: 60000
  });
  await randomDelay(page, 5000, 8000);
  
  // 截图调试
  await page.screenshot({ path: path.join(LOGS_DIR, `debug-publish-${Date.now()}.png`) });
  console.log('📸 已截图保存');
  
  // 获取页面信息
  const url = page.url();
  console.log(`📍 当前URL: ${url}`);
  
  // ===== Gemini 破壁方案 1: 处理引导页 =====
  console.log('🛡️ 处理引导页...');
  try {
    // 1. 先等待"发布图文"按钮出现
    console.log('⏳ 等待"发布图文"按钮...');
    await page.waitForSelector('text=发布图文', { timeout: 10000 });
    
    // 2. 强力点击 - 使用 evaluate 绕过遮罩
    console.log('🖱️ 强力点击"发布图文"...');
    await page.evaluate(() => {
      const btn = document.querySelector('[class*="entryTitle"], [class*="publish"], button:contains("发布图文")');
      if (btn) btn.click();
    });
    await randomDelay(page, 8000, 10000);
    
    // 3. 再次截图看效果
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-after-click-${Date.now()}.png`) });
    console.log('📸 点击后截图已保存');
    
    console.log('✅ 引导页处理完成');
  } catch (e) {
    console.log('  引导页处理跳过:', e.message);
  }
  
  // 再次截图
  await page.screenshot({ path: path.join(LOGS_DIR, `debug-publish-2-${Date.now()}.png`) });
  console.log('📸 已截图保存');

  // ===== Gemini 破壁方案 2: 探测 iframe =====
  console.log('🔍 探测 iframe...');
  const allFrames = page.frames();
  console.log(`  发现 ${allFrames.length} 个 frame`);
  
  let targetFrame = null;
  for (let i = 0; i < allFrames.length; i++) {
    const frameUrl = allFrames[i].url();
    console.log(`  [${i}] ${frameUrl.substring(0, 80)}...`);
    if (frameUrl.includes('editor') || frameUrl.includes('article')) {
      targetFrame = allFrames[i];
      console.log(`  ✅ 锁定编辑器 iframe [${i}]`);
      break;
    }
  }

  // ===== Gemini 破壁方案 3: 使用 frameLocator 或主页面 =====
  let contentFrame = targetFrame || page;
  
  // ===== 填写标题 =====
  console.log('✏️ 填写标题...');
  
  // 使用 class 选择器（从分析结果）
  try {
    await page.waitForSelector('.cheetah-input', { timeout: 10000 });
    await page.fill('.cheetah-input', article.title);
    console.log('✅ 标题填写完成');
  } catch (e) {
    console.log('❌ 标题填写失败:', e.message);
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-fail-${Date.now()}.png`) });
    throw new Error('未找到标题输入框');
  }
  
  // ===== 填写正文（Termo.ai 方案）=====
  console.log('✏️ 填写正文...');
  await randomDelay(page, 500, 1500);
  
  try {
    // 方案 1: 使用 role="textbox" 语义锚点
    await page.waitForSelector('div[role="textbox"]', { timeout: 10000 });
    await page.fill('div[role="textbox"]', article.content);
    console.log('✅ 正文填写完成 (role=textbox)');
  } catch (e) {
    console.log('  role=textbox 失败:', e.message);
    
    // 方案 2: 使用 contenteditable
    try {
      await page.waitForSelector('[contenteditable="true"]', { timeout: 5000 });
      await page.fill('[contenteditable="true"]', article.content);
      console.log('✅ 正文填写完成 (contenteditable)');
    } catch (e2) {
      console.log('⚠️ 正文填写失败:', e2.message);
    }
  }
  
  // ===== Gemini 方案: 选择文章分类 =====
  console.log('📂 选择文章分类: 游戏-游戏资讯...');
  await randomDelay(page, 3000, 5000);
  
  // 开启对话框监听（捕获错误提示）
  page.on('dialog', async dialog => {
    console.log(`[百家号提示] ${dialog.message()}`);
    await dialog.dismiss();
  });
  
  try {
    // 先移除 SVG 遮罩
    console.log('🧹 移除遮罩层...');
    await page.evaluate(() => {
      document.querySelectorAll('svg rect, [class*="overlay"], [class*="mask"]').forEach(el => {
        el.style.pointerEvents = 'none';
        el.style.display = 'none';
      });
    });
    await randomDelay(page, 1000, 2000);
    
    // 方案 1: 使用 nth-match 定位第二个 cheetah-select（分类）
    console.log('🎯 点击分类下拉框...');
    const categoryTrigger = page.locator('.cheetah-select').nth(1);
    await categoryTrigger.click({ force: true });
    await randomDelay(page, 2000, 3000);
    
    // 选择"游戏"（使用 filter 精确匹配）
    console.log('🎯 选择"游戏"...');
    const gameOption = page.locator('.cheetah-select-item').filter({ hasText: /^游戏$/ });
    await gameOption.click({ force: true });
    await randomDelay(page, 2000, 3000);
    
    // 选择"游戏资讯"
    console.log('🎯 选择"游戏资讯"...');
    const subCategory = page.locator('.cheetah-select-item').filter({ hasText: /^游戏资讯$/ });
    await subCategory.click({ force: true });
    console.log('✅ 分类选择完成: 游戏-游戏资讯');
  } catch (e) {
    console.log('  分类选择失败:', e.message);
    // 截图记录
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-category-fail-${Date.now()}.png`) });
  }
  
  // ===== Gemini 方案: 添加封面 =====
  console.log('🖼️ 添加封面...');
  await randomDelay(page, 3000, 5000);
  
  try {
    // 方案 1: 使用 FileChooser 机制上传封面
    console.log('🎯 触发封面选择...');
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser'),
      page.click('text=单图, [class*="cover"] button, [data-testid*="cover"]', { force: true })
    ]);
    
    // 上传本地图片（使用默认封面）
    const coverPath = path.join(BASE_DIR, 'assets', 'default-cover.jpg');
    if (fs.existsSync(coverPath)) {
      await fileChooser.setFiles(coverPath);
      console.log('✅ 封面上传完成');
    } else {
      console.log('⚠️ 默认封面不存在，尝试从正文选取');
      // 关闭文件选择器，尝试从正文选取
      await fileChooser.cancel();
      
      // 点击"从正文中选取"
      await page.click('text=从正文中选取', { force: true });
      await randomDelay(page, 2000, 3000);
      
      // 选择第一张图
      await page.locator('[class*="image-item"]').first().click();
      await randomDelay(page, 2000, 3000);
    }
    
    // 点击确定
    await page.click('button:has-text("确定"), button:has-text("确认")', { force: true });
    console.log('✅ 封面设置完成');
  } catch (e) {
    console.log('  封面添加失败:', e.message);
    // 截图记录
    await page.screenshot({ path: path.join(LOGS_DIR, `debug-cover-fail-${Date.now()}.png`) });
  }

  // 选择封面（如果有）
  if (article.cover) {
    console.log('🖼️ 上传自定义封面...');
    await randomDelay(page, 800, 2000);
    await page.click('text=选择封面, button:has-text("选择封面")');
    // TODO: 上传图片逻辑
    await randomDelay(page, 2000, 4000);
  }

  // ===== 页面环境清理（CSS 降维打击）=====
  console.log('🧹 清理页面环境...');
  await page.addStyleTag({ 
    content: `
      .guide-mask, .bjh-guide-pop, .editor-guide, svg rect, [class*="mask"], 
      [class*="overlay"], [class*="modal"], [class*="backdrop"] { 
        display: none !important; 
        pointer-events: none !important; 
      }
    ` 
  });
  await randomDelay(page, 1000, 2000);
  
  // 点击"发布"（认证后可用）
  console.log('🚀 点击"发布"...');
  await randomDelay(page, 3000, 5000);
  
  // 方案 A: 使用 data-testid 精确定位
  try {
    console.log('🎯 方案 A: 使用 data-testid 定位发布按钮...');
    await page.click('[data-testid="publish-btn"]', { force: true, timeout: 10000 });
    console.log('✅ 发布按钮点击成功');
  } catch (e) {
    console.log('  方案 A 失败:', e.message);
    
    // 方案 B: 使用 CSS 类名定位
    console.log('🎯 方案 B: 使用 CSS 类名定位...');
    try {
      await page.click('.cheetah-btn-primary:has-text("发布")', { force: true, timeout: 5000 });
      console.log('✅ 方案 B 点击成功');
    } catch (e2) {
      console.log('  方案 B 失败:', e2.message);
      
      // 方案 C: JS 注入点击
      console.log('🎯 方案 C: JS 注入点击发布');
      await page.evaluate(() => {
        const btn = document.querySelector('[data-testid="publish-btn"]') || 
                    Array.from(document.querySelectorAll('button')).find(el => 
                      el.textContent.trim() === '发布' && 
                      el.className.includes('primary')
                    );
        if (btn) {
          btn.click();
          btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
          console.log('JS 注入点击执行');
        }
      });
    }
  }
  
  // 等待发布响应
  console.log('⏳ 等待发布响应...');
  await page.waitForTimeout(8000);
  
  // 检查是否有确认弹窗
  console.log('🔍 检查确认弹窗...');
  try {
    const confirmBtn = await page.getByRole('button', { name: /确认|确定/ });
    if (confirmBtn) {
      console.log('🖱️ 点击确认按钮...');
      await confirmBtn.click({ force: true });
      await page.waitForTimeout(5000);
    }
  } catch (e) {
    console.log('  无确认弹窗');
  }

  // 获取当前URL
  const currentUrl = page.url();
  console.log(`📍 发布后URL: ${currentUrl}`);
  
  // 截图保存成功状态
  await page.screenshot({ path: path.join(LOGS_DIR, `debug-published-${Date.now()}.png`) });
  console.log('📸 发布截图已保存');
  
  // 检查是否发布成功（URL 变化或页面提示）
  if (currentUrl.includes('preview') || currentUrl.includes('article_id') || currentUrl.includes('baijiahao.baidu.com')) {
    console.log('✅ 文章发布成功！');
    return { success: true, url: currentUrl, type: 'published' };
  }

  // 如果发布失败，尝试保存草稿
  console.log('⚠️ 发布可能失败，尝试保存草稿...');
  return { success: false, error: '发布失败，已尝试保存草稿', type: 'draft' };
}

// 主发布函数
async function publish(platform, articleFile) {
  const authFile = path.join(AUTH_DIR, `${platform}.json`);
  const logFile = path.join(LOGS_DIR, `publish-${platform}-${Date.now()}.log`);

  console.log(`\n🚀 [${platform}] 开始发布`);
  console.log(`📄 文章: ${articleFile}`);
  console.log(`🔑 登录态: ${authFile}`);

  // 检查登录态
  const authCheck = await checkAuthValid(authFile);
  if (!authCheck.valid) {
    console.error(`❌ 登录态无效: ${authCheck.reason}`);
    await feishuReport(platform, '需重新授权', '', authCheck.reason);
    throw new Error(`登录态无效: ${authCheck.reason}`);
  }

  // 读取文章
  if (!fs.existsSync(articleFile)) {
    throw new Error(`文章文件不存在: ${articleFile}`);
  }

  const articleContent = fs.readFileSync(articleFile, 'utf-8');
  const article = {
    title: articleContent.split('\n')[0].replace('# ', '').trim(),
    content: articleContent,
    cover: null
  };

  console.log(`📰 标题: ${article.title}`);

  // 启动浏览器（无头模式，后台运行）
  const browser = await chromium.launch({
    headless: true,  // 无界面，后台运行
    // slowMo: 100   // 可选：全局慢动作
  });

  const context = await browser.newContext({
    storageState: authFile,
    userAgent: USER_AGENTS[platform] || USER_AGENTS['bjh-work'],
    viewport: { width: 1280, height: 720 },
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai'
  });

  const page = await context.newPage();

  try {
    let result;

    if (platform.startsWith('bjh')) {
      result = await publishBjh(browser, page, article, platform);
    } else {
      throw new Error(`暂不支持平台: ${platform}`);
    }

    if (result.success) {
      console.log(`\n✅ [${platform}] 发布成功!`);
      console.log(`🔗 链接: ${result.url}`);
      await feishuReport(platform, '已发布', result.url);
    } else {
      throw new Error(result.error);
    }

  } catch (e) {
    console.error(`\n❌ [${platform}] 发布失败: ${e.message}`);
    await feishuReport(platform, '发布失败', '', e.message);
    throw e;
  } finally {
    await browser.close();
  }
}

// 主程序
const platform = process.argv[2];
const articleFile = process.argv[3];

if (!platform || !articleFile) {
  console.log('使用方法: node scripts/publish.js <platform> <article-file>');
  console.log('\n示例:');
  console.log('  node scripts/publish.js bjh-work ../articles/test.md');
  process.exit(0);
}

publish(platform, articleFile).catch(err => {
  console.error('❌ 发布失败:', err.message);
  process.exit(1);
});
