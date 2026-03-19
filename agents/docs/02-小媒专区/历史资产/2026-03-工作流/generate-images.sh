#!/bin/bash
# 小媒的信息图生成脚本
# 使用 DALL-E 3 生成杀戮尖塔 2 攻略信息图

CONTENT_DIR="/Users/wh1ko/Documents/openclaw/agents/media/outbox"
OUTPUT_DIR="$CONTENT_DIR/xhs-images/slay-the-spire-2-guide"

mkdir -p "$OUTPUT_DIR"

echo "🎨 小媒开始生成信息图..."

# 封面图提示词
COVER_PROMPT="小红书风格信息图封面，标题'杀戮尖塔 2 新手必知的 5 件事'，像素游戏风格，极简手绘线条，notion 风格，清新配色，1080x1920 竖版"

echo "生成封面图..."
# 这里调用 DALL-E 3 API
# dall-e-3 --prompt "$COVER_PROMPT" --output "$OUTPUT_DIR/01-cover.png"

echo "✅ 图片生成脚本准备完成"
echo "输出目录：$OUTPUT_DIR"
