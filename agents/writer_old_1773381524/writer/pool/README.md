# 墨墨记忆池

**创建时间**: 2026-03-13
**Agent**: 墨墨 (writer)

## 目录说明

```
pool/
├── incoming/     # 待审查的记忆（从公司同步）
├── approved/     # 已批准的记忆
├── rejected/     # 已拒绝的记忆
├── shared/       # 共享知识
└── .last_sync    # 上次同步时间戳
```

## 使用方式

### 推送记忆（家里 → 公司）
```bash
bash ~/.openclaw/scripts/agent-pool-sync.sh writer push
```

### 拉取记忆（公司 → 家里）
```bash
bash ~/.openclaw/scripts/agent-pool-sync.sh writer pull
```

### 审查记忆
```bash
bash ~/.openclaw/scripts/agent-pool-sync.sh writer review
```

## 同步规则

- **自动同步**: SOUL.md, MEMORY.md, knowledge/
- **本地保留**: memory/（每日记忆）
- **审查机制**: 高风险记忆需人工确认

## 远程仓库

- **主仓库**: `git@github.com:Zoopools/momo-config.git`
- **同步分支**: main

---

*墨墨签名: 🖤*
