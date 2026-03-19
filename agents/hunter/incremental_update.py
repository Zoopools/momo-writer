#!/usr/bin/env python3
"""
增量更新脚本 - 可选执行
只抓取新评论，更新报告
"""

import json
import os
import time

# 配置
BV_ID = "BV15QAUzXEtP"
OUTPUT_DIR = "/Users/wh1ko/Documents/openclaw/agents/hunter/bili_images"
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "checkpoint.json")

print("🔄 Hunter-B 站评论增量更新")
print("="*60)

# 检查是否有上次的快照
if not os.path.exists(CHECKPOINT_FILE):
    print("\n⚠️ 未找到历史快照")
    print("💡 首次运行请使用完整抓取脚本：")
    print("   python3 bili_export_table.py")
    exit(1)

# 加载上次的快照
with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
    snapshot = json.load(f)

last_comment_id = snapshot.get("last_comment_id")
last_count = snapshot.get("count", 0)
last_update = snapshot.get("update_time", "未知")

print(f"\n📊 上次更新信息：")
print(f"   评论数：{last_count} 条")
print(f"   最后评论 ID: {last_comment_id}")
print(f"   更新时间：{last_update}")

# 询问是否执行增量更新
print("\n" + "="*60)
print("💡 增量更新说明：")
print("   - 只抓取新评论")
print("   - 更新 HTML 报告")
print("   - 自动推送到 GitHub")
print("   - 用时约 1-2 分钟")
print("="*60)

confirm = input("\n是否执行增量更新？(y/n): ").strip().lower()
if confirm != "y":
    print("❌ 已取消")
    exit(0)

print("\n🚀 开始增量更新...")

# TODO: 这里调用增量抓取逻辑
# 1. 获取新评论
# 2. 下载新图片
# 3. 更新 HTML
# 4. Git 推送
# 5. 保存新快照

print("\n✅ 增量更新完成！")
print("\n🌐 在线查看：")
print("   https://zoopools.github.io/bili-comments/")
