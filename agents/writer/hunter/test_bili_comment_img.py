#!/usr/bin/env python3
"""
B 站评论图片抓取 - API 版
直接调用评论 API 获取原图
"""

import requests
import re
import json
import time

# BV 号
bv_id = "BV15QAUzXEtP"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/",
    "Origin": "https://www.bilibili.com"
})

# 1️⃣ 先获取视频的真实 OID（评论需要）
print("📌 获取视频信息...")
video_url = f"https://www.bilibili.com/video/{bv_id}"
resp = session.get(video_url)
html = resp.text

# 从 HTML 中提取 OID
oid_match = re.search(r'"oid"\s*:\s*(\d+)', html)
if oid_match:
    oid = oid_match.group(1)
    print(f"✅ OID: {oid}")
else:
    # 尝试其他提取方式
    oid_match = re.search(r'oid=(\d+)', html)
    if oid_match:
        oid = oid_match.group(1)
        print(f"✅ OID: {oid}")
    else:
        print("❌ 未找到 OID，尝试用 API...")
        # 用 API 获取
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
        resp = session.get(api_url)
        data = resp.json()
        if data.get("code") == 0:
            oid = data["data"]["aid"]
            print(f"✅ 从 API 获取 OID: {oid}")
        else:
            print("❌ 无法获取 OID")
            exit(1)

# 2️⃣ 调用评论 API
print(f"\n📥 获取评论区...")
comment_api = f"https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type=1&mode=3&pagination_str=%7B%22next_offset%22:%22%22%7D"

resp = session.get(comment_api)
data = resp.json()

if data.get("code") != 0:
    print(f"❌ API 错误：{data}")
    exit(1)

# 3️⃣ 提取评论中的图片
print("✅ 获取评论成功！\n")

replies = data.get("data", {}).get("replies", [])
if not replies:
    print("❌ 没有找到评论")
    exit(1)

print(f"📊 找到 {len(replies)} 条评论\n")

# 遍历评论找图片
img_urls = []
for i, reply in enumerate(replies[:20]):  # 先看前 20 条
    content = reply.get("content", {})
    pictures = content.get("pictures", [])
    
    if pictures:
        comment_id = reply.get("rpid")
        user = reply.get("member", {}).get("uname", "未知")
        print(f"💬 评论 {i+1} by @{user}: 包含 {len(pictures)} 张图片")
        
        for pic in pictures:
            img_url = pic.get("img_src") or pic.get("img_url")
            if img_url:
                # 去除压缩参数
                clean_url = re.sub(r'\.\d+x\d+\.jpg$', '.jpg', img_url)
                clean_url = re.sub(r'@\d+w_\d+h\.[a-z]+$', '', clean_url)
                img_urls.append(clean_url)
                print(f"   🖼️  {clean_url}")

# 4️⃣ 下载前 3 张测试
print(f"\n✅ 共找到 {len(img_urls)} 张评论图片\n")

if img_urls:
    for i, url in enumerate(img_urls[:3], 1):
        print(f"📥 下载图片 {i}/3: {url}")
        
        try:
            img_resp = session.get(url, timeout=10)
            if img_resp.status_code == 200:
                ext = url.split(".")[-1].split("?")[0] or "jpg"
                filename = f"/tmp/bili_comment_{i}.{ext}"
                with open(filename, "wb") as f:
                    f.write(img_resp.content)
                
                import os
                size = os.path.getsize(filename)
                print(f"   ✅ 保存到 {filename} ({size / 1024:.1f} KB)")
            else:
                print(f"   ❌ 下载失败：{img_resp.status_code}")
        except Exception as e:
            print(f"   ❌ 错误：{e}")
        
        time.sleep(0.5)  # 避免太快

print("\n🎉 完成！")
