#!/bin/bash
# 🔗 [自动生成] 细胞受体挂载 (PATH Wrapper)
DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")

LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"

# 1. 动态生成主中枢指令 noa
cat << EOF > "$LOCAL_BIN/noa"
#!/bin/bash
if [[ "\$OSTYPE" == "linux-gnu"* ]] || [[ "\$OSTYPE" == "darwin"* ]]; then
    bash "$DNA_DIR/noa_cli.sh" "\$@"
else
    # 纯异构系统兜底
    python3 "$DNA_DIR/noa_cli.py" "\$@"
fi
EOF
chmod +x "$LOCAL_BIN/noa"

# 2. 动态生成审批受体指令 noa-approve
cat << EOF > "$LOCAL_BIN/noa-approve"
#!/bin/bash
python3 "$DNA_DIR/device_manager.py" "\$@"
EOF
chmod +x "$LOCAL_BIN/noa-approve"

# 3. 动态生成日志追踪指令 noa-log
cat << EOF > "$LOCAL_BIN/noa-log"
#!/bin/bash
tail -f "$DNA_DIR/noa.log" "\$@"
EOF
chmod +x "$LOCAL_BIN/noa-log"

# 4. 动态生成 TUI 终端指令 noa-tui
cat << EOF > "$LOCAL_BIN/noa-tui"
#!/bin/bash
python3 "$DNA_DIR/local_tui.py" "\$@"
EOF
chmod +x "$LOCAL_BIN/noa-tui"

# 5. 动态生成受体同步指令 noa-install
cat << EOF > "$LOCAL_BIN/noa-install"
#!/bin/bash
python3 "$DNA_DIR/sync_receptors.py" "\$@"
EOF
chmod +x "$LOCAL_BIN/noa-install"

# 6. 将物理路径注入环境变量
RC_FILE="$HOME/.bashrc"
if [[ ":\$PATH:" != *":\$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC_FILE"
fi

echo -e "✅ 物理 PATH 工具箱已与宿主融合！"
