#!/usr/bin/env python3
"""
下载 B 站评论图片并上传到飞书
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def download_comment_images():
    save_dir = Path.home() / ".openclaw/temp/bili_real_comment_images"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        
        print("📥 打开 B 站视频...")
        await page.goto("https://www.bilibili.com/video/BV15QAUzXEtP", wait_until="domcontentloaded")
        await page.wait_for_timeout(8000)
        
        # 滚动到评论区
        print("📜 滚动到评论区...")
        for i in range(15):
            await page.evaluate("window.scrollBy(0, 200)")
            await page.wait_for_timeout(800)
        
        # 等待图片加载
        print("⏳ 等待图片加载...")
        await page.wait_for_timeout(10000)
        
        # 提取图片 - 尝试所有可能的选择器
        print("🔍 提取评论图片...")
        images = await page.evaluate("""() => {
            const results = [];
            // 尝试多种选择器
            const selectors = [
                '.root-comment-container img',
                '.comment-item img',
                '[class*="reply"] img',
                '[class*="comment"] img',
                '.reply-item img',
                'img[src*="/bfs/new_dyn/"]',
                'img[src*="/bfs/archive/"]'
            ];
            
            let allImgs = [];
            selectors.forEach(sel => {
                allImgs = allImgs.concat(Array.from(document.querySelectorAll(sel)));
            });
            
            // 去重
            allImgs = [...new Set(allImgs)];
            
            allImgs.forEach((img, i) => {
                if (results.length >= 10) return;
                const src = img.src || '';
                if ((src.includes('/bfs/new_dyn/') || src.includes('/bfs/archive/')) && 
                    !src.includes('/bfs/face/') && 
                    !src.includes('cover') && 
                    !src.includes('.avif') &&
                    src.length > 50 &&
                    img.width > 50 &&
                    img.height > 50) {
                    results.push({
                        index: i,
                        src: src.split('@')[0],
                        alt: img.alt,
                        width: img.width,
                        height: img.height
                    });
                }
            });
            return results;
        }""")
        
        print(f"✅ 找到 {len(images)} 张评论图片")
        
        # 下载图片
        for i, img in enumerate(images):
            try:
                response = await page.goto(img['src'])
                if response and response.status == 200:
                    buffer = await response.body()
                    save_path = save_dir / f"comment_{i+1}.jpg"
                    with open(save_path, 'wb') as f:
                        f.write(buffer)
                    print(f"✅ 下载：comment_{i+1}.jpg ({len(buffer)/1024:.1f} KB)")
            except Exception as e:
                print(f"❌ 下载失败：{e}")
        
        await browser.close()
        return save_dir

if __name__ == "__main__":
    save_dir = asyncio.run(download_comment_images())
    print(f"\n💾 图片保存到：{save_dir}")
