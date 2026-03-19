#!/bin/bash
# 小媒内容分块脚本
# 用途：将超长内容分割成安全块

set -e

MAX_LENGTH=160000  # 每块最大字符数

if [ $# -eq 0 ]; then
    echo "用法：chunk-content.sh <文件>"
    echo ""
    echo "将超长文件分割成 16 万字符的块"
    echo "输出：filename.chunk.1, filename.chunk.2, ..."
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "错误：文件不存在：$FILE"
    exit 1
fi

LENGTH=$(wc -c < "$FILE")

if [ $LENGTH -le $MAX_LENGTH ]; then
    echo "✓ 文件长度正常（$LENGTH 字符），无需分块"
    exit 0
fi

echo "文件长度：$LENGTH 字符"
echo "分块大小：$MAX_LENGTH 字符"
echo "预计块数：$(( (LENGTH + MAX_LENGTH - 1) / MAX_LENGTH ))"
echo ""

# 分块
split -b $MAX_LENGTH "$FILE" "${FILE}.chunk."

echo "✓ 分块完成："
ls -la "${FILE}.chunk."*

echo ""
echo "合并命令："
echo "  cat ${FILE}.chunk.* > ${FILE}.merged"
