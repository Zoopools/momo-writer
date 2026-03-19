#!/usr/bin/env python3
import requests
import os
import sys

def download_bili_img(url, filename):
    # 1. 自动补全协议并清理 B 站专有的缩略图后缀
    if url.startswith('//'):
        url = 'https:' + url
    # 去掉 @ 后的后缀（例如 @100w_100h.webp），获取最高清原图
    url = url.split('@')[0]

    # 2. 核心：伪装成 B 站网页发出的请求
    headers = {
        "Referer": "https://www.bilibili.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    try:
        print(f"🚀 正在破防下载：{url}")
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            # 确保保存目录存在
            save_path = os.path.expanduser(f"~/.openclaw/temp/{filename}")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ 下载成功！保存在：{save_path}")
            return save_path
        else:
            print(f"❌ 下载失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ 出错了：{e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python3 bili_fix.py <图片 URL> <文件名>")
        sys.exit(1)
    
    url = sys.argv[1]
    filename = sys.argv[2]
    result = download_bili_img(url, filename)
    if result:
        print(result)
    else:
        sys.exit(1)
