#!/usr/bin/env python3
"""
B 站评论区图片抓取脚本
专门抓取 BV15QAUzXEtP 评论区的所有用户截图
"""

import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright

async def fetch_bilibili_comment_images():
    """使用 Playwright 抓取 B 站评论图片"""
    
    video_url = "https://www.bilibili.com/video/BV15QAUzXEtP"
    save_dir = Path.home() / ".openclaw/temp/bili_comment_images"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        # 启动浏览器（使用 CDP 模式，复用已登录的 Chrome）
        print("🚀 连接 CDP 浏览器...")
        
        # 连接到 CDP Chrome
        browser = await p.chromium.connect_over_cdp(
            "http://127.0.0.1:9222",
            timeout=10000
        )
        print("✅ 连接到 CDP Chrome 浏览器")
        context = browser.contexts[0]
        
        page = await context.new_page()
        
        print(f"📥 打开视频页面：{video_url}")
        await page.goto(video_url, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        
        # 滚动到评论区
        print("📜 滚动到评论区...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(3000)
        
        # 多次滚动加载更多评论
        for i in range(3):
            print(f"🔄 第 {i+1} 次滚动加载更多评论...")
            await page.evaluate("window.scrollBy(0, 500)")
            await page.wait_for_timeout(2000)
        
        # 提取所有评论图片
        print("🔍 提取评论图片...")
        
        # 调试：先获取所有图片看看
        debug_images = await page.evaluate("""() => {
            const allImages = [];
            const commentItems = document.querySelectorAll('[class*="comment"], .comment-list .item');
            commentItems.forEach((item, i) => {
                if (i >= 5) return;
                const imgs = item.querySelectorAll('img');
                imgs.forEach(img => {
                    const src = img.src || img.dataset?.src;
                    if (src) {
                        allImages.push({
                            src: src,
                            width: img.width,
                            height: img.height,
                            alt: img.alt
                        });
                    }
                });
            });
            return allImages;
        }""")
        
        print(f"\n🔍 调试：前 5 条评论共有 {len(debug_images)} 张图片")
        for i, img in enumerate(debug_images[:10]):
            print(f"  [{i}] {img['src'][:80]}... ({img['width']}x{img['height']})")
        
        images_data = await page.evaluate("""() => {
            const results = [];
            
            // 查找所有评论元素
            const commentItems = document.querySelectorAll('[class*="comment-item"], [class*="reply-item"], .comment-list .item, .comment-container');
            
            commentItems.forEach((item, index) => {
                // 获取用户信息
                const userElement = item.querySelector('[class*="user-name"], .user-name, [class*="username"]');
                const contentElement = item.querySelector('[class*="content"], .comment-content, [class*="text"]');
                
                // 获取所有图片
                const imgElements = item.querySelectorAll('img');
                const images = [];
                
                imgElements.forEach(img => {
                    const src = img.src || img.dataset?.src || img.dataset?.original;
                    if (!src) return;
                    
                    const width = img.naturalWidth || img.width;
                    const height = img.naturalHeight || img.height;
                    
                    // ✅ 用户截图规则：
                    // 1. 域名：i0/i1/i2.hdslb.com
                    // 2. 路径：/bfs/new_dyn/ 或 /bfs/archive/
                    // 3. 排除：头像、表情、等级图标等
                    
                    const isUserImage = (
                        // 域名正确
                        (src.includes('i0.hdslb.com') || 
                         src.includes('i1.hdslb.com') || 
                         src.includes('i2.hdslb.com')) &&
                        // 路径正确
                        (src.includes('/bfs/new_dyn/') || src.includes('/bfs/archive/')) &&
                        // 排除头像
                        !src.includes('/bfs/face/') &&
                        // 排除表情包
                        !src.includes('/bfs/emote/') &&
                        // 排除三连表情
                        !src.includes('/bfs/sycp/') &&
                        // 排除装扮
                        !src.includes('/bfs/garb/') &&
                        // 排除活动素材
                        !src.includes('/bfs/activity-plat/') &&
                        // 排除横幅
                        !src.includes('/bfs/banner/') &&
                        // 尺寸合理（不是太小的图标）
                        (width >= 50 && height >= 50)
                    );
                    
                    if (isUserImage) {
                        images.push({
                            src: src.split('@')[0],  // 去除压缩后缀
                            alt: img.alt || '',
                            width: width,
                            height: height
                        });
                    }
                });
                
                if (images.length > 0) {
                    results.push({
                        index: index,
                        user: userElement?.textContent?.trim() || '未知用户',
                        content: contentElement?.textContent?.trim() || '',
                        images: images
                    });
                }
            });
            
            return results;
        }""")
        
        print(f"✅ 找到 {len(images_data)} 条带图评论")
        
        # 调试：输出所有找到的图片
        print("\n🔍 调试信息 - 所有评论图片：")
        for comment in images_data[:5]:
            print(f"  评论：{comment['user']}: {comment['content'][:50]}...")
            for img in comment['images']:
                print(f"    - {img['src']} ({img['width']}x{img['height']})")
        
        # 保存图片信息
        with open(save_dir / "images_info.json", "w", encoding="utf-8") as f:
            json.dump(images_data, f, ensure_ascii=False, indent=2)
        
        # 下载图片
        print(f"\n🚀 开始下载图片...")
        downloaded_count = 0
        
        for comment in images_data:
            for i, img_info in enumerate(comment['images']):
                img_url = img_info['src']
                
                # 生成文件名
                filename = f"comment{comment['index']}_img{i}_{comment['user'][:10]}.jpg"
                save_path = save_dir / filename
                
                try:
                    # 下载图片
                    response = await page.goto(img_url)
                    if response and response.status == 200:
                        buffer = await response.body()
                        with open(save_path, 'wb') as f:
                            f.write(buffer)
                        print(f"✅ 下载：{filename}")
                        downloaded_count += 1
                    else:
                        print(f"❌ 下载失败：{img_url}")
                except Exception as e:
                    print(f"⚠️  错误：{e}")
        
        print(f"\n💾 数据保存到：{save_dir}")
        print(f"📊 下载完成：{downloaded_count} 张图片")
        
        # 返回结果
        return {
            "save_dir": str(save_dir),
            "total_comments": len(images_data),
            "total_images": downloaded_count,
            "images_info": images_data
        }

if __name__ == "__main__":
    print("=" * 50)
    print("🔍 B 站评论区图片抓取工具")
    print("=" * 50)
    
    try:
        result = asyncio.run(fetch_bilibili_comment_images())
        
        print("\n" + "=" * 50)
        print("✨ 完成！")
        print(f"📁 保存目录：{result['save_dir']}")
        print(f"📊 带图评论：{result['total_comments']} 条")
        print(f"🖼️  下载图片：{result['total_images']} 张")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
