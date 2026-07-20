#!/bin/bash
# 🧬 [自动生成] 体液受体挂载 (Alias & Smart Router)
RC_FILE="$HOME/.bashrc"
echo -e "📝 正在清理并重植 ~/.bashrc 基因..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/alias noa=/d' "$RC_FILE"
    sed -i '' '/noa() {/d' "$RC_FILE"
else
    sed -i '/alias noa=/d' "$RC_FILE"
    sed -i '/noa() {/d' "$RC_FILE"
fi
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/alias noa-approve=/d' "$RC_FILE"
    sed -i '' '/noa-approve() {/d' "$RC_FILE"
else
    sed -i '/alias noa-approve=/d' "$RC_FILE"
    sed -i '/noa-approve() {/d' "$RC_FILE"
fi
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/alias noa-log=/d' "$RC_FILE"
    sed -i '' '/noa-log() {/d' "$RC_FILE"
else
    sed -i '/alias noa-log=/d' "$RC_FILE"
    sed -i '/noa-log() {/d' "$RC_FILE"
fi
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/alias noa-tui=/d' "$RC_FILE"
    sed -i '' '/noa-tui() {/d' "$RC_FILE"
else
    sed -i '/alias noa-tui=/d' "$RC_FILE"
    sed -i '/noa-tui() {/d' "$RC_FILE"
fi
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' '/alias noa-install=/d' "$RC_FILE"
    sed -i '' '/noa-install() {/d' "$RC_FILE"
else
    sed -i '/alias noa-install=/d' "$RC_FILE"
    sed -i '/noa-install() {/d' "$RC_FILE"
fi
echo "noa() { bash '/home/hashi/Noagent/dna/noa_cli.sh' "$@" || python3 '/home/hashi/Noagent/dna/noa_cli.py' "$@"; }" >> "$RC_FILE"
echo "alias noa-approve='python3 /home/hashi/Noagent/dna/device_manager.py'" >> "$RC_FILE"
echo "alias noa-log='tail -f /home/hashi/Noagent/thalamus.log'" >> "$RC_FILE"
echo "alias noa-tui='python3 /home/hashi/Noagent/dna/local_tui.py'" >> "$RC_FILE"
echo "alias noa-install='python3 /home/hashi/Noagent/dna/install.py'" >> "$RC_FILE"
echo -e "✅ Alias 别名与动态路由挂载成功！"
echo -e "💡 提示: 若要让受体立即生效，请手动敲击: \033[1;33msource $RC_FILE\033[0m"
