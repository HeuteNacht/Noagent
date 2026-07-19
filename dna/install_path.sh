#!/bin/bash
# 🔗 [自动生成] 细胞受体挂载 (PATH Wrapper)
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"
cat << 'EOF' > "$LOCAL_BIN/noa"
#!/bin/bash
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    bash "D:\Arbeiten\Codes\Noagent\dna\noa_cli.sh" "$@" || {
        echo -e "\033[1;33m⚠️ Bash 反射弧执行阻断，已降级至 Python 皮层路由...\033[0m"
        python3 "D:\Arbeiten\Codes\Noagent\dna\noa_cli.py" "$@"
    }
else
    # 纯异构系统兜底
    python3 "D:\Arbeiten\Codes\Noagent\dna\noa_cli.py" "$@"
fi
EOF
chmod +x "$LOCAL_BIN/noa"
cat << 'EOF' > "$LOCAL_BIN/noa-approve"
#!/bin/bash
python3 D:\Arbeiten\Codes\Noagent/dna/device_manager.py "$@"
EOF
chmod +x "$LOCAL_BIN/noa-approve"
cat << 'EOF' > "$LOCAL_BIN/noa-log"
#!/bin/bash
tail -f D:\Arbeiten\Codes\Noagent/thalamus.log "$@"
EOF
chmod +x "$LOCAL_BIN/noa-log"
cat << 'EOF' > "$LOCAL_BIN/noa-tui"
#!/bin/bash
python3 D:\Arbeiten\Codes\Noagent/dna/local_tui.py "$@"
EOF
chmod +x "$LOCAL_BIN/noa-tui"
cat << 'EOF' > "$LOCAL_BIN/noa-install"
#!/bin/bash
python3 D:\Arbeiten\Codes\Noagent/dna/install.py "$@"
EOF
chmod +x "$LOCAL_BIN/noa-install"
RC_FILE="$HOME/.bashrc"
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC_FILE"
fi
echo -e "✅ 物理 PATH 工具箱已与宿主融合！"
