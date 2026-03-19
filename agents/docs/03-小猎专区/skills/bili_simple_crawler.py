#!/usr/bin/env python3
"""
精简版 B 站评论爬虫 - 基于 Playwright
专门抓取 BV15QAUzXEtP 的评论和用户截图
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def fetch_bilibili_comments():
    """使用 Playwright 抓取 B 站评论"""
    
    video_url = "https://www.bilibili.com/video/BV15QAUzXEtP"
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        page = await context.new_page()
        
        print("🚀 正在打开视频页面...")
        await page.goto(video_url, wait_until="domcontentloaded")
        
        # 等待页面加载
        print("📥 等待页面加载...")
        await page.wait_for_timeout(10000)
        
        # 滚动到底部加载评论
        print("📜 滚动到评论区...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(5000)
        
        # 等待评论渲染
        await page.wait_for_timeout(5000)
        
        # 提取评论数据
        print("🔍 提取评论数据...")
        comments_data = await page.evaluate("""() => {
            const comments = [];
            // B 站评论区选择器
            const commentItems = document.querySelectorAll('[class*="comment-item"], [class*="reply-item"], .comment-list .item');
            
            commentItems.forEach((item, index) => {
                if (index >= 20) return;
                
                const userElement = item.querySelector('[class*="user-name"], [class*="username"], .user-name');
                const contentElement = item.querySelector('[class*="content"], .comment-content');
                const images = item.querySelectorAll('img');
                
                const comment = {
                    user: userElement?.textContent?.trim() || '未知用户',
                    content: contentElement?.textContent?.trim() || '',
                    images: Array.from(images)
                        .map(img => img.src || img.dataset?.src)
                        .filter(src => src && src.includes('bfs'))
                        .slice(0, 5),  // 每条评论最多 5 张图
                    time: item.querySelector('[class*="time"], .time')?.textContent?.trim() || ''
                };
                
                if (comment.content) {
                    comments.push(comment);
                }
            });
            
            return comments;
        }""")
        
        print(f"✅ 获取到 {len(comments_data)} 条评论")
        
        # 筛选带图评论
        image_comments = [c for c in comments_data if c.get('images')]
        print(f"🖼️  其中 {len(image_comments)} 条带图")
        
        # 保存结果
        save_dir = Path.home() / ".openclaw/temp/mediacrawler_bili"
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存评论数据
        with open(save_dir / "comments.json", "w", encoding="utf-8") as f:
            json.dump(comments_data, f, ensure_ascii=False, indent=2)
        
        # 保存带图评论
        with open(save_dir / "image_comments.json", "w", encoding="utf-8") as f:
            json.dump(image_comments, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 数据已保存到：{save_dir}")
        
        # 显示前 3 条带图评论
        print("\n" + "=" * 50)
        print("📊 前 3 条带图评论：")
        print("=" * 50)
        
        for i, comment in enumerate(image_comments[:3], 1):
            print(f"\n[{i}] 用户：{comment['user']}")
            print(f"    评论：{comment['content'][:60]}...")
            print(f"    图片：{len(comment['images'])} 张")
            for img_url in comment['images'][:2]:
                print(f"         - {img_url[:80]}...")
        
        await browser.close()
        
        return image_comments

if __name__ == "__main__":
    print("🔍 精简版 B 站评论爬虫")
    print("=" * 50)
    
    try:
        result = asyncio.run(fetch_bilibili_comments())
        print("\n✨ 完成！")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
