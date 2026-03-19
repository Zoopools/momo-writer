#!/usr/bin/env python3
"""
B 站评论区图片抓取 - CDP 直连版
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    save_dir = Path.home() / ".openclaw/temp/bili_comment_images_cdp"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        print("🔌 连接 CDP 浏览器...")
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        print("✅ 连接成功")
        
        # 打开新页面
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()
        
        print("📥 打开 B 站视频...")
        await page.goto("https://www.bilibili.com/video/BV15QAUzXEtP", wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        
        # 滚动到评论区
        print("📜 滚动到评论区...")
        for i in range(5):
            await page.evaluate("window.scrollBy(0, 500)")
            await page.wait_for_timeout(1500)
        
        # 提取所有图片
        print("🔍 提取图片...")
        images = await page.evaluate("""() => {
            const results = [];
            document.querySelectorAll('img').forEach(img => {
                const src = img.src || '';
                if (src.includes('/bfs/new_dyn/') || src.includes('/bfs/archive/')) {
                    // 排除头像
                    if (!src.includes('/bfs/face/') && !src.includes('/bfs/garb/') && !src.includes('/bfs/sycp/')) {
                        results.push({
                            src: src.split('@')[0],
                            width: img.naturalWidth || img.width,
                            height: img.naturalHeight || img.height,
                            alt: img.alt
                        });
                    }
                }
            });
            return results;
        }""")
        
        print(f"✅ 找到 {len(images)} 张用户图片")
        
        # 保存结果
        with open(save_dir / "images.json", "w", encoding="utf-8") as f:
            json.dump(images, f, ensure_ascii=False, indent=2)
        
        # 下载前 10 张
        print("\n🚀 下载图片...")
        for i, img in enumerate(images[:10]):
            try:
                response = await page.goto(img['src'])
                if response and response.status == 200:
                    buffer = await response.body()
                    save_path = save_dir / f"image_{i+1}.jpg"
                    with open(save_path, 'wb') as f:
                        f.write(buffer)
                    print(f"✅ 下载：image_{i+1}.jpg ({len(buffer)/1024:.1f} KB)")
            except Exception as e:
                print(f"❌ 失败：{e}")
        
        print(f"\n💾 保存到：{save_dir}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
