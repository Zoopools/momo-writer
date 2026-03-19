#!/usr/bin/env python3
"""
图片压缩对比 - 生成原图和压缩图的对比页面
"""

import os
from PIL import Image

# 配置
OUTPUT_DIR = "/Users/wh1ko/Documents/openclaw/agents/hunter/bili_images"
COMPRESS_DIR = os.path.join(OUTPUT_DIR, "compressed")
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

print("📸 开始压缩图片对比...\n")

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
        
        # 压缩为 JPEG（质量 60）
        compress_file = img_info["file"].replace(".png", ".jpg")
        compress_path = os.path.join(COMPRESS_DIR, compress_file)
        
        # 转换为 RGB 模式（PNG 可能有透明通道）
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # 保存压缩版本
        img.save(compress_path, "JPEG", quality=60, optimize=True, progressive=True)
        
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
            "format": format
        })
        
        print(f"✅ {img_info['user']}")
        print(f"   原图：{original_size / 1024:.1f} KB")
        print(f"   压缩：{compress_size / 1024:.1f} KB")
        print(f"   节省：{save_rate:.1f}%")
        print()

# 计算总计
total_original = sum(s["original_size"] for s in stats)
total_compress = sum(s["compress_size"] for s in stats)
total_save_rate = (1 - total_compress / total_original) * 100

print("="*60)
print(f"📊 总计统计")
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
    <title>图片压缩效果对比</title>
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
        }}
        .user-name {{ font-size: 1.3em; font-weight: 600; }}
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
        <h1>📸 图片压缩效果对比</h1>
        <p class="subtitle">原图 vs 压缩图（质量 60%）</p>
        
        <div class="stats">
            <h2>📊 总体统计</h2>
            <div class="stats-grid">
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
                <div class="stat-card">
                    <div class="stat-number">{len(stats)}</div>
                    <div class="stat-label">图片数量</div>
                </div>
            </div>
        </div>
        
        <div class="comparison">
"""

for s in stats:
    html += f"""
            <div class="card">
                <div class="card-header">
                    <span class="user-name">@{s["user"]}</span>
                </div>
                <div class="card-body">
                    <div class="image-compare">
                        <div class="image-item">
                            <img src="{s["file"]}" alt="原图">
                            <div class="image-label">原图</div>
                            <div class="size-info">{s["original_size"] / 1024:.1f} KB</div>
                            <div class="size-info">{s["dimensions"]}</div>
                        </div>
                        <div class="image-item">
                            <img src="compressed/{s["compress_file"]}" alt="压缩图">
                            <div class="image-label">压缩图</div>
                            <div class="size-info">{s["compress_size"] / 1024:.1f} KB</div>
                            <div class="size-info">质量 60%</div>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <span class="save-badge">节省 {s["save_rate"]:.1f}%</span>
                    </div>
                </div>
            </div>
"""

html += f"""
        </div>
        
        <div class="footer">
            <p>🏹 Hunter-B 站评论 + 图片获取及在线访问 1.0</p>
            <p>💡 压缩质量：JPEG 60% | 优化：开启 | 渐进式：开启</p>
        </div>
    </div>
</body>
</html>
"""

# 保存对比 HTML
compare_html = os.path.join(OUTPUT_DIR, "压缩对比.html")
with open(compare_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ 对比页面已生成：{compare_html}")
print(f"\n🌐 本地打开：")
print(f"   file://{compare_html}")
