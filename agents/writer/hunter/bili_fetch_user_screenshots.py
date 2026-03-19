#!/usr/bin/env python3
"""
B 站评论 API 抓取 - 获取用户真实截图
视频：BV15QAUzXEtP
"""

import requests
import json
from pathlib import Path

# 视频 OID (BV15QAUzXEtP)
OID = "116141955481993"

headers = {
    "Referer": "https://www.bilibili.com/video/BV15QAUzXEtP",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}

def fetch_comments(page=1, page_size=20):
    """获取评论"""
    url = "https://api.bilibili.com/x/v2/reply"
    params = {
        "oid": OID,
        "type": 1,  # 视频评论
        "sort": 1,  # 按热度
        "ps": page_size,
        "pn": page,
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        if data.get("code") == 0:
            return data.get("data", {})
        else:
            print(f"❌ API 错误：{data.get('message')}")
            return None
    except Exception as e:
        print(f"⚠️ 请求失败：{e}")
        return None

def is_user_screenshot(url):
    """判断是否是用户截图"""
    if not url:
        return False
    
    # 用户截图路径
    user_paths = ['/bfs/new_dyn/', '/bfs/archive/']
    
    # 排除官方素材
    exclude_paths = [
        '/bfs/activity-plat/',
        '/bfs/sycp/',
        '/bfs/garb/',
        '/bfs/banner/',
        '/bfs/emote/',
        '/bfs/face/',  # 头像
    ]
    
    # 检查排除
    for exclude in exclude_paths:
        if exclude in url:
            return False
    
    # 检查包含
    for include in user_paths:
        if include in url:
            return True
    
    return False

def download_image(url, save_path):
    """下载图片"""
    if url.startswith('//'):
        url = 'https:' + url
    
    # 去除压缩后缀
    url = url.split('@')[0]
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            size = len(response.content)
            if size > 30000:  # 大于 30KB
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ 下载成功：{size/1024:.1f} KB")
                return True
        return False
    except Exception as e:
        print(f"⚠️ 下载失败：{e}")
        return False

if __name__ == "__main__":
    print("🔍 B 站评论抓取 - 用户截图")
    print("=" * 50)
    
    save_dir = Path.home() / ".openclaw/temp/user_screenshots"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取第 1 页评论
    print("\n📥 获取评论...")
    data = fetch_comments(page=1, page_size=20)
    
    if not data:
        print("❌ 获取评论失败")
        exit(1)
    
    replies = data.get("replies", [])
    print(f"✅ 获取到 {len(replies)} 条评论")
    
    # 提取带图评论
    user_images = []
    
    for reply in replies:
        content = reply.get("content", {})
        text = content.get("message", "")
        pictures = content.get("pictures", [])
        
        if pictures:
            user = reply.get("member", {})
            uname = user.get("uname", "未知用户")
            
            for pic in pictures:
                img_url = pic.get("src", "")
                
                if is_user_screenshot(img_url):
                    user_images.append({
                        "user": uname,
                        "text": text[:50] + "..." if len(text) > 50 else text,
                        "url": img_url,
                    })
                    print(f"\n🖼️  发现用户截图：")
                    print(f"   用户：{uname}")
                    print(f"   评论：{text[:60]}...")
                    print(f"   URL: {img_url[:80]}...")
    
    print("\n" + "=" * 50)
    print(f"📊 共找到 {len(user_images)} 张用户截图")
    
    # 下载前 3 张
    if user_images:
        print("\n🚀 开始下载前 3 张...")
        for i, img_info in enumerate(user_images[:3], 1):
            print(f"\n[{i}/3] {img_info['user']}: {img_info['text'][:30]}...")
            
            # 生成文件名
            filename = f"{i}_{img_info['user']}_{i}.jpg"
            save_path = save_dir / filename
            
            if download_image(img_info['url'], save_path):
                print(f"   💾 保存：{save_path}")
            else:
                print(f"   ❌ 下载失败")
    
    print("\n✨ 完成！")
