#!/usr/bin/env python3
"""
智能图片压缩 - 根据图片类型选择最佳压缩策略
"""

import os
from PIL import Image

# 配置
OUTPUT_DIR = "/Users/wh1ko/Documents/openclaw/agents/hunter/bili_images"
COMPRESS_DIR = os.path.join(OUTPUT_DIR, "compressed_v2")
os.makedirs(COMPRESS_DIR, exist_ok=True)

# 原图列表
images = [
    {"file": "bili_BV15QAUzXEtP_1.jpg", "user": "鲍比烤迪克"},
    {"file": "bili_BV15QAUzXEtP_2.jpg", "user": "队友脚下火"},
    {"file": "bili_BV15QAUzXEtP_3.jpg", "user": "參悟自由的意義"},
    {"file": "bili_BV15QAUzXEtP_4.png", "user": "起语风"},
    {"file": "bili_BV15QAUzXEtP_5.jpg", "user": "赤瞳的夜刃"},
    {"file": "bili_BV15QAUzXEtP_6.jpg", "user": "阿拉斯苒"},
    {"file": "bili_BV15QAUzXEtP_7.png", "user": "Mad-Monk"},
]

print("📸 开始智能压缩...\n")

stats = []

for img_info in images:
    filepath = os.path.join(OUTPUT_DIR, img_info["file"])
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在：{filepath}")
        continue
    
    # 获取原图信息
    original_size = os.path.getsize(filepath)
    
    # 打开图片
    with Image.open(filepath) as img:
        width, height = img.size
        format = img.format
        mode = img.mode
        
        # 判断图片类型
        # 简单判断：小尺寸 + PNG = 可能是简单图形
        is_simple = (format == "PNG" and original_size < 50 * 1024)
        
        # 确定压缩策略
        if is_simple:
            # 简单图形：保持 PNG，使用优化
            compress_file = img_info["file"]
            compress_path = os.path.join(COMPRESS_DIR, compress_file)
            
            # PNG 优化（不转格式）
            img.save(compress_path, "PNG", optimize=True)
            strategy = "PNG 优化"
        else:
            # 照片：转 JPEG，质量 75
            compress_file = img_info["file"].replace(".png", ".jpg")
            compress_path = os.path.join(COMPRESS_DIR, compress_file)
            
            # 转 RGB 模式
            if mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # JPEG 压缩
            img.save(compress_path, "JPEG", quality=75, optimize=True, progressive=True)
            strategy = "JPEG 75%"
        
        # 获取压缩后大小
        compress_size = os.path.getsize(compress_path)
        
        # 计算压缩率
        save_rate = (1 - compress_size / original_size) * 100
        
        stats.append({
            "file": img_info["file"],
            "compress_file": compress_file,
            "user": img_info["user"],
            "original_size": original_size,
            "compress_size": compress_size,
            "save_rate": save_rate,
            "dimensions": f"{width}x{height}",
            "format": format,
            "strategy": strategy
        })
        
        status = "✅" if save_rate > 0 else "⚠️"
        print(f"{status} {img_info['user']}")
        print(f"   原图：{original_size / 1024:.1f} KB ({format})")
        print(f"   压缩：{compress_size / 1024:.1f} KB ({strategy})")
        if save_rate > 0:
            print(f"   节省：{save_rate:.1f}%")
        else:
            print(f"   增加：{abs(save_rate):.1f}% (保持原格式)")
        print()

# 计算总计
total_original = sum(s["original_size"] for s in stats)
total_compress = sum(s["compress_size"] for s in stats)
total_save_rate = (1 - total_compress / total_original) * 100

# 计算成功压缩的数量
success_count = sum(1 for s in stats if s["save_rate"] > 0)

print("="*60)
print(f"📊 智能压缩统计")
print(f"   图片总数：{len(stats)} 张")
print(f"   成功压缩：{success_count} 张")
print(f"   原图总计：{total_original / 1024:.1f} KB")
print(f"   压缩总计：{total_compress / 1024:.1f} KB")
print(f"   总节省：{total_save_rate:.1f}%")
print("="*60)

# 生成对比 HTML
html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能压缩效果对比</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
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
        .stats {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .stats h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 10px;
        }}
        .comparison {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .card-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .user-name {{ font-size: 1.3em; font-weight: 600; }}
        .strategy-badge {{
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
        }}
        .card-body {{ padding: 25px; }}
        .image-compare {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .image-item {{
            text-align: center;
        }}
        .image-item img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        .image-label {{
            margin-top: 10px;
            font-weight: 600;
            color: #333;
        }}
        .size-info {{
            margin-top: 5px;
            color: #666;
            font-size: 0.9em;
        }}
        .save-badge {{
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        .warn-badge {{
            display: inline-block;
            background: #f59e0b;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-top: 40px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📸 智能压缩效果对比</h1>
        <p class="subtitle">根据图片类型自动选择最佳压缩策略</p>
        
        <div class="stats">
            <h2>📊 总体统计</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(stats)}</div>
                    <div class="stat-label">图片总数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{success_count}</div>
                    <div class="stat-label">成功压缩</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_original / 1024:.1f} KB</div>
                    <div class="stat-label">原图总大小</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_compress / 1024:.1f} KB</div>
                    <div class="stat-label">压缩后总大小</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_save_rate:.1f}%</div>
                    <div class="stat-label">总体节省</div>
                </div>
            </div>
        </div>
        
        <div class="comparison">
"""

for s in stats:
    badge_class = "save-badge" if s["save_rate"] > 0 else "warn-badge"
    badge_text = f"节省 {s['save_rate']:.1f}%" if s["save_rate"] > 0 else f"增加 {abs(s['save_rate']):.1f}%"
    
    html += f"""
            <div class="card">
                <div class="card-header">
                    <span class="user-name">@{s["user"]}</span>
                    <span class="strategy-badge">{s["strategy"]}</span>
                </div>
                <div class="card-body">
                    <div class="image-compare">
                        <div class="image-item">
                            <img src="{s["file"]}" alt="原图">
                            <div class="image-label">原图</div>
                            <div class="size-info">{s["original_size"] / 1024:.1f} KB</div>
                            <div class="size-info">{s["dimensions"]} | {s["format"]}</div>
                        </div>
                        <div class="image-item">
                            <img src="compressed_v2/{s["compress_file"]}" alt="压缩图">
                            <div class="image-label">压缩图</div>
                            <div class="size-info">{s["compress_size"] / 1024:.1f} KB</div>
                            <div class="size-info">{s["strategy"]}</div>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <span class="{badge_class}">{badge_text}</span>
                    </div>
                </div>
            </div>
"""

html += f"""
        </div>
        
        <div class="footer">
            <p>🏹 Hunter-B 站评论 + 图片获取及在线访问 1.0 | 智能压缩版</p>
            <p>💡 压缩策略：</p>
            <p>   • 照片类 → JPEG 75% 质量</p>
            <p>   • 简单图形/文字 → PNG 优化（保持原格式）</p>
        </div>
    </div>
</body>
</html>
"""

# 保存对比 HTML
compare_html = os.path.join(OUTPUT_DIR, "智能压缩对比.html")
with open(compare_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ 对比页面已生成：{compare_html}")
print(f"\n🌐 本地打开：")
print(f"   file://{compare_html}")
