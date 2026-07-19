#!/bin/bash
#Noagent/dna/install_path.sh
# 🔗 [自动生成] 细胞受体挂载 (PATH Wrapper)
# 定义当前用户级的独立可执行二进制工具箱路径
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"

# ⚡ 利用 cat << 'EOF' 机制批量有丝分裂出独立的二进制 Wrapper 脚本
# 注意：使用单引号 'EOF' 可以锁定文本，防止 Bash 在生成文件时提前解析内部的 "$@" 变量
cat << 'EOF' > "$LOCAL_BIN/noa"
#!/bin/bash
# 完美透传：利用 "$@" 确保用户在终端输入的任何子命令或附加参数（如 noa start --force）均能无损投递
bash /home/hashi/Noagent/dna/noa_cli.sh "$@"
EOF
chmod +x "$LOCAL_BIN/noa"

# ---- 以下为同类型指令工具的无缝有丝分裂派生，逻辑完全对称 ----
cat << 'EOF' > "$LOCAL_BIN/noa-approve"
#!/bin/bash
python3 /home/hashi/Noagent/dna/device_manager.py "$@"
EOF
chmod +x "$LOCAL_BIN/noa-approve"
cat << 'EOF' > "$LOCAL_BIN/noa-log"
#!/bin/bash
tail -f /home/hashi/Noagent/thalamus.log "$@"
EOF
chmod +x "$LOCAL_BIN/noa-log"
cat << 'EOF' > "$LOCAL_BIN/noa-tui"
#!/bin/bash
python3 /home/hashi/Noagent/dna/local_tui.py "$@"
EOF
chmod +x "$LOCAL_BIN/noa-tui"
cat << 'EOF' > "$LOCAL_BIN/noa-install"
#!/bin/bash
bash /home/hashi/Noagent/dna/install.sh "$@"
EOF
chmod +x "$LOCAL_BIN/noa-install"

# 🔍 路径环境拓扑自检：如果发现宿主机的 $PATH 环境变量中还没包含这个本地工具箱，
# 则自动在 ~/.bashrc 中追加一条 export，确保指令可以在全域被直接唤醒
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi
echo -e "✅ 物理 PATH 工具挂载成功！"
