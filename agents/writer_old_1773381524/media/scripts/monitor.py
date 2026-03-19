#!/usr/bin/env python3
"""
数据监控脚本 - 小媒
功能：
- 定时抓取各平台数据
- 存入 SQLite 数据库
- 检查异常（播放量过低）
- 发送飞书通知（如有异常）
"""

import sqlite3
import requests
from datetime import datetime
import os

# 数据库路径
DB_PATH = os.path.expanduser('~/Documents/openclaw/agents/media/newmedia.db')

# 飞书 Webhook（从环境变量读取）
FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', '')

def connect_db():
    """连接数据库"""
    conn = sqlite3.connect(DB_PATH)
    return conn

def fetch_platform_data(platform):
    """
    抓取平台数据
    
    TODO: 接入各平台 API
    目前返回模拟数据用于测试
    """
    # 模拟数据（后期替换为真实 API 调用）
    if platform == 'douyin':
        return {
            'views': 1000,
            'likes': 100,
            'comments': 20,
            'shares': 10,
            'followers_gained': 5
        }
    elif platform == 'bilibili':
        return {
            'views': 500,
            'likes': 50,
            'comments': 10,
            'shares': 5,
            'followers_gained': 3
        }
    else:
        return {
            'views': 200,
            'likes': 20,
            'comments': 5,
            'shares': 2,
            'followers_gained': 1
        }

def save_analytics(platform, content_id, data):
    """保存数据到数据库"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO analytics (
            id, platform, content_id, views, likes, comments, 
            shares, followers_gained, recorded_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        f"{platform}_{content_id}_{datetime.now().strftime('%Y%m%d')}",
        platform,
        content_id,
        data['views'],
        data['likes'],
        data['comments'],
        data['shares'],
        data['followers_gained'],
        datetime.now()
    ))
    
    conn.commit()
    conn.close()
    print(f"✓ {platform} 数据已保存")

def check_anomalies():
    """检查数据异常"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # 检查播放量低于平均 50% 的内容
    cursor.execute('''
        SELECT platform, content_id, views 
        FROM analytics 
        WHERE recorded_at >= datetime('now', '-1 day')
        AND views < (
            SELECT AVG(views) * 0.5 
            FROM analytics 
            WHERE platform = analytics.platform
        )
    ''')
    
    anomalies = cursor.fetchall()
    conn.close()
    
    if anomalies:
        send_notification(f"发现 {len(anomalies)} 条内容播放量异常")
        return anomalies
    
    return []

def send_notification(message):
    """发送飞书通知"""
    if not FEISHU_WEBHOOK:
        print("⚠️ 未配置飞书 Webhook")
        return
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": f"📊 小媒数据监控告警\n\n{message}\n\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        }
    }
    
    try:
        response = requests.post(FEISHU_WEBHOOK, json=payload)
        if response.status_code == 200:
            print("✓ 飞书通知已发送")
        else:
            print(f"⚠️ 飞书通知失败：{response.text}")
    except Exception as e:
        print(f"⚠️ 发送通知失败：{e}")

def main():
    """主函数"""
    print("🚀 小媒数据监控开始")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 抓取各平台数据
    platforms = ['douyin', 'bilibili', 'xiaohongshu']
    for platform in platforms:
        print(f"\n📱 抓取 {platform} 数据...")
        data = fetch_platform_data(platform)
        save_analytics(platform, 'test_001', data)
    
    # 检查异常
    print("\n🔍 检查数据异常...")
    anomalies = check_anomalies()
    
    if anomalies:
        print(f"⚠️ 发现 {len(anomalies)} 条异常")
    else:
        print("✓ 无异常")
    
    print("\n✅ 数据监控完成")

if __name__ == '__main__':
    main()
