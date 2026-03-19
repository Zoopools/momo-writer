#!/usr/bin/env python3
"""
B 站评论图片抓取 - 调试版
先查看页面结构，找到正确的选择器
"""

from playwright.sync_api import sync_playwright
import time
import json

bv_id = "BV15QAUzXEtP"
video_url = f"https://www.bilibili.com/video/{bv_id}"

print("🚀 启动 Playwright 调试...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 有头模式方便调试
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )
    
    page = context.new_page()
    
    # 设置请求头
    page.set_extra_http_headers({
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com"
    })
    
    # 1️⃣ 打开视频页
    print(f"📥 打开视频：{video_url}")
    page.goto(video_url, wait_until="domcontentloaded")
    print("✅ 页面加载完成")
    
    # 2️⃣ 等待视频区域加载
    time.sleep(2)
    
    # 3️⃣ 滚动到评论区
    print("📜 滚动到评论区...")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
    time.sleep(2)
    
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    
    # 4️⃣ 查找评论区相关元素
    print("\n🔍 分析页面结构...\n")
    
    # 获取所有包含 'comment' 的类名
    class_names = page.evaluate("""
        () => {
            const allElements = document.querySelectorAll('*');
            const commentClasses = new Set();
            
            allElements.forEach(el => {
                const className = el.className;
                if (typeof className === 'string' && 
                    (className.toLowerCase().includes('comment') || 
                     className.toLowerCase().includes('reply'))) {
                    className.split(' ').forEach(c => commentClasses.add(c));
                }
            });
            
            return Array.from(commentClasses).slice(0, 30);
        }
    """)
    
    print("📋 找到包含 comment/reply 的类名:")
    for cls in class_names:
        print(f"   .{cls}")
    
    # 5️⃣ 查找图片元素
    print("\n🖼️  查找图片元素...")
    
    img_info = page.evaluate("""
        () => {
            const imgs = document.querySelectorAll('img');
            const result = [];
            
            imgs.forEach((img, i) => {
                const src = img.src || img.dataset?.src;
                if (src && src.includes('hdslb') || src.includes('bili')) {
                    result.push({
                        index: i,
                        src: src.substring(0, 100),
                        className: img.className,
                        id: img.id,
                        alt: img.alt,
                        parentClass: img.parentElement?.className
                    });
                }
            });
            
            return result.slice(0, 20);
        }
    """)
    
    print(f"\n找到 {len(img_info)} 张相关图片:")
    for img in img_info:
        print(f"\n[{img['index']}] {img['src']}...")
        print(f"    类名：{img['className']}")
        print(f"    父级：{img['parentClass']}")
    
    # 6️⃣ 尝试获取评论内容
    print("\n💬 尝试获取评论内容...")
    
    comments = page.evaluate("""
        () => {
            // 尝试多种选择器
            const selectors = [
                '.root-comment .reply-item',
                '.comment-list .comment-item',
                '[class*="CommentItem"]',
                '.bb-comment .comment-item',
                '.bili-dyn-item'
            ];
            
            let found = null;
            let usedSelector = '';
            
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    found = el;
                    usedSelector = sel;
                    break;
                }
            }
            
            if (found) {
                return {
                    found: true,
                    selector: usedSelector,
                    innerHTML: found.innerHTML.substring(0, 500),
                    outerHTML: found.outerHTML.substring(0, 500)
                };
            }
            
            return { found: false };
        }
    """)
    
    if comments.get('found'):
        print(f"✅ 找到评论区！选择器：{comments['selector']}")
        print(f"\nHTML 结构预览:\n{comments['innerHTML'][:300]}...")
    else:
        print("❌ 未找到评论区，可能需要更多时间加载")
    
    # 7️⃣ 截图保存
    print("\n📸 保存页面截图...")
    page.screenshot(path="/tmp/bili_debug.png", full_page=True)
    print("✅ 截图保存到 /tmp/bili_debug.png")
    
    print("\n⏸️  浏览器保持打开，请手动检查页面结构...")
    print("按 Enter 键关闭浏览器...")
    input()
    
    browser.close()

print("🔍 调试完成！")
