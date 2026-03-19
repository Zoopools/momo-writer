#!/usr/bin/env python3
"""
B 站评论 API 抓取工具
使用 API 直接获取评论数据（包括图片）
"""

import requests
import json
import os

# B 站 Cookie（哥哥之前提供的）
COOKIES = {
    "buvid3": "3A941B3A-4C3F-ED97-F142-0E32A26BFE7D16746infoc",
    "b_nut": "1772635016",
    "DedeUserID": "306850784",
    "bili_jct": "457dbd4b2d1beff302759c6fe699aac5",
    "sid": "7tbm8dr6",
}

HEADERS = {
    "Referer": "https://www.bilibili.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# 视频 BV 号转 AV 号
BV_ID = "BV15QAUzXEtP"

def bv2av(bv_id):
    """BV 号转 AV 号（简化版）"""
    # 调用 API 获取视频信息
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
    resp = requests.get(url, headers=HEADERS, cookies=COOKIES)
    data = resp.json()
    if data.get('code') == 0:
        return data['data']['aid']
    return None

def get_comments(aid, pn=1, ps=20):
    """获取评论"""
    url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={pn}&oid={aid}&type=1&sort=2&ps={ps}"
    resp = requests.get(url, headers=HEADERS, cookies=COOKIES)
    data = resp.json()
    
    if data.get('code') == 0:
        replies = data['data'].get('replies')
        if not replies:
            return []
        comments = []
        
        for reply in replies:
            member = reply.get('member', {})
            content = reply.get('content', {})
            
            comment = {
                'user': member.get('uname', ''),
                'content': content.get('message', ''),
                'likes': reply.get('like', 0),
                'ctime': reply.get('ctime', 0),
                'pictures': content.get('pictures', []),  # 图片列表
            }
            
            # 过滤有图片的评论
            if comment['pictures']:
                # 排除表情包（检查图片类型）
                real_pictures = [
                    pic for pic in comment['pictures'] 
                    if not any(kw in pic.get('img_src', '') for kw in ['/garb/', '/face/', '/activity-plat/'])
                ]
                if real_pictures:
                    comment['real_pictures'] = real_pictures
                    comments.append(comment)
        
        return comments
    else:
        print(f"API 错误：{data.get('message', 'Unknown error')}")
        return []

def download_image(img_url, save_path):
    """下载图片"""
    headers = {
        "Referer": "https://www.bilibili.com/",
        "User-Agent": HEADERS['User-Agent'],
    }
    
    try:
        resp = requests.get(img_url, headers=headers, timeout=15)
        if resp.status_code == 200:
            os.makedirs(save_path, exist_ok=True)
            img_name = img_url.split('/')[-1].split('?')[0]
            file_path = os.path.join(save_path, img_name)
            
            with open(file_path, 'wb') as f:
                f.write(resp.content)
            
            return file_path
    except Exception as e:
        print(f"下载失败：{e}")
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 B 站评论 API 抓取工具")
    print("=" * 60)
    
    # 1. BV 转 AV
    print(f"\n📌 步骤 1: 转换 BV 号 {BV_ID}...")
    aid = bv2av(BV_ID)
    if not aid:
        print("❌ 无法获取 AV 号")
        exit(1)
    print(f"✅ AV 号：{aid}")
    
    # 2. 获取评论（分页获取）
    print(f"\n📌 步骤 2: 获取评论...")
    all_comments = []
    for pn in range(1, 4):  # 获取前 3 页
        comments = get_comments(aid, pn=pn, ps=20)
        all_comments.extend(comments)
        if comments:
            print(f"   第{pn}页：{len(comments)}条带图评论")
    print(f"✅ 找到 {len(all_comments)} 条带图片的评论")
    
    if not all_comments:
        print("\n⚠️  该视频评论区没有用户上传图片（只有表情包或纯文本）")
        print("\n💡 建议：")
        print("   1. 检查视频评论区是否真的有用户截图")
        print("   2. 尝试其他可能有用户截图的视频")
        exit(0)
    
    # 3. 下载图片
    print(f"\n📌 步骤 3: 下载图片...")
    save_path = os.path.expanduser("~/.openclaw/temp/bili_api_comments/")
    os.makedirs(save_path, exist_ok=True)
    
    for i, comment in enumerate(comments[:10]):
        print(f"\n[{i+1}/{len(comments)}] {comment['user']}: {comment['content'][:50]}...")
        
        for pic in comment.get('real_pictures', []):
            img_url = pic.get('img_src', '')
            print(f"   🖼️  {img_url[:60]}...")
            downloaded = download_image(img_url, save_path)
            if downloaded:
                print(f"   ✅ {downloaded}")
    
    # 4. 保存结果
    result_file = os.path.join(save_path, "bili_api_result.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(comments[:10], f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"✅ 完成！结果保存在：{result_file}")
    print(f"📁 图片保存位置：{save_path}")
