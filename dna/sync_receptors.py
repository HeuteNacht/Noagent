#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import os
import stat

DNA_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(DNA_DIR)
YAML_PATH = os.path.join(DNA_DIR, "receptors.yaml")
ALIAS_SH_PATH = os.path.join(DNA_DIR, "install_alias.sh")
PATH_SH_PATH = os.path.join(DNA_DIR, "install_path.sh")

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
    
    # 先清理旧的同名 alias
    for cmd_name in commands.keys():
        alias_sh_content.append(f"sed -i '/alias {cmd_name}=/d' \"$BASHRC\"")
        
    # 写入新 alias
    for cmd_name, raw_cmd in commands.items():
        actual_cmd = raw_cmd.replace("{WORKSPACE}", WORKSPACE)
        alias_sh_content.append(f"echo \"alias {cmd_name}='{actual_cmd}'\" >> \"$BASHRC\"")
        
    alias_sh_content.append("echo -e \"✅ Alias 别名挂载成功！\"")


    # --- 构建 install_path.sh 内容 ---
    path_sh_content = [
        "#!/bin/bash",
        "# 🔗 [自动生成] 细胞受体挂载 (PATH Wrapper)",
        "LOCAL_BIN=\"$HOME/.local/bin\"",
        "mkdir -p \"$LOCAL_BIN\""
    ]
    
    for cmd_name, raw_cmd in commands.items():
        actual_cmd = raw_cmd.replace("{WORKSPACE}", WORKSPACE)
        target_bin = f"$LOCAL_BIN/{cmd_name}"
        # 生成包装脚本，并使用 "$@" 透传参数
        path_sh_content.extend([
            f"cat << 'EOF' > \"{target_bin}\"",
            "#!/bin/bash",
            f"{actual_cmd} \"$@\"",
            "EOF",
            f"chmod +x \"{target_bin}\""
        ])
    
    path_sh_content.extend([
        "if [[ \":$PATH:\" != *\":$HOME/.local/bin:\"* ]]; then",
        "    echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> \"$HOME/.bashrc\"",
        "fi",
        "echo -e \"✅ 物理 PATH 工具挂载成功！\""
    ])

    # 写入文件并赋予物理权限
    with open(ALIAS_SH_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(alias_sh_content) + "\n")
    os.chmod(ALIAS_SH_PATH, os.stat(ALIAS_SH_PATH).st_mode | stat.S_IEXEC)

    with open(PATH_SH_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(path_sh_content) + "\n")
    os.chmod(PATH_SH_PATH, os.stat(PATH_SH_PATH).st_mode | stat.S_IEXEC)

    print(f"✅ [配置解析完成] 已成功同步生成 install_alias.sh 与 install_path.sh")

if __name__ == "__main__":
    main()
