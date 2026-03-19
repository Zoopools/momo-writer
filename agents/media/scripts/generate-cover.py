#!/usr/bin/env python3

import requests
import json
import base64

API_HOST = "sg.uiuiapi.com"
API_KEY = "sk-L4i8yqAoOpOKxTQwCXNW3RvZOdjEwInbkodfr8MqeWyjryjq"
MODEL = "gpt-4o-image"

# 定义图片生成的参数
PROMPT = "A professional tech tutorial cover image for OpenClaw local deployment. Main title \"OpenClaw\" in bold modern white text at the top. Subtitle \"本地部署完整指南\" in smaller white text below the main title. Tag \"手把手教学\" in small text at the bottom. Blue gradient background from #0F4C81 to #1E90FF. Visual elements: minimalist server icon on the left, AI assistant robot icon in the center, lock icon on the right. Clean, minimalist design. High contrast, publication ready. Professional tech style. Modern typography."
N = 1  # 生成数量
SIZE = "1536x1024"  # 图片大小（横向）

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
conn = requests.post(
    f"https://{API_HOST}/v1/chat/completions",
    json=payload,
    headers=headers
)

# 获取并打印响应
print(f"Status Code: {conn.status_code}")
print(f"Response:\n{conn.text}")

# 尝试解析响应
try:
    data = conn.json()
    print(f"\nParsed JSON:\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    
    # 提取图片数据
    if 'choices' in data and len(data['choices']) > 0:
        content = data['choices'][0].get('message', {}).get('content', '')
        
        # 查找图片数据
        if content and 'data:image' in content:
            # 提取 base64 数据
            header, b64_data = content.split(',', 1)
            image_bytes = base64.b64decode(b64_data)
            
            # 保存图片
            output_file = "/Users/wh1ko/Documents/openclaw/agents/media/outbox/openclaw-cover.png"
            with open(output_file, 'wb') as f:
                f.write(image_bytes)
            
            print(f"\n✅ 图片已保存到: {output_file}")
            print(f"✅ 图片大小: {len(image_bytes)} bytes")
        else:
            print(f"\n❌ 未找到图片数据")
            print(f"Content: {content[:500]}")
    else:
        print(f"\n❌ 响应中没有 choices")
        
except Exception as e:
    print(f"\n❌ 解析响应时出错: {e}")