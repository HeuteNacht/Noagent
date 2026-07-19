#!/bin/bash
# 🔗 [自动生成] 细胞受体挂载 (PATH Wrapper)
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"
cat << 'EOF' > "$LOCAL_BIN/noa"
#!/bin/bash
bash /home/hashi/Noagent/dna/noa_cli.sh "$@"
EOF
chmod +x "$LOCAL_BIN/noa"
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
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi
echo -e "✅ 物理 PATH 工具挂载成功！"
