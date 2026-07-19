#!/bin/bash
#Noagent/dna/install_alias.sh
# 🧬 [自动生成] 体液受体挂载 (Alias)
# 定位当前用户 hashi 的 Bash 配置文件路径
BASHRC="$HOME/.bashrc"
# 🛡️ 幂等性清理：利用 sed 命令精准删除 ~/.bashrc 中历史残留的老旧 Noa 指令别名，防止多次重构导致文件无限膨胀
echo -e "📝 正在清理并重植 ~/.bashrc 别名基因..."
sed -i '/alias noa=/d' "$BASHRC"
sed -i '/alias noa-approve=/d' "$BASHRC"
sed -i '/alias noa-log=/d' "$BASHRC"
sed -i '/alias noa-tui=/d' "$BASHRC"
sed -i '/alias noa-install=/d' "$BASHRC"

# 🧬 基因写入：将劫持替换为绝对物理路径的 alias 指令，以追加（>>）形式永久注入 ~/.bashrc 底部
echo "alias noa='bash /home/hashi/Noagent/dna/noa_cli.sh'" >> "$BASHRC"
echo "alias noa-approve='python3 /home/hashi/Noagent/dna/device_manager.py'" >> "$BASHRC"
echo "alias noa-log='tail -f /home/hashi/Noagent/thalamus.log'" >> "$BASHRC"
echo "alias noa-tui='python3 /home/hashi/Noagent/dna/local_tui.py'" >> "$BASHRC"
echo "alias noa-install='bash /home/hashi/Noagent/dna/install.sh'" >> "$BASHRC"
echo -e "✅ Alias 别名挂载成功！"
