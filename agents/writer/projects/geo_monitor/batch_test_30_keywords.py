#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇游加速器 - 30个关键词GEO批量测试
使用无头浏览器后台运行
"""

import pandas as pd
import json
import os
import re
import time
from datetime import datetime
from typing import List, Dict
import sqlite3

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright未安装，请先运行: pip install playwright")
    print("⚠️  然后运行: playwright install chromium")
    exit(1)

# 30个测试关键词
KEYWORDS = [
    "免费游戏加速器",
    "哪个游戏加速器最好用",
    "游戏加速器免费",
    "pubg加速器推荐",
    "免费加速器steam",
    "哪个游戏加速器好用",
    "steam错误代码-118",
    "永恒之塔2用什么加速器",
    "pubg加速器哪个好用",
    "免费游戏加速器steam",
    "steam用什么加速器好",
    "steam游戏加速器",
    "steam打不开",
    "免费游戏加速器推荐",
    "永恒之塔2加速器推荐",
    "有好用的游戏加速器推荐吗",
    "steam加速器推荐",
    "游戏加速器推荐",
    "游戏加速器",
    "游戏加速器哪个好用",
    "steam进不去",
    "steam加速器免费",
    "游戏加速器评测",
    "打不开steam用啥加速器",
    "免费加速器推荐",
    "绝地求生加速器推荐",
    "steam加速器用哪个好",
    "主机加速器推荐",
    "主机加速器哪个好用",
    "绝地求生用什么加速器"
]

TARGET_BRAND = "奇游加速器"
COMPETITOR_BRANDS = ['迅游', '雷神', 'UU', '网易UU', '暴喵', 'biubiu', '海豚', '玲珑', '赛博', '鲜牛', '斧牛', 'GoLink', '夸克']


def test_keyword_baidu(keyword: str) -> Dict:
    """测试单个关键词在百度AI摘要中的表现"""
    print(f"\n🔍 测试: {keyword}")
    
    result = {
        'keyword': keyword,
        'brand_appeared': False,
        'position': '未出现',
        'competitors': [],
        'ai_summary': '',
        'has_ai_summary': False
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # 搜索
            encoded_keyword = keyword.replace(" ", "%20")
            url = f"https://www.baidu.com/s?wd={encoded_keyword}"
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000)
            
            # 提取页面内容
            content = page.evaluate('''() => {
                // 尝试获取AI摘要
                const aiSection = document.querySelector('[class*="ai-"], [class*="AI-"], .result, #content_left');
                return aiSection ? aiSection.innerText : document.body.innerText;
            }''')
            
            result['ai_summary'] = content[:2000] if content else "未获取到内容"
            
            # 检测是否有AI摘要区域
            result['has_ai_summary'] = page.evaluate('''() => {
                return document.querySelector('[class*="ai-"], [class*="AI-"]') !== null;
            }''')
            
            # 检测奇游品牌
            if '奇游' in content or '奇游加速器' in content:
                result['brand_appeared'] = True
                index = content.find('奇游')
                if index < len(content) * 0.3:
                    result['position'] = '第1位'
                elif index < len(content) * 0.6:
                    result['position'] = '第2位'
                else:
                    result['position'] = '第3位+'
            
            # 检测竞品
            for competitor in COMPETITOR_BRANDS:
                if competitor in content:
                    result['competitors'].append(competitor)
            
            browser.close()
            
            status = "✅" if result['brand_appeared'] else "❌"
            print(f"  {status} 奇游: {result['position']} | 竞品: {', '.join(result['competitors']) or '无'}")
            
        except Exception as e:
            browser.close()
            print(f"  ⚠️  测试失败: {e}")
            result['error'] = str(e)
    
    return result


def main():
    """主函数 - 批量测试30个关键词"""
    print("="*60)
    print("🚀 奇游加速器 - 30个关键词GEO批量测试")
    print("="*60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试关键词数: {len(KEYWORDS)}")
    print("="*60)
    
    results = []
    
    for i, keyword in enumerate(KEYWORDS, 1):
        print(f"\n[{i}/{len(KEYWORDS)}] ", end="")
        result = test_keyword_baidu(keyword)
        results.append(result)
        
        # 间隔2秒，避免请求过快
        if i < len(KEYWORDS):
            time.sleep(2)
    
    # 生成报告
    generate_report(results)
    
    print("\n" + "="*60)
    print("✅ 测试完成!")
    print("="*60)


def generate_report(results: List[Dict]):
    """生成测试报告"""
    
    # 统计
    total = len(results)
    appeared = sum(1 for r in results if r.get('brand_appeared', False))
    not_appeared = total - appeared
    
    # 创建DataFrame
    df_data = []
    for r in results:
        df_data.append({
            '关键词': r['keyword'],
            '奇游出现': '✅' if r.get('brand_appeared', False) else '❌',
            '位置': r.get('position', '未知'),
            '竞品出现': ', '.join(r.get('competitors', [])) or '无',
            'AI摘要': '有' if r.get('has_ai_summary', False) else '无',
            'AI内容摘要': r.get('ai_summary', '')[:100] + '...' if r.get('ai_summary') else ''
        })
    
    df = pd.DataFrame(df_data)
    
    # 保存Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_file = f'奇游GEO测试_30关键词_{timestamp}.xlsx'
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # 详细结果
        df.to_excel(writer, sheet_name='详细结果', index=False)
        
        # 统计摘要
        summary_data = {
            '指标': ['总关键词数', '奇游出现数', '未出现数', '出现率', '测试时间'],
            '数值': [total, appeared, not_appeared, f'{appeared/total*100:.1f}%', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='统计摘要', index=False)
    
    print(f"\n📊 报告已保存: {excel_file}")
    
    # 打印统计
    print("\n" + "="*60)
    print("📈 测试结果统计")
    print("="*60)
    print(f"总关键词数: {total}")
    print(f"奇游出现: {appeared} ({appeared/total*100:.1f}%)")
    print(f"未出现: {not_appeared} ({not_appeared/total*100:.1f}%)")
    print("="*60)
    
    # 列出未出现的关键词
    if not_appeared > 0:
        print("\n🔴 奇游未出现的关键词（需优化）:")
        for r in results:
            if not r.get('brand_appeared', False):
                print(f"  - {r['keyword']}")


if __name__ == "__main__":
    main()
