#!/bin/bash
# start-chrome-debug.sh
# 启动 Chrome CDP 调试模式

# 第一步：彻底关闭 Chrome（重要！）
echo "🔒 关闭现有 Chrome..."
pkill -f "Google Chrome"
sleep 2

# 第二步：启动 Chrome CDP 模式
echo "🚀 启动 Chrome CDP 模式..."
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="$HOME/Library/Application Support/Google/ChromeDebug" &

# 第三步：等待并验证
echo "⏳ 等待 Chrome 启动..."
sleep 5

# 验证端口是否打开
if curl -s http://127.0.0.1:9222/json/version > /dev/null; then
    echo "✅ Chrome CDP 启动成功！"
    echo "📍 CDP URL: http://127.0.0.1:9222"
    echo "🔗 DevTools: http://127.0.0.1:9222"
else
    echo "❌ Chrome 启动失败！"
    exit 1
fi
