#!/usr/bin/env node
/**
 * 快速导出 - 连接已运行的 Chrome
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const AUTH_DIR = path.join(__dirname, '..', 'auth');

async function exportQuick() {
  const authFile = path.join(AUTH_DIR, 'bjh-work.json');
  
  console.log('🚀 快速导出登录态');
  console.log('💾 保存到:', authFile);
  
  // 尝试连接各种可能的端口
  const ports = [9222, 9223, 9224, 9333];
  let browser = null;
  
  for (const port of ports) {
    try {
      browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`);
      console.log(`✅ 已连接到 Chrome (端口: ${port})`);
      break;
    } catch (e) {
      console.log(`  端口 ${port} 未连接`);
    }
  }
  
  if (!browser) {
    console.error('❌ 无法连接到任何 Chrome 实例');
    console.log('\n请确保 Chrome 已启动调试模式:');
    console.log('  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222');
    process.exit(1);
  }
  
  // 获取第一个上下文
  const context = browser.contexts()[0];
  if (!context) {
    console.error('❌ 未找到浏览器上下文');
    process.exit(1);
  }
  
  // 保存登录态
  await context.storageState({ path: authFile });
  
  console.log('\n✅ 登录态导出成功!');
  console.log('📁 文件:', authFile);
  console.log('\n现在可以关闭 Chrome，使用 publish.js 进行自动发布了');
}

exportQuick().catch(err => {
  console.error('❌ 导出失败:', err.message);
  process.exit(1);
});
