#!/usr/bin/env python3
"""
B 站评论图片抓取 - 导出表格版
获取评论图片 + 文案，导出为 CSV/Excel 格式
"""

import requests
import re
import json
import time
import os
import csv

# ============ 配置区 ============
BV_ID = "BV15QAUzXEtP"  # 修改这里
OUTPUT_DIR = "/Users/wh1ko/Documents/openclaw/agents/hunter/bili_images"
# ===============================

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 osType/ios osVersion/17.0 model/iphone14pro build/7.40.0 osi/jacketStatus/0",
    "Referer": "https://m.bilibili.com/",
})

print(f"📺 开始抓取 BV 号：{BV_ID}\n")

# 1️⃣ 获取视频信息（获取 aid）
print("📌 获取视频信息...")
video_info_url = f"https://api.bilibili.com/x/web-interface/view?bvid={BV_ID}"
resp = session.get(video_info_url)
video_data = resp.json()

if video_data.get("code") != 0:
    print(f"❌ 视频信息获取失败：{video_data}")
    exit(1)

aid = video_data["data"]["aid"]
title = video_data["data"]["title"]
print(f"✅ 标题：{title}")
print(f"✅ aid: {aid}\n")

# 2️⃣ 获取评论区
print(f"📥 获取评论区...")
comment_url = f"https://api.bilibili.com/x/v2/reply/main?oid={aid}&type=1&mode=3&next=0"
resp = session.get(comment_url)
comment_data = resp.json()

if comment_data.get("code") != 0:
    print(f"❌ 评论获取失败：{comment_data}")
    exit(1)

replies = comment_data.get("data", {}).get("replies", [])
print(f"✅ 获取到 {len(replies)} 条评论\n")

# 3️⃣ 提取评论图片
img_records = []

for i, reply in enumerate(replies):
    content = reply.get("content", {})
    pictures = content.get("pictures", [])
    
    if pictures:
        user = reply.get("member", {}).get("uname", "未知用户")
        comment_text = content.get("message", "")
        reply_id = reply.get("rpid")
        create_time = reply.get("ctime", 0)
        
        print(f"💬 评论 {i+1} by @{user}: {len(pictures)} 张图片")
        
        for j, pic in enumerate(pictures):
            img_url = pic.get("img_src") or pic.get("img_url")
            if img_url:
                # 清理 URL（去除压缩参数）
                clean_url = re.sub(r'\.\d+x\d+\.jpg$', '.jpg', img_url)
                clean_url = re.sub(r'@\d+w_\d+h\.[a-z]+$', '', clean_url)
                clean_url = re.sub(r'\?[\w=&%]+$', '', clean_url)
                
                # 确保是 HTTPS
                if clean_url.startswith("http://"):
                    clean_url = clean_url.replace("http://", "https://")
                
                record = {
                    "BV 号": BV_ID,
                    "视频标题": title,
                    "用户名": user,
                    "评论内容": comment_text,
                    "图片 URL": clean_url,
                    "评论时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time)),
                    "回复 ID": str(reply_id)
                }
                img_records.append(record)
                print(f"   🖼️  {clean_url}")

print(f"\n📊 共找到 {len(img_records)} 张评论图片\n")

# 4️⃣ 下载图片
if img_records:
    print("📥 开始下载图片...\n")
    
    for i, record in enumerate(img_records, 1):
        url = record["图片 URL"]
        print(f"[{i}/{len(img_records)}] 下载：{url}")
        
        try:
            img_resp = session.get(url, timeout=15)
            if img_resp.status_code == 200:
                ext = url.split("?")[0].split(".")[-1] or "jpg"
                filename = f"bili_{BV_ID}_{i}.{ext}"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, "wb") as f:
                    f.write(img_resp.content)
                
                size = os.path.getsize(filepath)
                record["本地文件"] = filename
                record["文件大小"] = f"{size / 1024:.1f} KB"
                print(f"   ✅ {filename} ({size / 1024:.1f} KB)")
            else:
                record["本地文件"] = "下载失败"
                record["文件大小"] = "-"
                print(f"   ❌ HTTP {img_resp.status_code}")
        except Exception as e:
            record["本地文件"] = f"错误：{e}"
            record["文件大小"] = "-"
            print(f"   ❌ {e}")
        
        time.sleep(0.5)
        print()

# 5️⃣ 导出 CSV
csv_file = os.path.join(OUTPUT_DIR, f"bili_{BV_ID}_comments.csv")
print(f"📄 导出 CSV: {csv_file}\n")

if img_records:
    fieldnames = ["BV 号", "视频标题", "用户名", "评论内容", "图片 URL", "本地文件", "文件大小", "评论时间", "回复 ID"]
    
    with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(img_records)
    
    print(f"✅ 导出成功！共 {len(img_records)} 条记录")
    
    # 显示预览
    print("\n📋 数据预览:")
    print("-" * 100)
    for i, record in enumerate(img_records[:5], 1):
        print(f"{i}. @{record['用户名']}: {record['评论内容'][:50]}...")
        print(f"   图片：{record['图片 URL']}")
        print(f"   文件：{record.get('本地文件', 'N/A')}")
        print()

# 6️⃣ 导出 JSON
json_file = os.path.join(OUTPUT_DIR, f"bili_{BV_ID}_comments.json")
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(img_records, f, ensure_ascii=False, indent=2)

print(f"✅ JSON 导出：{json_file}")
print(f"\n📁 输出目录：{OUTPUT_DIR}")
print("\n🎉 完成！")
