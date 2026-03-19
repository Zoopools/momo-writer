#!/usr/bin/env node
/**
 * GEO 发布系统 - 登录态导出（最终版）
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_DIR = path.resolve(__dirname, '..');
const AUTH_DIR = path.join(BASE_DIR, 'auth');

if (!fs.existsSync(AUTH_DIR)) fs.mkdirSync(AUTH_DIR, { recursive: true });

async function exportAuth() {
  console.log('\n🚀 百家号登录态导出\n');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('📍 请手动导航到 https://baijiahao.baidu.com 并登录');
  console.log('💡 浏览器已打开，请自由操作\n');
  
  // 打开一个空白页，让用户自己导航
  await page.goto('about:blank');

  // 等待用户按回车
  console.log('👉 登录完成后，按回车保存登录态...');
  await new Promise(resolve => process.stdin.once('data', resolve));

  // 保存登录态
  const authFile = path.join(AUTH_DIR, 'bjh-work.json');
  await context.storageState({ path: authFile });

  await browser.close();

  if (fs.existsSync(authFile)) {
    const size = fs.statSync(authFile).size;
    console.log(`\n✅ 登录态导出成功! (${size} bytes)`);
    console.log(`📁 ${authFile}\n`);
  } else {
    console.log('\n❌ 导出失败\n');
    process.exit(1);
  }
}

exportAuth().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
