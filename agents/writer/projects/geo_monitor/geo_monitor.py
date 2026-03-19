#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO效果监控系统 v1.0
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
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import sqlite3

# 浏览器自动化
try:
    from playwright.sync_api import sync_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright未安装，请先运行: pip install playwright")
    print("⚠️  然后运行: playwright install chromium")


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
        """初始化监控器"""
        self.config_file = config_file
        self.config_df = self._load_config()
        self.results = []
        
        # 创建截图目录
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        # 竞品品牌库
        self.competitor_brands = [
            '迅游', '雷神', 'UU', '网易UU', '暴喵', 'biubiu',
            '海豚', '玲珑', '赛博', '鲜牛', '斧牛'
        ]
        
        # 正面关键词库
        self.positive_words = [
            '推荐', '好用', '稳定', '快速', '专业', '免费', 
            '优质', '首选', '最佳', '解决', '有效', '流畅',
            '低延迟', '不卡顿', '性价比高', '口碑好'
        ]
        
        # 负面关键词库
        self.negative_words = [
            '卡顿', '慢', '贵', '不好用', '问题', '错误',
            '失效', '不稳定', '掉线', '延迟高', '坑', '避雷'
        ]
        
        print(f"✅ GEO监控器初始化完成")
        print(f"📊 配置关键词数: {len(self.config_df)}")
    
    def _load_config(self) -> pd.DataFrame:
        """加载监控配置"""
        if os.path.exists(self.config_file):
            df = pd.read_excel(self.config_file)
            print(f"✅ 已加载配置文件: {self.config_file}")
            return df
        else:
            # 创建示例配置
            sample_config = {
                "question": [
                    "steam错误代码118怎么办",
                    "加速器哪个好用",
                    "游戏卡顿怎么解决"
                ],
                "ai_model": ["百度", "百度", "豆包"],
                "target_brand": ["奇游加速器", "奇游加速器", "奇游加速器"],
                "priority": ["P0", "P0", "P1"],
                "category": ["Steam问题", "产品推荐", "问题解决"],
                "frequency": ["daily", "daily", "daily"],
                "status": ["active", "active", "active"]
            }
            df = pd.DataFrame(sample_config)
            df.to_excel(self.config_file, index=False)
            print(f"✅ 示例配置已创建: {self.config_file}")
            return df
    
    def _init_database(self):
        """初始化SQLite数据库"""
        conn = sqlite3.connect('geo_monitor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS geo_monitor_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                ai_model TEXT,
                target_brand TEXT,
                ai_answer TEXT,
                query_time TIMESTAMP,
                brand_appeared BOOLEAN,
                position TEXT,
                positive_keywords TEXT,
                negative_keywords TEXT,
                competitors_mentioned TEXT,
                references TEXT,
                screenshot_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ 数据库初始化完成")
    
    def _save_to_database(self, result: GEOResult):
        """保存结果到数据库"""
        conn = sqlite3.connect('geo_monitor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO geo_monitor_results 
            (question, ai_model, target_brand, ai_answer, query_time, 
             brand_appeared, position, positive_keywords, negative_keywords,
             competitors_mentioned, references, screenshot_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.question, result.ai_model, result.target_brand,
            result.ai_answer, result.query_time, result.brand_appeared,
            result.position, result.positive_keywords, result.negative_keywords,
            result.competitors_mentioned, result.references, result.screenshot_path
        ))
        
        conn.commit()
        conn.close()
    
    def _create_error_result(self, question: str, ai_model: str, 
                            target_brand: str, error: str) -> GEOResult:
        """创建错误结果"""
        return GEOResult(
            question=question, ai_model=ai_model, target_brand=target_brand,
            ai_answer=f"错误: {error}", query_time=datetime.now(),
            brand_appeared=False, position='查询失败',
            positive_keywords='', negative_keywords='',
            competitors_mentioned='', references='[]', screenshot_path=''
        )
    
    def search_baidu(self, question: str, target_brand: str) -> GEOResult:
        """百度搜索AI摘要抓取"""
        if not PLAYWRIGHT_AVAILABLE:
            return self._create_error_result(question, "百度", target_brand, "Playwright未安装")
        
        print(f"\n🔍 查询百度: {question}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                # 搜索
                encoded_question = question.replace(" ", "%20")
                url = f"https://www.baidu.com/s?wd={encoded_question}"
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(3000)
                
                # 截图
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_file = f"{self.screenshot_dir}/baidu_{timestamp}.png"
                page.screenshot(path=screenshot_file, full_page=True)
                
                # 提取内容
                ai_summary = self._extract_baidu_content(page)
                analysis = self._analyze_content(ai_summary, target_brand)
                
                browser.close()
                
                return GEOResult(
                    question=question, ai_model="百度", target_brand=target_brand,
                    ai_answer=ai_summary, query_time=datetime.now(),
                    brand_appeared=analysis['brand_appeared'], position=analysis['position'],
                    positive_keywords=analysis['positive_keywords'],
                    negative_keywords=analysis['negative_keywords'],
                    competitors_mentioned=analysis['competitors_mentioned'],
                    references=json.dumps(analysis['references']),
                    screenshot_path=screenshot_file
                )
                
            except Exception as e:
                browser.close()
                return self._create_error_result(question, "百度", target_brand, str(e))
    
    def _extract_baidu_content(self, page) -> str:
        """提取百度AI摘要内容"""
        try:
            content = page.evaluate('''() => {
                const aiSection = document.querySelector('[class*="ai-"], [class*="AI-"]');
                if (aiSection) return aiSection.innerText;
                const result = document.querySelector('.result, #content_left