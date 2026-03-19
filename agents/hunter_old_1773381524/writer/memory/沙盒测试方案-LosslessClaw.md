# Lossless Claw 插件沙盒测试方案

**测试目标**: 在隔离环境中测试 Lossless Claw 插件，不影响生产环境

**测试时间**: 2026-03-09 10:35 AM

---

## 🎯 测试策略

### 方案 A: 沙盒 Gateway 测试（推荐）

**原理**: 启动一个独立的沙盒 Gateway 实例，使用独立配置和数据库

**优点**:
- ✅ 完全隔离（不影响生产 Gateway）
- ✅ 独立数据库（不会污染生产数据）
- ✅ 可随时停止（不影响当前工作）
- ✅ 可重复测试

**端口**:
- 生产 Gateway: 18789
- 沙盒 Gateway: 18790

---

## 📋 测试步骤

### 1️⃣ 准备工作

```bash
# 创建沙盒测试目录
mkdir -p /tmp/openclaw-sandbox-lossless

# 复制当前配置
cp ~/.openclaw/openclaw.json /tmp/openclaw-sandbox-lossless/openclaw.json

# 复制插件（包含 lossless-claw）
cp -r ~/.openclaw/plugins /tmp/openclaw-sandbox-lossless/plugins
```

### 2️⃣ 修改沙盒配置

```bash
# 编辑沙盒配置，启用 lossless-claw
# 在 /tmp/openclaw-sandbox-lossless/openclaw.json 中添加：
{
  "plugins": {
    "allow": ["feishu-openclaw-plugin", "lossless-claw"],
    "entries": {
      "feishu-openclaw-plugin": {"enabled": true},
      "lossless-claw": {"enabled": true}
    }
  }
}
```

### 3️⃣ 启动沙盒 Gateway

```bash
OPENCLAW_STATE=/tmp/openclaw-sandbox-lossless \
  openclaw gateway start \
  --port 18790 \
  --log-level debug
```

### 4️⃣ 验证插件加载

```bash
# 查看沙盒 Gateway 日志
tail -f /tmp/openclaw-sandbox-lossless/logs/gateway.log | grep -i "lossless\|lcm"
```

**预期输出**:
```
[plugins] lossless-claw: Plugin loaded successfully
[lcm] Database initialized at /tmp/openclaw-sandbox-lossless/lcm.db
[lcm] Context engine ready
```

### 5️⃣ 测试对话

```bash
# 通过 WebUI 测试
open http://127.0.0.1:18790

# 或通过 API 测试
curl -X POST http://127.0.0.1:18790/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，测试 LCM 功能"}'
```

### 6️⃣ 检查功能

**测试项目**:
- [ ] 插件是否正常加载
- [ ] LCM 数据库是否创建
- [ ] 上下文管理是否正常工作
- [ ] 长对话是否自动压缩
- [ ] 历史消息是否可检索

### 7️⃣ 停止沙盒

```bash
# Ctrl+C 停止沙盒 Gateway
# 或
pkill -f "openclaw gateway.*18790"
```

### 8️⃣ 清理沙盒

```bash
rm -rf /tmp/openclaw-sandbox-lossless
```

---

## 📊 成功标准

| 检查项 | 预期结果 | 实际结果 |
|--------|---------|---------|
| 插件加载 | ✅ 无错误 | ⏳ 待测试 |
| 数据库创建 | ✅ lcm.db 生成 | ⏳ 待测试 |
| 上下文管理 | ✅ 正常工作 | ⏳ 待测试 |
| 自动压缩 | ✅ 达到阈值触发 | ⏳ 待测试 |
| 历史检索 | ✅ lcm_grep 可用 | ⏳ 待测试 |

---

## ⚠️ 注意事项

1. **沙盒隔离**: 沙盒 Gateway 使用独立配置和数据库，不影响生产
2. **端口占用**: 确保 18790 端口未被占用
3. **资源消耗**: 沙盒会占用额外内存（约 300-500MB）
4. **测试时间**: 建议测试 10-15 分钟，观察稳定性

---

## 🔄 回滚方案

如果测试失败：
```bash
# 1. 停止沙盒
pkill -f "openclaw gateway.*18790"

# 2. 清理沙盒
rm -rf /tmp/openclaw-sandbox-lossless

# 3. 生产环境不受影响
echo "✅ 生产 Gateway 正常运行（Port 18789）"
```

---

## 🖤 墨墨的建议

**推荐执行顺序**:
1. ✅ 先启动沙盒 Gateway
2. ✅ 观察插件加载日志
3. ✅ 进行短对话测试
4. ✅ 进行长对话测试（触发压缩）
5. ✅ 测试历史检索功能
6. ✅ 确认无问题后停止沙盒
7. ⏳ 如果一切正常，再考虑在生产环境安装

---

*创建时间：2026-03-09 10:35 AM*  
*创建者：墨墨 (writer)*
