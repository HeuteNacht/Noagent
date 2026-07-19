#!/bin/bash
# 路径：~/Noagent/dna/install.sh
# 职责：主控调度器 (数据驱动模式)

# 🧬 路径自锚定：精准捕获当前脚本执行时的真实绝对路径 ~/Noagent/dna
DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")

# 🎨 渲染出充满工业科技感的加粗蓝色与加粗绿色 UI
echo -e "\033[1;34m=============================================================\033[0m"
echo -e "🧬 \033[1;32mNoa 突触重构开始 (动态受体挂载引擎)...\033[0m"
echo -e "\033[1;34m=============================================================\033[0m"


# evolve 1: 营养液依赖包自动灌溉机制 (requirements.txt 联动)
#演进可能性：可以在主控 install.sh 的第 1 步之前，直接追加一行 Python 环境自检与依赖自动灌溉逻辑。
if [ -f "$WORKSPACE/requirements.txt" ]; then
    echo "🧪 正在注入营养液依赖包 (pip install)..."
    pip3 install -r "$WORKSPACE/requirements.txt" --quiet
fi

# 1. 唤醒 Python 逆转录引擎，去解析 receptors.yaml 蓝图并自动生成上面那两个物理 .sh 脚本
python3 "$DNA_DIR/sync_receptors.py"

# 2. 严格的基因完整性检查：如果发现那两个脚本没有被成功有丝分裂出来，立刻报警并强制阻断退出，防止破坏系统既有的环境变量
if [ ! -f "$DNA_DIR/install_alias.sh" ] || [ ! -f "$DNA_DIR/install_path.sh" ]; then
    echo -e "❌ 致命错误：受体生成失败，停止有丝分裂。"
    exit 1
fi

# 3. 统一顺序调用运行，先挂载体液别名，再建立物理可执行文件
bash "$DNA_DIR/install_alias.sh"
bash "$DNA_DIR/install_path.sh"

echo -e "\033[1;32m🎉 数据驱动架构部署完毕！\033[0m"
echo -e "🚀 已挂载的终端指令："

# 🔮 极客黑客流输出：利用 grep 抓取 install_alias.sh 中包含的物理别名，再配合两级 awk 管道动态剔除
# 杂质符号，最终干净利落地在控制台把刚刚部署好的全量系统指令整齐打印出来
grep "alias " "$DNA_DIR/install_alias.sh" | awk -F "alias " '{print "  - " $2}' | awk -F "=" '{print $1}'
echo -e "💡 请执行 'source ~/.bashrc' 或新开终端以激活全局仿生超能力！"
echo -e "\033[1;34m=============================================================\033[0m"
