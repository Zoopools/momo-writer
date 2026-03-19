#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇游加速器 - 30关键词完整报告生成
整合前10个 + 剩余20个测试结果
"""

import pandas as pd
from datetime import datetime

# 前10个关键词结果
RESULTS_10 = [
    {'keyword': '免费游戏加速器', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '哪个游戏加速器最好用', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': 'steam错误代码-118', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': True, 'competitors': ['迅游', 'UU']},
    {'keyword': 'steam用什么加速器好', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '游戏加速器推荐', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': 'steam加速器推荐', 'qiyou_appeared': True, 'position': '第1位', 'has_ai': True, 'competitors': ['迅游', '雷神', 'UU', 'biubiu', '海豚', '鲜牛']},
    {'keyword': 'pubg加速器推荐', 'qiyou_appeared': True, 'position': '第1位', 'has_ai': True, 'competitors': ['迅游', '雷神', 'UU', 'biubiu', '鲜牛']},
    {'keyword': '免费加速器推荐', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': 'steam进不去', 'qiyou_appeared': True, 'position': '第3位+', 'has_ai': False, 'competitors': ['迅游', 'UU']},
    {'keyword': '游戏加速器哪个好用', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
]

# 剩余20个关键词结果
RESULTS_20 = [
    {'keyword': '游戏加速器免费', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': ['迅游', '雷神', 'UU', 'biubiu', '鲜牛', '斧牛']},
    {'keyword': '免费加速器steam', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': True, 'competitors': ['迅游', '雷神', 'UU', 'biubiu']},
    {'keyword': '永恒之塔2用什么加速器', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': 'pubg加速器哪个好用', 'qiyou_appeared': True, 'position': '第1位', 'has_ai': True, 'competitors': ['迅游', '雷神', 'UU', 'biubiu', '鲜牛']},
    {'keyword': '免费游戏加速器steam', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': 'steam游戏加速器', 'qiyou_appeared': True, 'position': '第2位', 'has_ai': True, 'competitors': ['迅游', '雷神', 'UU', 'biubiu', '斧牛']},
    {'keyword': 'steam打不开', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': True, 'competitors': []},
    {'keyword': '免费游戏加速器推荐', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '永恒之塔2加速器推荐', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '有好用的游戏加速器推荐吗', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '游戏加速器', 'qiyou_appeared': True, 'position': '第1位', 'has_ai': False, 'competitors': ['迅游', '雷神', 'UU', 'biubiu', '鲜牛']},
    {'keyword': 'steam加速器免费', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '游戏加速器评测', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '打不开steam用啥加速器', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '绝地求生加速器推荐', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': 'steam加速器用哪个好', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '主机加速器推荐', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '主机加速器哪个好用', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
    {'keyword': '绝地求生用什么加速器', 'qiyou_appeared': False, 'position': '未出现', 'has_ai': False, 'competitors': []},
]

# 合并所有结果
ALL_RESULTS = RESULTS_10 + RESULTS_20

def generate_report():
    """生成完整报告"""
    print("="*60)
    print("📊 奇游加速器 - 30关键词GEO测试完整报告")
    print("="*60)
    
    # 统计
    total = len(ALL_RESULTS)
    appeared = sum(1 for r in ALL_RESULTS if r['qiyou_appeared'])
    not_appeared = total - appeared
    
    # 分类统计
    position_1 = sum(1 for r in ALL_RESULTS if r['position'] == '第1位')
    position_2 = sum(1 for r in ALL_RESULTS if r['position'] == '第2位')
    position_3 = sum(1 for r in ALL_RESULTS if r['position'] == '第3位+')
    
    # 有AI摘要的词
    has_ai = sum(1 for r in ALL_RESULTS if r['has_ai'])
    
    print(f"\n总关键词数: {total}")
    print(f"奇游出现: {appeared} ({appeared/total*100:.1f}%)")
    print(f"  - 第1位: {position_1}个")
    print(f"  - 第2位: {position_2}个")
    print(f"  - 第3位+: {position_3}个")
    print(f"未出现: {not_appeared} ({not_appeared/total*100:.1f}%)")
    print(f"有AI摘要: {has_ai}个")
    
    # 创建DataFrame
    df = pd.DataFrame([{
        '序号': i+1,
        '关键词': r['keyword'],
        '奇游出现': '✅' if r['qiyou_appeared'] else '❌',
        '位置': r['position'],
        'AI摘要': '有' if r['has_ai'] else '无',
        '竞品出现': ', '.join(r['competitors']) if r['competitors'] else '无',
        '优先级': 'P0' if 'steam' in r['keyword'] or 'pubg' in r['keyword'] else 'P1' if '加速器' in r['keyword'] else 'P2',
        '优化建议': get_optimization_suggestion(r)
    } for i, r in enumerate(ALL_RESULTS)])
    
    # 保存Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'奇游GEO测试_30关键词完整报告_{timestamp}.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 详细结果
        df.to_excel(writer, sheet_name='详细结果', index=False)
        
        # 统计摘要
        summary_data = {
            '指标': [
                '总关键词数', '奇游出现数', '未出现数', '出现率',
                '第1位数量', '第2位数量', '第3位+数量',
                '有AI摘要数', '测试时间'
            ],
            '数值': [
                total, appeared, not_appeared, f'{appeared/total*100:.1f}%',
                position_1, position_2, position_3,
                has_ai, datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='统计摘要', index=False)
        
        # 需优化的关键词
        need_optimize = df[df['奇游出现'] == '❌'][['序号', '关键词', '优先级', '优化建议']]
        need_optimize.to_excel(writer, sheet_name='需优化关键词', index=False)
        
        # 已出现的关键词（优势保持）
        appeared_df = df[df['奇游出现'] == '✅'][['序号', '关键词', '位置', '竞品出现']]
        appeared_df.to_excel(writer, sheet_name='优势关键词', index=False)
    
    print(f"\n📁 报告已保存: {filename}")
    
    # 打印需优化的关键词
    print("\n" + "="*60)
    print("🔴 需优化的关键词 (共{}个)".format(not_appeared))
    print("="*60)
    for _, row in df[df['奇游出现'] == '❌'].iterrows():
        print(f"{row['序号']:2d}. [{row['优先级']}] {row['关键词']}")
    
    # 打印已出现的关键词
    print("\n" + "="*60)
    print("🟢 奇游已出现的关键词 (共{}个)".format(appeared))
    print("="*60)
    for _, row in df[df['奇游出现'] == '✅'].iterrows():
        print(f"{row['序号']:2d}. [{row['位置']}] {row['关键词']}")
    
    return filename


def get_optimization_suggestion(r):
    """生成优化建议"""
    if r['qiyou_appeared']:
        if r['position'] == '第1位':
            return '保持优势，继续维护'
        elif r['position'] == '第2位':
            return '优化内容，争取第1位'
        else:
            return '提升排名，进入前2位'
    else:
        if '免费' in r['keyword']:
            return '重点布局：强调免费试用/免费功能'
        elif '推荐' in r['keyword'] or '哪个' in r['keyword']:
            return '重点布局：发布评测对比内容'
        elif 'steam' in r['keyword']:
            return '高优先级：Steam相关内容优化'
        elif 'pubg' in r['keyword'] or '绝地求生' in r['keyword']:
            return '高优先级：PUBG相关内容优化'
        elif '永恒之塔' in r['keyword']:
            return '中优先级：特定游戏内容布局'
        elif '主机' in r['keyword']:
            return '中优先级：主机游戏内容布局'
        else:
            return '常规优化：增加相关内容覆盖'


if __name__ == "__main__":
    filename = generate_report()
    print("\n✅ 报告生成完成!")
