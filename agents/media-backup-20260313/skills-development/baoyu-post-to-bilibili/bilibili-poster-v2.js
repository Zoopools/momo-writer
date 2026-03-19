#!/usr/bin/env node
/**
 * Bilibili Poster v2 - 简化版 B站自动发布脚本
 * 
 * 使用方法:
 * node bilibili-poster-v2.js --video <path> --title <title> [options]
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// 配置
const CONFIG = {
  bilibiliUploadUrl: 'https://member.bilibili.com/platform/upload/video/frame',
  headless: false,
  slowMo: 100,
  timeout: 30000,
};

// 分区映射（常见分区）
const PARTITIONS = {
  '动画': '1',
  '番剧': '2',
  '国创': '3',
  '音乐': '4',
  '舞蹈': '5',
  '游戏': '6',
  '知识': '7',
  '科技': '8',
  '数码': '9',
  '生活': '10',
  '美食': '11',
  '动物': '12',
  '鬼畜': '13',
  '时尚': '14',
  '娱乐': '15',
  '影视': '16',
};

/**
 * 主函数
 */
async function main() {
  const args = parseArgs();
  
  if (!args.video || !args.title) {
    console.error('❌ 错误: 必须提供 --video 和 --title 参数');
    printUsage();
    process.exit(1);
  }

  // 检查视频文件
  if (!fs.existsSync(args.video)) {
    console.error(`❌ 错误: 视频文件不存在: ${args.video}`);
    process.exit(1);
  }

  console.log('🎬 Bilibili 自动发布工具 v2');
  console.log('============================');
  console.log(`视频: ${args.video}`);
  console.log(`标题: ${args.title}`);
  console.log(`描述: ${args.description || '(无)'}`);
  console.log(`标签: ${args.tags || '(无)'}`);
  console.log(`分区: ${args.partition || '(默认)'}`);
  console.log('');

  const browser = await chromium.launch({
    headless: CONFIG.headless,
    slowMo: CONFIG.slowMo,
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
  });

  const page = await context.newPage();

  try {
    // 1. 打开 B站上传页面
    console.log('1️⃣ 打开 B站上传页面...');
    await page.goto(CONFIG.bilibiliUploadUrl, { timeout: CONFIG.timeout });
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    // 2. 检查登录状态
    console.log('2️⃣ 检查登录状态...');
    const isLoggedIn = await checkLoginStatus(page);
    if (!isLoggedIn) {
      console.log('⚠️  未检测到登录状态');
      console.log('请手动登录 B站（扫码或密码登录）');
      console.log('登录完成后按回车继续...');
      
      // 等待用户登录
      await waitForEnter();
      
      // 再次检查
      const nowLoggedIn = await checkLoginStatus(page);
      if (!nowLoggedIn) {
        console.log('❌ 仍未登录，退出');
        await browser.close();
        process.exit(1);
      }
    }
    console.log('✅ 已登录');

    // 3. 上传视频
    console.log('3️⃣ 上传视频...');
    await uploadVideo(page, args.video);

    // 4. 填写标题
    console.log('4️⃣ 填写标题...');
    await fillTitle(page, args.title);

    // 5. 填写描述
    if (args.description) {
      console.log('5️⃣ 填写描述...');
      await fillDescription(page, args.description);
    }

    // 6. 添加标签
    if (args.tags) {
      console.log('6️⃣ 添加标签...');
      await addTags(page, args.tags);
    }

    // 7. 设置封面（如果有）
    if (args.cover && fs.existsSync(args.cover)) {
      console.log('7️⃣ 设置封面...');
      await setCover(page, args.cover);
    }

    // 8. 选择分区
    if (args.partition) {
      console.log('8️⃣ 选择分区...');
      await selectPartition(page, args.partition);
    }

    console.log('');
    console.log('============================');
    console.log('✅ 表单填写完成！');
    console.log('');
    console.log('⚠️  请手动检查以下内容:');
    console.log('   - 视频是否上传完成');
    console.log('   - 标题、描述是否正确');
    console.log('   - 分区是否正确');
    console.log('   - 封面是否设置成功');
    console.log('');
    console.log('确认无误后，请手动点击"立即投稿"按钮');
    console.log('');
    console.log('按回车键关闭浏览器...');
    
    await waitForEnter();

  } catch (error) {
    console.error('');
    console.error('❌ 错误:', error.message);
    console.error(error.stack);
  } finally {
    await browser.close();
    console.log('');
    console.log('👋 浏览器已关闭');
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
  console.log('  node bilibili-poster-v2.js --video <path> --title <title> [options]');
  console.log('');
  console.log('参数:');
  console.log('  --video <path>       视频文件路径 (必需)');
  console.log('  --title <title>      视频标题 (必需)');
  console.log('  --description <desc> 视频描述');
  console.log('  --tags <tags>        标签，逗号分隔');
  console.log('  --cover <path>       封面图片路径');
  console.log('  --partition <name>   分区名称 (动画/游戏/知识/科技/生活/美食/影视)');
  console.log('');
  console.log('示例:');
  console.log('  node bilibili-poster-v2.js --video ./myvideo.mp4 --title "我的视频" --tags "科技,AI" --partition 科技');
}

/**
 * 检查登录状态
 */
async function checkLoginStatus(page) {
  try {
    // 检查是否有头像或用户名元素
    const avatar = await page.$('.header-avatar, .user-avatar, [class*="avatar"]');
    const username = await page.$('.user-name, [class*="username"], [class*="nickname"]');
    
    // 检查是否有登录按钮（如果有，说明未登录）
    const loginBtn = await page.$('.header-login-entry, .login-btn, a[href*="login"]');
    
    return !loginBtn && (avatar || username);
  } catch (e) {
    return false;
  }
}

/**
 * 等待用户按回车
 */
async function waitForEnter() {
  return new Promise((resolve) => {
    process.stdin.once('data', () => {
      resolve();
    });
  });
}

/**
 * 上传视频
 */
async function uploadVideo(page, videoPath) {
  try {
    // 找到文件上传输入框（通常在隐藏的 input 中）
    const fileInput = await page.$('input[type="file"][accept*="video"]');
    
    if (!fileInput) {
      // 尝试点击上传区域
      const uploadArea = await page.$('[class*="upload"], [class*="upload-area"], .upload-btn');
      if (uploadArea) {
        await uploadArea.click();
        await page.waitForTimeout(1000);
      }
    }
    
    // 再次尝试找到文件输入框
    const fileInput2 = await page.$('input[type="file"]');
    if (fileInput2) {
      await fileInput2.setInputFiles(videoPath);
      console.log(`   📁 已选择: ${path.basename(videoPath)}`);
      
      // 等待上传开始
      await page.waitForTimeout(3000);
      
      // 等待上传进度（最多 5 分钟）
      console.log('   ⏳ 等待上传完成（这可能需要几分钟）...');
      let uploaded = false;
      for (let i = 0; i < 60; i++) {
        await page.waitForTimeout(5000);
        
        // 检查是否上传完成（通过检查进度条或成功提示）
        const progress = await page.$('[class*="progress"], [class*="success"], [class*="complete"]');
        if (progress) {
          const text = await progress.textContent();
          if (text && (text.includes('100') || text.includes('完成') || text.includes('成功'))) {
            uploaded = true;
            break;
          }
        }
        
        process.stdout.write('   .');
      }
      
      if (uploaded) {
        console.log(' ✅ 上传完成！');
      } else {
        console.log(' ⚠️  上传时间较长，请手动确认');
      }
    } else {
      throw new Error('未找到文件上传输入框');
    }
  } catch (error) {
    console.error(`   ❌ 上传失败: ${error.message}`);
    throw error;
  }
}

/**
 * 填写标题
 */
async function fillTitle(page, title) {
  try {
    // 尝试多种选择器
    const selectors = [
      'input[placeholder*="标题"]',
      'input[name*="title"]',
      'input[id*="title"]',
      '[class*="title"] input[type="text"]',
      'input[type="text"]:nth-of-type(1)',
    ];
    
    for (const selector of selectors) {
      const input = await page.$(selector);
      if (input) {
        await input.fill(title);
        console.log(`   ✅ 标题已填写`);
        return;
      }
    }
    
    console.log('   ⚠️  未找到标题输入框，请手动填写');
  } catch (error) {
    console.error(`   ❌ 填写标题失败: ${error.message}`);
  }
}

/**
 * 填写描述
 */
async function fillDescription(page, description) {
  try {
    const selectors = [
      'textarea[placeholder*="简介"]',
      'textarea[placeholder*="描述"]',
      'textarea[name*="desc"]',
      '[class*="desc"] textarea',
      '[class*="description"] textarea',
    ];
    
    for (const selector of selectors) {
      const textarea = await page.$(selector);
      if (textarea) {
        await textarea.fill(description);
        console.log(`   ✅ 描述已填写`);
        return;
      }
    }
    
    console.log('   ⚠️  未找到描述输入框，请手动填写');
  } catch (error) {
    console.error(`   ❌ 填写描述失败: ${error.message}`);
  }
}

/**
 * 添加标签
 */
async function addTags(page, tags) {
  try {
    const tagList = tags.split(',').map(t => t.trim()).filter(t => t);
    
    const selectors = [
      'input[placeholder*="标签"]',
      'input[placeholder*="tag"]',
      '[class*="tag"] input',
    ];
    
    for (const selector of selectors) {
      const input = await page.$(selector);
      if (input) {
        for (const tag of tagList) {
          await input.fill(tag);
          await input.press('Enter');
          await page.waitForTimeout(500);
        }
        console.log(`   ✅ 标签已添加: ${tagList.join(', ')}`);
        return;
      }
    }
    
    console.log('   ⚠️  未找到标签输入框，请手动添加');
  } catch (error) {
    console.error(`   ❌ 添加标签失败: ${error.message}`);
  }
}

/**
 * 设置封面
 */
async function setCover(page, coverPath) {
  try {
    // 点击封面上传按钮
    const coverBtn = await page.$('[class*="cover"] button, [class*="cover"] [class*="upload"], .cover-upload');
    if (coverBtn) {
      await coverBtn.click();
      await page.waitForTimeout(1000);
      
      // 找到文件输入框
      const fileInput = await page.$('input[type="file"][accept*="image"]');
      if (fileInput) {
        await fileInput.setInputFiles(coverPath);
        console.log(`   ✅ 封面已设置: ${path.basename(coverPath)}`);
        await page.waitForTimeout(2000);
        return;
      }
    }
    
    console.log('   ⚠️  未找到封面上传按钮，请手动设置');
  } catch (error) {
    console.error(`   ❌ 设置封面失败: ${error.message}`);
  }
}

/**
 * 选择分区
 */
async function selectPartition(page, partitionName) {
  try {
    const partitionId = PARTITIONS[partitionName];
    if (!partitionId) {
      console.log(`   ⚠️  未知分区: ${partitionName}，使用默认分区`);
      return;
    }
    
    // 点击分区选择器
    const partitionSelector = await page.$('[class*="partition"], [class*="category"], [class*="type-select"]');
    if (partitionSelector) {
      await partitionSelector.click();
      await page.waitForTimeout(500);
      
      // 选择具体分区
      const option = await page.$(`[data-value="${partitionId}"], [data-id="${partitionId}"], text="${partitionName}"`);
      if (option) {
        await option.click();
        console.log(`   ✅ 分区已选择: ${partitionName}`);
      } else {
        console.log(`   ⚠️  未找到分区选项，请手动选择`);
      }
    } else {
      console.log('   ⚠️  未找到分区选择器，请手动选择');
    }
  } catch (error) {
    console.error(`   ❌ 选择分区失败: ${error.message}`);
  }
}

// 运行
main().catch(console.error);
