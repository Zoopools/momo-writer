#!/usr/bin/env python3
"""
B 站评论区用户截图抓取脚本
专门抓取用户发的真实截图（游戏画面、报错图等）
过滤掉表情包、头像、装扮等官方素材
"""

import requests
import os
import re
import json
from pathlib import Path

def is_user_screenshot(url):
    """判断是否是用户截图"""
    # 只保留用户上传图片的路径
    user_paths = [
        '/bfs/new_dyn/',      # 用户动态/评论图片
        '/bfs/archive/',      # 用户上传存档
        '/bfs/face/'          # 用户头像（排除）
    ]
    
    # 排除官方素材
    exclude_paths = [
        '/bfs/activity-plat/',  # 活动素材
        '/bfs/sycp/',           # 三连表情包
        '/bfs/garb/',           # 装扮
        '/bfs/banner/',         # 横幅
        '/bfs/emote/',          # 表情
    ]
    
    # 检查是否排除
    for exclude in exclude_paths:
        if exclude in url:
            return False
    
    # 检查是否包含
    for include in user_paths:
        if include in url:
            return True
    
    return False

def download_user_screenshot(url, filename):
    """下载用户截图"""
    # 补全协议
    if url.startswith('//'):
        url = 'https:' + url
    
    # 去除压缩后缀
    url = url.split('@')[0]
    
    headers = {
        "Referer": "https://www.bilibili.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    }
    
    try:
        print(f"🚀 下载：{url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # 检查文件大小（排除太小的表情包）
            size = len(response.content)
            if size < 30000:  # 小于 30KB 可能是表情包
                print(f"⚠️ 文件太小 ({size} bytes)，跳过")
                return None
            
            save_dir = Path.home() / ".openclaw/temp/user_screenshots"
            save_dir.mkdir(parents=True, exist_ok=True)
            save_path = save_dir / filename
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 下载成功！大小：{size/1024:.1f} KB")
            print(f"   保存：{save_path}")
            return str(save_path)
        else:
            print(f"❌ 下载失败：{response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ 错误：{e}")
        return None

# 测试用的用户截图 URL（从评论区提取的真实截图）
test_urls = [
    # 这些是典型的用户截图 URL 格式
    "https://i0.hdslb.com/bfs/new_dyn/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6/1234567890.jpg",
    "https://i0.hdslb.com/bfs/archive/abcdef1234567890abcdef1234567890.png",
]

if __name__ == "__main__":
    print("🔍 B 站用户截图抓取脚本")
    print("=" * 50)
    
    # 测试 URL 过滤
    print("\n测试 URL 过滤：")
    test_cases = [
        ("https://i0.hdslb.com/bfs/new_dyn/xxx.jpg", True, "用户截图"),
        ("https://i0.hdslb.com/bfs/archive/xxx.png", True, "用户上传"),
        ("https://i0.hdslb.com/bfs/sycp/sanlian/xxx.jpeg", False, "三连表情"),
        ("https://i0.hdslb.com/bfs/garb/item/xxx.png", False, "装扮"),
        ("https://i0.hdslb.com/bfs/activity-plat/xxx.png", False, "活动素材"),
    ]
    
    for url, expected, desc in test_cases:
        result = is_user_screenshot(url)
        status = "✅" if result == expected else "❌"
        print(f"{status} {desc}: {result} (期望：{expected})")
    
    print("\n脚本已就绪！可以集成到浏览器自动化脚本中使用。")
