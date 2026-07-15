#!/usr/bin/env python3
import os, re, sys
bashrc_path = os.path.expanduser("~/.bashrc")
bin_dir = os.path.expanduser("~/.local/bin")
target_bin_path = os.path.join(bin_dir, "noa")

command_to_run = None
if os.path.exists(bashrc_path):
    with open(bashrc_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(r"^alias noa='(.*)'", line.strip())
            if match: command_to_run = match.group(1)

if not command_to_run: sys.exit(1)

os.makedirs(bin_dir, exist_ok=True)
with open(target_bin_path, "w", encoding="utf-8") as f:
    f.write(f"#!/bin/bash\n# 🧬 物理路径转译器\n{command_to_run} \"$@\"\n")
os.chmod(target_bin_path, 0o755)
print(f"✅ [逆转录成功] 已生成物理实体: {target_bin_path}")
