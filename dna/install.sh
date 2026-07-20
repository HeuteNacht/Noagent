#!/bin/bash
# 路径：~/Noagent/dna/install.sh
# 职责：主控调度器 (环境隔离 + 依赖灌溉 + 分发挂载)

# 🧬 路径自锚定：精准捕获当前脚本执行时的真实绝对路径
DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")

# 🎨 渲染出充满工业科技感的 UI
echo -e "\033[1;34m=============================================================\033[0m"
echo -e "🧬 \033[1;32mNoa 突触重构开始 (动态受体挂载引擎)...\033[0m"
echo -e "\033[1;34m=============================================================\033[0m"

# ========================================================
# 👇 [极限修复] 自动检测/部署 Miniconda 虚拟环境并固化 base
# ========================================================
CONDA_DIR="$HOME/miniconda3"
export PIP_BREAK_SYSTEM_PACKAGES=1 # 🛡️ 异构系统兜底护盾

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
        
        # 🛡️ 增加对极简镜像 (如 Debian 13) 缺失 wget 的代偿突触
        if command -v curl &> /dev/null; then
            curl -sS -o /tmp/miniconda.sh "$MINICONDA_URL"
        else
            wget -q --show-progress "$MINICONDA_URL" -O /tmp/miniconda.sh
        fi

        bash /tmp/miniconda.sh -b -p "$CONDA_DIR"
        rm -f /tmp/miniconda.sh
        source "$CONDA_DIR/etc/profile.d/conda.sh"
        echo -e "✅ \033[1;32mMiniconda 物理躯壳植入完成！\033[0m"
    fi
    NOA_PIP_PATH="$CONDA_DIR/bin/pip3" # 物理锚定新环境的 pip
else
    CONDA_BASE=$(conda info --base)
    source "$CONDA_BASE/etc/profile.d/conda.sh"
    NOA_PIP_PATH="$CONDA_BASE/bin/pip3" # 物理锚定已有环境的 pip
fi

conda init bash > /dev/null 2>&1
conda config --set auto_activate_base true > /dev/null 2>&1
conda activate base

# 🛡️ 绝杀修复：强制刷新 Bash 指令路径缓存，切断跌落宿主系统的退路
hash -r

echo -e "🟢 \033[1;32m已成功切入隔离细胞核环境 (base)！当前 Python: $(which python3)\033[0m"
# ========================================================

# evolve 1: 营养液依赖包自动灌溉机制
if [ -f "$WORKSPACE/requirements.txt" ]; then
    echo "🧪 正在注入营养液依赖包 (pip install)..."
    # 🔒 绝对路径锁定：坚决不使用泛化的 pip3
    "$NOA_PIP_PATH" install -r "$WORKSPACE/requirements.txt" --quiet
fi

# ========================================================
# evolve 2: 双轨制受体挂载 (Alias + PATH)
# ========================================================
if [ -f "$DNA_DIR/install_alias.sh" ] && [ -f "$DNA_DIR/install_path.sh" ]; then
    # 确保子脚本具备执行权限
    chmod +x "$DNA_DIR/install_alias.sh" "$DNA_DIR/install_path.sh"
    
    bash "$DNA_DIR/install_alias.sh"
    bash "$DNA_DIR/install_path.sh"
else
    echo -e "❌ 致命错误：受体挂载引擎缺失，请确保 dna 目录下存在 install_alias.sh 与 install_path.sh"
    exit 1
fi

echo -e "\033[1;32m🎉 数据驱动架构部署完毕！\033[0m"
echo -e "💡 请执行 '\033[1;33msource ~/.bashrc\033[0m' 激活全局仿生超能力！"
echo -e "\033[1;34m=============================================================\033[0m"
