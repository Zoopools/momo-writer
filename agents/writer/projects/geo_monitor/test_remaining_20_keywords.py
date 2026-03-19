#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇游加速器 - 剩余20个关键词测试
"""

import pandas as pd
import time
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright未安装")
    exit(1)

# 剩余20个关键词（排除已测试的10个）
KEYWORDS = [
    "游戏加速器免费",
    "免费加速器steam",
    "永恒之塔2用什么加速器",
    "pubg加速器哪个好用",
    "免费游戏加速器steam",
    "steam游戏加速器",
    "steam打不开",
    "免费游戏加速器推荐",
    "永恒之塔2加速器推荐",
    "有好用的游戏加速器推荐吗",
    "游戏加速器",
    "steam加速器免费",
    "游戏加速器评测",
    "打不开steam用啥加速器",
    "绝地求生加速器推荐",
    "steam加速器用哪个好",
    "主机加速器推荐",
    "主机加速器哪个好用",
    "绝地求生用什么加速器"
]

TARGET_BRAND = "奇游"
COMPETITORS = ['迅游', '雷神', 'UU', '暴喵', 'biubiu', '海豚', '玲珑', '鲜牛', '斧牛']


def test_baidu(keyword):
    """测试单个关键词"""
    idx = KEYWORDS.index(keyword) + 1
    print(f"\n🔍 [{idx}/20] {keyword}")
    
    result = {
        'keyword': keyword,
        'qiyou_appeared': False,
        'position': '未出现',
        'competitors': [],
        'has_ai': False
    }
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            url = f"https://www.baidu.com/s?wd={keyword.replace(' ', '%20')}"
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000)
            
            # 获取内容
            content = page.evaluate('''() => {
                const el = document.querySelector('[class*="ai-"], .result, #content_left');
                return el ? el.innerText : document.body.innerText.substring(0, 3000);
            }''')
            
            # 检测AI摘要
            result['has_ai'] = page.evaluate('''() => {
                return document.querySelector('[class*="ai-"]') !== null;
            }''')
            
            # 检测奇游
            if TARGET_BRAND in content:
                result['qiyou_appeared'] = True
                idx = content.find(TARGET_BRAND)
                if idx < len(content) * 0.3:
                    result['position'] = '第1位'
                elif idx < len(content) * 0.6:
                    result['position'] = '第2位'
                else:
                    result['position'] = '第3位+'
            
            # 检测竞品
            for c in COMPETITORS:
                if c in content and c not in result['competitors']:
                    result['competitors'].append(c)
            
            browser.close()
            
    except Exception as e:
        print(f"  ⚠️ 错误: {e}")
        result['error'] = str(e)
    
    # 打印结果
    status = "✅" if result['qiyou_appeared'] else "❌"
    comps = ', '.join(result['competitors']) if result['competitors'] else '无'
    print(f"  {status} 奇游: {result['position']} | AI摘要: {'有' if result['has_ai'] else '无'} | 竞品: {comps}")
    
    return result


def main():
    print("="*60)
    print("🚀 奇游加速器 - 剩余20个关键词测试")
    print("="*60)
    print(f"开始: {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    results = []
    for kw in KEYWORDS:
        r = test_baidu(kw)
        results.append(r)
        time.sleep(2)
    
    # 统计
    appeared = sum(1 for r in results if r['qiyou_appeared'])
    
    print("\n" + "="*60)
    print("📊 测试结果")
    print("="*60)
    print(f"总关键词: {len(KEYWORDS)}")
    print(f"奇游出现: {appeared} ({appeared/len(KEYWORDS)*100:.0f}%)")
    print(f"未出现: {len(KEYWORDS)-appeared}")
    
    # 出现的关键词
    if appeared > 0:
        print("\n🟢 奇游出现的关键词:")
        for r in results:
            if r['qiyou_appeared']:
                print(f"  ✅ {r['keyword']} - {r['position']}")
    
    # 未出现的关键词
    print("\n🔴 需优化的关键词:")
    for r in results:
        if not r['qiyou_appeared']:
            print(f"  - {r['keyword']}")
    
    # 保存报告
    df = pd.DataFrame([{
        '关键词': r['keyword'],
        '奇游出现': '✅' if r['qiyou_appeared'] else '❌',
        '位置': r['position'],
        'AI摘要': '有' if r['has_ai'] else '无',
        '竞品': ', '.join(r['competitors']) if r['competitors'] else '无'
    } for r in results])
    
    filename = f'奇游测试_剩余20关键词_{datetime.now().strftime("%H%M%S")}.xlsx'
    df.to_excel(filename, index=False)
    print(f"\n📁 报告保存: {filename}")
    
    return results


if __name__ == "__main__":
    main()
