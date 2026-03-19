#!/usr/bin/env python3
"""
B 站评论抓取 - 使用浏览器 Cookie
"""

import requests
import json
from pathlib import Path

# 视频 OID
OID = "116141955481993"

# 从浏览器复制的 Cookie (需要哥哥帮忙从浏览器复制)
# 打开 https://www.bilibili.com/video/BV15QAUzXEtP
# 按 F12 → Network → 刷新 → 点击任意请求 → 复制 Cookie
COOKIE = ""

def fetch_comments_with_cookie(page=1, page_size=20):
    """使用 Cookie 获取评论"""
    url = "https://api.bilibili.com/x/v2/reply"
    params = {
        "oid": OID,
        "type": 1,
        "sort": 1,
        "ps": page_size,
        "pn": page,
    }
    
    headers = {
        "Referer": "https://www.bilibili.com/video/BV15QAUzXEtP",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    }
    
    if COOKIE:
        headers["Cookie"] = COOKIE
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        print(f"API 返回：code={data.get('code')}, message={data.get('message')}")
        
        if data.get("code") == 0:
            return data.get("data", {})
        else:
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None

if __name__ == "__main__":
    print("🔍 B 站评论 API 测试")
    print("=" * 50)
    
    if not COOKIE:
        print("\n⚠️  需要 Cookie！")
        print("\n📋 获取 Cookie 步骤：")
        print("1. 用浏览器打开：https://www.bilibili.com/video/BV15QAUzXEtP")
        print("2. 按 F12 打开开发者工具")
        print("3. 切换到 Network (网络) 标签")
        print("4. 刷新页面")
        print("5. 点击任意 api.bilibili.com 的请求")
        print("6. 在 Request Headers 里找到 Cookie")
        print("7. 复制整个 Cookie 值")
        print("8. 粘贴到脚本顶部的 COOKIE = \"\" 中")
        print("\n💡 或者哥哥告诉我，我用浏览器自动化来抓取！")
    else:
        print("\n📥 使用 Cookie 获取评论...")
        data = fetch_comments_with_cookie()
        
        if data:
            replies = data.get("replies", [])
            print(f"✅ 获取到 {len(replies)} 条评论")
            
            for reply in replies:
                content = reply.get("content", {})
                pictures = content.get("pictures", [])
                if pictures:
                    print(f"\n🖼️  带图评论：")
                    for pic in pictures:
                        print(f"   URL: {pic.get('src')}")
