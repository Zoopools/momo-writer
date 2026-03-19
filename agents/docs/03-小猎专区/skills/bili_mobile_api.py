#!/usr/bin/env python3
"""
B 站评论图片抓取 - 移动端 API 版
移动端 API 限制较少，更容易获取
"""

import requests
import re
import json
import time
import os

bv_id = "BV15QAUzXEtP"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 osType/ios osVersion/17.0 model/iphone14pro build/7.40.0 osi/jacketStatus/0",
    "Referer": "https://m.bilibili.com/",
})

# 1️⃣ 获取视频信息（获取 aid）
print("📌 获取视频信息...")
video_info_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
resp = session.get(video_info_url)
video_data = resp.json()

if video_data.get("code") != 0:
    print(f"❌ 视频信息获取失败：{video_data}")
    exit(1)

aid = video_data["data"]["aid"]
print(f"✅ aid: {aid}")
print(f"📺 标题：{video_data['data']['title']}")

# 2️⃣ 获取评论区（移动端 API）
print(f"\n📥 获取评论区...")

# 移动端评论 API
comment_url = f"https://api.bilibili.com/x/v2/reply/main?oid={aid}&type=1&mode=3&next=0"

resp = session.get(comment_url)
comment_data = resp.json()

if comment_data.get("code") != 0:
    print(f"❌ 评论获取失败：{comment_data}")
    print("\n💡 可能需要登录或 API 有访问限制")
    exit(1)

replies = comment_data.get("data", {}).get("replies", [])
print(f"✅ 获取到 {len(replies)} 条评论\n")

# 3️⃣ 提取评论图片
img_urls = []

for i, reply in enumerate(replies):
    content = reply.get("content", {})
    pictures = content.get("pictures", [])
    
    if pictures:
        user = reply.get("member", {}).get("uname", "未知用户")
        print(f"💬 评论 {i+1} by @{user}: {len(pictures)} 张图片")
        
        for pic in pictures:
            img_url = pic.get("img_src") or pic.get("img_url")
            if img_url:
                # 清理 URL（去除压缩参数）
                clean = re.sub(r'\.\d+x\d+\.jpg$', '.jpg', img_url)
                clean = re.sub(r'@\d+w_\d+h\.[a-z]+$', '', clean)
                clean = re.sub(r'\?[\w=&%]+$', '', clean)
                
                img_urls.append({
                    "url": clean,
                    "user": user,
                    "comment": content.get("message", "")[:50]
                })
                print(f"   🖼️  {clean}")

print(f"\n📊 共找到 {len(img_urls)} 张评论图片\n")

# 4️⃣ 下载前 3 张
if img_urls:
    print("📥 下载前 3 张原图测试...\n")
    
    for i, img_info in enumerate(img_urls[:3], 1):
        url = img_info["url"]
        print(f"[{i}/3] 用户：@{img_info['user']}")
        print(f"     评论：{img_info['comment']}...")
        print(f"     URL: {url}")
        
        try:
            img_resp = session.get(url, timeout=15)
            if img_resp.status_code == 200:
                ext = url.split("?")[0].split(".")[-1] or "jpg"
                filename = f"/tmp/bili_mobile_{i}.{ext}"
                with open(filename, "wb") as f:
                    f.write(img_resp.content)
                
                size = os.path.getsize(filename)
                print(f"     ✅ 保存：{filename} ({size / 1024:.1f} KB)")
                
                # 显示尺寸
                from PIL import Image
                with Image.open(filename) as img:
                    print(f"     📐 分辨率：{img.width}x{img.height}")
            else:
                print(f"     ❌ HTTP {img_resp.status_code}")
        except Exception as e:
            print(f"     ❌ 错误：{e}")
        
        print()
        time.sleep(0.5)

print("🎉 完成！")

# 保存所有 URL 到文件
if img_urls:
    with open("/tmp/bili_img_urls.json", "w", encoding="utf-8") as f:
        json.dump(img_urls, f, ensure_ascii=False, indent=2)
    print(f"📄 所有图片 URL 已保存到 /tmp/bili_img_urls.json")
