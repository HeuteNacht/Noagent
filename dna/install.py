#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 环境自检与坐标锚定
# ========================================================
import os
import sys
import subprocess

DNA_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(DNA_DIR)
CURRENT_PYTHON = sys.executable

def print_ui(text, color_code="32"):
    """跨平台 ANSI 仿生终端渲染"""
    print(f"\033[1;{color_code}m{text}\033[0m")

def main():
    print_ui("=============================================================", "34")
    print_ui("🧬 Noa 突触重构开始 (跨平台动态受体挂载引擎)...")
    print_ui("=============================================================", "34")

    # ========================================================
    #  2. 营养液依赖包自动灌溉机制
    # ========================================================
    req_path = os.path.join(WORKSPACE, "requirements.txt")
    if os.path.exists(req_path):
        print("🧪 正在注入营养液依赖包 (pip install)...")
        subprocess.run([CURRENT_PYTHON, "-m", "pip", "install", "-r", req_path, "--quiet"])

    # ========================================================
    #  3. 唤醒逆转录引擎 (有丝分裂)
    # ========================================================
    print("🔄 正在解析 receptors.yaml 蓝图并派生物理受体...")
    sync_script = os.path.join(DNA_DIR, "sync_receptors.py")
    subprocess.run([CURRENT_PYTHON, sync_script])

    # ========================================================
    #  4. 宿主系统自适应挂载
    # ========================================================
    if sys.platform != "win32":
        # Linux / macOS (Debian 13 等) 的物理挂载
        alias_sh = os.path.join(DNA_DIR, "install_alias.sh")
        path_sh = os.path.join(DNA_DIR, "install_path.sh")
        
        if not os.path.exists(alias_sh) or not os.path.exists(path_sh):
            print_ui("❌ 致命错误：受体生成失败，停止有丝分裂。", "31")
            sys.exit(1)
            
        subprocess.run(["bash", alias_sh])
        subprocess.run(["bash", path_sh])
        
        print_ui("🎉 Unix 数据驱动架构部署完毕！")
        print_ui("💡 请执行 'source ~/.bashrc' (或 ~/.zshrc) 或新开终端以激活全局仿生超能力！", "33")
    else:
        # Windows 11 的物理挂载提示
        print_ui("🎉 Windows 环境部署完毕！", "32")
        print("💡 由于你在 Windows 11 环境下，请在 PowerShell 中执行以下命令挂载受体：")
        ps_profile_cmd = f"Set-Alias -Name noa -Value '{CURRENT_PYTHON} {WORKSPACE}\\dna\\noa_cli.py'"
        print_ui(f"   {ps_profile_cmd}", "36")
        
    print_ui("=============================================================", "34")

if __name__ == "__main__":
    main()