#!/bin/bash
# 路径：~/noa/dna/install.sh
# 职责：主控调度器 (数据驱动模式)

DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")

echo -e "\033[1;34m=============================================================\033[0m"
echo -e "🧬 \033[1;32mNoa 突触重构开始 (动态受体挂载引擎)...\033[0m"
echo -e "\033[1;34m=============================================================\033[0m"

# 1. 唤醒 Python 引擎，读取 yaml，同步生成两个 sh 挂载脚本
python3 "$DNA_DIR/sync_receptors.py"

# 2. 检查生成是否成功
if [ ! -f "$DNA_DIR/install_alias.sh" ] || [ ! -f "$DNA_DIR/install_path.sh" ]; then
    echo -e "❌ 致命错误：受体生成失败，停止有丝分裂。"
    exit 1
fi

# 3. 统一调用运行
bash "$DNA_DIR/install_alias.sh"
bash "$DNA_DIR/install_path.sh"

echo -e "\033[1;32m🎉 数据驱动架构部署完毕！\033[0m"
echo -e "🚀 已挂载的终端指令："
grep "alias " "$DNA_DIR/install_alias.sh" | awk -F "alias " '{print "  - " $2}' | awk -F "=" '{print $1}'
echo -e "\033[1;34m=============================================================\033[0m"
