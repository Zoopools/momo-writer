#!/usr/bin/env python3
"""
测试飞书 Webhook 连接
"""
import os
import requests
import json

FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

def test_webhook():
    """测试飞书 Webhook"""
    if not FEISHU_WEBHOOK or 'xxxxxxxxxxxxxxxx' in FEISHU_WEBHOOK:
        print("⚠️ 飞书 Webhook 未配置")
        print("请在 .env.local 中配置 FEISHU_WEBHOOK")
        print("格式：FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_URL")
        return False
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": "✅ 小媒飞书 Webhook 测试成功！\n\n时间：2026-03-09 23:20\n\n飞书通知系统已就绪！"
        }
    }
    
    try:
        response = requests.post(FEISHU_WEBHOOK, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ 飞书 Webhook 连接成功！")
            return True
        else:
            print(f"⚠️ 飞书 Webhook 连接失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ 连接异常：{e}")
        return False

if __name__ == '__main__':
    print("🧪 测试飞书 Webhook 连接...")
    test_webhook()