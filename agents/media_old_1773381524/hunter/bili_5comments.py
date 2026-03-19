#!/usr/bin/env python3
"""
B 站评论区图片抓取 - 简单版
目标：抓取 5 条带图评论（评论内容 + 图片）
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    save_dir = Path.home() / ".openclaw/temp/bili_5comments"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        print("🔌 连接 CDP 浏览器...")
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=60000)
            print("✅ 连接成功")
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            print("💡 请确保 Chrome CDP 已启动：./start-chrome-debug.sh")
            return
        
        # 使用现有上下文
        contexts = browser.contexts
        if not contexts:
            context = await browser.new_context()
        else:
            context = contexts[0]
        
        pages = context.pages
        if pages:
            page = pages[0]
        else:
            page = await context.new_page()
        
        print("📥 打开 B 站视频...")
        await page.goto("https://www.bilibili.com/video/BV15QAUzXEtP", wait_until="domcontentloaded", timeout=60000)
        print("⏳ 等待页面加载...")
        await page.wait_for_timeout(8000)
        
        # 滚动到评论区
        print("📜 滚动到评论区...")
        for i in range(15):
            await page.evaluate("window.scrollBy(0, 200)")
            await page.wait_for_timeout(800)
        
        # 额外等待评论加载
        print("⏳ 等待评论加载...")
        await page.wait_for_timeout(5000)
        
        # 提取评论
        print("🔍 提取带图评论...")
        comments = await page.evaluate("""() => {
            const results = [];
            // B 站评论选择器
            const commentItems = document.querySelectorAll('[class*="comment-item"], .comment-list .item, [class*="comment-container"]');
            
            commentItems.forEach(item => {
                if (results.length >= 10) return;
                
                // 获取用户名
                const userEl = item.querySelector('[class*="user-name"], .user-name, [class*="username"]');
                const username = userEl ? userEl.textContent.trim() : '未知用户';
                
                // 获取评论内容
                const contentEl = item.querySelector('[class*="content"], .comment-content, [class*="message"]');
                const content = contentEl ? contentEl.textContent.trim() : '';
                
                // 获取图片
                const imgs = item.querySelectorAll('img');
                const images = [];
                imgs.forEach(img => {
                    const src = img.src || '';
                    // 只保留用户发的图片（new_dyn 或 archive）
                    if ((src.includes('/bfs/new_dyn/') || src.includes('/bfs/archive/')) &&
                        !src.includes('/bfs/face/') && 
                        !src.includes('/bfs/garb/') &&
                        !src.includes('/bfs/sycp/') &&
                        !src.includes('/bfs/activity-plat/')) {
                        images.push(src.split('@')[0]);
                    }
                });
                
                // 只保存带图的评论
                if (images.length > 0 && content) {
                    results.push({
                        user: username,
                        content: content,
                        images: images
                    });
                }
            });
            
            return results;
        }""")
        
        print(f"✅ 找到 {len(comments)} 条带图评论")
        
        # 保存评论数据
        with open(save_dir / "comments.json", "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        
        # 下载图片
        print("\n🚀 下载图片...")
        downloaded = 0
        for i, comment in enumerate(comments[:5]):
            print(f"\n📝 评论 {i+1}: {comment['user']}")
            print(f"   内容：{comment['content'][:80]}...")
            
            for j, img_url in enumerate(comment['images'][:2]):  # 每条评论最多下 2 张图
                try:
                    response = await page.goto(img_url, timeout=30000)
                    if response and response.status == 200:
                        buffer = await response.body()
                        save_path = save_dir / f"comment{i+1}_img{j+1}.jpg"
                        with open(save_path, 'wb') as f:
                            f.write(buffer)
                        print(f"   ✅ 下载：comment{i+1}_img{j+1}.jpg ({len(buffer)/1024:.1f} KB)")
                        downloaded += 1
                except Exception as e:
                    print(f"   ❌ 下载失败：{e}")
        
        print(f"\n💾 保存到：{save_dir}")
        print(f"📊 总计：{len(comments[:5])} 条评论，{downloaded} 张图片")
        
        # 打印结果
        print("\n" + "="*50)
        print("📋 评论列表：")
        print("="*50)
        for i, comment in enumerate(comments[:5], 1):
            print(f"\n【评论{i}】{comment['user']}")
            print(f"内容：{comment['content']}")
            print(f"图片：{len(comment['images'])} 张")
            for img in comment['images'][:2]:
                print(f"  - {img[:80]}...")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
