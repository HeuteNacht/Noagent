#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/dna/sync_receptors.py
# ========================================================
#  1. 物理坐标计算与依赖导入
# ========================================================
import yaml
import os
# 导入文件权限状态常量库
import stat

# 精准计算 DNA 目录的绝对路径：~/Noagent/dna
DNA_DIR = os.path.dirname(os.path.abspath(__file__))
# 向上级回溯，完美锚定最新的物理根目录路径：~/Noagent
WORKSPACE = os.path.dirname(DNA_DIR)

# 动态定义配置文件、别名输出脚本、物理工具流输出脚本的物理路径
YAML_PATH = os.path.join(DNA_DIR, "receptors.yaml")
ALIAS_SH_PATH = os.path.join(DNA_DIR, "install_alias.sh")
PATH_SH_PATH = os.path.join(DNA_DIR, "install_path.sh")

# ========================================================
#  2. 别名受体挂载（Mode A: Alias 基因重植）
# ========================================================
def main():
    if not os.path.exists(YAML_PATH):
        print("❌ 未找到受体配置文件 receptors.yaml")
        return

    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    commands = data.get('commands', {})
    
    # --- 构建 install_alias.sh 内容 ---
    alias_sh_content = [
        "#!/bin/bash",
        "# 🧬 [自动生成] 体液受体挂载 (Alias)",
        "BASHRC=\"$HOME/.bashrc\"",
        "echo -e \"📝 正在清理并重植 ~/.bashrc 别名基因...\""
    ]
    
    # ⚡️ 幂等性清洗：遍历所有受体命令，利用 sed -i 正则匹配强行删除历史残留的同名别名，防止多次安装导致 .bashrc 臃肿过载
    for cmd_name in commands.keys():
        alias_sh_content.append(f"sed -i '/alias {cmd_name}=/d' \"$BASHRC\"")
        
    # 🧬 逆转录落盘：将 {WORKSPACE} 劫持替换为当前系统的真实绝对路径，并追加写回 ~/.bashrc
    for cmd_name, raw_cmd in commands.items():
        actual_cmd = raw_cmd.replace("{WORKSPACE}", WORKSPACE)
        alias_sh_content.append(f"echo \"alias {cmd_name}='{actual_cmd}'\" >> \"$BASHRC\"")
        
    alias_sh_content.append("echo -e \"✅ Alias 别名挂载成功！\"")

    # ========================================================
    #  3. 物理可执行工具挂载（Mode B: PATH Wrapper 派生）
    # ========================================================
    # --- 构建 install_path.sh 内容 ---
    path_sh_content = [
        "#!/bin/bash",
        "# 🔗 [自动生成] 细胞受体挂载 (PATH Wrapper)",
        "LOCAL_BIN=\"$HOME/.local/bin\"",
        "mkdir -p \"$LOCAL_BIN\""# 确保物理工具箱目录必然存在
    ]
    
    for cmd_name, raw_cmd in commands.items():
        actual_cmd = raw_cmd.replace("{WORKSPACE}", WORKSPACE)
        target_bin = f"$LOCAL_BIN/{cmd_name}"
        # ⚡ 极高明的参数透传包装：利用 cat << 'EOF' 生成不解析变量的 Bash 脚本
        # 末尾追加的 "$@" 是精髓所在！它保证了用户在任意路径输入 noa start --flag 时，后面的所有附加参数和物理参数能够无损透传给底层具体脑区
        path_sh_content.extend([
            f"cat << 'EOF' > \"{target_bin}\"",
            "#!/bin/bash",
            f"{actual_cmd} \"$@\"",
            "EOF",
            f"chmod +x \"{target_bin}\""# 赋予生成的物理包装程序可执行权限
        ])
    
    # 检查当前环境变量，若系统中没有 ~/.local/bin，则自动将该受体通道合并进入用户全域 PATH
    path_sh_content.extend([
        "if [[ \":$PATH:\" != *\":$HOME/.local/bin:\"* ]]; then",
        "    echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> \"$HOME/.bashrc\"",
        "fi",
        "echo -e \"✅ 物理 PATH 工具挂载成功！\""
    ])

    # ========================================================
    #  4. 物理有丝分裂执行权激活
    # ========================================================
    # 1. 物理写入 install_alias.sh 并利用位运算 `| stat.S_IEXEC` 动态追加 `chmod +x` 的操作系统物理执行权限
    with open(ALIAS_SH_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(alias_sh_content) + "\n")
    os.chmod(ALIAS_SH_PATH, os.stat(ALIAS_SH_PATH).st_mode | stat.S_IEXEC)

    with open(PATH_SH_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(path_sh_content) + "\n")
    os.chmod(PATH_SH_PATH, os.stat(PATH_SH_PATH).st_mode | stat.S_IEXEC)

    print(f"✅ [配置解析完成] 已成功同步生成 install_alias.sh 与 install_path.sh")

if __name__ == "__main__":
    main()
