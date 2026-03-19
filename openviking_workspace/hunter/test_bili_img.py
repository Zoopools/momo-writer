#!/usr/bin/env python3
"""
B 站评论图片抓取测试
获取原图 URL（非截图）
"""

import requests
import re
import json

# 视频 ID（从 URL 提取）
video_url = "https://b23.tv/I9wkO0d"

# 1️⃣ 先获取真实视频 URL（b23.tv 是短链接）
print("📌 解析短链接...")
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/"
})

resp = session.get(video_url, allow_redirects=True)
real_url = resp.url
print(f"✅ 真实 URL: {real_url}")

# 2️⃣ 提取 BV 号
bv_match = re.search(r'(BV\w+)', real_url)
if bv_match:
    bv_id = bv_match.group(1)
    print(f"✅ BV 号：{bv_id}")
else:
    print("❌ 未找到 BV 号")
    exit(1)

# 3️⃣ 获取视频页面 HTML
print("\n📥 获取页面 HTML...")
resp = session.get(real_url)
html = resp.text

# 4️⃣ 尝试从 HTML 中提取图片 URL
# B 站评论区是动态加载的，但我们可以找一些静态图片
print("\n🔍 搜索图片 URL...")

# 找所有 http 开头的图片 URL
img_urls = re.findall(r'https://i\d\.hdslb\.com/bfs/[^"\s<>]+', html)

# 去重
img_urls = list(set(img_urls))

print(f"✅ 找到 {len(img_urls)} 张图片 URL\n")

# 5️⃣ 显示前 3 张
for i, url in enumerate(img_urls[:3], 1):
    # 去除压缩参数
    clean_url = re.sub(r'@\d+w_\d+h\.[a-z]+$', '', url)
    print(f"【图片 {i}】")
    print(f"  原始：{url}")
    print(f"   cleaned: {clean_url}")
    print()

# 6️⃣ 下载测试
if img_urls:
    test_url = re.sub(r'@\d+w_\d+h\.[a-z]+$', '', img_urls[0])
    print(f"📥 下载测试：{test_url}")
    
    img_resp = session.get(test_url)
    if img_resp.status_code == 200:
        with open("/tmp/bili_test_img.png", "wb") as f:
            f.write(img_resp.content)
        print("✅ 下载成功！保存到 /tmp/bili_test_img.png")
        
        # 显示文件大小
        import os
        size = os.path.getsize("/tmp/bili_test_img.png")
        print(f"📊 文件大小：{size / 1024:.1f} KB")
    else:
        print(f"❌ 下载失败：{img_resp.status_code}")
