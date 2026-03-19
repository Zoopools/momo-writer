#!/usr/bin/env node
/**
 * Bilibili Poster - B站自动发布脚本
 * 
 * 使用方法:
 * node bilibili-poster.js --video <path> --title <title> [options]
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// 配置
const CONFIG = {
  bilibiliUploadUrl: 'https://member.bilibili.com/platform/upload/video/frame',
  headless: false, // 开发阶段设为 false 以便观察
  slowMo: 100,
};

// 分区映射
const PARTITIONS = {
  '动画': '1',
  '游戏': '4',
  '知识': '36',
  '科技': '188',
  '生活': '160',
  '美食': '211',
  '影视': '181',
  // 更多分区...
};

/**
 * 主函数
 */
async function main() {
  const args = parseArgs();
  
  if (!args.video || !args.title) {
    console.error('错误: 必须提供 --video 和 --title 参数');
    printUsage();
    process.exit(1);
  }

  console.log('🎬 Bilibili 自动发布工具');
  console.log(`视频: ${args.video}`);
  console.log(`标题: ${args.title}`);
  console.log('');

  // 检查视频文件
  if (!fs.existsSync(args.video)) {
    console.error(`错误: 视频文件不存在: ${args.video}`);
    process.exit(1);
  }

  const browser = await chromium.launch({
    headless: CONFIG.headless,
    slowMo: CONFIG.slowMo,
  });

  try {
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
    });

    const page = await context.newPage();

    // 1. 打开B站上传页面
    console.log('1. 打开B站上传页面...');
    await page.goto(CONFIG.bilibiliUploadUrl);
    
    // 等待页面加载
    await page.waitForTimeout(3000);

    // 2. 检查登录状态
    console.log('2. 检查登录状态...');
    const isLoggedIn = await checkLoginStatus(page);
    if (!isLoggedIn) {
      console.log('⚠️ 未登录，请手动登录...');
      await waitForLogin(page);
    }

    // 3. 上传视频
    console.log('3. 上传视频...');
    await uploadVideo(page, args.video);

    // 4. 填写标题
    console.log('4. 填写标题...');
    await fillTitle(page, args.title);

    // 5. 填写描述
    if (args.description) {
      console.log('5. 填写描述...');
      await fillDescription(page, args.description);
    }

    // 6. 添加标签
    if (args.tags) {
      console.log('6. 添加标签...');
      await addTags(page, args.tags.split(','));
    }

    // 7. 设置封面
    if (args.cover) {
      console.log('7. 设置封面...');
      await setCover(page, args.cover);
    }

    // 8. 选择分区
    if (args.partition) {
      console.log('8. 选择分区...');
      await selectPartition(page, args.partition);
    }

    console.log('');
    console.log('✅ 表单填写完成！');
    console.log('请手动确认并提交投稿。');

    // 等待用户手动提交或超时
    await page.waitForTimeout(30000);

  } catch (error) {
    console.error('❌ 错误:', error.message);
    console.error(error.stack);
  } finally {
    // 开发阶段不关闭浏览器，方便调试
    // await browser.close();
    console.log('');
    console.log('浏览器保持打开状态，请手动关闭。');
  }
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = {};
  const argv = process.argv.slice(2);
  
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  
  return args;
}

/**
 * 打印用法
 */
function printUsage() {
  console.log('');
  console.log('用法:');
  console.log('  node bilibili-poster.js --video <path> --title <title> [options]');
  console.log('');
  console.log('参数:');
  console.log('  --video <path>       视频文件路径 (必需)');
  console.log('  --title <title>      视频标题 (必需)');
  console.log('  --description <desc> 视频描述');
  console.log('  --tags <tags>        标签，逗号分隔');
  console.log('  --cover <path>       封面图片路径');
  console.log('  --partition <name>   分区名称');
  console.log('  --schedule <time>    定时发布时间');
  console.log('');
  console.log('示例:');
  console.log('  node bilibili-poster.js --video ./myvideo.mp4 --title "我的视频"');
}

/**
 * 检查登录状态
 */
async function checkLoginStatus(page) {
  // 检查是否有登录按钮或用户头像
  const loginButton = await page.$('.header-login-entry');
  return !loginButton;
}

/**
 * 等待登录
 */
async function waitForLogin(page) {
  console.log('等待登录完成...');
  // 等待登录按钮消失
  await page.waitForSelector('.header-login-entry', { state: 'detached', timeout: 120000 });
  console.log('✓ 登录成功');
}

/**
 * 上传视频
 */
async function uploadVideo(page, videoPath) {
  // 找到文件上传输入框
  const fileInput = await page.$('input[type="file"]');
  if (!fileInput) {
    throw new Error('未找到文件上传输入框');
  }
  
  await fileInput.setInputFiles(videoPath);
  console.log(`  已选择文件: ${path.basename(videoPath)}`);
  
  // 等待上传完成（这里需要根据实际情况调整）
  console.log('  等待上传完成...');
  await page.waitForTimeout(10000);
}

/**
 * 填写标题
 */
async function fillTitle(page, title) {
  // 根据实际页面结构调整选择器
  const titleInput = await page.$('input[placeholder*="标题"]');
  if (titleInput) {
    await titleInput.fill(title);
    console.log(`  标题: ${title}`);
  }
}

/**
 * 填写描述
 */
async function fillDescription(page, description) {
  const descInput = await page.$('textarea[placeholder*="简介"]');
  if (descInput) {
    await descInput.fill(description);
    console.log(`  描述已填写`);
  }
}

/**
 * 添加标签
 */
async function addTags(page, tags) {
  const tagInput = await page.$('input[placeholder*="标签"]');
  if (tagInput) {
    for (const tag of tags) {
      await tagInput.fill(tag.trim());
      await tagInput.press('Enter');
      await page.waitForTimeout(500);
    }
    console.log(`  标签: ${tags.join(', ')}`);
  }
}

/**
 * 设置封面
 */
async function setCover(page, coverPath) {
  // 点击上传封面按钮
  const coverButton = await page.$('.cover-upload-btn');
  if (coverButton) {
    await coverButton.click();
    
    // 等待文件选择对话框
    await page.waitForTimeout(1000);
    
    // 找到文件输入框
    const fileInput = await page.$('input[type="file"]');
    if (fileInput) {
      await fileInput.setInputFiles(coverPath);
      console.log(`  封面: ${path.basename(coverPath)}`);
    }
  }
}

/**
 * 选择分区
 */
async function selectPartition(page, partitionName) {
  const partitionId = PARTITIONS[partitionName];
  if (!partitionId) {
    console.log(`  ⚠️ 未知分区: ${partitionName}`);
    return;
  }
  
  // 点击分区选择器
  const partitionSelector = await page.$('.partition-selector');
  if (partitionSelector) {
    await partitionSelector.click();
    await page.waitForTimeout(500);
    
    // 选择具体分区
    const partitionOption = await page.$(`[data-partition-id="${partitionId}"]`);
    if (partitionOption) {
      await partitionOption.click();
      console.log(`  分区: ${partitionName}`);
    }
  }
}

// 运行
main().catch(console.error);
