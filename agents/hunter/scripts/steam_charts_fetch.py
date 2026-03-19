#!/usr/bin/env python3
"""
SteamCharts 数据抓取脚本
提取月度历史数据并计算增长率
"""

import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_steamcharts(app_id):
    """抓取 SteamCharts 数据"""
    url = f"https://steamcharts.com/app/{app_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        return None
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # 提取当前数据
    current_section = soup.find('div', class_='single-stat')
    current_players = None
    peak_24h = None
    peak_all = None
    
    # 提取月度表格数据
    table = soup.find('table', class_='table-table')
    monthly_data = []
    
    if table:
        rows = table.find_all('tr')[1:]  # 跳过表头
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 5:
                month = cells[0].get_text(strip=True)
                avg = cells[1].get_text(strip=True)
                gain = cells[2].get_text(strip=True)
                gain_pct = cells[3].get_text(strip=True)
                peak = cells[4].get_text(strip=True)
                
                # 处理 "Last 30 Days"
                if "Last 30" in month:
                    current_players = avg
                    continue
                
                monthly_data.append({
                    'month': month,
                    'avg': avg,
                    'gain': gain,
                    'gain_pct': gain_pct,
                    'peak': peak
                })
    
    # 提取 24h 峰值和全时间峰值
    stats = soup.find_all('div', class_='single-stat')
    for stat in stats:
        label = stat.find('div', class_='subhead-label')
        if label:
            label_text = label.get_text(strip=True).lower()
            value = stat.find('div', class_='single-stat-value')
            if value:
                if '24-hour' in label_text:
                    peak_24h = value.get_text(strip=True)
                elif 'all-time' in label_text:
                    peak_all = value.get_text(strip=True)
    
    return {
        'app_id': app_id,
        'current': current_players,
        'peak_24h': peak_24h,
        'peak_all': peak_all,
        'monthly': monthly_data[:12]  # 最近 12 个月
    }

def calculate_7day_growth(monthly_data):
    """从月度数据估算 7 天增长率"""
    if len(monthly_data) < 2:
        return None
    
    # 使用最近两个月的数据估算
    last_month = monthly_data[0]
    prev_month = monthly_data[1]
    
    try:
        last_avg = float(last_month['avg'].replace(',', ''))
        prev_avg = float(prev_month['avg'].replace(',', ''))
        
        if prev_avg == 0:
            return None
        
        growth = ((last_avg - prev_avg) / prev_avg) * 100
        return growth
    except:
        return None

def main():
    # 测试：赛博朋克 2077
    app_id = "1091500"
    print(f"抓取 App ID: {app_id}")
    
    data = fetch_steamcharts(app_id)
    
    if data:
        print(f"\n=== {data['app_id']} ===")
        print(f"当前在线 (Last 30 Days 平均): {data['current']}")
        print(f"24 小时峰值：{data['peak_24h']}")
        print(f"历史峰值：{data['peak_all']}")
        
        print("\n最近 6 个月数据:")
        for m in data['monthly'][:6]:
            print(f"  {m['month']}: 平均={m['avg']}, 增长={m['gain']}, 增长率={m['gain_pct']}, 峰值={m['peak']}")
        
        growth = calculate_7day_growth(data['monthly'])
        if growth:
            print(f"\n月度增长率估算：{growth:.2f}%")
    else:
        print("抓取失败")

if __name__ == "__main__":
    main()
