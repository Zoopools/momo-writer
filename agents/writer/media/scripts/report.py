#!/usr/bin/env python3
"""
报告生成脚本 - 小媒
功能：
- 汇总各平台数据
- 生成日报/周报
- 发送给哥哥
"""

import sqlite3
from datetime import datetime, timedelta
import os

# 数据库路径
DB_PATH = os.path.expanduser('~/Documents/openclaw/agents/media/newmedia.db')

def connect_db():
    """连接数据库"""
    conn = sqlite3.connect(DB_PATH)
    return conn

def generate_daily_report():
    """生成日报"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # 获取今日数据
    cursor.execute('''
        SELECT platform, COUNT(*) as content_count,
               SUM(views) as total_views,
               SUM(likes) as total_likes,
               SUM(comments) as total_comments,
               SUM(followers_gained) as total_followers
        FROM analytics
        WHERE date(recorded_at) = date('now')
        GROUP BY platform
    ''')
    
    today_data = cursor.fetchall()
    
    # 获取昨日数据（对比）
    cursor.execute('''
        SELECT platform, SUM(views) as total_views
        FROM analytics
        WHERE date(recorded_at) = date('now', '-1 day')
        GROUP BY platform
    ''')
    
    yesterday_data = cursor.fetchall()
    conn.close()
    
    # 生成报告
    report = []
    report.append("📊 小媒·新媒体日报")
    report.append(f"日期：{datetime.now().strftime('%Y-%m-%d')}")
    report.append("=" * 40)
    report.append("")
    
    report.append("**今日概览**")
    for row in today_data:
        platform, count, views, likes, comments, followers = row
        report.append(f"- {platform}: {count}条内容, {views}播放, +{followers}粉丝")
    
    report.append("")
    report.append("**明日计划**")
    report.append("- 继续监控各平台数据")
    report.append("- 分析爆款内容规律")
    report.append("- 优化内容策略")
    
    return "\n".join(report)

def generate_weekly_report():
    """生成周报"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # 获取本周数据
    cursor.execute('''
        SELECT platform, COUNT(*) as content_count,
               SUM(views) as total_views,
               SUM(likes) as total_likes,
               AVG(views) as avg_views,
               SUM(followers_gained) as total_followers
        FROM analytics
        WHERE date(recorded_at) >= date('now', 'weekday 0', '-7 days')
        GROUP BY platform
    ''')
    
    week_data = cursor.fetchall()
    conn.close()
    
    # 生成报告
    report = []
    report.append("📊 小媒·新媒体周报")
    report.append(f"周期：{datetime.now().strftime('%Y-%m-%d')} 本周")
    report.append("=" * 40)
    report.append("")
    
    report.append("**本周数据**")
    for row in week_data:
        platform, count, views, likes, avg_views, followers = row
        report.append(f"- {platform}: {count}条，总计{views}播放，平均{avg_views:.0f}播放，+{followers}粉丝")
    
    report.append("")
    report.append("**增长亮点**")
    report.append("- 待分析（数据积累后自动生成）")
    
    report.append("")
    report.append("**下周计划**")
    report.append("- 继续优化内容策略")
    report.append("- 测试新的内容形式")
    report.append("- 分析竞品数据")
    
    return "\n".join(report)

def send_to_feishu(report):
    """发送飞书"""
    # TODO: 实现飞书发送
    print("📤 报告已生成（飞书发送功能待实现）")
    print(report)

def main():
    """主函数"""
    print("🚀 小媒报告生成开始")
    
    # 生成日报
    daily_report = generate_daily_report()
    print("\n" + daily_report)
    
    # 生成周报（每周五）
    if datetime.now().weekday() == 4:  # 周五
        weekly_report = generate_weekly_report()
        print("\n" + weekly_report)
    
    print("\n✅ 报告生成完成")

if __name__ == '__main__':
    main()
