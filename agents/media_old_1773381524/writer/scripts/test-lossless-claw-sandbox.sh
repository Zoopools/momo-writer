#!/bin/bash
# Lossless Claw 插件沙盒测试脚本
# 用途：在隔离环境中测试插件，不影响生产环境

set -e

SANDBOX_DIR="/tmp/openclaw-sandbox-lossless"
SANDBOX_PORT="18790"
PRODUCTION_PORT="18789"

echo "🧪 Lossless Claw 插件沙盒测试"
echo "================================"
echo ""

# 1. 清理旧沙盒
echo "🧹 清理旧沙盒..."
rm -rf $SANDBOX_DIR
mkdir -p $SANDBOX_DIR

# 2. 准备沙盒环境
echo "📦 准备沙盒环境..."

# 复制配置
cp ~/.openclaw/openclaw.json $SANDBOX_DIR/openclaw.json

# 复制插件目录（包含 lossless-claw）
if [ -d ~/.openclaw/plugins ]; then
    cp -r ~/.openclaw/plugins $SANDBOX_DIR/plugins
    echo "✅ 插件已复制"
else
    echo "⚠️  插件目录不存在，创建空目录"
    mkdir -p $SANDBOX_DIR/plugins
fi

# 3. 启用 lossless-claw 插件
echo "🔧 启用 lossless-claw 插件..."
python3 << PYTHON
import json

with open('$SANDBOX_DIR/openclaw.json', 'r') as f:
    config = json.load(f)

# 添加插件到 allow 列表
if 'lossless-claw' not in config['plugins']['allow']:
    config['plugins']['allow'].append('lossless-claw')

# 启用插件
config['plugins']['entries']['lossless-claw'] = {
    'enabled': True
}

with open('$SANDBOX_DIR/openclaw.json', 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("✅ 配置已更新")
PYTHON

# 4. 启动沙盒 Gateway
echo ""
echo "🚀 启动沙盒 Gateway (Port: $SANDBOX_PORT)..."
echo "📊 生产 Gateway (Port: $PRODUCTION_PORT) 不受影响"
echo ""
echo "⏳ 沙盒运行中... 按 Ctrl+C 停止"
echo ""

OPENCLAW_STATE=$SANDBOX_DIR \
  openclaw gateway start \
  --port $SANDBOX_PORT \
  --log-level debug

# 5. 清理
echo ""
echo "🧹 清理沙盒..."
rm -rf $SANDBOX_DIR
echo "✅ 沙盒已清理"
echo ""
echo "🎉 测试完成！"
