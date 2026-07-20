#!/bin/bash
# 路径：~/Noagent/dna/install_alias.sh
# 职责：清理残骸并重植 ~/.bashrc 动态路由基因

DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")
RC_FILE="$HOME/.bashrc"

echo -e "📝 正在清理并重植 ~/.bashrc 动态路由基因 (Alias)..."

# 1. 精准清剿旧的致病基因
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/# Noagent Bionic Aliases/,$d' "$RC_FILE"
else
    sed -i '/# Noagent Bionic Aliases/,$d' "$RC_FILE"
    sed -i '/alias noa/d' "$RC_FILE"
    sed -i '/noa() {/d' "$RC_FILE"
fi

# 2. 纯净态基因注入 (使用单引号 'EOF' 完美冻结 "$@"，防止执行时被展开)
cat << 'EOF' >> "$RC_FILE"
# Noagent Bionic Aliases
noa() {
    bash 'NOA_DIR_PLACEHOLDER/noa_cli.sh' "$@" || python3 'NOA_DIR_PLACEHOLDER/noa_cli.py' "$@"
}
alias noa-tui='python3 NOA_DIR_PLACEHOLDER/local_tui.py'
alias noa-log='tail -f WORKSPACE_PLACEHOLDER/thalamus.log'
alias noa-approve='python3 NOA_DIR_PLACEHOLDER/device_manager.py'
EOF

# 3. 手术刀式路径填补
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|NOA_DIR_PLACEHOLDER|$DNA_DIR|g" "$RC_FILE"
    sed -i '' "s|WORKSPACE_PLACEHOLDER|$WORKSPACE|g" "$RC_FILE"
else
    sed -i "s|NOA_DIR_PLACEHOLDER|$DNA_DIR|g" "$RC_FILE"
    sed -i "s|WORKSPACE_PLACEHOLDER|$WORKSPACE|g" "$RC_FILE"
fi

echo -e "✅ Alias 别名与动态路由挂载成功！"
