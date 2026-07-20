#!/bin/bash
# 路径：~/Noagent/dna/install_path.sh
# 职责：锻造物理 PATH 工具箱 (~/.local/bin)

DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")
LOCAL_BIN="$HOME/.local/bin"
RC_FILE="$HOME/.bashrc"

echo -e "🔗 正在注入物理 PATH 受体..."
mkdir -p "$LOCAL_BIN"

# 1. 挂载 noa 核心网关
cat << 'EOF' > "$LOCAL_BIN/noa"
#!/bin/bash
bash "NOA_DIR_PLACEHOLDER/noa_cli.sh" "$@" || python3 "NOA_DIR_PLACEHOLDER/noa_cli.py" "$@"
EOF

# 2. 挂载 noa-tui 子突触
cat << 'EOF' > "$LOCAL_BIN/noa-tui"
#!/bin/bash
python3 "NOA_DIR_PLACEHOLDER/local_tui.py" "$@"
EOF

# 3. 挂载 noa-log 子突触
cat << 'EOF' > "$LOCAL_BIN/noa-log"
#!/bin/bash
tail -f "WORKSPACE_PLACEHOLDER/thalamus.log" "$@"
EOF

# 4. 挂载 noa-approve 子突触
cat << 'EOF' > "$LOCAL_BIN/noa-approve"
#!/bin/bash
python3 "NOA_DIR_PLACEHOLDER/device_manager.py" "$@"
EOF

# 赋予执行权限并进行动态路径填补
chmod +x "$LOCAL_BIN/noa"*

if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|NOA_DIR_PLACEHOLDER|$DNA_DIR|g" "$LOCAL_BIN/noa"*
    sed -i '' "s|WORKSPACE_PLACEHOLDER|$WORKSPACE|g" "$LOCAL_BIN/noa"*
else
    sed -i "s|NOA_DIR_PLACEHOLDER|$DNA_DIR|g" "$LOCAL_BIN/noa"*
    sed -i "s|WORKSPACE_PLACEHOLDER|$WORKSPACE|g" "$LOCAL_BIN/noa"*
fi

# 校准宿主 PATH 寻路基因
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "\n# Noagent Bionic PATH" >> "$RC_FILE"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC_FILE"
fi

echo -e "✅ 物理 PATH 工具箱已融合！"
