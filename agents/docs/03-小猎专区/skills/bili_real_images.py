#!/usr/bin/env python3
"""
B 站评论图片抓取 - 排除表情包版本
只抓取用户自己上传的截图/图片
"""

import requests
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ==================== 配置项 ====================
BILI_COMMENT_URL = "https://www.bilibili.com/video/BV15QAUzXEtP/#reply-area"
TEMP_SAVE_PATH = os.path.expanduser("~/.openclaw/temp/bili_comments/")
BILI_REFERER = "https://www.bilibili.com/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 表情包 URL 特征（排除）
EXCLUDE_KEYWORDS = ['/garb/item/', '/sycp/', '/face/', '/activity-plat/', '/emoji/']
# 用户截图 URL 特征（保留）
INCLUDE_KEYWORDS = ['/bfs/archive/', '/bfs/new_dyn/', '/bfs/album/']

# ==================== 工具函数 ====================

def is_user_image(img_url):
    """判断是否为用户上传的图片（排除表情包）"""
    # 排除表情包
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in img_url:
            return False
    # 保留用户截图
    for keyword in INCLUDE_KEYWORDS:
        if keyword in img_url:
            return True
    # 其他 hdslb 图片也保留
    if 'hdslb.com' in img_url and '/bfs/' in img_url:
        return True
    return False

def init_chrome_driver():
    """初始化 Chrome 浏览器"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--user-agent={USER_AGENT}")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def get_comments_with_images(driver, page_url, scroll_times=15):
    """获取评论及其关联的图片（排除表情包）"""
    print(f"🔍 正在打开页面：{page_url}")
    driver.get(page_url)
    time.sleep(3)
    
    # 深度滚动加载评论
    print(f"📜 深度滚动加载评论 {scroll_times} 次...")
    for i in range(scroll_times):
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(1.5)
    
    # 使用 JavaScript 获取评论和图片
    print("🔍 提取评论数据...")
    js_code = """
    const results = [];
    // 获取所有评论容器
    const commentContainers = document.querySelectorAll('.root-reply-container');
    
    for (let container of commentContainers) {
        // 获取评论者
        const userEl = container.querySelector('.user-name, .root-reply-container .user-name');
        // 获取评论内容
        const contentEl = container.querySelector('.root-reply-container .content, .reply-content');
        // 获取点赞数
        const likeEl = container.querySelector('.like-count');
        // 获取图片（排除表情包）
        const imgEl = container.querySelector('img');
        
        if (userEl && contentEl) {
            const user = userEl.textContent.trim();
            const content = contentEl.textContent.trim().substring(0, 200);
            const likes = likeEl ? parseInt(likeEl.textContent) || 0 : 0;
            let imgUrl = '';
            
            if (imgEl) {
                const src = imgEl.src;
                // 检查是否为用户图片（排除表情包）
                const excludeKeywords = ['/garb/item/', '/sycp/', '/face/', '/activity-plat/'];
                const includeKeywords = ['/bfs/archive/', '/bfs/new_dyn/', '/bfs/album/'];
                
                let isUserImg = false;
                for (let kw of excludeKeywords) {
                    if (src.includes(kw)) {
                        isUserImg = false;
                        break;
                    }
                }
                for (let kw of includeKeywords) {
                    if (src.includes(kw)) {
                        isUserImg = true;
                        break;
                    }
                }
                if (src.includes('hdslb.com') && src.includes('/bfs/') && !src.includes('/face/')) {
                    isUserImg = true;
                }
                
                if (isUserImg) {
                    imgUrl = src.split('@')[0];
                }
            }
            
            if (content.length > 5 && !content.includes('首页') && !content.includes('大会员')) {
                results.push({
                    user: user,
                    content: content,
                    likes: likes,
                    imageUrl: imgUrl
                });
            }
        }
    }
    
    return results;
    """
    
    comments = driver.execute_script(js_code)
    
    # 过滤有效评论
    valid_comments = [c for c in comments if c['imageUrl']]  # 只保留带图片的评论
    
    print(f"✅ 共找到 {len(comments)} 条评论，其中 {len(valid_comments)} 条带用户图片")
    return valid_comments[:10]  # 返回前 10 条带图评论

def download_bili_image(img_url, save_path, referer=BILI_REFERER):
    """下载 B 站图片（带 Referer 绕过 403）"""
    headers = {
        "Referer": referer,
        "User-Agent": USER_AGENT
    }
    
    try:
        print(f"🚀 正在下载：{img_url[:60]}...")
        response = requests.get(img_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 提取文件名
        img_name = img_url.split("/")[-1].split("?")[0]
        if not img_name.endswith(('.jpg', '.png', '.webp', '.gif')):
            img_name = f"{img_name}.jpg"
        
        full_save_path = os.path.join(save_path, img_name)
        
        # 创建目录
        os.makedirs(save_path, exist_ok=True)
        
        # 保存图片
        with open(full_save_path, "wb") as f:
            f.write(response.content)
        
        print(f"✅ 下载成功：{full_save_path}")
        return full_save_path
    
    except Exception as e:
        print(f"❌ 下载失败：{str(e)}")
        return None

# ==================== 主流程 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 B 站评论图片抓取工具（排除表情包版）")
    print("=" * 60)
    
    driver = None
    try:
        # 1. 初始化浏览器
        print("\n📌 步骤 1: 初始化浏览器...")
        driver = init_chrome_driver()
        
        # 2. 获取带图评论
        print("\n📌 步骤 2: 获取评论及图片...")
        comments = get_comments_with_images(driver, BILI_COMMENT_URL, scroll_times=15)
        
        if not comments:
            print("⚠️  未找到带用户图片的评论")
            exit(0)
        
        # 3. 下载图片
        print(f"\n📌 步骤 3: 下载 {len(comments)} 张图片...")
        downloaded_files = []
        
        for i, comment in enumerate(comments):
            print(f"\n[{i+1}/{len(comments)}] {comment['user']}: {comment['content'][:30]}...")
            if comment['imageUrl']:
                save_file = download_bili_image(comment['imageUrl'], TEMP_SAVE_PATH)
                if save_file:
                    downloaded_files.append({
                        "index": i + 1,
                        "user": comment['user'],
                        "content": comment['content'],
                        "likes": comment['likes'],
                        "image_url": comment['imageUrl'],
                        "local_path": save_file,
                        "size": os.path.getsize(save_file)
                    })
        
        # 4. 结果汇总
        print("\n" + "=" * 60)
        print("📊 下载结果汇总")
        print("=" * 60)
        
        for item in downloaded_files:
            size_kb = item["size"] / 1024
            print(f"{item['index']}. {item['user']}: {item['content'][:40]}... ({size_kb:.1f}KB)")
        
        print(f"\n✅ 成功下载 {len(downloaded_files)} 张用户图片")
        print(f"📁 保存位置：{TEMP_SAVE_PATH}")
        
        # 保存结果到 JSON
        result_file = os.path.join(TEMP_SAVE_PATH, "bili_comments_result.json")
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(downloaded_files, f, ensure_ascii=False, indent=2)
        print(f"📄 结果已保存：{result_file}")
        
    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            print("\n🔚 关闭浏览器...")
            driver.quit()
    
    print("\n🎉 完成！")
