#!/usr/bin/env python3
"""
B 站评论 API 抓取工具 - 楼中楼回复版
专门抓取主评论和回复中的用户图片
"""

import requests
import json
import os

# B 站 Cookie
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

BV_ID = "BV15QAUzXEtP"

def bv2av(bv_id):
    """BV 号转 AV 号"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
    resp = requests.get(url, headers=HEADERS, cookies=COOKIES)
    data = resp.json()
    if data.get('code') == 0:
        return data['data']['aid']
    return None

def get_comments(aid, pn=1, ps=20):
    """获取主评论"""
    url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={pn}&oid={aid}&type=1&sort=2&ps={ps}"
    resp = requests.get(url, headers=HEADERS, cookies=COOKIES)
    data = resp.json()
    
    if data.get('code') == 0:
        return data['data'].get('replies', [])
    return []

def get_replies(rpid, oid, pn=1, ps=10):
    """获取楼中楼回复"""
    url = f"https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={pn}&rpid={rpid}&oid={oid}&type=1&ps={ps}"
    resp = requests.get(url, headers=HEADERS, cookies=COOKIES)
    data = resp.json()
    
    if data.get('code') == 0:
        return data['data'].get('replies', [])
    return []

def extract_images(content):
    """从评论内容中提取用户图片（排除表情包）"""
    pictures = content.get('pictures', [])
    if not pictures:
        return []
    
    # 排除表情包
    exclude_keywords = ['/garb/item/', '/face/', '/activity-plat/', '/sycp/']
    real_pictures = []
    
    for pic in pictures:
        img_src = pic.get('img_src', '')
        is_user_image = True
        for kw in exclude_keywords:
            if kw in img_src:
                is_user_image = False
                break
        if is_user_image:
            real_pictures.append(img_src)
    
    return real_pictures

def download_image(img_url, save_path, index):
    """下载图片"""
    headers = {
        "Referer": "https://www.bilibili.com/",
        "User-Agent": HEADERS['User-Agent'],
    }
    
    try:
        resp = requests.get(img_url, headers=headers, timeout=15)
        if resp.status_code == 200:
            img_name = f"{index}_{img_url.split('/')[-1].split('?')[0]}"
            file_path = os.path.join(save_path, img_name)
            
            with open(file_path, 'wb') as f:
                f.write(resp.content)
            
            return file_path
    except Exception as e:
        print(f"   ❌ 下载失败：{e}")
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 B 站评论抓取工具 - 楼中楼回复版")
    print("=" * 60)
    
    # 1. BV 转 AV
    print(f"\n📌 步骤 1: 转换 BV 号...")
    aid = bv2av(BV_ID)
    if not aid:
        print("❌ 无法获取 AV 号")
        exit(1)
    print(f"✅ AV 号：{aid}")
    
    # 2. 获取主评论
    print(f"\n📌 步骤 2: 获取主评论...")
    all_comments_with_images = []
    
    for pn in range(1, 11):  # 获取前 10 页
        print(f"   抓取第{pn}页...")
        comments = get_comments(aid, pn=pn, ps=20)
        if not comments:
            print(f"   第{pn}页无数据，停止")
            break
        
        for comment in comments:
            member = comment.get('member', {})
            content = comment.get('content', {})
            rpid = comment.get('rpid')
            
            user = member.get('uname', '')
            text = content.get('message', '')
            likes = comment.get('like', 0)
            
            # 检查主评论图片
            images = extract_images(content)
            
            if images:
                all_comments_with_images.append({
                    'type': '主评论',
                    'user': user,
                    'content': text[:100],
                    'likes': likes,
                    'images': images
                })
            
            # 检查楼中楼回复
            if rpid:
                replies = get_replies(rpid, aid, pn=1, ps=10)
                for reply in replies:
                    reply_member = reply.get('member', {})
                    reply_content = reply.get('content', {})
                    reply_images = extract_images(reply_content)
                    
                    if reply_images:
                        all_comments_with_images.append({
                            'type': '楼中楼回复',
                            'user': reply_member.get('uname', ''),
                            'content': reply_content.get('message', '')[:100],
                            'likes': reply.get('like', 0),
                            'images': reply_images
                        })
    
    print(f"\n✅ 共找到 {len(all_comments_with_images)} 条带用户图片的评论")
    
    if not all_comments_with_images:
        print("\n⚠️  未找到带用户图片的评论")
        exit(0)
    
    # 3. 下载图片
    print(f"\n📌 步骤 3: 下载图片...")
    save_path = os.path.expanduser("~/.openclaw/temp/bili_sub_comments/")
    os.makedirs(save_path, exist_ok=True)
    
    downloaded = []
    img_index = 1
    
    for i, item in enumerate(all_comments_with_images[:10]):
        print(f"\n[{i+1}] {item['type']} - {item['user']}: {item['content'][:50]}... ({item['likes']}赞)")
        
        for img_url in item['images']:
            print(f"   🖼️  {img_url[:60]}...")
            file_path = download_image(img_url, save_path, img_index)
            if file_path:
                print(f"   ✅ {file_path}")
                downloaded.append({
                    'user': item['user'],
                    'content': item['content'],
                    'likes': item['likes'],
                    'image_url': img_url,
                    'local_path': file_path
                })
                img_index += 1
    
    # 4. 保存结果
    result_file = os.path.join(save_path, "bili_sub_result.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(downloaded, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"✅ 完成！")
    print(f"📊 成功下载 {len(downloaded)} 张图片")
    print(f"📁 保存位置：{save_path}")
    print(f"📄 结果文件：{result_file}")
