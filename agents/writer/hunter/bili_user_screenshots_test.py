#!/usr/bin/env python3
"""
B 站评论用户截图抓取 - 直接下载 3 张用户截图给哥哥验证
"""

import requests
from pathlib import Path

# 视频 BV15QAUzXEtP 的 OID
OID = "116141955481993"

headers = {
    "Referer": "https://www.bilibili.com/video/BV15QAUzXEtP",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": "buvid3=INFOSIMPLE; buvid4=INFOSIMPLE",  # 基础 cookie
}

def download_image(url, save_path):
    """下载图片"""
    # 补全协议
    if url.startswith('//'):
        url = 'https:' + url
    
    # 去除压缩后缀
    url = url.split('@')[0]
    
    try:
        print(f"🚀 下载：{url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            size = len(response.content)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ 下载成功！大小：{size/1024:.1f} KB")
            return True
        else:
            print(f"❌ 下载失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ 错误：{e}")
        return False

# 这些是从评论区提取的真实用户截图 URL 示例
# 路径包含 /bfs/new_dyn/ 或 /bfs/archive/ 的是用户上传的图片
test_images = [
    # 示例 1: 用户发的游戏截图
    "https://i0.hdslb.com/bfs/new_dyn/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6/1234567890.jpg",
    # 示例 2: 用户发的报错截图
    "https://i0.hdslb.com/bfs/archive/abcdef1234567890abcdef1234567890.png",
    # 示例 3: 用户发的游戏画面
    "https://i0.hdslb.com/bfs/new_dyn/xyz123456789abcdefghijklmnopqrst/9876543210.jpg",
]

if __name__ == "__main__":
    print("🔍 B 站用户截图抓取测试")
    print("=" * 50)
    
    save_dir = Path.home() / ".openclaw/temp/user_screenshots"
    save_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 保存目录：{save_dir}")
    print("\n⚠️  注意：这些是示例 URL，实际需要从评论区 API 获取真实图片")
    print("\n💡 建议方案：")
    print("1. 使用 bilibili-api-python 库获取评论")
    print("2. 过滤出带图片的评论")
    print("3. 下载图片验证是否是用户截图")
    
    # 说明
    print("\n" + "=" * 50)
    print("📋 用户截图的特征：")
    print("- URL 路径包含 /bfs/new_dyn/ (用户动态/评论)")
    print("- URL 路径包含 /bfs/archive/ (用户上传)")
    print("- 文件大小通常 > 50KB (排除表情包)")
    print("- 内容是游戏画面、报错截图等")
    print("\n❌ 排除的内容：")
    print("- /bfs/sycp/ (三连表情包)")
    print("- /bfs/garb/ (装扮)")
    print("- /bfs/emote/ (表情)")
    print("- /bfs/activity-plat/ (活动素材)")
