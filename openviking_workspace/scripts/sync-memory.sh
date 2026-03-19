#!/bin/bash
WORKSPACE_DIR="$HOME/Documents/openclaw/openviking_workspace"
SKILLS_LIST="$WORKSPACE_DIR/skills.list"
SKILLS_DIR="$HOME/.openclaw/skills"

cd "$WORKSPACE_DIR" || exit

# A. 灵魂同步
git pull origin main --rebase > /dev/null 2>&1

# B. 肉身对齐
CHANGE_OCCURRED=false
mkdir -p "$SKILLS_DIR"
if [ -f "$SKILLS_LIST" ]; then
    ACTIVE_SKILLS=$(grep -v '^#' "$SKILLS_LIST" | grep -v '^$' | cut -d'|' -f1)
    while IFS='|' read -r folder url; do
        [[ "$folder" =~ ^#.*$ || -z "$folder" ]] && continue
        if [ ! -d "$SKILLS_DIR/$folder" ]; then
            git clone --depth 1 "$url" "$SKILLS_DIR/$folder" && CHANGE_OCCURRED=true
        fi
    done < "$SKILLS_LIST"
    for local_folder in $(ls "$SKILLS_DIR"); do
        if [[ ! " $ACTIVE_SKILLS " =~ " $local_folder " ]]; then
            rm -rf "$SKILLS_DIR/$local_folder" && CHANGE_OCCURRED=true
        fi
    done
fi

# C. 自动推送变动
if [[ $(git status --porcelain) ]]; then
    git add .
    git commit -m "chore: 3.12 宇宙环境自动对齐 [$(date '+%H:%M')]"
    git push origin main && CHANGE_OCCURRED=true
fi
[ "$CHANGE_OCCURRED" = true ] && echo "✨ [$(date '+%H:%M:%S')] 宇宙已对齐并同步云端。" || echo "💤 状态一致。"
