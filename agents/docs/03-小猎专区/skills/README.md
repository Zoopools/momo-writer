# 小猎记忆池

**创建时间**: 2026-03-13
**Agent**: 小猎 (hunter)

## 目录说明

```
pool/
├── incoming/     # 待审查的记忆
├── approved/     # 已批准的记忆
├── rejected/     # 已拒绝的记忆
├── shared/       # 共享知识
└── .last_sync    # 上次同步时间戳
```

## 使用方式

### 推送记忆
```bash
bash ~/.openclaw/scripts/agent-pool-sync.sh hunter push
```

### 拉取记忆
```bash
bash ~/.openclaw/scripts/agent-pool-sync.sh hunter pull
```

### 审查记忆
```bash
bash ~/.openclaw/scripts/agent-pool-sync.sh hunter review
```

## 远程仓库

- **共享仓库**: `git@github.com:Zoopools/momo-config.git`
- **本地路径**: `~/Documents/openclaw/agents/hunter/`
- **同步目录**: `hunter/`

---

*小猎签名: 🏹*
