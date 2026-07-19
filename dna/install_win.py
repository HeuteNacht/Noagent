#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Noagent/dna/install_win.py

import os
import sys
import subprocess

DNA_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(DNA_DIR)
CURRENT_PYTHON = sys.executable.replace('\\', '\\\\') # 转义物理路径中的斜杠

def print_ui(text, color_code="32"):
    print(f"\033[1;{color_code}m{text}\033[0m")

def main():
    print_ui("=============================================================", "34")
    print_ui("🧬 Noa 突触重构 - Windows 11 专属环境自适应挂载开始...")
    print_ui("=============================================================", "34")

    # 1. 自动定位 Windows 当前用户的 PowerShell Profile 路径
    # 模拟 PowerShell 中的 $PROFILE 变量
    user_home = os.path.expanduser("~")
    ps_profile_dir = os.path.join(user_home, "Documents", "WindowsPowerShell")
    ps_profile_path = os.path.join(ps_profile_dir, "Microsoft.PowerShell_profile.ps1")

    # 2. 锻造要注入的 Windows 仿生函数基因组 (完美支持参数透传 $args)
    # $args 相当于 Linux 中的 "$@"，确保 `noa start --force` 完美透传
    ps_functions = f"""
# ==========================================
# 🧠 Noa System - Windows 11 神经指令中心
# ==========================================
function noa {{ & "{CURRENT_PYTHON}" "{WORKSPACE}\\dna\\noa_cli.py" $args }}
function noa-approve {{ & "{CURRENT_PYTHON}" "{WORKSPACE}\\dna\\device_manager.py" $args }}
function noa-tui {{ & "{CURRENT_PYTHON}" "{WORKSPACE}\\dna\\local_tui.py" $args }}
function noa-log {{ powershell -Command "Get-Content '{WORKSPACE}\\dna\\noa.log' -Wait" }}
function noa-install {{ & "{CURRENT_PYTHON}" "{WORKSPACE}\\dna\\install_win.py" $args }}
"""

    try:
        # 3. 确保配置文件夹必须存在
        os.makedirs(ps_profile_dir, exist_ok=True)

        # 4. 幂等性清洗：如果之前注入过旧基因，先将其剔除
        existing_content = ""
        if os.path.exists(ps_profile_path):
            with open(ps_profile_path, "r", encoding="utf-8-sig") as f:
                existing_content = f.read()

        # 清洗旧指令
        cleaned_lines = []
        skip = False
        for line in existing_content.splitlines():
            if "# 🧠 Noa System" in line:
                skip = True
            if skip and "noa-install" in line:
                skip = False
                continue
            if not skip:
                cleaned_lines.append(line)

        # 5. 追加新基因落盘
        new_content = "\n".join(cleaned_lines) + "\n" + ps_functions.strip() + "\n"
        with open(ps_profile_path, "w", encoding="utf-8-sig") as f:
            f.write(new_content)

        print_ui(f"✅ 成功将神经命令刻录进物理骨架: {ps_profile_path}")
        
        # 6. 开启执行策略权限，防止 Windows 默认拦截自定义脚本
        print("🛡️ 正在向 Windows 申请策略解锁权限...")
        subprocess.run(["powershell", "-Command", "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"])

        print_ui("\n🎉 Windows 11 数据驱动架构部署完毕！", "32")
        print_ui("💡 请新开一个 PowerShell 窗口，或者敲击以下命令让超能力瞬间觉醒：", "33")
        print_ui("   . $PROFILE", "36")

    except Exception as e:
        print_ui(f"❌ 突触移植失败: {e}", "31")
    print_ui("=============================================================", "34")

if __name__ == "__main__":
    main()