#!/bin/bash
# 🧬 [自动生成] 体液受体挂载 (Alias & Smart Router)
RC_FILE="$HOME/.bashrc"
DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")

echo -e "📝 正在清理并重植 ~/.bashrc 基因..."

# 清理旧有的别名和函数定义
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/alias noa=/d; /noa() {/,/}/d; /alias noa-/d' "$RC_FILE"
else
    sed -i '/alias noa=/d; /noa() {/,/}/d; /alias noa-/d' "$RC_FILE"
fi

# 🧬 使用 EOF 动态注入，完美规避引号冲突，并动态适配当前用户路径
cat << EOF >> "$RC_FILE"

# >>> noa initialize >>>
noa() {
    bash '$DNA_DIR/noa_cli.sh' "\$@"
}
alias noa-approve='python3 $DNA_DIR/device_manager.py'
alias noa-log='tail -f $DNA_DIR/noa.log'
alias noa-tui='python3 $DNA_DIR/local_tui.py'
alias noa-install='python3 $DNA_DIR/sync_receptors.py'
# <<< noa initialize <<<
EOF

echo -e "✅ Alias 别名与动态路由挂载成功！"
echo -e "💡 提示: 若要让受体立即生效，请手动敲击: \033[1;33msource $RC_FILE\033[0m"
