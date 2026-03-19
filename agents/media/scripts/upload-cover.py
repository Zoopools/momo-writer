#!/usr/bin/env python3

"""
添加封面图到微信公众号草稿文章
使用 selenium 自动化操作浏览器
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置
WECHAT_URL = "https://mp.weixin.qq.com"
ARTICLE_URL = "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&reprint_confirm=0&timestamp=1773143463679&type=77&appmsgid=100000581&token=277556341&lang=zh_CN"
COVER_IMAGE_PATH = "/Users/wh1ko/Documents/openclaw/agents/media/outbox/openclaw-cover.png"

def add_cover_image():
    """
    添加封面图到微信公众号文章
    """
    print("🚀 开始添加封面图...")
    
    # 配置 Chrome
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/Users/wh1ko/Library/Application Support/baoyu-skills/chrome-profile")
    chrome_options.add_argument("--remote-debugging-port=51754")
    
    try:
        # 连接到已存在的 Chrome
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ 已连接到 Chrome")
        
        # 等待页面加载
        driver.get(ARTICLE_URL)
        print(f"✅ 已打开文章编辑页面")
        time.sleep(3)
        
        # 等待封面图上传区域
        wait = WebDriverWait(driver, 10)
        
        try:
            # 尝试找到封面图上传按钮
            cover_upload = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#app-cover, .cover-upload, [data-e2e='cover']"))
            )
            print("✅ 找到封面图上传区域")
            
            # 点击封面图上传区域
            cover_upload.click()
            print("✅ 点击了封面图上传区域")
            time.sleep(2)
            
            # 等待文件选择对话框
            print("⏳ 等待文件选择对话框...")
            time.sleep(2)
            
            # 使用 JavaScript 触发文件选择（因为 selenium 不能直接操作文件选择对话框）
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            
            if file_input:
                # 上传封面图
                print(f"📤 上传封面图: {COVER_IMAGE_PATH}")
                file_input.send_keys(COVER_IMAGE_PATH)
                print("✅ 封面图已上传")
                time.sleep(3)
                
                # 保存文章
                print("💾 保存文章...")
                save_button = driver.find_element(By.CSS_SELECTOR, ".weui-desktop-btn_save")
                save_button.click()
                print("✅ 文章已保存")
                time.sleep(2)
                
                return True
            else:
                print("❌ 未找到文件上传输入框")
                return False
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            print("💡 提示：请在浏览器中手动上传封面图")
            print(f"📁 封面图路径: {COVER_IMAGE_PATH}")
            return False
        
    except Exception as e:
        print(f"❌ 连接 Chrome 失败: {e}")
        print("💡 提示：请手动打开浏览器并上传封面图")
        return False
    finally:
        # 不关闭浏览器，保留供用户查看
        print("🔄 浏览器保持打开状态，方便你手动操作")

if __name__ == "__main__":
    add_cover_image()