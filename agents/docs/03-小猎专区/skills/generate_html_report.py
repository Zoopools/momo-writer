#!/usr/bin/env python3
"""
B 站评论图片 - 生成 HTML 报告
本地查看，无需上传任何平台
"""

import json
import os
import time

# 数据
BV_ID = "BV15QAUzXEtP"
OUTPUT_DIR = "/Users/wh1ko/Documents/openclaw/agents/hunter/bili_images"

# 评论数据
comments = [
    {"user": "鲍比烤迪克", "comment": "有没有大佬帮忙翻译翻译是因为啥 [笑哭]", "file": "bili_BV15QAUzXEtP_1.jpg"},
    {"user": "队友脚下火", "comment": "之前可以正常玩，昨天突然出现这样的报错", "file": "bili_BV15QAUzXEtP_2.jpg"},
    {"user": "參悟自由的意義", "comment": "嘗試，還是這樣", "file": "bili_BV15QAUzXEtP_3.jpg"},
    {"user": "起语风", "comment": "有没有大佬知道这个怎么解决", "file": "bili_BV15QAUzXEtP_4.png"},
    {"user": "赤瞳的夜刃", "comment": "这又是什么问题报错，在线等很急", "file": "bili_BV15QAUzXEtP_5.jpg"},
    {"user": "阿拉斯苒", "comment": "这个是什么情况", "file": "bili_BV15QAUzXEtP_6.jpg"},
    {"user": "Mad-Monk", "comment": "按照 up 的指南从头到尾试了一遍，依然如此，游戏时长 50 分钟，满满的解密环节，可能跟我用的是网吧的电脑", "file": "bili_BV15QAUzXEtP_7.png"},
]

# 生成 HTML
html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B 站评论图片抓取 - {BV_ID}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: white;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .subtitle {{
            text-align: center;
            color: rgba(255,255,255,0.9);
            margin-bottom: 40px;
            font-size: 1.1em;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }}
        .card-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .user-name {{
            font-size: 1.3em;
            font-weight: 600;
        }}
        .comment-index {{
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        .card-body {{
            padding: 25px;
        }}
        .comment-text {{
            font-size: 1.1em;
            color: #333;
            line-height: 1.6;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .image-container {{
            text-align: center;
        }}
        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            cursor: pointer;
            transition: transform 0.3s ease;
        }}
        .image-container img:hover {{
            transform: scale(1.02);
        }}
        .image-info {{
            margin-top: 10px;
            color: #666;
            font-size: 0.9em;
        }}
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-top: 40px;
            padding: 20px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
        }}
        .stat-item {{
            background: rgba(255,255,255,0.2);
            padding: 15px 30px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: white;
        }}
        .stat-label {{
            color: rgba(255,255,255,0.9);
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📸 B 站评论图片抓取</h1>
        <p class="subtitle">BV 号：{BV_ID} | 生化危机 9 Crash 崩溃报错</p>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{len(comments)}</div>
                <div class="stat-label">条评论</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(comments)}</div>
                <div class="stat-label">张图片</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">100%</div>
                <div class="stat-label">原图画质</div>
            </div>
        </div>
"""

for i, c in enumerate(comments, 1):
    filepath = os.path.join(OUTPUT_DIR, c["file"])
    filesize = os.path.getsize(filepath) / 1024 if os.path.exists(filepath) else 0
    
    html += f"""
        <div class="card">
            <div class="card-header">
                <span class="user-name">@{c["user"]}</span>
                <span class="comment-index">评论 #{i}</span>
            </div>
            <div class="card-body">
                <div class="comment-text">
                    {c["comment"]}
                </div>
                <div class="image-container">
                    <img src="{filepath}" alt="{c["user"]} 的评论图片" onclick="window.open('{filepath}')">
                    <div class="image-info">📁 {c["file"]} | 📊 {filesize:.1f} KB</div>
                </div>
            </div>
        </div>
"""

html += """
        <div class="footer">
            <p>🏹 小猎 · 信息捕手 | 生成时间：""" + time.strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p>💡 点击图片可以全屏查看</p>
        </div>
    </div>
</body>
</html>
"""

# 添加 time 模块
import time

# 保存 HTML
output_file = os.path.join(OUTPUT_DIR, "B 站评论图片报告.html")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ HTML 报告已生成：{output_file}")
print(f"\n🌐 在浏览器中打开查看：")
print(f"   open \"{output_file}\"")
print(f"\n📁 共 {len(comments)} 条评论图片")
