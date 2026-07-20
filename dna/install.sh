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
# 👇 [新增模块开始] 异构环境嗅探与 Miniconda 独立细胞核自动部署
# ========================================================
OS_TYPE=$(uname -s)
ARCH_TYPE=$(uname -m)
CONDA_DIR="$HOME/miniconda3"

if ! command -v conda &> /dev/null; then
    if [ -d "$CONDA_DIR" ]; then
        echo -e "\033[1;33m⚠️ 发现残留的 Miniconda 躯壳，但未激活。正在尝试强行唤醒...\033[0m"
    else
        echo -e "\033[1;33m⬇️ 侦测到原生 Linux 裸机环境 (防备 PEP 668 封锁)。\033[0m"
        echo -e "\033[1;32m📦 正在为你全自动下载并植入 Miniconda 独立细胞环境...\033[0m"
        
        if [ "$OS_TYPE" == "Linux" ]; then
            if [ "$ARCH_TYPE" == "x86_64" ]; then
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
            elif [ "$ARCH_TYPE" == "aarch64" ]; then
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
            fi
        elif [ "$OS_TYPE" == "Darwin" ]; then
            if [ "$ARCH_TYPE" == "arm64" ]; then
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
            else
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
            fi
        fi

        wget -q --show-progress "$MINICONDA_URL" -O /tmp/miniconda.sh
        bash /tmp/miniconda.sh -b -p "$CONDA_DIR"
        rm -f /tmp/miniconda.sh
        echo -e "\033[1;32m✅ Miniconda 物理躯壳植入完成！\033[0m"
    fi
    source "$CONDA_DIR/etc/profile.d/conda.sh"
else
    echo -e "\033[1;32m✅ Miniconda 突触节点已在线。\033[0m"
    CONDA_BASE=$(conda info --base)
    source "$CONDA_BASE/etc/profile.d/conda.sh"
fi

echo -e "\033[1;36m🔄 正在将 base 环境固化为系统默认反射弧...\033[0m"
conda init bash > /dev/null
conda config --set auto_activate_base true
conda activate base
echo -e "\033[1;32m🟢 已成功切入隔离细胞核环境 (base)！使用的 Python: $(which python3)\033[0m"
# ========================================================
# 👆 [新增模块结束]
# ========================================================


# evolve 1: 营养液依赖包自动灌溉机制 (PEP 668 环境自适应版)
if [ -f "$WORKSPACE/requirements.txt" ]; then
    echo "🧪 正在检测神经元环境健康状态..."
    
    # 尝试检测环境是否受限
    if pip3 install --dry-run . > /dev/null 2>&1; then
        echo "🧪 系统环境自由，开始直接灌溉..."
        pip3 install -r "$WORKSPACE/requirements.txt" --quiet
    else
        echo "🧪 侦测到受限环境 (PEP 668)，正在本地构建虚拟神经元环境..."
        VENV_DIR="$WORKSPACE/.venv"
        python3 -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        pip install -r "$WORKSPACE/requirements.txt" --quiet
        
        # 补丁：将激活后的 python 路径强制注入后续逻辑
        PYTHON_EXEC="$VENV_DIR/bin/python3"
        export NOA_PYTHON="$PYTHON_EXEC"
        echo "✅ 虚拟环境构建完毕，当前路由路径已重定向。"
    fi
fi

# 1. 唤醒 Python 逆转录引擎 (如果存在虚拟环境，使用指定的路径)
if [ -z "$NOA_PYTHON" ]; then
    python3 "$DNA_DIR/sync_receptors.py"
else
    "$NOA_PYTHON" "$DNA_DIR/sync_receptors.py"
fi


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
