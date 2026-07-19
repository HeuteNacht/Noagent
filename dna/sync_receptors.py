#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ========================================================
#  1. 物理坐标计算与依赖导入
# ========================================================
import yaml
import os
import stat

DNA_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(DNA_DIR)

YAML_PATH = os.path.join(DNA_DIR, "receptors.yaml")
ALIAS_SH_PATH = os.path.join(DNA_DIR, "install_alias.sh")
PATH_SH_PATH = os.path.join(DNA_DIR, "install_path.sh")

# ========================================================
#  2. 跨异构 Shell 的免疫嗅探
# ========================================================
def detect_host_shell() -> str:
    current_shell = os.environ.get("SHELL", "").lower()
    if "zsh" in current_shell:
        return ".zshrc"
    elif "fish" in current_shell:
        return ".config/fish/config.fish"
    else:
        return ".bashrc"

# ========================================================
#  3. 别名与函数挂载 (Mode A)
# ========================================================
def main():
    if not os.path.exists(YAML_PATH):
        print("❌ 未找到受体配置文件 receptors.yaml")
        return

    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    commands = data.get('commands', {})
    rc_file_name = detect_host_shell()
    
    alias_sh_content = [
        "#!/bin/bash",
        "# 🧬 [自动生成] 体液受体挂载 (Alias & Smart Router)",
        f"RC_FILE=\"$HOME/{rc_file_name}\"",
        f"echo -e \"📝 正在清理并重植 ~/{rc_file_name} 基因...\""
    ]
    
    # ⚡️ 跨平台底层内核防御与旧基因清洗
    for cmd_name, raw_cmd in commands.items():
        alias_sh_content.extend([
            'if [[ "$OSTYPE" == "darwin"* ]]; then',
            f'    sed -i \'\' \'/alias {cmd_name}=/d\' "$RC_FILE"',
            f'    sed -i \'\' \'/{cmd_name}() {{/d\' "$RC_FILE"', # 清洗旧的同名路由函数
            'else',
            f'    sed -i \'/alias {cmd_name}=/d\' "$RC_FILE"',
            f'    sed -i \'/{cmd_name}() {{/d\' "$RC_FILE"',
            'fi'
        ])
        
    # 🧬 动态基因逆转录
    for cmd_name, raw_cmd in commands.items():
        if "{SMART_ROUTER}" in raw_cmd:
            # 智能代偿函数：利用 bash 的逻辑或 (||)。若 sh 脚本报错或不存在，瞬间执行 py 脚本
            sh_target = os.path.join(DNA_DIR, "noa_cli.sh")
            py_target = os.path.join(DNA_DIR, "noa_cli.py")
            func_line = f"{cmd_name}() {{ bash '{sh_target}' \"$@\" || python3 '{py_target}' \"$@\"; }}"
            alias_sh_content.append(f"echo \"{func_line}\" >> \"$RC_FILE\"")
        else:
            actual_cmd = raw_cmd.replace("{WORKSPACE}", WORKSPACE)
            alias_sh_content.append(f"echo \"alias {cmd_name}='{actual_cmd}'\" >> \"$RC_FILE\"")
        
    alias_sh_content.append("echo -e \"✅ Alias 别名与动态路由挂载成功！\"")
    alias_sh_content.append(f"echo -e \"💡 提示: 若要让受体立即生效，请手动敲击: \\033[1;33msource $RC_FILE\\033[0m\"")

    # ========================================================
    #  4. 物理可执行工具挂载 (Mode B: PATH Wrapper 派生)
    # ========================================================
    path_sh_content = [
        "#!/bin/bash",
        "# 🔗 [自动生成] 细胞受体挂载 (PATH Wrapper)",
        "LOCAL_BIN=\"$HOME/.local/bin\"",
        "mkdir -p \"$LOCAL_BIN\""
    ]
    
    for cmd_name, raw_cmd in commands.items():
        target_bin = f"$LOCAL_BIN/{cmd_name}"
        
        if "{SMART_ROUTER}" in raw_cmd:
            # 锻造具备环境嗅探与降级代偿机制的物理 Wrapper
            sh_target = os.path.join(DNA_DIR, "noa_cli.sh")
            py_target = os.path.join(DNA_DIR, "noa_cli.py")
            smart_script = f"""#!/bin/bash
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    bash "{sh_target}" "$@" || {{
        echo -e "\\033[1;33m⚠️ Bash 反射弧执行阻断，已降级至 Python 皮层路由...\\033[0m"
        python3 "{py_target}" "$@"
    }}
else
    # 纯异构系统兜底
    python3 "{py_target}" "$@"
fi
"""
            path_sh_content.extend([
                f"cat << 'EOF' > \"{target_bin}\"",
                smart_script.strip(),
                "EOF",
                f"chmod +x \"{target_bin}\""
            ])
        else:
            actual_cmd = raw_cmd.replace("{WORKSPACE}", WORKSPACE)
            path_sh_content.extend([
                f"cat << 'EOF' > \"{target_bin}\"",
                "#!/bin/bash",
                f"{actual_cmd} \"$@\"",
                "EOF",
                f"chmod +x \"{target_bin}\""
            ])
    
    path_sh_content.extend([
        f"RC_FILE=\"$HOME/{rc_file_name}\"",
        "if [[ \":$PATH:\" != *\":$HOME/.local/bin:\"* ]]; then",
        "    echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> \"$RC_FILE\"",
        "fi",
        "echo -e \"✅ 物理 PATH 工具箱已与宿主融合！\""
    ])

    # ========================================================
    #  5. 执行权激活
    # ========================================================
    with open(ALIAS_SH_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(alias_sh_content) + "\n")
    os.chmod(ALIAS_SH_PATH, os.stat(ALIAS_SH_PATH).st_mode | stat.S_IEXEC)

    with open(PATH_SH_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(path_sh_content) + "\n")
    os.chmod(PATH_SH_PATH, os.stat(PATH_SH_PATH).st_mode | stat.S_IEXEC)

    print("✅ [配置解析完成] 已生成具备智能代偿路由的 install_alias.sh 与 install_path.sh")

if __name__ == "__main__":
    main()