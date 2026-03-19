const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const htmlPath = path.join(__dirname, 'index.html');
  const outputPath = path.join(__dirname, 'openclaw-blueprint-infographic.png');
  
  console.log('🎨 小媒正在生成信息图...');
  console.log('📄 HTML 文件:', htmlPath);
  console.log('📤 输出文件:', outputPath);
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // 设置视口大小
  await page.setViewport({ width: 1080, height: 1920 });
  
  // 加载 HTML 文件
  await page.goto(`file://${htmlPath}`, { 
    waitUntil: 'networkidle0',
    timeout: 30000
  });
  
  // 等待渲染完成
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // 截图
  await page.screenshot({
    path: outputPath,
    fullPage: true,
    type: 'png'
  });
  
  await browser.close();
  
  console.log('✅ 截图完成！');
  console.log('📊 文件大小:', require('fs').statSync(outputPath).size, 'bytes');
})();
