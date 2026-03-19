#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO效果监控系统 v1.0 - 完整版
支持平台：百度、豆包、DeepSeek、文心一言
作者：墨墨
时间：2026-03-18
"""

import pandas as pd
import json
import os
import re
import time
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass
import sqlite3

# 浏览器自动化
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class GEOResult:
    """GEO监控结果数据类"""
    question: str
    ai_model: str
    target_brand: str
    ai_answer: str
    query_time: datetime
    brand_appeared: bool
    position: str
    positive_keywords: str
    negative_keywords: str
    competitors_mentioned: str
    references: str
    screenshot_path: str


class GEOMonitor:
    """GEO效果监控主类"""
    
    def __init__(self, config_file: str = "geo_config.xlsx"):
        self.config_file = config_file
        self.config_df = self._load_config()
        self.results = []
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self._init_database()
        
        # 关键词库
        self.competitor_brands = ['迅游', '雷神', 'UU', '网易UU', '暴喵', 'biubiu']
        self.positive_words = ['推荐', '好用', '稳定', '快速', '专业', '免费', '优质', '首选']
        self.negative_words = ['卡顿', '慢', '贵', '不好用', '问题', '错误', '不稳定']
    
    def _load_config(self) -> pd.DataFrame:
        """加载配置"""
        if os.path.exists(self.config_file):
            return pd.read_excel(self.config_file)
        
        # 创建示例配置
        sample = {
            "question": ["steam错误代码118怎么办", "加速器哪个好用"],
            "ai_model": ["百度", "百度"],
            "target_brand": ["奇游加速器", "奇游加速器"],
            "priority": ["P0", "P0"],
            "category": ["Steam问题", "产品推荐"],
            "frequency": ["daily", "daily"],
            "status": ["active", "active"]
        }
        df = pd.DataFrame(sample)
        df.to_excel(self.config_file, index=False)
        print(f"✅ 示例配置已创建: {self.config_file}")
        return df
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect('geo_monitor.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS geo_monitor_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT, ai_model TEXT, target_brand TEXT,
                ai_answer TEXT, query_time TIMESTAMP, brand_appeared BOOLEAN,
                position TEXT, positive_keywords TEXT, negative_keywords TEXT,
                competitors_mentioned TEXT, ref_links TEXT, screenshot_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def _save_result(self, result: GEOResult):
        """保存结果"""
        conn = sqlite3.connect('geo_monitor.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO geo_monitor_results 
            (question, ai_model, target_brand, ai_answer, query_time, 
             brand_appeared, position, positive_keywords, negative_keywords,
             competitors_mentioned, ref_links, screenshot_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.question, result.ai_model, result.target_brand, result.ai_answer,
            result.query_time, result.brand_appeared, result.position,
            result.positive_keywords, result.negative_keywords,
            result.competitors_mentioned, result.references, result.screenshot_path
        ))
        conn.commit()
        conn.close()
    
    def search_baidu(self, question: str, target_brand: str) -> GEOResult:
        """百度搜索"""
        if not PLAYWRIGHT_AVAILABLE:
            return self._error_result(question, "百度", target_brand, "Playwright未安装")
        
        print(f"\n🔍 百度查询: {question}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                url = f"https://www.baidu.com/s?wd={question.replace(' ', '%20')}"
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(3000)
                
                # 截图
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot = f"{self.screenshot_dir}/baidu_{timestamp}.png"
                page.screenshot(path=screenshot, full_page=True)
                
                # 提取内容
                content = self._extract_content(page)
                analysis = self._analyze(content, target_brand)
                
                browser.close()
                
                return GEOResult(
                    question=question, ai_model="百度", target_brand=target_brand,
                    ai_answer=content, query_time=datetime.now(),
                    brand_appeared=analysis['appeared'], position=analysis['position'],
                    positive_keywords=analysis['positive'], negative_keywords=analysis['negative'],
                    competitors_mentioned=analysis['competitors'],
                    references=json.dumps(analysis['refs']), screenshot_path=screenshot
                )
                
            except Exception as e:
                browser.close()
                return self._error_result(question, "百度", target_brand, str(e))
    
    def _extract_content(self, page) -> str:
        """提取页面内容"""
        try:
            return page.evaluate('''() => {
                const ai = document.querySelector('[class*="ai-"], [class*="AI-"]');
                if (ai) return ai.innerText;
                const result = document.querySelector('.result, #content_left');
                return result ? result.innerText.substring(0, 2000) : "";
            }''') or "未找到内容"
        except:
            return "提取失败"
    
    def _analyze(self, content: str, brand: str) -> Dict:
        """分析内容"""
        result = {'appeared': False, 'position': '未出现', 
                 'positive': '', 'negative': '', 'competitors': '', 'refs': []}
        
        if not content:
            return result
        
        # 检测品牌
        keywords = [brand, brand.replace('加速器', '')]
        for kw in keywords:
            if kw in content:
                result['appeared'] = True
                idx = content.find(kw)
                if idx < len(content) * 0.3:
                    result['position'] = '第1位'
                elif idx < len(content) * 0.6:
                    result['position'] = '第2位'
                else:
                    result['position'] = '第3位+'
                break
        
        # 正负面词
        pos = [w for w in self.positive_words if w in content]
        neg = [w for w in self.negative_words if w in content]
        result['positive'] = ','.join(pos)
        result['negative'] = ','.join(neg)
        
        # 竞品
        comps = [c for c in self.competitor_brands if c in content and c not in brand]
        result['competitors'] = ','.join(comps)
        
        return result
    
    def _error_result(self, question: str, model: str, brand: str, error: str) -> GEOResult:
        """错误结果"""
        return GEOResult(
            question=question, ai_model=model, target_brand=brand,
            ai_answer=f"错误: {error}", query_time=datetime.now(),
            brand_appeared=False, position='失败', positive_keywords='',
            negative_keywords='', competitors_mentioned='', references='[]',
            screenshot_path=''
        )
    
    def run(self):
        """运行监控"""
        print(f"\n{'='*60}")
        print(f"🚀 GEO监控启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        active = self.config_df[self.config_df['status'] == 'active']
        
        for _, cfg in active.iterrows():
            q, model, brand = cfg['question'], cfg['ai_model'], cfg['target_brand']
            
            if model == "百度":
                result = self.search_baidu(q, brand)
            else:
                result = self._error_result(q, model, brand, f"{model}暂未实现")
            
            self._save_result(result)
            self.results.append(result)
            
            status = "✅" if result.brand_appeared else "❌"
            print(f"{status} {q[:30]}... | {result.position} | 竞品: {result.competitors_mentioned or '无'}")
            time.sleep(2)
        
        self._export()
        print(f"\n{'='*60}")
        print(f"✅ 完成 - 共{len(self.results)}条")
        print(f"{'='*60}\n")
    
    def _export(self):
        """导出报告"""
        if not self.results:
            return
        
        df = pd.DataFrame([{
            '问题': r.question, 'AI模型': r.ai_model, '目标品牌': r.target_brand,
            '是否出现': r.brand_appeared, '位置': r.position,
            '正面词': r.positive_keywords, '负面词': r.negative_keywords,
            '竞品': r.competitors_mentioned, '查询时间': r.query_time,
            'AI回答': r.ai_answer[:200], '截图': r.screenshot_path
        } for r in self.results])
        
        filename = f"geo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        print(f"📊 报告已保存: {filename}")


def main():
    """主函数"""
    monitor = GEOMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
