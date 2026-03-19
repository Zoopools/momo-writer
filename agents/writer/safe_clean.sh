#!/bin/zsh
echo "正在清理 OpenClaw 僵尸进程锁..."
find ~/.openclaw -name "*.lock" -type f -delete
echo "正在清理临时缓存..."
rm -rf ~/.openclaw/cache/*
echo "清理完成！Session 已保留，墨墨不会失忆。"
