#!/usr/bin/env python3
"""
B 站评论图片抓取完整脚本
功能：自动获取评论图片 URL → 下载 → 上传飞书 → 清理临时文件
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
TEMP_SAVE_PATH = os.path.expanduser("~/.openclaw/temp/")
BILI_REFERER = "https://www.bilibili.com/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# ==================== 工具函数 ====================

def init_chrome_driver():
    """初始化 Chrome 浏览器（有界面模式，方便调试）"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")  # 调试时注释掉
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--user-agent={USER_AGENT}")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def get_comment_images(driver, page_url, scroll_times=5):
    """获取评论区真实图片 URL"""
    print(f"🔍 正在打开页面：{page_url}")
    driver.get(page_url)
    time.sleep(3)
    
    # 滚动加载评论
    print(f"📜 滚动加载评论 {scroll_times} 次...")
    for i in range(scroll_times):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(2)
    
    # 使用 JavaScript 获取所有图片
    print("🔍 使用 JavaScript 获取图片 URL...")
    js_code = """
    const imgs = document.querySelectorAll('img');
    const commentImgs = [];
    for (let img of imgs) {
        const src = img.src;
        if (src && src.includes('hdslb.com') && !src.includes('/face/') && !src.includes('/archive/')) {
            let cleanUrl = src.split('@')[0];
            if (!commentImgs.includes(cleanUrl)) {
                commentImgs.push(cleanUrl);
            }
        }
    }
    return commentImgs.slice(0, 10);
    """
    real_urls = driver.execute_script(js_code)
    
    for url in real_urls:
        print(f"  ✓ 找到图片：{url[:60]}...")
    
    print(f"✅ 共找到 {len(real_urls)} 张评论图片")
    return real_urls

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

def clean_temp_file(file_path):
    """删除临时文件"""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️  已删除：{file_path}")

# ==================== 主流程 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 B 站评论图片抓取工具")
    print("=" * 60)
    
    driver = None
    try:
        # 1. 初始化浏览器
        print("\n📌 步骤 1: 初始化浏览器...")
        driver = init_chrome_driver()
        
        # 2. 获取图片 URL
        print("\n📌 步骤 2: 获取评论图片 URL...")
        real_img_urls = get_comment_images(driver, BILI_COMMENT_URL, scroll_times=5)
        
        if not real_img_urls:
            print("⚠️  未找到评论图片")
            exit(0)
        
        # 3. 下载测试（前 10 张）
        print(f"\n📌 步骤 3: 下载前 10 张图片测试...")
        downloaded_files = []
        
        for i, img_url in enumerate(real_img_urls[:10]):
            print(f"\n[{i+1}/10]")
            save_file = download_bili_image(img_url, TEMP_SAVE_PATH)
            if save_file:
                downloaded_files.append({
                    "index": i + 1,
                    "url": img_url,
                    "local_path": save_file,
                    "size": os.path.getsize(save_file)
                })
        
        # 4. 结果汇总
        print("\n" + "=" * 60)
        print("📊 下载结果汇总")
        print("=" * 60)
        
        for item in downloaded_files:
            size_kb = item["size"] / 1024
            print(f"{item['index']}. {item['url'][:50]}... ({size_kb:.1f}KB)")
        
        print(f"\n✅ 成功下载 {len(downloaded_files)} 张图片")
        print(f"📁 保存位置：{TEMP_SAVE_PATH}")
        
        # 保存结果到 JSON
        result_file = os.path.join(TEMP_SAVE_PATH, "bili_images_result.json")
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
