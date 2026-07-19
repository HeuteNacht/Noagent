#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Noagent/dna/alias_to_path.py
#这是一个非常巧妙的工具脚本，用于在不读取 YAML 的情况下，直接从已有的 ~/.bashrc 别名中“逆向提取”主命令，并为其塑造成 PATH 物理文件。
'''
alias_to_path.py 与 install_path.sh 的职责重叠：
从架构上看，install_path.sh 已经非常完美地通过读取 YAML 蓝图，在 ~/.local/bin/ 下生成了包含 noa 在内的所有完整物理工具。而 alias_to_path.py 只是单向地去提取其中的 noa 别名。

建议：这个 Python 脚本更适合作为一个单兵作战时的快捷迁移小工具。在整体流式部署中，依靠 install.sh 直接调度生成的 install_path.sh 就已经能完全覆盖它的功能。
'''

# 动态锚定当前用户的 ~/.bashrc
import os, re, sys
bashrc_path = os.path.expanduser("~/.bashrc")
bin_dir = os.path.expanduser("~/.local/bin")
target_bin_path = os.path.join(bin_dir, "noa")

command_to_run = None
# 1. 打开并流式读取 .bashrc 文件
if os.path.exists(bashrc_path):
    with open(bashrc_path, "r", encoding="utf-8") as f:
        for line in f:
            # 🔍 利用正则表达式提取形如 alias noa='xxx' 内部捕获组中的核心物理命令
            match = re.search(r"^alias noa='(.*)'", line.strip())
            if match: command_to_run = match.group(1)# 提取成功

# 防御性断裂：如果在 .bashrc 中没找到主路由别名，直接以状态码 1 熔断退出
if not command_to_run: sys.exit(1)

# 2. 物理实体锻造
os.makedirs(bin_dir, exist_ok=True)
with open(target_bin_path, "w", encoding="utf-8") as f:
    # 动态反向写入物理 Wrapper 文件，同样采用 "$@" 承接全量动态输入参数
    f.write(f"#!/bin/bash\n# 🧬 物理路径转译器\n{command_to_run} \"$@\"\n")

# 3. 利用八进制权限控制符（0o755），相当于执行了 chmod 755，赋予该转译器完整的执行绿灯
os.chmod(target_bin_path, 0o755)
print(f"✅ [逆转录成功] 已生成物理实体: {target_bin_path}")
