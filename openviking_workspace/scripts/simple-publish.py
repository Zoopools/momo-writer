#!/usr/bin/env python3

"""
微信公众号简单发布脚本
上传封面图并保存草稿
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置
WECHAT_URL = "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&reprint_confirm=0&timestamp=1773143463679&type=77&appmsg=100000581&token=277556341&lang=zh_CN"
COVER_IMAGE_PATH = "/Users/wh1ko/Documents/openclaw/agents/media/outbox/openclaw-cover-optimized.png"

print("🚀 开始自动化上传封面图...")

# 配置 Chrome
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=/Users/wh1ko/Library/Application Support/baoyu-skills/chrome-profile")
chrome_options.add_argument("--remote-debugging-port=51754")
chrome_options.add_argument("--no-first-run")

try:
    # 连接到已存在的 Chrome
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ 已连接到 Chrome")
    
    # 打开文章编辑页面
    print(f"📝 打开文章编辑页面...")
    driver.get(WECHAT_URL)
    print("✅ 已打开文章编辑页面")
    time.sleep(5)
    
    # 等待页面加载
    wait = WebDriverWait(driver, 20)
    
    # 上传封面图
    print("\n📤 上传封面图...")
    print(f"   文件路径：{COVER_IMAGE_PATH}")
    
    try:
        # 方法1：查找并点击封面图上传区域
        cover_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#app-cover"))
        )
        cover_button.click()
        print("   ✅ 点击了封面图区域")
        time.sleep(2)
        
        # 找到文件输入框
        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        
        # 上传文件
        file_input.send_keys(COVER_IMAGE_PATH)
        print("   ✅ 封面图已上传")
        time.sleep(3)
        
    except Exception as e:
        print(f"   ⚠️ 自动上传失败：{e}")
        print(f"   💡 请手动上传：{COVER_IMAGE_PATH}")
    
    # 保存文章
    print("\n💾 保存文章...")
    try:
        save_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".weui-desktop-btn_save"))
        )
        save_button.click()
        print("   ✅ 已点击「保存」按钮")
        time.sleep(3)
        print("   ✅ 文章已保存")
    except Exception as e:
        print(f"   ⚠️ 保存失败：{e}")
    
    print("\n📋 下一步操作：")
    print("   1. 在编辑器中手动添加封面图文字（确保清晰可读）")
    print("   2. 预览文章")
    print("   3. 发布文章")
    
    print("\n🔄 浏览器保持打开状态，方便你继续操作...")
    
except Exception as e:
    print(f"❌ 发生错误：{e}")
    print("💡 请手动完成后续操作")

print("\n✨ 完成！")