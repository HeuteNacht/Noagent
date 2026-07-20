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


# ========================================================
# 👇 [新增模块] 自动检测/部署 Miniconda 虚拟环境并固化 base
# ========================================================
CONDA_DIR="$HOME/miniconda3"
export PIP_BREAK_SYSTEM_PACKAGES=1 # 🛡️ 终极护盾：允许在任何边缘状况下无条件绕过 PEP 668 阻断

if ! command -v conda &> /dev/null; then
    if [ -d "$CONDA_DIR" ]; then
        source "$CONDA_DIR/etc/profile.d/conda.sh"
    else
        echo -e "⬇️ \033[1;33m侦测到原生裸机环境，正在全自动下载并植入 Miniconda 独立细胞环境...\033[0m"
        ARCH_TYPE=$(uname -m)
        if [ "$ARCH_TYPE" == "x86_64" ]; then
            MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        else
            MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
        fi
        wget -q --show-progress "$MINICONDA_URL" -O /tmp/miniconda.sh
        bash /tmp/miniconda.sh -b -p "$CONDA_DIR"
        rm -f /tmp/miniconda.sh
        source "$CONDA_DIR/etc/profile.d/conda.sh"
        echo -e "✅ \033[1;32mMiniconda 物理躯壳植入完成！\033[0m"
    fi
else
    CONDA_BASE=$(conda info --base)
    source "$CONDA_BASE/etc/profile.d/conda.sh"
fi

conda init bash > /dev/null 2>&1
conda config --set auto_activate_base true > /dev/null 2>&1
conda activate base
echo -e "🟢 \033[1;32m已成功切入隔离细胞核环境 (base)！当前 Python: $(which python3)\033[0m"
# ========================================================


# evolve 1: 营养液依赖包自动灌溉机制 (requirements.txt 联动)
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

# 🔮 极客黑客流输出
grep "alias " "$DNA_DIR/install_alias.sh" | awk -F "alias " '{print "  - " $2}' | awk -F "=" '{print $1}'
echo -e "💡 请执行 'source ~/.bashrc' 或新开终端以激活全局仿生超能力！"
echo -e "\033[1;34m=============================================================\033[0m"
