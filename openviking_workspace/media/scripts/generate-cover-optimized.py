#!/usr/bin/env python3

"""
生成 OpenClaw 部署教程封面图（优化文字可读性）
"""

import requests
import json
import base64

# 配置
API_HOST = "sg.uiuiapi.com"
API_KEY = "sk-L4i8yqAoOpOKxTQwCXNW3RvZOdjEwInbkodfr8MqeWyjryjq"
MODEL = "gpt-4o-image"

# 优化后的提示词 - 强调文字清晰可读
PROMPT = """Create a professional tech tutorial cover image for "OpenClaw 本地部署完整指南".

REQUIREMENTS:
- Use a clean, minimalist design
- Blue gradient background from #0F4C81 to #1E90FF
- Professional tech style

TEXT REQUIREMENTS (CRITICAL):
- DO NOT generate any text on the image. Keep the image clean.
- Use only visual elements: server icon, AI assistant robot icon, lock icon
- Make the icons simple and recognizable
- Leave space at the top, center, and bottom for text to be added in the editor later
- Ensure high contrast and clarity

SIZE: 1536x1024 pixels (landscape aspect ratio for WeChat cover)
STYLE: Professional, modern, minimalist
COLOR: Blue gradient background with white/light icons
"""

N = 1  # 生成数量
SIZE = "1536x1024"  # 图片大小（横向）

print("🎨 生成封面图（优化文字可读性版）...")
print("💡 策略：生成干净的图片，文字将在编辑器中手动添加，确保清晰可读")

# 构建请求的payload
payload = {
    "stream": False,
    "model": MODEL,
    "messages": [
        {
            "content": PROMPT,
            "role": "user"
        }
    ],
    "num_images": N,
    "size": SIZE
}

# 设置请求头
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

# 发送HTTP请求
try:
    print("📤 正在发送 API 请求...")
    conn = requests.post(
        f"https://{API_HOST}/v1/chat/completions",
        json=payload,
        headers=headers,
        timeout=60
    )

    print(f"✅ API 响应状态: {conn.status_code}")

    if conn.status_code == 200:
        data = conn.json()

        # 提取图片 URL
        if 'choices' in data and len(data['choices']) > 0:
            content = data['choices'][0].get('message', {}).get('content', '')

            # 查找图片 URL
            if '图片URL:' in content:
                image_url = content.split('图片URL:')[1].strip()
                print(f"🖼️ 图片 URL: {image_url}")

                # 下载图片
                print(f"⬇️  下载图片...")
                response = requests.get(image_url, timeout=60)

                if response.status_code == 200:
                    # 保存图片
                    output_file = "/Users/wh1ko/Documents/openclaw/agents/media/outbox/openclaw-cover-optimized.png"
                    with open(output_file, 'wb') as f:
                        f.write(response.content)

                    file_size = len(response.content)
                    print(f"✅ 图片已保存到: {output_file}")
                    print(f"✅ 图片大小: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
                    print(f"✅ 尺寸: 1536x1024（横向，适合微信公众号封面）")
                    print(f"\n💡 图片特点:")
                    print(f"   - 蓝色渐变背景 (#0F4C81 → #1E90FF)")
                    print(f"   - 简洁的图标（服务器、AI 助手、锁）")
                    print(f"   - 预留了文字区域（顶部、中间、底部）")
                    print(f"   - 高对比度，适合公众号封面")
                    print(f"\n📝 后续操作:")
                    print(f"   1. 打开微信公众号编辑器")
                    print(f"   2. 上传此封面图")
                    print(f"   3. 在编辑器中添加标题文字（保证清晰可读）")
                    print(f"   4. 发布文章")
                else:
                    print(f"❌ 下载图片失败: {response.status_code}")
            else:
                print(f"❌ 响应中没有图片 URL")
                print(f"Content: {content[:500]}")
        else:
            print(f"❌ 响应中没有 choices")
    else:
        print(f"❌ API 请求失败: {conn.status_code}")
        print(f"Response: {conn.text}")

except requests.exceptions.Timeout:
    print("❌ 请求超时（60秒），请重试")
except Exception as e:
    print(f"❌ 发生错误: {e}")

print("\n✨ 完成！")