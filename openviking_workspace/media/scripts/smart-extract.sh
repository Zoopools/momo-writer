#!/bin/bash
# smart-extract.sh - 智能网页内容提取脚本
# 用法：./smart-extract.sh <url> [type]
# type: google_news (默认), generic, article

set -e

URL="$1"
TYPE="${2:-google_news}"
OUTPUT="/tmp/web-extract-$(date +%s).md"
MAX_CHARS=150000

echo "🔍 智能提取网页内容..."
echo "URL: $URL"
echo "类型：$TYPE"
echo ""

# 使用 camofox 打开网页并提取内容
case $TYPE in
  google_news)
    echo "📰 提取 Google News 内容..."
    JS_CODE='() => {
  const title = document.title;
  const items = Array.from(document.querySelectorAll("a[role=\"heading\"]")).slice(0, 10);
  let result = `# ${title}\n\n## 最新资讯\n\n`;
  items.forEach((item, i) => {
    result += `${i+1}. ${item.textContent.trim()}\n`;
  });
  return result;
}'
    ;;
  
  generic)
    echo "🌐 提取通用网页内容..."
    JS_CODE='() => {
  const title = document.title;
  const paragraphs = Array.from(document.querySelectorAll("p")).slice(0, 3).map(p => p.textContent.trim());
  let result = `# ${title}\n\n## 内容摘要\n\n`;
  paragraphs.forEach(p => result += `${p}\n\n`);
  return result;
}'
    ;;
  
  article)
    echo "📄 提取文章内容..."
    JS_CODE='() => {
  const title = document.querySelector("h1")?.textContent || document.title;
  const content = document.querySelector("article")?.textContent || document.querySelector("[class*=\"content\"]")?.textContent || "";
  let result = `# ${title}\n\n`;
  result += content.substring(0, 50000);
  if (content.length > 50000) result += `\n\n*(内容较长，仅显示前 5 万字)*`;
  return result;
}'
    ;;
  
  *)
    echo "❌ 未知类型：$TYPE"
    echo "可用类型：google_news, generic, article"
    exit 1
    ;;
esac

# 使用 camofox 提取内容
echo "执行 JS 提取..."
TAB_ID=$(camofox_create_tab --url "$URL" 2>&1 | grep -oE 'tabId=[^ ]+' | cut -d= -f2)

if [ -z "$TAB_ID" ]; then
  echo "❌ 无法创建浏览器标签"
  exit 1
fi

echo "标签 ID: $TAB_ID"
sleep 3  # 等待页面加载

# 执行 JS 提取
CONTENT=$(camofox_evaluate --tab-id "$TAB_ID" --expression "$JS_CODE" 2>&1)

# 关闭标签
camofox_close_tab --tab-id "$TAB_ID" > /dev/null 2>&1

# 保存结果
echo "$CONTENT" > "$OUTPUT"

# 检查长度
CHAR_COUNT=$(echo "$CONTENT" | wc -c | tr -d ' ')
echo ""
echo "✅ 提取完成！"
echo "字符数：$CHAR_COUNT / $MAX_CHARS"

if [ "$CHAR_COUNT" -gt "$MAX_CHARS" ]; then
  echo "⚠️  内容超长，自动截断到 $MAX_CHARS 字符"
  echo "$CONTENT" | head -c "$MAX_CHARS" > "$OUTPUT"
  CHAR_COUNT=$(wc -c < "$OUTPUT" | tr -d ' ')
  echo "截断后字符数：$CHAR_COUNT"
fi

echo ""
echo "📁 输出文件：$OUTPUT"
echo ""
echo "📋 内容预览:"
echo "---"
head -20 "$OUTPUT"
echo "---"
echo ""
echo "💡 使用方法:"
echo "cat $OUTPUT  # 查看完整内容"
