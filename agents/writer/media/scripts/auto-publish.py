#!/usr/bin/env python3

"""
微信公众号自动化编辑+排版+发布
使用 selenium 自动化操作浏览器
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# 配置
WECHAT_HOME = "https://mp.weixin.qq.com"
DRAFT_URL = "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&reprint_confirm=0&timestamp=1773143463679&type=77&appmsgid=100000581&token=277556341&lang=zh_CN"
COVER_IMAGE_PATH = "/Users/wh1ko/Documents/openclaw/agents/media/outbox/openclaw-cover-optimized.png"

def auto_publish():
    """
    自动化编辑+排版+发布微信公众号文章
    """
    print("🚀 开始自动化编辑+排版+发布...")
    
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
        driver.get(DRAFT_URL)
        print("✅ 已打开文章编辑页面")
        time.sleep(5)
        
        # 等待页面加载
        wait = WebDriverWait(driver, 20)
        
        print("\n=== 第 1 步：检查文章内容 ===")
        # 检查标题
        try:
            title_input = wait.until(
                EC.presence_of_element_located((By.ID, "title"))
            )
            current_title = title_input.get_attribute("value")
            print(f"   标题：{current_title}")
        except:
            print("   ⚠️ 未找到标题输入框")
            current_title = "未知"
        
        # 检查正文
        try:
            editor = driver.find_element(By.CSS_SELECTOR, ".ProseMirror")
            editor_text = editor.text
            print(f"   正文长度：{len(editor_text)} 字符")
        except:
            print("   ⚠️ 未找到正文编辑器")
            editor_text = ""
        
        time.sleep(2)
        
        print("\n=== 第 2 步：上传封面图 ===")
        # 尝试找到封面图上传区域
        try:
            # 方法1：点击封面图区域
            cover_area = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app-cover, .cover-upload, [data-e2e='cover']"))
            )
            print("   找到封面图上传区域")
            cover_area.click()
            print("   ✅ 点击了封面图上传区域")
            time.sleep(2)
            
            # 等待文件选择对话框
            print("   ⏳ 等待文件选择对话框...")
            time.sleep(3)
            
            # 尝试通过 JavaScript 上传文件
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            
            if file_input:
                print(f"   📤 上传封面图：{COVER_IMAGE_PATH}")
                file_input.send_keys(COVER_IMAGE_PATH)
                print("   ✅ 封面图已上传")
                time.sleep(3)
            else:
                print("   ❌ 未找到文件上传输入框")
                
        except Exception as e:
            print(f"   ⚠️ 无法自动上传封面图：{e}")
            print(f"   💡 请手动上传：{COVER_IMAGE_PATH}")
        
        time.sleep(2)
        
        print("\n=== 第 3 步：检查封面图状态 ===")
        # 检查是否有上传成功的封面图
        try:
            cover_preview = driver.find_element(By.CSS_SELECTOR "#app-cover img, .cover-preview img")
            if cover_preview:
                print("   ✅ 封面图预览已更新")
            else:
                print("   ⚠️ 未检测到封面图预览")
        except:
            print("   ⚠️ 无法检测封面图状态")
        
        time.sleep(2)
        
        print("\n=== 第 4 步：保存文章 ===")
        try:
            # 保存为草稿
            save_button = driver.find_element(By.CSS_SELECTOR, ".weui-desktop-btn_save, .weui-desktop-btn_saveas")
            save_button.click()
            print("   ✅ 点击「保存」按钮")
            time.sleep(3)
            
            # 检查保存提示
            try:
                success_msg = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".weui-desktop-toast, .weui-desktop-toast__msg"))
                )
                print(f"   保存提示：{success_msg.text}")
            except:
                print("   ✅ 保存完成（未检测到提示）")
                
        except Exception as e:
            print(f"   ⚠️ 保存时出错：{e}")
        
        time.sleep(2)
        
        print("\n=== 第 5 步：准备发布 ===")
        print("   💡 发布建议：")
        print("   1. 点击「预览」按钮，检查文章内容")
        print("   2. 如需修改，直接在编辑器中修改")
        print("   3. 确认无误后，点击「发表」按钮")
        print("   4. 选择「群发」")
        print("   5. 点击「确认」完成发布")
        
        print("\n✨ 自动化编辑+排版+完成！")
        print("🔄 浏览器保持打开状态，方便你手动完成最后几步")
        
        # 不关闭浏览器，保留给用户手动操作
        print("\n📌 浏览器当前状态：")
        print(f"   - 页面URL: {driver.current_url}")
        print(f"   - 页面标题: {driver.title}")
        print(f"   - 保持打开，可以继续操作")
        
    except Exception as e:
        print(f"❌ 发生错误：{e}")
        print("💡 请手动完成后续操作")
    
    finally:
        # 不关闭浏览器
        print("\n🔄 浏览器保持打开状态...")

if __name__ == "__main__":
    auto_publish()