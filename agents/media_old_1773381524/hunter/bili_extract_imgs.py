#!/usr/bin/env python3
"""
B 站评论图片抓取 - 多选择器尝试版
自动尝试多种选择器，找到能提取评论图片的方案
"""

from playwright.sync_api import sync_playwright
import time
import re
import os

bv_id = "BV15QAUzXEtP"
video_url = f"https://www.bilibili.com/video/{bv_id}"

print("🚀 启动 Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080}
    )
    
    page = context.new_page()
    page.set_extra_http_headers({
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com"
    })
    
    # 1️⃣ 打开页面
    print(f"📥 打开：{video_url}")
    page.goto(video_url, wait_until="domcontentloaded", timeout=60000)
    print("✅ 页面加载完成")
    
    # 2️⃣ 等待 + 滚动
    print("\n📜 滚动加载评论...")
    time.sleep(3)
    
    for i in range(5):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(1.5)
        print(f"   滚动 {i+1}/5")
    
    # 3️⃣ 尝试多种选择器提取评论容器
    selectors_to_try = [
        # 常见 B 站选择器
        '.root-comment .reply-item',
        '.comment-list .comment-item',
        '[class*="comment-item"]',
        '[class*="CommentItem"]',
        '.bb-comment .comment-item',
        '.bili-dyn-item',
        # 通用选择器
        '.comment-container',
        '#comment-list .item',
        '.main-container .comment',
    ]
    
    print("\n🔍 尝试不同选择器...")
    
    for selector in selectors_to_try:
        count = page.evaluate(f"""
            () => document.querySelectorAll('{selector}').length
        """)
        if count > 0:
            print(f"   ✅ {selector} → {count} 个元素")
        else:
            print(f"   ❌ {selector} → 0 个")
    
    # 4️⃣ 提取所有图片（不管选择器）
    print("\n🖼️  提取所有 B 站相关图片...")
    
    all_imgs = page.evaluate("""
        () => {
            const imgs = document.querySelectorAll('img');
            const result = [];
            
            imgs.forEach(img => {
                let src = img.src || img.dataset?.src || img.dataset?.original;
                
                if (src && (src.includes('hdslb.com') || src.includes('bili.com'))) {
                    // 获取上下文信息
                    const parent = img.parentElement;
                    const grandParent = parent?.parentElement;
                    
                    result.push({
                        src: src,
                        className: img.className || '',
                        parentClass: parent?.className || '',
                        grandParentClass: grandParent?.className || '',
                        alt: img.alt || '',
                        width: img.width,
                        height: img.height
                    });
                }
            });
            
            return result;
        }
    """)
    
    print(f"✅ 找到 {len(all_imgs)} 张图片\n")
    
    # 5️⃣ 过滤出评论区图片（根据父级类名判断）
    comment_keywords = ['comment', 'reply', 'dynamic']
    comment_imgs = []
    
    for img in all_imgs:
        combined = (img['className'] + ' ' + img['parentClass'] + ' ' + img['grandParentClass']).lower()
        if any(kw in combined for kw in comment_keywords):
            comment_imgs.append(img)
    
    print(f"📋 评论区相关图片：{len(comment_imgs)} 张\n")
    
    # 6️⃣ 清理 URL 并去重
    def clean_url(url):
        # 去除各种压缩参数
        url = re.sub(r'\.\d+x\d+\.jpg$', '.jpg', url)
        url = re.sub(r'@\d+w_\d+h\.[a-z]+$', '', url)
        url = re.sub(r'@\d+w$', '', url)
        url = re.sub(r'\?[\w=&%]+$', '', url)
        return url
    
    clean_urls = list(dict.fromkeys([clean_url(img['src']) for img in comment_imgs]))
    
    # 7️⃣ 显示结果
    print("📸 评论图片 URL:")
    for i, url in enumerate(clean_urls[:10], 1):
        print(f"   {i}. {url}")
    
    # 8️⃣ 下载前 3 张
    if clean_urls:
        print(f"\n📥 下载前 3 张测试...")
        
        import requests
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com/"
        })
        
        for i, url in enumerate(clean_urls[:3], 1):
            print(f"\n下载 {i}/3: {url}")
            
            try:
                resp = session.get(url, timeout=15)
                if resp.status_code == 200:
                    ext = url.split("?")[0].split(".")[-1] or "jpg"
                    filename = f"/tmp/bili_final_{i}.{ext}"
                    with open(filename, "wb") as f:
                        f.write(resp.content)
                    
                    size = os.path.getsize(filename)
                    print(f"   ✅ {filename} ({size / 1024:.1f} KB)")
                    
                    # 显示图片信息
                    from PIL import Image
                    with Image.open(filename) as img:
                        print(f"   📐 尺寸：{img.width}x{img.height}")
                else:
                    print(f"   ❌ HTTP {resp.status_code}")
            except Exception as e:
                print(f"   ❌ {e}")
    
    browser.close()

print("\n🎉 完成！")
