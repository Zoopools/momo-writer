#!/bin/zsh
# 用法: ./init_agent_soul.sh [agent_name]
AGENT_NAME=$1

if [ -z "$AGENT_NAME" ]; then
    echo "❌ 请输入 Agent 名称 (例如: writer, hunter, media)"
    exit 1
fi

echo "🚀 正在为 Agent [$AGENT_NAME] 建立分布式灵魂链接..."

# 1. 在 Git 工作区创建持久化目录
DEST_DIR="~/Documents/openclaw/openviking_workspace/backups/agents_memory/$AGENT_NAME"
eval mkdir -p $DEST_DIR

# 2. 确保配置目录存在
eval mkdir -p ~/.openclaw/agents/$AGENT_NAME

# 3. 迁移并建立软链接
# 如果原路径是目录而非链接，则迁移；否则跳过
SOURCE_DIR="~/.openclaw/agents/$AGENT_NAME/sessions"
if [ -d "$SOURCE_DIR" ] && [ ! -L "$SOURCE_DIR" ]; then
    eval mv $SOURCE_DIR $DEST_DIR/
fi

eval ln -sfn $DEST_DIR/sessions $SOURCE_DIR

# 4. 拷贝指挥官档案，确保身份认同
eval cp ~/Documents/openclaw/openviking_workspace/media/knowledge/commander.md ~/.openclaw/agents/$AGENT_NAME/agent/media/knowledge/ 2>/dev/null

echo "✅ Agent [$AGENT_NAME] 已成功接入全域同步系统！"
