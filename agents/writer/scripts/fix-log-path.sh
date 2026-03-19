#!/bin/bash
# fix-log-path.sh - 统一 AGFS 日志路径
# OmniPresence Agent Matrix - 3.12 宇宙

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 统一日志路径
LOG_DIR="$HOME/Documents/openclaw/logs"
LOG_FILE="$LOG_DIR/agfs.server.log"

echo -e "${GREEN}🔧 AGFS 日志路径统一化工具${NC}"
echo "================================"
echo ""

# 1. 创建统一日志目录
echo -e "${YELLOW}[1/4] 创建统一日志目录...${NC}"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    echo -e "  ✅ 创建目录: $LOG_DIR"
else
    echo -e "  ✅ 目录已存在: $LOG_DIR"
fi

# 2. 检查当前端点
echo -e "${YELLOW}[2/4] 检测当前端点...${NC}"
CURRENT_USER=$(whoami)
if [ "$CURRENT_USER" == "wh1ko" ]; then
    ENDPOINT="家里端 (MBP)"
    OLD_LOG="$HOME/.openviking/server.log"
elif [ "$CURRENT_USER" == "whiteareas" ]; then
    ENDPOINT="公司端 (Mac-mini)"
    OLD_LOG="$HOME/agfs.log"
else
    ENDPOINT="未知端点 ($CURRENT_USER)"
    OLD_LOG="$HOME/.openviking/server.log"
fi
echo -e "  📍 当前端点: $ENDPOINT"
echo -e "  📄 旧日志路径: $OLD_LOG"
echo -e "  📄 新日志路径: $LOG_FILE"

# 3. 迁移旧日志（如果存在）
echo -e "${YELLOW}[3/4] 迁移旧日志...${NC}"
if [ -f "$OLD_LOG" ]; then
    # 备份旧日志
    cp "$OLD_LOG" "$LOG_FILE.bak.$(date +%Y%m%d_%H%M%S)"
    echo -e "  ✅ 已备份旧日志"
    
    # 迁移内容
    cat "$OLD_LOG" >> "$LOG_FILE" 2>/dev/null || true
    echo -e "  ✅ 已迁移日志内容"
    
    # 创建软链接（可选）
    # ln -sf "$LOG_FILE" "$OLD_LOG"
    # echo -e "  ✅ 已创建软链接"
else
    echo -e "  ⚠️  旧日志不存在，跳过迁移"
fi

# 4. 创建日志轮转配置
echo -e "${YELLOW}[4/4] 配置日志轮转...${NC}"
LOGROTATE_CONF="$HOME/.openviking/logrotate.conf"
if [ ! -f "$LOGROTATE_CONF" ]; then
    cat > "$LOGROTATE_CONF" << 'EOF'
# AGFS 日志轮转配置
~/Documents/openclaw/logs/agfs.server.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644
}
EOF
    echo -e "  ✅ 创建日志轮转配置: $LOGROTATE_CONF"
else
    echo -e "  ✅ 日志轮转配置已存在"
fi

# 5. 输出配置指南
echo ""
echo -e "${GREEN}✅ 日志路径统一化完成！${NC}"
echo "================================"
echo ""
echo -e "📋 统一日志路径: ${GREEN}$LOG_FILE${NC}"
echo ""
echo -e "📝 后续操作指南:"
echo ""
echo "1. 启动 AGFS Server 时指定日志路径:"
echo -e "   ${YELLOW}~/.local/bin/agfs-server -c ~/.openviking/AGFS_GOLDEN_V1.yaml > $LOG_FILE 2>&1 &${NC}"
echo ""
echo "2. 查看日志:"
echo -e "   ${YELLOW}tail -f $LOG_FILE${NC}"
echo ""
echo "3. 日志轮转（每日自动）:"
echo -e "   ${YELLOW}logrotate ~/.openviking/logrotate.conf${NC}"
echo ""
echo "4. 清理旧日志（保留7天）:"
echo -e "   ${YELLOW}find $LOG_DIR -name '*.log' -mtime +7 -delete${NC}"
echo ""
echo "================================"
echo -e "${GREEN}🎉 完成！两端日志路径已统一。${NC}"
