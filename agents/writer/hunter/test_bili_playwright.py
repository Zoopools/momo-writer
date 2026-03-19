#!/usr/bin/env python3
"""
B 站评论图片抓取 - Playwright 版
模拟真人浏览器，绕过反爬
"""

from playwright.sync_api import sync_playwright
import time
import re
import os

bv_id = "BV15QAUzXEtP"
video_url = f"https://www.bilibili.com/video/{bv_id}"

print("🚀 启动 Playwright...")

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=True)
    
    # 创建页面
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    # 设置请求头
    page.set_extra_http_headers({
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com"
    })
    
    # 1️⃣ 打开视频页
    print(f"📥 打开视频：{video_url}")
    page.goto(video_url, wait_until="networkidle")
    time.sleep(3)  # 等待页面加载
    
    # 2️⃣ 滚动到评论区
    print("📜 滚动到评论区...")
    for i in range(5):
        page.evaluate("window.scrollBy(0, 1000)")
        time.sleep(1)
    
    # 3️⃣ 提取评论图片
    print("🔍 提取评论图片 URL...")
    
    img_urls = page.evaluate("""
        () => {
            const imgs = [];
            // B 站评论图片的常见选择器
            const selectors = [
                '.comment-container img',
                '.root-comment .reply-item img',
                '.bb-comment img',
                '[class*="comment"] img',
                '.bili-dyn-item__img'
            ];
            
            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach(img => {
                    let src = img.dataset?.src || img.src;
                    if (src && src.includes('hdslb.com')) {
                        imgs.push(src);
                    }
                });
            });
            
            // 去重
            return [...new Set(imgs)];
        }
    """)
    
    print(f"✅ 找到 {len(img_urls)} 张图片 URL\n")
    
    # 4️⃣ 清理 URL（去除压缩参数）
    clean_urls = []
    for url in img_urls:
        # 去除各种压缩参数
        clean = re.sub(r'\.\d+x\d+\.jpg$', '.jpg', url)
        clean = re.sub(r'@\d+w_\d+h\.[a-z]+$', '', clean)
        clean = re.sub(r'\?[\w=&%]+$', '', clean)  # 去除查询参数
        clean_urls.append(clean)
    
    # 去重
    clean_urls = list(dict.fromkeys(clean_urls))
    
    # 5️⃣ 下载前 3 张
    import requests
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com/"
    })
    
    for i, url in enumerate(clean_urls[:3], 1):
        print(f"📥 下载图片 {i}/3:")
        print(f"   URL: {url}")
        
        try:
            resp = session.get(url, timeout=10)
            if resp.status_code == 200:
                ext = url.split("?")[0].split(".")[-1] or "jpg"
                filename = f"/tmp/bili_pw_{i}.{ext}"
                with open(filename, "wb") as f:
                    f.write(resp.content)
                
                size = os.path.getsize(filename)
                print(f"   ✅ 保存：{filename} ({size / 1024:.1f} KB)")
            else:
                print(f"   ❌ 失败：{resp.status_code}")
        except Exception as e:
            print(f"   ❌ 错误：{e}")
        
        print()
    
    browser.close()

print("🎉 完成！")
