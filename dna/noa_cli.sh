#!/bin/bash
# ========================================================
#  1. 环境锚定与参数防御性清洗
# ========================================================
DNA_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORKSPACE=$(dirname "$DNA_DIR")
CMD=$(echo "$1" | sed 's/—/-/g')

# 🧬 【双轨制核心对齐】：使用与 noa_cli.py 完全相同的物理锁与日志路径
PID_FILE="$DNA_DIR/.brain.pid"
LOG_FILE="$DNA_DIR/noa.log"

# ========================================================
#  2. 神经清剿反射弧 (全泛型动态阻断)
# ========================================================
purge_existing_neural_processes() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo -e "🔄 正在执行督导树靶向阻断 (主 PID: $PID)..."
            kill -TERM "$PID" 2>/dev/null
            sleep 0.5
        fi
        rm -f "$PID_FILE"
    fi

    if pgrep -f "Noagent/brain/" >/dev/null 2>&1; then
        ORPHAN_COUNT=$(pgrep -f "Noagent/brain/" | wc -l)
        echo -e "🧹 扫描到活跃的游离脑区，正在执行外周清剿..."
        pkill -9 -f "Noagent/brain/" 2>/dev/null
        sleep 1
    fi

    # 强力解封已知端口段 (支持 22001 到 22020 的动态节点)
    for port in {22001..22020}; do
        fuser -k -9 ${port}/tcp >/dev/null 2>&1
    done
    echo -e "✅ 当前物理宿主机内存与网络端口已完全纯净。"
}

start_system() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo -e "⚠️ 基因锁 .brain.pid 存在且进程活跃，请先执行 noa stop！"
        exit 1
    fi
    echo -e "\033[1;34m=============================================================\033[0m"
    echo -e "⚡️ Noa ZMQ 分布式全脑起搏器点火 (Bash 极速模式)..."
    echo -e "\033[1;34m=============================================================\033[0m"
    nohup python3 "$WORKSPACE/main.py" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    sleep 1.5
    echo -e "✅ \033[1;32m神经中枢已在后台潜意识运行 (PID: $(cat $PID_FILE))！终端已释放。\033[0m"
}

# ========================================================
#  3. 多路意图分发引擎
# ========================================================
case "$CMD" in
    start)
        start_system
        ;;
    stop)
        purge_existing_neural_processes
        ;;
    restart)
        echo -e "🔄 正在执行全脑强制重启序列..."
        purge_existing_neural_processes
        sleep 1
        start_system
        ;;
    tui)
        python3 "$DNA_DIR/local_tui.py"
        ;;
    approve)
        python3 "$DNA_DIR/device_manager.py"
        ;;
    log)
        tail -f "$LOG_FILE"
        ;;
    install|evolve)
        python3 "$DNA_DIR/sync_receptors.py"
        ;;
    add)
        if [ "$2" == "cortex" ]; then
            python3 "$DNA_DIR/cortex_manager.py"
        else
            echo -e "⚠️ 基因指令错误。预期用法: noa add cortex"
        fi
        ;;
    *)
        echo -e "\033[1;32m🧠 Noa ZMQ Bionic AI System (Dual-Track Bash)\033[0m"
        echo "  noa start     - 唤醒集群 (一键拉起全脑区)"
        echo "  noa stop      - 精准休眠全系统"
        echo "  noa restart   - 🔄 强力绞杀游离进程并重启全脑"
        echo "  noa tui       - 💻 进入本地交互终端"
        echo "  noa log       - 📜 追踪系统底层日志"
        echo "  noa add cortex- 🧬 智能扫描并注册所有游离皮层"
        ;;
esac
